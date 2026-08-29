"""
BillLens API Application
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import questions

# Initialize FastAPI app
app = FastAPI(
    title="BillLens API",
    description="AI-powered parliamentary intelligence",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions.router)


@app.get("/health")
async def health() -> dict[str, str]:
    """
    Liveness check.
    """
    return {
        "status": "ok",
        "service": "billlens",
    }


@app.get("/ready")
async def ready() -> dict[str, str]:
    """
    Readiness check.
    """
    return {
        "status": "ready",
        "service": "billlens",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )