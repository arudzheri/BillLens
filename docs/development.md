
# Development Guide

## Setup

### Requirements
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- pip/poetry

### Installation

```bash
# Clone repository
git clone https://github.com/arudzheri/BillLens.git
cd BillLens

# Create environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -e .
pip install -e ".[dev]"
```

### Database Setup

```bash
# Set DATABASE_URL in .env
export DATABASE_URL=postgresql+asyncpg://user:password@localhost/billlens

# Run migrations (when available)
alembic upgrade head
```

### Environment

Copy `.env.example` to `.env` and update values.

## Running Locally

### Terminal 1: API

```bash
python -m uvicorn apps.api.main:app --reload --port 8000
```

API at `http://localhost:8000`

### Terminal 2: Dashboard

```bash
streamlit run apps/web/dashboard/app.py
```

Dashboard at `http://localhost:8501`

### Terminal 3 (optional): Redis

```bash
redis-server
```

## Testing

```bash
# All tests
python -m pytest

# Specific file
python -m pytest tests/test_orchestrator.py

# With output
python -m pytest -s

# Coverage report
python -m pytest --cov=billlens --cov=apps --cov-report=html
```

## Code Quality

```bash
# Linting
ruff check .
ruff format .

# Type checking
mypy billlens apps

# All checks
python -m pytest && ruff check . && mypy billlens apps
```

## Project Structure

```
billlens/
├── agent/
│   ├── planner.py         # Research planning
│   ├── researcher.py      # Evidence gathering
│   ├── claims.py          # Claim extraction
│   ├── verifier.py        # Claim verification
│   ├── answer.py          # Answer generation
│   └── orchestrator.py    # Main pipeline
├── data/
│   ├── parliament.py      # Parliament API client
│   ├── lex.py             # Lex API client
│   ├── legislation.py     # Legislation retrieval
│   └── cache.py           # Redis cache
├── models/                # Pydantic domain models
├── retrieval/             # Search and ranking
└── persistence/           # Database and repos
apps/
├── api/
│   ├── main.py            # FastAPI app
│   ├── dependencies.py    # Dependency injection
│   └── routes/            # Endpoint handlers
└── web/dashboard/         # Streamlit app
tests/                     # Test suite
```

## Common Tasks

### Adding a New Data Source

1. Create `billlens/data/newsource.py`
2. Implement client class with `search()` method
3. Return `Evidence` objects
4. Update `billlens/agent/researcher.py` to call it
5. Add tests in `tests/test_newsource.py`

### Adding an API Endpoint

1. Create route file in `apps/api/routes/`
2. Import in `apps/api/main.py`
3. Include router: `app.include_router(router)`
4. Add test in `tests/test_api_*.py`

### Modifying Domain Models

1. Edit file in `billlens/models/`
2. Update `__init__.py` exports
3. Update tests that use the model
4. Document breaking changes

## Debugging

### Enable verbose logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test a specific component

```bash
python -c "from billlens.agent.orchestrator import BillLensOrchestrator; print('works')"
```

### Database queries

Enable SQLAlchemy echo:
```python
Database(..., echo=True)
```

## Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... code to profile ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative').print_stats(10)
```

## Deployment Checklist

- [ ] Environment variables set
- [ ] Database migrated
- [ ] Tests passing
- [ ] Linting clean
- [ ] Type checking clean
- [ ] Docker builds successfully
- [ ] Health check working
- [ ] API responding
- [ ] Dashboard loading
- [ ] Rate limiting configured (if needed)
- [ ] Authentication enabled (if needed)
