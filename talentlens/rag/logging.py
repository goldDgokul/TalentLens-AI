from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from talentlens.config import get_settings
from talentlens.rag.retrieval import RetrievedChunk


def log_retrieval(query: str, chunks: list[RetrievedChunk]) -> Path:
    settings = get_settings()
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = settings.logs_dir / "retrieval_log.jsonl"
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "chunks": [
            {
                "chunk_id": chunk.chunk_id,
                "score": chunk.score,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ],
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")
    return log_path
