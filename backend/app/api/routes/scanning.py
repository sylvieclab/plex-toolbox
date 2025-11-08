"""
Scan history tracking and management
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from loguru import logger
from pydantic import BaseModel
import os

from app.services.plex.connection import plex_connection
from app.db.session import get_db
from app.models.plex import ScanHistory

router = APIRouter()


class ScanRequest(BaseModel):
    path: Optional[str] = None


@router.post("/libraries/{library_key}/scan")
async def scan_library_with_history(
    library_key: str,
    request: ScanRequest = ScanRequest(),
    db: Session = Depends(get_db)
):
    """
    Scan library or specific path within library
    
    If path provided: Partial scan (fast) - uses Plex's knowledge of show locations
    If no path: Full library scan (slow)
    """
    try:
        server = plex_connection.get_connection()
        library = server.library.sectionByID(int(library_key))
        
        started_at = datetime.utcnow()
        
        # Determine scan type and prepare path
        scan_path = None
        full_path = None
        if request.path:
            # Parse the logical path (e.g., "/Drake & Josh")
            path_parts = [p for p in request.path.split('/') if p]
            
            if len(path_parts) > 0:
                # User wants to scan a specific show/movie
                show_title = path_parts[0]
                
                # Get the show from Plex to find its filesystem location
                items = library.all()
                show = next((s for s in items if s.title == show_title), None)
                
                if show and hasattr(show, 'locations') and show.locations:
                    # Use the show's actual filesystem location
                    full_path = show.locations[0]
                    logger.info(f"Found show filesystem path: {full_path}")
                    
                    scan_type = 'partial'
                    scan_path = request.path
                    message = f"Partial scan initiated for: {request.path}"
                else:
                    raise ValueError(f"Could not find filesystem location for: {show_title}")
            else:
                # Shouldn't happen, but fall back to library base
                base_location = library.locations[0]
                full_path = base_location
                scan_type = 'partial'
                scan_path = request.path
                message = f"Partial scan initiated for: {request.path}"
        else:
            # Full library scan
            scan_type = 'full'
            message = f"Full scan initiated for library: {library.title}"
        
        # Create scan history record
        scan = ScanHistory(
            library_key=library_key,
            library_name=library.title,
            library_type=library.type,
            scan_type=scan_type,
            path=scan_path,
            status='started',
            started_at=started_at
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        # Execute scan
        try:
            if scan_type == 'partial' and full_path:
                # Partial scan with specific path from Plex's knowledge
                library.update(path=full_path)
                logger.info(f"Partial scan completed for {library.title} at path: {full_path}")
            else:
                # Full library scan
                library.refresh()
                logger.info(f"Full scan completed for {library.title}")
            
            scan.status = 'completed'
            scan.completed_at = datetime.utcnow()
            scan.duration_seconds = (scan.completed_at - scan.started_at).total_seconds()
            
        except Exception as e:
            scan.status = 'failed'
            scan.error_message = str(e)
            scan.completed_at = datetime.utcnow()
            scan.duration_seconds = (scan.completed_at - scan.started_at).total_seconds()
            logger.error(f"Scan failed for {library.title}: {str(e)}")
        
        db.commit()
        db.refresh(scan)
        
        return {
            "status": scan.status,
            "message": message,
            "scan_id": scan.id,
            "scan_type": scan_type,
            "path": scan_path,
            "library_key": library_key,
            "library_name": library.title,
            "started_at": scan.started_at.isoformat(),
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
            "duration_seconds": scan.duration_seconds
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to scan library: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scan-history")
async def get_scan_history(
    limit: int = 50,
    library_key: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get scan history with optional library filter
    """
    try:
        query = db.query(ScanHistory)
        
        if library_key:
            query = query.filter(ScanHistory.library_key == library_key)
        
        scans = query.order_by(ScanHistory.started_at.desc()).limit(limit).all()
        
        return {
            "scans": [
                {
                    "id": scan.id,
                    "library_key": scan.library_key,
                    "library_name": scan.library_name,
                    "library_type": scan.library_type,
                    "scan_type": scan.scan_type,
                    "path": scan.path,
                    "status": scan.status,
                    "started_at": scan.started_at.isoformat(),
                    "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
                    "duration_seconds": scan.duration_seconds,
                    "error_message": scan.error_message
                }
                for scan in scans
            ],
            "total": len(scans)
        }
        
    except Exception as e:
        logger.error(f"Failed to get scan history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plex-activities")
async def get_current_plex_activities():
    """
    Get current Plex server activities (scans, processing, etc.)
    Shows what Plex is currently doing in real-time
    """
    try:
        server = plex_connection.get_connection()
        
        activities = []
        try:
            # Get all current activities from Plex
            server_activities = server.activities()
            
            for activity in server_activities:
                activity_data = {
                    "uuid": activity.uuid if hasattr(activity, 'uuid') else None,
                    "title": activity.title,
                    "subtitle": activity.subtitle if hasattr(activity, 'subtitle') else None,
                    "type": activity.type,
                    "cancellable": activity.cancellable if hasattr(activity, 'cancellable') else False,
                    "user_id": activity.userID if hasattr(activity, 'userID') else None,
                    "progress": activity.progress if hasattr(activity, 'progress') else 0,
                }
                activities.append(activity_data)
                
        except Exception as e:
            logger.warning(f"Could not fetch Plex activities: {str(e)}")
            return {"activities": []}
        
        return {"activities": activities}
        
    except Exception as e:
        logger.error(f"Failed to get current activities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/scan-history/{scan_id}")
async def delete_scan_history(
    scan_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific scan history record
    """
    try:
        scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan history not found")
        
        db.delete(scan)
        db.commit()
        
        return {"status": "success", "message": "Scan history deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete scan history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
