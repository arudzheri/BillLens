from __future__ import annotations

import math
import re

from billlens.models import Evidence


def tokenize(text: str) -> list[str]:
    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )


class BM25Retriever:

    def __init__(
        self,
        documents: list[Evidence],
        k1: float = 1.5,
        b: float = 0.75,
    ):
        self.documents = documents

        self.k1 = k1

        self.b = b

        self.doc_tokens = [
            tokenize(
                doc.title
                + " "
                + doc.content
            )
            for doc in documents
        ]

        self.avgdl = (
            sum(
                len(tokens)
                for tokens in self.doc_tokens
            )
            / max(len(self.doc_tokens), 1)
        )

        self.document_frequency = {}

        for tokens in self.doc_tokens:

            for token in set(tokens):

                self.document_frequency[
                    token
                ] = (
                    self.document_frequency.get(
                        token,
                        0,
                    )
                    + 1
                )

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[Evidence]:

        query_tokens = tokenize(query)

        scored = []

        total_docs = len(
            self.documents
        )

        for index, document in enumerate(
            self.documents
        ):

            tokens = self.doc_tokens[index]

            score = 0.0

            for term in query_tokens:

                frequency = tokens.count(term)

                if frequency == 0:
                    continue

                df = self.document_frequency.get(
                    term,
                    0,
                )

                idf = math.log(
                    1
                    + (
                        total_docs - df + 0.5
                    )
                    / (
                        df + 0.5
                    )
                )

                denominator = (
                    frequency
                    + self.k1
                    * (
                        1
                        - self.b
                        + self.b
                        * (
                            len(tokens)
                            / max(
                                self.avgdl,
                                1,
                            )
                        )
                    )
                )

                score += (
                    idf
                    * (
                        frequency
                        * (
                            self.k1 + 1
                        )
                        / denominator
                    )
                )

            scored.append(
                (
                    score,
                    document,
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for score, document
            in scored[:top_k]
            if score > 0
        ]
