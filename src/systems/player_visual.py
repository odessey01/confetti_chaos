"""Player rendering module decoupled from player movement/combat logic."""

from __future__ import annotations

import pygame

from player import Player
from .paths import asset_path
from .party_animals import draw_party_animal_shape, get_party_animal


class PlayerRenderer:
    """Draw the player using gameplay state exposed by Player."""

    VISUAL_SCALE_BY_VARIANT: dict[str, float] = {
        "bunny_f": 0.5,
    }

    def __init__(self) -> None:
        self._sprite_cache: dict[str, pygame.Surface | None] = {}

    def draw(
        self,
        surface: pygame.Surface,
        player: Player,
        *,
        animation_frame: pygame.Surface | None = None,
        animation_rect: pygame.Rect | None = None,
        animation_flip_x: bool = False,
        show_shadow: bool = True,
        show_outline: bool = True,
        show_direction_indicator: bool = True,
    ) -> str:
        if getattr(player, "is_invulnerable", False):
            if (pygame.time.get_ticks() // 70) % 2 == 0:
                if show_direction_indicator:
                    self._draw_direction_indicator(surface, player)
                return "shape"
        if animation_frame is not None and animation_rect is not None:
            self._draw_animation_frame(
                surface,
                animation_frame,
                animation_rect,
                flip_x=animation_flip_x,
            )
            if show_direction_indicator:
                self._draw_direction_indicator(surface, player)
            return "animated"
        variant = self._variant_for_player(player)
        sprite = self._sprite_for_variant(variant.sprite_asset_path) if variant.prefers_sprite else None
        if sprite is not None:
            self._draw_sprite(surface, player, sprite)
            if show_direction_indicator:
                self._draw_direction_indicator(surface, player)
            return "sprite"
        draw_party_animal_shape(
            surface,
            player=player,
            config=variant,
            show_outline=show_outline,
            show_shadow=show_shadow,
        )
        if show_direction_indicator:
            self._draw_direction_indicator(surface, player)
        return "shape"

    def _variant_for_player(self, player: Player):
        variant_id = str(getattr(player, "visual_variant_id", "teddy_f"))
        return get_party_animal(variant_id)

    def _draw_sprite(self, surface: pygame.Surface, player: Player, sprite: pygame.Surface) -> None:
        target_size = max(8, int(round(float(player.size) * self._visual_scale_for_player(player))))
        scaled = pygame.transform.smoothscale(sprite, (target_size, target_size))
        draw_rect = scaled.get_rect(center=player.rect.center)
        surface.blit(scaled, draw_rect)

    def _draw_animation_frame(
        self,
        surface: pygame.Surface,
        frame: pygame.Surface,
        target_rect: pygame.Rect,
        *,
        flip_x: bool,
    ) -> None:
        source = pygame.transform.flip(frame, True, False) if flip_x else frame
        scaled = pygame.transform.smoothscale(source, target_rect.size)
        surface.blit(scaled, target_rect)

    def _visual_scale_for_player(self, player: Player) -> float:
        variant_id = str(getattr(player, "visual_variant_id", "teddy_f"))
        return max(0.1, float(self.VISUAL_SCALE_BY_VARIANT.get(variant_id, 1.0)))

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

    def _draw_direction_indicator(self, surface: pygame.Surface, player: Player) -> None:
        facing = pygame.Vector2(getattr(player, "facing", pygame.Vector2(1, 0)))
        if facing.length_squared() <= 0.0:
            facing = pygame.Vector2(1, 0)
        else:
            facing = facing.normalize()

        center = pygame.Vector2(player.rect.center)
        length = max(18.0, float(player.size) * 0.42)
        tip = center + (facing * length)
        base = center + (facing * max(8.0, length * 0.25))
        side = pygame.Vector2(-facing.y, facing.x)
        wing = max(4.0, float(player.size) * 0.08)
        left = base + (side * wing)
        right = base - (side * wing)

        # High-contrast marker: dark outline under bright fill for readability.
        pygame.draw.line(surface, (20, 24, 30), center, tip, width=4)
        pygame.draw.polygon(
            surface,
            (20, 24, 30),
            [(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))],
        )
        pygame.draw.line(surface, (255, 246, 110), center, tip, width=2)
        pygame.draw.polygon(
            surface,
            (255, 246, 110),
            [(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))],
        )
