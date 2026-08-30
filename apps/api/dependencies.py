"""
Dependency injection helpers for FastAPI endpoints.
"""

from __future__ import annotations

import os

from billlens.agent.orchestrator import BillLensOrchestrator
from billlens.agent.researcher import BillLensResearcher


def get_orchestrator() -> BillLensOrchestrator:
    """
    Dependency provider for BillLensOrchestrator.
    """
    lex_url = os.getenv("LEX_BASE_URL")
    parliament_url = os.getenv("PARLIAMENT_BASE_URL")

    researcher = BillLensResearcher(
        lex_base_url=lex_url,
        parliament_base_url=parliament_url,
    )

    return BillLensOrchestrator(researcher=researcher)