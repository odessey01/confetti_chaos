from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json

from confetti_chaos.settings import SAVE_FILE, ensure_runtime_dirs


@dataclass(slots=True)
class SaveData:
    player_name: str = "Player One"
    total_score: int = 0
    best_combo: int = 0
    unlocked_levels: list[str] = field(default_factory=lambda: ["meadow-pop"])
    last_scene: str = "title"


def load_save() -> SaveData:
    ensure_runtime_dirs()
    if not SAVE_FILE.exists():
        data = SaveData()
        save_game(data)
        return data

    raw_data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
    return SaveData(**raw_data)


def save_game(data: SaveData) -> None:
    ensure_runtime_dirs()
    SAVE_FILE.write_text(
        json.dumps(asdict(data), indent=2),
        encoding="utf-8",
    )
