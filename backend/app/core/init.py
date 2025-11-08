"""
Startup initialization script for Plex Toolbox
This script runs before the application starts and ensures proper configuration
"""
import os
import sys
import secrets
from pathlib import Path
from urllib.parse import quote_plus
from loguru import logger

# Get the backend directory
BACKEND_DIR = Path(__file__).parent.parent.parent
ENV_FILE = BACKEND_DIR / ".env"
ENV_EXAMPLE = BACKEND_DIR / ".env.example"


def generate_secret_key() -> str:
    """Generate a secure random secret key"""
    return secrets.token_hex(32)


def validate_database_url(database_url: str) -> bool:
    """
    Validate database URL format and warn about special characters
    Returns True if valid, False if contains issues
    """
    if not database_url:
        return False
    
    # Check for placeholder values
    if 'YOUR_PASSWORD' in database_url or 'YOUR_DATABASE_HOST' in database_url:
        return False
    
    # Check if it's a PostgreSQL URL with potential special characters
    if database_url.startswith('postgresql://'):
        # Extract the password portion (between : and @)
        try:
            # Format: postgresql://user:password@host:port/database
            if ':' in database_url and '@' in database_url:
                parts = database_url.split('://', 1)[1]  # Remove protocol
                auth_part = parts.split('@', 1)[0]  # Get user:password
                if ':' in auth_part:
                    password = auth_part.split(':', 1)[1]
                    
                    # Check for unencoded special characters
                    special_chars = ['@', ':', '/', '?', '#', '[', ']', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=', '%']
                    unencoded_chars = [char for char in special_chars if char in password and f'%{ord(char):02X}' not in password]
                    
                    if unencoded_chars:
                        logger.warning("⚠️  Password contains special characters that may need URL encoding:")
                        logger.warning(f"   Found: {', '.join(unencoded_chars)}")
                        logger.warning("   If connection fails, use the URL encoding tool:")
                        logger.warning("   python -m app.core.url_encoder")
                        return True  # Still valid, just warn
        except:
            pass  # If parsing fails, let SQLAlchemy handle it
    
    return True


def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    if ENV_FILE.exists():
        logger.info(".env file already exists")
        return
    
    logger.warning(".env file not found! Creating from .env.example...")
    
    if not ENV_EXAMPLE.exists():
        logger.error(".env.example not found! Cannot create .env file.")
        logger.error("Please create .env.example or manually create .env file")
        sys.exit(1)
    
    # Read the example file
    with open(ENV_EXAMPLE, 'r') as f:
        content = f.read()
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    # Replace the placeholder secret key with a real one
    content = content.replace(
        'change-this-to-a-random-secret-key-in-production',
        secret_key
    )
    
    # Write to .env
    with open(ENV_FILE, 'w') as f:
        f.write(content)
    
    logger.success(f"Created .env file at {ENV_FILE}")
    logger.warning("IMPORTANT: Please edit .env and configure your database connection!")
    logger.warning("  - Update DATABASE_URL with your actual database credentials")
    logger.warning("  - The SECRET_KEY has been automatically generated for you")
    logger.warning("  - If your password has special characters, use: python -m app.core.url_encoder")
    logger.info("")
    logger.info("Example database configurations:")
    logger.info("  SQLite (dev):       DATABASE_URL=sqlite:///./plex_toolbox.db")
    logger.info("  PostgreSQL (local): DATABASE_URL=postgresql://user:pass@localhost:5432/plex_toolbox")
    logger.info("  TimescaleDB (prod): DATABASE_URL=postgresql://user:pass@192.168.1.100:5432/plex_toolbox")
    logger.info("")


def check_env_configuration():
    """Check if critical environment variables are configured"""
    if not ENV_FILE.exists():
        logger.error(".env file not found after initialization!")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)
    
    database_url = os.getenv('DATABASE_URL', '')
    secret_key = os.getenv('SECRET_KEY', '')
    
    warnings = []
    errors = []
    
    # Check DATABASE_URL
    if not database_url:
        errors.append("DATABASE_URL is not set")
    elif not validate_database_url(database_url):
        errors.append("DATABASE_URL contains placeholder values - please update with real credentials")
    
    # Check SECRET_KEY
    if not secret_key:
        errors.append("SECRET_KEY is not set")
    elif secret_key == 'change-this-to-a-random-secret-key-in-production':
        warnings.append("SECRET_KEY is using the default value - it should be randomly generated")
    
    # Report findings
    if errors:
        logger.error("Configuration errors found:")
        for error in errors:
            logger.error(f"  ❌ {error}")
        logger.error("\nPlease edit .env file and fix these issues before starting the application.")
        logger.info("\nIf your password has special characters, encode it with:")
        logger.info("  python -m app.core.url_encoder")
        return False
    
    if warnings:
        logger.warning("Configuration warnings:")
        for warning in warnings:
            logger.warning(f"  ⚠️  {warning}")
    
    logger.success("✅ Environment configuration looks good!")
    return True


def initialize():
    """Main initialization function"""
    logger.info("="*60)
    logger.info("Plex Toolbox - Startup Initialization")
    logger.info("="*60)
    
    # Create .env if it doesn't exist
    create_env_file()
    
    # Check configuration
    config_ok = check_env_configuration()
    
    logger.info("="*60)
    
    return config_ok


if __name__ == "__main__":
    # When run directly, just initialize and exit
    if initialize():
        logger.success("Initialization complete!")
        sys.exit(0)
    else:
        logger.error("Initialization failed - please fix configuration errors")
        sys.exit(1)
