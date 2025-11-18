# Frontend Application

Next.js 14 frontend with TypeScript and Tailwind CSS.

## Features

- Server-side rendering (SSR)
- App Router (Next.js 14)
- TypeScript for type safety
- Tailwind CSS for styling
- Responsive design
- JWT authentication
- Real-time API integration

## Pages

### Home (`/`)
- Anime grid with search and filter
- Top recommendations section
- Responsive layout

### Anime Detail (`/anime/[id]`)
- Dynamic routing
- Detailed anime information
- Content-based recommendations
- Rating system (for logged-in users)

### Login (`/login`)
- User authentication
- Form validation
- Error handling

### Register (`/register`)
- User registration
- Password confirmation
- Email validation

### Profile (`/profile`)
- User information
- Rating history
- Protected route (requires auth)

## Components

### AnimeCard
Reusable card component for displaying anime.

```tsx
<AnimeCard anime={anime} showSimilarity={true} />
```

### Navbar
Navigation bar with authentication state.

### RecommendationList
Displays a list of recommended anime.

```tsx
<RecommendationList
  animeId={1}
  title="You Might Also Like"
  limit={5}
/>
```

## API Integration

API client in `src/lib/api.ts`:

```typescript
import { animeApi, authApi, userApi, recommendationApi } from '@/lib/api';

// Get all anime
const data = await animeApi.getAll({ limit: 20 });

// Get recommendations
const recs = await recommendationApi.getForAnime(animeId, 5);

// Login
const tokens = await authApi.login({ username, password });
```

## Authentication

Uses React Context for state management:

```tsx
import { useAuth } from '@/contexts/AuthContext';

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth();

  if (isAuthenticated) {
    // User is logged in
  }
}
```

## Running

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build
npm start
```

## Environment Variables

`.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/src/
├── app/                  # App router pages
│   ├── page.tsx         # Homepage
│   ├── anime/[id]/      # Dynamic anime pages
│   ├── login/           # Login page
│   ├── register/        # Register page
│   └── profile/         # Profile page
├── components/          # Reusable components
│   ├── AnimeCard.tsx
│   ├── Navbar.tsx
│   └── RecommendationList.tsx
├── contexts/            # React contexts
│   └── AuthContext.tsx
├── lib/                 # Utilities
│   └── api.ts          # API client
└── types/              # TypeScript types
    └── index.ts
```

## Styling

Uses Tailwind CSS with custom configuration:

- Primary color: Blue (customizable in `tailwind.config.js`)
- Responsive breakpoints
- Utility classes
- Custom components

## Type Safety

All API responses are typed:

```typescript
import type { Anime, User, Recommendation } from '@/types';
```

## Best Practices

- Use TypeScript for type safety
- Use client components (`'use client'`) for interactivity
- Use server components for static content
- Implement proper error handling
- Use loading states for better UX
- Validate forms before submission

## Deployment

### Vercel (Recommended)

```bash
npm run build
vercel deploy
```

### Other Platforms

```bash
# Build
npm run build

# Start production server
npm start
```

Set environment variables in your deployment platform:
- `NEXT_PUBLIC_API_URL`: Your backend API URL
