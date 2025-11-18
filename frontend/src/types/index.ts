/**
 * TypeScript type definitions
 * Defines interfaces for API responses and application data
 */

export interface Anime {
  anime_id: number;
  title: string;
  image_url?: string;
  genres: string[];
  description?: string;
  release_date?: string;
  rating: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  user_id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface Rating {
  rating_id: number;
  user_id: number;
  anime_id: number;
  rating: number;
  created_at: string;
}

export interface Recommendation {
  anime_id: number;
  title: string;
  image_url?: string;
  genres: string[];
  similarity_score: number;
  rating: number;
}

export interface AnimeListResponse {
  total: number;
  anime: Anime[];
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
}
