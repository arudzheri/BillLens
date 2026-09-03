from __future__ import annotations

from fastapi import APIRouter, Depends

from apps.web.dashboard.schemas import (
    DashboardResponse,
)
from apps.api.services.dashboard_service import (
    DashboardService,
)


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


def get_dashboard_service() -> DashboardService:

    return DashboardService()


@router.get(
    "",
    response_model=DashboardResponse,
)
async def dashboard(
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):

    return await service.get_dashboard()
