"""
API routes for Radarr integration
Handles movie management and missing movie tracking
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from loguru import logger

from app.db.session import get_db
from app.models.integrations import IntegrationConfig
from app.services.integrations import RadarrClient

router = APIRouter(prefix="/radarr", tags=["radarr"])


async def get_radarr_client(db: Session = Depends(get_db)) -> RadarrClient:
    """Get an enabled Radarr client"""
    config = (
        db.query(IntegrationConfig)
        .filter(
            IntegrationConfig.service_type == "radarr",
            IntegrationConfig.enabled == True
        )
        .first()
    )
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enabled Radarr integration found. Please configure Radarr in Settings."
        )
    
    return RadarrClient(config.url, config.api_key)


@router.get("/movies")
async def get_all_movies(client: RadarrClient = Depends(get_radarr_client)) -> List[Dict[str, Any]]:
    """
    Get all movies from Radarr
    
    Returns all movies configured in Radarr with their metadata.
    """
    try:
        movies_data = await client.get_movies()
        return movies_data
    except Exception as e:
        logger.error(f"Failed to get Radarr movies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get movies: {str(e)}"
        )


@router.get("/missing")
async def get_missing_movies(client: RadarrClient = Depends(get_radarr_client)) -> List[Dict[str, Any]]:
    """
    Get missing movies from Radarr
    
    Returns movies that are monitored but not yet downloaded.
    """
    try:
        missing_data = await client.get_missing_movies()
        return missing_data
    except Exception as e:
        logger.error(f"Failed to get missing movies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get missing movies: {str(e)}"
        )


@router.post("/search")
async def search_movies(
    movie_ids: List[int],
    client: RadarrClient = Depends(get_radarr_client)
) -> Dict[str, Any]:
    """
    Trigger a search for specific movies
    
    Initiates a search in Radarr for the provided movie IDs.
    """
    try:
        result = await client.search_movies(movie_ids)
        logger.info(f"Initiated search for {len(movie_ids)} movies")
        return {"success": True, "message": f"Search initiated for {len(movie_ids)} movies", "data": result}
    except Exception as e:
        logger.error(f"Failed to search movies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search movies: {str(e)}"
        )


@router.get("/queue")
async def get_queue(client: RadarrClient = Depends(get_radarr_client)) -> Dict[str, Any]:
    """
    Get the Radarr download queue
    
    Returns currently downloading and queued movies.
    """
    try:
        queue_data = await client.get_queue()
        return queue_data
    except Exception as e:
        logger.error(f"Failed to get Radarr queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get queue: {str(e)}"
        )
