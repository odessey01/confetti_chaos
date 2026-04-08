"""Player rendering module decoupled from player movement/combat logic."""

from __future__ import annotations

import pygame

from player import Player
from .paths import asset_path
from .party_animals import draw_party_animal_shape, get_party_animal


class PlayerRenderer:
    """Draw the player using gameplay state exposed by Player."""

    def __init__(self) -> None:
        self._sprite_cache: dict[str, pygame.Surface | None] = {}

    def draw(
        self,
        surface: pygame.Surface,
        player: Player,
        *,
        show_shadow: bool = True,
        show_outline: bool = True,
    ) -> str:
        if getattr(player, "is_invulnerable", False):
            if (pygame.time.get_ticks() // 70) % 2 == 0:
                return "shape"
        variant = self._variant_for_player(player)
        sprite = self._sprite_for_variant(variant.sprite_asset_path) if variant.prefers_sprite else None
        if sprite is not None:
            self._draw_sprite(surface, player, sprite)
            return "sprite"
        draw_party_animal_shape(
            surface,
            player=player,
            config=variant,
            show_outline=show_outline,
            show_shadow=show_shadow,
        )
        return "shape"

    def _variant_for_player(self, player: Player):
        variant_id = str(getattr(player, "visual_variant_id", "teddy_f"))
        return get_party_animal(variant_id)

    def _draw_sprite(self, surface: pygame.Surface, player: Player, sprite: pygame.Surface) -> None:
        target_size = max(8, int(player.size))
        scaled = pygame.transform.smoothscale(sprite, (target_size, target_size))
        draw_rect = scaled.get_rect(center=player.rect.center)
        surface.blit(scaled, draw_rect)

    def _sprite_for_variant(self, sprite_asset_path: str | None) -> pygame.Surface | None:
        if not sprite_asset_path:
            return None
        cache_key = sprite_asset_path
        if cache_key in self._sprite_cache:
            return self._sprite_cache[cache_key]
        try:
            loaded = pygame.image.load(str(asset_path(*sprite_asset_path.split("/"))))
            self._sprite_cache[cache_key] = loaded
            return loaded
        except (pygame.error, FileNotFoundError, OSError):
            self._sprite_cache[cache_key] = None
            return None
