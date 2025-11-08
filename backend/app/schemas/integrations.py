"""
Pydantic schemas for integration API requests/responses
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime


class IntegrationConfigBase(BaseModel):
    """Base schema for integration configuration"""
    service_type: str = Field(..., description="Type of service: sonarr, radarr, sabnzbd, prowlarr")
    name: str = Field(..., description="User-friendly name for this integration")
    url: str = Field(..., description="Base URL of the service")
    api_key: str = Field(..., description="API key for authentication")
    enabled: bool = Field(default=True, description="Whether this integration is active")


class IntegrationConfigCreate(IntegrationConfigBase):
    """Schema for creating a new integration"""
    pass


class IntegrationConfigUpdate(BaseModel):
    """Schema for updating an integration"""
    name: Optional[str] = None
    url: Optional[str] = None
    api_key: Optional[str] = None
    enabled: Optional[bool] = None


class IntegrationConfigResponse(IntegrationConfigBase):
    """Schema for integration responses (with masked API key)"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class IntegrationConfigFull(IntegrationConfigBase):
    """Schema for integration with full API key (for editing)"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class IntegrationTestRequest(BaseModel):
    """Schema for testing an integration connection"""
    service_type: str
    url: str
    api_key: str


class IntegrationTestResponse(BaseModel):
    """Schema for integration test response"""
    success: bool
    message: str
    version: Optional[str] = None
    error: Optional[str] = None
