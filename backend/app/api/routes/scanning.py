"""
Scan history tracking and management
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from loguru import logger

from app.services.plex.connection import plex_connection
from app.db.session import get_db
from app.models.plex import ScanHistory

router = APIRouter()


@router.post("/libraries/{library_key}/scan")
async def scan_library_with_history(
    library_key: str,
    db: Session = Depends(get_db)
):
    """
    Scan library and record in history
    """
    try:
        server = plex_connection.get_connection()
        library = server.library.sectionByID(int(library_key))
        
        # Create scan history record
        scan = ScanHistory(
            library_key=library_key,
            library_name=library.title,
            library_type=library.type,
            scan_type='full',
            status='started',
            started_at=datetime.utcnow()
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        # Trigger scan
        try:
            library.refresh()
            scan.status = 'completed'
            scan.completed_at = datetime.utcnow()
            logger.info(f"Scan completed for {library.title}")
        except Exception as e:
            scan.status = 'failed'
            scan.error_message = str(e)
            scan.completed_at = datetime.utcnow()
            logger.error(f"Scan failed for {library.title}: {str(e)}")
        
        db.commit()
        db.refresh(scan)
        
        return {
            "status": scan.status,
            "message": f"Scan {scan.status} for library: {library.title}",
            "library_key": library_key,
            "scan_id": scan.id,
            "started_at": scan.started_at.isoformat(),
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None
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
                    "status": scan.status,
                    "started_at": scan.started_at.isoformat(),
                    "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
                    "duration_seconds": (scan.completed_at - scan.started_at).total_seconds() if scan.completed_at else None,
                    "error_message": scan.error_message
                }
                for scan in scans
            ],
            "total": len(scans)
        }
        
    except Exception as e:
        logger.error(f"Failed to get scan history: {str(e)}")
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
