/**
 * AnimeCard Component
 * Displays an anime card with image, title, rating, and genres
 */

'use client';

import Link from 'next/link';
import Image from 'next/image';
import type { Anime, Recommendation } from '@/types';

interface AnimeCardProps {
  anime: Anime | Recommendation;
  showSimilarity?: boolean;
}

export default function AnimeCard({ anime, showSimilarity = false }: AnimeCardProps) {
  const similarityScore = 'similarity_score' in anime ? anime.similarity_score : null;

  return (
    <Link href={`/anime/${anime.anime_id}`}>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer h-full flex flex-col">
        {/* Anime Image */}
        <div className="relative h-64 w-full bg-gray-200">
          {anime.image_url ? (
            <Image
              src={anime.image_url}
              alt={anime.title}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              No Image
            </div>
          )}

          {/* Rating Badge */}
          <div className="absolute top-2 right-2 bg-primary-600 text-white px-2 py-1 rounded-md text-sm font-bold">
            {anime.rating.toFixed(1)}
          </div>

          {/* Similarity Score Badge */}
          {showSimilarity && similarityScore !== null && (
            <div className="absolute top-2 left-2 bg-green-600 text-white px-2 py-1 rounded-md text-xs font-bold">
              {(similarityScore * 100).toFixed(0)}% Match
            </div>
          )}
        </div>

        {/* Anime Info */}
        <div className="p-4 flex-grow flex flex-col">
          <h3 className="text-lg font-semibold mb-2 line-clamp-2 flex-grow">
            {anime.title}
          </h3>

          {/* Genres */}
          <div className="flex flex-wrap gap-1 mt-2">
            {anime.genres.slice(0, 3).map((genre) => (
              <span
                key={genre}
                className="bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded-full"
              >
                {genre}
              </span>
            ))}
            {anime.genres.length > 3 && (
              <span className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                +{anime.genres.length - 3}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}
