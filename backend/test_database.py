"""
Test script to verify TimescaleDB connection and setup
Run this after setting up your .env file with TimescaleDB credentials
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings
from loguru import logger

def test_connection():
    """Test basic database connection"""
    logger.info("Testing database connection...")
    logger.info(f"Connecting to: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local database'}")
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            logger.success(f"✅ Connected to PostgreSQL!")
            logger.info(f"Version: {version}")
            
            # Check if TimescaleDB extension is installed
            result = conn.execute(text("""
                SELECT * FROM pg_extension WHERE extname = 'timescaledb';
            """))
            
            if result.rowcount > 0:
                logger.success("✅ TimescaleDB extension is installed!")
                
                # Get TimescaleDB version
                result = conn.execute(text("SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';"))
                ts_version = result.scalar()
                logger.info(f"TimescaleDB version: {ts_version}")
            else:
                logger.warning("⚠️  TimescaleDB extension NOT installed!")
                logger.info("Run this in psql to install:")
                logger.info("  CREATE EXTENSION IF NOT EXISTS timescaledb;")
            
            # List existing tables
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """))
            
            tables = [row[0] for row in result]
            
            if tables:
                logger.info(f"📊 Found {len(tables)} existing tables:")
                for table in tables:
                    logger.info(f"  - {table}")
            else:
                logger.info("📊 No tables found (run init_db to create them)")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        logger.error("\nTroubleshooting:")
        logger.error("1. Check your .env file has correct DATABASE_URL")
        logger.error("2. Verify TimescaleDB container is running on Unraid")
        logger.error("3. Check IP address and port are correct")
        logger.error("4. Verify username and password")
        logger.error("5. Make sure psycopg2-binary is installed: pip install psycopg2-binary")
        return False


def initialize_database():
    """Initialize database tables"""
    logger.info("\n" + "="*60)
    logger.info("Initializing database tables...")
    
    try:
        from app.db.session import init_db
        init_db()
        logger.success("✅ Database tables created successfully!")
        
        # Verify tables were created
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """))
            tables = [row[0] for row in result]
            logger.info(f"📊 Created {len(tables)} tables:")
            for table in tables:
                logger.info(f"  - {table}")
                
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {str(e)}")
        return False


def main():
    """Main test function"""
    logger.info("="*60)
    logger.info("TimescaleDB Connection Test")
    logger.info("="*60)
    
    # Test connection
    if not test_connection():
        sys.exit(1)
    
    # Ask if user wants to initialize database
    logger.info("\n" + "="*60)
    response = input("Do you want to initialize database tables? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        if initialize_database():
            logger.success("\n✅ All tests passed! Database is ready to use.")
            logger.info("\nNext steps:")
            logger.info("1. Start your backend: python -m uvicorn app.main:app --reload")
            logger.info("2. Start your frontend: npm start")
            logger.info("3. Test the Statistics page")
        else:
            logger.error("\n❌ Database initialization failed")
            sys.exit(1)
    else:
        logger.info("\nSkipping database initialization.")
        logger.info("Run this script again or call init_db() when ready.")
    
    logger.info("\n" + "="*60)


if __name__ == "__main__":
    main()
