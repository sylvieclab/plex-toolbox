"""
Plex-related Pydantic schemas
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime


class PlexConnectionConfig(BaseModel):
    """Plex server connection configuration"""
    url: str = Field(..., description="Plex server URL (e.g., http://192.168.1.100:32400)")
    token: str = Field(..., description="Plex authentication token")


class PlexServerInfo(BaseModel):
    """Plex server information"""
    name: str
    version: str
    platform: str
    platform_version: str
    machine_identifier: str


class PlexLibrary(BaseModel):
    """Plex library information"""
    key: str
    title: str
    type: str
    agent: Optional[str] = None
    scanner: Optional[str] = None
    language: Optional[str] = None
    uuid: str
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    scanned_at: Optional[datetime] = None
    content_count: int = 0


class LibraryScanRequest(BaseModel):
    """Request to scan a library"""
    library_key: str = Field(..., description="Library section key")
    path: Optional[str] = Field(None, description="Optional specific path to scan")


class LibraryScanResponse(BaseModel):
    """Response from library scan"""
    status: str
    library_key: str
    library_name: str
    message: str
    started_at: datetime


class PlexMediaItem(BaseModel):
    """Generic Plex media item"""
    key: str
    title: str
    type: str
    year: Optional[int] = None
    rating: Optional[float] = None
    summary: Optional[str] = None
    thumb: Optional[str] = None
    art: Optional[str] = None
    duration: Optional[int] = None
    added_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PlexTVShow(PlexMediaItem):
    """Plex TV Show"""
    season_count: int = 0
    episode_count: int = 0
    studio: Optional[str] = None
    content_rating: Optional[str] = None


class PlexMovie(PlexMediaItem):
    """Plex Movie"""
    studio: Optional[str] = None
    content_rating: Optional[str] = None
    tagline: Optional[str] = None
