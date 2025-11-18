# Backend API

FastAPI backend server for the anime website.

## Features

- RESTful API design
- JWT authentication
- PostgreSQL database with connection pooling
- Pydantic data validation
- Interactive API documentation
- CORS enabled for frontend

## API Endpoints

### Anime Routes (`/api/anime`)

- `GET /api/anime/` - List all anime with pagination and filters
  - Query params: `skip`, `limit`, `search`, `genre`
- `GET /api/anime/{id}` - Get anime by ID
- `POST /api/anime/` - Create anime (requires auth)
- `PUT /api/anime/{id}` - Update anime (requires auth)
- `DELETE /api/anime/{id}` - Delete anime (requires auth)

### Authentication Routes (`/api/auth`)

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### User Routes (`/api/users`)

- `GET /api/users/me` - Get current user (requires auth)
- `POST /api/users/rate` - Rate an anime (requires auth)
- `GET /api/users/ratings` - Get user ratings (requires auth)

### Recommendation Routes (`/api/recommendations`)

- `GET /api/recommendations/{anime_id}` - Get content-based recommendations
- `GET /api/recommendations/` - Get general recommendations

## Configuration

Environment variables in `.env`:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=anime_user
DB_PASSWORD=anime_password
DB_NAME=anime_db
SECRET_KEY=your-secret-key
RECOMMENDER_URL=http://localhost:8001
```

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

## API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## Project Structure

```
backend/
├── main.py           # FastAPI app and startup
├── routes.py         # API route handlers
├── models.py         # Pydantic models
├── database.py       # Database connection
├── auth.py          # JWT authentication
├── config.py        # Configuration
└── requirements.txt # Dependencies
```

## Testing with cURL

```bash
# Get all anime
curl http://localhost:8000/api/anime/

# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```
