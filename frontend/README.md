# Implodesc Frontend

Modern web interface for AI-driven supply chain analysis built with Next.js 14.

## Quick Start

### Prerequisites
- Node.js 18.17+
- npm 9.0+

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment:
```bash
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

3. Start development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Development Commands

```bash
# Development
npm run dev           # Start development server
npm run build         # Build for production
npm run start         # Start production server

# Code Quality
npm run lint          # Run ESLint
npm run lint:fix      # Fix ESLint issues
npm run type-check    # Run TypeScript type checking
npm run format        # Format code with Prettier
npm run format:check  # Check code formatting

# Testing
npm run test          # Run unit tests
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Run tests with coverage
npm run test:e2e      # Run E2E tests with Playwright
npm run test:e2e:ui   # Run E2E tests with UI
```

## Features

- **Next.js 14** with App Router and TypeScript
- **Tailwind CSS** with custom design system
- **shadcn/ui** component library
- **Clerk** authentication
- **Zustand** state management
- **React Query** for server state
- **Zod** schema validation
- **Recharts** for data visualization
- **D3.js** for advanced visualizations

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── (auth)/         # Authentication routes
│   ├── analyze/        # Analysis pages
│   ├── dashboard/      # User dashboard
│   └── globals.css     # Global styles
├── components/         # React components
│   └── ui/            # shadcn/ui components
├── lib/               # Utility libraries
├── hooks/             # Custom React hooks
├── store/             # Zustand stores
├── types/             # TypeScript type definitions
└── utils/             # Utility functions
```

## Environment Variables

See `.env.local.example` for all available configuration options.

Key variables:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk authentication
- `CLERK_SECRET_KEY` - Clerk server-side authentication
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Authentication

Authentication is handled by Clerk with the following routes:
- `/sign-in` - User sign in
- `/sign-up` - User registration
- `/dashboard` - Protected user dashboard

## API Integration

The frontend communicates with the backend through:
- RESTful API endpoints
- React Query for caching and state management
- Type-safe API calls with Zod validation

## Deployment

The application is ready for deployment on Vercel, Netlify, or any Node.js hosting platform.

Build the application:
```bash
npm run build
```

The built application will be in the `.next` directory.