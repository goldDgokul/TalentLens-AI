from __future__ import annotations

from typing import Any

from talentlens.llm import LLMClient


def extract_structured_resume(resume_text: str) -> dict[str, Any]:
    client = LLMClient()
    return client.extract_resume(resume_text)
