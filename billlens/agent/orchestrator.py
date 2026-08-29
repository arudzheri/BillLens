"""
BillLens Orchestrator

Central application service that connects planning, research,
verification, and answer generation.
"""

from __future__ import annotations

import hashlib
from typing import Optional

from billlens.models.question import QuestionRequest
from billlens.models.answer import AnswerResponse, AnswerClaim, AnswerSource
from billlens.models.evidence import Evidence

from .planner import BillLensPlanner
from .researcher import BillLensResearcher
from .verifier import BillLensVerifier
from .answer import BillLensAnswerGenerator
from .claims import ClaimExtractor


class BillLensOrchestrator:
    """
    Orchestrates the entire question-answering pipeline.
    
    Flow:
    1. Plan: Parse question into research steps
    2. Research: Execute steps and gather evidence
    3. Extract: Convert evidence into claims
    4. Verify: Check claims against evidence
    5. Generate: Build final answer response
    """
    
    def __init__(
        self,
        lex_base_url: Optional[str] = None,
        parliament_base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.planner = BillLensPlanner()
        self.researcher = BillLensResearcher(
            lex_base_url=lex_base_url,
            parliament_base_url=parliament_base_url,
            timeout=timeout,
        )
        self.claim_extractor = ClaimExtractor()
        self.verifier = BillLensVerifier()
        self.answer_generator = BillLensAnswerGenerator()
    
    async def answer(
        self,
        request: QuestionRequest,
    ) -> AnswerResponse:
        """
        Process a question and return a verified answer.
        """
        
        # Step 1: Plan the research
        plan = self.planner.create_plan(request.question)
        
        # Step 2: Execute research
        research_result = await self.researcher.research(plan)
        
        # Step 3: Extract claims from evidence
        claims = self.claim_extractor.extract(
            request.question,
            research_result.evidence,
        )
        
        # Step 4: Verify claims
        verification = self.verifier.verify(
            claims,
            research_result.evidence,
        )
        
        # Step 5: Generate answer
        answer = self.answer_generator.generate(
            request.question,
            verification,
            research_result.evidence,
        )
        
        return answer