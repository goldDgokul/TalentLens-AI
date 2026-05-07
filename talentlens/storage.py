from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from talentlens.config import get_settings


def ensure_data_dirs() -> None:
    settings = get_settings()
    settings.raw_dir.mkdir(parents=True, exist_ok=True)
    settings.processed_dir.mkdir(parents=True, exist_ok=True)
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    (settings.raw_dir / "uploads").mkdir(parents=True, exist_ok=True)
    (settings.processed_dir / "resumes").mkdir(parents=True, exist_ok=True)


def save_raw_resume(resume_id: str, filename: str, content: bytes) -> Path:
    settings = get_settings()
    target_dir = settings.raw_dir / "uploads" / resume_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / filename
    target_path.write_bytes(content)
    return target_path


def save_processed_resume(
    resume_id: str,
    resume_text: str,
    structured_data: dict[str, Any],
    source_path: Path,
) -> Path:
    settings = get_settings()
    target_dir = settings.processed_dir / "resumes"
    target_dir.mkdir(parents=True, exist_ok=True)
    raw_structured_path = source_path.parent / "structured.json"
    record = {
        "id": resume_id,
        "raw_text_path": str(source_path),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "structured": structured_data,
        "text": resume_text,
    }
    raw_structured_path.write_text(json.dumps(structured_data, indent=2))
    target_path = target_dir / f"{resume_id}.json"
    target_path.write_text(json.dumps(record, indent=2))
    return target_path


def load_resume(resume_id: str) -> dict[str, Any]:
    settings = get_settings()
    path = settings.processed_dir / "resumes" / f"{resume_id}.json"
    return json.loads(path.read_text())
