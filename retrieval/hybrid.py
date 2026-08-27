from __future__ import annotations

from billlens.models import Evidence

from .bm25 import BM25Retriever
from .semantic import SemanticRetriever


class HybridRetriever:

    def __init__(
        self,
        documents: list[Evidence],
        semantic_retriever: (
            SemanticRetriever | None
        ) = None,
    ):

        self.documents = documents

        self.bm25 = BM25Retriever(
            documents
        )

        self.semantic = (
            semantic_retriever
            or SemanticRetriever()
        )

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[Evidence]:

        bm25_results = self.bm25.search(
            query,
            top_k=top_k * 2,
        )

        semantic_results = (
            self.semantic.search(
                query,
                self.documents,
                top_k=top_k * 2,
            )
        )

        combined = {}

        # BM25 contribution
        for rank, document in enumerate(
            bm25_results
        ):

            key = (
                document.id
                or document.url
                or document.title
            )

            score = (
                1.0 / (rank + 1)
            )

            combined[key] = (
                combined.get(key, 0)
                + score * 0.5
            )

        # Semantic contribution
        for rank, document in enumerate(
            semantic_results
        ):

            key = (
                document.id
                or document.url
                or document.title
            )

            score = (
                1.0 / (rank + 1)
            )

            combined[key] = (
                combined.get(key, 0)
                + score * 0.5
            )

        document_lookup = {}

        for document in (
            bm25_results
            + semantic_results
        ):

            key = (
                document.id
                or document.url
                or document.title
            )

            document_lookup[key] = document

        ranked = sorted(
            combined.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        results = []

        for key, score in ranked[:top_k]:

            document = document_lookup[key]

            results.append(
                document.model_copy(
                    update={
                        "relevance_score": float(
                            min(score, 1.0)
                        )
                    }
                )
            )

        return results
