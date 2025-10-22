"""
Admin routes for administrative operations
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.services.admin_service import AdminService
from app.services.auth_service import get_current_user_id

router = APIRouter(prefix="/api/admin", tags=["Admin"])


async def verify_admin_access(current_user_id: str = Depends(get_current_user_id)) -> str:
    """
    Verify that the current user has admin access
    
    Returns:
        User ID if admin, raises HTTPException otherwise
    """
    admin_service = AdminService()
    is_admin = await admin_service.verify_admin(current_user_id)
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user_id


@router.get("/analytics/overview", response_model=Dict[str, Any])
async def get_analytics_overview(admin_id: str = Depends(verify_admin_access)):
    """
    Get comprehensive analytics overview
    
    Returns system-wide statistics including:
    - Total students, companies, internships, applications
    - Application status breakdown
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_analytics_overview()


@router.get("/analytics/students-by-branch", response_model=List[Dict[str, Any]])
async def get_students_by_branch(admin_id: str = Depends(verify_admin_access)):
    """
    Get student statistics grouped by branch
    
    Returns count and average CGPA for each branch
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_students_by_branch()


@router.get("/analytics/students-by-semester", response_model=List[Dict[str, Any]])
async def get_students_by_semester(admin_id: str = Depends(verify_admin_access)):
    """
    Get student statistics grouped by semester
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_students_by_semester()


@router.get("/analytics/top-students", response_model=List[Dict[str, Any]])
async def get_top_performing_students(
    limit: int = Query(10, ge=1, le=50, description="Number of top students to return"),
    admin_id: str = Depends(verify_admin_access)
):
    """
    Get top performing students by CGPA
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_top_performing_students(limit)


@router.get("/analytics/internships", response_model=List[Dict[str, Any]])
async def get_internship_analytics(admin_id: str = Depends(verify_admin_access)):
    """
    Get internship analytics by domain
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_internship_analytics()


@router.get("/analytics/applications", response_model=Dict[str, Any])
async def get_application_analytics(admin_id: str = Depends(verify_admin_access)):
    """
    Get detailed application analytics
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_application_analytics()


@router.get("/students", response_model=List[Dict[str, Any]])
async def get_all_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum records to return"),
    admin_id: str = Depends(verify_admin_access)
):
    """
    Get all students with pagination
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_all_students(skip, limit)


@router.get("/internships", response_model=List[Dict[str, Any]])
async def get_all_internships_admin(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum records to return"),
    admin_id: str = Depends(verify_admin_access)
):
    """
    Get all internships for admin view with application counts
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_all_internships_admin(skip, limit)


@router.post("/students/{student_id}/block", status_code=status.HTTP_200_OK)
async def block_student(
    student_id: str,
    admin_id: str = Depends(verify_admin_access)
):
    """
    Block a student account
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    success = await admin_service.block_student(student_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return {"message": "Student blocked successfully", "student_id": student_id}


@router.post("/students/{student_id}/unblock", status_code=status.HTTP_200_OK)
async def unblock_student(
    student_id: str,
    admin_id: str = Depends(verify_admin_access)
):
    """
    Unblock a student account
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    success = await admin_service.unblock_student(student_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return {"message": "Student unblocked successfully", "student_id": student_id}


@router.delete("/internships/{internship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_internship_admin(
    internship_id: str,
    admin_id: str = Depends(verify_admin_access)
):
    """
    Delete an internship (admin can delete any internship)
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    success = await admin_service.delete_internship_admin(internship_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internship not found"
        )
    
    return None


@router.get("/analytics/placement", response_model=Dict[str, Any])
async def get_placement_analytics(admin_id: str = Depends(verify_admin_access)):
    """
    Get placement tracking analytics
    
    Returns placement statistics including:
    - Total, placed, searching, not placed counts
    - Placement rate
    - Placement type distribution
    - Salary statistics by placement type
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_placement_analytics()


@router.get("/analytics/company-hiring", response_model=List[Dict[str, Any]])
async def get_company_hiring_stats(admin_id: str = Depends(verify_admin_access)):
    """
    Get company hiring statistics
    
    Returns companies with student count and average salary offered
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_company_hiring_stats()


@router.get("/students/unplaced", response_model=List[Dict[str, Any]])
async def get_unplaced_students(admin_id: str = Depends(verify_admin_access)):
    """
    Get list of unplaced students
    
    Returns students without placements sorted by CGPA
    
    **Requires admin authentication**
    """
    admin_service = AdminService()
    return await admin_service.get_unplaced_students()
