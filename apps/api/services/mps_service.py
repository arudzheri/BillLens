from __future__ import annotations

from typing import Any

from billlens.mps.schemas import (
    MPSearchRequest,
    MPSearchResponse,
    MPSummary,
)


class MPsService:
    """
    Application service for Members of Parliament.
    """

    def __init__(self, mps_client: Any):
        self.client = mps_client

    async def search(
        self,
        request: MPSearchRequest,
    ) -> MPSearchResponse:

        results = await self.client.search(
            query=request.query,
            limit=request.limit,
        )

        mps = []

        for mp in results:

            mps.append(
                MPSummary(
                    id=mp.id,
                    name=mp.name,
                    party=getattr(
                        mp,
                        "party",
                        None,
                    ),
                    constituency=getattr(
                        mp,
                        "constituency",
                        None,
                    ),
                    house=getattr(
                        mp,
                        "house",
                        "Commons",
                    ),
                    image_url=getattr(
                        mp,
                        "image_url",
                        None,
                    ),
                    profile_url=getattr(
                        mp,
                        "profile_url",
                        None,
                    ),
                )
            )

        return MPSearchResponse(
            query=request.query,
            results=mps,
        )

    async def get(
        self,
        mp_id: str,
    ):

        mp = await self.client.get(mp_id)

        if mp is None:
            raise ValueError(
                f"MP not found: {mp_id}"
            )

        return MPSummary(
            id=mp.id,
            name=mp.name,
            party=getattr(
                mp,
                "party",
                None,
            ),
            constituency=getattr(
                mp,
                "constituency",
                None,
            ),
            house=getattr(
                mp,
                "house",
                "Commons",
            ),
            image_url=getattr(
                mp,
                "image_url",
                None,
            ),
            profile_url=getattr(
                mp,
                "profile_url",
                None,
            ),
        )
