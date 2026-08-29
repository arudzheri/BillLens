from __future__ import annotations

from billlens.data.parliament import (
    ParliamentClient,
)

from billlens.models import MP


class MPsClient:

    def __init__(
        self,
        parliament_client: ParliamentClient,
    ):
        self.parliament = parliament_client

    async def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[MP]:

        results = await self.parliament.search(
            query=query,
            category="mps",
            limit=limit,
        )

        mps = []

        for item in results:

            metadata = item.metadata

            mps.append(
                MP(
                    id=item.id or "",
                    name=metadata.get(
                        "name",
                        item.title,
                    ),
                    party=metadata.get(
                        "party"
                    ),
                    constituency=metadata.get(
                        "constituency"
                    ),
                    profile_url=item.url,
                )
            )

        return mps
