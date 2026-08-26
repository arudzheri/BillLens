from __future__ import annotations

import httpx

from billlens.models import Evidence


class ParliamentClient:
    """
    Client for parliamentary data.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

    async def search(
        self,
        query: str,
        category: str | None = None,
        limit: int = 10,
    ) -> list[Evidence]:

        params = {
            "q": query,
            "limit": limit,
        }

        if category:
            params["type"] = category

        endpoint = (
            f"{self.base_url}/search"
        )

        async with httpx.AsyncClient(
            timeout=self.timeout
        ) as client:

            response = await client.get(
                endpoint,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

        return self._parse_results(
            data,
            category,
        )

    @staticmethod
    def _parse_results(
        data: dict,
        category: str | None,
    ) -> list[Evidence]:

        results = data.get(
            "results",
            [],
        )

        evidence = []

        for index, item in enumerate(results):

            source_type = (
                f"parliament_{category}"
                if category
                else "parliament"
            )

            evidence.append(
                Evidence(
                    id=str(
                        item.get(
                            "id",
                            index,
                        )
                    ),
                    title=item.get(
                        "title",
                        "Parliamentary document",
                    ),
                    content=item.get(
                        "text",
                        item.get(
                            "description",
                            "",
                        ),
                    ),
                    source_type=source_type,
                    url=item.get("url"),
                    date=item.get("date"),
                    relevance_score=float(
                        item.get(
                            "score",
                            0.0,
                        )
                    ),
                    metadata=item,
                )
            )

        return evidence
