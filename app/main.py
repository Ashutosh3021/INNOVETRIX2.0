"""
FastAPI application entry point for SkillMatchAI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from app.config import settings
from app.database.db import connect_to_mongo, close_mongo_connection
from app.routes import auth, users, internships, matching


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Application lifespan context manager
    Handles startup and shutdown events
    """
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started successfully!")
    
    yield
    
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()
    print(f"👋 {settings.APP_NAME} shut down gracefully")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    SkillMatchAI - Intelligent Internship Matching Platform
    
    Match students to internships based on skills using TF-IDF and cosine similarity.
    
    ## Features
    * 🔐 JWT-based authentication
    * 👤 User management with skills and projects
    * 💼 Internship listing management
    * 🎯 AI-powered skill matching using TF-IDF
    * 📊 Ranked recommendations with match scores
    
    ## Authentication
    All endpoints except `/api/auth/register` and `/api/auth/login` require JWT authentication.
    Include the token in the Authorization header: `Bearer <your_token>`
    """,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc UI
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(internships.router)
app.include_router(matching.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint. Returns 503 if database isn't ready."""
    # Import here to avoid circular imports at module load
    from app.database.db import is_db_ready

    healthy = is_db_ready()
    if not healthy:
        content = {
            "status": "unhealthy",
            "detail": "database unavailable",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }
        return JSONResponse(content=content, status_code=503)

    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )