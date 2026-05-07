from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import chromadb

from talentlens.config import get_settings
from talentlens.rag.embedder import Embedder


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    score: float


class ResumeRetriever:
    def __init__(self, collection_name: str = "resume_chunks") -> None:
        settings = get_settings()
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = Embedder()

    def retrieve(
        self, query: str, top_k: int = 4, resume_id: str | None = None
    ) -> list[RetrievedChunk]:
        embeddings = self.embedder.embed([query])
        where_clause = {"resume_id": resume_id} if resume_id else None
        result = self.collection.query(
            query_embeddings=embeddings,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
            where=where_clause,
        )
        chunks: list[RetrievedChunk] = []
        for idx, chunk_id in enumerate(result["ids"][0]):
            text = result["documents"][0][idx]
            metadata = result["metadatas"][0][idx]
            distance = result["distances"][0][idx]
            score = 1 - distance if distance is not None else 0.0
            chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id, text=text, metadata=metadata, score=score
                )
            )
        return chunks
