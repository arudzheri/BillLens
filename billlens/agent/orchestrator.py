"""
BillLens Orchestrator
"""

from __future__ import annotations

from billlens.agent.answer import BillLensAnswerGenerator
from billlens.agent.planner import BillLensPlanner
from billlens.agent.researcher import BillLensResearcher
from billlens.agent.verifier import BillLensVerifier, Claim
from billlens.models.answer import AnswerResponse
from billlens.models.question import QuestionRequest


class BillLensOrchestrator:

    def __init__(
        self,
        planner: BillLensPlanner | None = None,
        researcher: BillLensResearcher | None = None,
        verifier: BillLensVerifier | None = None,
        answer_generator: BillLensAnswerGenerator | None = None,
        **kwargs,
    ) -> None:
        self.planner = planner or BillLensPlanner()
        self.researcher = researcher or BillLensResearcher()
        self.verifier = verifier or BillLensVerifier()
        self.answer_generator = answer_generator or BillLensAnswerGenerator()

    async def answer(self, request: QuestionRequest) -> AnswerResponse:
        question = request.question

        # 1. Plan research
        plan = self.planner.create_plan(question)

        # 2. Gather live evidence
        research_result = await self.researcher.research(plan)

        # 3. Create claims from evidence safely
        claims = []
        if research_result and research_result.evidence:
            for item in research_result.evidence:
                claim_text = item.content or item.title
                if claim_text:
                    claims.append(Claim(text=str(claim_text)))

        # 4. Verify claims
        verification = self.verifier.verify(claims, research_result.evidence)

        # 5. Generate final structured response
        return self.answer_generator.generate(
            question=question,
            verification=verification,
            evidence=research_result.evidence,
        )