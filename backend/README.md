# Implodesc Backend

AI-driven supply chain analysis API built with FastAPI.

## Quick Start

### Prerequisites
- Python 3.11+
- UV package manager
- Redis (for caching and task queue)
- PostgreSQL (for data storage)

### Installation

1. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start development server:
```bash
uvicorn src.implodesc.main:app --reload --host 0.0.0.0 --port 8000
```

### Development Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src/implodesc --cov-report=html

# Lint code
ruff check .

# Format code
black .

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

## API Documentation

When running in development mode, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
src/implodesc/
├── main.py              # FastAPI application
├── core/                # Core configuration and utilities
│   ├── config.py       # Settings management
│   └── logging.py      # Structured logging
├── api/                # API routes and endpoints
│   └── routes/         # Route modules
├── services/           # Business logic services
├── models/             # Database models
└── utils/              # Utility functions

tests/
├── unit/               # Unit tests
└── integration/        # Integration tests
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `OPENAI_API_KEY` - OpenAI API key for AI analysis
- `ANTHROPIC_API_KEY` - Anthropic API key (alternative AI provider)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

## Health Checks

- `/health/` - Basic health check
- `/health/ready` - Readiness check with dependencies
- `/health/live` - Liveness check for Kubernetes