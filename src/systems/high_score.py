"""Local high score persistence for the active game loop."""

from __future__ import annotations

import json
from pathlib import Path

from .paths import saves_dir


HIGH_SCORE_FILE_NAME = "high_score.json"


def _high_score_file_path(path: Path | None = None) -> Path:
    return path if path is not None else saves_dir() / HIGH_SCORE_FILE_NAME


def load_high_score(path: Path | None = None) -> int:
    file_path = _high_score_file_path(path)
    if not file_path.exists():
        return 0

    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0

    value = payload.get("high_score", 0) if isinstance(payload, dict) else 0
    return int(value) if isinstance(value, int) and value >= 0 else 0


def save_high_score(value: int, path: Path | None = None) -> None:
    file_path = _high_score_file_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"high_score": max(0, int(value))}
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
