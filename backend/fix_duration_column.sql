-- Quick fix: Add duration_seconds column to scan_history
-- Run this in the backend directory where plex_toolbox.db is located

ALTER TABLE scan_history ADD COLUMN duration_seconds REAL;
