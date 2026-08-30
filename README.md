# BillLens

AI-powered parliamentary intelligence for everyone.


## Overview

BillLens helps citizens understand what UK Parliament has done, debated, or voted on. It combines parliamentary records from multiple sources, verifies claims against evidence, and provides confidence scores for transparency.

## Features

- **Multi-source research**: Searches bills, debates, votes, legislation, and MPs
- **Evidence verification**: Checks claims against retrieved evidence with confidence scoring
- **Transparent results**: Shows all sources, warnings, and unverified claims
- **API & Dashboard**: REST API for integration, web dashboard for exploration
- **Caching & persistence**: Redis cache and PostgreSQL database

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -e .
```

2. Run tests:
```bash
python -m pytest
```

3. Start the API:
```bash
python -m uvicorn apps.api.main:app --reload
```

API available at `http://localhost:8000`

### Dashboard

In a separate terminal:
```bash
streamlit run apps/web/dashboard/app.py
```

Dashboard available at `http://localhost:8501`

## Project Structure

```
billlens/
├── agent/              # Planning, research, verification, answer generation
├── data/               # Parliament, Lex, bills, MPs, votes clients
├── models/             # Pydantic domain models
├── retrieval/          # BM25, semantic, hybrid search
├── persistence/        # Database and cache layers
apps/
├── api/                # FastAPI application
└── web/dashboard/      # Streamlit dashboard
tests/                  # Test suite
docs/                   # Architecture and API docs
```

## API Usage

### Ask a Question

```bash
curl -X POST http://localhost:8000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{"question": "What laws have changed about housing?"}'
```

Response:
```json
{
  "question": "What laws have changed about housing?",
  "summary": "...",
  "what_happened": [...],
  "legislation": [...],
  "parliamentary_activity": [...],
  "votes": [...],
  "what_did_not_happen": [...],
  "claims": [...],
  "sources": [...],
  "confidence": 0.75,
  "warnings": [...]
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Architecture

```
Question
    ↓
Planner (identify research steps)
    ↓
Researcher (execute steps, gather evidence)
    ↓
ClaimExtractor (convert evidence to claims)
    ↓
Verifier (check claims against evidence)
    ↓
AnswerGenerator (format final response)
    ↓
Answer (with sources, confidence, warnings)
```

## Data Sources

- **Parliament API**: Bills, debates, votes, MPs
- **Lex API**: UK legislation
- **Hansard**: Parliamentary debates (via Parliament API)

## Confidence Scoring

Confidence is calculated from:
- **Lexical overlap**: Keyword matching between claim and evidence
- **Semantic relevance**: Retrieved evidence relevance score
- **Source diversity**: Multiple sources increase confidence
- **Minimum threshold**: 0.35 to be considered supported

## Limitations

- Deterministic planning (no LLM-based reasoning yet)
- BM25 search only (Qdrant vector store not yet integrated)
- No amendment tracking
- Limited MP biographical data

## Testing

```bash
# Run all tests
python -m pytest

# With coverage
python -m pytest --cov=billlens --cov=apps

# Linting
ruff check .

# Type checking
mypy billlens apps
```

## Environment Variables

See `.env.example` for all options:

```
PARLIAMENT_API_URL      # Parliament API endpoint
LEX_API_URL             # Lex (legislation) API endpoint
DATABASE_URL            # PostgreSQL connection string
REDIS_URL               # Redis connection string
API_URL                 # API base URL (for dashboard)
EMBEDDING_MODEL         # Sentence Transformers model name
```

## Documentation

- [API Reference](docs/api.md)
- [Architecture](docs/architecture.md)
- [Development Guide](docs/development.md)
- [Data Sources](docs/data-sources.md)
- [Retrieval System](docs/retrieval.md)
- [Verification & Confidence](docs/verification.md)

## Status

**MVP (Minimum Viable Product)**

The project is functionally complete with:
- Full question-answering pipeline
- Evidence verification
- REST API
- Web dashboard
- Database persistence
- Redis caching

## License

MIT
