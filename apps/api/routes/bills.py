from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from apps.web.bills.schemas import (
    BillDetailResponse,
    BillSearchRequest,
    BillSearchResponse,
)
from apps.api.services.bills_service import (
    BillsService,
)


router = APIRouter(
    prefix="/api/bills",
    tags=["Bills"],
)


def get_bills_service() -> BillsService:
    """
    Dependency provider.

    Connect the real Parliament client here.
    """

    raise NotImplementedError(
        "Configure the BillsService dependency."
    )


@router.get(
    "",
    response_model=BillSearchResponse,
)
async def search_bills(
    query: str = "",
    limit: int = 20,
    service: BillsService = Depends(
        get_bills_service
    ),
):

    request = BillSearchRequest(
        query=query,
        limit=limit,
    )

    return await service.search(request)


@router.get(
    "/{bill_id}",
    response_model=BillDetailResponse,
)
async def get_bill(
    bill_id: str,
    service: BillsService = Depends(
        get_bills_service
    ),
):

    try:

        return await service.get(
            bill_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
