"""
BillLens Claim Extraction

Converts research evidence into factual claims.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from billlens.models.evidence import Evidence


class Claim(BaseModel):
    """A factual claim extracted from evidence."""
    
    text: str
    importance: str = "normal"
    supporting_evidence: list[Evidence] = Field(default_factory=list)


class ClaimExtractor:
    """
    Extracts claims from research evidence.
    
    This first version uses deterministic extraction.
    Later, an LLM can be added for more sophisticated reasoning.
    """
    
    def extract(
        self,
        question: str,
        evidence: list[Evidence],
    ) -> list[Claim]:
        """
        Extract claims from evidence.
        
        Returns a list of claims with supporting evidence.
        """
        
        if not evidence:
            return []
        
        claims = []
        
        # Group evidence by source type
        by_source_type = {}
        for item in evidence:
            if item.source_type not in by_source_type:
                by_source_type[item.source_type] = []
            by_source_type[item.source_type].append(item)
        
        # Extract one claim per source type
        for source_type, items in by_source_type.items():
            if not items:
                continue
            
            top_item = items[0]
            
            # Generate a simple claim from the top evidence
            claim_text = self._generate_claim_text(
                source_type,
                top_item,
            )
            
            if claim_text:
                claims.append(
                    Claim(
                        text=claim_text,
                        importance="normal",
                        supporting_evidence=items[:3],
                    )
                )
        
        return claims
    
    @staticmethod
    def _generate_claim_text(
        source_type: str,
        evidence: Evidence,
    ) -> str:
        """Generate a claim text from evidence."""
        
        if not evidence.content:
            return f"There is {source_type} information: {evidence.title}"
        
        # Simple claim: first sentence of content
        content = evidence.content.strip()
        sentences = content.split(".")
        
        if sentences:
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 10:
                return first_sentence
        
        return f"According to {source_type}: {evidence.title}"