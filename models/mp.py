from __future__ import annotations

from pydantic import BaseModel, Field


class MP(BaseModel):
    """
    Member of Parliament.
    """

    id: str

    name: str

    party: str | None = None

    constituency: str | None = None

    house: str = "Commons"

    image_url: str | None = None

    profile_url: str | None = None

    email: str | None = None

    twitter: str | None = None

    website: str | None = None

    active: bool = True

    roles: list[str] = Field(
        default_factory=list
    )
