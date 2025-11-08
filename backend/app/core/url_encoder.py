"""
URL Encoder Utility for Database Passwords
Use this to encode passwords with special characters for DATABASE_URL
"""
from urllib.parse import quote_plus
import sys


def encode_password(password: str) -> str:
    """
    Encode a password for use in a database URL
    Handles special characters like: @ : / ? # [ ] ! $ & ' ( ) * + , ; = %
    """
    return quote_plus(password)


def build_database_url(username: str, password: str, host: str, port: str, database: str) -> str:
    """Build a complete database URL with encoded password"""
    encoded_password = encode_password(password)
    return f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}"


def main():
    print("=" * 70)
    print("Database Password URL Encoder")
    print("=" * 70)
    print()
    print("This tool helps you encode passwords with special characters")
    print("for use in DATABASE_URL connection strings.")
    print()
    print("Special characters that need encoding:")
    print("  @ : / ? # [ ] ! $ & ' ( ) * + , ; = %")
    print()
    print("-" * 70)
    
    # Option 1: Just encode a password
    print("\nOption 1: Encode password only")
    print("Option 2: Build complete DATABASE_URL")
    print()
    
    choice = input("Choose option (1 or 2): ").strip()
    print()
    
    if choice == '1':
        # Just encode password
        password = input("Enter password to encode: ").strip()
        
        if not password:
            print("❌ Password cannot be empty")
            sys.exit(1)
        
        encoded = encode_password(password)
        
        print()
        print("=" * 70)
        print("✅ Encoded Password:")
        print("-" * 70)
        print(f"Original:  {password}")
        print(f"Encoded:   {encoded}")
        print()
        print("Use the encoded version in your DATABASE_URL:")
        print(f"DATABASE_URL=postgresql://username:{encoded}@host:5432/database")
        print("=" * 70)
        
    elif choice == '2':
        # Build complete URL
        print("Enter database connection details:")
        print("-" * 70)
        
        username = input("Username [plextoolbox]: ").strip() or "plextoolbox"
        password = input("Password: ").strip()
        host = input("Host (e.g., 192.168.1.100): ").strip()
        port = input("Port [5432]: ").strip() or "5432"
        database = input("Database name [plex_toolbox]: ").strip() or "plex_toolbox"
        
        if not password:
            print("❌ Password cannot be empty")
            sys.exit(1)
        
        if not host:
            print("❌ Host cannot be empty")
            sys.exit(1)
        
        database_url = build_database_url(username, password, host, port, database)
        encoded_password = encode_password(password)
        
        print()
        print("=" * 70)
        print("✅ Database Configuration:")
        print("-" * 70)
        print(f"Username:          {username}")
        print(f"Password:          {password}")
        print(f"Encoded Password:  {encoded_password}")
        print(f"Host:              {host}")
        print(f"Port:              {port}")
        print(f"Database:          {database}")
        print()
        print("Complete DATABASE_URL:")
        print("-" * 70)
        print(database_url)
        print()
        print("Copy this line to your .env file:")
        print("-" * 70)
        print(f"DATABASE_URL={database_url}")
        print("=" * 70)
    else:
        print("❌ Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
