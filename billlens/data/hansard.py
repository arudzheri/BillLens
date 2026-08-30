from __future__ import annotations

from billlens.data.parliament import (
    ParliamentClient,
)

from billlens.models import Evidence


class HansardClient:
    """
    Hansard-specific interface.

    Uses the Parliament client underneath,
    allowing the rest of BillLens to treat Hansard
    as a specialised source.
    """

    def __init__(
        self,
        parliament_client: ParliamentClient,
    ):
        self.parliament = parliament_client

    async def search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Evidence]:
        """
        Search Hansard/debate records via the underlying Parliament client.
        """
        try:
            raw_results = await self.parliament.search(query=query)
        except Exception as err:
            print(f"Hansard search error: {err}")
            return []

        evidence: list[Evidence] = []
        for item in raw_results[:limit]:
            title = item.get("title") or "Parliamentary debate"
            content = item.get("description") or title
            evidence.append(
                Evidence(
                    title=title,
                    content=content,
                    source_type="debate",
                    url=item.get("url"),
                    relevance_score=0.6,
                    metadata=item,
                )
            )
        return evidence