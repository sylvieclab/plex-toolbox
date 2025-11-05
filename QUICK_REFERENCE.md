# 🚀 Plex Toolbox - Quick Reference Card

## Starting Development

```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox
start-simple.bat
```

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web UI |
| Backend | http://localhost:8000 | API Server |
| API Docs | http://localhost:8000/api/docs | Interactive API Documentation |
| Health Check | http://localhost:8000/api/health | Server Status |

## Quick Commands

| Command | Purpose |
|---------|---------|
| `start-simple.bat` | Start both backend and frontend |
| `start-backend.bat` | Start backend only |
| `start-frontend.bat` | Start frontend only |
| `cleanup.bat` | Remove all dependencies |
| `full-reset.bat` | Clean install everything |
| `fix-frontend.bat` | Fix frontend dependency issues |

## Project Structure

```
plex-toolbox/
├── backend/           # FastAPI + Python
│   ├── app/          # Application code
│   └── venv/         # Virtual environment
├── frontend/         # React + TypeScript
│   ├── src/          # Source code
│   └── node_modules/ # Dependencies
└── Claude_Docs/      # Documentation
```

## Current Status

✅ **Backend**: Running on port 8000  
✅ **Frontend**: Running on port 3000  
✅ **Database**: SQLite initialized  
✅ **Plex**: Connected to "Montahulu"  

## Next Priorities

1. 🔧 Database persistence
2. 📚 Libraries page
3. 🔍 Selective scanning
4. 📊 Dashboard enhancements

## Important Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | Backend entry point |
| `frontend/src/App.tsx` | Frontend entry point |
| `Claude_Docs/NEXT_SESSION_ROADMAP.md` | Detailed next steps |
| `Claude_Docs/API_REFERENCE.md` | API documentation |

## Troubleshooting

**Backend won't start?**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
cd frontend
npm install --force
```

**Both fail?**
```bash
full-reset.bat
```

## Tech Stack

**Backend**: FastAPI, SQLAlchemy, PlexAPI, Uvicorn  
**Frontend**: React, TypeScript, Material-UI, Zustand  
**Database**: SQLite (local file)  
**Dev Tools**: Python 3.13, Node.js 18+  

## Documentation

📖 **NEXT_SESSION_ROADMAP.md** - Start here next time  
📖 **THIS_SESSION_SUMMARY.md** - What we built today  
📖 **API_REFERENCE.md** - All API endpoints  
📖 **QUICK_START.md** - Getting started guide  

---

**Last Updated**: 2025-11-03  
**Version**: 0.1.0  
**Status**: ✅ Working!
