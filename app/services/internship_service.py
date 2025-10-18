"""
Internship service for business logic related to internship operations
"""
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from app.database.db import get_database
from app.models.internship import (
    InternshipCreate,
    InternshipUpdate,
    InternshipInDB,
    InternshipResponse
)


class InternshipService:
    """Service class for internship-related operations"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.internships
    
    async def create_internship(
        self,
        internship_data: InternshipCreate,
        user_id: str
    ) -> InternshipInDB:
        """
        Create a new internship listing
        
        Args:
            internship_data: Internship data
            user_id: ID of user creating the internship
            
        Returns:
            Created internship object
        """
        # Prepare internship document
        internship_dict = internship_data.model_dump()
        internship_dict.update({
            "posted_by": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        # Insert into database
        result = await self.collection.insert_one(internship_dict)
        internship_dict["_id"] = str(result.inserted_id)
        
        return InternshipInDB(**internship_dict)
    
    async def get_internship_by_id(self, internship_id: str) -> Optional[InternshipInDB]:
        """
        Get internship by ID
        
        Args:
            internship_id: Internship ID string
            
        Returns:
            Internship object if found, None otherwise
        """
        try:
            internship = await self.collection.find_one({"_id": ObjectId(internship_id)})
            
            if not internship:
                return None
            
            internship["_id"] = str(internship["_id"])
            return InternshipInDB(**internship)
            
        except Exception:
            return None
    
    async def get_all_internships(
        self,
        skip: int = 0,
        limit: int = 100,
        domain: Optional[str] = None,
        company: Optional[str] = None
    ) -> List[InternshipInDB]:
        """
        Get all internships with optional filtering
        
        Args:
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            domain: Filter by domain
            company: Filter by company
            
        Returns:
            List of internship objects
        """
        # Build query filter
        query = {}
        if domain:
            query["domain"] = {"$regex": domain, "$options": "i"}
        if company:
            query["company"] = {"$regex": company, "$options": "i"}
        
        # Query database
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        internships = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        result = []
        for internship in internships:
            internship["_id"] = str(internship["_id"])
            result.append(InternshipInDB(**internship))
        
        return result
    
    async def update_internship(
        self,
        internship_id: str,
        internship_data: InternshipUpdate,
        user_id: str
    ) -> Optional[InternshipInDB]:
        """
        Update an internship listing
        
        Args:
            internship_id: Internship ID string
            internship_data: Updated internship data
            user_id: ID of user updating the internship
            
        Returns:
            Updated internship object if successful, None otherwise
        """
        # Check if internship exists and user is the owner
        existing = await self.get_internship_by_id(internship_id)
        if not existing or existing.posted_by != user_id:
            return None
        
        # Prepare update data (exclude None values)
        update_dict = internship_data.model_dump(exclude_none=True)
        
        if not update_dict:
            return existing
        
        update_dict["updated_at"] = datetime.utcnow()
        
        # Update in database
        await self.collection.update_one(
            {"_id": ObjectId(internship_id)},
            {"$set": update_dict}
        )
        
        return await self.get_internship_by_id(internship_id)
    
    async def delete_internship(self, internship_id: str, user_id: str) -> bool:
        """
        Delete an internship listing
        
        Args:
            internship_id: Internship ID string
            user_id: ID of user deleting the internship
            
        Returns:
            True if deleted successfully, False otherwise
        """
        # Check if internship exists and user is the owner
        existing = await self.get_internship_by_id(internship_id)
        if not existing or existing.posted_by != user_id:
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(internship_id)})
        return result.deleted_count > 0
    
    def internship_to_response(self, internship: InternshipInDB) -> InternshipResponse:
        """
        Convert InternshipInDB to InternshipResponse
        
        Args:
            internship: Internship object from database
            
        Returns:
            Internship response object
        """
        return InternshipResponse(
            _id=internship.id,
            title=internship.title,
            company=internship.company,
            domain=internship.domain,
            required_skills=internship.required_skills,
            description=internship.description,
            location=internship.location,
            duration=internship.duration,
            stipend=internship.stipend,
            created_at=internship.created_at
        )