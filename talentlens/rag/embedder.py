from __future__ import annotations

import zlib
import numpy as np
from sentence_transformers import SentenceTransformer

from talentlens.config import get_settings


class Embedder:
    def __init__(self) -> None:
        settings = get_settings()
        self.backend = settings.embedding_backend.lower()
        self.model_name = settings.embedding_model
        self._model: SentenceTransformer | None = None
        if self.backend == "sentence-transformers":
            self._model = SentenceTransformer(self.model_name)
        elif self.backend == "hash":
            self._model = None
        else:
            raise ValueError(f"Unsupported embedding backend: {self.backend}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self.backend == "sentence-transformers":
            assert self._model is not None
            embeddings = self._model.encode(list(texts), normalize_embeddings=True)
            return embeddings.tolist()
        return [self._hash_embed(text) for text in texts]

    def _hash_embed(self, text: str, dims: int = 256) -> list[float]:
        vector = np.zeros(dims, dtype=float)
        for token in text.lower().split():
            index = zlib.crc32(token.encode("utf-8")) % dims
            vector[index] += 1.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()
