from __future__ import annotations

from billlens.data.parliament import (
    BillsAPIClient,
    ParliamentAPIClient,
)
from billlens.models import Bill


class BillsClient:

    def __init__(
        self,
        parliament_client: ParliamentAPIClient | None = None,
    ):
        self.parliament = parliament_client or ParliamentAPIClient()
        self.bills_api = BillsAPIClient()

    async def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[Bill]:
        # Query live Bills API
        raw_bills = await self.bills_api.search_bills(search_term=query)

        bills = []
        for item in raw_bills[:limit]:
            bills.append(
                Bill(
                    id=str(item.get("id") or ""),
                    title=item.get("title") or "",
                    description=(
                        f"Stage: {item.get('stage')} in {item.get('house')}."
                    ),
                    status=item.get("stage"),
                    source_url=(
                        f"https://bills.parliament.uk/bills/{item.get('id')}"
                    ),
                )
            )

        return bills