# Recommendation Engine

Content-based recommendation system using machine learning.

## How It Works

### 1. Feature Extraction
- Combines anime genres and description into feature vectors
- Genres are weighted more heavily (repeated 3x)

### 2. TF-IDF Vectorization
- Converts text to numerical vectors
- Uses scikit-learn's TfidfVectorizer
- Parameters:
  - max_features: 5000
  - ngram_range: (1, 2) - unigrams and bigrams
  - stop_words: english

### 3. Similarity Computation
- Computes cosine similarity between all anime pairs
- Creates similarity matrix (N × N)
- Each cell represents similarity (0-1) between two anime

### 4. Recommendation Generation
- Finds top-N most similar anime
- Excludes the anime itself
- Returns sorted by similarity score

## API Endpoints

### Get Recommendations
```
GET /recommend/{anime_id}?limit=5
```

Returns top-N similar anime based on content.

### Retrain Model
```
POST /retrain
```

Retrains the recommendation model with latest database data.

### Get Statistics
```
GET /stats
```

Returns model statistics like total anime count and matrix shape.

### Get Anime Info
```
GET /anime/{anime_id}/info
```

Returns basic info about a specific anime.

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run service
python main.py
```

Service runs on port 8001.

## Testing

```bash
# Run the recommender engine directly
python recommender_engine.py
```

This will:
1. Load anime from database
2. Train the model
3. Generate test recommendations

## Model Parameters

Configurable in `recommender_engine.py`:

- `genre_weights`: Weight for genre similarity (default: 0.4)
- `description_weights`: Weight for description similarity (default: 0.6)
- `max_features`: Maximum TF-IDF features (default: 5000)
- `ngram_range`: N-gram range for TF-IDF (default: (1, 2))

## Performance

- Training time: ~1-2 seconds for 10 anime
- Recommendation time: <10ms per request
- Memory usage: ~50MB for 100 anime

## Scaling

For larger datasets:
- Increase `max_features` for better accuracy
- Use approximate nearest neighbors (ANN) for faster lookups
- Consider caching similarity scores
- Use batch processing for retraining

## Example Usage

```python
from recommender_engine import AnimeRecommender

# Initialize
recommender = AnimeRecommender(db_config)
recommender.train()

# Get recommendations
recommendations = recommender.get_recommendations(
    anime_id=1,
    n_recommendations=5
)

# Results
for rec in recommendations:
    print(f"{rec['title']}: {rec['similarity_score']:.2f}")
```

## Dependencies

- scikit-learn: TF-IDF and cosine similarity
- pandas: Data manipulation
- numpy: Numerical operations
- psycopg2: PostgreSQL connection
- FastAPI: API server
