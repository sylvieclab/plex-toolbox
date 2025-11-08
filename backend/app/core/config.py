"""
Application configuration using Pydantic settings
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """Application settings"""
    
    # Project info
    PROJECT_NAME: str = "Totarr"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    
    # API settings
    API_V1_STR: str = "/api"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://totarr:totarr@db:5432/totarr"
    
    # Redis (for Celery)
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Plex connection (stored in database, these are defaults)
    PLEX_URL: str = ""
    PLEX_TOKEN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
