from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextChunk:
    id: str

    text: str

    source_id: str

    chunk_index: int


def chunk_text(
    text: str,
    source_id: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[TextChunk]:

    words = text.split()

    chunks = []

    start = 0
    index = 0

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words),
        )

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(
            TextChunk(
                id=f"{source_id}:{index}",
                text=chunk,
                source_id=source_id,
                chunk_index=index,
            )
        )

        if end == len(words):
            break

        start = end - overlap

        index += 1

    return chunks
