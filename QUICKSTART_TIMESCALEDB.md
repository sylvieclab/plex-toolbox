# 🚀 TimescaleDB Setup - Quick Start

## Files Created for You

1. **TIMESCALEDB_SETUP.md** - Complete step-by-step setup guide
2. **UNRAID_DOCKER_TEMPLATE.md** - Quick copy/paste values for Unraid
3. **.env.timescaledb** - Template environment configuration
4. **requirements.txt** - Updated with PostgreSQL driver (psycopg2-binary)
5. **test_database.py** - Script to test connection and initialize database

---

## 🎯 Setup Checklist (Do in Order)

### ☐ 1. Set Up TimescaleDB on Unraid (15 minutes)

**Use:** `UNRAID_DOCKER_TEMPLATE.md` for quick copy/paste

1. Open Unraid → Docker → Add Container
2. Copy/paste settings from template
3. **IMPORTANT:** Set a secure password for `POSTGRES_PASSWORD`
4. Click Apply and wait for container to start
5. Verify container is running (green status)

**Enable TimescaleDB:**
```bash
# In Unraid console (Docker Tab → timescaledb → Console)
psql -U plextoolbox -d plex_toolbox
CREATE EXTENSION IF NOT EXISTS timescaledb;
\dx
\q
```

---

### ☐ 2. Update Plex Toolbox Backend (5 minutes)

**A. Install PostgreSQL Driver:**
```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend
pip install psycopg2-binary
```

**B. Configure Database Connection:**
```bash
# Edit .env.timescaledb file
# Replace YOUR_UNRAID_IP with actual IP (e.g., 192.168.1.100)
# Replace YOUR_PASSWORD with the password from Step 1

# Backup current .env
copy .env .env.backup

# Use TimescaleDB config
copy .env.timescaledb .env
```

---

### ☐ 3. Test Connection (2 minutes)

```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend
python test_database.py
```

This script will:
- ✅ Test database connection
- ✅ Verify TimescaleDB extension is installed
- ✅ List existing tables
- ✅ Offer to initialize database tables

**Expected Output:**
```
✅ Connected to PostgreSQL!
✅ TimescaleDB extension is installed!
📊 Found X tables: [or "No tables found"]
Do you want to initialize database tables? (y/n):
```

Type `y` to create all tables.

---

### ☐ 4. Start Development (1 minute)

**Backend:**
```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\frontend
npm start
```

**Test:** Open http://localhost:3000 and check Statistics page

---

## 🎉 What You Get

- ✅ **Production-ready database** on your Unraid server
- ✅ **Same functionality** - all existing code works
- ✅ **Ready for time-series** - we'll add statistics history next
- ✅ **Scalable** - can handle millions of data points
- ✅ **Persistent** - data survives restarts
- ✅ **Network accessible** - can connect from anywhere on your network

---

## 🔍 Troubleshooting

### "Can't connect to database"
1. Check Unraid IP is correct in `.env`
2. Verify container is running: Unraid → Docker → look for green icon
3. Test port is open: `telnet [UNRAID_IP] 5432` (should connect)
4. Check password matches what you set

### "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### "TimescaleDB extension not found"
Run in Unraid console:
```bash
# Docker Tab → timescaledb → Console
psql -U plextoolbox -d plex_toolbox -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

### Container won't start
1. Check Docker logs: Docker Tab → timescaledb → Logs
2. Verify appdata folder has correct permissions
3. Try different host port (e.g., 5433 instead of 5432)

---

## 📞 Need Help?

Tell me:
1. Which step you're on
2. Error message (exact text)
3. What you've tried

Let's get this working! 🚀

---

## 🎯 Next Steps (After Basic Setup Works)

Once your connection is working, we'll:
1. **Create time-series models** for statistics
2. **Add background task** to collect stats every 5-30 min
3. **Create history endpoints** to view trends
4. **Add data retention** to auto-cleanup old data
5. **Build charts/graphs** to visualize trends

But first - let's get the basic connection working! 🎉
