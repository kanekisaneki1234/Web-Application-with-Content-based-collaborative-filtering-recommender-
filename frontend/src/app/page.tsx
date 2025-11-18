/**
 * Homepage
 * Displays featured anime and recommendations
 */

'use client';

import { useEffect, useState } from 'react';
import { animeApi } from '@/lib/api';
import AnimeCard from '@/components/AnimeCard';
import RecommendationList from '@/components/RecommendationList';
import type { Anime } from '@/types';

export default function HomePage() {
  const [anime, setAnime] = useState<Anime[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');

  // List of all genres from our sample data
  const genres = [
    'Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror',
    'Mystery', 'Psychological', 'Romance', 'Sci-Fi', 'Supernatural',
    'Thriller', 'Mecha', 'Military', 'School', 'Superhero', 'Game'
  ];

  useEffect(() => {
    loadAnime();
  }, [searchQuery, selectedGenre]);

  const loadAnime = async () => {
    try {
      setLoading(true);
      const data = await animeApi.getAll({
        search: searchQuery || undefined,
        genre: selectedGenre || undefined,
        limit: 20,
      });
      setAnime(data.anime);
    } catch (error) {
      console.error('Failed to load anime:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg p-8 mb-8 text-white">
        <h1 className="text-4xl font-bold mb-4">
          Discover Your Next Favorite Anime
        </h1>
        <p className="text-xl text-primary-100">
          Powered by AI-driven content-based recommendations
        </p>
      </div>

      {/* Search and Filter Section */}
      <div className="mb-8 bg-white p-6 rounded-lg shadow-md">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Search Input */}
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
              Search Anime
            </label>
            <input
              id="search"
              type="text"
              placeholder="Search by title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Genre Filter */}
          <div>
            <label htmlFor="genre" className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Genre
            </label>
            <select
              id="genre"
              value={selectedGenre}
              onChange={(e) => setSelectedGenre(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">All Genres</option>
              {genres.map((genre) => (
                <option key={genre} value={genre}>
                  {genre}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Active Filters */}
        {(searchQuery || selectedGenre) && (
          <div className="mt-4 flex items-center gap-2">
            <span className="text-sm text-gray-600">Active filters:</span>
            {searchQuery && (
              <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm">
                Search: "{searchQuery}"
              </span>
            )}
            {selectedGenre && (
              <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm">
                Genre: {selectedGenre}
              </span>
            )}
            <button
              onClick={() => {
                setSearchQuery('');
                setSelectedGenre('');
              }}
              className="text-sm text-primary-600 hover:text-primary-700 underline"
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Top Recommendations */}
      <RecommendationList title="Top Rated Anime" limit={10} />

      {/* All Anime Grid */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-6">
          {searchQuery || selectedGenre ? 'Search Results' : 'All Anime'}
          <span className="text-gray-500 text-lg ml-2">
            ({anime.length} {anime.length === 1 ? 'result' : 'results'})
          </span>
        </h2>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="bg-gray-200 rounded-lg h-96 animate-pulse" />
            ))}
          </div>
        ) : anime.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {anime.map((item) => (
              <AnimeCard key={item.anime_id} anime={item} />
            ))}
          </div>
        ) : (
          <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <p className="text-gray-600 text-lg">No anime found matching your criteria.</p>
            <button
              onClick={() => {
                setSearchQuery('');
                setSelectedGenre('');
              }}
              className="mt-4 text-primary-600 hover:text-primary-700 underline"
            >
              Clear filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
