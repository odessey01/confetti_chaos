"""System-level modules."""

from .audio import AudioManager
from .game_session import GameSession
from .high_score import load_high_score, save_high_score
from .input_controller import InputController
from .paths import asset_path, assets_dir, project_root, runtime_root, saves_dir
from .settings import RuntimeSettings
from .spawn_controller import SpawnController
from .ui import UiRenderer
from .visual_feedback import VisualFeedback

__all__ = [
    "AudioManager",
    "GameSession",
    "InputController",
    "SpawnController",
    "RuntimeSettings",
    "UiRenderer",
    "VisualFeedback",
    "load_high_score",
    "save_high_score",
    "asset_path",
    "assets_dir",
    "project_root",
    "runtime_root",
    "saves_dir",
]
