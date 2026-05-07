from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    role_family: str
    embedding_model: str
    embedding_backend: str
    llm_provider: str
    llm_model: str

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def eval_dir(self) -> Path:
        return self.data_dir / "eval"

    @property
    def logs_dir(self) -> Path:
        return self.data_dir / "logs"

    @property
    def chroma_dir(self) -> Path:
        return self.data_dir / "index" / "chroma"


def get_settings() -> Settings:
    data_dir = Path(os.getenv("TALENTLENS_DATA_DIR", "data")).resolve()
    return Settings(
        data_dir=data_dir,
        role_family=os.getenv("ROLE_FAMILY", "data-ml"),
        embedding_model=os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/bge-small-en-v1.5"
        ),
        embedding_backend=os.getenv("EMBEDDING_BACKEND", "sentence-transformers"),
        llm_provider=os.getenv("LLM_PROVIDER", "openai"),
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
    )


ROLE_FAMILY_KEYWORDS = {
    "data-ml": [
        "data scientist",
        "data science",
        "machine learning",
        "ml engineer",
        "data engineer",
        "analytics",
        "ai engineer",
        "deep learning",
    ],
    "software": [
        "software engineer",
        "backend",
        "frontend",
        "full stack",
        "full-stack",
        "platform engineer",
    ],
}
