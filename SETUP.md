# Detailed Setup Guide

This guide provides step-by-step instructions for setting up the Anime Website with Content-Based Recommendations.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup](#backend-setup)
4. [Recommendation Service Setup](#recommendation-service-setup)
5. [Frontend Setup](#frontend-setup)
6. [Verification](#verification)
7. [Common Issues](#common-issues)

## Prerequisites

### Required Software

1. **Node.js and npm**
   - Version: 18.x or higher
   - Download: https://nodejs.org/
   - Verify installation:
     ```bash
     node --version
     npm --version
     ```

2. **Python**
   - Version: 3.9 or higher
   - Download: https://www.python.org/
   - Verify installation:
     ```bash
     python --version  # or python3 --version
     ```

3. **PostgreSQL**
   - Version: 15.x or higher
   - Option 1: Docker (recommended)
   - Option 2: Native installation
   - Verify installation:
     ```bash
     psql --version
     ```

4. **Git**
   - Download: https://git-scm.com/
   - Verify installation:
     ```bash
     git --version
     ```

## Database Setup

### Option 1: Using Docker (Recommended)

1. **Install Docker**
   - Download Docker Desktop from https://www.docker.com/

2. **Start PostgreSQL Container**
   ```bash
   docker-compose up -d
   ```

3. **Verify Container is Running**
   ```bash
   docker ps
   ```
   You should see `anime_postgres` in the list.

4. **Connect to Database (Optional)**
   ```bash
   docker exec -it anime_postgres psql -U anime_user -d anime_db
   ```

### Option 2: Native PostgreSQL Installation

1. **Install PostgreSQL**
   - Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```
   - macOS:
     ```bash
     brew install postgresql@15
     brew services start postgresql@15
     ```
   - Windows: Download installer from https://www.postgresql.org/

2. **Create Database and User**
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql

   # Run these SQL commands
   CREATE USER anime_user WITH PASSWORD 'anime_password';
   CREATE DATABASE anime_db OWNER anime_user;
   GRANT ALL PRIVILEGES ON DATABASE anime_db TO anime_user;
   \q
   ```

3. **Update Configuration**
   Edit `backend/.env` and `recommender/.env` with your database credentials.

### Initialize Database Schema and Data

```bash
# Install required Python packages
pip install psycopg2-binary python-dotenv

# Run initialization script
python database/init_db.py
```

Expected output:
```
============================================================
🚀 Anime Database Initialization
============================================================
✓ Database 'anime_db' created successfully
🗄️  Initializing database schema...
✓ Successfully executed schema.sql
📊 Populating database with sample data...
✓ Successfully executed seed_data.sql
✓ Database initialized successfully with 10 anime entries
============================================================
✅ Database setup completed successfully!
============================================================
```

## Backend Setup

1. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

2. **Create Virtual Environment**
   - Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=anime_user
   DB_PASSWORD=anime_password
   DB_NAME=anime_db
   SECRET_KEY=your-secret-key-change-in-production
   ```

5. **Run Backend Server**
   ```bash
   python main.py
   ```

   Expected output:
   ```
   🚀 Starting anime API server...
   ✓ Database connection pool initialized
   ✓ Server running on http://0.0.0.0:8000
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

6. **Verify Backend**
   - Open browser: http://localhost:8000
   - API docs: http://localhost:8000/docs

## Recommendation Service Setup

1. **Open New Terminal**
   Keep the backend running in the previous terminal.

2. **Navigate to Recommender Directory**
   ```bash
   cd recommender
   ```

3. **Create Virtual Environment**
   - Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Recommender Service**
   ```bash
   python main.py
   ```

   Expected output:
   ```
   🚀 Starting recommendation service...
   ============================================================
   🚀 Training Content-Based Recommendation System
   ============================================================
   📊 Loading anime data from database...
   ✓ Loaded 10 anime entries
   🔧 Preprocessing features...
   ✓ Features preprocessed
   🧮 Building similarity matrix...
   ✓ Similarity matrix built: (10, 10)
     - Feature vocabulary size: XXX
   ============================================================
   ✅ Training completed successfully!
   ============================================================
   ✓ Recommendation service ready
   INFO:     Uvicorn running on http://0.0.0.0:8001
   ```

6. **Verify Recommender**
   - Open browser: http://localhost:8001
   - API docs: http://localhost:8001/docs

## Frontend Setup

1. **Open New Terminal**
   Keep both backend and recommender running.

2. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

3. **Install Dependencies**
   ```bash
   npm install
   ```

   This will install:
   - Next.js
   - React
   - Tailwind CSS
   - TypeScript
   - Axios
   - And other dependencies

4. **Configure Environment Variables**
   ```bash
   cp .env.local.example .env.local
   ```

   Content of `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Run Development Server**
   ```bash
   npm run dev
   ```

   Expected output:
   ```
   ▲ Next.js 14.0.4
   - Local:        http://localhost:3000
   - Ready in 2.3s
   ```

6. **Access Application**
   Open browser: http://localhost:3000

## Verification

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Get all anime
curl http://localhost:8000/api/anime/

# Get specific anime
curl http://localhost:8000/api/anime/1
```

### 2. Test Recommender Service

```bash
# Health check
curl http://localhost:8001/health

# Get recommendations
curl http://localhost:8001/recommend/1?limit=5

# Get stats
curl http://localhost:8001/stats
```

### 3. Test Frontend

1. **Homepage**
   - Visit http://localhost:3000
   - Should see anime grid and search/filter options

2. **Anime Detail Page**
   - Click on any anime card
   - Should show detailed information and recommendations

3. **Authentication**
   - Click "Register"
   - Create a test account
   - Login with credentials

4. **Rating**
   - Login to your account
   - Visit an anime detail page
   - Rate the anime (1-10)
   - Verify rating is saved

5. **Profile**
   - Click "Profile" after logging in
   - Should see your ratings

## Common Issues

### Issue 1: Database Connection Failed

**Error:** `psycopg2.OperationalError: connection failed`

**Solutions:**
- Verify PostgreSQL is running:
  ```bash
  # Docker
  docker ps

  # Native
  sudo systemctl status postgresql
  ```
- Check credentials in `.env`
- Ensure database `anime_db` exists
- Check firewall settings

### Issue 2: Port Already in Use

**Error:** `Address already in use`

**Solutions:**
- Backend (8000):
  ```bash
  # Find process
  lsof -i :8000
  # Kill process
  kill -9 <PID>
  ```
- Recommender (8001):
  ```bash
  lsof -i :8001
  kill -9 <PID>
  ```
- Frontend (3000):
  ```bash
  lsof -i :3000
  kill -9 <PID>
  ```

### Issue 3: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Issue 4: CORS Error in Frontend

**Error:** `Access to fetch blocked by CORS policy`

**Solution:**
- Verify backend is running
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure backend CORS settings include frontend URL

### Issue 5: Recommendation Service Unavailable

**Error:** `503 Service Unavailable`

**Solution:**
- Verify recommender service is running on port 8001
- Check `RECOMMENDER_URL` in backend `.env`
- Check recommender logs for errors

### Issue 6: TypeScript Errors in Frontend

**Error:** Type errors during build

**Solution:**
```bash
# Clear Next.js cache
rm -rf frontend/.next

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run dev
```

## Next Steps

1. Explore the application at http://localhost:3000
2. Read the API documentation at http://localhost:8000/docs
3. Try the recommendation system
4. Add your own anime data
5. Customize the application to your needs

## Getting Help

- Check README.md for feature documentation
- Review API docs at `/docs` endpoints
- Check application logs for errors
- Open an issue on GitHub
