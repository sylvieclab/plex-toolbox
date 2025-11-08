"""
Base client for integration services
Provides common functionality for API calls
"""
import httpx
from typing import Optional, Dict, Any
from loguru import logger


class BaseIntegrationClient:
    """Base class for integration clients"""
    
    def __init__(self, url: str, api_key: str):
        """
        Initialize the client
        
        Args:
            url: Base URL of the service (e.g., "http://localhost:8989")
            api_key: API key for authentication
        """
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.timeout = 30.0
        
    def _get_headers(self) -> Dict[str, str]:
        """Get common headers for requests"""
        return {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the service
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/api/v3/system/status")
            params: Query parameters
            json_data: JSON body for POST/PUT requests
            
        Returns:
            Response data as dictionary
            
        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.url}{endpoint}"
        headers = self._get_headers()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_data,
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Request to {url} failed: {str(e)}")
            raise
    
    async def test_connection(self) -> tuple[bool, str, Optional[str]]:
        """
        Test connection to the service
        
        Returns:
            Tuple of (success, message, version)
        """
        raise NotImplementedError("Subclasses must implement test_connection")
