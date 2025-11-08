"""
Sonarr client for TV show management
"""
from typing import Optional, Dict, Any, List
from loguru import logger
from .base import BaseIntegrationClient


class SonarrClient(BaseIntegrationClient):
    """Client for Sonarr API v3"""
    
    async def test_connection(self) -> tuple[bool, str, Optional[str]]:
        """Test connection to Sonarr"""
        try:
            data = await self.get_system_status()
            version = data.get("version", "Unknown")
            return True, "Successfully connected to Sonarr", version
        except Exception as e:
            logger.error(f"Sonarr connection test failed: {str(e)}")
            return False, f"Connection failed: {str(e)}", None
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get Sonarr system status"""
        return await self._request("GET", "/api/v3/system/status")
    
    async def get_series(self) -> List[Dict[str, Any]]:
        """Get all series from Sonarr"""
        return await self._request("GET", "/api/v3/series")
    
    async def get_missing_episodes(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """Get missing episodes"""
        return await self._request(
            "GET",
            "/api/v3/wanted/missing",
            params={"page": page, "pageSize": page_size, "sortKey": "airDateUtc", "sortDirection": "descending"}
        )
    
    async def search_episodes(self, episode_ids: List[int]) -> Dict[str, Any]:
        """Search for specific episodes"""
        return await self._request(
            "POST",
            "/api/v3/command",
            json_data={"name": "EpisodeSearch", "episodeIds": episode_ids}
        )
    
    async def get_queue(self) -> Dict[str, Any]:
        """Get download queue"""
        return await self._request("GET", "/api/v3/queue")
    
    async def get_calendar(self, start: str, end: str) -> List[Dict[str, Any]]:
        """Get upcoming episodes"""
        return await self._request(
            "GET",
            "/api/v3/calendar",
            params={"start": start, "end": end}
        )
