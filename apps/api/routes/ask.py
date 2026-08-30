from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from billlens.ask.schemas import (
    AskRequest,
    AskResponse,
)
from billlens.services.ask_service import AskService


router = APIRouter(
    prefix="/api/ask",
    tags=["Ask Parliament"],
)


def get_ask_service() -> AskService:
    """
    Dependency provider.

    Replace this with the application's
    dependency container in production.
    """

    return AskService()


@router.post(
    "",
    response_model=AskResponse,
)
async def ask_parliament(
    request: AskRequest,
    service: AskService = Depends(
        get_ask_service
    ),
) -> AskResponse:

    try:

        return await service.ask(request)

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Unable to process question.",
        ) from exc
