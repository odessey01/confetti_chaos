"""Asset registry for weapon-attached visuals."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from .paths import asset_path


@dataclass(frozen=True, slots=True)
class WeaponVisualAssetDefinition:
    """Describe a loadable sprite asset for a weapon visual overlay."""

    asset_id: str
    sprite_path: str
    pivot: tuple[int, int]

    def resolved_path(self) -> str:
        return str(asset_path(*self.sprite_path.split("/")))


WEAPON_VISUAL_ASSETS: dict[str, WeaponVisualAssetDefinition] = {
    "bottle_rocket_tier1": WeaponVisualAssetDefinition(
        asset_id="bottle_rocket_tier1",
        sprite_path="images/weapons/bottle_rocket/tier1.png",
        # Pivot is near the stick/body junction so the rocket mounts cleanly later.
        pivot=(18, 32),
    ),
}


def list_weapon_visual_assets() -> tuple[WeaponVisualAssetDefinition, ...]:
    return tuple(WEAPON_VISUAL_ASSETS.values())


def get_weapon_visual_asset(asset_id: str) -> WeaponVisualAssetDefinition | None:
    return WEAPON_VISUAL_ASSETS.get(str(asset_id))


def load_weapon_visual_asset(asset_id: str) -> pygame.Surface | None:
    definition = get_weapon_visual_asset(asset_id)
    if definition is None:
        return None
    try:
        return pygame.image.load(definition.resolved_path())
    except (pygame.error, FileNotFoundError, OSError):
        return None
