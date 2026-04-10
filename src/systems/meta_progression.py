"""Persistent meta progression storage for cross-run unlock state."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .paths import saves_dir


META_PROGRESSION_FILE_NAME = "meta_progression.json"
DEFAULT_UNLOCKED_CHARACTERS: tuple[str, ...] = ("teddy_f",)


@dataclass
class MetaProgression:
    unlocked_characters: list[str] = field(default_factory=lambda: list(DEFAULT_UNLOCKED_CHARACTERS))
    unlock_conditions_met: list[str] = field(default_factory=list)
    total_runs_completed: int = 0
    bosses_defeated: int = 0
    best_score: int = 0

    def to_payload(self) -> dict[str, object]:
        unlocked = sorted({str(char_id) for char_id in self.unlocked_characters if str(char_id)})
        if not unlocked:
            unlocked = list(DEFAULT_UNLOCKED_CHARACTERS)
        conditions = sorted(
            {
                str(condition_id)
                for condition_id in self.unlock_conditions_met
                if str(condition_id)
            }
        )
        return {
            "unlocked_characters": unlocked,
            "unlock_conditions_met": conditions,
            "total_runs_completed": max(0, int(self.total_runs_completed)),
            "bosses_defeated": max(0, int(self.bosses_defeated)),
            "best_score": max(0, int(self.best_score)),
        }


def _meta_progression_file_path(path: Path | None = None) -> Path:
    return path if path is not None else saves_dir() / META_PROGRESSION_FILE_NAME


def load_meta_progression(path: Path | None = None) -> MetaProgression:
    file_path = _meta_progression_file_path(path)
    defaults = MetaProgression()
    if not file_path.exists():
        return defaults
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return defaults
    if not isinstance(payload, dict):
        return defaults

    unlocked_raw = payload.get("unlocked_characters", defaults.unlocked_characters)
    conditions_raw = payload.get("unlock_conditions_met", defaults.unlock_conditions_met)
    total_runs_raw = payload.get("total_runs_completed", defaults.total_runs_completed)
    bosses_raw = payload.get("bosses_defeated", defaults.bosses_defeated)
    best_score_raw = payload.get("best_score", defaults.best_score)
    unlocked = (
        [str(item) for item in unlocked_raw if isinstance(item, str) and str(item)]
        if isinstance(unlocked_raw, list)
        else list(defaults.unlocked_characters)
    )
    conditions = (
        [str(item) for item in conditions_raw if isinstance(item, str) and str(item)]
        if isinstance(conditions_raw, list)
        else list(defaults.unlock_conditions_met)
    )
    if not unlocked:
        unlocked = list(DEFAULT_UNLOCKED_CHARACTERS)
    return MetaProgression(
        unlocked_characters=sorted(set(unlocked)),
        unlock_conditions_met=sorted(set(conditions)),
        total_runs_completed=max(0, int(total_runs_raw)) if isinstance(total_runs_raw, int) else 0,
        bosses_defeated=max(0, int(bosses_raw)) if isinstance(bosses_raw, int) else 0,
        best_score=max(0, int(best_score_raw)) if isinstance(best_score_raw, int) else 0,
    )


def save_meta_progression(progress: MetaProgression, path: Path | None = None) -> None:
    file_path = _meta_progression_file_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(progress.to_payload(), indent=2),
        encoding="utf-8",
    )
