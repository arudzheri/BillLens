from __future__ import annotations

from pydantic import BaseModel, Field


class DashboardStats(BaseModel):
    """
    High-level statistics displayed on the BillLens dashboard.
    """

    bills_tracked: int = 0

    active_bills: int = 0

    MPs_tracked: int = 0

    legislation_tracked: int = 0

    debates_indexed: int = 0

    votes_indexed: int = 0


class RecentActivity(BaseModel):
    """
    Recent parliamentary activity.
    """

    title: str

    activity_type: str

    date: str | None = None

    url: str | None = None


class DashboardResponse(BaseModel):
    """
    Complete dashboard response.
    """

    stats: DashboardStats

    recent_activity: list[RecentActivity] = Field(
        default_factory=list
    )
