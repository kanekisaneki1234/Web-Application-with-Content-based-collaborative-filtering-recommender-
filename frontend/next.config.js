/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    // Allow images from MyAnimeList CDN and other common anime image sources
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.myanimelist.net',
      },
      {
        protocol: 'https',
        hostname: '*.imgur.com',
      },
    ],
  },
}

module.exports = nextConfig
