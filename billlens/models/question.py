"""
Question Models
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Request model for user questions.
    """
    question: str = Field(..., description="The natural language question to ask BillLens.")
    context: Optional[str] = Field(None, description="Optional extra context for the query.")


class QuestionResponse(BaseModel):
    """
    Response model wrapper for question queries.
    """
    question: str
    status: str = "success"


class QuestionPlan(BaseModel):
    """
    Plan model generated for answering a question.
    """
    original_question: str
    topic: str
    steps: List[str] = Field(default_factory=list)
    