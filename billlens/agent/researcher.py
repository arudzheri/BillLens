import json
from pathlib import Path
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

from billlens.data.lex import LexClient
from billlens.data.parliament import BillsAPIClient, ParliamentAPIClient
from billlens.models.evidence import Evidence


class ResearchResult(BaseModel):
    topic: str
    evidence: list[Evidence] = Field(default_factory=list)


class BillLensResearcher:

    def __init__(
        self,
        lex_base_url: str | None = None,
        parliament_base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.lex_client = LexClient(base_url=lex_base_url, timeout=timeout)
        self.members_client = ParliamentAPIClient()
        self.bills_client = BillsAPIClient()

    def load_local_fallback(self, query: str) -> List[Evidence]:
        """Load local backup dataset if live calls yield zero records."""
        fallback_path = (
            Path(__file__).parent.parent / "data" / "fallback_data.json"
        )

        if not fallback_path.exists():
            return []

        with open(fallback_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        evidence: List[Evidence] = []
        for item in data:
            if isinstance(item, Evidence):
                evidence.append(item)
            elif isinstance(item, dict):
                evidence.append(
                    Evidence(
                        title=item.get("title", "Fallback evidence"),
                        content=item.get("text") or item.get("content") or "",
                        source_type=item.get("source_type", "legislation"),
                        url=item.get("url"),
                        date=item.get("date"),
                        relevance_score=float(item.get("score", 0.0)),
                        metadata=item,
                    )
                )
        return evidence

    async def gather_evidence(self, query: str) -> List[Evidence]:
        evidence: List[Evidence] = []

        try:
            legislation = await self.lex_client.search(query, limit=5)
            evidence.extend(legislation)
        except Exception as err:
            print(f"Lex API Error: {err}")

        try:
            bills = await self.bills_client.search_bills(search_term=query)
            for bill in bills:
                evidence.append(
                    Evidence(
                        title=bill.get("title", "Parliamentary bill"),
                        content=(
                            f"{('Enacted Law (Act)' if bill.get('is_act') else 'Proposed Bill')}: "
                            f"'{bill.get('title', 'Bill')}' is currently at stage "
                            f"'{bill.get('stage', 'Unknown stage')}' in the {bill.get('house', 'Unknown house')}."
                        ),
                        source_type="bill",
                        url=f"https://bills.parliament.uk/bills/{bill.get('id')}",
                        date=bill.get("last_updated"),
                        relevance_score=0.7,
                        metadata=bill,
                    )
                )
        except Exception as err:
            print(f"Bills API Error: {err}")

        try:
            members = await self.members_client.search_members(name=query)
            for member in members:
                evidence.append(
                    Evidence(
                        title=member.get("name") or "Member of Parliament",
                        content=(
                            f"{member.get('full_title', '')} represents "
                            f"{member.get('constituency_or_house', '')} ({member.get('party', 'Unknown party')})."
                        ).strip(),
                        source_type="parliament",
                        url=f"https://members-api.parliament.uk/api/Members/{member.get('id')}",
                        date=None,
                        relevance_score=0.6,
                        metadata=member,
                    )
                )
        except Exception as err:
            print(f"Members API Error: {err}")

        deduped: List[Evidence] = []
        seen = set()
        for item in evidence:
            key = item.url or item.title
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)

        if not deduped:
            deduped = self.load_local_fallback(query)

        return deduped

    async def research(self, plan: Union[str, Any]) -> ResearchResult:
        if hasattr(plan, "original_question") and hasattr(plan, "topic"):
            topic = plan.topic
            query = plan.original_question
        elif isinstance(plan, str):
            topic = self._topic_from_query(plan)
            query = plan
        else:
            topic = getattr(plan, "topic", str(plan))
            query = getattr(plan, "original_question", str(plan))

        evidence = await self.gather_evidence(query)
        return ResearchResult(topic=topic, evidence=evidence)

    @staticmethod
    def _topic_from_query(query: str) -> str:
        normalized = query.strip().lower()
        for prefix in (
            "what has parliament actually done about ",
            "what has parliament done about ",
            "what has parliament done on ",
            "what has parliament discussed about ",
            "what has parliament discussed on ",
            "tell me about ",
            "what happened with ",
        ):
            if normalized.startswith(prefix):
                return normalized[len(prefix):].strip(" ?.")
        return normalized.strip(" ?.")

    async def run(self, query: str) -> List[Evidence]:
        return await self.gather_evidence(query)

    async def search(self, query: str) -> List[Evidence]:
        return await self.gather_evidence(query)


# Backward compatibility alias
Researcher = BillLensResearcher