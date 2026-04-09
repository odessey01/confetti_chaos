"""Character-specific super ability definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterSuperProfile:
    character_id: str
    super_id: str
    super_name: str
    max_charge: int
    activation_behavior: str


DEFAULT_CHARACTER_SUPER_ID = "teddy_f"

CHARACTER_SUPER_PROFILES: dict[str, CharacterSuperProfile] = {
    "teddy_f": CharacterSuperProfile(
        character_id="teddy_f",
        super_id="bear_roar",
        super_name="Roar",
        max_charge=100,
        activation_behavior="radial_knockback",
    ),
    "bunny_f": CharacterSuperProfile(
        character_id="bunny_f",
        super_id="bunny_mega_hop",
        super_name="Mega Hop",
        max_charge=100,
        activation_behavior="long_dodge_impact",
    ),
    "cat_f": CharacterSuperProfile(
        character_id="cat_f",
        super_id="cat_frenzy",
        super_name="Frenzy",
        max_charge=100,
        activation_behavior="offense_burst",
    ),
    "fox_f": CharacterSuperProfile(
        character_id="fox_f",
        super_id="raccoon_chaos_drop",
        super_name="Chaos Drop",
        max_charge=100,
        activation_behavior="reward_control_pulse",
    ),
}


def get_character_super(character_id: str | None) -> CharacterSuperProfile:
    key = str(character_id or DEFAULT_CHARACTER_SUPER_ID)
    return CHARACTER_SUPER_PROFILES.get(key, CHARACTER_SUPER_PROFILES[DEFAULT_CHARACTER_SUPER_ID])
