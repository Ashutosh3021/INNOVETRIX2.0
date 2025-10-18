"""
Skill matching routes using TF-IDF and cosine similarity
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.internship import MatchedInternship
from app.services.user_service import UserService
from app.services.internship_service import InternshipService
from app.services.matching_service import MatchingService
from app.services.auth_service import get_current_user_id

router = APIRouter(prefix="/api/match", tags=["Skill Matching"])


@router.get("/{user_id}", response_model=List[MatchedInternship])
async def match_internships_for_user(
    user_id: str,
    top_n: int = Query(10, ge=1, le=50, description="Number of top matches to return"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum match score"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Match internships to a user based on their skills using TF-IDF and cosine similarity
    
    **Path Parameters:**
    - **user_id**: ID of the user to match internships for
    
    **Query Parameters:**
    - **top_n**: Number of top matches to return (default: 10, max: 50)
    - **min_score**: Minimum match score threshold 0.0-1.0 (default: 0.0)
    
    **Returns:**
    - List of internships ranked by match score (highest first)
    - Each internship includes:
        - All internship details
        - **match_score**: Similarity score between 0.0 and 1.0
        - **matched_skills**: List of skills that match between user and internship
    
    **Requires authentication token in header**
    """
    # Initialize services
    user_service = UserService()
    internship_service = InternshipService()
    matching_service = MatchingService()
    
    # Get user
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get all available internships
    internships = await internship_service.get_all_internships(skip=0, limit=1000)
    
    if not internships:
        return []
    
    # Calculate match scores using TF-IDF and cosine similarity
    matched_internships = matching_service.calculate_match_score(user, internships)
    
    # Filter and return top matches
    top_matches = matching_service.get_top_matches(
        matched_internships,
        top_n=top_n,
        min_score=min_score
    )
    
    return top_matches


@router.get("/me/recommendations", response_model=List[MatchedInternship])
async def get_my_recommendations(
    top_n: int = Query(10, ge=1, le=50, description="Number of top matches to return"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum match score"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get internship recommendations for the current authenticated user
    
    **Query Parameters:**
    - **top_n**: Number of top matches to return (default: 10, max: 50)
    - **min_score**: Minimum match score threshold 0.0-1.0 (default: 0.0)
    
    **Returns:**
    - List of internships ranked by match score (highest first)
    
    **Requires authentication token in header**
    """
    # Initialize services
    user_service = UserService()
    internship_service = InternshipService()
    matching_service = MatchingService()
    
    # Get current user
    user = await user_service.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get all available internships
    internships = await internship_service.get_all_internships(skip=0, limit=1000)
    
    if not internships:
        return []
    
    # Calculate match scores
    matched_internships = matching_service.calculate_match_score(user, internships)
    
    # Filter and return top matches
    top_matches = matching_service.get_top_matches(
        matched_internships,
        top_n=top_n,
        min_score=min_score
    )
    
    return top_matches