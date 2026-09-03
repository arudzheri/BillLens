from __future__ import annotations

from apps.web.legislation.schemas import (
    LegislationDetailResponse,
    LegislationSearchRequest,
    LegislationSearchResponse,
    LegislationSummary,
)


class LegislationService:
    """
    Business logic for UK legislation.
    """

    def __init__(
        self,
        legislation_client,
        search_client=None,
    ):
        self.client = legislation_client

        self.search_client = search_client

    async def get(
        self,
        legislation_id: str,
    ) -> LegislationDetailResponse:

        legislation = await self.client.get(
            legislation_id
        )

        return LegislationDetailResponse(
            id=legislation.id,
            title=legislation.title,
            year=legislation.year,
            legislation_type=(
                legislation.legislation_type
            ),
            status=legislation.status,
            description=legislation.description,
            source_url=legislation.source_url,
            sections=[
                section.model_dump()
                for section in legislation.sections
            ],
        )

    async def search(
        self,
        request: LegislationSearchRequest,
    ) -> LegislationSearchResponse:

        if not self.search_client:

            return LegislationSearchResponse(
                query=request.query,
                results=[],
            )

        results = await self.search_client.search(
            query=request.query,
            limit=request.limit,
        )

        output = []

        for legislation in results:

            output.append(
                LegislationSummary(
                    id=legislation.id,
                    title=legislation.title,
                    year=legislation.year,
                    legislation_type=(
                        legislation.legislation_type
                    ),
                    status=legislation.status,
                    description=(
                        legislation.description
                    ),
                    source_url=(
                        legislation.source_url
                    ),
                )
            )

        return LegislationSearchResponse(
            query=request.query,
            results=output,
        )
