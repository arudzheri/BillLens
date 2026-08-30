from __future__ import annotations

from pydantic import BaseModel, Field


class MPSearchRequest(BaseModel):

    query: str = ""

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )


class MPSummary(BaseModel):

    id: str

    name: str

    party: str | None = None

    constituency: str | None = None

    house: str = "Commons"

    image_url: str | None = None

    profile_url: str | None = None


class MPSearchResponse(BaseModel):

    query: str

    results: list[MPSummary] = Field(
        default_factory=list
    )
