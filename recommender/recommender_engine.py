"""
Content-Based Recommendation Engine
Uses TF-IDF vectorization and cosine similarity to recommend similar anime
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
import os

class AnimeRecommender:
    """
    Content-based recommendation system for anime

    This class builds a recommendation model based on:
    - Genres (categorical feature)
    - Description (text feature using TF-IDF)

    The system computes cosine similarity between anime to find similar titles
    """

    def __init__(self, db_config: dict):
        """
        Initialize the recommender

        Args:
            db_config: Dictionary containing database connection parameters
        """
        self.db_config = db_config
        self.anime_df = None
        self.similarity_matrix = None
        self.tfidf_vectorizer = None
        self.genre_weights = 0.4  # Weight for genre similarity
        self.description_weights = 0.6  # Weight for description similarity

    def connect_db(self):
        """Create a database connection"""
        return psycopg2.connect(**self.db_config)

    def load_anime_data(self) -> pd.DataFrame:
        """
        Load anime data from the database

        Returns:
            DataFrame containing all anime with their features
        """
        print("📊 Loading anime data from database...")

        conn = self.connect_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT anime_id, title, genres, description, rating, image_url
            FROM anime
            ORDER BY anime_id
        """)

        anime_data = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert to DataFrame
        self.anime_df = pd.DataFrame(anime_data)

        print(f"✓ Loaded {len(self.anime_df)} anime entries")
        return self.anime_df

    def preprocess_features(self) -> pd.DataFrame:
        """
        Preprocess anime features for recommendation

        Creates combined feature text from genres and description

        Returns:
            DataFrame with processed features
        """
        print("🔧 Preprocessing features...")

        # Convert genres array to space-separated string
        # Repeat genres to give them more weight in similarity calculation
        self.anime_df['genres_str'] = self.anime_df['genres'].apply(
            lambda x: ' '.join(x * 3) if x else ''  # Repeat genres 3 times for emphasis
        )

        # Clean and prepare description
        self.anime_df['description_clean'] = self.anime_df['description'].fillna('')

        # Combine features: genres get more weight by repetition
        self.anime_df['combined_features'] = (
            self.anime_df['genres_str'] + ' ' +
            self.anime_df['description_clean']
        )

        print("✓ Features preprocessed")
        return self.anime_df

    def build_similarity_matrix(self):
        """
        Build the similarity matrix using TF-IDF and cosine similarity

        This creates a matrix where each cell (i,j) represents the similarity
        between anime i and anime j
        """
        print("🧮 Building similarity matrix...")

        # Create TF-IDF matrix from combined features
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),  # Use both unigrams and bigrams
            min_df=1,
            max_df=0.8
        )

        # Fit and transform the combined features
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.anime_df['combined_features']
        )

        # Compute cosine similarity matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        print(f"✓ Similarity matrix built: {self.similarity_matrix.shape}")
        print(f"  - Feature vocabulary size: {len(self.tfidf_vectorizer.vocabulary_)}")

    def get_recommendations(
        self,
        anime_id: int,
        n_recommendations: int = 5
    ) -> List[Dict]:
        """
        Get top-N recommendations for a given anime

        Args:
            anime_id: The ID of the anime to get recommendations for
            n_recommendations: Number of recommendations to return

        Returns:
            List of recommended anime with similarity scores
        """
        # Find the index of the anime in our DataFrame
        try:
            idx = self.anime_df[self.anime_df['anime_id'] == anime_id].index[0]
        except IndexError:
            raise ValueError(f"Anime with ID {anime_id} not found")

        # Get similarity scores for this anime
        similarity_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort by similarity score (descending) and exclude the anime itself
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )[1:n_recommendations + 1]  # Skip first one (itself)

        # Get anime details for recommendations
        recommendations = []
        for anime_idx, score in similarity_scores:
            anime = self.anime_df.iloc[anime_idx]
            recommendations.append({
                'anime_id': int(anime['anime_id']),
                'title': anime['title'],
                'image_url': anime['image_url'],
                'genres': anime['genres'],
                'similarity_score': float(score),
                'rating': float(anime['rating']) if anime['rating'] else 0.0
            })

        return recommendations

    def train(self):
        """
        Train the recommendation system

        This method:
        1. Loads anime data from database
        2. Preprocesses features
        3. Builds similarity matrix
        """
        print("\n" + "=" * 60)
        print("🚀 Training Content-Based Recommendation System")
        print("=" * 60)

        self.load_anime_data()
        self.preprocess_features()
        self.build_similarity_matrix()

        print("\n" + "=" * 60)
        print("✅ Training completed successfully!")
        print("=" * 60 + "\n")

    def get_anime_info(self, anime_id: int) -> Dict:
        """
        Get information about a specific anime

        Args:
            anime_id: The ID of the anime

        Returns:
            Dictionary with anime information
        """
        try:
            anime = self.anime_df[self.anime_df['anime_id'] == anime_id].iloc[0]
            return {
                'anime_id': int(anime['anime_id']),
                'title': anime['title'],
                'genres': anime['genres'],
                'rating': float(anime['rating']) if anime['rating'] else 0.0
            }
        except IndexError:
            raise ValueError(f"Anime with ID {anime_id} not found")

# Example usage and testing
if __name__ == "__main__":
    # Database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'anime_user'),
        'password': os.getenv('DB_PASSWORD', 'anime_password'),
        'database': os.getenv('DB_NAME', 'anime_db')
    }

    # Create and train recommender
    recommender = AnimeRecommender(db_config)
    recommender.train()

    # Test recommendations
    print("\n📝 Testing recommendations...")
    test_anime_id = 1  # Attack on Titan

    try:
        anime_info = recommender.get_anime_info(test_anime_id)
        print(f"\nGetting recommendations for: {anime_info['title']}")
        print(f"Genres: {', '.join(anime_info['genres'])}")

        recommendations = recommender.get_recommendations(test_anime_id, n_recommendations=5)

        print(f"\n🎯 Top 5 Recommendations:")
        print("-" * 80)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']}")
            print(f"   Genres: {', '.join(rec['genres'])}")
            print(f"   Similarity: {rec['similarity_score']:.4f} | Rating: {rec['rating']:.2f}")
            print()
    except Exception as e:
        print(f"Error: {e}")
