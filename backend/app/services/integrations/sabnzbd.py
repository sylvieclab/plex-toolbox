"""
SABnzbd client for download queue and history management
"""
from typing import Optional, Dict, Any, List
import httpx
from loguru import logger
from .base import BaseIntegrationClient


class SabnzbdClient(BaseIntegrationClient):
    """Client for SABnzbd API"""
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to SABnzbd
        
        SABnzbd uses API key in URL params, not headers
        """
        url = f"{self.url}{endpoint}"
        
        # Add API key to params for SABnzbd
        if params is None:
            params = {}
        params["apikey"] = self.api_key
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Request to {url} failed: {str(e)}")
            raise
    
    async def test_connection(self) -> tuple[bool, str, Optional[str]]:
        """Test connection to SABnzbd"""
        try:
            data = await self.get_version()
            version = data.get("version", "Unknown")
            return True, "Successfully connected to SABnzbd", version
        except Exception as e:
            logger.error(f"SABnzbd connection test failed: {str(e)}")
            return False, f"Connection failed: {str(e)}", None
    
    async def get_version(self) -> Dict[str, Any]:
        """Get SABnzbd version"""
        return await self._request(
            "GET",
            "/api",
            params={"mode": "version", "output": "json"}
        )
    
    async def get_queue(self) -> Dict[str, Any]:
        """
        Get current download queue
        
        Returns:
            Queue data including active downloads, speed, ETA, etc.
        """
        return await self._request(
            "GET",
            "/api",
            params={"mode": "queue", "output": "json"}
        )
    
    async def get_history(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get download history
        
        Args:
            limit: Maximum number of history items to return
            
        Returns:
            History data including completed/failed downloads
        """
        return await self._request(
            "GET",
            "/api",
            params={
                "mode": "history",
                "limit": limit,
                "output": "json"
            }
        )
    
    async def pause_queue(self) -> Dict[str, Any]:
        """Pause all downloads"""
        return await self._request(
            "GET",
            "/api",
            params={"mode": "pause", "output": "json"}
        )
    
    async def resume_queue(self) -> Dict[str, Any]:
        """Resume all downloads"""
        return await self._request(
            "GET",
            "/api",
            params={"mode": "resume", "output": "json"}
        )
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get SABnzbd status
        
        Returns:
            Status data including speed, disk space, etc.
        """
        queue_data = await self.get_queue()
        
        # Extract key status info
        queue = queue_data.get("queue", {})
        return {
            "paused": queue.get("paused", False),
            "speed": queue.get("speed", "0"),
            "size_left": queue.get("sizeleft", "0"),
            "size": queue.get("size", "0"),
            "eta": queue.get("eta", "unknown"),
            "disk_space": queue.get("diskspace1", "unknown"),
            "slots": len(queue.get("slots", [])),
        }
    
    async def delete_history_item(self, nzo_id: str) -> Dict[str, Any]:
        """
        Delete an item from history
        
        Args:
            nzo_id: NZO ID of the history item to delete
        """
        return await self._request(
            "GET",
            "/api",
            params={
                "mode": "history",
                "name": "delete",
                "value": nzo_id,
                "output": "json"
            }
        )
    
    async def retry_download(self, nzo_id: str) -> Dict[str, Any]:
        """
        Retry a failed download
        
        Args:
            nzo_id: NZO ID of the download to retry
        """
        return await self._request(
            "GET",
            "/api",
            params={
                "mode": "retry",
                "value": nzo_id,
                "output": "json"
            }
        )
    
    async def get_server_stats(self) -> Dict[str, Any]:
        """
        Get server download statistics
        
        Returns:
            Server statistics including day/week/month/total downloads
        """
        return await self._request(
            "GET",
            "/api",
            params={
                "mode": "server_stats",
                "output": "json"
            }
        )
