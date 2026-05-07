from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Iterable

import pandas as pd

from talentlens.config import ROLE_FAMILY_KEYWORDS, get_settings


RESUME_TEXT_COLUMNS = [
    "resume",
    "resume_text",
    "Resume",
    "Resume_str",
    "text",
    "Content",
]
RESUME_CATEGORY_COLUMNS = [
    "Category",
    "category",
    "job_title",
    "Job Title",
    "Role",
    "role",
]
JD_TEXT_COLUMNS = [
    "description",
    "job_description",
    "jobDescription",
    "Job Description",
    "details",
]
JD_TITLE_COLUMNS = ["title", "job_title", "Job Title", "position_title"]


def _find_column(columns: Iterable[str], candidates: list[str]) -> str | None:
    lowered = {col.lower(): col for col in columns}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    return None


def _column_attr(column: str) -> str:
    return re.sub(r"\W|^(?=\d)", "_", column)


def _matches_role_family(text: str, role_family: str) -> bool:
    keywords = ROLE_FAMILY_KEYWORDS.get(role_family, [])
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)


def _write_manifest_row(manifest_path: Path, row: dict) -> None:
    with manifest_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


def normalize_resumes(raw_dir: Path | None = None, output_dir: Path | None = None) -> int:
    settings = get_settings()
    raw_dir = raw_dir or settings.raw_dir / "kaggle"
    output_dir = output_dir or settings.processed_dir / "resumes"
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.jsonl"
    if manifest_path.exists():
        manifest_path.unlink()

    resume_index = 0
    for data_file in raw_dir.glob("**/*.csv"):
        frame = pd.read_csv(data_file)
        text_column = _find_column(frame.columns, RESUME_TEXT_COLUMNS)
        if not text_column:
            continue
        category_column = _find_column(frame.columns, RESUME_CATEGORY_COLUMNS)
        text_attr = _column_attr(text_column)
        category_attr = _column_attr(category_column) if category_column else None
        for row in frame.itertuples(index=True, name="ResumeRow"):
            row_index = row.Index
            text = str(getattr(row, text_attr, "")).strip()
            if not text:
                continue
            category = str(getattr(row, category_attr, "")).strip() if category_attr else ""
            if category and not _matches_role_family(category, settings.role_family):
                if not _matches_role_family(text, settings.role_family):
                    continue
            resume_id = f"res_{resume_index:04d}"
            payload = {
                "id": resume_id,
                "source": "kaggle",
                "role_family": settings.role_family,
                "category": category,
                "text": text,
                "metadata": {
                    "source_file": str(data_file),
                    "row_index": int(row_index),
                },
            }
            (output_dir / f"{resume_id}.json").write_text(
                json.dumps(payload, indent=2)
            )
            _write_manifest_row(
                manifest_path,
                {
                    "id": resume_id,
                    "source_file": str(data_file),
                    "row_index": int(row_index),
                },
            )
            resume_index += 1

    return resume_index


def normalize_job_descriptions(
    raw_dir: Path | None = None, output_dir: Path | None = None
) -> int:
    settings = get_settings()
    raw_dir = raw_dir or settings.raw_dir / "kaggle"
    output_dir = output_dir or settings.processed_dir / "jds"
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.jsonl"
    if manifest_path.exists():
        manifest_path.unlink()

    jd_index = 0
    for data_file in raw_dir.glob("**/*.csv"):
        frame = pd.read_csv(data_file)
        text_column = _find_column(frame.columns, JD_TEXT_COLUMNS)
        title_column = _find_column(frame.columns, JD_TITLE_COLUMNS)
        if not text_column:
            continue
        text_attr = _column_attr(text_column)
        title_attr = _column_attr(title_column) if title_column else None
        for row in frame.itertuples(index=True, name="JDRow"):
            row_index = row.Index
            text = str(getattr(row, text_attr, "")).strip()
            if not text:
                continue
            title = str(getattr(row, title_attr, "")).strip() if title_attr else ""
            combined = f"{title} {text}"
            if not _matches_role_family(combined, settings.role_family):
                continue
            jd_id = f"jd_{jd_index:04d}"
            payload = {
                "id": jd_id,
                "source": "kaggle",
                "role_family": settings.role_family,
                "title": title,
                "text": text,
                "metadata": {
                    "source_file": str(data_file),
                    "row_index": int(row_index),
                },
            }
            (output_dir / f"{jd_id}.json").write_text(json.dumps(payload, indent=2))
            _write_manifest_row(
                manifest_path,
                {
                    "id": jd_id,
                    "source_file": str(data_file),
                    "row_index": int(row_index),
                },
            )
            jd_index += 1
    return jd_index


if __name__ == "__main__":
    normalize_resumes()
    normalize_job_descriptions()
