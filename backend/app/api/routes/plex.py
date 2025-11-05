"""
Plex server connection and management routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from loguru import logger

from app.services.plex.connection import plex_connection
from app.db.session import get_db
from app.models.plex import PlexServerConfig

router = APIRouter()


class PlexConnectionConfig(BaseModel):
    """Plex connection configuration"""
    url: str
    token: str


class PlexServerInfo(BaseModel):
    """Plex server information response"""
    name: str
    version: str
    platform: str
    platform_version: str
    machine_identifier: str


@router.post("/test-connection")
async def test_plex_connection(config: PlexConnectionConfig):
    """
    Test connection to Plex server without saving
    
    This endpoint tests the connection to a Plex server using the provided
    URL and token. It does not save the configuration.
    """
    try:
        result = plex_connection.test_connection(config.url, config.token)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to test connection: {str(e)}")


@router.post("/config")
async def save_plex_config(config: PlexConnectionConfig, db: Session = Depends(get_db)):
    """
    Save Plex connection configuration to database
    
    Saves the Plex server URL and token to the database for persistent use.
    Also tests the connection before saving.
    """
    try:
        # Test connection first
        test_result = plex_connection.test_connection(config.url, config.token)
        if not test_result["success"]:
            raise HTTPException(status_code=400, detail=test_result["error"])
        
        # Save to database
        db_config = db.query(PlexServerConfig).first()
        if db_config:
            db_config.url = config.url
            db_config.token = config.token
            db_config.name = test_result.get("server_name")
            db_config.version = test_result.get("version")
            db_config.platform = test_result.get("platform")
        else:
            db_config = PlexServerConfig(
                url=config.url,
                token=config.token,
                name=test_result.get("server_name"),
                version=test_result.get("version"),
                platform=test_result.get("platform")
            )
            db.add(db_config)
        
        db.commit()
        db.refresh(db_config)
        
        # Update in-memory connection
        plex_connection.set_config(config.url, config.token)
        
        logger.info(f"Plex config saved: {test_result.get('server_name')}")
        
        return {
            "status": "success",
            "message": "Plex configuration saved",
            "server_name": test_result.get("server_name")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save Plex config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_plex_config(db: Session = Depends(get_db)):
    """
    Get current Plex configuration from database
    
    Returns the saved configuration (without the token for security).
    """
    try:
        db_config = db.query(PlexServerConfig).first()
        if db_config:
            return {
                "configured": True,
                "url": db_config.url,
                "server_name": db_config.name,
                "version": db_config.version,
                "platform": db_config.platform
            }
        return {"configured": False}
    except Exception as e:
        logger.error(f"Failed to get Plex config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/server-info")
async def get_server_info():
    """
    Get Plex server information from active connection
    
    Returns detailed server information if connected.
    """
    try:
        server = plex_connection.get_connection()
        return {
            "server_name": server.friendlyName,
            "version": server.version,
            "platform": server.platform,
            "platform_version": server.platformVersion,
            "library_count": len(server.library.sections()),
            "transcoder_video": server.transcoderVideoQualities,
            "my_plex_username": server.myPlexUsername if hasattr(server, 'myPlexUsername') else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get server info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/libraries")
async def get_libraries():
    """
    Get all Plex libraries
    
    Returns a list of all libraries with basic information.
    """
    try:
        server = plex_connection.get_connection()
        libraries = []
        
        for section in server.library.sections():
            libraries.append({
                "key": section.key,
                "title": section.title,
                "type": section.type,
                "total_items": section.totalSize,
                "agent": section.agent,
                "scanner": section.scanner,
                "language": section.language,
                "uuid": section.uuid,
                "updated_at": section.updatedAt.isoformat() if section.updatedAt else None,
                "created_at": section.createdAt.isoformat() if section.createdAt else None
            })
        
        return {"libraries": libraries}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get libraries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/libraries/{library_key}")
async def get_library_details(library_key: str):
    """
    Get detailed information about a specific library
    """
    try:
        server = plex_connection.get_connection()
        section = server.library.sectionByID(int(library_key))
        
        return {
            "key": section.key,
            "title": section.title,
            "type": section.type,
            "total_items": section.totalSize,
            "agent": section.agent,
            "scanner": section.scanner,
            "language": section.language,
            "uuid": section.uuid,
            "refreshing": section.refreshing,
            "locations": [loc for loc in section.locations],
            "updated_at": section.updatedAt.isoformat() if section.updatedAt else None,
            "created_at": section.createdAt.isoformat() if section.createdAt else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get library details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/libraries/{library_key}/scan")
async def scan_library(library_key: str):
    """
    Trigger a scan of a specific library
    """
    try:
        server = plex_connection.get_connection()
        section = server.library.sectionByID(int(library_key))
        section.refresh()
        
        return {
            "status": "success",
            "message": f"Scan initiated for library: {section.title}",
            "library_key": library_key
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to scan library: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
