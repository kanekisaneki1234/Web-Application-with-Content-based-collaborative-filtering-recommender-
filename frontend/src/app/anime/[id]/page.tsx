/**
 * Anime Detail Page
 * Dynamic page that displays detailed information about a specific anime
 */

'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import { animeApi, userApi } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import RecommendationList from '@/components/RecommendationList';
import type { Anime } from '@/types';

export default function AnimeDetailPage() {
  const params = useParams();
  const animeId = parseInt(params.id as string);
  const { isAuthenticated } = useAuth();

  const [anime, setAnime] = useState<Anime | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userRating, setUserRating] = useState<number>(0);
  const [submittingRating, setSubmittingRating] = useState(false);

  useEffect(() => {
    loadAnime();
  }, [animeId]);

  const loadAnime = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await animeApi.getById(animeId);
      setAnime(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load anime');
    } finally {
      setLoading(false);
    }
  };

  const handleRating = async (rating: number) => {
    if (!isAuthenticated) {
      alert('Please login to rate this anime');
      return;
    }

    try {
      setSubmittingRating(true);
      await userApi.rateAnime(animeId, rating);
      setUserRating(rating);
      // Reload anime to get updated average rating
      await loadAnime();
    } catch (error) {
      console.error('Failed to submit rating:', error);
      alert('Failed to submit rating');
    } finally {
      setSubmittingRating(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="bg-gray-200 h-96 rounded-lg mb-8" />
          <div className="bg-gray-200 h-8 w-2/3 mb-4 rounded" />
          <div className="bg-gray-200 h-4 w-full mb-2 rounded" />
          <div className="bg-gray-200 h-4 w-full mb-2 rounded" />
          <div className="bg-gray-200 h-4 w-2/3 rounded" />
        </div>
      </div>
    );
  }

  if (error || !anime) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg">
          {error || 'Anime not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Anime Details Section */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
        <div className="md:flex">
          {/* Anime Image */}
          <div className="md:w-1/3 relative h-96 md:h-auto">
            {anime.image_url ? (
              <Image
                src={anime.image_url}
                alt={anime.title}
                fill
                className="object-cover"
                priority
              />
            ) : (
              <div className="flex items-center justify-center h-full bg-gray-200 text-gray-400">
                No Image
              </div>
            )}
          </div>

          {/* Anime Information */}
          <div className="md:w-2/3 p-8">
            <h1 className="text-4xl font-bold mb-4">{anime.title}</h1>

            {/* Rating */}
            <div className="flex items-center mb-4">
              <div className="bg-primary-600 text-white px-4 py-2 rounded-lg text-2xl font-bold mr-4">
                {anime.rating.toFixed(1)}
              </div>
              <span className="text-gray-600">Average Rating</span>
            </div>

            {/* Genres */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">GENRES</h3>
              <div className="flex flex-wrap gap-2">
                {anime.genres.map((genre) => (
                  <span
                    key={genre}
                    className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {genre}
                  </span>
                ))}
              </div>
            </div>

            {/* Release Date */}
            {anime.release_date && (
              <div className="mb-6">
                <h3 className="text-sm font-semibold text-gray-600 mb-2">RELEASE DATE</h3>
                <p className="text-gray-800">
                  {new Date(anime.release_date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
            )}

            {/* Description */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">SYNOPSIS</h3>
              <p className="text-gray-700 leading-relaxed">{anime.description}</p>
            </div>

            {/* User Rating Section */}
            {isAuthenticated && (
              <div className="border-t pt-6">
                <h3 className="text-sm font-semibold text-gray-600 mb-3">RATE THIS ANIME</h3>
                <div className="flex items-center gap-2">
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((rating) => (
                    <button
                      key={rating}
                      onClick={() => handleRating(rating)}
                      disabled={submittingRating}
                      className={`w-10 h-10 rounded-full font-semibold transition-colors ${
                        userRating === rating
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-primary-100'
                      } ${submittingRating ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                      {rating}
                    </button>
                  ))}
                </div>
                {userRating > 0 && (
                  <p className="text-sm text-green-600 mt-2">
                    You rated this anime: {userRating}/10
                  </p>
                )}
              </div>
            )}

            {!isAuthenticated && (
              <div className="border-t pt-6">
                <p className="text-gray-600">
                  <a href="/login" className="text-primary-600 hover:underline">
                    Login
                  </a>{' '}
                  to rate this anime
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recommendations Section */}
      <RecommendationList
        animeId={animeId}
        title="You Might Also Like"
        limit={5}
      />
    </div>
  );
}
