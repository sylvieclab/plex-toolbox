"""
Check database schema for scan_history table
"""
import sqlite3
import os

db_path = 'plex_toolbox.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("SCAN HISTORY TABLE SCHEMA")
print("=" * 60)

cursor.execute("PRAGMA table_info(scan_history)")
columns = cursor.fetchall()

print("\nColumns in scan_history table:")
print("-" * 60)
for col in columns:
    col_id, name, col_type, not_null, default, pk = col
    nullable = "NOT NULL" if not_null else "NULL"
    pk_status = "PRIMARY KEY" if pk else ""
    print(f"{name:20} {col_type:15} {nullable:10} {pk_status}")

print("\n" + "=" * 60)
print("CHECKING REQUIRED COLUMNS")
print("=" * 60)

required_columns = {
    'scan_type': 'VARCHAR',
    'path': 'VARCHAR',
    'duration_seconds': 'REAL',
    'library_type': 'VARCHAR'
}

column_names = {col[1]: col[2] for col in columns}

print("\nRequired columns check:")
for col_name, expected_type in required_columns.items():
    if col_name in column_names:
        actual_type = column_names[col_name]
        print(f"✅ {col_name:20} - Present ({actual_type})")
    else:
        print(f"❌ {col_name:20} - MISSING!")

print("\n" + "=" * 60)
print("SAMPLE DATA")
print("=" * 60)

cursor.execute("""
    SELECT id, library_name, scan_type, path, duration_seconds, status 
    FROM scan_history 
    ORDER BY started_at DESC 
    LIMIT 5
""")

rows = cursor.fetchall()
if rows:
    print("\nMost recent scans:")
    print("-" * 60)
    for row in rows:
        scan_id, lib_name, scan_type, path, duration, status = row
        path_display = path if path else "(entire library)"
        print(f"ID: {scan_id} | {lib_name:20} | {scan_type:8} | {status:10} | {duration}s")
        print(f"       Path: {path_display}")
else:
    print("\nNo scan history records found")

conn.close()

print("\n" + "=" * 60)
print("✅ Database schema check complete!")
print("=" * 60)
