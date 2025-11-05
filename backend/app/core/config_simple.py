"""
Simplified configuration for local development without external dependencies
Uses SQLite instead of PostgreSQL for easier local testing
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Project info
    PROJECT_NAME: str = "Plex Toolbox"
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
    
    # Database - use SQLite for local dev if PostgreSQL not available
    DATABASE_URL: str = "sqlite:///./plex_toolbox.db"
    
    # Redis (optional for local dev)
    REDIS_URL: str = ""
    
    # Celery (optional for local dev)
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Plex connection (stored in database, these are defaults)
    PLEX_URL: str = ""
    PLEX_TOKEN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
