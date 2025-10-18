"""
User data models and schemas using Pydantic
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with common fields"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)


class UserCreate(UserBase):
    """Model for user registration"""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Model for updating user profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    skills: Optional[List[str]] = None
    projects: Optional[List[str]] = None


class UserInDB(UserBase):
    """User model as stored in database"""
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john@example.com",
                "skills": ["Python", "FastAPI", "Machine Learning"],
                "projects": ["E-commerce API", "ML Classification Model"],
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class UserResponse(UserBase):
    """Model for user response (without sensitive data)"""
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True


class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None