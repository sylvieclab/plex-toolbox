# Project Rename Summary: Plex Toolbox → Totarr

**Date:** November 8, 2025  
**Reason:** Expanding scope beyond Plex to include all *arr apps (Radarr, Sonarr, SABnzbd, Prowlarr) and Jellyfin

---

## ✅ Files Updated

### Frontend Files
1. **`frontend/package.json`**
   - Package name: `plex-toolbox-frontend` → `totarr-frontend`

2. **`frontend/public/index.html`**
   - Title: `Plex Toolbox` → `Totarr`
   - Description: Updated to reflect broader scope

3. **`frontend/src/components/common/Layout.tsx`**
   - App bar title: `Plex Toolbox` → `Totarr`

### Backend Files
4. **`backend/app/core/config.py`**
   - `PROJECT_NAME`: `"Plex Toolbox"` → `"Totarr"`
   - `DATABASE_URL` default: `plextoolbox` → `totarr` (database name and user)

5. **`backend/app/main.py`**
   - Log file: `logs/plex-toolbox.log` → `logs/totarr.log`
   - FastAPI description: Updated to reflect full ecosystem
   - Startup/shutdown log messages: Updated app name

6. **`backend/.env.example`**
   - All database URLs: `plex_toolbox` → `totarr` (database name)
   - Database user: `plextoolbox` → `totarr`
   - `PROJECT_NAME`: `Plex Toolbox` → `Totarr`
   - Header comments: Updated

### Documentation Files
7. **`README.md`**
   - Title: `Plex Toolbox` → `Totarr`
   - Description: Expanded to include Jellyfin and *arr ecosystem
   - All references updated throughout
   - Project structure path: `plex-toolbox/` → `totarr/`

8. **`DATABASE_SETUP.md`**
   - All references to `Plex Toolbox` → `Totarr`
   - Database names: `plex_toolbox` → `totarr`
   - Database users: `plextoolbox` → `totarr`
   - Docker service names updated

9. **`Claude_Docs/START_HERE.md`**
   - Title: Updated
   - Project description: Expanded scope
   - File path: Updated to reflect new name
   - Added services list (Plex, Radarr, Sonarr, SABnzbd, Prowlarr, Jellyfin planned)

10. **`Claude_Docs/HANDOFF_SUMMARY.md`**
    - Title: Updated
    - Project structure: `plex-toolbox/` → `totarr/`
    - File paths: Updated

---

## 📝 Name Changes Summary

### Application Names
- **Old:** Plex Toolbox
- **New:** Totarr

### Database Names
- **Old:** 
  - Database: `plex_toolbox`
  - User: `plextoolbox`
  - SQLite file: `plex_toolbox.db`
- **New:**
  - Database: `totarr`
  - User: `totarr`
  - SQLite file: `totarr.db`

### Docker/Service Names
- **Old:** `plex-toolbox`, `plextoolbox`
- **New:** `totarr`

### Package Names
- **Old:** `plex-toolbox-frontend`
- **New:** `totarr-frontend`

### Log Files
- **Old:** `logs/plex-toolbox.log`
- **New:** `logs/totarr.log`

---

## 🔄 Next Steps for User

### 1. Optional: Rename Directory
If you want to rename the project directory:
```bash
# Navigate to parent directory
cd C:\Users\Administrator\Documents\Github

# Rename (Git will track this)
mv plex-toolbox totarr
cd totarr
```

### 2. Update Git Remote (if applicable)
If you have a Git remote repository:
```bash
# Update repository name on GitHub/GitLab first, then:
git remote set-url origin <new-repo-url>
```

### 3. Database Migration (Optional)
If you're currently using the old database names:

**For SQLite:**
```bash
cd backend
# Simply restart the app - it will create totarr.db
# Old plex_toolbox.db will remain (you can delete it later)
```

**For PostgreSQL/TimescaleDB:**
- If you haven't set up the database yet, follow the updated DATABASE_SETUP.md
- If you have existing data:
  1. Create new database: `CREATE DATABASE totarr;`
  2. Create new user: `CREATE USER totarr WITH PASSWORD 'yourpassword';`
  3. Grant permissions: `GRANT ALL PRIVILEGES ON DATABASE totarr TO totarr;`
  4. Export/import data if needed
  5. Update `.env` with new DATABASE_URL

### 4. Rebuild Frontend (if needed)
```bash
cd frontend
npm install  # In case package name affects anything
npm start
```

### 5. No Action Required For:
- ✅ Integration configurations (stored in database, name-agnostic)
- ✅ Plex tokens and URLs (stored in database)
- ✅ Backend dependencies
- ✅ API endpoints (unchanged)

---

## 🎯 Scope Expansion Rationale

### Old Scope (Plex Toolbox):
- Focused primarily on Plex Media Server management
- Library scanning and management
- Basic statistics

### New Scope (Totarr):
- **Central management hub** for:
  - ✅ Plex Media Server
  - ✅ Radarr (movie management)
  - ✅ Sonarr (TV show management)
  - ✅ SABnzbd (download client)
  - ✅ Prowlarr (indexer management)
  - 🔄 Jellyfin (planned)
  
- **Unified monitoring and statistics**
- **One interface to rule them all** (*arr pun intended!)

The name "Totarr" reflects:
- **Tot** = "All" or "Whole" (Latin/Germanic root)
- **arr** = Following the *arr naming convention
- **Meaning:** "All *arr apps in one place"

---

## 🐛 Known Issues / Things to Watch

1. **Browser Cache:** Users may need to clear cache to see new title
2. **Old Logs:** `logs/plex-toolbox.log` will remain (can be deleted manually)
3. **Old Database:** If using SQLite, `plex_toolbox.db` will remain (can be deleted manually)
4. **Documentation:** Some older docs may still reference old name (will update as we find them)

---

## ✨ Benefits of New Name

1. **More Accurate:** Reflects the actual purpose and scope
2. **Community Alignment:** Follows *arr naming convention, familiar to self-hosters
3. **Future-Proof:** Room to add more integrations without name being limiting
4. **Memorable:** Short, punchy, clear purpose
5. **Unique:** Not conflicting with existing tools

---

**Rename Complete! 🎉**

The application now accurately reflects its purpose as a central management hub for the entire *arr ecosystem plus media servers.
