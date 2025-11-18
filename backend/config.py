"""
Configuration settings for the backend API
Loads environment variables and provides configuration objects
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database settings
    db_host: str = "localhost"
    db_port: str = "5432"
    db_user: str = "anime_user"
    db_password: str = "anime_password"
    db_name: str = "anime_db"

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Security settings
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Recommender service
    recommender_url: str = "http://localhost:8001"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()
