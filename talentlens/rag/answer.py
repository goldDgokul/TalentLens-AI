from __future__ import annotations

from typing import Any

from talentlens.llm import LLMClient
from talentlens.rag.retrieval import RetrievedChunk


def build_context(chunks: list[RetrievedChunk]) -> str:
    return "\n\n".join(
        f"[{chunk.chunk_id}] {chunk.text}" for chunk in chunks
    ).strip()


def answer_with_citations(question: str, chunks: list[RetrievedChunk]) -> dict[str, Any]:
    client = LLMClient()
    context = build_context(chunks)
    answer = client.answer_question(question, context)
    return {"answer": answer, "citations": [chunk.chunk_id for chunk in chunks]}
