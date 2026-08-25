"""
BillLens Researcher

Executes a ResearchPlan and collects evidence from
parliamentary and legislative data sources.
"""

from __future__ import annotations

from typing import Any, Dict, List

import httpx

from .planner import ResearchPlan, ResearchStep, ResearchType


class Evidence(BaseModel):
    title: str
    source_type: str
    url: str | None = None
    content: str
    date: str | None = None
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = {}


class ResearchResult(BaseModel):
    question: str
    topic: str
    evidence: List[Evidence] = []
    completed_steps: List[str] = []
    failed_steps: List[str] = []


class BillLensResearcher:
    """
    Research engine for BillLens.

    Each source is accessed through a small adapter method so the
    implementation can later be replaced with MCP tools, Qdrant,
    Parliament APIs, or other services.
    """

    def __init__(
        self,
        lex_base_url: str | None = None,
        parliament_base_url: str | None = None,
        timeout: float = 30.0,
    ):
        self.lex_base_url = lex_base_url
        self.parliament_base_url = parliament_base_url
        self.timeout = timeout

    async def research(
        self,
        plan: ResearchPlan,
    ) -> ResearchResult:

        all_evidence: list[Evidence] = []
        completed: list[str] = []
        failed: list[str] = []

        async with httpx.AsyncClient(timeout=self.timeout) as client:

            for step in plan.steps:
                try:
                    evidence = await self._execute_step(
                        client,
                        step,
                    )

                    all_evidence.extend(evidence)
                    completed.append(step.type.value)

                except Exception as exc:
                    failed.append(
                        f"{step.type.value}: {exc}"
                    )

        # Remove duplicate sources.
        all_evidence = self._deduplicate(all_evidence)

        # Highest relevance first.
        all_evidence.sort(
            key=lambda item: item.relevance_score,
            reverse=True,
        )

        return ResearchResult(
            question=plan.original_question,
            topic=plan.topic,
            evidence=all_evidence,
            completed_steps=completed,
            failed_steps=failed,
        )

    async def _execute_step(
        self,
        client: httpx.AsyncClient,
        step: ResearchStep,
    ) -> list[Evidence]:

        if step.type == ResearchType.LEGISLATION:
            return await self._search_legislation(
                client,
                step.question,
            )

        if step.type == ResearchType.BILLS:
            return await self._search_parliament(
                client,
                step.question,
                "bills",
            )

        if step.type == ResearchType.DEBATES:
            return await self._search_parliament(
                client,
                step.question,
                "debates",
            )

        if step.type == ResearchType.VOTES:
            return await self._search_parliament(
                client,
                step.question,
                "votes",
            )

        if step.type == ResearchType.MPS:
            return await self._search_parliament(
                client,
                step.question,
                "mps",
            )

        if step.type == ResearchType.AMENDMENTS:
            return await self._search_legislation(
                client,
                step.question,
            )

        if step.type == ResearchType.TIMELINE:
            return await self._search_parliament(
                client,
                step.question,
                "timeline",
            )

        return []

    async def _search_legislation(
        self,
        client: httpx.AsyncClient,
        query: str,
    ) -> list[Evidence]:

        if not self.lex_base_url:
            return []

        endpoint = (
            f"{self.lex_base_url.rstrip('/')}"
            "/legislation/section/search"
        )

        response = await client.post(
            endpoint,
            json={
                "query": query,
                "limit": 10,
            },
        )

        response.raise_for_status()

        data = response.json()

        return self._parse_lex_results(data)

    async def _search_parliament(
        self,
        client: httpx.AsyncClient,
        query: str,
        category: str,
    ) -> list[Evidence]:

        if not self.parliament_base_url:
            return []

        endpoint = (
            f"{self.parliament_base_url.rstrip('/')}"
            f"/search"
        )

        response = await client.get(
            endpoint,
            params={
                "q": query,
                "type": category,
                "limit": 10,
            },
        )

        response.raise_for_status()

        data = response.json()

        return self._parse_parliament_results(
            data,
            category,
        )

    @staticmethod
    def _parse_lex_results(
        data: Dict[str, Any],
    ) -> list[Evidence]:

        results = data.get("results", [])

        evidence = []

        for item in results:
            evidence.append(
                Evidence(
                    title=item.get(
                        "title",
                        "UK legislation",
                    ),
                    source_type="legislation",
                    url=item.get("url"),
                    content=item.get(
                        "text",
                        item.get("description", ""),
                    ),
                    date=item.get("date"),
                    relevance_score=float(
                        item.get("score", 0)
                    ),
                    metadata=item,
                )
            )

        return evidence

    @staticmethod
    def _parse_parliament_results(
        data: Dict[str, Any],
        category: str,
    ) -> list[Evidence]:

        results = data.get("results", [])

        evidence = []

        for item in results:
            evidence.append(
                Evidence(
                    title=item.get(
                        "title",
                        f"Parliament {category}",
                    ),
                    source_type=f"parliament_{category}",
                    url=item.get("url"),
                    content=item.get(
                        "text",
                        item.get("description", ""),
                    ),
                    date=item.get("date"),
                    relevance_score=float(
                        item.get("score", 0)
                    ),
                    metadata=item,
                )
            )

        return evidence

    @staticmethod
    def _deduplicate(
        evidence: list[Evidence],
    ) -> list[Evidence]:

        seen = set()
        unique = []

        for item in evidence:

            key = (
                item.url
                or item.title,
                item.source_type,
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(item)

        return unique
