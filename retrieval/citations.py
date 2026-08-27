from __future__ import annotations

from billlens.models import Evidence


def build_citations(
    evidence: list[Evidence],
    max_sources: int = 5,
) -> list[dict]:

    citations = []

    seen = set()

    for index, item in enumerate(
        evidence[:max_sources],
        start=1,
    ):

        key = (
            item.url
            or item.title
        )

        if key in seen:
            continue

        seen.add(key)

        citations.append(
            {
                "number": index,
                "title": item.title,
                "url": item.url,
                "source_type": item.source_type,
                "date": item.date,
            }
        )

    return citations
