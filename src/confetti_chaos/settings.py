from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from pathlib import Path
import json

APP_NAME = "Confetti Chaos"
APP_AUTHOR = "Jason Mosley"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAVE_DIR = PROJECT_ROOT / "saves"
SETTINGS_FILE = SAVE_DIR / "settings.json"
SAVE_FILE = SAVE_DIR / "savegame.json"


@dataclass(slots=True)
class GameSettings:
    screen_width: int = 1280
    screen_height: int = 720
    title: str = APP_NAME
    fps: int = 60
    master_volume: float = 0.8
    fullscreen: bool = False
    show_debug_overlay: bool = False
    starting_scene: str = "title"
    background_color: tuple[int, int, int] = (250, 247, 241)

    @property
    def window_size(self) -> tuple[int, int]:
        return (self.screen_width, self.screen_height)


def ensure_runtime_dirs() -> None:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


def load_settings() -> GameSettings:
    ensure_runtime_dirs()
    if not SETTINGS_FILE.exists():
        return GameSettings()

    raw_data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    allowed = {field.name for field in fields(GameSettings)}
    normalized = {key: value for key, value in raw_data.items() if key in allowed}

    if "background_color" in normalized:
        normalized["background_color"] = tuple(normalized["background_color"])

    return GameSettings(**normalized)


def save_settings(settings: GameSettings) -> None:
    ensure_runtime_dirs()
    SETTINGS_FILE.write_text(
        json.dumps(asdict(settings), indent=2),
        encoding="utf-8",
    )
