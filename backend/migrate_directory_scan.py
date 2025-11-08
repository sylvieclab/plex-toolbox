"""
Migration: Add duration_seconds to scan_history table
This migration ensures all required columns exist for directory scanning feature
"""
import sqlite3
import os

def migrate():
    db_path = 'plex_toolbox.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        print("Database will be created automatically when the app starts.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(scan_history)")
        columns = [col[1] for col in cursor.fetchall()]
        
        changes_made = False
        
        # Check and add path column
        if 'path' not in columns:
            print("Adding 'path' column...")
            cursor.execute('ALTER TABLE scan_history ADD COLUMN path TEXT')
            print("✓ Added 'path' column")
            changes_made = True
        else:
            print("✓ 'path' column already exists")
        
        # Check and add scan_type column
        if 'scan_type' not in columns:
            print("Adding 'scan_type' column...")
            cursor.execute("ALTER TABLE scan_history ADD COLUMN scan_type TEXT DEFAULT 'full'")
            print("✓ Added 'scan_type' column")
            changes_made = True
        else:
            print("✓ 'scan_type' column already exists")
        
        # Check and add duration_seconds column
        if 'duration_seconds' not in columns:
            print("Adding 'duration_seconds' column...")
            cursor.execute('ALTER TABLE scan_history ADD COLUMN duration_seconds REAL')
            print("✓ Added 'duration_seconds' column")
            changes_made = True
        else:
            print("✓ 'duration_seconds' column already exists")
        
        if changes_made:
            conn.commit()
            print("\n✅ Migration completed successfully!")
        else:
            print("\n✅ All columns already exist - no migration needed")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting migration: Add directory scanning fields")
    print("=" * 50)
    migrate()
