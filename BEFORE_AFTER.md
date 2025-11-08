# Totarr Rename - Before & After Reference

Quick visual reference of what changed from "Plex Toolbox" to "Totarr"

---

## Application Display Names

### Browser Tab Title
```diff
- Plex Toolbox
+ Totarr
```

### App Header (Top Navigation Bar)
```diff
- Plex Toolbox
+ Totarr
```

### Meta Description
```diff
- Advanced management tools for Plex Media Server
+ Advanced management and monitoring for Plex, Jellyfin, and the *arr ecosystem
```

---

## Package & Project Names

### Frontend Package
```diff
- "name": "plex-toolbox-frontend"
+ "name": "totarr-frontend"
```

### Backend Project Name
```diff
- PROJECT_NAME: str = "Plex Toolbox"
+ PROJECT_NAME: str = "Totarr"
```

---

## Database Names

### PostgreSQL/TimescaleDB
```diff
# Database name
- plex_toolbox
+ totarr

# Username
- plextoolbox
+ totarr

# Full connection string
- postgresql://plextoolbox:password@host:5432/plex_toolbox
+ postgresql://totarr:password@host:5432/totarr
```

### SQLite
```diff
- plex_toolbox.db
+ totarr.db
```

---

## File & Directory Names

### Log Files
```diff
- backend/logs/plex-toolbox.log
+ backend/logs/totarr.log
```

### Project Directory (Optional)
```diff
- C:\Users\Administrator\Documents\Github\plex-toolbox
+ C:\Users\Administrator\Documents\Github\totarr
```

### Docker Service Names
```diff
- plex-toolbox
+ totarr
```

---

## API & Service Names

### FastAPI Description
```diff
- "Advanced management tools for Plex Media Server"
+ "Advanced management and monitoring for Plex, Jellyfin, and the *arr ecosystem"
```

### Health Check Response
```diff
- "service": "plex-toolbox-backend"
+ "service": "totarr-backend"
```

### Startup Logs
```diff
- "Starting Plex Toolbox application"
+ "Starting Totarr application"
```

---

## Documentation Paths

### Project Structure
```diff
- plex-toolbox/
+ totarr/
  ├── backend/
  ├── frontend/
  └── ...
```

---

## What DIDN'T Change

These remain the same:

✅ **API Endpoints** - All routes unchanged
- `/api/health`
- `/api/plex/*`
- `/api/library/*`
- `/api/statistics/*`
- `/api/integrations/*`
- etc.

✅ **Port Numbers**
- Backend: `8000`
- Frontend: `3000`

✅ **Directory Structure**
- `backend/` folder
- `frontend/` folder
- `Claude_Docs/` folder

✅ **Integration Data**
- All stored configurations remain valid
- Plex tokens still work
- API keys still work

✅ **Features & Functionality**
- Everything works exactly the same
- Just with a better name!

---

## Side-by-Side Comparison

### Old URLs
```
http://localhost:3000  → Shows "Plex Toolbox"
http://localhost:8000  → "plex-toolbox-backend"
```

### New URLs
```
http://localhost:3000  → Shows "Totarr"
http://localhost:8000  → "totarr-backend"
```

*(Same URLs, different display names)*

---

## Example .env File

### Before
```bash
PROJECT_NAME=Plex Toolbox
DATABASE_URL=postgresql://plextoolbox:pass@host:5432/plex_toolbox
```

### After
```bash
PROJECT_NAME=Totarr
DATABASE_URL=postgresql://totarr:pass@host:5432/totarr
```

---

## Visual Changes Users Will See

### 1. Browser Tab
```
[Icon] Plex Toolbox    →    [Icon] Totarr
```

### 2. Application Header
```
≡ Plex Toolbox         →    ≡ Totarr
```

### 3. Logs
```
2025-11-08 | Starting Plex Toolbox application
↓
2025-11-08 | Starting Totarr application
```

---

## Migration Summary

| Item | Old Value | New Value | Action Required |
|------|-----------|-----------|-----------------|
| **App Name** | Plex Toolbox | Totarr | ✅ Done |
| **Database Name** | plex_toolbox | totarr | ⚠️ Optional |
| **Database User** | plextoolbox | totarr | ⚠️ Optional |
| **Log File** | plex-toolbox.log | totarr.log | ✅ Auto-created |
| **Package Name** | plex-toolbox-frontend | totarr-frontend | ✅ Done |
| **Directory Name** | plex-toolbox | totarr | ⚠️ Optional |
| **Config Values** | Updated in files | New defaults | ✅ Done |

Legend:
- ✅ Done = Already changed in code
- ⚠️ Optional = Your choice (see POST_RENAME_CHECKLIST.md)

---

## Quick Reference Card

**Old Name:** Plex Toolbox  
**New Name:** Totarr

**Pronunciation:** "toe-tar"  
**Meaning:** "Tot" (all/whole) + "arr" (*arr ecosystem)

**Old Focus:** Plex management tools  
**New Focus:** Central hub for Plex, Jellyfin, and all *arr apps

**Tech Stack:** Same (React + FastAPI + TimescaleDB)  
**Features:** Enhanced (now manages entire ecosystem)

---

**Remember:** This is just a name change + scope expansion. All your existing functionality, integrations, and data remain intact! 🎉
