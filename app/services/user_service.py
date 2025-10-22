"""  
User service for business logic related to user operations
"""
from datetime import datetime
from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
import re
import random
from app.database.db import get_database, is_db_ready
from app.models.user import UserCreate, UserUpdate, UserInDB, UserResponse
from app.services.auth_service import AuthService


class UserService:
    """Service class for user-related operations"""
    
    def __init__(self):
        if not is_db_ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not ready. Please try again later."
            )
        self.db = get_database()
        if self.db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available."
            )
        self.collection = self.db.users
    
    async def generate_unique_username(self, name: str) -> str:
        """
        Generate a unique username from user's name
        Format: firstname_lastname_randomnumber
        
        Args:
            name: User's full name
            
        Returns:
            Unique username string
        """
        # Clean name: remove special chars, lowercase, split
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name.lower())
        parts = clean_name.split()
        
        # Create base username
        if len(parts) >= 2:
            base_username = f"{parts[0]}_{parts[-1]}"
        elif len(parts) == 1:
            base_username = parts[0]
        else:
            base_username = "user"
        
        # Keep trying until we find unique username
        max_attempts = 10
        for attempt in range(max_attempts):
            # Add random number suffix
            random_suffix = random.randint(1000, 9999)
            username = f"{base_username}_{random_suffix}"
            
            # Check if username already exists
            existing = await self.collection.find_one({"username": username})
            if not existing:
                return username
        
        # Fallback: use timestamp
        import time
        timestamp = int(time.time() * 1000) % 100000
        return f"{base_username}_{timestamp}"
    
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
        
        # Generate unique username
        username = await self.generate_unique_username(user_data.name)
        
        # Hash password
        hashed_password = AuthService.hash_password(user_data.password)
        
        # Prepare user document
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict.update({
            "username": username,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        # Insert into database
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        return UserInDB(**user_dict)
    
    async def authenticate_user(self, username_or_email: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate user with username/email and password
        
        Args:
            username_or_email: User's username or email
            password: User password
            
        Returns:
            User object if authentication successful, None otherwise
            
        Raises:
            HTTPException: If user is blocked
        """
        # Try to find user by email OR username
        user = await self.collection.find_one({
            "$or": [
                {"email": username_or_email},
                {"username": username_or_email}
            ]
        })
        
        if not user:
            return None
        
        # Check if user is blocked
        if user.get("is_blocked", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been blocked by the administrator. Please contact support."
            )
        
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
            
        Raises:
            HTTPException: If user_id format is invalid
        """
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid user ID format: {user_id}"
            )
        
        try:
            user = await self.collection.find_one({"_id": object_id})
            
            if not user:
                return None
            
            user["_id"] = str(user["_id"])
            return UserInDB(**user)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserInDB]:
        """
        Update user profile
        
        Args:
            user_id: User ID string
            user_data: Updated user data
            
        Returns:
            Updated user object if successful, None otherwise
            
        Raises:
            HTTPException: If user_id format is invalid or update data is empty
        """
        # Prepare update data (exclude None values)
        update_dict = user_data.model_dump(exclude_none=True)
        
        if not update_dict:
            # No fields to update - validate request
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No valid fields provided for update. Please provide at least one field to update."
            )
        
        # Validate ObjectId format
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid user ID format: {user_id}"
            )
        
        update_dict["updated_at"] = datetime.utcnow()
        
        # Update in database
        try:
            result = await self.collection.update_one(
                {"_id": object_id},
                {"$set": update_dict}
            )
            
            # Check if document was found (matched_count > 0)
            if result.matched_count == 0:
                return None
            
            return await self.get_user_by_id(user_id)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Delete user account
        
        Args:
            user_id: User ID string
            
        Returns:
            True if deleted successfully, False otherwise
            
        Raises:
            HTTPException: If user_id format is invalid
        """
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid user ID format: {user_id}"
            )
        
        try:
            result = await self.collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    
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
            username=user.username,
            role=user.role,
            skills=user.skills,
            projects=user.projects,
            branch=user.branch,
            semester=user.semester,
            cgpa=user.cgpa,
            certifications=user.certifications,
            experience=user.experience,
            languages=user.languages,
            resume_url=user.resume_url,
            placement_status=user.placement_status,
            company_placed=user.company_placed,
            salary_package=user.salary_package,
            placement_type=user.placement_type,
            is_blocked=user.is_blocked,
            created_at=user.created_at
        )