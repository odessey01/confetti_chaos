"""Weapon definition registry and lookup helpers."""

from __future__ import annotations

from dataclasses import dataclass


WEAPON_TYPE_PROJECTILE = "projectile"
WEAPON_TYPE_MELEE = "melee"


@dataclass(frozen=True)
class WeaponDefinition:
    weapon_id: str
    display_name: str
    weapon_type: str
    base_damage: int
    effective_range: float
    attack_cooldown_seconds: float
    travel_speed: float = 0.0
    return_speed: float = 0.0
    active_cap: int = 1
    per_enemy_hit_cooldown: float = 0.2
    hover_pause_seconds: float = 0.0


@dataclass(frozen=True)
class SparklerAttackProfile:
    damage_bonus: int = 0
    range_bonus: float = 0.0
    cone_bonus_degrees: float = 0.0
    cooldown_multiplier: float = 1.0
    spark_projectile_count: int = 0
    aura_radius: float = 0.0


DEFAULT_WEAPON_ID = "bottle_rocket"

WEAPON_DEFINITIONS: dict[str, WeaponDefinition] = {
    "bottle_rocket": WeaponDefinition(
        weapon_id="bottle_rocket",
        display_name="Bottle Rocket",
        weapon_type=WEAPON_TYPE_PROJECTILE,
        base_damage=1,
        effective_range=1120.0,
        attack_cooldown_seconds=0.18,
    ),
    "sparkler": WeaponDefinition(
        weapon_id="sparkler",
        display_name="Sparkler",
        weapon_type=WEAPON_TYPE_MELEE,
        base_damage=2,
        effective_range=128.0,
        attack_cooldown_seconds=0.22,
    ),
    "yoyo": WeaponDefinition(
        weapon_id="yoyo",
        display_name="Yo-Yo",
        weapon_type=WEAPON_TYPE_PROJECTILE,
        base_damage=2,
        effective_range=205.0,
        attack_cooldown_seconds=0.36,
        travel_speed=500.0,
        return_speed=650.0,
        active_cap=1,
        per_enemy_hit_cooldown=0.24,
        hover_pause_seconds=0.03,
    ),
    "bubble_wand": WeaponDefinition(
        weapon_id="bubble_wand",
        display_name="Bubble Wand",
        weapon_type=WEAPON_TYPE_PROJECTILE,
        base_damage=1,
        effective_range=520.0,
        attack_cooldown_seconds=0.42,
        travel_speed=180.0,
        active_cap=4,
    ),
    "kazoo_beam": WeaponDefinition(
        weapon_id="kazoo_beam",
        display_name="Kazoo Beam",
        weapon_type=WEAPON_TYPE_PROJECTILE,
        base_damage=1,
        effective_range=360.0,
        attack_cooldown_seconds=0.62,
        travel_speed=0.0,
        active_cap=999,
    ),
}


def get_weapon_definition(weapon_id: str | None) -> WeaponDefinition:
    key = str(weapon_id or DEFAULT_WEAPON_ID)
    return WEAPON_DEFINITIONS.get(key, WEAPON_DEFINITIONS[DEFAULT_WEAPON_ID])


def list_weapon_definitions() -> tuple[WeaponDefinition, ...]:
    return tuple(WEAPON_DEFINITIONS.values())
