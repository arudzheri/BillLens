"""
Embedding service for semantic search.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Manages embeddings using Sentence Transformers.
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
    
    async def load(self) -> None:
        """Load the embedding model."""
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load embedding model: {e}"
            )
    
    async def unload(self) -> None:
        """Unload the embedding model."""
        if self.model:
            del self.model
            self.model = None
    
    def encode(
        self,
        texts: list[str] | str,
        normalize: bool = True,
    ) -> np.ndarray:
        """
        Encode text(s) into embeddings.
        
        Returns normalized embeddings by default.
        """
        
        if not self.model:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize,
        )
        
        return embeddings
    
    def similarity(
        self,
        embeddings1: np.ndarray,
        embeddings2: np.ndarray,
    ) -> np.ndarray:
        """
        Compute cosine similarity between embeddings.
        """
        
        if embeddings1.ndim == 1:
            embeddings1 = embeddings1.reshape(1, -1)
        
        if embeddings2.ndim == 1:
            embeddings2 = embeddings2.reshape(1, -1)
        
        return np.dot(embeddings1, embeddings2.T)