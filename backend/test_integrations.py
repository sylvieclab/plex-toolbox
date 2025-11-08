"""
Quick test script for integration APIs
Tests all integration endpoints to verify they're working
"""
import asyncio
import sys
from loguru import logger

# Add parent directory to path
sys.path.append(".")

from app.services.integrations import SabnzbdClient, SonarrClient, RadarrClient, ProwlarrClient


async def test_sabnzbd():
    """Test SABnzbd connection"""
    logger.info("Testing SABnzbd...")
    
    # Replace with your actual values
    url = "http://localhost:8080"
    api_key = "YOUR-API-KEY-HERE"
    
    client = SabnzbdClient(url, api_key)
    
    try:
        success, message, version = await client.test_connection()
        if success:
            logger.success(f"✓ SABnzbd: {message} (v{version})")
            
            # Test queue
            queue = await client.get_queue()
            logger.info(f"  Queue has {len(queue.get('queue', {}).get('slots', []))} items")
            
            # Test status
            status = await client.get_status()
            logger.info(f"  Status: Speed={status['speed']}, Paused={status['paused']}")
            
        else:
            logger.error(f"✗ SABnzbd: {message}")
    except Exception as e:
        logger.error(f"✗ SABnzbd: {e}")


async def test_sonarr():
    """Test Sonarr connection"""
    logger.info("Testing Sonarr...")
    
    # Replace with your actual values
    url = "http://localhost:8989"
    api_key = "YOUR-API-KEY-HERE"
    
    client = SonarrClient(url, api_key)
    
    try:
        success, message, version = await client.test_connection()
        if success:
            logger.success(f"✓ Sonarr: {message} (v{version})")
            
            # Test series
            series = await client.get_series()
            logger.info(f"  Found {len(series)} series")
            
        else:
            logger.error(f"✗ Sonarr: {message}")
    except Exception as e:
        logger.error(f"✗ Sonarr: {e}")


async def test_radarr():
    """Test Radarr connection"""
    logger.info("Testing Radarr...")
    
    # Replace with your actual values
    url = "http://localhost:7878"
    api_key = "YOUR-API-KEY-HERE"
    
    client = RadarrClient(url, api_key)
    
    try:
        success, message, version = await client.test_connection()
        if success:
            logger.success(f"✓ Radarr: {message} (v{version})")
            
            # Test movies
            movies = await client.get_movies()
            logger.info(f"  Found {len(movies)} movies")
            
        else:
            logger.error(f"✗ Radarr: {message}")
    except Exception as e:
        logger.error(f"✗ Radarr: {e}")


async def test_prowlarr():
    """Test Prowlarr connection"""
    logger.info("Testing Prowlarr...")
    
    # Replace with your actual values
    url = "http://localhost:9696"
    api_key = "YOUR-API-KEY-HERE"
    
    client = ProwlarrClient(url, api_key)
    
    try:
        success, message, version = await client.test_connection()
        if success:
            logger.success(f"✓ Prowlarr: {message} (v{version})")
            
            # Test indexers
            indexers = await client.get_indexers()
            logger.info(f"  Found {len(indexers)} indexers")
            
        else:
            logger.error(f"✗ Prowlarr: {message}")
    except Exception as e:
        logger.error(f"✗ Prowlarr: {e}")


async def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Integration Client Tests")
    logger.info("=" * 60)
    logger.info("")
    logger.warning("⚠️  Edit this file to add your actual URLs and API keys!")
    logger.info("")
    
    # Test each service
    await test_sabnzbd()
    logger.info("")
    
    await test_sonarr()
    logger.info("")
    
    await test_radarr()
    logger.info("")
    
    await test_prowlarr()
    logger.info("")
    
    logger.info("=" * 60)
    logger.success("Testing complete!")


if __name__ == "__main__":
    asyncio.run(main())
