"""
Quick fix: Add duration_seconds column to scan_history table
Run this from the backend directory
"""
import sqlite3
import os

def fix_database():
    db_path = 'plex_toolbox.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        print("Make sure you're in the backend directory!")
        return False
    
    print("Connecting to database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current columns
        cursor.execute("PRAGMA table_info(scan_history)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"\nCurrent columns: {', '.join(columns)}")
        
        # Check if duration_seconds exists
        if 'duration_seconds' in columns:
            print("\n✅ duration_seconds column already exists!")
            return True
        
        # Add the column
        print("\nAdding duration_seconds column...")
        cursor.execute('ALTER TABLE scan_history ADD COLUMN duration_seconds REAL')
        conn.commit()
        
        print("✅ Successfully added duration_seconds column!")
        
        # Verify
        cursor.execute("PRAGMA table_info(scan_history)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'duration_seconds' in columns:
            print("✅ Verified: Column was added successfully")
            return True
        else:
            print("❌ Error: Column was not added")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("QUICK FIX: Add duration_seconds column")
    print("=" * 60)
    
    if fix_database():
        print("\n✅ Database fixed! Restart your backend server.")
    else:
        print("\n❌ Fix failed. Check the error messages above.")
    
    print("=" * 60)
