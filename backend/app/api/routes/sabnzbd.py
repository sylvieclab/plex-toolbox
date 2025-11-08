"""
API routes for SABnzbd integration
Handles download queue and history management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from loguru import logger

from app.db.session import get_db
from app.models.integrations import IntegrationConfig
from app.services.integrations import SabnzbdClient

router = APIRouter(prefix="/sabnzbd", tags=["sabnzbd"])


async def get_sabnzbd_client(db: Session = Depends(get_db)) -> SabnzbdClient:
    """Get an enabled SABnzbd client"""
    config = (
        db.query(IntegrationConfig)
        .filter(
            IntegrationConfig.service_type == "sabnzbd",
            IntegrationConfig.enabled == True
        )
        .first()
    )
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enabled SABnzbd integration found. Please configure SABnzbd in Settings."
        )
    
    return SabnzbdClient(config.url, config.api_key)


@router.get("/queue")
async def get_queue(client: SabnzbdClient = Depends(get_sabnzbd_client)) -> Dict[str, Any]:
    """
    Get the current download queue
    
    Returns active downloads with progress, speed, ETA, etc.
    """
    try:
        queue_data = await client.get_queue()
        return queue_data
    except Exception as e:
        logger.error(f"Failed to get SABnzbd queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get queue: {str(e)}"
        )


@router.get("/history")
async def get_history(
    limit: int = 50,
    client: SabnzbdClient = Depends(get_sabnzbd_client)
) -> Dict[str, Any]:
    """
    Get download history
    
    Returns completed and failed downloads.
    """
    try:
        history_data = await client.get_history(limit)
        return history_data
    except Exception as e:
        logger.error(f"Failed to get SABnzbd history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}"
        )


@router.post("/pause")
async def pause_queue(client: SabnzbdClient = Depends(get_sabnzbd_client)) -> Dict[str, Any]:
    """
    Pause the download queue
    
    Pauses all active downloads.
    """
    try:
        result = await client.pause_queue()
        logger.info("SABnzbd queue paused")
        return {"success": True, "message": "Queue paused", "data": result}
    except Exception as e:
        logger.error(f"Failed to pause SABnzbd queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pause queue: {str(e)}"
        )


@router.post("/resume")
async def resume_queue(client: SabnzbdClient = Depends(get_sabnzbd_client)) -> Dict[str, Any]:
    """
    Resume the download queue
    
    Resumes all paused downloads.
    """
    try:
        result = await client.resume_queue()
        logger.info("SABnzbd queue resumed")
        return {"success": True, "message": "Queue resumed", "data": result}
    except Exception as e:
        logger.error(f"Failed to resume SABnzbd queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resume queue: {str(e)}"
        )


@router.get("/status")
async def get_status(client: SabnzbdClient = Depends(get_sabnzbd_client)) -> Dict[str, Any]:
    """
    Get SABnzbd status
    
    Returns current status including speed, disk space, etc.
    """
    try:
        status_data = await client.get_status()
        return status_data
    except Exception as e:
        logger.error(f"Failed to get SABnzbd status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status: {str(e)}"
        )


@router.delete("/history/{nzo_id}")
async def delete_history_item(
    nzo_id: str,
    client: SabnzbdClient = Depends(get_sabnzbd_client)
) -> Dict[str, Any]:
    """
    Delete an item from history
    """
    try:
        result = await client.delete_history_item(nzo_id)
        logger.info(f"Deleted history item: {nzo_id}")
        return {"success": True, "message": "History item deleted", "data": result}
    except Exception as e:
        logger.error(f"Failed to delete history item {nzo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete history item: {str(e)}"
        )


@router.post("/retry/{nzo_id}")
async def retry_download(
    nzo_id: str,
    client: SabnzbdClient = Depends(get_sabnzbd_client)
) -> Dict[str, Any]:
    """
    Retry a failed download
    """
    try:
        result = await client.retry_download(nzo_id)
        logger.info(f"Retrying download: {nzo_id}")
        return {"success": True, "message": "Download retry initiated", "data": result}
    except Exception as e:
        logger.error(f"Failed to retry download {nzo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retry download: {str(e)}"
        )
