"""Level Flavor System - Provides variety to difficulty progression."""

from dataclasses import dataclass
from enum import Enum, auto


class LevelFlavor(Enum):
    """Flavor profiles that modify difficulty curve characteristics."""
    STANDARD = auto()  # Baseline difficulty progression
    SWARM = auto()     # High spawn rate, slower enemies, more simultaneous
    HUNTERS = auto()   # Low spawn rate, faster enemies, fewer simultaneous
    STORM = auto()     # Burst mode - rapid spawn peaks followed by calm periods


@dataclass
class FlavorModifiers:
    """Multipliers applied to level config based on flavor."""
    spawn_rate_multiplier: float = 1.0
    enemy_speed_multiplier: float = 1.0
    max_enemies_multiplier: float = 1.0


@dataclass
class HazardMix:
    """Specifies the probability distribution of hazard types."""
    tracking_hazard_chance: float = 0.5  # Probability of spawning a tracking hazard
    balloon_enemy_chance: float = 0.5    # Probability of spawning a balloon


def get_flavor_modifiers(flavor: LevelFlavor) -> FlavorModifiers:
    """Return multiplier modifiers for a given flavor."""
    modifiers = {
        LevelFlavor.STANDARD: FlavorModifiers(
            spawn_rate_multiplier=1.0,
            enemy_speed_multiplier=1.0,
            max_enemies_multiplier=1.0,
        ),
        LevelFlavor.SWARM: FlavorModifiers(
            spawn_rate_multiplier=1.5,
            enemy_speed_multiplier=0.8,
            max_enemies_multiplier=1.3,
        ),
        LevelFlavor.HUNTERS: FlavorModifiers(
            spawn_rate_multiplier=0.7,
            enemy_speed_multiplier=1.15,  # Reduced from 1.3
            max_enemies_multiplier=0.6,
        ),
        LevelFlavor.STORM: FlavorModifiers(
            spawn_rate_multiplier=1.2,
            enemy_speed_multiplier=1.0,
            max_enemies_multiplier=1.0,
        ),
    }
    return modifiers[flavor]


def get_hazard_mix(flavor: LevelFlavor) -> HazardMix:
    """Return hazard type distribution for a given flavor."""
    mixes = {
        LevelFlavor.STANDARD: HazardMix(
            tracking_hazard_chance=0.5,
            balloon_enemy_chance=0.5,
        ),
        LevelFlavor.SWARM: HazardMix(
            tracking_hazard_chance=0.2,
            balloon_enemy_chance=0.8,
        ),
        LevelFlavor.HUNTERS: HazardMix(
            tracking_hazard_chance=0.6,
            balloon_enemy_chance=0.4,
        ),
        LevelFlavor.STORM: HazardMix(
            tracking_hazard_chance=0.5,
            balloon_enemy_chance=0.5,
        ),
    }
    return mixes[flavor]


def get_flavor_for_level(level: int) -> LevelFlavor:
    """Return flavor using 3-level cycle pattern."""
    flavors = [
        LevelFlavor.STANDARD,
        LevelFlavor.SWARM,
        LevelFlavor.HUNTERS,
    ]
    # Storm appears every 12 levels (at levels 12, 24, 36, etc.)
    if level > 0 and level % 12 == 0:
        return LevelFlavor.STORM
    # Cycle through Standard, Swarm, Hunters in repeating pattern
    return flavors[(level - 1) % 3]
