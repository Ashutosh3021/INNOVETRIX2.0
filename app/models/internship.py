"""
Internship data models and schemas using Pydantic
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime


class InternshipBase(BaseModel):
    """Base internship model with common fields"""
    title: str = Field(..., min_length=3, max_length=200)
    company: str = Field(..., min_length=2, max_length=100)
    domain: str = Field(..., min_length=2, max_length=100)
    required_skills: List[str] = Field(default_factory=list)
    description: str = Field(..., min_length=10, max_length=2000)
    location: Optional[str] = Field(None, max_length=100)
    duration: Optional[str] = Field(None, max_length=50)
    stipend: Optional[str] = Field(None, max_length=50)


class InternshipCreate(InternshipBase):
    """Model for creating a new internship"""
    
    @field_validator('required_skills')
    @classmethod
    def validate_skills(cls, v: List[str]) -> List[str]:
        """Ensure skills are not empty and clean duplicates"""
        if not v or len(v) == 0:
            raise ValueError('At least one required skill must be specified')
        
        # Remove empty strings and duplicates
        cleaned_skills = list(dict.fromkeys([s.strip() for s in v if s.strip()]))
        
        if not cleaned_skills:
            raise ValueError('At least one valid required skill must be specified')
        
        return cleaned_skills


class InternshipUpdate(BaseModel):
    """Model for updating an internship"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    company: Optional[str] = Field(None, min_length=2, max_length=100)
    domain: Optional[str] = Field(None, min_length=2, max_length=100)
    required_skills: Optional[List[str]] = None
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    location: Optional[str] = None
    duration: Optional[str] = None
    stipend: Optional[str] = None


class InternshipInDB(InternshipBase):
    """Internship model as stored in database"""
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    posted_by: str  # User ID who posted the internship
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439012",
                "title": "Backend Developer Intern",
                "company": "TechCorp",
                "domain": "Software Development",
                "required_skills": ["Python", "FastAPI", "MongoDB"],
                "description": "Looking for a backend developer intern...",
                "location": "Remote",
                "duration": "3 months",
                "stipend": "$500/month",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "posted_by": "507f1f77bcf86cd799439011"
            }
        }
    )


class InternshipResponse(InternshipBase):
    """Model for internship response"""
    id: str = Field(alias="_id")
    created_at: datetime
    location: Optional[str] = None
    duration: Optional[str] = None
    stipend: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True)


class MatchedInternship(InternshipResponse):
    """Internship with match score"""
    match_score: float = Field(..., ge=0.0, le=1.0)
    matched_skills: List[str] = Field(default_factory=list)
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439012",
                "title": "Backend Developer Intern",
                "company": "TechCorp",
                "domain": "Software Development",
                "required_skills": ["Python", "FastAPI", "MongoDB"],
                "description": "Looking for a backend developer intern...",
                "match_score": 0.85,
                "matched_skills": ["Python", "FastAPI"],
                "created_at": "2024-01-15T10:30:00"
            }
        }
    )