from __future__ import annotations

import json
from pathlib import Path

import chromadb

from talentlens.config import get_settings
from talentlens.rag.chunking import chunk_resume_text
from talentlens.rag.embedder import Embedder


class ResumeIndex:
    def __init__(self, collection_name: str = "resume_chunks") -> None:
        settings = get_settings()
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = Embedder()

    def reset(self) -> None:
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(self.collection.name)

    def index_resume(self, resume_id: str, resume_text: str) -> int:
        chunks = chunk_resume_text(resume_text)
        if not chunks:
            return 0
        embeddings = self.embedder.embed([chunk.text for chunk in chunks])
        ids = [f"{resume_id}:chunk_{chunk.index}" for chunk in chunks]
        metadatas = [
            {"resume_id": resume_id, "section": chunk.section, "chunk_index": chunk.index}
            for chunk in chunks
        ]
        self.collection.add(
            ids=ids,
            documents=[chunk.text for chunk in chunks],
            metadatas=metadatas,
            embeddings=embeddings,
        )
        return len(chunks)

    def index_processed_resumes(self, processed_dir: Path | None = None) -> int:
        settings = get_settings()
        processed_dir = processed_dir or settings.processed_dir / "resumes"
        total = 0
        for resume_path in processed_dir.glob("*.json"):
            payload = json.loads(resume_path.read_text())
            total += self.index_resume(payload["id"], payload["text"])
        return total


def build_resume_index(processed_dir: Path | None = None) -> int:
    index = ResumeIndex()
    return index.index_processed_resumes(processed_dir)


if __name__ == "__main__":
    build_resume_index()
