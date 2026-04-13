"""Reusable player animation system for main-game runtime state and frame selection."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Callable

import pygame

from .paths import asset_path


@dataclass(frozen=True)
class AnimationClipConfig:
    sheet_path: str
    rows: int
    columns: int
    fps: float
    frame_order: str = "row_major"
    loop_mode: str = "loop"
    extraction_mode: str = "grid"
    bbox_guide_path: str | None = None
    frame_rects_path: str | None = None


@dataclass(frozen=True)
class CharacterAnimationConfig:
    character_id: str
    idle: AnimationClipConfig
    walk: AnimationClipConfig
    base_display_scale: float = 1.0
    anchor_offset: tuple[int, int] = (0, 0)
    hitbox_radius: float = 18.0
    hitbox_vertical_offset: float = 20.0
    flip_left: bool = True


@dataclass(frozen=True)
class LoadedAnimationClip:
    frames: tuple[pygame.Surface, ...]
    fps: float
    available: bool


@dataclass(frozen=True)
class LoadedCharacterAnimation:
    character_id: str
    idle: LoadedAnimationClip
    walk: LoadedAnimationClip
    base_display_scale: float
    anchor_offset: tuple[int, int]
    hitbox_radius: float
    hitbox_vertical_offset: float
    flip_left: bool


def _default_bear_clip(path: str, *, fps: float) -> AnimationClipConfig:
    cache_path = path.replace(".png", ".frames.json")
    return AnimationClipConfig(
        sheet_path=path,
        rows=5,
        columns=4,
        fps=fps,
        frame_order="row_major",
        loop_mode="loop",
        extraction_mode="bbox_guide",
        bbox_guide_path=path,
        frame_rects_path=cache_path,
    )


CHARACTER_ANIMATION_CONFIGS: dict[str, CharacterAnimationConfig] = {
    "teddy_f": CharacterAnimationConfig(
        character_id="teddy_f",
        idle=_default_bear_clip("images/player/bear/bbox_bear_idle.png", fps=5.0),
        walk=_default_bear_clip("images/player/bear/bbox_bear_walking.png", fps=8.0),
        base_display_scale=0.475,
        anchor_offset=(0, 0),
        hitbox_radius=18.0,
        hitbox_vertical_offset=20.0,
        flip_left=True,
    ),
    "bunny_f": CharacterAnimationConfig(
        character_id="bunny_f",
        idle=_default_bear_clip("images/player/bear/bbox_bear_idle.png", fps=5.0),
        walk=_default_bear_clip("images/player/bear/bbox_bear_walking.png", fps=8.0),
        base_display_scale=0.2375,
    ),
    "fox_f": CharacterAnimationConfig(
        character_id="fox_f",
        idle=_default_bear_clip("images/player/bear/bbox_bear_idle.png", fps=5.0),
        walk=_default_bear_clip("images/player/bear/bbox_bear_walking.png", fps=8.0),
    ),
    "cat_f": CharacterAnimationConfig(
        character_id="cat_f",
        idle=_default_bear_clip("images/player/bear/bbox_bear_idle.png", fps=5.0),
        walk=_default_bear_clip("images/player/bear/bbox_bear_walking.png", fps=8.0),
    ),
}

DEFAULT_CHARACTER_ANIMATION_ID = "teddy_f"
ANIMATION_PLAYBACK_SPEED_MULTIPLIER = 2.0

_CHARACTER_ANIMATION_REGISTRY: dict[str, CharacterAnimationConfig] = dict(CHARACTER_ANIMATION_CONFIGS)


def register_character_animation_config(config: CharacterAnimationConfig) -> None:
    _CHARACTER_ANIMATION_REGISTRY[config.character_id] = config


def get_character_animation_config(character_id: str) -> CharacterAnimationConfig:
    selected = _CHARACTER_ANIMATION_REGISTRY.get(str(character_id))
    if selected is not None:
        return selected
    return _CHARACTER_ANIMATION_REGISTRY[DEFAULT_CHARACTER_ANIMATION_ID]


def list_character_animation_configs() -> tuple[CharacterAnimationConfig, ...]:
    return tuple(_CHARACTER_ANIMATION_REGISTRY.values())


def _safe_load_sheet(path_value: str) -> pygame.Surface | None:
    try:
        loaded = pygame.image.load(str(asset_path(*path_value.split("/"))))
        try:
            return loaded.convert_alpha()
        except pygame.error:
            return loaded.copy()
    except (pygame.error, FileNotFoundError, OSError):
        return None


def _resolve_data_path(path_value: str) -> Path:
    maybe_absolute = Path(path_value)
    if maybe_absolute.is_absolute():
        return maybe_absolute
    return asset_path(*path_value.split("/"))


def _extract_frames(sheet: pygame.Surface, *, rows: int, columns: int) -> tuple[pygame.Surface, ...]:
    safe_rows = max(1, int(rows))
    safe_columns = max(1, int(columns))
    frame_width = sheet.get_width() // safe_columns
    frame_height = sheet.get_height() // safe_rows
    if frame_width <= 0 or frame_height <= 0:
        return ()
    frames: list[pygame.Surface] = []
    for row in range(safe_rows):
        for column in range(safe_columns):
            rect = pygame.Rect(column * frame_width, row * frame_height, frame_width, frame_height)
            frames.append(sheet.subsurface(rect).copy())
    return tuple(frames)


def _detect_bbox_rects(
    guide_sheet: pygame.Surface,
    *,
    bbox_color: tuple[int, int, int, int] = (255, 0, 0, 255),
    color_tolerance: tuple[int, int, int, int] = (30, 60, 60, 255),
    min_size: tuple[int, int] = (24, 24),
) -> tuple[pygame.Rect, ...]:
    mask = pygame.mask.from_threshold(guide_sheet, bbox_color, color_tolerance)
    raw_rects = mask.get_bounding_rects()
    filtered = [
        rect
        for rect in raw_rects
        if rect.width >= int(min_size[0]) and rect.height >= int(min_size[1])
    ]
    if not filtered:
        return ()
    return tuple(_sort_rects_row_major(filtered))


def _sort_rects_row_major(rects: list[pygame.Rect]) -> list[pygame.Rect]:
    if not rects:
        return []
    sorted_by_y = sorted(rects, key=lambda rect: rect.centery)
    average_height = sum(rect.height for rect in sorted_by_y) / max(1, len(sorted_by_y))
    row_tolerance = max(6.0, average_height * 0.5)
    rows: list[list[pygame.Rect]] = []
    row_centers: list[float] = []
    for rect in sorted_by_y:
        assigned = False
        for index, center in enumerate(row_centers):
            if abs(rect.centery - center) <= row_tolerance:
                rows[index].append(rect)
                count = len(rows[index])
                row_centers[index] = ((center * (count - 1)) + rect.centery) / count
                assigned = True
                break
        if not assigned:
            rows.append([rect])
            row_centers.append(float(rect.centery))
    ordered: list[pygame.Rect] = []
    for _, row_rects in sorted(zip(row_centers, rows), key=lambda item: item[0]):
        ordered.extend(sorted(row_rects, key=lambda rect: rect.x))
    return ordered


def _inset_rect_for_bbox_content(rect: pygame.Rect) -> pygame.Rect:
    return _inset_rect(rect, inset_pixels=1)


def _inset_rect(rect: pygame.Rect, *, inset_pixels: int) -> pygame.Rect:
    inset = max(0, int(inset_pixels))
    if inset <= 0:
        return rect
    min_size = (inset * 2) + 1
    if rect.width < min_size or rect.height < min_size:
        return rect
    shrink = inset * 2
    return rect.inflate(-shrink, -shrink)


def _clear_bbox_red_pixels(frame: pygame.Surface) -> None:
    width, height = frame.get_size()
    if width <= 0 or height <= 0:
        return
    pixels = pygame.surfarray.pixels3d(frame)
    alpha = pygame.surfarray.pixels_alpha(frame)
    for x in range(width):
        for y in range(height):
            if alpha[x, y] <= 0:
                continue
            r, g, b = pixels[x, y]
            if r >= 240 and g <= 40 and b <= 40:
                alpha[x, y] = 0
    del pixels
    del alpha


def _extract_frames_from_bbox_guide(
    target_sheet: pygame.Surface,
    guide_sheet: pygame.Surface,
) -> tuple[pygame.Surface, ...]:
    guide_rects = _detect_bbox_rects(guide_sheet)
    if not guide_rects:
        return ()
    scale_x = target_sheet.get_width() / max(1.0, float(guide_sheet.get_width()))
    scale_y = target_sheet.get_height() / max(1.0, float(guide_sheet.get_height()))
    frames: list[pygame.Surface] = []
    for rect in guide_rects:
        mapped = pygame.Rect(
            int(round(rect.x * scale_x)),
            int(round(rect.y * scale_y)),
            max(1, int(round(rect.width * scale_x))),
            max(1, int(round(rect.height * scale_y))),
        )
        mapped = mapped.clip(target_sheet.get_rect())
        if mapped.width <= 0 or mapped.height <= 0:
            continue
        content_rect = _inset_rect_for_bbox_content(mapped)
        if content_rect.width <= 0 or content_rect.height <= 0:
            continue
        frame = target_sheet.subsurface(content_rect).copy()
        _clear_bbox_red_pixels(frame)
        frames.append(frame)
    return tuple(frames)


def _load_frame_rect_cache(
    frame_rects_path: str,
    *,
    expected_sheet_path: str | None = None,
) -> tuple[tuple[pygame.Rect, ...], int] | None:
    try:
        data_path = _resolve_data_path(frame_rects_path)
        raw = data_path.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    if expected_sheet_path is not None:
        cached_sheet = payload.get("sheet_path")
        if isinstance(cached_sheet, str) and cached_sheet and cached_sheet != expected_sheet_path:
            return None
    rect_entries = payload.get("frame_rects")
    if not isinstance(rect_entries, list) or len(rect_entries) == 0:
        return None
    rects: list[pygame.Rect] = []
    for entry in rect_entries:
        if not isinstance(entry, dict):
            return None
        try:
            x = int(entry["x"])
            y = int(entry["y"])
            w = int(entry["w"])
            h = int(entry["h"])
        except (KeyError, TypeError, ValueError):
            return None
        if w <= 0 or h <= 0:
            return None
        rects.append(pygame.Rect(x, y, w, h))
    inset_pixels = max(0, int(payload.get("content_inset", 1)))
    return tuple(rects), inset_pixels


def _extract_frames_from_cached_rects(
    target_sheet: pygame.Surface,
    frame_rects: tuple[pygame.Rect, ...],
    *,
    inset_pixels: int,
) -> tuple[pygame.Surface, ...]:
    frames: list[pygame.Surface] = []
    sheet_bounds = target_sheet.get_rect()
    for raw_rect in frame_rects:
        clipped = pygame.Rect(raw_rect).clip(sheet_bounds)
        if clipped.width <= 0 or clipped.height <= 0:
            continue
        content_rect = _inset_rect(clipped, inset_pixels=inset_pixels)
        if content_rect.width <= 0 or content_rect.height <= 0:
            continue
        frame = target_sheet.subsurface(content_rect).copy()
        _clear_bbox_red_pixels(frame)
        frames.append(frame)
    return tuple(frames)


def _load_clip(config: AnimationClipConfig) -> LoadedAnimationClip:
    sheet = _safe_load_sheet(config.sheet_path)
    if sheet is None:
        return LoadedAnimationClip(frames=(), fps=max(1.0, float(config.fps)), available=False)
    if config.frame_rects_path:
        cached = _load_frame_rect_cache(
            config.frame_rects_path,
            expected_sheet_path=config.sheet_path,
        )
        if cached is not None:
            frame_rects, inset_pixels = cached
            cached_frames = _extract_frames_from_cached_rects(
                sheet,
                frame_rects,
                inset_pixels=inset_pixels,
            )
            if len(cached_frames) > 0:
                return LoadedAnimationClip(
                    frames=cached_frames,
                    fps=max(1.0, float(config.fps)),
                    available=True,
                )
    if config.extraction_mode == "bbox_guide" and config.bbox_guide_path:
        guide = _safe_load_sheet(config.bbox_guide_path)
        if guide is not None:
            bbox_frames = _extract_frames_from_bbox_guide(sheet, guide)
            if len(bbox_frames) > 0:
                return LoadedAnimationClip(
                    frames=bbox_frames,
                    fps=max(1.0, float(config.fps)),
                    available=True,
                )
    frames = _extract_frames(sheet, rows=config.rows, columns=config.columns)
    return LoadedAnimationClip(frames=frames, fps=max(1.0, float(config.fps)), available=len(frames) > 0)


def load_character_animation(config: CharacterAnimationConfig) -> LoadedCharacterAnimation:
    return LoadedCharacterAnimation(
        character_id=config.character_id,
        idle=_load_clip(config.idle),
        walk=_load_clip(config.walk),
        base_display_scale=float(config.base_display_scale),
        anchor_offset=(int(config.anchor_offset[0]), int(config.anchor_offset[1])),
        hitbox_radius=float(config.hitbox_radius),
        hitbox_vertical_offset=float(config.hitbox_vertical_offset),
        flip_left=bool(config.flip_left),
    )


class PlayerAnimationSystem:
    """Owns player animation clip loading, state selection, and frame advancement."""

    def __init__(
        self,
        *,
        configs: dict[str, CharacterAnimationConfig] | None = None,
        loader: Callable[[CharacterAnimationConfig], LoadedCharacterAnimation] = load_character_animation,
    ) -> None:
        if configs is None:
            self._configs = {item.character_id: item for item in list_character_animation_configs()}
        else:
            self._configs = dict(configs)
        self._loader = loader
        self._loaded: dict[str, LoadedCharacterAnimation] = {}
        self._active_character_id = DEFAULT_CHARACTER_ANIMATION_ID
        self._state = "idle"
        self._frame_index = 0
        self._timer = 0.0
        self._last_facing = pygame.Vector2(1.0, 0.0)

    def set_character(self, character_id: str) -> None:
        selected = str(character_id)
        if selected not in self._configs:
            selected = DEFAULT_CHARACTER_ANIMATION_ID
        if selected != self._active_character_id:
            self._active_character_id = selected
            self._state = "idle"
            self._frame_index = 0
            self._timer = 0.0

    def reset(self) -> None:
        self._state = "idle"
        self._frame_index = 0
        self._timer = 0.0
        self._last_facing = pygame.Vector2(1.0, 0.0)

    def update(self, delta_seconds: float, *, moving: bool, facing: pygame.Vector2) -> None:
        facing_vector = pygame.Vector2(facing)
        if facing_vector.length_squared() > 0.0:
            self._last_facing = facing_vector.normalize()
        desired_state = "walk" if moving else "idle"
        if desired_state != self._state:
            self._state = desired_state
            self._frame_index = 0
            self._timer = 0.0
        clip = self._active_clip()
        if not clip.available or len(clip.frames) <= 1:
            return
        frame_duration = 1.0 / max(1.0, clip.fps)
        self._timer += max(0.0, float(delta_seconds)) * ANIMATION_PLAYBACK_SPEED_MULTIPLIER
        while self._timer >= frame_duration:
            self._timer -= frame_duration
            self._frame_index = (self._frame_index + 1) % len(clip.frames)

    def current_frame(self) -> pygame.Surface | None:
        clip = self._active_clip()
        if not clip.available or len(clip.frames) == 0:
            return None
        return clip.frames[self._frame_index % len(clip.frames)]

    def frame_rect_for_player(self, player_rect: pygame.Rect) -> pygame.Rect | None:
        frame = self.current_frame()
        if frame is None:
            return None
        loaded = self._active_loaded()
        width = max(1, int(round(frame.get_width() * loaded.base_display_scale)))
        height = max(1, int(round(frame.get_height() * loaded.base_display_scale)))
        rect = pygame.Rect(0, 0, width, height)
        rect.midbottom = (
            player_rect.centerx + loaded.anchor_offset[0],
            player_rect.bottom + loaded.anchor_offset[1],
        )
        return rect

    def snapshot(self) -> dict[str, object]:
        clip = self._active_clip()
        loaded = self._active_loaded()
        return {
            "character_id": self._active_character_id,
            "state": self._state,
            "frame_index": int(self._frame_index),
            "frame_count": len(clip.frames),
            "clip_available": bool(clip.available),
            "fps": float(clip.fps),
            "idle_clip_available": bool(loaded.idle.available),
            "walk_clip_available": bool(loaded.walk.available),
            "flip_x": bool(self.should_flip_horizontal()),
        }

    def should_flip_horizontal(self) -> bool:
        loaded = self._active_loaded()
        if not loaded.flip_left:
            return False
        facing = pygame.Vector2(self._last_facing)
        if facing.length_squared() <= 0.0:
            return False
        return facing.x > 0.15 and abs(facing.x) >= (abs(facing.y) * 0.6)

    def _active_loaded(self) -> LoadedCharacterAnimation:
        character_id = self._active_character_id
        loaded = self._loaded.get(character_id)
        if loaded is None:
            config = self._configs.get(character_id, self._configs[DEFAULT_CHARACTER_ANIMATION_ID])
            loaded = self._loader(config)
            self._loaded[character_id] = loaded
        return loaded

    def _active_clip(self) -> LoadedAnimationClip:
        loaded = self._active_loaded()
        if self._state == "walk":
            return loaded.walk
        return loaded.idle
