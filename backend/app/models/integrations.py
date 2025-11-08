"""
Integration configuration models
Stores connection details for Sonarr, Radarr, SABnzbd, and Prowlarr
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .base import Base, TimestampMixin


class IntegrationConfig(Base, TimestampMixin):
    """Store configuration for external integrations"""
    __tablename__ = "integration_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String, nullable=False, index=True)  # sonarr, radarr, sabnzbd, prowlarr
    name = Column(String, nullable=False)  # User-friendly name (e.g., "Main Sonarr", "4K Radarr")
    url = Column(String, nullable=False)  # Base URL (e.g., "http://localhost:8989")
    api_key = Column(String, nullable=False)  # API key for authentication
    enabled = Column(Boolean, default=True, nullable=False)  # Whether this integration is active
    
    def __repr__(self):
        return f"<IntegrationConfig(id={self.id}, service_type={self.service_type}, name={self.name})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "service_type": self.service_type,
            "name": self.name,
            "url": self.url,
            "api_key": self.api_key[:8] + "..." if self.api_key else None,  # Mask API key in responses
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def to_dict_full(self):
        """Convert to dictionary including full API key (for editing)"""
        return {
            "id": self.id,
            "service_type": self.service_type,
            "name": self.name,
            "url": self.url,
            "api_key": self.api_key,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
