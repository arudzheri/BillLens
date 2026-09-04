"""
BillLens Answer Generator

Produces a structured, evidence-backed answer from
verified parliamentary research.
"""

from __future__ import annotations

from typing import List

from billlens.models.answer import (
    AnswerClaim,
    AnswerResponse,
    AnswerSource,
)
from billlens.models.evidence import Evidence
from .verifier import VerificationResult


class BillLensAnswerGenerator:
    """
    Converts verified claims into a structured answer response.
    """

    def generate(
        self,
        question: str,
        verification: VerificationResult,
        evidence: List[Evidence],
    ) -> AnswerResponse:
        """
        Generate a final answer from verification results.
        """

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

        # Categorize supported claims
        for claim in supported:
            text = claim.claim

            source_types = {
                source.source_type
                for source in claim.supporting_evidence
            }

            if any("legislation" in source for source in source_types):
                legislation.append(text)
            elif any("vote" in source for source in source_types):
                votes.append(text)
            elif any(
                "debate" in source
                or "parliament" in source
                or "hansard" in source
                for source in source_types
            ):
                parliamentary_activity.append(text)
            else:
                what_happened.append(text)

        # Build dynamic summary
        summary = self._build_summary(
            supported,
            question,
            evidence,
        )

        # Build sources
        answer_sources = self._build_sources(supported)

        # Build warnings
        warnings = list(verification.warnings)

        if unsupported:
            warnings.append(
                "Some claims could not be verified against the available evidence."
            )

        if hasattr(verification, "planned_steps"):
            research_completed = all(
                step in verification.completed_steps
                for step in verification.planned_steps
            )
        else:
            research_completed = True

        if not research_completed:
            warnings.append("Research did not complete all planned steps.")

        what_did_not_happen = [
            f"Not verified: {claim.claim}" for claim in unsupported
        ]

        answer_claims = [
            AnswerClaim(
                text=claim.claim,
                supported=claim.supported,
                confidence=claim.confidence,
                sources=[
                    AnswerSource(
                        title=source.title,
                        source_type=source.source_type,
                        url=source.url,
                        date=source.date,
                    )
                    for source in claim.supporting_evidence
                ],
            )
            for claim in verification.verified_claims
        ]

        return AnswerResponse(
            question=question,
            summary=summary,
            what_happened=what_happened,
            legislation=legislation,
            parliamentary_activity=parliamentary_activity,
            votes=votes,
            what_did_not_happen=what_did_not_happen,
            claims=answer_claims,
            sources=answer_sources,
            confidence=verification.overall_confidence if supported else 0.8,
            warnings=warnings,
        )

    @staticmethod
    def _build_summary(
        claims,
        question: str,
        evidence: List[Evidence],
    ) -> str:
        """Build a dynamic summary from claims or raw gathered evidence."""

        if claims:
            first_claims = [claim.claim for claim in claims[:3]]
            return (
                "Based on the parliamentary and legislative evidence retrieved: "
                + " ".join(first_claims)
            )

        if evidence:
            top_evidence = [e.content for e in evidence[:2] if e.content]
            if top_evidence:
                return f"Retrieved parliamentary records indicate: {' '.join(top_evidence)}"

        return (
            f"BillLens searched parliamentary databases for '{question}' but did not find "
            "sufficient matching legislative records."
        )

    @staticmethod
    def _build_sources(claims) -> List[AnswerSource]:
        """Build unique sources from claims."""

        sources = []
        seen = set()

        for claim in claims:
            for evidence in claim.supporting_evidence:
                key = evidence.url or evidence.title

                if key in seen:
                    continue

                seen.add(key)

                sources.append(
                    AnswerSource(
                        title=evidence.title,
                        source_type=evidence.source_type,
                        url=evidence.url,
                        date=evidence.date,
                    )
                )

        return sources[:20]
