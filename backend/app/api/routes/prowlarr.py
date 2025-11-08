"""
API routes for Prowlarr integration
Handles indexer management and monitoring
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from loguru import logger

from app.db.session import get_db
from app.models.integrations import IntegrationConfig
from app.services.integrations import ProwlarrClient

router = APIRouter(prefix="/prowlarr", tags=["prowlarr"])


async def get_prowlarr_client(db: Session = Depends(get_db)) -> ProwlarrClient:
    """Get an enabled Prowlarr client"""
    config = (
        db.query(IntegrationConfig)
        .filter(
            IntegrationConfig.service_type == "prowlarr",
            IntegrationConfig.enabled == True
        )
        .first()
    )
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enabled Prowlarr integration found. Please configure Prowlarr in Settings."
        )
    
    return ProwlarrClient(config.url, config.api_key)


@router.get("/indexers")
async def get_indexers(client: ProwlarrClient = Depends(get_prowlarr_client)) -> List[Dict[str, Any]]:
    """
    Get all indexers from Prowlarr
    
    Returns all configured indexers with their status and settings.
    """
    try:
        indexers_data = await client.get_indexers()
        return indexers_data
    except Exception as e:
        logger.error(f"Failed to get Prowlarr indexers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get indexers: {str(e)}"
        )


@router.get("/stats")
async def get_stats(client: ProwlarrClient = Depends(get_prowlarr_client)) -> Dict[str, Any]:
    """
    Get indexer statistics from Prowlarr
    
    Returns query statistics and success/failure rates for indexers.
    """
    try:
        stats_data = await client.get_indexer_stats()
        return stats_data
    except Exception as e:
        logger.error(f"Failed to get Prowlarr stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.post("/test/{indexer_id}")
async def test_indexer(
    indexer_id: int,
    client: ProwlarrClient = Depends(get_prowlarr_client)
) -> Dict[str, Any]:
    """
    Test a specific indexer
    
    Tests connectivity and functionality of an indexer.
    """
    try:
        result = await client.test_indexer(indexer_id)
        logger.info(f"Tested indexer {indexer_id}")
        return {"success": True, "message": f"Indexer {indexer_id} test completed", "data": result}
    except Exception as e:
        logger.error(f"Failed to test indexer {indexer_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test indexer: {str(e)}"
        )
