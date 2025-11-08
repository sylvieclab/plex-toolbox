# Post-Rename Checklist

## ✅ Completed Changes

All of these have been done for you:

- [x] **Frontend package.json** - Updated package name
- [x] **Frontend index.html** - Updated title and description
- [x] **Layout component** - Updated app name in header
- [x] **Backend config.py** - Updated PROJECT_NAME and database defaults
- [x] **Backend main.py** - Updated log files and descriptions
- [x] **Backend .env.example** - Updated all database references
- [x] **README.md** - Complete rewrite with new name and scope
- [x] **DATABASE_SETUP.md** - Updated all references
- [x] **QUICK_START.md** - Updated all references
- [x] **START_HERE.md** - Updated project description
- [x] **HANDOFF_SUMMARY.md** - Updated project references
- [x] **WELCOME.md** - Created new welcome document
- [x] **RENAME_SUMMARY.md** - Created documentation of changes

---

## 🔄 Optional: Actions for You

These are things you may want to do (but they're optional):

### 1. Rename the Directory (Optional)
```bash
cd C:\Users\Administrator\Documents\Github
# Close any open terminals/IDEs first
rename plex-toolbox totarr
```

### 2. Update Git Repository (If Applicable)
If you have this on GitHub/GitLab:

**On GitHub:**
1. Go to repository Settings
2. Change repository name to `totarr`
3. Update local remote:
   ```bash
   git remote set-url origin https://github.com/yourusername/totarr.git
   ```

### 3. Clean Up Old Files (Optional)
You may want to delete:
- `backend/logs/plex-toolbox.log` (old log file)
- `backend/plex_toolbox.db` (old SQLite database - if you have one)

**Note:** The app will create new files (`totarr.log` and `totarr.db`) automatically.

### 4. Update Environment Variables (If Using .env)
If you already have a `.env` file:

**Check your DATABASE_URL:**
```bash
# Old format (if using PostgreSQL)
DATABASE_URL=postgresql://plextoolbox:password@host:5432/plex_toolbox

# New format (update to)
DATABASE_URL=postgresql://totarr:password@host:5432/totarr
```

**If still using SQLite:**
```bash
# Old (will still work but creates old filename)
DATABASE_URL=sqlite:///./plex_toolbox.db

# New (recommended - creates new filename)
DATABASE_URL=sqlite:///./totarr.db
```

### 5. Restart Your Application
```bash
# Stop any running instances (Ctrl+C in terminals)

# Start fresh
start-simple.bat

# Or manually:
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# (new terminal)
cd frontend
npm start
```

### 6. Clear Browser Cache (Optional)
To see the new name immediately:
- Chrome/Edge: `Ctrl+Shift+Delete` → Clear cached images and files
- Or just do a hard refresh: `Ctrl+F5`

---

## 🧪 Testing Checklist

Verify everything still works:

### Backend Tests
- [ ] Backend starts without errors
- [ ] Can access http://localhost:8000/api/health
- [ ] API docs load at http://localhost:8000/api/docs
- [ ] New log file created: `backend/logs/totarr.log`
- [ ] Database connection works

### Frontend Tests
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:3000
- [ ] Page title shows "Totarr" (check browser tab)
- [ ] App header shows "Totarr"
- [ ] All pages load correctly

### Integration Tests (If Already Configured)
- [ ] Plex connection still works
- [ ] Library scanning still works
- [ ] Radarr integration still works (if configured)
- [ ] Sonarr integration still works (if configured)
- [ ] SABnzbd integration still works (if configured)
- [ ] Prowlarr integration still works (if configured)
- [ ] Statistics page loads correctly

---

## 📋 What You DON'T Need to Do

These things are **already handled** or **not necessary**:

- ❌ Don't need to reinstall dependencies
- ❌ Don't need to reconfigure integrations (stored in database)
- ❌ Don't need to update API endpoints (they're the same)
- ❌ Don't need to change any code
- ❌ Don't need to rebuild/recompile anything
- ❌ Don't need to migrate data (unless changing database name)

---

## 🐛 If Something Breaks

### "Module not found" errors
```bash
cd backend
pip install -r requirements.txt --break-system-packages

cd frontend
npm install
```

### "Can't connect to database"
Check your `.env` file - make sure DATABASE_URL is correct.

### Old data not showing
If you renamed the database from `plex_toolbox` to `totarr`, your data is in the old database. Either:
- Use the old database name (keep `DATABASE_URL` pointing to `plex_toolbox`)
- Migrate data to new database
- Start fresh with new database

### Integration configs disappeared
If using SQLite and changed the database filename, your configs are in the old database. Either:
- Point DATABASE_URL back to `plex_toolbox.db`
- Reconfigure integrations (only takes a minute)

---

## 💡 Pro Tips

1. **Keep the old database name** initially if you want to keep all your data
2. **Test thoroughly** before deleting any old files
3. **Take a backup** of your `.env` file before making changes
4. **One change at a time** - don't rename everything at once if issues arise

---

## 🎯 Recommended Next Steps

After confirming everything works:

1. **Test the application** - Make sure all features work
2. **Update your documentation** - If you have any custom docs
3. **Update bookmarks** - If you have any saved URLs
4. **Tell your users** - If others use your instance
5. **Consider a new release** - Tag this as v0.4.0 "Totarr Rename"

---

## 📞 Need Help?

If you encounter any issues:

1. Check `backend/logs/totarr.log` for backend errors
2. Check browser console (F12) for frontend errors
3. Verify `.env` configuration
4. Check that all services are running
5. Review the error messages carefully

Most issues are usually:
- Database configuration (check DATABASE_URL)
- Missing dependencies (run installs again)
- Port conflicts (check nothing else using 3000/8000)
- Old cached files (clear browser cache)

---

**That's it! Your project is now Totarr!** 🎉

The rename is complete and ready to go. Just test it out and optionally do the items in the "Optional Actions" section above.
