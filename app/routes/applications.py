"""
Application routes for internship applications
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.application import (
    ApplicationCreate, ApplicationResponse, ApplicationStatus
)
from app.services.application_service import ApplicationService
from app.services.auth_service import get_current_user_id

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_internship(
    application_data: ApplicationCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Apply for an internship
    
    - **internship_id**: ID of the internship
    - **cover_letter**: Optional cover letter
    - **resume_url**: Optional resume URL
    
    **Requires authentication token**
    """
    app_service = ApplicationService()
    application = await app_service.create_application(application_data, current_user_id)
    
    # Return with internship details
    applications = await app_service.get_student_applications(current_user_id)
    for app in applications:
        if app.id == application.id:
            return app
    
    # Fallback
    return ApplicationResponse(
        _id=application.id,
        student_id=application.student_id,
        internship_id=application.internship_id,
        status=application.status,
        cover_letter=application.cover_letter,
        applied_at=application.applied_at,
        updated_at=application.updated_at
    )


@router.get("/my-applications", response_model=List[ApplicationResponse])
async def get_my_applications(
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get all applications submitted by the current user
    
    **Requires authentication token**
    """
    app_service = ApplicationService()
    return await app_service.get_student_applications(current_user_id)


@router.get("/company/all", response_model=List[ApplicationResponse])
async def get_company_applications(
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get all applications for all internships posted by the company
    
    **Requires authentication token** (company only)
    """
    app_service = ApplicationService()
    return await app_service.get_company_all_applications(current_user_id)


@router.get("/internship/{internship_id}", response_model=List[ApplicationResponse])
async def get_internship_applications(
    internship_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get all applications for an internship (company view)
    
    **Requires authentication token** (company only)
    """
    app_service = ApplicationService()
    return await app_service.get_internship_applications(internship_id, current_user_id)


@router.put("/{application_id}/status/{new_status}")
async def update_application_status(
    application_id: str,
    new_status: ApplicationStatus,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Update application status (company only)
    
    **Requires authentication token** (company only)
    """
    app_service = ApplicationService()
    application = await app_service.update_application_status(
        application_id, new_status, current_user_id
    )
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found or unauthorized"
        )
    
    return {"message": "Status updated successfully", "status": new_status}


@router.delete("/{application_id}")
async def withdraw_application(
    application_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Withdraw an application
    
    **Requires authentication token** (student only)
    """
    app_service = ApplicationService()
    success = await app_service.withdraw_application(application_id, current_user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    return {"message": "Application withdrawn successfully"}
