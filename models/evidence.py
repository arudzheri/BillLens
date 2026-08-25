from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """
    A single piece of evidence retrieved from
    Parliament, legislation, Lex, Hansard, etc.
    """

    id: str | None = None

    title: str

    content: str

    source_type: str

    url: str | None = None

    date: str | None = None

    relevance_score: float = 0.0

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    def citation(self) -> str:
        """
        Human-readable citation.
        """

        if self.url:
            return f"{self.title} ({self.url})"

        return self.title
