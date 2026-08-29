from __future__ import annotations

from pydantic import BaseModel, Field


class VoteRecord(BaseModel):
    """
    An individual MP's vote.
    """

    mp_id: str

    mp_name: str

    vote: str

    party: str | None = None


class Vote(BaseModel):
    """
    Parliamentary division/vote.
    """

    id: str

    title: str

    date: str | None = None

    house: str | None = None

    result: str | None = None

    ayes: int | None = None

    noes: int | None = None

    source_url: str | None = None

    records: list[VoteRecord] = Field(
        default_factory=list
    )
