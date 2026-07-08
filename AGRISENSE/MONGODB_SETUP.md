# 🚀 AGRISENSE Setup Guide - MongoDB Required

## 📋 Current Status
- ✅ Django Application: Ready
- ✅ UI/UX: Modern and Dynamic
- ⚠️ MongoDB: **NOT RUNNING** - Required for full functionality

## 🔧 MongoDB Setup Instructions

### Option 1: Install MongoDB Community Edition (Recommended)

#### For Windows:
1. **Download MongoDB Community Edition**
   - Visit: https://www.mongodb.com/try/download/community
   - Select Windows (x64)
   - Download the .msi installer

2. **Install MongoDB**
   - Run the downloaded .msi file
   - Choose "Complete" installation
   - Check "Install MongoDB Compass" (for GUI access)
   - Complete the installation

3. **Start MongoDB Service**
   - Windows will automatically create a MongoDB service
   - The service should start automatically after installation
   - Verify it's running: Open Services (services.msc) and look for "MongoDB"

4. **Verify Installation**
   - Open Command Prompt or PowerShell
   - Run: `mongosh` or `mongo`
   - Should connect to: `mongodb://127.0.0.1:27017`

### Option 2: Use Docker (If Docker is installed)

```bash
# Pull MongoDB image
docker pull mongo:latest

# Start MongoDB in a container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify it's running
docker logs mongodb
```

### Option 3: Download and Run Portable MongoDB

1. Download MongoDB portable from: https://www.mongodb.com/try/download/community
2. Extract to a folder (e.g., `C:\MongoDB`)
3. Create a data directory: `C:\MongoDB\data`
4. Open Command Prompt and navigate to MongoDB bin folder
5. Run: `mongod.exe --dbpath=C:\MongoDB\data`

---

## ✅ How to Run AGRISENSE After MongoDB is Running

### Prerequisites:
- Python 3.8+ installed
- MongoDB running on `localhost:27017`
- Project dependencies installed (`pip install -r requirements.txt`)

### Steps:

```bash
# Navigate to project directory
cd c:\Users\user\OneDrive\OneDrive\Desktop\AGRISENSE

# Create/activate virtual environment (if not already done)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if needed)
python manage.py migrate

# Start the development server
python manage.py runserver

# Access the application
# Open browser and go to: http://127.0.0.1:8000/
```

---

## 📊 What Works Without MongoDB (Read-Only)
- ✅ Home page loads with bootstrap UI
- ✅ Navigation works
- ✅ Login/Register pages display
- ✅ Styling and JavaScript loaded
- ❌ Cannot view marketplace listings
- ❌ Cannot log in/register users
- ❌ Cannot create seller listings

## 🎯 What Works With MongoDB (Full Features)
- ✅ User registration and authentication
- ✅ View all marketplace listings
- ✅ Seller dashboard with inventory management
- ✅ Price trend charts (7-day data)
- ✅ Contact seller functionality
- ✅ Search and filter listings
- ✅ Real-time updates

---

## 🧪 Testing MongoDB Connection

After starting MongoDB, test the connection:

```powershell
# Open PowerShell and run:
$connection = New-Object MongoDB.Driver.MongoClient("mongodb://localhost:27017/")
$database = $connection.GetDatabase("agrisense")
Write-Host "Connected to MongoDB!"

# Or use mongo shell:
mongosh "mongodb://localhost:27017"
```

---

## 📝 MongoDB Data Structure

The application uses these collections:
- `marketplace_user` - User accounts
- `marketplace_croplisting` - Crop listings
- `marketplace_pricehistory` - Historical price data

---

## 🔗 Useful Links

- MongoDB Community: https://www.mongodb.com/try/download/community
- MongoDB Compass (GUI): https://www.mongodb.com/products/tools/compass
- MongoDB Documentation: https://docs.mongodb.com/manual/
- PyMongo Documentation: https://pymongo.readthedocs.io/

---

## ❓ Troubleshooting

### Port 27017 already in use
```powershell
# Find process using port 27017
netstat -ano | findstr :27017

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### MongoDB won't start
1. Check Windows Event Viewer for error logs
2. Verify disk space is available
3. Check file permissions on MongoDB data folder
4. Try starting from command line: `mongod --dbpath=C:\path\to\data`

### Can't connect to database from Django
1. Ensure MongoDB is running: `mongosh`
2. Check settings.py - connection string should be:
   ```python
   'CLIENT': {
       'host': 'localhost',
       'port': 27017,
   }
   ```
3. Verify firewall isn't blocking port 27017
4. Check for MongoDB errors in server console

---

**Version**: 1.0  
**Last Updated**: March 31, 2026  
**Status**: Application Ready - Awaiting MongoDB Setup
