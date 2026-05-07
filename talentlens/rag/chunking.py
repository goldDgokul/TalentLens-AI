from __future__ import annotations

from dataclasses import dataclass


SECTION_HEADERS = {
    "experience": ["experience", "work history", "employment"],
    "projects": ["projects", "project experience"],
    "education": ["education", "academic"],
    "skills": ["skills", "technical skills"],
    "summary": ["summary", "profile", "objective"],
}


@dataclass(frozen=True)
class Chunk:
    text: str
    section: str
    index: int


def _detect_section(line: str) -> str | None:
    normalized = line.strip().lower().rstrip(":")
    for section, headers in SECTION_HEADERS.items():
        if normalized in headers:
            return section
    return None


def chunk_resume_text(resume_text: str, max_chars: int = 800) -> list[Chunk]:
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    current_section = "general"
    sections: dict[str, list[str]] = {current_section: []}
    for line in lines:
        detected = _detect_section(line)
        if detected:
            current_section = detected
            sections.setdefault(current_section, [])
            continue
        sections.setdefault(current_section, []).append(line)

    chunks: list[Chunk] = []
    chunk_index = 0
    for section, content_lines in sections.items():
        buffer: list[str] = []
        buffer_len = 0
        for line in content_lines:
            if buffer_len + len(line) > max_chars:
                text = "\n".join(buffer).strip()
                if text:
                    chunks.append(Chunk(text=text, section=section, index=chunk_index))
                    chunk_index += 1
                buffer = []
                buffer_len = 0
            buffer.append(line)
            buffer_len += len(line)
        text = "\n".join(buffer).strip()
        if text:
            chunks.append(Chunk(text=text, section=section, index=chunk_index))
            chunk_index += 1
    return chunks
