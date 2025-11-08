"""
Radarr client for movie management
"""
from typing import Optional, Dict, Any, List
from loguru import logger
from .base import BaseIntegrationClient


class RadarrClient(BaseIntegrationClient):
    """Client for Radarr API v3"""
    
    async def test_connection(self) -> tuple[bool, str, Optional[str]]:
        """Test connection to Radarr"""
        try:
            data = await self.get_system_status()
            version = data.get("version", "Unknown")
            return True, "Successfully connected to Radarr", version
        except Exception as e:
            logger.error(f"Radarr connection test failed: {str(e)}")
            return False, f"Connection failed: {str(e)}", None
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get Radarr system status"""
        return await self._request("GET", "/api/v3/system/status")
    
    async def get_movies(self) -> List[Dict[str, Any]]:
        """Get all movies from Radarr"""
        return await self._request("GET", "/api/v3/movie")
    
    async def get_missing_movies(self) -> List[Dict[str, Any]]:
        """Get missing movies (monitored but not downloaded)"""
        movies = await self.get_movies()
        return [m for m in movies if m.get("monitored") and not m.get("hasFile")]
    
    async def search_movies(self, movie_ids: List[int]) -> Dict[str, Any]:
        """Search for specific movies"""
        return await self._request(
            "POST",
            "/api/v3/command",
            json_data={"name": "MoviesSearch", "movieIds": movie_ids}
        )
    
    async def get_queue(self) -> Dict[str, Any]:
        """Get download queue"""
        return await self._request("GET", "/api/v3/queue")
