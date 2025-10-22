"""
Application service for managing internship applications
"""
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from app.database.db import get_database, is_db_ready
from app.models.application import (
    ApplicationCreate, ApplicationUpdate, ApplicationInDB, 
    ApplicationResponse, ApplicationStatus
)


class ApplicationService:
    """Service class for application-related operations"""
    
    def __init__(self):
        if not is_db_ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not ready"
            )
        self.db = get_database()
        if self.db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available"
            )
        self.collection = self.db.applications
        self.internships_collection = self.db.internships
    
    async def create_application(
        self, 
        application_data: ApplicationCreate, 
        student_id: str
    ) -> ApplicationInDB:
        """Create a new application"""
        # Check if student already applied
        existing = await self.collection.find_one({
            "student_id": student_id,
            "internship_id": application_data.internship_id
        })
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied to this internship"
            )
        
        # Verify internship exists
        try:
            internship_id = ObjectId(application_data.internship_id)
            internship = await self.internships_collection.find_one({"_id": internship_id})
            if not internship:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Internship not found"
                )
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid internship ID format"
            )
        
        # Create application
        app_dict = {
            "student_id": student_id,
            "internship_id": application_data.internship_id,
            "status": ApplicationStatus.PENDING,
            "cover_letter": application_data.cover_letter,
            "resume_url": application_data.resume_url,
            "applied_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(app_dict)
        app_dict["_id"] = str(result.inserted_id)
        
        return ApplicationInDB(**app_dict)
    
    async def get_student_applications(self, student_id: str) -> List[ApplicationResponse]:
        """Get all applications for a student"""
        cursor = self.collection.find({"student_id": student_id}).sort("applied_at", -1)
        applications = await cursor.to_list(length=100)
        
        # Enrich with internship details
        result = []
        for app in applications:
            app["_id"] = str(app["_id"])
            
            # Get internship details
            try:
                internship_id = ObjectId(app["internship_id"])
                internship = await self.internships_collection.find_one({"_id": internship_id})
                
                response = ApplicationResponse(
                    **app,
                    internship_title=internship.get("title") if internship else "Unknown",
                    company_name=internship.get("company") if internship else "Unknown"
                )
                result.append(response)
            except:
                # If internship not found, skip it
                continue
        
        return result
    
    async def get_internship_applications(
        self, 
        internship_id: str, 
        company_user_id: str
    ) -> List[ApplicationResponse]:
        """Get all applications for an internship (company view)"""
        # Verify internship belongs to company
        try:
            obj_id = ObjectId(internship_id)
            internship = await self.internships_collection.find_one({
                "_id": obj_id,
                "posted_by": company_user_id
            })
            
            if not internship:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Internship not found or unauthorized"
                )
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid internship ID"
            )
        
        cursor = self.collection.find({"internship_id": internship_id}).sort("applied_at", -1)
        applications = await cursor.to_list(length=100)
        
        result = []
        for app in applications:
            app["_id"] = str(app["_id"])
            result.append(ApplicationResponse(
                **app,
                internship_title=internship.get("title"),
                company_name=internship.get("company")
            ))
        
        return result
    
    async def update_application_status(
        self,
        application_id: str,
        new_status: ApplicationStatus,
        company_user_id: str
    ) -> Optional[ApplicationInDB]:
        """Update application status (company only)"""
        try:
            app_id = ObjectId(application_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid application ID"
            )
        
        # Get application
        application = await self.collection.find_one({"_id": app_id})
        if not application:
            return None
        
        # Verify internship belongs to company
        internship = await self.internships_collection.find_one({
            "_id": ObjectId(application["internship_id"]),
            "posted_by": company_user_id
        })
        
        if not internship:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to update this application"
            )
        
        # Update status
        result = await self.collection.update_one(
            {"_id": app_id},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count > 0:
            updated_app = await self.collection.find_one({"_id": app_id})
            updated_app["_id"] = str(updated_app["_id"])
            return ApplicationInDB(**updated_app)
        
        return None
    
    async def get_company_all_applications(self, company_user_id: str) -> List[ApplicationResponse]:
        """
        Get all applications for all internships posted by a company
        
        Args:
            company_user_id: ID of the company user
            
        Returns:
            List of all applications with internship details
        """
        # Get all internships posted by this company
        cursor = self.internships_collection.find({"posted_by": company_user_id})
        internships = await cursor.to_list(length=None)
        
        if not internships:
            return []
        
        # Get internship IDs
        internship_ids = [str(internship["_id"]) for internship in internships]
        
        # Create a map of internship details
        internship_map = {
            str(internship["_id"]): {
                "title": internship.get("title"),
                "company": internship.get("company")
            }
            for internship in internships
        }
        
        # Get all applications for these internships
        cursor = self.collection.find({
            "internship_id": {"$in": internship_ids}
        }).sort("applied_at", -1)
        
        applications = await cursor.to_list(length=None)
        
        # Enrich with internship details and student info
        result = []
        for app in applications:
            app["_id"] = str(app["_id"])
            internship_info = internship_map.get(app["internship_id"], {})
            
            # Get student details
            student_name = "Unknown Student"
            student_email = ""
            try:
                student_obj_id = ObjectId(app["student_id"])
                users_collection = self.db.users
                student = await users_collection.find_one({"_id": student_obj_id})
                if student:
                    student_name = student.get("name", "Unknown Student")
                    student_email = student.get("email", "")
            except:
                pass
            
            result.append(ApplicationResponse(
                **app,
                internship_title=internship_info.get("title", "Unknown"),
                company_name=internship_info.get("company", "Unknown"),
                student_name=student_name,
                student_email=student_email
            ))
        
        return result
    
    async def withdraw_application(
        self,
        application_id: str,
        student_id: str
    ) -> bool:
        """Withdraw application (student only)"""
        try:
            app_id = ObjectId(application_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid application ID"
            )
        
        result = await self.collection.update_one(
            {"_id": app_id, "student_id": student_id},
            {"$set": {"status": ApplicationStatus.WITHDRAWN, "updated_at": datetime.utcnow()}}
        )
        
        return result.modified_count > 0
