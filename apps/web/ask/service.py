from __future__ import annotations

from billlens.ask.schemas import (
    AskRequest,
    AskResponse,
    AskSource,
)


class AskService:
    """
    Main orchestration service for Ask Parliament.
    """

    def __init__(
        self,
        planner=None,
        researcher=None,
        verifier=None,
        answer_generator=None,
    ):
        self.planner = planner

        self.researcher = researcher

        self.verifier = verifier

        self.answer_generator = (
            answer_generator
        )

    async def ask(
        self,
        request: AskRequest,
    ) -> AskResponse:

        question = request.question

        # --------------------------------------------------
        # 1. Create research plan
        # --------------------------------------------------

        if self.planner:

            plan = await self.planner.plan(
                question
            )

        else:

            plan = {
                "question": question,
                "queries": [question],
            }

        # --------------------------------------------------
        # 2. Research
        # --------------------------------------------------

        if self.researcher:

            evidence = await self.researcher.research(
                plan
            )

        else:

            evidence = []

        # --------------------------------------------------
        # 3. Verify
        # --------------------------------------------------

        if self.verifier:

            verified = await self.verifier.verify(
                question,
                evidence,
            )

        else:

            verified = evidence

        # --------------------------------------------------
        # 4. Generate answer
        # --------------------------------------------------

        if self.answer_generator:

            result = await self.answer_generator.generate(
                question,
                verified,
            )

            return result

        # --------------------------------------------------
        # Fallback
        # --------------------------------------------------

        sources = [
            AskSource(
                title=item.title,
                source_type=item.source_type,
                url=item.url,
                date=item.date,
            )
            for item in verified[:5]
        ]

        return AskResponse(
            question=question,
            answer=(
                "BillLens found "
                f"{len(verified)} relevant "
                "pieces of parliamentary evidence."
            ),
            confidence=0.0,
            sources=sources,
            warnings=[
                "AI answer generation is not configured."
            ],
        )
