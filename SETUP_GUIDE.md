# Farmers First - Setup & Deployment Guide

## Prerequisites Completed ✓
- All Python dependencies installed
- SQLite database configured
- Flask CORS enabled
- Backend APIs ready

## Quick Start

### 1. Start the Flask Development Server

**Windows PowerShell:**
```powershell
cd d:\pycoreog
.\.venv\Scripts\Activate.ps1
python app.py
```

You should see:
```
WARNING: This is a development server. Do not use it in production deployment.
Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### 2. Access the Web App in Browser

Open your browser and go to:
```
http://localhost:5000
```

The login page will load automatically.

---

## Features Overview

### Text-Based Login/Registration
1. Enter any **username**
2. Enter a **secure password**
3. Click **Login** to sign in with existing account
4. Click **Register** to create a new account
5. Credentials are stored in SQLite database

### Face-Based Authentication (Experimental)
1. Click **"Face Login"** tab
2. Click **"Capture Face"** to take a photo
3. For registration: Click **"Register Face"** and enter a username when prompted
4. For login: Click **"Login with Face"** to authenticate using your face

**Note:** Face recognition uses basic OpenCV detection. Install `face-recognition` library for advanced AI-powered matching.

---

## Using the Application

### After Successful Login
- Redirected to **Assistant** page for AI-powered farming assistance
- Can access **Market** prices for agricultural products
- View **Weather** forecasts by location
- Check **Soil** moisture data

### User Data Storage
- Username and password hash stored in `data/users.db` (SQLite)
- Face encodings stored safely in database
- Data persists between sessions

---

## Troubleshooting

### Issue: Login button doesn't respond
**Solution:** 
- Ensure Flask server is running (should show `Running on http://0.0.0.0:5000`)
- Check browser console for errors (F12 → Console tab)
- Try refreshing the page

### Issue: Face detection not working
**Solution:**
- Browser must have camera access permission
- Accept camera access when prompted
- Make sure face is clearly visible in frame
- Try capturing again if first attempt fails

### Issue: "Server error" message
**Solution:**
- Check Flask terminal for error messages
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Delete `data/users.db` and restart server to reset database

### Issue: Register button not responding
**Solution:**
- Enter both username AND password
- Click Register button
- Check for error message on page

---

## Database Management

### View User Accounts
```python
# Run in Python:
from pycore.database import find_user, get_connection

# List all users:
conn = get_connection()
cursor = conn.execute('SELECT username, created_at FROM users')
for row in cursor:
    print(row)
conn.close()
```

### Reset Database
```powershell
# Delete database file - it will be recreated on next server start
Remove-Item data\users.db
```

---

## Production Deployment

### For Public Access (Not Development):

1. **Install production server:**
   ```powershell
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```powershell
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

3. **Use HTTPS:**
   - Set up SSL certificates (Let's Encrypt)
   - Configure reverse proxy (nginx/Apache)

4. **Database:**
   - Consider migrating to PostgreSQL for production
   - Set up backups
   - Enable WAL mode in SQLite: `PRAGMA journal_mode=WAL;`

---

## Project Structure

```
d:\pycoreog/
├── app.py                 # Flask main application
├── requirements.txt       # Python dependencies
├── test_setup.py         # Setup verification script
├── data/
│   └── users.db          # SQLite user database
├── pycore/
│   ├── __init__.py
│   └── database.py       # Database operations
└── frontnd/              # Frontend files
    ├── index.html        # Home page
    ├── login.html        # Login/Register page
    ├── login.js          # Login logic
    ├── assistant.html    # AI Assistant page
    ├── market.html       # Market prices page
    ├── script.js         # General frontend logic
    ├── style.css         # Styling
    └── assets/           # Images and SVGs
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/login` | Text-based login |
| POST | `/api/register` | Text-based registration |
| POST | `/api/face_login` | Face recognition login |
| POST | `/api/weather` | Get weather forecast |
| POST | `/api/soil` | Get soil moisture data |
| POST | `/api/product_comparison` | Get product prices |

### Example API Calls:

**Login:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer","password":"secure123"}'
```

**Register:**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newfarmer","password":"mypassword"}'
```

---

## Common Commands

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# View running processes on port 5000
Get-NetTCPConnection -LocalPort 5000

# Install new package
pip install package_name

# View installed packages
pip list
```

---

## Support

If you encounter any issues:
1. Check the Flask server terminal for error messages
2. Verify all packages installed: `pip list | findstr Flask opencv`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Delete `data/users.db` and restart server
5. Check `requirements.txt` for correct versions

---

**Last Updated:** May 10, 2026
**Server:** Flask 2.3+
**Database:** SQLite
**Frontend:** Vanilla JavaScript
