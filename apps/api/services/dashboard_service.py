from __future__ import annotations

from typing import Any

from apps.web.dashboard.schemas import (
    DashboardResponse,
    DashboardStats,
    RecentActivity,
)


class DashboardService:
    """
    Aggregates information for the BillLens dashboard.
    """

    def __init__(
        self,
        bills_client: Any = None,
        mps_client: Any = None,
        legislation_client: Any = None,
    ):
        self.bills_client = bills_client
        self.mps_client = mps_client
        self.legislation_client = (
            legislation_client
        )

    async def get_dashboard(
        self,
    ) -> DashboardResponse:

        bills = []
        mps = []
        legislation = []

        if self.bills_client:

            try:

                bills = await self.bills_client.search(
                    query="",
                    limit=100,
                )

            except Exception:
                bills = []

        if self.mps_client:

            try:

                mps = await self.mps_client.search(
                    query="",
                    limit=100,
                )

            except Exception:
                mps = []

        if self.legislation_client:

            try:

                legislation = (
                    await self.legislation_client.search(
                        query="",
                        limit=100,
                    )
                )

            except Exception:
                legislation = []

        stats = DashboardStats(
            bills_tracked=len(bills),
            active_bills=sum(
                1
                for bill in bills
                if getattr(
                    bill,
                    "status",
                    None,
                )
                not in {
                    "completed",
                    "withdrawn",
                }
            ),
            MPs_tracked=len(mps),
            legislation_tracked=len(
                legislation
            ),
        )

        recent_activity = []

        for bill in bills[:10]:

            recent_activity.append(
                RecentActivity(
                    title=bill.title,
                    activity_type="bill",
                    date=getattr(
                        bill,
                        "introduced_date",
                        None,
                    ),
                    url=getattr(
                        bill,
                        "source_url",
                        None,
                    ),
                )
            )

        return DashboardResponse(
            stats=stats,
            recent_activity=recent_activity,
        )
