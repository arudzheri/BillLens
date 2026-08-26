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

        return await self.parliament.search(
            query=query,
            category="debates",
            limit=limit,
        )
