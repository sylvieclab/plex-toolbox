"""
Plex connection service - Singleton pattern for global Plex connection
"""
from plexapi.server import PlexServer
from plexapi.exceptions import Unauthorized, BadRequest
from typing import Optional
from loguru import logger


class PlexConnection:
    """Singleton service for managing Plex server connection"""
    
    def __init__(self):
        self._url: Optional[str] = None
        self._token: Optional[str] = None
        self._server: Optional[PlexServer] = None
    
    def set_config(self, url: str, token: str):
        """Set Plex server configuration"""
        self._url = url
        self._token = token
        self._server = None  # Reset connection
        logger.info(f"Plex config updated: {url}")
    
    def get_connection(self) -> PlexServer:
        """Get or create Plex server connection"""
        if not self._url or not self._token:
            raise ValueError("Plex server not configured. Please configure in Settings.")
        
        if self._server is None:
            try:
                self._server = PlexServer(self._url, self._token)
                logger.info(f"Connected to Plex server: {self._server.friendlyName}")
            except Unauthorized:
                raise ValueError("Invalid Plex token")
            except BadRequest as e:
                raise ValueError(f"Failed to connect to Plex server: {str(e)}")
            except Exception as e:
                raise ValueError(f"Unexpected error connecting to Plex: {str(e)}")
        
        return self._server
    
    def test_connection(self, url: str, token: str) -> dict:
        """Test connection to Plex server"""
        try:
            server = PlexServer(url, token)
            return {
                "success": True,
                "server_name": server.friendlyName,
                "version": server.version,
                "platform": server.platform,
                "library_count": len(server.library.sections())
            }
        except Unauthorized:
            return {
                "success": False,
                "error": "Invalid Plex token"
            }
        except BadRequest as e:
            return {
                "success": False,
                "error": f"Failed to connect: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def is_configured(self) -> bool:
        """Check if Plex is configured"""
        return self._url is not None and self._token is not None
    
    def get_server_info(self) -> dict:
        """Get basic server information"""
        if not self.is_configured():
            return {"configured": False}
        
        try:
            server = self.get_connection()
            return {
                "configured": True,
                "server_name": server.friendlyName,
                "version": server.version,
                "platform": server.platform,
                "library_count": len(server.library.sections())
            }
        except Exception as e:
            logger.error(f"Failed to get server info: {str(e)}")
            return {
                "configured": True,
                "error": str(e)
            }


# Global singleton instance
plex_connection = PlexConnection()
