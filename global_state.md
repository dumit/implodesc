# Global State - Implodesc Project

## Project Vision
Implodesc is an AI-driven web interface for comprehensive supply chain analysis. Users input an item and receive:
- Step-by-step supply chain breakdown
- Underlying materials analysis  
- Carbon footprint calculations
- Potential companies/entities involved
- Interactive clarification for scope, quantity, specifications
- Graphically pleasing, interactive visualizations

## Current Status
Project initialized with basic directory structure and vision defined.

## What's Been Done
- [x] Created project directory structure:
  - backend/ - Python API for AI processing and data analysis ✅ INITIALIZED
  - frontend/ - TypeScript/React app with interactive UI ✅ INITIALIZED
  - shared/ - Shared types/schemas for supply chain data ✅ COMPLETE
  - docs/ - Project documentation (empty)
  - scripts/ - Deployment/utility scripts (empty)
  - plans/ - Plans for working with Claude Code ✅ ACTIVE
  - .github/workflows/ - CI/CD pipelines (empty)
- [x] Set up CLAUDE.md with development workflow and tech stack guidelines
- [x] Defined project vision and core requirements
- [x] Designed comprehensive data schemas (supply chain, carbon, API)
- [x] Initialized backend FastAPI application with:
  - [x] Complete project structure and dependencies
  - [x] Configuration management with Pydantic Settings
  - [x] Structured logging with structlog
  - [x] Health check endpoints
  - [x] Mock analysis API endpoints
- [x] Initialized frontend Next.js application with:
  - [x] Next.js 14+ with TypeScript and App Router
  - [x] Tailwind CSS with custom design system
  - [x] shadcn/ui component library
  - [x] Clerk authentication with protected routes
  - [x] Basic routing structure (home, analyze, dashboard, auth)
  - [x] React Query for API state management

## Current State
- **Backend**: FastAPI application structure complete, dependencies defined, but not yet installed
- **Frontend**: Next.js application fully functional and ready for development
- **Shared schemas**: Complete data models for supply chain analysis
- Development guidelines established in CLAUDE.md
- Clear vision for AI-driven supply chain analysis tool

## ⚠️ NEXT SESSION SETUP REQUIRED
To continue development, the next session needs to:

### Backend Setup (Required)
1. **Install Python dependencies**:
   ```bash
   cd backend
   # Install uv package manager (if not available)
   # Then install dependencies
   uv pip install -e ".[dev]"
   ```

2. **Start backend server**:
   ```bash
   uvicorn src.implodesc.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with API keys and configuration
   ```

### Frontend Setup (Ready)
1. **Install and start frontend**:
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local
   # Edit .env.local with Clerk keys
   npm run dev
   ```

### Missing Dependencies
- **Python environment**: uv package manager installation
- **Environment variables**: API keys for OpenAI/Anthropic, Clerk auth keys
- **Database**: PostgreSQL setup (optional for initial development)
- **Redis**: For caching (optional for initial development)

## Core Features Required
1. **Item Input & Clarification**: Smart form with AI-driven clarification questions
2. **Supply Chain Analysis Engine**: AI backend for processing and analysis
3. **Interactive Visualizations**: Charts, graphs, flow diagrams for supply chain
4. **Carbon Footprint Calculator**: Environmental impact analysis
5. **Company/Entity Database**: Identification of potential suppliers/manufacturers
6. **Data Export/Sharing**: Results sharing and export functionality

## Next Steps (Priority Order)
1. **Complete backend setup** - Install Python dependencies and start server
2. **Connect frontend to backend** - Implement API integration layer
3. **Build AI analysis pipeline** - OpenAI/Anthropic integration for supply chain analysis
4. **Implement clarification flow** - Interactive Q&A system
5. **Create visualization components** - Charts and diagrams for supply chain data
6. **Add carbon footprint calculations** - Real emission factor calculations
7. **Set up CI/CD pipeline** - Automated testing and deployment

## Architecture Notes
- Backend: Python with FastAPI, AI/ML libraries, pytest, ruff, mypy, pydantic
- Frontend: Next.js 14+ with TypeScript, Tailwind CSS, shadcn/ui, data visualization libs
- Authentication: Clerk for user management
- State Management: Zustand
- Testing: Jest + React Testing Library (frontend), pytest (backend)
- Integration Testing: Playwright
- AI Integration: OpenAI/Claude APIs for analysis, custom ML models for carbon calculations