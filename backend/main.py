"""
Main FastAPI application
Entry point for the backend API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_connection_pool, close_connection_pool
from routes import anime_router, auth_router, user_router, recommendation_router
from config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    Initializes database connection pool on startup
    Closes connections on shutdown
    """
    # Startup
    print("🚀 Starting anime API server...")
    init_connection_pool()
    print(f"✓ Server running on http://{settings.api_host}:{settings.api_port}")
    yield
    # Shutdown
    print("\n🛑 Shutting down anime API server...")
    close_connection_pool()

# Create FastAPI application
app = FastAPI(
    title="Anime Recommendation API",
    description="Backend API for anime website with content-based recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(anime_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(recommendation_router)

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Anime Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "anime": "/api/anime",
            "auth": "/api/auth",
            "users": "/api/users",
            "recommendations": "/api/recommendations"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
