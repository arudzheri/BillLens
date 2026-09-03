from __future__ import annotations

from apps.web.mps.schemas import (
    MPSearchRequest,
    MPSearchResponse,
    MPSummary,
)


class MPsService:
    """
    Business logic for MPs.
    """

    def __init__(
        self,
        MPs_client,
    ):
        self.client = MPs_client

    async def search(
        self,
        request: MPSearchRequest,
    ) -> MPSearchResponse:

        results = await self.client.search(
            query=request.query,
            limit=request.limit,
        )

        MPs = []

        for mp in results:

            MPs.append(
                MPSummary(
                    id=mp.id,
                    name=mp.name,
                    party=mp.party,
                    constituency=(
                        mp.constituency
                    ),
                    house=mp.house,
                    image_url=mp.image_url,
                    profile_url=mp.profile_url,
                )
            )

        return MPSearchResponse(
            query=request.query,
            results=MPs,
        )
