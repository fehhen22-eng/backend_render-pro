# H2H Predictor - Head-to-Head Football Match Analysis Platform

## Overview

H2H Predictor is a comprehensive football match analysis platform that provides detailed head-to-head statistics, predictions, and betting insights. The system consists of a FastAPI backend that processes match data from CSV files and a React-based frontend dashboard for visualization and interaction.

The platform enables users to:
- Analyze confrontations between teams with advanced statistics
- Access Asian handicap market predictions (conservative and bold strategies)
- Import and manage league/team data via CSV uploads
- Automatically update team statistics from SofaScore API
- View detailed probabilistic predictions for match outcomes

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture (FastAPI)

**Framework**: Python FastAPI with CORS middleware for cross-origin requests

**API Structure**:
- RESTful endpoints organized by domain (leagues, teams, h2h, upload, update)
- Proxy configuration through Vite for `/api` routes
- Two separate backend implementations exist in the repository:
  - Root-level: Simpler implementation with basic H2H analysis
  - `h2h_backend_painel_refinado/backend`: Enhanced version with Asian markets and team logos

**Data Processing**:
- CSV-based data storage for team statistics (one CSV per team per league)
- Pandas DataFrames for statistical calculations
- File-based league/team organization: `data/leagues/{league_id}/{team_slug}.csv`
- Team name normalization using slugification (converts "Manchester United" to "manchester-united")

**Analysis Engine**:
- H2H analyzer calculates probabilities, over/under, BTTS, corners, shots, cards
- Asian handicap market analysis with conservative and bold betting strategies
- Statistical aggregation from historical match data
- Safe mean calculations with fallback values for missing data

**Update Mechanism**:
- APScheduler for background updates (48-hour intervals)
- SofaScore API integration for fetching live team statistics
- Incremental CSV updates without data loss
- Team logo caching system with local storage

**Design Rationale**: 
- CSV storage chosen for simplicity and portability over traditional databases
- File-based approach allows easy manual data inspection and modification
- Separate implementations allow for gradual feature rollout

### Frontend Architecture (React + TypeScript)

**Framework**: React 18 with TypeScript, built using Vite

**UI Library**: shadcn/ui components based on Radix UI primitives
- Provides accessible, customizable component system
- Tailwind CSS for styling with custom design tokens
- Dark theme optimized with HSL color system

**State Management**:
- TanStack Query (React Query) for server state and caching
- Local component state for UI interactions
- No global state library needed due to query-based architecture

**Routing**: React Router v6 for client-side navigation

**Key Features**:
- League and team selection with dynamic loading
- H2H analysis results display with statistical visualizations
- CSV import dialog with league/team management
- Responsive design with mobile breakpoints at 768px
- Progress indicators and loading states

**Replit Optimization**:
- Fixed port 5000 for webview compatibility
- Host set to 0.0.0.0 for external access
- Vite HMR configured for Replit environment
- Proxy configuration handles API routing

**Design Rationale**:
- Vite chosen for fast development experience and optimal bundling
- shadcn/ui provides consistency without heavy framework overhead
- TypeScript with relaxed settings (`strict: false`) for faster development
- Component-based architecture with clear separation of concerns

### Data Flow

1. User selects league → Frontend fetches leagues from `/api/leagues`
2. User selects teams → Frontend fetches teams from `/api/league/{league_id}/teams`
3. User requests analysis → Frontend POST to `/api/h2h` with league_id, team1_id, team2_id
4. Backend loads CSV files for both teams
5. H2H analyzer processes data and generates predictions
6. Frontend displays results with statistical breakdowns

### File Organization

**Backend Modules**:
- `routers/`: API endpoint definitions (leagues, teams, h2h, upload, update, logos)
- `utils/`: Helper functions (h2h_engine, csv_loader, logo_cache)
- `updater/`: Background update services (sofascorer, update_engine)

**Frontend Modules**:
- `src/pages/`: Page components (Index, NotFound)
- `src/components/`: Reusable UI components (AnalysisResults, ImportDialog, StatBar)
- `src/components/ui/`: shadcn/ui component library
- `src/hooks/`: Custom React hooks (use-toast, use-mobile)

**Data Directory**:
- `data/leagues/{league_id}/`: Contains team CSVs and `liga.json` metadata
- League metadata includes: league name, slug, ID, season, country

## External Dependencies

### Third-Party APIs

**SofaScore API**:
- Base URL: `https://api.sofascore.com/api/v1`
- Used for: Team search, match statistics, team logos
- Authentication: User-Agent header simulation
- Rate limiting: Not explicitly implemented (relies on polite scraping)
- Fallback: System continues to work with existing CSV data if API unavailable

**API Endpoints Used**:
- `/search/all` - Team search by name
- `/team/{team_id}/events/last/0` - Recent match events
- `/event/{match_id}/statistics` - Detailed match statistics
- `/team/{team_id}/image` - Team logo images

### Python Dependencies

**Core Framework**:
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server for running FastAPI

**Data Processing**:
- `pandas` - DataFrame operations and CSV handling
- `requests` - HTTP client for SofaScore API calls

**File Handling**:
- `python-multipart` - Multipart form data parsing for file uploads

**Background Tasks**:
- `apscheduler` - Scheduled background updates (optional dependency)

### JavaScript/Node Dependencies

**Core Framework**:
- `react` ^18.3.1 - UI library
- `react-dom` ^18.3.1 - React DOM rendering
- `vite` - Build tool and dev server

**UI Components**:
- `@radix-ui/*` - Headless UI component primitives (17+ packages)
- `lucide-react` - Icon library
- `tailwindcss` - Utility-first CSS framework

**Form & Validation**:
- `react-hook-form` - Form state management
- `@hookform/resolvers` - Form validation resolvers
- `zod` - Schema validation

**Data Fetching**:
- `@tanstack/react-query` ^5.83.0 - Server state management and caching

**Routing**:
- `react-router-dom` - Client-side routing

**Utilities**:
- `date-fns` - Date manipulation
- `clsx` + `tailwind-merge` - Conditional className utilities
- `class-variance-authority` - Component variant system

### Data Storage

**File System**:
- No database required - all data stored in CSV files
- Team logos cached in `backend/data/team_logos/`
- Configuration stored in `config/settings.py` and `liga.json` files

**CSV Schema** (typical columns):
- `team_id` - SofaScore team identifier
- `team_name` - Display name
- Match statistics: goals_scored, goals_conceded, corners, shots, cards
- Rate statistics: win_rate, rpg (rating per game), power_index

### Deployment Considerations

**Environment Variables**:
- `VITE_API_BASE` - API base URL for frontend (defaults to `/api`)
- `PORT` - Server port (Render deployment)

**Build Process**:
- Frontend: `npm run build` generates static files in `dist/`
- Backend: No build step, runs directly with `uvicorn`

**Hosting Platforms**:
- Replit: Configured with port 5000, host 0.0.0.0
- Render: Uses $PORT environment variable
- Generic: Requires proxy configuration for API routes