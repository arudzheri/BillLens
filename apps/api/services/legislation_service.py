from __future__ import annotations

from typing import Any

from billlens.legislation.schemas import (
    LegislationDetailResponse,
    LegislationSearchRequest,
    LegislationSearchResponse,
    LegislationSummary,
)


class LegislationService:
    """
    Application service for UK legislation.
    """

    def __init__(
        self,
        legislation_client: Any,
        search_client: Any = None,
    ):
        self.client = legislation_client
        self.search_client = search_client

    async def search(
        self,
        request: LegislationSearchRequest,
    ) -> LegislationSearchResponse:

        if self.search_client is None:

            return LegislationSearchResponse(
                query=request.query,
                results=[],
            )

        results = await self.search_client.search(
            query=request.query,
            limit=request.limit,
        )

        legislation = []

        for item in results:

            legislation.append(
                LegislationSummary(
                    id=item.id,
                    title=item.title,
                    year=getattr(
                        item,
                        "year",
                        None,
                    ),
                    legislation_type=getattr(
                        item,
                        "legislation_type",
                        None,
                    ),
                    status=getattr(
                        item,
                        "status",
                        None,
                    ),
                    description=getattr(
                        item,
                        "description",
                        None,
                    ),
                    source_url=getattr(
                        item,
                        "source_url",
                        None,
                    ),
                )
            )

        return LegislationSearchResponse(
            query=request.query,
            results=legislation,
        )

    async def get(
        self,
        legislation_id: str,
    ) -> LegislationDetailResponse:

        item = await self.client.get(
            legislation_id
        )

        if item is None:

            raise ValueError(
                f"Legislation not found: "
                f"{legislation_id}"
            )

        return LegislationDetailResponse(
            id=item.id,
            title=item.title,
            year=getattr(
                item,
                "year",
                None,
            ),
            legislation_type=getattr(
                item,
                "legislation_type",
                None,
            ),
            status=getattr(
                item,
                "status",
                None,
            ),
            description=getattr(
                item,
                "description",
                None,
            ),
            source_url=getattr(
                item,
                "source_url",
                None,
            ),
            sections=[
                section.model_dump()
                if hasattr(section, "model_dump")
                else section
                for section in getattr(
                    item,
                    "sections",
                    [],
                )
            ],
        )
