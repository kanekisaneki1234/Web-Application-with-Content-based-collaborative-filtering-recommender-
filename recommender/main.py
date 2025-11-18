"""
Recommendation Service API
FastAPI service that provides content-based recommendations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List
import os

from recommender_engine import AnimeRecommender

# Global recommender instance
recommender = None

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'user': os.getenv('DB_USER', 'anime_user'),
    'password': os.getenv('DB_PASSWORD', 'anime_password'),
    'database': os.getenv('DB_NAME', 'anime_db')
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager
    Trains the recommendation model on startup
    """
    global recommender

    # Startup
    print("🚀 Starting recommendation service...")
    recommender = AnimeRecommender(db_config)
    recommender.train()
    print("✓ Recommendation service ready")

    yield

    # Shutdown
    print("\n🛑 Shutting down recommendation service...")

# Create FastAPI application
app = FastAPI(
    title="Anime Recommendation Service",
    description="Content-based recommendation engine for anime",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Anime Recommendation Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": recommender is not None}

@app.get("/recommend/{anime_id}")
async def get_recommendations(anime_id: int, limit: int = 5):
    """
    Get content-based recommendations for a specific anime

    Args:
        anime_id: The ID of the anime to get recommendations for
        limit: Number of recommendations to return (default: 5, max: 20)

    Returns:
        List of recommended anime with similarity scores
    """
    if recommender is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model not loaded"
        )

    # Validate limit
    if limit < 1 or limit > 20:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 20"
        )

    try:
        recommendations = recommender.get_recommendations(
            anime_id=anime_id,
            n_recommendations=limit
        )
        return recommendations

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/retrain")
async def retrain_model():
    """
    Retrain the recommendation model
    Use this endpoint when new anime are added to the database
    """
    global recommender

    try:
        print("🔄 Retraining recommendation model...")
        recommender = AnimeRecommender(db_config)
        recommender.train()
        return {"message": "Model retrained successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retraining model: {str(e)}"
        )

@app.get("/anime/{anime_id}/info")
async def get_anime_info(anime_id: int):
    """Get information about a specific anime"""
    if recommender is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model not loaded"
        )

    try:
        anime_info = recommender.get_anime_info(anime_id)
        return anime_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get statistics about the recommendation system"""
    if recommender is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model not loaded"
        )

    return {
        "total_anime": len(recommender.anime_df),
        "similarity_matrix_shape": recommender.similarity_matrix.shape,
        "vocabulary_size": len(recommender.tfidf_vectorizer.vocabulary_) if recommender.tfidf_vectorizer else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
