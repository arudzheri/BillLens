from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from billlens.mps.schemas import (
    MPSearchRequest,
    MPSearchResponse,
    MPSummary,
)
from billlens.services.mps_service import (
    MPsService,
)


router = APIRouter(
    prefix="/api/mps",
    tags=["MPs"],
)


def get_mps_service() -> MPsService:

    raise NotImplementedError(
        "Configure the MPsService dependency."
    )


@router.get(
    "",
    response_model=MPSearchResponse,
)
async def search_mps(
    query: str = "",
    limit: int = 20,
    service: MPsService = Depends(
        get_mps_service
    ),
):

    request = MPSearchRequest(
        query=query,
        limit=limit,
    )

    return await service.search(request)


@router.get(
    "/{mp_id}",
    response_model=MPSummary,
)
async def get_mp(
    mp_id: str,
    service: MPsService = Depends(
        get_mps_service
    ),
):

    try:

        return await service.get(mp_id)

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
