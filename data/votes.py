from __future__ import annotations

from billlens.data.parliament import (
    ParliamentClient,
)

from billlens.models import Vote


class VotesClient:

    def __init__(
        self,
        parliament_client: ParliamentClient,
    ):
        self.parliament = parliament_client

    async def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[Vote]:

        results = await self.parliament.search(
            query=query,
            category="votes",
            limit=limit,
        )

        votes = []

        for item in results:

            votes.append(
                Vote(
                    id=item.id or "",
                    title=item.title,
                    date=item.date,
                    source_url=item.url,
                    result=item.metadata.get(
                        "result"
                    ),
                    ayes=item.metadata.get(
                        "ayes"
                    ),
                    noes=item.metadata.get(
                        "noes"
                    ),
                )
            )

        return votes
