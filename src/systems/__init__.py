"""System-level modules."""

from .audio import AudioManager
from .background import BackgroundRenderer
from .game_session import GameSession
from .high_score import load_high_score, save_high_score
from .input_controller import InputController
from .paths import asset_path, assets_dir, project_root, runtime_root, saves_dir
from .party_animals import (
    DEFAULT_PARTY_ANIMAL_ID,
    FUTURE_PARTY_ANIMAL_PLACEHOLDERS,
    PLAYABLE_PARTY_ANIMAL_IDS,
    PARTY_ANIMAL_CONFIGS,
    PARTY_ANIMAL_CONFIGS_BY_ID,
    PartyAnimalVisualConfig,
    SHARED_PARTY_ACCESSORY_RULES,
    draw_party_animal_shape,
    get_party_animal,
    list_party_animals,
    register_party_animal,
)
from .player_visual import PlayerRenderer
from .player_variants import PLAYER_VARIANTS, PLAYER_VARIANTS_BY_ID, PlayerVisualVariant
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
from .teddy_shape_variants import TEDDY_SHAPE_VARIANTS, TeddyShapeVariant, draw_teddy_shape_variant
from .ui import UiRenderer
from .visual_feedback import VisualFeedback

__all__ = [
    "AudioManager",
    "BackgroundRenderer",
    "GameSession",
    "InputController",
    "SpawnController",
    "PartyAnimalVisualConfig",
    "PARTY_ANIMAL_CONFIGS",
    "PARTY_ANIMAL_CONFIGS_BY_ID",
    "DEFAULT_PARTY_ANIMAL_ID",
    "SHARED_PARTY_ACCESSORY_RULES",
    "FUTURE_PARTY_ANIMAL_PLACEHOLDERS",
    "PLAYABLE_PARTY_ANIMAL_IDS",
    "register_party_animal",
    "list_party_animals",
    "get_party_animal",
    "draw_party_animal_shape",
    "TeddyShapeVariant",
    "TEDDY_SHAPE_VARIANTS",
    "draw_teddy_shape_variant",
    "RuntimeSettings",
    "PlayerRenderer",
    "PlayerVisualVariant",
    "PLAYER_VARIANTS",
    "PLAYER_VARIANTS_BY_ID",
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
