"""
BillLens Research Planner

Turns a citizen's natural-language question into a structured
research plan for the BillLens agent.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ResearchType(str, Enum):
    LEGISLATION = "legislation"
    BILLS = "bills"
    DEBATES = "debates"
    VOTES = "votes"
    MPS = "mps"
    AMENDMENTS = "amendments"
    TIMELINE = "timeline"


class ResearchStep(BaseModel):
    type: ResearchType
    question: str
    keywords: List[str] = Field(default_factory=list)
    priority: int = 1


class ResearchPlan(BaseModel):
    original_question: str
    topic: str
    steps: List[ResearchStep]
    requires_mp_lookup: bool = False
    requires_vote_lookup: bool = False
    requires_timeline: bool = False


class BillLensPlanner:
    """
    Converts a user question into a multi-source research plan.

    This first version uses deterministic planning so that the system
    is predictable. An LLM can later be added for more sophisticated
    planning.
    """

    def create_plan(self, question: str) -> ResearchPlan:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        normalized = question.lower()

        steps: list[ResearchStep] = []

        topic = self._extract_topic(normalized)

        # Always investigate legislation for policy questions.
        steps.append(
            ResearchStep(
                type=ResearchType.LEGISLATION,
                question=f"What legislation is relevant to: {topic}?",
                keywords=[topic],
                priority=1,
            )
        )

        # Bills
        if any(
            word in normalized
            for word in ["bill", "bills", "legislation", "law", "laws"]
        ):
            steps.append(
                ResearchStep(
                    type=ResearchType.BILLS,
                    question=f"What bills concerning {topic} were introduced or progressed?",
                    keywords=[topic, "bill"],
                    priority=1,
                )
            )

        # Debates
        if any(
            word in normalized
            for word in ["discuss", "discussed", "debate", "debated", "parliament"]
        ):
            steps.append(
                ResearchStep(
                    type=ResearchType.DEBATES,
                    question=f"What has Parliament debated about {topic}?",
                    keywords=[topic, "debate"],
                    priority=1,
                )
            )

        # Votes
        requires_votes = any(
            word in normalized
            for word in ["vote", "voted", "voting", "division"]
        )

        if requires_votes:
            steps.append(
                ResearchStep(
                    type=ResearchType.VOTES,
                    question=f"What parliamentary votes relate to {topic}?",
                    keywords=[topic, "vote"],
                    priority=1,
                )
            )

        # MPs
        requires_mp = any(
            word in normalized
            for word in ["mp", "mps", "member", "members", "my mp"]
        )

        if requires_mp:
            steps.append(
                ResearchStep(
                    type=ResearchType.MPS,
                    question=f"Which MPs are associated with {topic}?",
                    keywords=[topic, "MP"],
                    priority=1,
                )
            )

        # Amendments
        if any(
            word in normalized
            for word in ["amendment", "amendments", "changed", "change"]
        ):
            steps.append(
                ResearchStep(
                    type=ResearchType.AMENDMENTS,
                    question=f"What amendments changed legislation concerning {topic}?",
                    keywords=[topic, "amendment"],
                    priority=2,
                )
            )

        # Timeline
        requires_timeline = any(
            word in normalized
            for word in ["what happened", "history", "since", "over time", "actually"]
        )

        if requires_timeline:
            steps.append(
                ResearchStep(
                    type=ResearchType.TIMELINE,
                    question=f"What is the timeline of parliamentary action on {topic}?",
                    keywords=[topic],
                    priority=2,
                )
            )

        steps.sort(key=lambda step: step.priority)

        return ResearchPlan(
            original_question=question,
            topic=topic,
            steps=steps,
            requires_mp_lookup=requires_mp,
            requires_vote_lookup=requires_votes,
            requires_timeline=requires_timeline,
        )

    @staticmethod
    def _extract_topic(question: str) -> str:
        """
        Basic topic extraction.

        Replace this with an LLM/entity extraction layer later.
        """

        prefixes = [
            "what laws have changed about ",
            "what laws changed about ",
            "what has parliament actually done about ",
            "what has parliament done about ",
            "what has parliament done on ",
            "what has parliament discussed about ",
            "what has parliament discussed on ",
            "tell me about ",
            "what happened with ",
        ]

        cleaned = question.strip(" ?.").lower()

        for prefix in prefixes:
            if cleaned.startswith(prefix):
                return cleaned[len(prefix):].strip(" ?.")

        return cleaned