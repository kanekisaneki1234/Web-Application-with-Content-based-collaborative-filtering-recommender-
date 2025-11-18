"""
Pydantic models for request/response validation
Defines the data structures used by the API
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

# Anime Models
class AnimeBase(BaseModel):
    """Base anime model with common fields"""
    title: str = Field(..., min_length=1, max_length=255)
    image_url: Optional[str] = None
    genres: List[str] = []
    description: Optional[str] = None
    release_date: Optional[date] = None
    rating: Optional[Decimal] = Field(default=0.0, ge=0, le=10)

class AnimeCreate(AnimeBase):
    """Model for creating a new anime"""
    pass

class AnimeUpdate(BaseModel):
    """Model for updating anime (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    image_url: Optional[str] = None
    genres: Optional[List[str]] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    rating: Optional[Decimal] = Field(None, ge=0, le=10)

class Anime(AnimeBase):
    """Complete anime model with database fields"""
    anime_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# User Models
class UserBase(BaseModel):
    """Base user model"""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    """Model for user registration"""
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """Model for user login"""
    username: str
    password: str

class User(UserBase):
    """Complete user model"""
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"

# Rating Models
class RatingCreate(BaseModel):
    """Model for creating a rating"""
    anime_id: int
    rating: Decimal = Field(..., ge=0, le=10)

class Rating(RatingCreate):
    """Complete rating model"""
    rating_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Recommendation Models
class RecommendationResponse(BaseModel):
    """Model for recommendation response"""
    anime_id: int
    title: str
    image_url: Optional[str]
    genres: List[str]
    similarity_score: float
    rating: Optional[Decimal]

# Response Models
class AnimeListResponse(BaseModel):
    """Response model for anime list"""
    total: int
    anime: List[Anime]

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
