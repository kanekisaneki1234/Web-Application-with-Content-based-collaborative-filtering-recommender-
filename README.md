# Anime Website with Content-Based Recommendations

A full-stack web application for discovering anime with AI-powered content-based recommendations using machine learning.

![Tech Stack](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.3-orange)

## Features

- **Dynamic Anime Pages**: Single template dynamically renders all anime content based on ID
- **Content-Based Recommendations**: ML-powered recommendations using TF-IDF and cosine similarity
- **User Authentication**: Secure JWT-based login and registration
- **Rating System**: Users can rate anime and see average ratings
- **Advanced Search**: Filter by title and genre with real-time results
- **Responsive Design**: Beautiful UI built with Tailwind CSS
- **RESTful API**: Well-documented FastAPI backend

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **JWT** - Secure authentication
- **Pydantic** - Data validation

### Recommendation Engine
- **scikit-learn** - TF-IDF vectorization and cosine similarity
- **pandas** - Data manipulation
- **NumPy** - Numerical computing

## Project Structure

```
.
├── frontend/              # Next.js frontend application
│   ├── src/
│   │   ├── app/          # App router pages
│   │   ├── components/   # Reusable components
│   │   ├── contexts/     # React contexts (Auth)
│   │   ├── lib/          # API client and utilities
│   │   └── types/        # TypeScript type definitions
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/              # FastAPI backend server
│   ├── main.py          # Application entry point
│   ├── routes.py        # API route handlers
│   ├── models.py        # Pydantic models
│   ├── database.py      # Database connection
│   ├── auth.py          # Authentication utilities
│   ├── config.py        # Configuration settings
│   └── requirements.txt
│
├── recommender/          # Content-based recommendation system
│   ├── main.py          # Recommender API service
│   ├── recommender_engine.py  # ML recommendation logic
│   └── requirements.txt
│
├── database/             # Database schemas and scripts
│   ├── schema.sql       # Database schema
│   ├── seed_data.sql    # Sample anime data
│   └── init_db.py       # Database initialization script
│
└── docker-compose.yml   # PostgreSQL container setup
```

## Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **PostgreSQL** 15+ (or use Docker)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Web-Application-with-Content-based-collaborative-filtering-recommender-
   ```

2. **Set up PostgreSQL**

   Using Docker (recommended):
   ```bash
   docker-compose up -d
   ```

   Or install PostgreSQL manually and create a database named `anime_db`.

3. **Initialize the database**
   ```bash
   # Install Python dependencies
   pip install psycopg2-binary python-dotenv

   # Run initialization script
   python database/init_db.py
   ```

4. **Set up the Backend API**
   ```bash
   cd backend

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Copy environment variables
   cp .env.example .env
   # Edit .env if needed

   # Run the backend server
   python main.py
   ```
   Backend will run on `http://localhost:8000`

5. **Set up the Recommendation Service**
   ```bash
   # Open a new terminal
   cd recommender

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run the recommender service
   python main.py
   ```
   Recommender service will run on `http://localhost:8001`

6. **Set up the Frontend**
   ```bash
   # Open a new terminal
   cd frontend

   # Install dependencies
   npm install

   # Copy environment variables
   cp .env.local.example .env.local

   # Run the development server
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

7. **Access the application**

   Open your browser and navigate to `http://localhost:3000`

## Usage

### Browse Anime
- Visit the homepage to see all anime
- Use the search bar to find specific titles
- Filter by genre using the dropdown

### View Anime Details
- Click on any anime card to view detailed information
- See recommendations based on content similarity
- View synopsis, genres, release date, and ratings

### User Registration & Login
- Click "Register" to create an account
- Login with your credentials
- Authenticated users can rate anime

### Rate Anime
- Login to your account
- Navigate to any anime detail page
- Click a number (1-10) to rate the anime
- Your rating is saved and the average rating updates

### View Profile
- Click "Profile" in the navigation
- See your username, email, and registration date
- View all your anime ratings

## API Documentation

### Backend API Endpoints

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

#### Anime Endpoints
- `GET /api/anime/` - Get all anime (with pagination and filters)
- `GET /api/anime/{id}` - Get specific anime by ID
- `POST /api/anime/` - Create new anime (requires auth)
- `PUT /api/anime/{id}` - Update anime (requires auth)
- `DELETE /api/anime/{id}` - Delete anime (requires auth)

#### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

#### User Endpoints
- `GET /api/users/me` - Get current user info (requires auth)
- `POST /api/users/rate` - Rate an anime (requires auth)
- `GET /api/users/ratings` - Get user's ratings (requires auth)

#### Recommendation Endpoints
- `GET /api/recommendations/{anime_id}` - Get recommendations for anime
- `GET /api/recommendations/` - Get general recommendations

### Recommender Service Endpoints

Visit `http://localhost:8001/docs` for recommender API documentation.

- `GET /recommend/{anime_id}` - Get content-based recommendations
- `POST /retrain` - Retrain the model (use when adding new anime)
- `GET /stats` - Get model statistics

## How the Recommendation System Works

The content-based recommendation system uses the following approach:

1. **Feature Extraction**
   - Combines genres and description text into a single feature vector
   - Genres are repeated 3x to give them more weight

2. **TF-IDF Vectorization**
   - Converts text features into numerical vectors using TF-IDF
   - Uses both unigrams and bigrams
   - Vocabulary size: ~5000 features

3. **Similarity Computation**
   - Computes cosine similarity between all anime pairs
   - Creates a similarity matrix (N × N where N = number of anime)

4. **Recommendation Generation**
   - For a given anime, finds the top-N most similar anime
   - Returns sorted by similarity score (0-1)

5. **Real-time Updates**
   - Recommendations are computed on-demand
   - Model can be retrained when new anime are added

## Adding New Anime

### Via API

```bash
curl -X POST http://localhost:8000/api/anime/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Anime",
    "image_url": "https://example.com/image.jpg",
    "genres": ["Action", "Adventure"],
    "description": "An exciting new anime...",
    "release_date": "2024-01-01",
    "rating": 8.5
  }'
```

### Retrain Recommendation Model

After adding new anime:
```bash
curl -X POST http://localhost:8001/retrain
```

## Environment Variables

### Backend (.env)
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=anime_user
DB_PASSWORD=anime_password
DB_NAME=anime_db
SECRET_KEY=your-secret-key-here
RECOMMENDER_URL=http://localhost:8001
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Database Schema

### Anime Table
- `anime_id` - Primary key
- `title` - Anime title
- `image_url` - Cover image URL
- `genres` - Array of genres
- `description` - Synopsis
- `release_date` - Release date
- `rating` - Average rating (0-10)

### Users Table
- `user_id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `password_hash` - Hashed password

### User Ratings Table
- `rating_id` - Primary key
- `user_id` - Foreign key to users
- `anime_id` - Foreign key to anime
- `rating` - User's rating (0-10)

## Troubleshooting

### Database Connection Failed
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database `anime_db` exists

### Recommendation Service Unavailable
- Ensure the recommender service is running on port 8001
- Check `RECOMMENDER_URL` in backend `.env`

### Frontend Can't Connect to Backend
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

### CORS Errors
- Backend allows origins: `http://localhost:3000` and `http://localhost:3001`
- Update `CORSMiddleware` in `backend/main.py` if using different ports

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Testing Recommendations
```python
# In recommender directory
python recommender_engine.py
```

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
npm start
```

### Run Backend in Production
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Security Considerations
1. Change `SECRET_KEY` in production
2. Use environment variables for all sensitive data
3. Enable HTTPS
4. Restrict CORS origins
5. Use a production-grade PostgreSQL setup
6. Implement rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`

---

Built with ❤️ using Next.js, FastAPI, and scikit-learn
