from __future__ import annotations

from pathlib import Path

import pdfplumber
from docx import Document


def extract_text_from_pdf(path: Path) -> str:
    chunks: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text:
                chunks.append(text)
    return "\n".join(chunks).strip()


def extract_text_from_docx(path: Path) -> str:
    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs).strip()


def parse_resume_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    if suffix in {".docx", ".doc"}:
        return extract_text_from_docx(path)
    return path.read_text(encoding="utf-8").strip()
