from __future__ import annotations

from pydantic import BaseModel, Field


class DebateContribution(BaseModel):
    """
    A contribution made during a parliamentary debate.
    """

    speaker: str

    text: str

    party: str | None = None

    role: str | None = None

    timestamp: str | None = None


class Debate(BaseModel):
    """
    Parliamentary debate.
    """

    id: str

    title: str

    date: str | None = None

    house: str | None = None

    topic: str | None = None

    source_url: str | None = None

    contributions: list[
        DebateContribution
    ] = Field(default_factory=list)
