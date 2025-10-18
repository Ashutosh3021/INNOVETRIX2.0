"""
Authentication service for JWT token and password handling
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
from jwt.exceptions import PyJWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.models.user import TokenData

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token security
security = HTTPBearer()


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain text password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token
        
        Args:
            data: Payload data to encode in token
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow()
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str) -> TokenData:
        """
        Decode and verify JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            TokenData object with user information
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            
            if user_id is None:
                raise credentials_exception
            
            return TokenData(user_id=user_id, email=email)
            
        except PyJWTError:
            raise credentials_exception


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current authenticated user ID from JWT token
    
    Args:
        credentials: HTTP Bearer token from request header
        
    Returns:
        User ID string
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    token_data = AuthService.decode_access_token(token)
    
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return token_data.user_id