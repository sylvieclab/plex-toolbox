# Quick Start Guide - No Docker Required!

## The Easiest Way to Get Started

### Option 1: Simple Start (Recommended for Testing)

This method uses SQLite (no database installation needed) and works without Redis.

1. **Run the setup script:**
   ```batch
   cd C:\Users\Administrator\Documents\Github\plex-toolbox
   setup-dev.bat
   ```

2. **Start everything:**
   ```batch
   start-simple.bat
   ```

This will:
- Set up Python virtual environment
- Install all dependencies
- Start backend with SQLite database
- Start frontend
- Open browser to http://localhost:3000

**That's it!** You can now:
- Access frontend at http://localhost:3000
- Access API at http://localhost:8000
- View API docs at http://localhost:8000/api/docs

### Option 2: Manual Start (More Control)

If you prefer to run backend and frontend separately:

#### Terminal 1 - Backend
```batch
cd C:\Users\Administrator\Documents\Github\plex-toolbox
start-backend.bat
```

#### Terminal 2 - Frontend
```batch
cd C:\Users\Administrator\Documents\Github\plex-toolbox
start-frontend.bat
```

## Testing Your Setup

1. **Check Backend Health:**
   Open http://localhost:8000/api/health in your browser
   
   You should see:
   ```json
   {
     "status": "healthy",
     "timestamp": "...",
     "service": "plex-toolbox-backend"
   }
   ```

2. **Check Frontend:**
   Open http://localhost:3000
   
   You should see the Plex Toolbox setup page

3. **Check API Documentation:**
   Open http://localhost:8000/api/docs
   
   You should see the interactive API documentation (Swagger UI)

## Connecting to Your Plex Server

1. Open http://localhost:3000
2. You'll see the setup page
3. Enter your Plex server information:
   - **URL**: Your Plex server address (e.g., `http://192.168.1.100:32400`)
   - **Token**: Your Plex authentication token

### Finding Your Plex Token

1. Open Plex Web App (https://app.plex.tv)
2. Play any media item
3. Click the three dots (...) > "Get Info"
4. Click "View XML"
5. Look for `X-Plex-Token=` in the URL
6. Copy the token value

Or follow [this official guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

## What Works Without PostgreSQL/Redis?

✅ **Works:**
- Basic API functionality
- Plex server connection
- Library browsing
- Library statistics
- Health checks
- API documentation

❌ **Doesn't Work:**
- Background scanning tasks (requires Celery/Redis)
- Some advanced features that need task queues

## Troubleshooting

### "Python is not recognized"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### "Node is not recognized"
- Install Node.js from https://nodejs.org/
- Choose the LTS version

### Port 8000 or 3000 already in use
```batch
# Find what's using the port
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <process_id> /F
```

### Backend won't start
1. Check if Python virtual environment was created:
   ```batch
   dir backend\venv
   ```
2. If not, create it manually:
   ```batch
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Frontend won't start
1. Check if node_modules exists:
   ```batch
   dir frontend\node_modules
   ```
2. If not, install manually:
   ```batch
   cd frontend
   npm install
   ```

### Can't connect to Plex
- Verify your Plex server is running
- Check your Plex URL is correct (include the port)
- Verify your token is correct
- Make sure you can access Plex from your browser at that URL

## Stopping the Servers

- **If using start-simple.bat**: Press `Ctrl+C` in the terminal window
- **If using separate terminals**: Press `Ctrl+C` in each terminal window

## File Locations

- **Backend logs**: `backend/logs/plex-toolbox.log`
- **SQLite database**: `backend/plex_toolbox.db`
- **Backend config**: `backend/.env`
- **Frontend config**: `frontend/.env`

## Next Steps

Once you have everything running:

1. **Connect to Plex** using the setup page
2. **Browse your libraries** (once we implement the UI)
3. **Test API endpoints** using http://localhost:8000/api/docs
4. **Start developing features!**

## Need More Features?

For full functionality (background tasks, etc.), you'll need:
- PostgreSQL (instead of SQLite)
- Redis (for Celery task queue)

See `Claude_Docs/LOCAL_DEVELOPMENT_SETUP.md` for full setup instructions.

## Development Tips

### Backend Changes
- Auto-reloads when you save Python files
- Check logs in terminal for errors
- Access logs at `backend/logs/plex-toolbox.log`

### Frontend Changes
- Auto-reloads when you save React files
- Check browser console (F12) for errors
- React error overlay shows errors in the browser

### Testing API Endpoints
- Use the Swagger UI at http://localhost:8000/api/docs
- Click "Try it out" to test endpoints directly
- View request/response formats

---

**You're all set!** 🎉

The simplest path is:
1. Run `setup-dev.bat` (once)
2. Run `start-simple.bat` (every time you want to develop)
3. Open http://localhost:3000 in your browser

Happy coding! 🚀
