-- Database schema for anime website
-- This file contains the table definitions for storing anime data

-- Drop tables if they exist (for clean re-initialization)
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS anime CASCADE;
DROP TABLE IF EXISTS user_ratings CASCADE;

-- Anime table: stores all anime information
CREATE TABLE anime (
    anime_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    image_url TEXT,
    genres TEXT[], -- Array of genres
    description TEXT,
    release_date DATE,
    rating DECIMAL(3, 2) DEFAULT 0.00, -- Average rating (0.00 to 10.00)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table: stores user account information
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User ratings table: stores user ratings for anime
CREATE TABLE user_ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    anime_id INTEGER REFERENCES anime(anime_id) ON DELETE CASCADE,
    rating DECIMAL(3, 2) NOT NULL CHECK (rating >= 0 AND rating <= 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, anime_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_anime_title ON anime(title);
CREATE INDEX idx_anime_rating ON anime(rating DESC);
CREATE INDEX idx_user_ratings_anime ON user_ratings(anime_id);
CREATE INDEX idx_user_ratings_user ON user_ratings(user_id);
