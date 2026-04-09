"""Character passive definitions and lookup helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterPassiveProfile:
    character_id: str
    display_name: str
    passive_bonus: str
    passive_drawback: str
    max_health_bonus: int = 0
    move_speed_mult: float = 0.0
    outgoing_damage_bonus: int = 0
    incoming_damage_mult: float = 1.0
    xp_gain_mult: float = 0.0
    pickup_radius_bonus: float = 0.0
    xp_magnet_mult: float = 0.0


DEFAULT_CHARACTER_PASSIVE_ID = "teddy_f"

CHARACTER_PASSIVE_PROFILES: dict[str, CharacterPassiveProfile] = {
    "teddy_f": CharacterPassiveProfile(
        character_id="teddy_f",
        display_name="Bear",
        passive_bonus="+1 max health",
        passive_drawback="-12% movement speed",
        max_health_bonus=1,
        move_speed_mult=-0.12,
    ),
    "bunny_f": CharacterPassiveProfile(
        character_id="bunny_f",
        display_name="Bunny",
        passive_bonus="+16% movement speed",
        passive_drawback="-1 max health",
        max_health_bonus=-1,
        move_speed_mult=0.16,
    ),
    "cat_f": CharacterPassiveProfile(
        character_id="cat_f",
        display_name="Cat",
        passive_bonus="+1 projectile damage",
        passive_drawback="+100% damage taken",
        outgoing_damage_bonus=1,
        incoming_damage_mult=2.0,
    ),
    "fox_f": CharacterPassiveProfile(
        character_id="fox_f",
        display_name="Raccoon",
        passive_bonus="+35% XP gain, wider pickup",
        passive_drawback="-1 projectile damage",
        outgoing_damage_bonus=-1,
        xp_gain_mult=0.35,
        pickup_radius_bonus=10.0,
        xp_magnet_mult=0.15,
    ),
}


def get_character_passive(character_id: str | None) -> CharacterPassiveProfile:
    key = str(character_id or DEFAULT_CHARACTER_PASSIVE_ID)
    return CHARACTER_PASSIVE_PROFILES.get(
        key,
        CHARACTER_PASSIVE_PROFILES[DEFAULT_CHARACTER_PASSIVE_ID],
    )
