"""
Dependency injection helpers for FastAPI endpoints.
"""

from __future__ import annotations

import os

from billlens.agent.orchestrator import BillLensOrchestrator
from billlens.agent.planner import BillLensPlanner
from billlens.agent.researcher import BillLensResearcher
from billlens.agent.verifier import BillLensVerifier
from billlens.agent.answer import BillLensAnswerGenerator


def get_orchestrator() -> BillLensOrchestrator:
    """
    Dependency provider for BillLensOrchestrator.
    Initializes all components: planner, researcher, verifier, and answer_generator.
    """
    lex_url = os.getenv("LEX_BASE_URL")
    parliament_url = os.getenv("PARLIAMENT_BASE_URL")

    # Initialize all required components
    planner = BillLensPlanner()
    researcher = BillLensResearcher(
        lex_base_url=lex_url,
        parliament_base_url=parliament_url,
    )
    verifier = BillLensVerifier()
    answer_generator = BillLensAnswerGenerator()

    return BillLensOrchestrator(
        planner=planner,
        researcher=researcher,
        verifier=verifier,
        answer_generator=answer_generator,
    )
