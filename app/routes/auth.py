"""
Authentication routes for user registration and login
"""
from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserLogin, Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user
    
    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: User's password (min 6 characters)
    - **skills**: List of user's skills
    - **projects**: List of user's projects
    """
    user_service = UserService()
    
    # Create user
    user = await user_service.create_user(user_data)
    
    # Generate JWT token
    access_token = AuthService.create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Return token and user info
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_service.user_to_response(user)
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with email and password
    
    - **email**: User's email address
    - **password**: User's password
    """
    user_service = UserService()
    
    # Authenticate user
    user = await user_service.authenticate_user(
        credentials.email,
        credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Generate JWT token
    access_token = AuthService.create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Return token and user info
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_service.user_to_response(user)
    )