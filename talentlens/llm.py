from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from talentlens.config import get_settings


class LLMClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.provider = self.settings.llm_provider.lower()
        if self.provider == "openai":
            if not os.getenv("OPENAI_API_KEY"):
                raise EnvironmentError("OPENAI_API_KEY is required for OpenAI provider.")
            self.client = OpenAI()
        elif self.provider == "mock":
            self.client = None
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def extract_resume(self, resume_text: str) -> dict[str, Any]:
        if self.provider == "mock":
            return self._mock_extract(resume_text)
        system_prompt = (
            "You are a strict information extractor. Return only JSON with the fields: "
            "name, contact, summary, experience, skills, education, projects."
        )
        user_prompt = f"Extract structured resume data from the text below:\n\n{resume_text}"
        response = self.client.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)

    def answer_question(self, question: str, context: str) -> str:
        if self.provider == "mock":
            return context
        system_prompt = (
            "Answer the question using only the provided context. "
            "Cite sources in brackets like [res_0001:chunk_2]."
        )
        user_prompt = f"Question: {question}\n\nContext:\n{context}"
        response = self.client.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or ""
        return content.strip()

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
