"""
Citation management and deduplication.
"""

from __future__ import annotations

from billlens.models.evidence import Evidence


class CitationManager:
    """
    Manages citations and removes duplicates.
    """
    
    @staticmethod
    def deduplicate(
        evidence: list[Evidence],
    ) -> list[Evidence]:
        """
        Remove duplicate evidence.
        
        Uses URL or title as the dedup key.
        """
        
        seen = set()
        unique = []
        
        for item in evidence:
            key = (item.url or item.title, item.source_type)
            
            if key in seen:
                continue
            
            seen.add(key)
            unique.append(item)
        
        return unique
    
    @staticmethod
    def create_citations(
        evidence: list[Evidence],
    ) -> dict[str, dict]:
        """
        Create numbered citations from evidence.
        
        Returns dict mapping number to citation metadata.
        """
        
        citations = {}
        
        for idx, item in enumerate(evidence, start=1):
            citations[str(idx)] = {
                "title": item.title,
                "url": item.url,
                "source_type": item.source_type,
                "date": item.date,
            }
        
        return citations