from __future__ import annotations

from pydantic import BaseModel, Field


class LegislationSearchRequest(BaseModel):

    query: str = ""

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )


class LegislationSummary(BaseModel):

    id: str

    title: str

    year: int | None = None

    legislation_type: str | None = None

    status: str | None = None

    description: str | None = None

    source_url: str | None = None


class LegislationSearchResponse(BaseModel):

    query: str

    results: list[LegislationSummary] = Field(
        default_factory=list
    )


class LegislationDetailResponse(
    LegislationSummary
):

    sections: list[dict] = Field(
        default_factory=list
    )
