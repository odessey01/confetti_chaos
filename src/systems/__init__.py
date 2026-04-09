"""System-level modules."""

from .audio import AudioManager
from .aim_assist import AimAssistConfig, AimAssistSystem, AimAssistTarget
from .background import BackgroundRenderer
from .character_passives import (
    CHARACTER_PASSIVE_PROFILES,
    DEFAULT_CHARACTER_PASSIVE_ID,
    CharacterPassiveProfile,
    get_character_passive,
)
from .character_supers import (
    CHARACTER_SUPER_PROFILES,
    DEFAULT_CHARACTER_SUPER_ID,
    CharacterSuperProfile,
    get_character_super,
)
from .game_session import GameSession
from .high_score import load_high_score, save_high_score
from .input_controller import InputController, InputMethod
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
from .player_animation import (
    CHARACTER_ANIMATION_CONFIGS,
    DEFAULT_CHARACTER_ANIMATION_ID,
    AnimationClipConfig,
    CharacterAnimationConfig,
    LoadedAnimationClip,
    LoadedCharacterAnimation,
    PlayerAnimationSystem,
    get_character_animation_config,
    load_character_animation,
    list_character_animation_configs,
    register_character_animation_config,
)
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
from .weapons import (
    DEFAULT_WEAPON_ID,
    WEAPON_DEFINITIONS,
    WEAPON_TYPE_MELEE,
    WEAPON_TYPE_PROJECTILE,
    SparklerAttackProfile,
    WeaponDefinition,
    get_weapon_definition,
    list_weapon_definitions,
)

__all__ = [
    "AudioManager",
    "AimAssistConfig",
    "AimAssistSystem",
    "AimAssistTarget",
    "BackgroundRenderer",
    "CharacterPassiveProfile",
    "CHARACTER_PASSIVE_PROFILES",
    "DEFAULT_CHARACTER_PASSIVE_ID",
    "get_character_passive",
    "CharacterSuperProfile",
    "CHARACTER_SUPER_PROFILES",
    "DEFAULT_CHARACTER_SUPER_ID",
    "get_character_super",
    "GameSession",
    "InputController",
    "InputMethod",
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
    "AnimationClipConfig",
    "CharacterAnimationConfig",
    "LoadedAnimationClip",
    "LoadedCharacterAnimation",
    "PlayerAnimationSystem",
    "CHARACTER_ANIMATION_CONFIGS",
    "DEFAULT_CHARACTER_ANIMATION_ID",
    "register_character_animation_config",
    "get_character_animation_config",
    "list_character_animation_configs",
    "load_character_animation",
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
    "WeaponDefinition",
    "SparklerAttackProfile",
    "WEAPON_TYPE_PROJECTILE",
    "WEAPON_TYPE_MELEE",
    "WEAPON_DEFINITIONS",
    "DEFAULT_WEAPON_ID",
    "get_weapon_definition",
    "list_weapon_definitions",
]
