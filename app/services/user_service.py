"""
User service for business logic related to user operations
"""
from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from app.database.db import get_database
from app.models.user import UserCreate, UserUpdate, UserInDB, UserResponse
from app.services.auth_service import AuthService


class UserService:
    """Service class for user-related operations"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users
    
    async def create_user(self, user_data: UserCreate) -> UserInDB:
        """
        Create a new user
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user object
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user with email already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = AuthService.hash_password(user_data.password)
        
        # Prepare user document
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict.update({
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        # Insert into database
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        return UserInDB(**user_dict)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = await self.collection.find_one({"email": email})
        
        if not user:
            return None
        
        if not AuthService.verify_password(password, user["hashed_password"]):
            return None
        
        user["_id"] = str(user["_id"])
        return UserInDB(**user)
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """
        Get user by ID
        
        Args:
            user_id: User ID string
            
        Returns:
            User object if found, None otherwise
        """
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                return None
            
            user["_id"] = str(user["_id"])
            return UserInDB(**user)
            
        except Exception:
            return None
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserInDB]:
        """
        Update user profile
        
        Args:
            user_id: User ID string
            user_data: Updated user data
            
        Returns:
            Updated user object if successful, None otherwise
        """
        # Prepare update data (exclude None values)
        update_dict = user_data.model_dump(exclude_none=True)
        
        if not update_dict:
            # No fields to update
            return await self.get_user_by_id(user_id)
        
        update_dict["updated_at"] = datetime.utcnow()
        
        # Update in database
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get_user_by_id(user_id)
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Delete user account
        
        Args:
            user_id: User ID string
            
        Returns:
            True if deleted successfully, False otherwise
        """
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    def user_to_response(self, user: UserInDB) -> UserResponse:
        """
        Convert UserInDB to UserResponse (remove sensitive data)
        
        Args:
            user: User object from database
            
        Returns:
            User response object
        """
        return UserResponse(
            _id=user.id,
            name=user.name,
            email=user.email,
            skills=user.skills,
            projects=user.projects,
            created_at=user.created_at
        )