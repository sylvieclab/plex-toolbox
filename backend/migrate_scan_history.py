"""
Database migration: Add library_type column to scan_history table

This script adds the missing library_type column to the scan_history table.
"""
import sqlite3
import os

# Get database path
db_path = os.path.join(os.path.dirname(__file__), 'plex_toolbox.db')

print(f"Connecting to database: {db_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check current schema
    print("\n=== Current scan_history schema ===")
    cursor.execute("PRAGMA table_info(scan_history)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Check if library_type column exists
    column_names = [col[1] for col in columns]
    
    if 'library_type' not in column_names:
        print("\n=== Adding library_type column ===")
        cursor.execute("ALTER TABLE scan_history ADD COLUMN library_type VARCHAR")
        conn.commit()
        print("✅ Successfully added library_type column")
    else:
        print("\n✅ library_type column already exists")
    
    # Show updated schema
    print("\n=== Updated scan_history schema ===")
    cursor.execute("PRAGMA table_info(scan_history)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    print("\n✅ Migration complete!")
    
except Exception as e:
    print(f"\n❌ Migration failed: {e}")
    conn.rollback()
    raise

finally:
    conn.close()

print("\nYou can now restart the backend server.")
