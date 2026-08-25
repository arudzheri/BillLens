from __future__ import annotations

from pydantic import BaseModel, Field


class BillStage(BaseModel):
    """
    A single stage in the lifecycle of a bill.
    """

    name: str

    date: str | None = None

    house: str | None = None

    description: str | None = None

    source_url: str | None = None


class Bill(BaseModel):
    """
    Parliamentary bill.
    """

    id: str

    title: str

    short_title: str | None = None

    description: str | None = None

    status: str | None = None

    introduced_date: str | None = None

    sponsor: str | None = None

    house: str | None = None

    source_url: str | None = None

    stages: list[BillStage] = Field(
        default_factory=list
    )

    subjects: list[str] = Field(
        default_factory=list
    )
