"""
BillLens Answer Generator

Produces a structured, evidence-backed answer from
verified parliamentary research.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .researcher import Evidence
from .verifier import VerificationResult


class AnswerSource(BaseModel):
    title: str
    url: str | None = None
    source_type: str


class BillLensAnswer(BaseModel):
    question: str
    summary: str
    what_happened: List[str] = Field(
        default_factory=list
    )
    legislation: List[str] = Field(
        default_factory=list
    )
    parliamentary_activity: List[str] = Field(
        default_factory=list
    )
    votes: List[str] = Field(
        default_factory=list
    )
    what_did_not_happen: List[str] = Field(
        default_factory=list
    )
    sources: List[AnswerSource] = Field(
        default_factory=list
    )
    confidence: float = 0.0
    warnings: List[str] = Field(
        default_factory=list
    )


class BillLensAnswerGenerator:

    def generate(
        self,
        question: str,
        verification: VerificationResult,
        evidence: List[Evidence],
    ) -> BillLensAnswer:

        supported = [
            claim
            for claim in verification.verified_claims
            if claim.supported
        ]

        unsupported = [
            claim
            for claim in verification.verified_claims
            if not claim.supported
        ]

        what_happened = []
        legislation = []
        parliamentary_activity = []
        votes = []

        for claim in supported:

            text = claim.claim

            source_types = {
                source.source_type
                for source in claim.supporting_evidence
            }

            if any(
                "legislation" in source
                for source in source_types
            ):
                legislation.append(text)

            elif any(
                "vote" in source
                for source in source_types
            ):
                votes.append(text)

            elif any(
                "debate" in source
                or "parliament" in source
                for source in source_types
            ):
                parliamentary_activity.append(text)

            else:
                what_happened.append(text)

        summary = self._build_summary(
            supported,
            question,
        )

        sources = self._build_sources(
            supported
        )

        warnings = list(
            verification.warnings
        )

        if unsupported:
            warnings.append(
                "Some claims could not be verified "
                "against the available evidence."
            )

        return BillLensAnswer(
            question=question,
            summary=summary,
            what_happened=what_happened,
            legislation=legislation,
            parliamentary_activity=parliamentary_activity,
            votes=votes,
            what_did_not_happen=[],
            sources=sources,
            confidence=verification.overall_confidence,
            warnings=warnings,
        )

    @staticmethod
    def _build_summary(
        claims,
        question: str,
    ) -> str:

        if not claims:
            return (
                "BillLens could not find enough "
                "verified evidence to answer this "
                "question confidently."
            )

        first_claims = [
            claim.claim
            for claim in claims[:3]
        ]

        return (
            "Based on the parliamentary and "
            "legislative evidence retrieved, "
            + " ".join(first_claims)
        )

    @staticmethod
    def _build_sources(
        claims,
    ) -> List[AnswerSource]:

        sources = []
        seen = set()

        for claim in claims:

            for evidence in claim.supporting_evidence:

                key = (
                    evidence.url
                    or evidence.title
                )

                if key in seen:
                    continue

                seen.add(key)

                sources.append(
                    AnswerSource(
                        title=evidence.title,
                        url=evidence.url,
                        source_type=evidence.source_type,
                    )
                )

        return sources[:20]
