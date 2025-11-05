"""
Health check routes
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns the current status of the application
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "plex-toolbox-backend"
    }


@router.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Plex Toolbox API",
        "version": "0.1.0",
        "docs": "/api/docs"
    }
