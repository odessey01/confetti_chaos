"""Shared party-animal visual registry and shape rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from player import Player
from .teddy_shape_variants import (
    SHARED_PLUSH_ACCESSORY_RULES,
    SOFTER_PLUSH_DELUXE_VARIANT_IDS,
    TEDDY_SHAPE_VARIANTS,
    TeddyShapeVariant,
    draw_teddy_shape_variant,
)


@dataclass(frozen=True)
class PartyAnimalVisualConfig:
    variant_id: str
    display_name: str
    animal_name: str
    shape_profile: str
    color_palette_hint: str
    ear_trait: str
    accessory_trait: str
    outline_color: tuple[int, int, int]
    body_proportions: tuple[float, float]
    render_offset: tuple[int, int]
    source_variant_id: str
    sprite_asset_path: str | None = None
    prefers_sprite: bool = False


_TEDDY_VARIANTS_BY_ID: dict[str, TeddyShapeVariant] = {
    variant.variant_id: variant for variant in TEDDY_SHAPE_VARIANTS
}

DEFAULT_PARTY_ANIMAL_ID = "teddy_f"
FUTURE_PARTY_ANIMAL_PLACEHOLDERS: tuple[str, ...] = ("bunny", "fox", "cat")
PLAYABLE_PARTY_ANIMAL_IDS: tuple[str, ...] = ("teddy_f", "bunny_f", "fox_f", "cat_f")

_PARTY_ANIMAL_REGISTRY: dict[str, PartyAnimalVisualConfig] = {}


def _config_from_teddy_variant(variant: TeddyShapeVariant) -> PartyAnimalVisualConfig:
    display_name = variant.animal_type.title()
    return PartyAnimalVisualConfig(
        variant_id=variant.variant_id,
        display_name=display_name,
        animal_name=variant.animal_type,
        shape_profile=variant.silhouette_type,
        color_palette_hint=variant.proportion_style,
        ear_trait=variant.ear_type,
        accessory_trait=variant.accessory_style,
        outline_color=(250, 245, 234),
        body_proportions=(variant.body_width_scale, variant.body_height_scale),
        render_offset=(0, 0),
        source_variant_id=variant.variant_id,
        sprite_asset_path=None,
        prefers_sprite=False,
    )


def register_party_animal(config: PartyAnimalVisualConfig) -> None:
    _PARTY_ANIMAL_REGISTRY[config.variant_id] = config


def list_party_animals() -> tuple[PartyAnimalVisualConfig, ...]:
    return tuple(_PARTY_ANIMAL_REGISTRY.values())


def get_party_animal(variant_id: str | None) -> PartyAnimalVisualConfig:
    key = str(variant_id or DEFAULT_PARTY_ANIMAL_ID)
    return _PARTY_ANIMAL_REGISTRY.get(key, _PARTY_ANIMAL_REGISTRY[DEFAULT_PARTY_ANIMAL_ID])


def draw_party_animal_shape(
    surface: pygame.Surface,
    *,
    player: Player,
    config: PartyAnimalVisualConfig,
    show_outline: bool,
    show_shadow: bool,
) -> None:
    source_variant = _TEDDY_VARIANTS_BY_ID.get(
        config.source_variant_id,
        _TEDDY_VARIANTS_BY_ID[DEFAULT_PARTY_ANIMAL_ID],
    )
    anchor = (player.rect.centerx, player.rect.bottom)
    draw_teddy_shape_variant(
        surface,
        player=player,
        variant=source_variant,
        anchor=anchor,
        offset=config.render_offset,
        show_outline=show_outline,
        show_shadow=show_shadow,
    )


for variant_id in SOFTER_PLUSH_DELUXE_VARIANT_IDS:
    source = _TEDDY_VARIANTS_BY_ID.get(variant_id)
    if source is not None:
        register_party_animal(_config_from_teddy_variant(source))


SHARED_PARTY_ACCESSORY_RULES = dict(SHARED_PLUSH_ACCESSORY_RULES)
PARTY_ANIMAL_CONFIGS = tuple(_PARTY_ANIMAL_REGISTRY.values())
PARTY_ANIMAL_CONFIGS_BY_ID = dict(_PARTY_ANIMAL_REGISTRY)
