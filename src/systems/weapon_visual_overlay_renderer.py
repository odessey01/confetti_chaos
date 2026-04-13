"""Renderer for player-attached weapon visual overlays."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from player import Player

from .paths import asset_path
from .player_visual_anchors import resolve_player_visual_anchor
from .weapon_visual_overlays import WeaponVisualOverlay


@dataclass(frozen=True, slots=True)
class WeaponVisualOverlayDebugInfo:
    overlay_id: str
    anchor_point: tuple[int, int]
    pivot_point: tuple[int, int]
    draw_rect: pygame.Rect


class WeaponVisualOverlayRenderer:
    """Draw generic weapon visual overlays anchored to the player."""

    def __init__(self) -> None:
        self._sprite_cache: dict[str, pygame.Surface | None] = {}

    def draw_overlay(
        self,
        surface: pygame.Surface,
        player: Player,
        overlay: WeaponVisualOverlay,
    ) -> None:
        prepared = self._prepare_overlay(player, overlay)
        if prepared is None:
            return
        transformed, draw_rect, _anchor = prepared
        surface.blit(transformed, draw_rect)

    def debug_info_for_overlay(
        self,
        player: Player,
        overlay: WeaponVisualOverlay,
    ) -> WeaponVisualOverlayDebugInfo | None:
        prepared = self._prepare_overlay(player, overlay)
        if prepared is None:
            return None
        _surface, draw_rect, anchor = prepared
        return WeaponVisualOverlayDebugInfo(
            overlay_id=overlay.overlay_id,
            anchor_point=anchor,
            pivot_point=draw_rect.center,
            draw_rect=draw_rect,
        )

    def clear_cache(self) -> None:
        self._sprite_cache.clear()

    def _load_sprite(self, sprite_path: str) -> pygame.Surface | None:
        cached = self._sprite_cache.get(sprite_path)
        if sprite_path in self._sprite_cache:
            return cached
        try:
            loaded = pygame.image.load(str(asset_path(*sprite_path.split("/"))))
            self._sprite_cache[sprite_path] = loaded
            return loaded
        except (pygame.error, FileNotFoundError, OSError):
            self._sprite_cache[sprite_path] = None
            return None

    def _prepare_overlay(
        self,
        player: Player,
        overlay: WeaponVisualOverlay,
    ) -> tuple[pygame.Surface, pygame.Rect, tuple[int, int]] | None:
        if not overlay.visible:
            return None
        source = self._load_sprite(overlay.sprite_path)
        if source is None:
            return None
        if overlay.flip_x or overlay.flip_y:
            source = pygame.transform.flip(source, overlay.flip_x, overlay.flip_y)
        scale = max(0.05, float(overlay.scale))
        target_size = (
            max(1, int(round(source.get_width() * scale))),
            max(1, int(round(source.get_height() * scale))),
        )
        transformed = pygame.transform.smoothscale(source, target_size)
        if abs(float(overlay.rotation_degrees)) > 0.01:
            transformed = pygame.transform.rotate(transformed, float(overlay.rotation_degrees))
        anchor_x, anchor_y = resolve_player_visual_anchor(player, overlay.anchor_name)
        draw_rect = transformed.get_rect(
            center=(
                int(round(anchor_x + overlay.offset_x)),
                int(round(anchor_y + overlay.offset_y)),
            )
        )
        return transformed, draw_rect, (anchor_x, anchor_y)
