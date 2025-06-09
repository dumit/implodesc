## How you work
- For any new work, you always create a new git worktree unless otherwise asked
    - Command for that: `git worktree add ../my-feature-branch -b feature/new-feature`
- Read the current `global_state.md` to understand what has currently been done and the current state of the project relative to where it needs to go.
- Think through a plan and communicate back to the user. The user will either confirm or tell you what to update and iterate.
- Once the plan is agreed upon, write to plans/plan_for_{feature_X}.md
- Then, do the work as planned marking off in the plans/plan_for_{feature_X}.md as you go.
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
- Use `uv` for package maintenance
- Use `ruff` for linting
- Use types for everything. That includes all function signatures.
- Use `mypy` for static analysis
- Prefer `pydantic` types for passing around data to make it really easy.
- All checks will run automatically with `pre-commit` so use commits liberally rather than dealing with it all yourself.
- Use FastAPI for the combination of pydantic and easy server setup.

### Typescript / front end
- Maintain 90% test coverage with unit tests
- Use typescript for everything and always in strict mode
- Eslint + prettier
- Next.js 14+ (App Router) for core framework and routing
- Jest + React Testing Library for unit testing (Next.js default)
- Zustand for state management
- Let's use `zod` for schema validation
- `Playwright` for integration testing

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
├── scripts/         # Deployment/utility scripts
├── plans/           # Plans for working with claude code
└── .github/workflows/ # CI/CD pipelines