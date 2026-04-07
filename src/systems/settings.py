"""Runtime-adjustable settings with local persistence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .paths import saves_dir


SETTINGS_FILE_NAME = "settings.json"
MIN_START_LEVEL = 1
MAX_START_LEVEL = 10


def clamp_selected_start_level(value: int) -> int:
    return max(MIN_START_LEVEL, min(int(value), MAX_START_LEVEL))


@dataclass
class RuntimeSettings:
    music_enabled: bool = True
    selected_start_level: int = 1
    # Placeholder hook for future settings expansion.
    window_mode: str = "windowed"

    @property
    def audio_enabled(self) -> bool:
        """Backward-compatible alias used by existing UI/audio flow."""
        return self.music_enabled

    @audio_enabled.setter
    def audio_enabled(self, value: bool) -> None:
        self.music_enabled = bool(value)

    def to_payload(self) -> dict[str, object]:
        return {
            "music_enabled": bool(self.music_enabled),
            "selected_start_level": clamp_selected_start_level(self.selected_start_level),
        }


def _settings_file_path(path: Path | None = None) -> Path:
    return path if path is not None else saves_dir() / SETTINGS_FILE_NAME


def load_settings(path: Path | None = None) -> RuntimeSettings:
    file_path = _settings_file_path(path)
    defaults = RuntimeSettings()
    if not file_path.exists():
        return defaults

    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return defaults

    if not isinstance(payload, dict):
        return defaults

    music_enabled = payload.get("music_enabled", defaults.music_enabled)
    selected_start_level = payload.get("selected_start_level", defaults.selected_start_level)
    return RuntimeSettings(
        music_enabled=bool(music_enabled),
        selected_start_level=(
            clamp_selected_start_level(selected_start_level)
            if isinstance(selected_start_level, int)
            else defaults.selected_start_level
        ),
    )


def save_settings(settings: RuntimeSettings, path: Path | None = None) -> None:
    file_path = _settings_file_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(settings.to_payload(), indent=2),
        encoding="utf-8",
    )
