"""
Internship management routes (protected by JWT authentication)
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.internship import InternshipCreate, InternshipUpdate, InternshipResponse
from app.services.internship_service import InternshipService
from app.services.auth_service import get_current_user_id

router = APIRouter(prefix="/api/internships", tags=["Internships"])


@router.post("/", response_model=InternshipResponse, status_code=status.HTTP_201_CREATED)
async def create_internship(
    internship_data: InternshipCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create a new internship listing
    
    - **title**: Internship title
    - **company**: Company name
    - **domain**: Domain/field (e.g., Software Development, Data Science)
    - **required_skills**: List of required skills
    - **description**: Detailed description
    - **location**: Location (optional)
    - **duration**: Duration (optional)
    - **stipend**: Stipend amount (optional)
    
    **Requires authentication token in header**
    """
    internship_service = InternshipService()
    internship = await internship_service.create_internship(internship_data, current_user_id)
    return internship_service.internship_to_response(internship)


@router.get("/", response_model=List[InternshipResponse])
async def get_all_internships(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum records to return"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    company: Optional[str] = Query(None, description="Filter by company"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get all internship listings with optional filtering
    
    **Query Parameters:**
    - **skip**: Pagination offset (default: 0)
    - **limit**: Max results (default: 100)
    - **domain**: Filter by domain (optional)
    - **company**: Filter by company (optional)
    
    **Requires authentication token in header**
    """
    internship_service = InternshipService()
    internships = await internship_service.get_all_internships(
        skip=skip,
        limit=limit,
        domain=domain,
        company=company
    )
    
    return [
        internship_service.internship_to_response(internship)
        for internship in internships
    ]


@router.get("/{internship_id}", response_model=InternshipResponse)
async def get_internship(
    internship_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific internship by ID
    
    **Requires authentication token in header**
    """
    internship_service = InternshipService()
    internship = await internship_service.get_internship_by_id(internship_id)
    
    if not internship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internship not found"
        )
    
    return internship_service.internship_to_response(internship)


@router.put("/{internship_id}", response_model=InternshipResponse)
async def update_internship(
    internship_id: str,
    internship_data: InternshipUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Update an internship listing (only by the user who posted it)
    
    **Requires authentication token in header**
    """
    internship_service = InternshipService()
    internship = await internship_service.update_internship(
        internship_id,
        internship_data,
        current_user_id
    )
    
    if not internship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internship not found or you don't have permission to update it"
        )
    
    return internship_service.internship_to_response(internship)


@router.delete("/{internship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_internship(
    internship_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete an internship listing (only by the user who posted it)
    
    **Requires authentication token in header**
    """
    internship_service = InternshipService()
    deleted = await internship_service.delete_internship(internship_id, current_user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internship not found or you don't have permission to delete it"
        )
    
    return None