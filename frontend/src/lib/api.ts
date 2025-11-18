/**
 * API Client
 * Handles all API requests to the backend
 */

import axios from 'axios';
import type { Anime, AnimeListResponse, User, Recommendation, AuthTokens } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add authorization token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ============================================================================
// ANIME API
// ============================================================================

export const animeApi = {
  /**
   * Get all anime with optional filtering and pagination
   */
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    genre?: string;
  }): Promise<AnimeListResponse> => {
    const response = await apiClient.get('/api/anime/', { params });
    return response.data;
  },

  /**
   * Get a specific anime by ID
   */
  getById: async (animeId: number): Promise<Anime> => {
    const response = await apiClient.get(`/api/anime/${animeId}`);
    return response.data;
  },

  /**
   * Create a new anime (requires authentication)
   */
  create: async (anime: Partial<Anime>): Promise<Anime> => {
    const response = await apiClient.post('/api/anime/', anime);
    return response.data;
  },

  /**
   * Update an anime (requires authentication)
   */
  update: async (animeId: number, anime: Partial<Anime>): Promise<Anime> => {
    const response = await apiClient.put(`/api/anime/${animeId}`, anime);
    return response.data;
  },

  /**
   * Delete an anime (requires authentication)
   */
  delete: async (animeId: number): Promise<void> => {
    await apiClient.delete(`/api/anime/${animeId}`);
  },
};

// ============================================================================
// AUTHENTICATION API
// ============================================================================

export const authApi = {
  /**
   * Register a new user
   */
  register: async (userData: {
    username: string;
    email: string;
    password: string;
  }): Promise<User> => {
    const response = await apiClient.post('/api/auth/register', userData);
    return response.data;
  },

  /**
   * Login user and receive JWT token
   */
  login: async (credentials: {
    username: string;
    password: string;
  }): Promise<AuthTokens> => {
    const response = await apiClient.post('/api/auth/login', credentials);
    return response.data;
  },
};

// ============================================================================
// USER API
// ============================================================================

export const userApi = {
  /**
   * Get current user information (requires authentication)
   */
  getMe: async (): Promise<User> => {
    const response = await apiClient.get('/api/users/me');
    return response.data;
  },

  /**
   * Rate an anime (requires authentication)
   */
  rateAnime: async (animeId: number, rating: number): Promise<void> => {
    await apiClient.post('/api/users/rate', { anime_id: animeId, rating });
  },

  /**
   * Get user's ratings (requires authentication)
   */
  getRatings: async () => {
    const response = await apiClient.get('/api/users/ratings');
    return response.data;
  },
};

// ============================================================================
// RECOMMENDATION API
// ============================================================================

export const recommendationApi = {
  /**
   * Get recommendations for a specific anime
   */
  getForAnime: async (animeId: number, limit: number = 5): Promise<Recommendation[]> => {
    const response = await apiClient.get(`/api/recommendations/${animeId}`, {
      params: { limit },
    });
    return response.data;
  },

  /**
   * Get general recommendations (top-rated anime)
   */
  getGeneral: async (limit: number = 10): Promise<Recommendation[]> => {
    const response = await apiClient.get('/api/recommendations/', {
      params: { limit },
    });
    return response.data;
  },
};

export default apiClient;
