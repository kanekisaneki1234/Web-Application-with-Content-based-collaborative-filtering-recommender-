# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Node.js 18+
- Python 3.9+
- Docker (for PostgreSQL)

## Steps

### 1. Clone and Setup Database (1 min)

```bash
# Start PostgreSQL with Docker
docker-compose up -d

# Wait 10 seconds for database to be ready
sleep 10

# Initialize database
pip install psycopg2-binary python-dotenv
python database/init_db.py
```

### 2. Start Backend (1 min)

Open a new terminal:

```bash
cd backend

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start server
python main.py
```

Backend running at: http://localhost:8000

### 3. Start Recommendation Service (1 min)

Open a new terminal:

```bash
cd recommender

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start service
python main.py
```

Recommender running at: http://localhost:8001

### 4. Start Frontend (2 min)

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Start development server
npm run dev
```

Frontend running at: http://localhost:3000

## You're Done!

Visit http://localhost:3000 in your browser and start exploring!

### Quick Test

1. Browse anime on the homepage
2. Click on "Attack on Titan" to see details
3. Scroll down to see "You Might Also Like" recommendations
4. Click "Register" to create an account
5. Login and rate some anime

## Troubleshooting

### Database won't start?
```bash
docker-compose down
docker-compose up -d
```

### Port conflicts?
Kill processes on ports 8000, 8001, 3000 and restart

### Dependencies won't install?
- Python: Ensure you're using Python 3.9+
- Node: Ensure you're using Node 18+

## Architecture Overview

```
┌─────────────┐
│   Browser   │ ← User Interface (Next.js + Tailwind)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Backend   │ ← API Server (FastAPI)
│  Port 8000  │ → Handles anime data, auth, ratings
└──────┬──────┘
       │
       ├─→ PostgreSQL (Database)
       │
       └─→ Recommender Service
           │  Port 8001
           │ → TF-IDF + Cosine Similarity
           └─→ Content-based recommendations
```

## What's Included

- ✅ 10 sample anime with descriptions
- ✅ Content-based ML recommendations
- ✅ User authentication (JWT)
- ✅ Rating system
- ✅ Search and filter
- ✅ Responsive design
- ✅ API documentation

## API Endpoints

### View Interactive Docs
- Backend: http://localhost:8000/docs
- Recommender: http://localhost:8001/docs

### Quick API Tests

```bash
# Get all anime
curl http://localhost:8000/api/anime/

# Get recommendations for anime #1
curl http://localhost:8001/recommend/1?limit=5

# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

## Next Steps

1. Read [SETUP.md](SETUP.md) for detailed setup
2. Read [README.md](README.md) for full documentation
3. Explore the code and customize it
4. Add your own anime data
5. Deploy to production

## Adding Your Own Anime

1. Login to the application
2. Use the API to add anime:

```bash
curl -X POST http://localhost:8000/api/anime/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your Anime",
    "genres": ["Action", "Adventure"],
    "description": "An amazing anime...",
    "rating": 8.5
  }'
```

3. Retrain recommendations:
```bash
curl -X POST http://localhost:8001/retrain
```

## Development Tips

### Hot Reload
- Frontend: Automatically reloads on file changes
- Backend: Use `uvicorn main:app --reload`
- Recommender: Use `uvicorn main:app --reload`

### Debugging
- Frontend: Check browser console
- Backend: Check terminal logs
- Database: Use `docker exec -it anime_postgres psql -U anime_user -d anime_db`

### Code Formatting
- Python: Use `black` and `flake8`
- TypeScript: Next.js includes ESLint

## Support

Need help? Check:
1. [SETUP.md](SETUP.md) - Detailed setup guide
2. [README.md](README.md) - Full documentation
3. API Docs - http://localhost:8000/docs

Happy coding! 🚀
