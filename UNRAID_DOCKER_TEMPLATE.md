# TimescaleDB Unraid Docker Template - Quick Copy/Paste

## Container Settings (Copy these values)

### Basic
```
Name: timescaledb
Repository: timescale/timescaledb:latest-pg16
Network Type: Bridge
```

### Port Mappings
```
Container Port: 5432
Host Port: 5432
Connection Type: TCP
```

### Environment Variables (Click "Add another Path, Port, Variable..." for each)

**Variable 1:**
```
Config Type: Variable
Name: POSTGRES_DB
Key: POSTGRES_DB
Value: plex_toolbox
```

**Variable 2:**
```
Config Type: Variable
Name: POSTGRES_USER
Key: POSTGRES_USER
Value: plextoolbox
```

**Variable 3:**
```
Config Type: Variable
Name: POSTGRES_PASSWORD
Key: POSTGRES_PASSWORD
Value: [YOUR_SECURE_PASSWORD_HERE]
```

**Variable 4:**
```
Config Type: Variable
Name: TIMESCALEDB_TELEMETRY
Key: TIMESCALEDB_TELEMETRY
Value: off
```

### Volume Mappings

**Path 1:**
```
Config Type: Path
Name: Database Data
Container Path: /var/lib/postgresql/data
Host Path: /mnt/user/appdata/timescaledb
Access Mode: Read/Write
```

---

## After Container Starts

### Enable TimescaleDB Extension

**Via Unraid Console:**
1. Docker Tab → timescaledb → Console
2. Run:
```bash
psql -U plextoolbox -d plex_toolbox
```
3. In psql prompt:
```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
\dx
\q
```

**Via Windows (if psql installed):**
```bash
psql -h [YOUR_UNRAID_IP] -U plextoolbox -d plex_toolbox -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

---

## Connection String for Plex Toolbox

```
postgresql://plextoolbox:[YOUR_PASSWORD]@[YOUR_UNRAID_IP]:5432/plex_toolbox
```

Example:
```
postgresql://plextoolbox:mySecurePass123@192.168.1.100:5432/plex_toolbox
```

---

## Verify Container is Working

**Check logs:**
```
Docker Tab → timescaledb → Logs
```

Should see:
```
database system is ready to accept connections
```

**Test connection from Windows:**
```bash
# If you have psql installed
psql -h [UNRAID_IP] -U plextoolbox -d plex_toolbox

# If you have Python
python -c "import psycopg2; conn = psycopg2.connect('postgresql://plextoolbox:[PASSWORD]@[IP]:5432/plex_toolbox'); print('Connected!'); conn.close()"
```
