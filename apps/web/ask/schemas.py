from __future__ import annotations

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """
    User's parliamentary question.
    """

    question: str = Field(
        min_length=3,
        max_length=2000,
    )


class AskSource(BaseModel):
    """
    Source displayed underneath an answer.
    """

    title: str

    source_type: str

    url: str | None = None

    date: str | None = None


class AskResponse(BaseModel):
    """
    BillLens answer.
    """

    question: str

    answer: str

    confidence: float = 0.0

    sources: list[AskSource] = Field(
        default_factory=list
    )

    warnings: list[str] = Field(
        default_factory=list
    )
