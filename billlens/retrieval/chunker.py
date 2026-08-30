"""
Text chunking for retrieval.
"""

from __future__ import annotations


class TextChunker:
    """
    Splits long text into overlapping chunks.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError(
                "overlap must be >= 0 and < chunk_size"
            )
        
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into chunks.
        """
        
        if not text:
            return []
        
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append(chunk_text)
            
            i += self.chunk_size - self.overlap
        
        return chunks