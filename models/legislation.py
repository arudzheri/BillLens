from __future__ import annotations

from pydantic import BaseModel, Field


class LegislationSection(BaseModel):
    """
    A section of an Act or legislative document.
    """

    id: str

    title: str

    number: str | None = None

    text: str

    source_url: str | None = None


class Legislation(BaseModel):
    """
    UK legislation document.
    """

    id: str

    title: str

    year: int | None = None

    legislation_type: str | None = None

    status: str | None = None

    description: str | None = None

    source_url: str | None = None

    sections: list[LegislationSection] = Field(
        default_factory=list
    )
