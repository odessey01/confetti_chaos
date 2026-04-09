"""Reusable teddy-bear sprite demo config and directional rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from .paths import asset_path


@dataclass(frozen=True)
class DirectionalSpritePaths:
    front: str
    side: str
    rear: str


@dataclass(frozen=True)
class DemoSpriteConfig:
    variant_id: str
    sprite_paths: DirectionalSpritePaths
    canvas_size: tuple[int, int]
    base_display_scale: float
    anchor_offset: tuple[int, int]
    hitbox_radius: float
    hitbox_vertical_offset: float


@dataclass(frozen=True)
class AnimatedSpriteSheetConfig:
    sprite_sheet_path: str
    rows: int
    columns: int
    loop_mode: str
    frame_order: str
    direction_to_row: dict[str, int]
    direction_flip: dict[str, bool]
    base_display_scale: float
    anchor_offset: tuple[int, int]
    hitbox_radius: float
    hitbox_vertical_offset: float
    animation_fps: float
    extraction_mode: str = "grid"
    bbox_guide_path: str | None = None


TEDDY_BEAR_DEMO_CONFIG = DemoSpriteConfig(
    variant_id="bear",
    sprite_paths=DirectionalSpritePaths(
        front="images/player/bear/front.png",
        side="images/player/bear/side.png",
        rear="images/player/bear/rear.png",
    ),
    canvas_size=(96, 96),
    base_display_scale=1.0,
    anchor_offset=(0, 0),
    hitbox_radius=20.0,
    hitbox_vertical_offset=22.0,
)


BEAR_WALKING_ANIMATION_CONFIG = AnimatedSpriteSheetConfig(
    sprite_sheet_path="images/player/bear/bbox_bear_walking.png",
    rows=5,
    columns=4,
    extraction_mode="bbox_guide",
    bbox_guide_path="images/player/bear/bbox_bear_walking.png",
    loop_mode="full_sheet_loop",
    frame_order="row_major",
    direction_to_row={
        "down": 0,
        "right": 1,
        "up": 2,
        "left": 1,
    },
    direction_flip={
        "down": False,
        "right": False,
        "up": False,
        "left": True,
    },
    base_display_scale=0.95,
    anchor_offset=(0, 0),
    hitbox_radius=18.0,
    hitbox_vertical_offset=20.0,
    animation_fps=8.0,
)


BEAR_IDLE_ANIMATION_CONFIG = AnimatedSpriteSheetConfig(
    sprite_sheet_path="images/player/bear/bbox_bear_idle.png",
    rows=5,
    columns=4,
    extraction_mode="bbox_guide",
    bbox_guide_path="images/player/bear/bbox_bear_idle.png",
    loop_mode="full_sheet_loop",
    frame_order="row_major",
    direction_to_row={
        "down": 0,
        "right": 1,
        "up": 2,
        "left": 1,
    },
    direction_flip={
        "down": False,
        "right": False,
        "up": False,
        "left": True,
    },
    base_display_scale=0.95,
    anchor_offset=(0, 0),
    hitbox_radius=18.0,
    hitbox_vertical_offset=20.0,
    animation_fps=5.0,
)


def load_directional_sprites(
    paths: DirectionalSpritePaths,
) -> dict[str, pygame.Surface | None]:
    return {
        "front": _safe_load(paths.front),
        "side": _safe_load(paths.side),
        "rear": _safe_load(paths.rear),
    }


def normalize_directional_sprites(
    sprites: dict[str, pygame.Surface | None],
    *,
    canvas_size: tuple[int, int],
) -> dict[str, pygame.Surface | None]:
    normalized: dict[str, pygame.Surface | None] = {}
    for key, sprite in sprites.items():
        if sprite is None:
            normalized[key] = None
            continue
        normalized[key] = _normalize_to_canvas(sprite, canvas_size)
    return normalized


def direction_to_sprite_mapping(
    facing: pygame.Vector2,
) -> tuple[str, bool]:
    """Return sprite key and whether side sprite should be flipped."""
    if abs(facing.x) > abs(facing.y):
        return "side", facing.x < 0.0
    if facing.y < 0.0:
        return "rear", False
    return "front", False


def rect_from_center_bottom_anchor(
    *,
    anchor: tuple[float, float],
    sprite_size: tuple[int, int],
    offset: tuple[int, int],
) -> pygame.Rect:
    rect = pygame.Rect(0, 0, int(sprite_size[0]), int(sprite_size[1]))
    rect.midbottom = (
        int(anchor[0] + offset[0]),
        int(anchor[1] + offset[1]),
    )
    return rect


def hitbox_from_anchor(
    *,
    anchor: tuple[float, float],
    radius: float,
    vertical_offset: float,
) -> tuple[pygame.Vector2, float]:
    center = pygame.Vector2(anchor[0], anchor[1] - vertical_offset)
    return center, max(4.0, float(radius))


def _safe_load(path_value: str) -> pygame.Surface | None:
    try:
        return pygame.image.load(str(asset_path(*path_value.split("/"))))
    except (pygame.error, FileNotFoundError, OSError):
        return None


def _normalize_to_canvas(
    sprite: pygame.Surface,
    canvas_size: tuple[int, int],
) -> pygame.Surface:
    canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)
    target_rect = sprite.get_rect()
    target_rect.midbottom = (canvas_size[0] // 2, canvas_size[1] - 1)
    canvas.blit(sprite, target_rect)
    return canvas
