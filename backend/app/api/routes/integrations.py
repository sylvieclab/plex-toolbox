"""
API routes for integration management
Handles CRUD operations for integration configurations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from loguru import logger

from app.db.session import get_db
from app.models.integrations import IntegrationConfig
from app.schemas.integrations import (
    IntegrationConfigCreate,
    IntegrationConfigUpdate,
    IntegrationConfigResponse,
    IntegrationConfigFull,
    IntegrationTestRequest,
    IntegrationTestResponse,
)
from app.services.integrations import (
    SonarrClient,
    RadarrClient,
    SabnzbdClient,
    ProwlarrClient,
)

router = APIRouter(prefix="/integrations", tags=["integrations"])


def get_client(service_type: str, url: str, api_key: str):
    """Get the appropriate client for the service type"""
    clients = {
        "sonarr": SonarrClient,
        "radarr": RadarrClient,
        "sabnzbd": SabnzbdClient,
        "prowlarr": ProwlarrClient,
    }
    
    client_class = clients.get(service_type.lower())
    if not client_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown service type: {service_type}"
        )
    
    return client_class(url, api_key)


@router.post("/test", response_model=IntegrationTestResponse)
async def test_integration_connection(request: IntegrationTestRequest):
    """
    Test connection to an integration service
    
    This endpoint tests the connection to Sonarr, Radarr, SABnzbd, or Prowlarr
    without saving the configuration.
    """
    try:
        client = get_client(request.service_type, request.url, request.api_key)
        success, message, version = await client.test_connection()
        
        return IntegrationTestResponse(
            success=success,
            message=message,
            version=version,
            error=None if success else message
        )
    except Exception as e:
        logger.error(f"Integration test failed: {str(e)}")
        return IntegrationTestResponse(
            success=False,
            message="Connection test failed",
            error=str(e)
        )


@router.post("", response_model=IntegrationConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_integration(
    config: IntegrationConfigCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new integration configuration
    
    Creates a new integration for Sonarr, Radarr, SABnzbd, or Prowlarr.
    The connection is tested before saving.
    """
    # Test connection before saving
    try:
        client = get_client(config.service_type, config.url, config.api_key)
        success, message, version = await client.test_connection()
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Connection test failed: {message}"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Connection test failed: {str(e)}"
        )
    
    # Create the integration
    db_config = IntegrationConfig(**config.model_dump())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    logger.info(f"Created integration: {config.name} ({config.service_type})")
    
    return db_config.to_dict()


@router.get("", response_model=List[IntegrationConfigResponse])
async def list_integrations(
    service_type: str = None,
    enabled: bool = None,
    db: Session = Depends(get_db)
):
    """
    List all integration configurations
    
    Optionally filter by service type and/or enabled status.
    """
    query = db.query(IntegrationConfig)
    
    if service_type:
        query = query.filter(IntegrationConfig.service_type == service_type)
    
    if enabled is not None:
        query = query.filter(IntegrationConfig.enabled == enabled)
    
    configs = query.all()
    return [config.to_dict() for config in configs]


@router.get("/{config_id}", response_model=IntegrationConfigFull)
async def get_integration(config_id: int, db: Session = Depends(get_db)):
    """
    Get a specific integration configuration
    
    Returns the full configuration including the complete API key.
    """
    config = db.query(IntegrationConfig).filter(IntegrationConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration with ID {config_id} not found"
        )
    
    return config.to_dict_full()


@router.put("/{config_id}", response_model=IntegrationConfigResponse)
async def update_integration(
    config_id: int,
    update: IntegrationConfigUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an integration configuration
    
    Only provided fields will be updated. If URL or API key is changed,
    the connection is tested before saving.
    """
    config = db.query(IntegrationConfig).filter(IntegrationConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration with ID {config_id} not found"
        )
    
    # Test connection if URL or API key is being updated
    if update.url or update.api_key:
        test_url = update.url or config.url
        test_api_key = update.api_key or config.api_key
        
        try:
            client = get_client(config.service_type, test_url, test_api_key)
            success, message, version = await client.test_connection()
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Connection test failed: {message}"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Connection test failed: {str(e)}"
            )
    
    # Update fields
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    
    logger.info(f"Updated integration: {config.name} (ID: {config.id})")
    
    return config.to_dict()


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_integration(config_id: int, db: Session = Depends(get_db)):
    """
    Delete an integration configuration
    """
    config = db.query(IntegrationConfig).filter(IntegrationConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration with ID {config_id} not found"
        )
    
    logger.info(f"Deleting integration: {config.name} (ID: {config.id})")
    
    db.delete(config)
    db.commit()
    
    return None
