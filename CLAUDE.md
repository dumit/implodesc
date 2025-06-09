## How you work
- For any new work, you always create a new git worktree unless otherwise asked
    - Command for that: `git worktree add ../my-feature-branch -b feature/new-feature`
- Read the current `global_state.md` to understand what has currently been done and the current state of the project relative to where it needs to go.
- Check `docs/development_log.md` for detailed development history and lessons learned
- Think through a plan and communicate back to the user. The user will either confirm or tell you what to update and iterate.
- Once the plan is agreed upon, write to plans/plan_for_{feature_X}.md
- Then, do the work as planned marking off in the plans/plan_for_{feature_X}.md as you go.
- **Always update `docs/development_log.md`** with detailed progress, issues encountered, and solutions found
- When the work is done, go and check in with the user. Recommend how to test the change and then wait for their confirmation that it is a good change:
    - Confirmation that the task is done
    - Or, what to update.
- Once the work is confirmed, you should make a pull request via the github cli.
    - Use git push and then make that a PR with a sufficient description.
    - Once the PR is made, you should remove the git worktree with the following command: `git worktree remove <worktree-path>`


## General principles for code and project structure
### Python side
- Maintain 90%+ test coverage with unit tests
- Write integration tests for CI/CD pipeline
- Use black for formatting
- Use pytest for testing
- Use `uv` for package maintenance - always run Python commands with `uv run <command>`
- Use `ruff` for linting
- Use types for everything. That includes all function signatures.
- Use `mypy` for static analysis
- Prefer `pydantic` types for passing around data to make it really easy.
- All checks will run automatically with `pre-commit` so use commits liberally rather than dealing with it all yourself.
- Use FastAPI for the combination of pydantic and easy server setup.
- **Test command**: `PYTHONPATH=src uv run pytest tests/unit/ -v` (from backend/ directory)
- **Import setup**: Tests should import from `implodesc.module` (not `src.implodesc.module`)
- **Virtual environment**: Always activate venv with `source .venv/bin/activate` before running commands

### Typescript / front end
- Maintain 90% test coverage with unit tests
- Use typescript for everything and always in strict mode
- Eslint + prettier
- Next.js 14+ (App Router) for core framework and routing
- Jest + React Testing Library for unit testing (Next.js default)
- Zustand for state management
- Let's use `zod` for schema validation
- `Playwright` for integration testing
- **Test command**: `npm run test` (from frontend/ directory)
- **Test with coverage**: `npm run test:coverage`
- **Common issues**: 
  - Install missing dependencies: `tailwindcss-animate` required for shadcn/ui
  - Environment variables: Create `.env.local` from `.env.local.example`
  - Mock Next.js Link component in tests

#### UI stuff
- Tailwind CSS + shadcn/ui
- Authentication: Clerk


### CI/CD + Infrastructure
- Project structure:
implodesc/
├── backend/          # Python API
├── frontend/         # TypeScript/React app
├── shared/           # Shared types/schemas
├── docs/            # Project documentation
│   └── development_log.md  # Detailed development history
├── scripts/         # Deployment/utility scripts
├── plans/           # Plans for working with claude code
└── .github/workflows/ # CI/CD pipelines

## Development Environment Setup
### Prerequisites
- Python 3.11+ (using Python 3.13.4)
- Node.js 18.17+
- UV package manager for Python
- npm for Node.js

### Quick Start Commands
```bash
# Backend setup
cd backend
uv venv --python python3
source .venv/bin/activate
uv pip install -e ".[dev]"

# Start backend server - PREFERRED METHOD (reliable startup)
source .venv/bin/activate && PYTHONPATH=src nohup python -c "
from implodesc.main import app
import uvicorn
uvicorn.run(app, host='127.0.0.1', port=8001)
" > server.log 2>&1 &

# Alternative: Start backend server (if the above fails)
uv run uvicorn src.implodesc.main:app --reload --host 127.0.0.1 --port 8001

# Frontend setup
cd frontend
npm install
npm run dev  # Usually starts on port 3000, may auto-switch to 3001 if 3000 is busy

# Health checks
curl http://127.0.0.1:8001/health/  # Backend
curl http://localhost:3001/test     # Frontend (adjust port as needed)
```

## Known Issues and Solutions
### Shared Module Imports
- **Issue**: Backend analysis endpoints import `....shared` which fails
- **Temporary fix**: Analysis routes disabled in `main.py`
- **Proper solution**: Redesign shared module architecture

### Authentication
- **Issue**: ClerkProvider requires environment variables
- **Temporary fix**: Commented out ClerkProvider in layout.tsx
- **Proper solution**: Set up Clerk credentials or use alternative auth

### Server Startup Issues
#### Backend Configuration (.env) Issues
- **Issue**: Pydantic settings expect JSON arrays, not comma-separated strings
- **Symptoms**: `ValidationError: Input should be a valid list` or `JSONDecodeError: Expecting value`
- **Solution**: Use JSON array format in `.env` file:
  ```bash
  # ❌ Wrong format (causes pydantic errors)
  CORS_ORIGINS=http://localhost:3000,http://localhost:3001
  ALLOWED_HOSTS=localhost,127.0.0.1
  
  # ✅ Correct format (JSON arrays)
  CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
  ALLOWED_HOSTS=["localhost","127.0.0.1"]
  ```

#### Backend Server Startup Issues
- **Issue**: `uv run uvicorn` sometimes fails with module import errors or port conflicts
- **Symptoms**: Server starts but dies immediately, or fails to bind to port
- **Solution 1 (Preferred)**: Use direct Python startup with background process:
  ```bash
  source .venv/bin/activate && PYTHONPATH=src nohup python -c "
  from implodesc.main import app
  import uvicorn
  uvicorn.run(app, host='127.0.0.1', port=8001)
  " > server.log 2>&1 &
  ```
- **Solution 2**: Kill existing processes and use alternative port:
  ```bash
  pkill -f uvicorn
  uv run uvicorn src.implodesc.main:app --host 127.0.0.1 --port 8001
  ```
- **Debugging**: Check `server.log` for detailed error messages
- **Testing config**: Create `debug_config.py` to test settings loading:
  ```python
  from implodesc.core.config import Settings
  settings = Settings()  # Should not raise exceptions
  ```

#### Port Management
- **Default ports**: Backend 8000 → 8001 (if conflict), Frontend 3000 → 3001 (auto-switch)
- **Port conflicts**: Use `lsof -i :8000` to check what's using a port
- **Frontend auto-switching**: Next.js automatically tries 3001 if 3000 is busy