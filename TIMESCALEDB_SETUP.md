# TimescaleDB Setup Guide for Plex Toolbox

## ✅ Step 1: TimescaleDB Container on Unraid (DO THIS FIRST)

### Install via Unraid Docker UI:

1. **Docker Tab** → **Add Container**

2. **Basic Configuration:**
   - **Name:** `timescaledb`
   - **Repository:** `timescale/timescaledb:latest-pg16`
   - **Network Type:** `Bridge`

3. **Port Mapping:**
   - **Container Port:** `5432`
   - **Host Port:** `5432` (or use different port if 5432 is taken)
   - **Connection Type:** `TCP`

4. **Environment Variables:**
   ```
   POSTGRES_DB=plex_toolbox
   POSTGRES_USER=plextoolbox
   POSTGRES_PASSWORD=YourSecurePasswordHere
   TIMESCALEDB_TELEMETRY=off
   ```

5. **Volume Mapping:**
   - **Container Path:** `/var/lib/postgresql/data`
   - **Host Path:** `/mnt/user/appdata/timescaledb`
   - **Access Mode:** `Read/Write`

6. Click **Apply**

---

## ✅ Step 2: Verify Container is Running

**Option A: Unraid Console**
1. Docker Tab → Click timescaledb → Console
2. Run: `psql -U plextoolbox -d plex_toolbox`
3. Should see PostgreSQL prompt. Type `\q` to exit.

**Option B: From Windows (if you have psql installed)**
```bash
psql -h [UNRAID_IP] -U plextoolbox -d plex_toolbox
```

---

## ✅ Step 3: Enable TimescaleDB Extension

Connect to database and run:

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
\dx
```

You should see `timescaledb` in the extensions list.

---

## ✅ Step 4: Update Plex Toolbox Backend

### 4.1: Install PostgreSQL Driver

Open a terminal in your backend directory and run:

```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend
pip install psycopg2-binary==2.9.9
```

Or if using virtual environment:
```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend
.venv\Scripts\activate  # If using venv
pip install -r requirements.txt
```

### 4.2: Update .env File

I've created a template file `.env.timescaledb` for you. 

**Edit this file and replace:**
- `YOUR_UNRAID_IP` → Your actual Unraid server IP (e.g., 192.168.1.100)
- `YOUR_PASSWORD` → The password you set in Step 1

Then rename it:
```bash
# Backup your current .env
copy .env .env.backup

# Use the TimescaleDB config
copy .env.timescaledb .env
```

**Your .env should look like:**
```env
DATABASE_URL=postgresql://plextoolbox:YourPassword@192.168.1.100:5432/plex_toolbox
ENVIRONMENT=development
PROJECT_NAME=Plex Toolbox
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
SECRET_KEY=dev-secret-key
```

---

## ✅ Step 5: Initialize Database Schema

Run these commands to create the initial database tables:

```bash
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend

# Option A: Using Python directly
python -c "from app.db.session import init_db; init_db()"

# Option B: Using your app startup (if you have a main.py)
python -m uvicorn app.main:app --reload
```

The app should start and create all the necessary tables in TimescaleDB.

---

## ✅ Step 6: Verify Everything Works

1. **Start your backend:**
   ```bash
   cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start your frontend:**
   ```bash
   cd C:\Users\Administrator\Documents\Github\plex-toolbox\frontend
   npm start
   ```

3. **Test the Statistics page** - Your existing data should work the same way!

---

## 🔧 Troubleshooting

### Can't connect to database
- Check Unraid IP is correct
- Verify port 5432 is accessible (check firewall)
- Make sure container is running in Docker tab
- Check password is correct

### "No module named 'psycopg2'"
- Run: `pip install psycopg2-binary`

### Tables not created
- Run: `python -c "from app.db.session import init_db; init_db()"`
- Check logs for errors

---

## 🎯 Next Steps (After Basic Connection Works)

1. **Create Time-Series Models** for statistics storage
2. **Add Background Task** to collect stats every 5-30 minutes
3. **Create History API Endpoints** to query historical data
4. **Add Retention Policies** to auto-delete old data
5. **Implement Continuous Aggregates** for daily/weekly/monthly rollups

---

## 📊 Benefits of TimescaleDB

- ✅ All your existing code works (it's just PostgreSQL!)
- ✅ Ready for time-series statistics when we add them
- ✅ Can query historical trends efficiently
- ✅ Automatic data compression for older stats
- ✅ Production-ready and scalable

---

## 🔐 Security Notes (For Production Later)

- Change `SECRET_KEY` to a secure random string
- Use stronger passwords
- Consider using connection pooling
- Add SSL/TLS for database connections
- Restrict database access to only Plex Toolbox container

---

## Questions?

If you run into any issues during setup, let me know:
1. What step you're on
2. Any error messages
3. Container logs (if applicable)
