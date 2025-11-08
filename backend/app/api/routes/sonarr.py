"""
API routes for Sonarr integration
Handles TV show management and missing episode tracking
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from loguru import logger

from app.db.session import get_db
from app.models.integrations import IntegrationConfig
from app.services.integrations import SonarrClient

router = APIRouter(prefix="/sonarr", tags=["sonarr"])


async def get_sonarr_client(db: Session = Depends(get_db)) -> SonarrClient:
    """Get an enabled Sonarr client"""
    config = (
        db.query(IntegrationConfig)
        .filter(
            IntegrationConfig.service_type == "sonarr",
            IntegrationConfig.enabled == True
        )
        .first()
    )
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enabled Sonarr integration found. Please configure Sonarr in Settings."
        )
    
    return SonarrClient(config.url, config.api_key)


@router.get("/series")
async def get_all_series(client: SonarrClient = Depends(get_sonarr_client)) -> List[Dict[str, Any]]:
    """
    Get all TV series from Sonarr
    
    Returns all series configured in Sonarr with their metadata.
    """
    try:
        series_data = await client.get_series()
        return series_data
    except Exception as e:
        logger.error(f"Failed to get Sonarr series: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get series: {str(e)}"
        )


@router.get("/missing")
async def get_missing_episodes(
    page: int = 1,
    page_size: int = 50,
    client: SonarrClient = Depends(get_sonarr_client)
) -> Dict[str, Any]:
    """
    Get missing episodes from Sonarr
    
    Returns episodes that are monitored but not yet downloaded.
    Supports pagination for large libraries.
    """
    try:
        missing_data = await client.get_missing_episodes(page, page_size)
        return missing_data
    except Exception as e:
        logger.error(f"Failed to get missing episodes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get missing episodes: {str(e)}"
        )


@router.post("/search")
async def search_episodes(
    episode_ids: List[int],
    client: SonarrClient = Depends(get_sonarr_client)
) -> Dict[str, Any]:
    """
    Trigger a search for specific episodes
    
    Initiates a search in Sonarr for the provided episode IDs.
    """
    try:
        result = await client.search_episodes(episode_ids)
        logger.info(f"Initiated search for {len(episode_ids)} episodes")
        return {"success": True, "message": f"Search initiated for {len(episode_ids)} episodes", "data": result}
    except Exception as e:
        logger.error(f"Failed to search episodes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search episodes: {str(e)}"
        )


@router.get("/queue")
async def get_queue(client: SonarrClient = Depends(get_sonarr_client)) -> Dict[str, Any]:
    """
    Get the Sonarr download queue
    
    Returns currently downloading and queued episodes.
    """
    try:
        queue_data = await client.get_queue()
        return queue_data
    except Exception as e:
        logger.error(f"Failed to get Sonarr queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get queue: {str(e)}"
        )


@router.get("/calendar")
async def get_calendar(
    days: int = 7,
    client: SonarrClient = Depends(get_sonarr_client)
) -> List[Dict[str, Any]]:
    """
    Get upcoming episodes calendar
    
    Returns episodes airing in the next N days.
    """
    from datetime import datetime, timedelta
    
    try:
        start = datetime.now().isoformat()
        end = (datetime.now() + timedelta(days=days)).isoformat()
        calendar_data = await client.get_calendar(start, end)
        return calendar_data
    except Exception as e:
        logger.error(f"Failed to get Sonarr calendar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get calendar: {str(e)}"
        )
