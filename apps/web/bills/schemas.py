from __future__ import annotations

from pydantic import BaseModel, Field


class BillSearchRequest(BaseModel):

    query: str = ""

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )


class BillSummary(BaseModel):

    id: str

    title: str

    description: str | None = None

    status: str | None = None

    introduced_date: str | None = None

    sponsor: str | None = None

    source_url: str | None = None


class BillSearchResponse(BaseModel):

    query: str

    results: list[BillSummary] = Field(
        default_factory=list
    )


class BillDetailResponse(BillSummary):

    house: str | None = None

    subjects: list[str] = Field(
        default_factory=list
    )

    stages: list[dict] = Field(
        default_factory=list
    )
