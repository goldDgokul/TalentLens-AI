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
    if client.provider == "mock":
        top_chunk = chunks[0] if chunks else None
        answer = (
            f"{top_chunk.text} [{top_chunk.chunk_id}]"
            if top_chunk
            else "No relevant content found."
        )
    else:
        answer = client.answer_question(question, context)
    return {"answer": answer, "citations": [chunk.chunk_id for chunk in chunks]}
