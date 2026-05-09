# 🌾 Farmers First - Quick Start Guide

## ✅ Everything is Ready! Here's How to Run Your App

### Step 1: Open PowerShell Terminal
Navigate to your project folder `d:\pycoreog`

### Step 2: Start the Flask Server
```powershell
# Copy and paste this command:
.\.venv\Scripts\Activate.ps1
python app.py
```

You should see this:
```
Warning: Advanced face recognition not available. Using basic face detection if available.
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

**This means the server is running! ✓**

---

## Step 3: Open in Your Browser

**Go to:** `http://localhost:5000`

The login page will load automatically!

---

## 🎯 What Works Now

### ✅ Login & Registration (Text-Based)
1. **Register a new account:**
   - Enter any username
   - Enter a password
   - Click **Register** button
   - Account saved in database

2. **Login with credentials:**
   - Enter your username
   - Enter your password
   - Click **Login** button
   - Redirects to Assistant page

### ✅ Face Detection (Beta)
- Click **Face Login** tab
- Allow camera access when prompted
- Click **Capture Face**
- Register or login with face recognition
- Uses OpenCV for face detection

### ✅ Additional Features
- **Weather API:** Get forecasts by location
- **Soil Data:** Check soil moisture
- **Market Prices:** View agricultural product prices
- **AI Assistant:** Access farming assistance tools

---

## 📊 Database Info

- **Type:** SQLite
- **Location:** `data/users.db`
- **Stores:** Username, password hash, face encoding, created date
- **Auto-created:** First time server starts
- **Persistent:** Data saved between sessions

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Login button doesn't work** | Make sure Flask server is running (see terminal output) |
| **Register doesn't open form** | Click Register button after entering username & password |
| **Face detection not working** | Allow camera access + clear browser cache |
| **"Server error" message** | Check Flask terminal for error details |
| **Can't access http://localhost:5000** | Flask server not running - check Step 2 |

---

## 📝 Test the API (Optional)

To verify everything works:
```powershell
python test_api.py
```

You'll see:
```
✓ All API endpoints are functioning correctly!
✓ Database operations working properly
✓ Static files being served correctly
```

---

## 🚀 Files You'll Use

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server |
| `frontnd/login.html` | Login/Register page |
| `frontnd/login.js` | Login logic & API calls |
| `pycore/database.py` | Database operations |
| `data/users.db` | User data storage |
| `requirements.txt` | Python dependencies |

---

## 🎓 Example: Create a Test Account

1. **Server running at:** `http://localhost:5000`
2. **Register:**
   - Username: `farmer1`
   - Password: `farm123secure`
   - Click Register → Success!

3. **Login:**
   - Username: `farmer1`
   - Password: `farm123secure`
   - Click Login → Redirects to Assistant

---

## 💾 Resetting the Database

If you need to delete all users and start fresh:

```powershell
Remove-Item data\users.db
# Server will recreate it automatically
```

---

## 📱 Accessing from Other Devices on Network

Instead of `localhost:5000`, use your computer's IP:

**Find your IP:**
```powershell
ipconfig
```

Look for "IPv4 Address" (usually `192.168.x.x`)

**Then access from other device:**
```
http://YOUR_IP:5000
```

---

## ⚠️ Important Notes

- **Development server only** - Don't use in production
- **Face recognition** - Using basic OpenCV (not AI-powered)
- **Passwords** - Hashed with SHA256 (secure)
- **No HTTPS** - Local development only

---

## 🔐 Security for Production (Later)

When you deploy this app publicly, you'll need:
1. HTTPS/SSL certificates
2. Production WSGI server (Gunicorn)
3. Database backup strategy
4. Rate limiting
5. CSRF protection

*For now, this is perfect for local/network testing!*

---

## ✨ Summary of Fixes Made

✅ **Backend Connected** - Flask API working
✅ **Register Button Fixed** - Opens form and saves to database
✅ **Login System Working** - Validates credentials correctly
✅ **Face Detection Active** - Basic OpenCV detection works
✅ **Database Created** - SQLite storing user data
✅ **All APIs Tested** - Weather, Soil, Products all working
✅ **Static Files Served** - HTML/CSS/JS loading correctly

---

**Need help?** Check `SETUP_GUIDE.md` for detailed information.

**Questions about code?** Check `test_api.py` to see example API calls.

---

**Last Updated:** May 10, 2026 | **Status:** ✅ Ready to Use
