"""
BillLens Researcher Agent
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from billlens.data.parliament import BillsAPIClient, ParliamentAPIClient
from billlens.data.hansard import HansardClient
from billlens.data.keywords import extract_keywords
from billlens.models.evidence import Evidence

logger = logging.getLogger(__name__)


@dataclass
class ResearchResult:
    query: str
    evidence: List[Evidence]


class BillLensResearcher:
    """
    Gathers evidence from UK Parliament APIs and local fallback datasets.
    """

    def __init__(
        self,
        lex_base_url: Optional[str] = None,
        parliament_base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.bills_client = BillsAPIClient(base_url=parliament_base_url)
        self.members_client = ParliamentAPIClient(base_url=parliament_base_url)
        self.hansard_client = HansardClient(self.members_client)

    async def research(self, plan: Any) -> ResearchResult:
        """
        Execute research steps based on a plan.
        """
        query = getattr(plan, "original_question", str(plan))
        evidence = await self.gather_evidence(query)
        return ResearchResult(query=query, evidence=evidence)

    async def gather_evidence(self, query: str) -> List[Evidence]:
        """
        Gather evidence dynamically from live APIs.
        """
        evidence: List[Evidence] = []
        search_keyword = self._topic_from_query(query)
        
        logger.info(f"[GATHER_EVIDENCE] Query: '{query}'")
        logger.info(f"[GATHER_EVIDENCE] Extracted keyword: '{search_keyword}'")

        # Try to search with extracted keywords
        if search_keyword:
            # Search Parliamentary Bills API
            try:
                bills = await self.bills_client.search_bills(search_term=search_keyword)
                logger.info(f"[BILLS_API] Found {len(bills)} bills")
                for bill in bills:
                    evidence.append(
                        Evidence(
                            title=bill.get("title", "Parliamentary bill"),
                            content=(
                                f"{'Enacted Law (Act)' if bill.get('is_act') else 'Proposed Bill'}: "
                                f"'{bill.get('title', 'Bill')}' is currently at stage "
                                f"'{bill.get('stage', 'Unknown stage')}' in the {bill.get('house', 'Unknown house')}."
                            ),
                            source_type="bill",
                            url=f"https://bills.parliament.uk/bills/{bill.get('id')}",
                            date=bill.get("last_updated"),
                            relevance_score=0.8,
                            metadata=bill,
                        )
                    )
            except Exception as err:
                logger.error(f"[BILLS_API_ERROR] {err}")

            # Search Hansard for debates on the topic
            try:
                debate_evidence = await self.hansard_client.search(
                    query=search_keyword, limit=10
                )
                logger.info(f"[HANSARD] Found {len(debate_evidence)} debates")
                evidence.extend(debate_evidence)
            except Exception as err:
                logger.error(f"[HANSARD_ERROR] {err}")

        # Deduplicate
        deduped: List[Evidence] = []
        seen = set()
        for item in evidence:
            key = item.url or item.title
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)

        logger.info(f"[GATHER_EVIDENCE] After API calls: {len(deduped)} evidence items")

        # If no evidence found, try fallback dataset with topic filtering
        if not deduped:
            logger.info(f"[FALLBACK] No API evidence found, loading fallback data with topic: '{search_keyword or query}'")
            deduped = self.load_local_fallback(search_keyword or query)
            logger.info(f"[FALLBACK] Fallback returned {len(deduped)} items")

        return deduped

    def load_local_fallback(self, topic: str = "") -> List[Evidence]:
        """
        Load fallback evidence from local JSON.

        Improved behaviour:
        - If a topic is provided, only return fallback items that clearly match the
          topic (title or content contains the topic). This avoids returning
          unrelated (e.g. housing-only) fallback data for unrelated queries.
        - If no topic is provided, return the full fallback dataset.
        """
        fallback_path = Path("billlens/data/fallback_data.json")
        if not fallback_path.exists():
            logger.error(f"[FALLBACK] Path does not exist: {fallback_path}")
            return []

        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            evidence_items = []
            raw_items = data.get("evidence", [])
            logger.info(f"[FALLBACK] Loaded {len(raw_items)} total items from fallback_data.json")

            # If a topic was provided, try to filter the fallback dataset by topic
            if topic and topic.strip():
                topic_l = topic.strip().lower()
                topic_words = [w for w in topic_l.split() if len(w) > 2]
                
                logger.info(f"[FALLBACK] Topic words to match: {topic_words}")
                
                for idx, item in enumerate(raw_items):
                    title = (item.get("title") or "").lower()
                    content = (item.get("content") or "").lower()
                    
                    # Match if ANY topic word appears in title or content
                    matched = any(
                        word in title or word in content 
                        for word in topic_words
                    )
                    
                    logger.info(f"[FALLBACK] Item {idx} ({item.get('title')}): matched={matched}")
                    
                    if matched:
                        evidence_items.append(
                            Evidence(
                                title=item.get("title", "Fallback Record"),
                                content=item.get("content", ""),
                                source_type=item.get("source_type", "legislation"),
                                url=item.get("url", ""),
                                date=item.get("date", ""),
                                relevance_score=item.get("relevance_score", 0.7),
                            )
                        )

                logger.info(f"[FALLBACK] Filtered to {len(evidence_items)} matching items")
                return evidence_items

            # No topic provided: return all fallback items
            logger.info(f"[FALLBACK] No topic provided, returning all {len(raw_items)} items")
            for item in raw_items:
                evidence_items.append(
                    Evidence(
                        title=item.get("title", "Fallback Record"),
                        content=item.get("content", ""),
                        source_type=item.get("source_type", "legislation"),
                        url=item.get("url", ""),
                        date=item.get("date", ""),
                        relevance_score=item.get("relevance_score", 0.7),
                    )
                )

            return evidence_items
        except Exception as err:
            logger.error(f"[FALLBACK_ERROR] {err}")
            return []

    @staticmethod
    def _topic_from_query(text: str) -> str:
        return extract_keywords(text)
