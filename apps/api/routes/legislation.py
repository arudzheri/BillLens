from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from billlens.legislation.schemas import (
    LegislationDetailResponse,
    LegislationSearchRequest,
    LegislationSearchResponse,
)
from billlens.services.legislation_service import (
    LegislationService,
)


router = APIRouter(
    prefix="/api/legislation",
    tags=["Legislation"],
)


def get_legislation_service() -> LegislationService:

    raise NotImplementedError(
        "Configure the LegislationService dependency."
    )


@router.get(
    "",
    response_model=LegislationSearchResponse,
)
async def search_legislation(
    query: str = "",
    limit: int = 20,
    service: LegislationService = Depends(
        get_legislation_service
    ),
):

    request = LegislationSearchRequest(
        query=query,
        limit=limit,
    )

    return await service.search(request)


@router.get(
    "/{legislation_id}",
    response_model=LegislationDetailResponse,
)
async def get_legislation(
    legislation_id: str,
    service: LegislationService = Depends(
        get_legislation_service
    ),
):

    try:

        return await service.get(
            legislation_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
