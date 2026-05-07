from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from talentlens.config import get_settings


GITLAB_INTERVIEW_GUIDES_URL = (
    "https://handbook.gitlab.com/handbook/hiring/interviewing/interview-guides/"
)


def fetch_gitlab_interview_guides(
    url: str = GITLAB_INTERVIEW_GUIDES_URL, target_path: Path | None = None
) -> Path:
    settings = get_settings()
    target_path = target_path or settings.raw_dir / "policies" / "gitlab_interview_guides.md"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    target_path.write_text(response.text, encoding="utf-8")

    metadata = {
        "source": "gitlab_handbook",
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "path": str(target_path),
    }
    metadata_path = target_path.parent / "gitlab_interview_guides.metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    return target_path


if __name__ == "__main__":
    fetch_gitlab_interview_guides()
