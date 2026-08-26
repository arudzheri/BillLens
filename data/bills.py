from __future__ import annotations

from billlens.data.parliament import (
    ParliamentClient,
)

from billlens.models import Bill


class BillsClient:

    def __init__(
        self,
        parliament_client: ParliamentClient,
    ):
        self.parliament = parliament_client

    async def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[Bill]:

        results = await self.parliament.search(
            query=query,
            category="bills",
            limit=limit,
        )

        bills = []

        for item in results:

            bills.append(
                Bill(
                    id=item.id or "",
                    title=item.title,
                    description=item.content,
                    status=item.metadata.get(
                        "status"
                    ),
                    source_url=item.url,
                )
            )

        return bills
