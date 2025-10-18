"""
User management routes (protected by JWT authentication)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.services.auth_service import get_current_user_id

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user_id: str = Depends(get_current_user_id)):
    """
    Get current authenticated user's profile
    
    **Requires authentication token in header**
    """
    user_service = UserService()
    user = await user_service.get_user_by_id(current_user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_service.user_to_response(user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Update current authenticated user's profile
    
    - **name**: Updated name (optional)
    - **skills**: Updated skills list (optional)
    - **projects**: Updated projects list (optional)
    
    **Requires authentication token in header**
    """
    user_service = UserService()
    user = await user_service.update_user(current_user_id, user_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_service.user_to_response(user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user_id: str = Depends(get_current_user_id)):
    """
    Delete current authenticated user's account
    
    **Requires authentication token in header**
    """
    user_service = UserService()
    deleted = await user_service.delete_user(current_user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return None


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a user by ID
    
    **Requires authentication token in header**
    """
    user_service = UserService()
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_service.user_to_response(user)