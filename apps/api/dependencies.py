"""
Dependency injection for API routes.
"""

from __future__ import annotations

import os
from typing import AsyncGenerator

from billlens.data.cache import Cache
from billlens.agent.orchestrator import BillLensOrchestrator


async def get_orchestrator() -> BillLensOrchestrator:
    """Get the orchestrator instance."""
    lex_base_url = os.getenv("LEX_API_URL")
    parliament_base_url = os.getenv("PARLIAMENT_API_URL")
    
    return BillLensOrchestrator(
        lex_base_url=lex_base_url,
        parliament_base_url=parliament_base_url,
        timeout=30.0,
    )


async def get_cache() -> Cache:
    """Get Redis cache instance."""
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    return Cache(url=redis_url)