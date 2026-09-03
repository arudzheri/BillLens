from __future__ import annotations

from apps.web.dashboard.schemas import (
    DashboardResponse,
    DashboardStats,
    RecentActivity,
)


class DashboardService:
    """
    Provides data for the BillLens dashboard.
    """

    def __init__(
        self,
        bills_client=None,
        mps_client=None,
        legislation_client=None,
    ):
        self.bills_client = bills_client
        self.mps_client = mps_client
        self.legislation_client = legislation_client

    async def get_dashboard(
        self,
    ) -> DashboardResponse:

        bills = []
        MPs = []
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
                MPs = await self.mps_client.search(
                    query="",
                    limit=100,
                )
            except Exception:
                MPs = []

        stats = DashboardStats(
            bills_tracked=len(bills),
            active_bills=sum(
                1
                for bill in bills
                if bill.status
                and bill.status.lower()
                not in {
                    "completed",
                    "withdrawn",
                }
            ),
            MPs_tracked=len(MPs),
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
                    date=bill.introduced_date,
                    url=bill.source_url,
                )
            )

        return DashboardResponse(
            stats=stats,
            recent_activity=recent_activity,
        )
