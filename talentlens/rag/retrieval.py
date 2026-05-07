from __future__ import annotations

from dataclasses import dataclass
import re
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
        self.use_hash_backend = self.embedder.backend == "hash"

    def retrieve(
        self, query: str, top_k: int = 4, resume_id: str | None = None
    ) -> list[RetrievedChunk]:
        where_clause = {"resume_id": resume_id} if resume_id else None
        if self.use_hash_backend:
            results = self.collection.get(
                include=["documents", "metadatas"],
                where=where_clause,
            )
            query_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
            title_hint = bool({"title", "company", "employer", "current"} & query_tokens)
            scored: list[RetrievedChunk] = []
            for idx, chunk_id in enumerate(results["ids"]):
                text = results["documents"][idx]
                metadata = results["metadatas"][idx]
                tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
                score = len(tokens & query_tokens) / max(len(query_tokens), 1)
                if title_hint and metadata.get("section") == "experience":
                    score += 0.2
                scored.append(
                    RetrievedChunk(
                        chunk_id=chunk_id,
                        text=text,
                        metadata=metadata,
                        score=score,
                    )
                )
            return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

        embeddings = self.embedder.embed([query])
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
