/**
 * Profile Page
 * Displays user information and their anime ratings
 */

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { userApi, animeApi } from '@/lib/api';
import Link from 'next/link';
import type { Rating, Anime } from '@/types';

interface RatingWithAnime extends Rating {
  anime?: Anime;
}

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [ratings, setRatings] = useState<RatingWithAnime[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    } else if (isAuthenticated) {
      loadRatings();
    }
  }, [isAuthenticated, authLoading]);

  const loadRatings = async () => {
    try {
      setLoading(true);
      const userRatings = await userApi.getRatings();

      // Load anime details for each rating
      const ratingsWithAnime = await Promise.all(
        userRatings.map(async (rating: Rating) => {
          try {
            const anime = await animeApi.getById(rating.anime_id);
            return { ...rating, anime };
          } catch {
            return rating;
          }
        })
      );

      setRatings(ratingsWithAnime);
    } catch (error) {
      console.error('Failed to load ratings:', error);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || !isAuthenticated) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h1 className="text-3xl font-bold mb-2">Profile</h1>
        <div className="space-y-2">
          <p className="text-gray-600">
            <span className="font-semibold">Username:</span> {user?.username}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold">Email:</span> {user?.email}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold">Member since:</span>{' '}
            {user?.created_at &&
              new Date(user.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
          </p>
        </div>
      </div>

      {/* User Ratings */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold mb-6">
          Your Ratings
          <span className="text-gray-500 text-lg ml-2">({ratings.length})</span>
        </h2>

        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-gray-200 rounded-lg h-24 animate-pulse" />
            ))}
          </div>
        ) : ratings.length > 0 ? (
          <div className="space-y-4">
            {ratings.map((rating) => (
              <div
                key={rating.rating_id}
                className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-grow">
                    {rating.anime ? (
                      <Link
                        href={`/anime/${rating.anime_id}`}
                        className="text-lg font-semibold text-primary-600 hover:text-primary-700"
                      >
                        {rating.anime.title}
                      </Link>
                    ) : (
                      <span className="text-lg font-semibold">Anime #{rating.anime_id}</span>
                    )}

                    <div className="flex items-center gap-4 mt-2">
                      <span className="text-sm text-gray-600">
                        Your rating: <span className="font-bold">{rating.rating}/10</span>
                      </span>
                      {rating.anime && (
                        <>
                          <span className="text-gray-300">|</span>
                          <span className="text-sm text-gray-600">
                            Average: <span className="font-bold">{rating.anime.rating.toFixed(1)}/10</span>
                          </span>
                        </>
                      )}
                      <span className="text-gray-300">|</span>
                      <span className="text-sm text-gray-500">
                        {new Date(rating.created_at).toLocaleDateString()}
                      </span>
                    </div>

                    {rating.anime && rating.anime.genres.length > 0 && (
                      <div className="flex gap-2 mt-2">
                        {rating.anime.genres.slice(0, 3).map((genre) => (
                          <span
                            key={genre}
                            className="bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded-full"
                          >
                            {genre}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Rating Badge */}
                  <div className="ml-4">
                    <div className="bg-primary-600 text-white w-16 h-16 rounded-lg flex items-center justify-center">
                      <span className="text-2xl font-bold">{rating.rating}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">You haven't rated any anime yet.</p>
            <Link
              href="/"
              className="text-primary-600 hover:text-primary-700 font-medium underline"
            >
              Browse anime to get started
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
