"""
API route handlers
Defines all API endpoints for anime, users, and recommendations
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import timedelta
import requests

from models import (
    Anime, AnimeCreate, AnimeUpdate, AnimeListResponse,
    User, UserCreate, UserLogin, Token,
    RatingCreate, Rating,
    RecommendationResponse, MessageResponse
)
from database import get_db_cursor
from auth import verify_password, get_password_hash, create_access_token, verify_token
from config import get_settings

settings = get_settings()

# Create routers
anime_router = APIRouter(prefix="/api/anime", tags=["Anime"])
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])
user_router = APIRouter(prefix="/api/users", tags=["Users"])
recommendation_router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

# ============================================================================
# ANIME ROUTES
# ============================================================================

@anime_router.get("/", response_model=AnimeListResponse)
async def get_all_anime(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    genre: Optional[str] = None
):
    """
    Get all anime with optional filtering and pagination

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **search**: Search by title (case-insensitive)
    - **genre**: Filter by genre
    """
    with get_db_cursor() as cursor:
        # Build query with filters
        where_clauses = []
        params = []

        if search:
            where_clauses.append("title ILIKE %s")
            params.append(f"%{search}%")

        if genre:
            where_clauses.append("%s = ANY(genres)")
            params.append(genre)

        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM anime{where_sql}", params)
        total = cursor.fetchone()['count']

        # Get anime with pagination
        params.extend([limit, skip])
        cursor.execute(f"""
            SELECT * FROM anime
            {where_sql}
            ORDER BY rating DESC, created_at DESC
            LIMIT %s OFFSET %s
        """, params)

        anime = cursor.fetchall()

        return {"total": total, "anime": anime}

@anime_router.get("/{anime_id}", response_model=Anime)
async def get_anime_by_id(anime_id: int):
    """Get a specific anime by ID"""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM anime WHERE anime_id = %s", (anime_id,))
        anime = cursor.fetchone()

        if not anime:
            raise HTTPException(status_code=404, detail="Anime not found")

        return anime

@anime_router.post("/", response_model=Anime, status_code=201)
async def create_anime(anime: AnimeCreate, user_data: dict = Depends(verify_token)):
    """Create a new anime (requires authentication)"""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO anime (title, image_url, genres, description, release_date, rating)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            anime.title,
            anime.image_url,
            anime.genres,
            anime.description,
            anime.release_date,
            anime.rating
        ))

        new_anime = cursor.fetchone()
        return new_anime

@anime_router.put("/{anime_id}", response_model=Anime)
async def update_anime(
    anime_id: int,
    anime_update: AnimeUpdate,
    user_data: dict = Depends(verify_token)
):
    """Update an existing anime (requires authentication)"""
    with get_db_cursor(commit=True) as cursor:
        # Check if anime exists
        cursor.execute("SELECT * FROM anime WHERE anime_id = %s", (anime_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Anime not found")

        # Build update query dynamically
        update_fields = []
        params = []

        if anime_update.title is not None:
            update_fields.append("title = %s")
            params.append(anime_update.title)

        if anime_update.image_url is not None:
            update_fields.append("image_url = %s")
            params.append(anime_update.image_url)

        if anime_update.genres is not None:
            update_fields.append("genres = %s")
            params.append(anime_update.genres)

        if anime_update.description is not None:
            update_fields.append("description = %s")
            params.append(anime_update.description)

        if anime_update.release_date is not None:
            update_fields.append("release_date = %s")
            params.append(anime_update.release_date)

        if anime_update.rating is not None:
            update_fields.append("rating = %s")
            params.append(anime_update.rating)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(anime_id)

        cursor.execute(f"""
            UPDATE anime
            SET {', '.join(update_fields)}
            WHERE anime_id = %s
            RETURNING *
        """, params)

        updated_anime = cursor.fetchone()
        return updated_anime

@anime_router.delete("/{anime_id}", response_model=MessageResponse)
async def delete_anime(anime_id: int, user_data: dict = Depends(verify_token)):
    """Delete an anime (requires authentication)"""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM anime WHERE anime_id = %s RETURNING anime_id", (anime_id,))
        deleted = cursor.fetchone()

        if not deleted:
            raise HTTPException(status_code=404, detail="Anime not found")

        return {"message": f"Anime {anime_id} deleted successfully"}

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@auth_router.post("/register", response_model=User, status_code=201)
async def register(user: UserCreate):
    """Register a new user"""
    with get_db_cursor(commit=True) as cursor:
        # Check if username already exists
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already registered")

        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password and create user
        hashed_password = get_password_hash(user.password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING user_id, username, email, created_at
        """, (user.username, user.email, hashed_password))

        new_user = cursor.fetchone()
        return new_user

@auth_router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    """Login and receive JWT token"""
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT user_id, password_hash FROM users WHERE username = %s",
            (user_login.username,)
        )
        user = cursor.fetchone()

        if not user or not verify_password(user_login.password, user['password_hash']):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user['user_id'])},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

# ============================================================================
# USER ROUTES
# ============================================================================

@user_router.get("/me", response_model=User)
async def get_current_user(user_data: dict = Depends(verify_token)):
    """Get current user information"""
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT user_id, username, email, created_at FROM users WHERE user_id = %s",
            (user_data['user_id'],)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

@user_router.post("/rate", response_model=Rating, status_code=201)
async def rate_anime(rating: RatingCreate, user_data: dict = Depends(verify_token)):
    """Rate an anime"""
    with get_db_cursor(commit=True) as cursor:
        # Check if anime exists
        cursor.execute("SELECT anime_id FROM anime WHERE anime_id = %s", (rating.anime_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Anime not found")

        # Insert or update rating
        cursor.execute("""
            INSERT INTO user_ratings (user_id, anime_id, rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, anime_id)
            DO UPDATE SET rating = EXCLUDED.rating, created_at = CURRENT_TIMESTAMP
            RETURNING *
        """, (user_data['user_id'], rating.anime_id, rating.rating))

        new_rating = cursor.fetchone()

        # Update anime average rating
        cursor.execute("""
            UPDATE anime
            SET rating = (SELECT AVG(rating) FROM user_ratings WHERE anime_id = %s)
            WHERE anime_id = %s
        """, (rating.anime_id, rating.anime_id))

        return new_rating

@user_router.get("/ratings", response_model=List[Rating])
async def get_user_ratings(user_data: dict = Depends(verify_token)):
    """Get all ratings by current user"""
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM user_ratings WHERE user_id = %s ORDER BY created_at DESC",
            (user_data['user_id'],)
        )
        ratings = cursor.fetchall()
        return ratings

# ============================================================================
# RECOMMENDATION ROUTES
# ============================================================================

@recommendation_router.get("/{anime_id}", response_model=List[RecommendationResponse])
async def get_recommendations(anime_id: int, limit: int = Query(5, ge=1, le=20)):
    """
    Get content-based recommendations for a specific anime
    Calls the recommendation service to compute similarities
    """
    try:
        # Call the recommender service
        response = requests.get(
            f"{settings.recommender_url}/recommend/{anime_id}",
            params={"limit": limit},
            timeout=5
        )

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Anime not found")

        response.raise_for_status()
        recommendations = response.json()

        return recommendations

    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail="Recommendation service unavailable"
        )

@recommendation_router.get("/", response_model=List[RecommendationResponse])
async def get_general_recommendations(limit: int = Query(10, ge=1, le=20)):
    """
    Get general recommendations (top-rated anime)
    """
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT anime_id, title, image_url, genres, rating
            FROM anime
            ORDER BY rating DESC, created_at DESC
            LIMIT %s
        """, (limit,))

        anime_list = cursor.fetchall()

        # Format as recommendations with similarity score = 1.0
        recommendations = [
            {
                "anime_id": anime['anime_id'],
                "title": anime['title'],
                "image_url": anime['image_url'],
                "genres": anime['genres'],
                "similarity_score": 1.0,
                "rating": anime['rating']
            }
            for anime in anime_list
        ]

        return recommendations
