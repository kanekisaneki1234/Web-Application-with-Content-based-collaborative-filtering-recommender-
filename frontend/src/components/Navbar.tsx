/**
 * Navbar Component
 * Main navigation bar with links and authentication status
 */

'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <nav className="bg-primary-700 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold">AnimeHub</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            <Link
              href="/"
              className="hover:text-primary-200 transition-colors"
            >
              Home
            </Link>

            {isAuthenticated ? (
              <>
                <Link
                  href="/profile"
                  className="hover:text-primary-200 transition-colors"
                >
                  Profile
                </Link>
                <span className="text-primary-200">
                  Welcome, {user?.username}
                </span>
                <button
                  onClick={logout}
                  className="bg-primary-600 hover:bg-primary-500 px-4 py-2 rounded-md transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="hover:text-primary-200 transition-colors"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="bg-primary-600 hover:bg-primary-500 px-4 py-2 rounded-md transition-colors"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
