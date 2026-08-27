from __future__ import annotations

from billlens.models import Evidence


class Reranker:

    def rerank(
        self,
        query: str,
        documents: list[Evidence],
        top_k: int = 10,
    ) -> list[Evidence]:

        query_words = set(
            query.lower().split()
        )

        scored = []

        for document in documents:

            document_words = set(
                (
                    document.title
                    + " "
                    + document.content
                )
                .lower()
                .split()
            )

            overlap = len(
                query_words
                & document_words
            )

            lexical_score = (
                overlap
                / max(
                    len(query_words),
                    1,
                )
            )

            final_score = (
                document.relevance_score
                * 0.7
                + lexical_score
                * 0.3
            )

            scored.append(
                (
                    final_score,
                    document,
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document.model_copy(
                update={
                    "relevance_score": float(
                        min(score, 1.0)
                    )
                }
            )
            for score, document
            in scored[:top_k]
        ]
