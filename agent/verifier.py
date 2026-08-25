"""
BillLens Evidence Verifier

Checks whether generated claims are adequately supported
by retrieved parliamentary and legislative evidence.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .researcher import Evidence


class Claim(BaseModel):
    text: str
    importance: str = "normal"


class VerifiedClaim(BaseModel):
    claim: str
    supported: bool
    confidence: float
    supporting_evidence: List[Evidence] = Field(
        default_factory=list
    )
    explanation: str = ""


class VerificationResult(BaseModel):
    verified_claims: List[VerifiedClaim] = Field(
        default_factory=list
    )
    overall_confidence: float = 0.0
    warnings: List[str] = Field(
        default_factory=list
    )


class BillLensVerifier:

    MINIMUM_SCORE = 0.35

    def verify(
        self,
        claims: List[Claim],
        evidence: List[Evidence],
    ) -> VerificationResult:

        verified = []
        warnings = []

        for claim in claims:

            matches = self._find_supporting_evidence(
                claim,
                evidence,
            )

            if not matches:
                verified.append(
                    VerifiedClaim(
                        claim=claim.text,
                        supported=False,
                        confidence=0.0,
                        explanation=(
                            "No sufficiently relevant "
                            "evidence was found."
                        ),
                    )
                )

                warnings.append(
                    f"Unsupported claim: {claim.text}"
                )

                continue

            confidence = self._calculate_confidence(
                matches
            )

            supported = (
                confidence >= self.MINIMUM_SCORE
            )

            verified.append(
                VerifiedClaim(
                    claim=claim.text,
                    supported=supported,
                    confidence=confidence,
                    supporting_evidence=matches[:3],
                    explanation=self._explain(
                        confidence,
                        matches,
                    ),
                )
            )

            if not supported:
                warnings.append(
                    f"Weak evidence for claim: "
                    f"{claim.text}"
                )

        overall = (
            sum(
                claim.confidence
                for claim in verified
            )
            / len(verified)
            if verified
            else 0.0
        )

        return VerificationResult(
            verified_claims=verified,
            overall_confidence=overall,
            warnings=warnings,
        )

    def _find_supporting_evidence(
        self,
        claim: Claim,
        evidence: List[Evidence],
    ) -> List[Evidence]:

        claim_words = self._keywords(claim.text)

        scored = []

        for item in evidence:

            evidence_words = self._keywords(
                item.content + " " + item.title
            )

            overlap = (
                len(claim_words & evidence_words)
                / max(len(claim_words), 1)
            )

            semantic_score = item.relevance_score

            # Normalise search scores to [0, 1].
            semantic_score = min(
                max(semantic_score, 0.0),
                1.0,
            )

            combined = (
                overlap * 0.6
                + semantic_score * 0.4
            )

            if combined >= self.MINIMUM_SCORE:
                scored.append(
                    (
                        combined,
                        item,
                    )
                )

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [
            item
            for _, item in scored
        ]

    @staticmethod
    def _keywords(text: str) -> set[str]:

        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "to",
            "of",
            "in",
            "on",
            "for",
            "has",
            "have",
            "what",
            "did",
            "was",
            "were",
            "about",
        }

        return {
            word.strip(".,!?():;\"'")
            for word in text.lower().split()
            if len(word) > 2
            and word not in stop_words
        }

    @staticmethod
    def _calculate_confidence(
        evidence: List[Evidence],
    ) -> float:

        if not evidence:
            return 0.0

        top = evidence[:3]

        scores = [
            min(max(item.relevance_score, 0), 1)
            for item in top
        ]

        # Multiple independent sources increase confidence.
        source_bonus = min(
            len(
                {
                    item.source_type
                    for item in top
                }
            )
            * 0.05,
            0.15,
        )

        return min(
            sum(scores) / len(scores)
            + source_bonus,
            1.0,
        )

    @staticmethod
    def _explain(
        confidence: float,
        evidence: List[Evidence],
    ) -> str:

        if confidence >= 0.8:
            return (
                "Strong support from highly relevant "
                "parliamentary or legislative evidence."
            )

        if confidence >= 0.6:
            return (
                "The claim is reasonably supported by "
                "relevant evidence."
            )

        return (
            "The available evidence provides only "
            "limited support for this claim."
        )
