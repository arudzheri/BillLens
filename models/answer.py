from __future__ import annotations

from pydantic import BaseModel, Field


class AnswerSource(BaseModel):
    title: str

    source_type: str

    url: str | None = None

    date: str | None = None


class AnswerClaim(BaseModel):
    text: str

    supported: bool

    confidence: float

    sources: list[AnswerSource] = Field(
        default_factory=list
    )


class AnswerResponse(BaseModel):
    question: str

    summary: str

    what_happened: list[str] = Field(
        default_factory=list
    )

    legislation: list[str] = Field(
        default_factory=list
    )

    parliamentary_activity: list[str] = Field(
        default_factory=list
    )

    votes: list[str] = Field(
        default_factory=list
    )

    what_did_not_happen: list[str] = Field(
        default_factory=list
    )

    claims: list[AnswerClaim] = Field(
        default_factory=list
    )

    sources: list[AnswerSource] = Field(
        default_factory=list
    )

    confidence: float = 0.0

    warnings: list[str] = Field(
        default_factory=list
    )
