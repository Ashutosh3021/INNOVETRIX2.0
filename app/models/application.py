"""
Application data models for internship applications
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    """Application status enum"""
    PENDING = "pending"
    REVIEWING = "reviewing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ApplicationCreate(BaseModel):
    """Model for creating a new application"""
    internship_id: str = Field(..., description="ID of the internship being applied to")
    cover_letter: Optional[str] = Field(None, max_length=2000, description="Optional cover letter")
    resume_url: Optional[str] = Field(None, description="URL to resume/CV")


class ApplicationUpdate(BaseModel):
    """Model for updating application"""
    status: Optional[ApplicationStatus] = None
    cover_letter: Optional[str] = Field(None, max_length=2000)
    resume_url: Optional[str] = None


class ApplicationInDB(BaseModel):
    """Application model as stored in database"""
    id: str = Field(alias="_id")
    student_id: str
    internship_id: str
    status: ApplicationStatus
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    applied_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )


class ApplicationResponse(BaseModel):
    """Application response model with internship details"""
    id: str = Field(alias="_id")
    student_id: str
    internship_id: str
    internship_title: Optional[str] = None
    company_name: Optional[str] = None
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    status: ApplicationStatus
    cover_letter: Optional[str] = None
    applied_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )
