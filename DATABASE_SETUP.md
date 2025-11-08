# Database Setup Guide

## Quick Start

Totarr automatically creates a `.env` file on first startup if one doesn't exist. You just need to configure your database connection.

### 1. First Startup

When you first run the application, it will:
- ✅ Create `.env` from `.env.example` 
- ✅ Generate a secure `SECRET_KEY` automatically
- ⚠️ Show a warning that you need to configure `DATABASE_URL`

### 2. Configure Database

Edit the `.env` file and update the `DATABASE_URL`:

**For SQLite (Development/Testing):**
```bash
DATABASE_URL=sqlite:///./totarr.db
```

**For TimescaleDB/PostgreSQL (Production):**
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

### 🔒 Passwords with Special Characters

If your password contains special characters like `@ : / ? # [ ] ! $ & ' ( ) * + , ; = %`, you **must** URL-encode it.

**Quick Example:**
```
Password:     B*^Z*4t4hXPdBBAH^455d!I0f
Encoded:      B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f
DATABASE_URL: postgresql://totarr:B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f@192.168.1.100:5432/totarr
```

**Use the built-in encoder tool:**
```bash
cd backend
python -m app.core.url_encoder
```

The tool offers two options:
1. **Encode password only** - Just convert your password
2. **Build complete URL** - Interactive wizard that builds the entire DATABASE_URL

---

## Configuration Examples

```bash
# Local PostgreSQL (simple password)
DATABASE_URL=postgresql://totarr:mypassword@localhost:5432/totarr

# Unraid TimescaleDB (simple password)
DATABASE_URL=postgresql://totarr:mypassword@192.168.1.100:5432/totarr

# Docker Compose (using service name)
DATABASE_URL=postgresql://totarr:mypassword@timescaledb:5432/totarr

# Complex password with special characters (URL-encoded)
DATABASE_URL=postgresql://totarr:B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f@192.168.1.100:5432/totarr
```

---

## Docker Deployment

When deploying with Docker, set these environment variables in your `docker-compose.yml`:

```yaml
services:
  totarr:
    image: totarr:latest
    environment:
      # Simple password
      - DATABASE_URL=postgresql://totarr:${DB_PASSWORD}@timescaledb:5432/totarr
      
      # OR with complex password (URL-encode it first!)
      - DATABASE_URL=postgresql://totarr:B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f@timescaledb:5432/totarr
      
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
```

**Important:** Encode your password **before** adding it to docker-compose.yml!

---

## Unraid Template

For Unraid, add these variables to your Docker template:

| Config Type | Name | Key | Default Value |
|------------|------|-----|---------------|
| Variable | Database URL | DATABASE_URL | postgresql://totarr:YOUR_PASSWORD@YOUR_IP:5432/totarr |
| Variable | Secret Key | SECRET_KEY | (leave blank - auto-generated) |
| Variable | Environment | ENVIRONMENT | production |

**For complex passwords:**
1. Encode your password using the tool (on your computer): `python -m app.core.url_encoder`
2. Use the encoded password in the Unraid template

---

## Helper Tools

### Interactive Setup Wizard
```bash
cd backend
python setup_env.py
```
- Walks you through configuration
- Automatically encodes passwords with special characters
- Creates `.env` file for you

### URL Encoder Tool
```bash
cd backend
python -m app.core.url_encoder
```

**Option 1: Encode password only**
```
Enter password to encode: B*^Z*4t4hXPdBBAH^455d!I0f

Original:  B*^Z*4t4hXPdBBAH^455d!I0f
Encoded:   B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f

Use: postgresql://username:B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f@host:5432/database
```

**Option 2: Build complete DATABASE_URL**
- Interactive wizard
- Asks for username, password, host, port, database
- Builds complete connection string
- Automatically encodes password

---

## Special Character Reference

These characters **must** be URL-encoded in passwords:

| Character | Encoded | Character | Encoded |
|-----------|---------|-----------|---------|
| `@` | `%40` | `!` | `%21` |
| `:` | `%3A` | `$` | `%24` |
| `/` | `%2F` | `&` | `%26` |
| `?` | `%3F` | `'` | `%27` |
| `#` | `%23` | `(` | `%28` |
| `[` | `%5B` | `)` | `%29` |
| `]` | `%5D` | `*` | `%2A` |
| `%` | `%25` | `+` | `%2B` |
| `,` | `%2C` | `;` | `%3B` |
| `=` | `%3D` | `^` | `%5E` |

**Don't manually encode!** Use the tool: `python -m app.core.url_encoder`

---

## Security Notes

- ✅ `.env` files are automatically excluded from git
- ✅ `SECRET_KEY` is auto-generated on first run
- ✅ The app detects special characters and warns you
- ⚠️ **Never commit `.env` files to version control**
- ⚠️ **Use strong passwords for production databases**
- ⚠️ **Always URL-encode passwords with special characters**

---

## Troubleshooting

### "Configuration errors found: DATABASE_URL contains placeholder values"

Edit `.env` and replace `YOUR_PASSWORD` and `YOUR_DATABASE_HOST` with real values.

### "Can't connect to database" / "Authentication failed"

**If your password has special characters:**
1. Encode it: `python -m app.core.url_encoder`
2. Update `DATABASE_URL` with the encoded password
3. Restart the app

**Other causes:**
1. Check database is running: `docker ps` or Unraid Docker tab
2. Verify credentials are correct (try connecting with psql)
3. Test connectivity: `telnet YOUR_IP 5432`
4. Check firewall isn't blocking port 5432

### "No module named 'psycopg2'"

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

### Password encoding not working

Make sure you're using the **encoded** password in your `DATABASE_URL`, not the original.

**Wrong:**
```bash
DATABASE_URL=postgresql://user:my@pass!@host:5432/db
```

**Correct:**
```bash
DATABASE_URL=postgresql://user:my%40pass%21@host:5432/db
```

---

## Testing Your Setup

Run the database test script:

```bash
cd backend
python test_database.py
```

This will verify:
- ✅ Database connection works
- ✅ TimescaleDB extension is installed (if applicable)
- ✅ Tables can be created
- ✅ Configuration is valid

---

## Migration from SQLite to TimescaleDB

If you're currently using SQLite and want to migrate to TimescaleDB:

1. **Backup your data** (export integration configs if needed)
2. Encode your password if it has special characters
3. Update `DATABASE_URL` in `.env`
4. Restart the application
5. Tables will be created automatically
6. Reconfigure integrations via the UI

Note: Data doesn't automatically migrate - you'll need to reconfigure integrations.

---

## Need Help?

See the full setup guides:
- `QUICKSTART_TIMESCALEDB.md` - TimescaleDB setup on Unraid
- `TIMESCALEDB_SETUP.md` - Detailed TimescaleDB guide
- `UNRAID_DOCKER_TEMPLATE.md` - Unraid Docker template values
