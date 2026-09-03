# BillLens

AI-powered parliamentary intelligence for understanding UK legislation, debates, bills, votes, and MPs.

## Overview

BillLens researches parliamentary questions using data from UK Parliament and UK legislation sources. It returns evidence-backed answers with citations, confidence scores, and warnings when claims are not sufficiently supported.

## Features

- Multi-source research across bills, debates, legislation, votes, and MPs
- Deterministic research planning and evidence collection
- Hybrid retrieval with lexical and semantic-search support
- Claim extraction and evidence verification
- Source citations, confidence scores, and warnings
- FastAPI REST API
- Streamlit dashboard
- PostgreSQL persistence
- Redis caching
- Docker Compose development environment

## Project Structure

```text
billlens/
├── agent/          # Planning, research, verification, and answer generation
├── data/           # Parliament, bills, Hansard, legislation, votes, and MP clients
├── models/         # Domain models
├── persistence/    # Database and repository layers
└── retrieval/      # Search and citation utilities

apps/
├── api/             # FastAPI application
└── web/dashboard/   # Streamlit dashboard

tests/               # Automated tests
docs/                # API, architecture, and development documentation
```

## Quick Start

### Install

```bash
pip install -e .
```

### Configure

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

The application can run with local API services by default. PostgreSQL, Redis, and Qdrant are configured for the Docker Compose setup.

### Run the tests

```bash
python -m pytest
```

### Run the API

```bash
python -m uvicorn apps.api.main:app --reload --port 8000
```

The API is available at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Run the dashboard

In a separate terminal:

```bash
streamlit run apps/web/dashboard/app.py
```

The dashboard is available at http://localhost:8501.

### Run with Docker Compose

```bash
docker compose up --build
```

Stop the services with:

```bash
docker compose down
```

## API Usage

Ask a question:

```bash
curl -X POST http://localhost:8000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{"question":"What laws have changed about housing?"}'
```

The response includes an answer, parliamentary activity, legislation, votes, claims, source URLs, confidence, and warnings.

## Architecture

```text
Question
   ↓
Planner
   ↓
Researcher
   ↓
Claim Extractor
   ↓
Verifier
   ↓
Answer Generator
   ↓
Evidence-backed Answer
```

## Data Sources

- UK Parliament Members API
- UK Parliament Bills API
- Hansard and parliamentary debate data
- UK legislation at legislation.gov.uk

## Configuration

See `.env.example` for the complete configuration. Important variables include:

```text
API_URL
DASHBOARD_API_URL
PARLIAMENT_BASE_URL
LEX_BASE_URL
DATABASE_URL
REDIS_URL
QDRANT_URL
EMBEDDING_MODEL
```

## Documentation

- [API Reference](docs/api.md)
- [Architecture](docs/architecture.md)
- [Development Guide](docs/development.md)
- [Data Sources](docs/data-sources.md)
- [Retrieval System](docs/retrieval.md)
- [Verification and Confidence](docs/verification.md)

## Project Status

BillLens is an MVP. The current implementation includes the question-answering pipeline, evidence verification, REST API, Streamlit dashboard, persistence, caching, and retrieval components.

Known limitations include deterministic planning, limited amendment tracking, and incomplete MP biographical data.

## License

MIT