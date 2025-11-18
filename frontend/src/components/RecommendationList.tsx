/**
 * RecommendationList Component
 * Displays a list of anime recommendations
 */

'use client';

import { useEffect, useState } from 'react';
import { recommendationApi } from '@/lib/api';
import AnimeCard from './AnimeCard';
import type { Recommendation } from '@/types';

interface RecommendationListProps {
  animeId?: number;
  title?: string;
  limit?: number;
}

export default function RecommendationList({
  animeId,
  title = 'Recommendations',
  limit = 5,
}: RecommendationListProps) {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRecommendations();
  }, [animeId]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = animeId
        ? await recommendationApi.getForAnime(animeId, limit)
        : await recommendationApi.getGeneral(limit);

      setRecommendations(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-8">
        <h2 className="text-2xl font-bold mb-6">{title}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {[...Array(limit)].map((_, i) => (
            <div key={i} className="bg-gray-200 rounded-lg h-96 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-8">
        <h2 className="text-2xl font-bold mb-6">{title}</h2>
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="py-8">
        <h2 className="text-2xl font-bold mb-6">{title}</h2>
        <p className="text-gray-600">No recommendations available.</p>
      </div>
    );
  }

  return (
    <div className="py-8">
      <h2 className="text-2xl font-bold mb-6">{title}</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {recommendations.map((anime) => (
          <AnimeCard
            key={anime.anime_id}
            anime={anime}
            showSimilarity={!!animeId}
          />
        ))}
      </div>
    </div>
  );
}
