from __future__ import annotations

from typing import Any

from billlens.ask.schemas import AskRequest, AskResponse, AskSource


class AskService:
    """
    Orchestrates the BillLens Ask Parliament pipeline.

    Pipeline:

        Question
            ↓
        Planner
            ↓
        Researcher
            ↓
        Verifier
            ↓
        Answer Generator
    """

    def __init__(
        self,
        planner: Any = None,
        researcher: Any = None,
        verifier: Any = None,
        answer_generator: Any = None,
    ):
        self.planner = planner
        self.researcher = researcher
        self.verifier = verifier
        self.answer_generator = answer_generator

    async def ask(
        self,
        request: AskRequest,
    ) -> AskResponse:

        question = request.question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        # -------------------------------------------------
        # 1. Planning
        # -------------------------------------------------

        if self.planner:

            plan = await self.planner.plan(
                question
            )

        else:

            plan = {
                "question": question,
                "queries": [question],
            }

        # -------------------------------------------------
        # 2. Research
        # -------------------------------------------------

        if self.researcher:

            evidence = await self.researcher.research(
                plan
            )

        else:

            evidence = []

        # -------------------------------------------------
        # 3. Verification
        # -------------------------------------------------

        if self.verifier:

            verified = await self.verifier.verify(
                question=question,
                evidence=evidence,
            )

        else:

            verified = evidence

        # -------------------------------------------------
        # 4. Answer generation
        # -------------------------------------------------

        if self.answer_generator:

            return await self.answer_generator.generate(
                question=question,
                evidence=verified,
            )

        # -------------------------------------------------
        # Fallback response
        # -------------------------------------------------

        sources = []

        for item in verified[:10]:

            sources.append(
                AskSource(
                    title=getattr(
                        item,
                        "title",
                        "Parliamentary source",
                    ),
                    source_type=getattr(
                        item,
                        "source_type",
                        "unknown",
                    ),
                    url=getattr(
                        item,
                        "url",
                        None,
                    ),
                    date=getattr(
                        item,
                        "date",
                        None,
                    ),
                )
            )

        return AskResponse(
            question=question,
            answer=(
                "BillLens found "
                f"{len(verified)} relevant pieces "
                "of evidence."
            ),
            confidence=0.0,
            sources=sources,
            warnings=[
                "Answer generation is not configured."
            ],
        )
