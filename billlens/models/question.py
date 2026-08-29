from __future__ import annotations

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    User question sent to BillLens.
    """

    question: str = Field(
        min_length=3,
        max_length=2000,
    )


class QuestionResponse(BaseModel):
    """
    Basic response metadata.
    """

    question: str

    topic: str

    confidence: float = 0.0
