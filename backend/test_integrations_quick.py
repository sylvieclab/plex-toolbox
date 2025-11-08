"""
Quick Integration Test Script

This script will help you verify that:
1. Database migration has been run
2. Backend can connect to your services
3. All endpoints are working

Update the SERVICE_CONFIGS section with your actual service details.
"""

import httpx
import asyncio
from typing import Dict, Any
from loguru import logger

# ============================================================================
# CONFIGURATION - UPDATE THESE WITH YOUR ACTUAL SERVICE DETAILS
# ============================================================================

SERVICE_CONFIGS = {
    "sabnzbd": {
        "url": "http://localhost:8080",  # Update with your SABnzbd URL
        "api_key": "YOUR_SABNZBD_API_KEY_HERE",  # Update with your API key
        "enabled": True,
    },
    "sonarr": {
        "url": "http://localhost:8989",  # Update with your Sonarr URL
        "api_key": "YOUR_SONARR_API_KEY_HERE",  # Update with your API key
        "enabled": True,
    },
    "radarr": {
        "url": "http://localhost:7878",  # Update with your Radarr URL
        "api_key": "YOUR_RADARR_API_KEY_HERE",  # Update with your API key
        "enabled": True,
    },
    "prowlarr": {
        "url": "http://localhost:9696",  # Update with your Prowlarr URL
        "api_key": "YOUR_PROWLARR_API_KEY_HERE",  # Update with your API key
        "enabled": True,
    },
}

# Backend URL
BACKEND_URL = "http://localhost:8000"

# ============================================================================


class IntegrationTester:
    """Test integration setup"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results = []
    
    async def test_backend_health(self):
        """Test if backend is running"""
        logger.info("Testing backend health...")
        try:
            response = await self.client.get(f"{BACKEND_URL}/api/health")
            if response.status_code == 200:
                logger.success("✓ Backend is running")
                return True
            else:
                logger.error(f"✗ Backend returned status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"✗ Cannot connect to backend: {e}")
            logger.info("Make sure backend is running: python -m uvicorn app.main:app --reload")
            return False
    
    async def test_integration_connection(self, service_type: str, config: Dict[str, Any]):
        """Test connection to a service"""
        logger.info(f"\nTesting {service_type.upper()} connection...")
        
        try:
            response = await self.client.post(
                f"{BACKEND_URL}/api/integrations/test",
                json={
                    "service_type": service_type,
                    "url": config["url"],
                    "api_key": config["api_key"],
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    logger.success(f"✓ {service_type.upper()} connection successful")
                    logger.info(f"  Version: {data.get('version', 'Unknown')}")
                    return True, data
                else:
                    logger.error(f"✗ {service_type.upper()} connection failed")
                    logger.error(f"  Error: {data.get('error', 'Unknown error')}")
                    return False, data
            else:
                logger.error(f"✗ Request failed with status {response.status_code}")
                return False, None
                
        except Exception as e:
            logger.error(f"✗ Error testing {service_type}: {e}")
            return False, None
    
    async def add_integration(self, service_type: str, config: Dict[str, Any]):
        """Add an integration"""
        logger.info(f"Adding {service_type.upper()} integration...")
        
        try:
            response = await self.client.post(
                f"{BACKEND_URL}/api/integrations",
                json={
                    "service_type": service_type,
                    "name": f"Main {service_type.title()}",
                    "url": config["url"],
                    "api_key": config["api_key"],
                    "enabled": config["enabled"],
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                logger.success(f"✓ {service_type.upper()} integration added (ID: {data['id']})")
                return True, data
            else:
                logger.error(f"✗ Failed to add integration: {response.status_code}")
                logger.error(f"  {response.text}")
                return False, None
                
        except Exception as e:
            logger.error(f"✗ Error adding {service_type}: {e}")
            return False, None
    
    async def list_integrations(self):
        """List all configured integrations"""
        logger.info("\nListing all integrations...")
        
        try:
            response = await self.client.get(f"{BACKEND_URL}/api/integrations")
            
            if response.status_code == 200:
                data = response.json()
                logger.success(f"✓ Found {len(data)} integration(s)")
                
                for integration in data:
                    logger.info(f"  - {integration['name']} ({integration['service_type']})")
                    logger.info(f"    URL: {integration['url']}")
                    logger.info(f"    Enabled: {integration['enabled']}")
                
                return True, data
            else:
                logger.error(f"✗ Failed to list integrations: {response.status_code}")
                return False, None
                
        except Exception as e:
            logger.error(f"✗ Error listing integrations: {e}")
            return False, None
    
    async def test_service_operations(self):
        """Test basic operations for each service"""
        logger.info("\n" + "="*60)
        logger.info("Testing Service Operations")
        logger.info("="*60)
        
        # Test SABnzbd queue
        try:
            logger.info("\nTesting SABnzbd queue...")
            response = await self.client.get(f"{BACKEND_URL}/api/sabnzbd/queue")
            if response.status_code == 200:
                data = response.json()
                logger.success("✓ SABnzbd queue accessible")
                queue = data.get("queue", {})
                logger.info(f"  Active downloads: {len(queue.get('slots', []))}")
            else:
                logger.warning(f"⚠ SABnzbd queue: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠ SABnzbd operations not tested: {e}")
        
        # Test Sonarr series
        try:
            logger.info("\nTesting Sonarr series...")
            response = await self.client.get(f"{BACKEND_URL}/api/sonarr/series")
            if response.status_code == 200:
                data = response.json()
                logger.success("✓ Sonarr series accessible")
                logger.info(f"  Total series: {len(data)}")
            else:
                logger.warning(f"⚠ Sonarr series: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠ Sonarr operations not tested: {e}")
        
        # Test Radarr movies
        try:
            logger.info("\nTesting Radarr movies...")
            response = await self.client.get(f"{BACKEND_URL}/api/radarr/movies")
            if response.status_code == 200:
                data = response.json()
                logger.success("✓ Radarr movies accessible")
                logger.info(f"  Total movies: {len(data)}")
            else:
                logger.warning(f"⚠ Radarr movies: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠ Radarr operations not tested: {e}")
        
        # Test Prowlarr indexers
        try:
            logger.info("\nTesting Prowlarr indexers...")
            response = await self.client.get(f"{BACKEND_URL}/api/prowlarr/indexers")
            if response.status_code == 200:
                data = response.json()
                logger.success("✓ Prowlarr indexers accessible")
                logger.info(f"  Total indexers: {len(data)}")
            else:
                logger.warning(f"⚠ Prowlarr indexers: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠ Prowlarr operations not tested: {e}")
    
    async def run_tests(self):
        """Run all tests"""
        logger.info("="*60)
        logger.info("Integration Test Suite")
        logger.info("="*60)
        
        # Step 1: Check backend
        if not await self.test_backend_health():
            logger.error("\nBackend is not running. Please start it first:")
            logger.info("  cd backend")
            logger.info("  python -m uvicorn app.main:app --reload")
            return
        
        # Step 2: Test connections
        logger.info("\n" + "="*60)
        logger.info("Testing Service Connections")
        logger.info("="*60)
        
        successful_services = []
        
        for service_type, config in SERVICE_CONFIGS.items():
            if "YOUR_" in config["api_key"]:
                logger.warning(f"\n⚠ Skipping {service_type.upper()} - API key not configured")
                continue
            
            success, data = await self.test_integration_connection(service_type, config)
            if success:
                successful_services.append((service_type, config))
        
        if not successful_services:
            logger.error("\nNo services successfully tested.")
            logger.info("\nPlease update SERVICE_CONFIGS in this script with your actual service details.")
            return
        
        # Step 3: Add integrations
        logger.info("\n" + "="*60)
        logger.info("Adding Integrations")
        logger.info("="*60)
        
        for service_type, config in successful_services:
            await self.add_integration(service_type, config)
        
        # Step 4: List integrations
        await self.list_integrations()
        
        # Step 5: Test operations
        await self.test_service_operations()
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("Test Summary")
        logger.info("="*60)
        logger.success(f"✓ Successfully tested {len(successful_services)} service(s)")
        logger.info("\nNext steps:")
        logger.info("1. Check http://localhost:8000/api/docs for full API documentation")
        logger.info("2. Start building the frontend integration UI")
        logger.info("3. See INTEGRATION_STATUS_CURRENT.md for complete status")
        
        await self.client.aclose()


async def main():
    """Main entry point"""
    tester = IntegrationTester()
    await tester.run_tests()


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="<level>{message}</level>",
        colorize=True
    )
    
    asyncio.run(main())
