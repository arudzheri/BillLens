from __future__ import annotations

import httpx

from billlens.models import Evidence


class LexClient:
    """
    Client for the Lex API.

    Lex is used by BillLens as a legislation
    retrieval source.
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
        limit: int = 10,
    ) -> list[Evidence]:

        endpoint = (
            f"{self.base_url}"
            "/legislation/section/search"
        )

        async with httpx.AsyncClient(
            timeout=self.timeout
        ) as client:

            response = await client.post(
                endpoint,
                json={
                    "query": query,
                    "limit": limit,
                },
            )

            response.raise_for_status()

            data = response.json()

        return self._parse_results(data)

    @staticmethod
    def _parse_results(
        data: dict,
    ) -> list[Evidence]:

        results = data.get(
            "results",
            [],
        )

        evidence = []

        for index, item in enumerate(results):

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
                        "UK legislation",
                    ),
                    content=item.get(
                        "text",
                        item.get(
                            "description",
                            "",
                        ),
                    ),
                    source_type="lex",
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
