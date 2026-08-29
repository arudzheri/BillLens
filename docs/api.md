
# BillLens API Reference

## Overview

REST API for parliamentary question answering.

Base URL: `http://localhost:8000`

## Endpoints

### Health Check

```
GET /health
```

Returns liveness status.

**Response:**
```json
{
  "status": "ok",
  "service": "billlens"
}
```

### Readiness Check

```
GET /ready
```

Returns readiness status (dependencies available).

**Response:**
```json
{
  "status": "ready",
  "service": "billlens"
}
```

### Ask Question

```
POST /api/v1/questions
```

Submit a question about UK Parliament.

**Request:**
```json
{
  "question": "string (3-2000 chars)"
}
```

**Response:**
```json
{
  "question": "string",
  "summary": "string",
  "what_happened": ["string"],
  "legislation": ["string"],
  "parliamentary_activity": ["string"],
  "votes": ["string"],
  "what_did_not_happen": ["string"],
  "claims": [
    {
      "text": "string",
      "supported": "boolean",
      "confidence": "float (0-1)",
      "sources": [
        {
          "title": "string",
          "source_type": "string",
          "url": "string or null",
          "date": "string or null"
        }
      ]
    }
  ],
  "sources": [
    {
      "title": "string",
      "source_type": "string",
      "url": "string or null",
      "date": "string or null"
    }
  ],
  "confidence": "float (0-1)",
  "warnings": ["string"]
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid question
- `500 Internal Server Error`: Processing error

## Models

### QuestionRequest

```json
{
  "question": "string"
}
```

Constraints:
- Minimum length: 3 characters
- Maximum length: 2000 characters

### AnswerResponse

Main response model containing all answer information, evidence, and confidence data.

### Evidence

Retrieved evidence from parliamentary or legislative sources.

Fields:
- `title`: Evidence title
- `content`: Evidence text
- `source_type`: parliament_bills, parliament_debates, parliament_votes, legislation, hansard
- `url`: Source URL (optional)
- `date`: Publication/debate date (optional)
- `relevance_score`: 0-1 relevance
- `metadata`: Additional source-specific data

## Error Handling

All errors return JSON:

```json
{
  "detail": "error message"
}
```

## Rate Limiting

None currently. Production deployment should add rate limiting via reverse proxy.

## Caching

Responses are cached in Redis for 1 hour by default. Cache key includes question text hash.

## Authentication

None currently. Production deployment should add authentication.
