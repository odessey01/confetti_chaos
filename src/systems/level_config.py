"""Level configuration system for difficulty scaling."""

from __future__ import annotations

from dataclasses import dataclass

from .level_flavor import LevelFlavor, get_flavor_for_level, get_flavor_modifiers, HazardMix, get_hazard_mix


# Base configuration constants for Level 1
LEVEL_1_SPAWN_RATE = 0.5  # spawns per second
LEVEL_1_ENEMY_SPEED = 155.0  # pixels per second
LEVEL_1_MAX_ENEMIES = 3

# Peak configuration constants (Level 10+)
MAX_SPAWN_RATE = 2.0
MAX_ENEMY_SPEED = 265.0
MAX_ENEMIES = 12


@dataclass
class LevelConfig:
    """Configuration parameters for a specific level."""

    level: int
    spawn_rate: float
    enemy_speed: float
    max_simultaneous_enemies: int
    flavor: LevelFlavor
    hazard_mix: HazardMix

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.level < 1:
            raise ValueError("Level must be >= 1")
        if self.spawn_rate < 0:
            raise ValueError("spawn_rate must be >= 0")
        if self.enemy_speed < 0:
            raise ValueError("enemy_speed must be >= 0")
        if self.max_simultaneous_enemies < 1:
            raise ValueError("max_simultaneous_enemies must be >= 1")


def get_level_config(level: int) -> LevelConfig:
    """Compute and return level configuration for a given level.

    Scales parameters linearly from Level 1 baseline to peak at Level 10+.
    Applies flavor-based modifiers to add variety.

    Args:
        level: The level number (must be >= 1).

    Returns:
        LevelConfig with scaled and flavor-modified parameters for the given level.
    """
    if level < 1:
        raise ValueError("Level must be >= 1")

    # Determine flavor and get modifiers
    flavor = get_flavor_for_level(level)
    modifiers = get_flavor_modifiers(flavor)
    hazard_mix = get_hazard_mix(flavor)

    # Progress scaling: 0.0 at level 1, 1.0 at level 10+.
    # Use an easing curve that ramps enemy speed more gradually early on.
    linear_progress = min((level - 1) / 9.0, 1.0)
    progress = linear_progress ** 1.15

    # Linear interpolation for base parameters
    base_spawn_rate = LEVEL_1_SPAWN_RATE + (MAX_SPAWN_RATE - LEVEL_1_SPAWN_RATE) * progress
    base_enemy_speed = LEVEL_1_ENEMY_SPEED + (MAX_ENEMY_SPEED - LEVEL_1_ENEMY_SPEED) * progress
    base_max_enemies = int(
        LEVEL_1_MAX_ENEMIES + (MAX_ENEMIES - LEVEL_1_MAX_ENEMIES) * progress
    )

    # Apply flavor modifiers
    spawn_rate = base_spawn_rate * modifiers.spawn_rate_multiplier
    enemy_speed = base_enemy_speed * modifiers.enemy_speed_multiplier
    max_enemies = max(
        1,
        int(base_max_enemies * modifiers.max_enemies_multiplier),
    )

    return LevelConfig(
        level=level,
        spawn_rate=spawn_rate,
        enemy_speed=enemy_speed,
        max_simultaneous_enemies=max_enemies,
        flavor=flavor,
        hazard_mix=hazard_mix,
    )
