"""
Database migration to add integration_configs table

Run this script to add the integration_configs table to your database.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import inspect
from loguru import logger

from app.db.session import engine
from app.models.base import Base
from app.models.integrations import IntegrationConfig


def table_exists(table_name: str) -> bool:
    """Check if table exists in database"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def run_migration():
    """Run the migration"""
    logger.info("Starting integration configs migration...")
    
    # Check if table already exists
    if table_exists("integration_configs"):
        logger.info("✓ integration_configs table already exists, skipping migration")
        return
    
    try:
        # Create the table
        logger.info("Creating integration_configs table...")
        IntegrationConfig.__table__.create(engine)
        logger.success("✓ integration_configs table created successfully!")
        
    except Exception as e:
        logger.error(f"✗ Migration failed: {e}")
        raise


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Integration Configs Migration")
    logger.info("=" * 60)
    
    try:
        run_migration()
        logger.success("\n✓ Migration completed successfully!")
    except Exception as e:
        logger.error(f"\n✗ Migration failed: {e}")
        sys.exit(1)
