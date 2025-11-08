"""
Prowlarr client for indexer management
"""
from typing import Optional, Dict, Any, List
from loguru import logger
from .base import BaseIntegrationClient


class ProwlarrClient(BaseIntegrationClient):
    """Client for Prowlarr API v1"""
    
    async def test_connection(self) -> tuple[bool, str, Optional[str]]:
        """Test connection to Prowlarr"""
        try:
            data = await self.get_system_status()
            version = data.get("version", "Unknown")
            return True, "Successfully connected to Prowlarr", version
        except Exception as e:
            logger.error(f"Prowlarr connection test failed: {str(e)}")
            return False, f"Connection failed: {str(e)}", None
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get Prowlarr system status"""
        return await self._request("GET", "/api/v1/system/status")
    
    async def get_indexers(self) -> List[Dict[str, Any]]:
        """Get all indexers"""
        return await self._request("GET", "/api/v1/indexer")
    
    async def get_indexer_stats(self) -> Dict[str, Any]:
        """Get indexer statistics"""
        return await self._request("GET", "/api/v1/indexerstats")
    
    async def test_indexer(self, indexer_id: int) -> Dict[str, Any]:
        """Test specific indexer"""
        return await self._request("POST", f"/api/v1/indexer/test/{indexer_id}")
