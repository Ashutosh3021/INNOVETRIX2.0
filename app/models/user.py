"""
User data models and schemas using Pydantic
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime
import re


class UserBase(BaseModel):
    """Base user model with common fields"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    username: Optional[str] = Field(None, description="Auto-generated unique username")
    role: Literal["student", "company", "admin"] = Field(default="student")
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    
    # Academic fields
    branch: Optional[str] = Field(None, description="Student branch (e.g., CSE, ECE, ME)")
    semester: Optional[int] = Field(None, ge=1, le=8, description="Current semester")
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0, description="Current CGPA")
    
    # New fields for enhanced profile
    certifications: List[str] = Field(default_factory=list, description="List of certifications")
    experience: Optional[str] = Field(None, description="Work experience details")
    languages: List[str] = Field(default_factory=list, description="Languages known")
    resume_url: Optional[str] = Field(None, description="Resume file URL")
    
    # Placement tracking
    placement_status: Optional[Literal["placed", "not_placed", "searching"]] = Field(None, description="Placement status")
    company_placed: Optional[str] = Field(None, description="Company where placed")
    salary_package: Optional[float] = Field(None, ge=0, description="Salary package in LPA")
    placement_type: Optional[Literal["internship", "job", "both"]] = Field(None, description="Type of placement")
    
    is_blocked: bool = Field(default=False, description="Whether user is blocked by admin")


class UserCreate(UserBase):
    """Model for user registration"""
    password: str = Field(..., min_length=8, max_length=72)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength:
        - At least 8 characters
        - Maximum 72 characters (bcrypt limitation)
        - Contains at least one letter
        - Contains at least one number
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if len(v) > 72:
            raise ValueError('Password cannot be longer than 72 characters (bcrypt limitation)')
        
        # Check byte length for bcrypt (72 byte limit)
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long when encoded. Please use a shorter password (max 72 bytes)')
        
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        
        return v
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v: List[str]) -> List[str]:
        """Clean and validate skills list (optional for companies)"""
        # Allow empty skills list (will be validated at service layer based on user type)
        if not v:
            return []
        
        # Remove empty strings and duplicates
        cleaned_skills = list(dict.fromkeys([s.strip() for s in v if s.strip()]))
        
        return cleaned_skills


class UserLogin(BaseModel):
    """Model for user login"""
    username_or_email: str = Field(..., description="Username or Email")
    password: str


class UserUpdate(BaseModel):
    """Model for updating user profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    skills: Optional[List[str]] = None
    projects: Optional[List[str]] = None
    branch: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=8)
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    certifications: Optional[List[str]] = None
    experience: Optional[str] = None
    languages: Optional[List[str]] = None
    resume_url: Optional[str] = None
    placement_status: Optional[Literal["placed", "not_placed", "searching"]] = None
    company_placed: Optional[str] = None
    salary_package: Optional[float] = Field(None, ge=0)
    placement_type: Optional[Literal["internship", "job", "both"]] = None


class UserInDB(UserBase):
    """User model as stored in database"""
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john@example.com",
                "username": "john_doe_2024",
                "role": "student",
                "skills": ["Python", "FastAPI", "Machine Learning"],
                "projects": ["E-commerce API", "ML Classification Model"],
                "branch": "CSE",
                "semester": 6,
                "cgpa": 8.5,
                "certifications": ["AWS Certified", "Google Cloud"],
                "experience": "2 years internship experience",
                "languages": ["English", "Hindi"],
                "resume_url": "/resumes/john_doe_resume.pdf",
                "placement_status": "placed",
                "company_placed": "Tech Corp",
                "salary_package": 12.5,
                "placement_type": "job",
                "is_blocked": False,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }
    )


class UserResponse(UserBase):
    """Model for user response (without sensitive data)"""
    id: str = Field(alias="_id")
    created_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )


class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None