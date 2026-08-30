from __future__ import annotations

from billlens.models import Evidence


class SemanticRetriever:

    def __init__(
        self,
        model_name: str = (
            "all-MiniLM-L6-v2"
        ),
    ):

        from sentence_transformers import (
            SentenceTransformer,
        )

        self.model = SentenceTransformer(
            model_name
        )

    def search(
        self,
        query: str,
        documents: list[Evidence],
        top_k: int = 10,
    ) -> list[Evidence]:

        if not documents:
            return []

        query_embedding = (
            self.model.encode(
                query,
                normalize_embeddings=True,
            )
        )

        document_texts = [
            document.title
            + " "
            + document.content
            for document in documents
        ]

        document_embeddings = (
            self.model.encode(
                document_texts,
                normalize_embeddings=True,
            )
        )

        scores = (
            document_embeddings
            @ query_embedding
        )

        ranked = sorted(
            zip(
                scores,
                documents,
            ),
            key=lambda item: item[0],
            reverse=True,
        )

        results = []

        for score, document in ranked[:top_k]:

            # Don't mutate the original model.
            updated = document.model_copy(
                update={
                    "relevance_score": float(
                        score
                    )
                }
            )

            results.append(updated)

        return results
