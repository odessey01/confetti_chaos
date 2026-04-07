"""System-level modules."""

from .audio import AudioManager
from .background import BackgroundRenderer
from .game_session import GameSession
from .high_score import load_high_score, save_high_score
from .input_controller import InputController
from .paths import asset_path, assets_dir, project_root, runtime_root, saves_dir
from .run_progression import RunProgression
from .run_upgrades import RunUpgradeSystem, UpgradeDefinition
from .settings import (
    MAX_START_LEVEL,
    MIN_START_LEVEL,
    RuntimeSettings,
    clamp_selected_start_level,
    load_settings,
    save_settings,
)
from .spawn_controller import SpawnController
from .ui import UiRenderer
from .visual_feedback import VisualFeedback

__all__ = [
    "AudioManager",
    "BackgroundRenderer",
    "GameSession",
    "InputController",
    "SpawnController",
    "RuntimeSettings",
    "clamp_selected_start_level",
    "MIN_START_LEVEL",
    "MAX_START_LEVEL",
    "load_settings",
    "save_settings",
    "UiRenderer",
    "VisualFeedback",
    "load_high_score",
    "save_high_score",
    "asset_path",
    "assets_dir",
    "project_root",
    "runtime_root",
    "saves_dir",
    "RunProgression",
    "RunUpgradeSystem",
    "UpgradeDefinition",
]
