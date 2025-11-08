"""
Plex server configuration model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from app.models.base import Base, TimestampMixin


class PlexServerConfig(Base, TimestampMixin):
    """
    Stores Plex server connection configuration
    Only one configuration should exist at a time (singleton)
    """
    __tablename__ = "plex_server_config"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    token = Column(String, nullable=False)
    name = Column(String, nullable=True)
    machine_identifier = Column(String, nullable=True, unique=True)
    version = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_connected = Column(DateTime, nullable=True)


class ScanHistory(Base, TimestampMixin):
    """
    Stores history of library scans
    """
    __tablename__ = "scan_history"
    
    id = Column(Integer, primary_key=True, index=True)
    library_key = Column(String, nullable=False)
    library_name = Column(String, nullable=False)
    library_type = Column(String, nullable=False)  # 'movie', 'show', 'music', etc.
    scan_type = Column(String, nullable=False, default='full')  # 'full' or 'partial'
    path = Column(String, nullable=True)  # Specific path if partial scan
    status = Column(String, nullable=False)  # 'started', 'completed', 'failed'
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)  # NEW: Duration in seconds


class UserSettings(Base, TimestampMixin):
    """
    Stores user preferences and settings
    """
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String, unique=True, nullable=False)
    setting_value = Column(String, nullable=False)
    description = Column(String, nullable=True)
