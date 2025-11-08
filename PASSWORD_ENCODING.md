# 🔐 Password URL Encoding - Quick Reference

## Why Do I Need This?

Database connection strings (URLs) can't contain certain special characters directly. If your password has characters like `@ : / ! * ^ % #`, they must be URL-encoded.

---

## 🚀 Quick Solution

```bash
cd backend
python -m app.core.url_encoder
```

Follow the prompts - it will encode your password automatically!

---

## 📋 Common Examples

### Example 1: Simple Password (No encoding needed)
```bash
Password:     mySecurePass123
DATABASE_URL: postgresql://plextoolbox:mySecurePass123@192.168.1.100:5432/plex_toolbox
```

### Example 2: Password with Special Characters
```bash
Password:     B*^Z*4t4hXPdBBAH^455d!I0f
Encoded:      B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f
DATABASE_URL: postgresql://plextoolbox:B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f@192.168.1.100:5432/plex_toolbox
```

### Example 3: Password with @ symbol
```bash
Password:     Pass@word!123
Encoded:      Pass%40word%21123
DATABASE_URL: postgresql://plextoolbox:Pass%40word%21123@192.168.1.100:5432/plex_toolbox
```

---

## ⚡ Manual Encoding (Python)

If you want to encode manually:

```python
from urllib.parse import quote_plus

password = "B*^Z*4t4hXPdBBAH^455d!I0f"
encoded = quote_plus(password)
print(encoded)  # B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f
```

---

## 🔍 Character Encoding Table

| Char | Encoded | Char | Encoded | Char | Encoded |
|------|---------|------|---------|------|---------|
| `!`  | `%21`   | `@`  | `%40`   | `#`  | `%23`   |
| `$`  | `%24`   | `%`  | `%25`   | `^`  | `%5E`   |
| `&`  | `%26`   | `*`  | `%2A`   | `(`  | `%28`   |
| `)`  | `%29`   | `+`  | `%2B`   | `=`  | `%3D`   |
| `[`  | `%5B`   | `]`  | `%5D`   | `:`  | `%3A`   |
| `;`  | `%3B`   | `/`  | `%2F`   | `?`  | `%3F`   |

---

## ✅ Testing Connection

After encoding your password:

```bash
# Test the connection
cd backend
python test_database.py
```

If connection fails, double-check:
1. Password is encoded
2. IP address is correct
3. Port is correct (5432)
4. Database name is correct

---

## 🐳 Docker/Unraid Notes

**Always encode BEFORE adding to:**
- `docker-compose.yml`
- Unraid template variables
- Environment variables

**Example docker-compose.yml:**
```yaml
environment:
  # Encoded password
  - DATABASE_URL=postgresql://plextoolbox:B%2A%5EZ%2A4t4hXPdBBAH%5E455d%21I0f@timescaledb:5432/plex_toolbox
```

---

## 🆘 Still Having Issues?

1. **Run the encoder tool** - Don't encode manually
   ```bash
   python -m app.core.url_encoder
   ```

2. **Use Option 2** - Let it build the complete URL
   - Enter all connection details
   - It handles encoding automatically

3. **Copy the full DATABASE_URL** - Don't type it manually

4. **Test the connection** - Verify it works
   ```bash
   python test_database.py
   ```

---

## 💡 Pro Tips

- ✅ Use the tool - don't encode manually
- ✅ Copy/paste the encoded URL - don't type it
- ✅ Test before deploying to Docker
- ✅ Save the encoded password in your password manager
- ❌ Don't double-encode (if already encoded, don't encode again)
- ❌ Don't mix encoded and non-encoded parts
