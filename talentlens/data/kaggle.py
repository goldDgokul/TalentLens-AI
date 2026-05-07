from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from kaggle import api as kaggle_api

from talentlens.config import get_settings


@dataclass(frozen=True)
class KaggleDataset:
    name: str
    kaggle_slug: str


def _load_dataset_config(config_path: Path) -> list[KaggleDataset]:
    if not config_path.exists():
        return []
    payload = json.loads(config_path.read_text())
    return [
        KaggleDataset(name=item["name"], kaggle_slug=item.get("kaggle_slug", ""))
        for item in payload
        if "name" in item
    ]


def download_dataset(dataset: KaggleDataset, target_dir: Path) -> Path:
    if not dataset.kaggle_slug:
        raise ValueError(
            f"Kaggle slug missing for '{dataset.name}'. Update data/kaggle_datasets.json."
        )
    target_dir.mkdir(parents=True, exist_ok=True)
    kaggle_api.authenticate()
    kaggle_api.dataset_download_files(
        dataset.kaggle_slug,
        path=str(target_dir),
        unzip=True,
        quiet=False,
    )
    metadata = {
        "name": dataset.name,
        "kaggle_slug": dataset.kaggle_slug,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
    }
    (target_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    return target_dir


def download_all(datasets: list[KaggleDataset] | None = None) -> list[Path]:
    settings = get_settings()
    config_path = settings.data_dir / "kaggle_datasets.json"
    datasets = list(datasets or _load_dataset_config(config_path))
    if not datasets:
        raise ValueError(
            "No datasets configured. Populate data/kaggle_datasets.json and retry."
        )
    raw_dir = settings.raw_dir / "kaggle"
    downloaded: list[Path] = []
    for dataset in datasets:
        slug_name = dataset.kaggle_slug.replace("/", "__")
        target_dir = raw_dir / slug_name
        downloaded.append(download_dataset(dataset, target_dir))
    return downloaded


if __name__ == "__main__":
    download_all()
