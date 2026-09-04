"""
BillLens Researcher Agent
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from billlens.data.parliament import BillsAPIClient, ParliamentAPIClient
from billlens.data.hansard import HansardClient
from billlens.data.keywords import extract_keywords
from billlens.models.evidence import Evidence


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

        # Try to search with extracted keywords
        if search_keyword:
            # Search Parliamentary Bills API
            try:
                bills = await self.bills_client.search_bills(search_term=search_keyword)
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
                print(f"Bills API Error: {err}")

            # Search Hansard for debates on the topic
            try:
                debate_evidence = await self.hansard_client.search(
                    query=search_keyword, limit=10
                )
                evidence.extend(debate_evidence)
            except Exception as err:
                print(f"Hansard API Error: {err}")

        # Deduplicate
        deduped: List[Evidence] = []
        seen = set()
        for item in evidence:
            key = item.url or item.title
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)

        # If no evidence found, try fallback dataset
        if not deduped:
            deduped = self.load_local_fallback(search_keyword or query)

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
            return []

        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            evidence_items = []
            raw_items = data.get("evidence", [])

            # If a topic was provided, try to filter the fallback dataset by topic
            if topic:
                topic_l = topic.strip().lower()
                for item in raw_items:
                    title = (item.get("title") or "").lower()
                    content = (item.get("content") or "").lower()
                    # match if the topic appears in the title or content
                    if topic_l in title or topic_l in content:
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

                # If we found no matching fallback items, return empty list so callers
                # don't get unrelated (e.g. housing-only) results.
                return evidence_items

            # No topic provided: return all fallback items
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
            print(f"Error loading local fallback: {err}")
            return []

    @staticmethod
    def _topic_from_query(text: str) -> str:
        return extract_keywords(text)
