from __future__ import annotations

import json
from typing import Any

import requests

from talentlens.config import get_settings


class OllamaUnavailableError(RuntimeError):
    """Raised when Ollama HTTP requests fail or the Ollama service is unreachable."""


class LLMClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.provider = self.settings.llm_provider.lower()
        if self.provider == "ollama":
            self.base_url = self.settings.ollama_base_url.rstrip("/")
        elif self.provider in {"mock", "none"}:
            self.base_url = ""
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def extract_resume(self, resume_text: str) -> dict[str, Any]:
        if self.provider in {"mock", "none"}:
            return self._mock_extract(resume_text)
        prompt = (
            "Extract structured resume data from the text below and return only valid JSON "
            "with fields: name, contact, summary, experience, skills, education, projects.\n\n"
            f"{resume_text}"
        )
        data = self._ollama_request(
            "/api/generate",
            {
                "model": self.settings.llm_model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0},
            },
        )
        content = data.get("response", "{}")
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Ollama returned malformed JSON for resume extraction."
            ) from exc

    def answer_question(self, question: str, context: str) -> str:
        if self.provider in {"mock", "none"}:
            return context
        data = self._ollama_request(
            "/api/chat",
            {
                "model": self.settings.llm_model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Answer the question using only the provided context. "
                            "Cite sources in brackets like [res_0001:chunk_2]."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\n\nContext:\n{context}",
                    },
                ],
                "stream": False,
                "options": {"temperature": 0.2},
            },
        )
        message = data.get("message", {})
        content = message.get("content", "")
        return str(content).strip()

    def _ollama_request(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}{path}",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise OllamaUnavailableError(
                f"Failed to reach Ollama: {str(exc)}. "
                f"Ensure Ollama is running and accessible. Base URL: {self.base_url}"
            ) from exc

    def _mock_extract(self, resume_text: str) -> dict[str, Any]:
        lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
        name = lines[0] if lines else "Unknown"
        skills = []
        for line in lines:
            if line.lower().startswith("skills"):
                skills = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                break
        return {
            "name": name,
            "contact": {},
            "summary": "",
            "experience": [],
            "skills": skills,
            "education": [],
            "projects": [],
        }
