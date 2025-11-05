"""
Library management routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from loguru import logger

from app.schemas.plex import (
    PlexLibrary,
    LibraryScanRequest,
    LibraryScanResponse,
    PlexMediaItem
)
from app.services.plex.connection import plex_connection

router = APIRouter()


@router.get("/libraries", response_model=List[PlexLibrary])
async def get_libraries():
    """
    Get all Plex libraries
    
    Returns a list of all available libraries on the Plex server.
    """
    try:
        server = plex_connection.get_connection()
        libraries = server.library.sections()
        result = []
        for lib in libraries:
            result.append(PlexLibrary(
                key=str(lib.key),
                title=lib.title,
                type=lib.type,
                agent=lib.agent if hasattr(lib, 'agent') else None,
                scanner=lib.scanner if hasattr(lib, 'scanner') else None,
                language=lib.language if hasattr(lib, 'language') else None,
                uuid=lib.uuid,
                updated_at=lib.updatedAt if hasattr(lib, 'updatedAt') else None,
                created_at=lib.createdAt if hasattr(lib, 'createdAt') else None,
                scanned_at=lib.scannedAt if hasattr(lib, 'scannedAt') else None,
                content_count=lib.totalSize if hasattr(lib, 'totalSize') else 0
            ))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get libraries: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get libraries: {str(e)}")


@router.post("/scan", response_model=LibraryScanResponse)
async def scan_library(request: LibraryScanRequest):
    """
    Initiate a library scan
    
    Triggers a scan for the specified library. If a path is provided,
    only that specific path will be scanned (selective scanning).
    """
    try:
        server = plex_connection.get_connection()
        library = server.library.sectionByID(request.library_key)
        
        if not library:
            raise HTTPException(status_code=404, detail=f"Library not found: {request.library_key}")
        
        # Initiate scan
        if request.path:
            library.update(request.path)
        else:
            library.update()
        
        # TODO: Save to scan history in database
        
        return LibraryScanResponse(
            status="initiated",
            library_key=request.library_key,
            library_name=library.title,
            message=f"Scan initiated for {library.title}" + (f" at path: {request.path}" if request.path else ""),
            started_at=datetime.utcnow()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to initiate scan: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate scan: {str(e)}")


@router.get("/libraries/{library_key}")
async def get_library_details(library_key: str):
    """
    Get detailed information about a specific library
    """
    try:
        server = plex_connection.get_connection()
        library = server.library.sectionByID(library_key)
        
        if not library:
            raise HTTPException(status_code=404, detail=f"Library not found: {library_key}")
        
        return PlexLibrary(
            key=str(library.key),
            title=library.title,
            type=library.type,
            agent=library.agent if hasattr(library, 'agent') else None,
            scanner=library.scanner if hasattr(library, 'scanner') else None,
            language=library.language if hasattr(library, 'language') else None,
            uuid=library.uuid,
            updated_at=library.updatedAt if hasattr(library, 'updatedAt') else None,
            created_at=library.createdAt if hasattr(library, 'createdAt') else None,
            scanned_at=library.scannedAt if hasattr(library, 'scannedAt') else None,
            content_count=library.totalSize if hasattr(library, 'totalSize') else 0
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get library details: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get library details: {str(e)}")


@router.get("/libraries/{library_key}/content")
async def get_library_content(
    library_key: str,
    limit: int = 50,
    offset: int = 0
):
    """
    Get content from a specific library with pagination
    """
    try:
        server = plex_connection.get_connection()
        library = server.library.sectionByID(library_key)
        
        # Get all items and paginate
        all_items = library.all()
        total_count = len(all_items)
        paginated_items = all_items[offset:offset + limit]
        
        items = []
        for item in paginated_items:
            items.append(PlexMediaItem(
                key=str(item.key),
                title=item.title,
                type=item.type,
                year=item.year if hasattr(item, 'year') else None,
                rating=item.rating if hasattr(item, 'rating') else None,
                summary=item.summary if hasattr(item, 'summary') else None,
                thumb=item.thumb if hasattr(item, 'thumb') else None,
                art=item.art if hasattr(item, 'art') else None,
                duration=item.duration if hasattr(item, 'duration') else None,
                added_at=item.addedAt if hasattr(item, 'addedAt') else None,
                updated_at=item.updatedAt if hasattr(item, 'updatedAt') else None,
            ))
        
        return {
            "items": items,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total_count
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get library content: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get library content: {str(e)}")


@router.get("/libraries/{library_key}/stats")
async def get_library_stats(library_key: str):
    """
    Get statistics for a specific library
    
    Returns detailed statistics including size, count, recently added, etc.
    """
    try:
        server = plex_connection.get_connection()
        library = server.library.sectionByID(library_key)
        
        all_items = library.all()
        total_items = len(all_items)
        
        # Get recently added (last 10 items)
        recently_added = sorted(
            all_items, 
            key=lambda x: x.addedAt if hasattr(x, 'addedAt') and x.addedAt else datetime.min, 
            reverse=True
        )[:10]
        
        # Calculate total duration/size if applicable
        total_duration = sum(
            item.duration for item in all_items 
            if hasattr(item, 'duration') and item.duration
        ) / 1000 / 60  # Convert to minutes
        
        return {
            "library_key": library_key,
            "library_name": library.title,
            "library_type": library.type,
            "total_items": total_items,
            "total_duration_minutes": int(total_duration),
            "recently_added_count": len(recently_added),
            "last_scanned": library.scannedAt.isoformat() if hasattr(library, 'scannedAt') and library.scannedAt else None,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get library stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get library stats: {str(e)}")
