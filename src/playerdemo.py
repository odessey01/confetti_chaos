"""Standalone animated sprite-sheet preview sandbox."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from systems import player_demo_animation
from systems.player_demo_sprite import (
    BEAR_IDLE_ANIMATION_CONFIG,
    BEAR_WALKING_ANIMATION_CONFIG,
    AnimatedSpriteSheetConfig,
    hitbox_from_anchor,
)


WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
WINDOW_TITLE = "Confetti Chaos - Sprite Sheet Demo"
TARGET_FPS = 60
BASE_RENDER_ANCHOR = (WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.78))
ANIMATED_PREVIEW_HITBOX_RADIUS = BEAR_WALKING_ANIMATION_CONFIG.hitbox_radius
ANIMATED_PREVIEW_HITBOX_VERTICAL_OFFSET = BEAR_WALKING_ANIMATION_CONFIG.hitbox_vertical_offset

SPRITE_SHEET_CONFIGS: tuple[AnimatedSpriteSheetConfig, ...] = (
    BEAR_WALKING_ANIMATION_CONFIG,
    BEAR_IDLE_ANIMATION_CONFIG,
)


@dataclass
class DemoState:
    config_index: int = 0
    show_debug: bool = False
    sheet_loaded: bool = False
    sheet_error: str | None = None
    frames_by_row: list[list[pygame.Surface]] | None = None
    frame_sequence: list[pygame.Surface] | None = None
    animation_playing: bool = True
    animation_fps: float = BEAR_WALKING_ANIMATION_CONFIG.animation_fps
    animation_timer: float = 0.0
    animation_frame_index: int = 0
    animation_preview_mode: str = "loop"
    animation_hitbox_radius: float = ANIMATED_PREVIEW_HITBOX_RADIUS
    animation_hitbox_vertical_offset: float = ANIMATED_PREVIEW_HITBOX_VERTICAL_OFFSET
    animation_preview_scale: float = BEAR_WALKING_ANIMATION_CONFIG.base_display_scale
    animation_offset_x: int = BEAR_WALKING_ANIMATION_CONFIG.anchor_offset[0]
    animation_offset_y: int = BEAR_WALKING_ANIMATION_CONFIG.anchor_offset[1]
    loaded_sheet_size: tuple[int, int] | None = None
    loaded_cell_size: tuple[int, int] | None = None
    loaded_extraction_mode: str = "grid"
    detected_bbox_count: int = 0
    loaded_display_source_path: str | None = None
    loaded_detection_source_path: str | None = None


@dataclass(frozen=True)
class FrameExtractionResult:
    frames_by_row: list[list[pygame.Surface]] | None
    frame_sequence: list[pygame.Surface] | None
    extraction_mode: str
    cell_size: tuple[int, int] | None
    detected_bbox_count: int
    warning: str | None = None


def cycle_row_index(current_row: int, direction: int, row_count: int) -> int:
    if row_count <= 0:
        return 0
    return (current_row + direction) % row_count


def cycle_variant_index(current_index: int, direction: int, count: int) -> int:
    if count <= 0:
        return 0
    return (current_index + direction) % count


def clamp_scale(scale: float) -> float:
    return max(0.6, min(2.2, float(scale)))


def direction_to_facing(direction_name: str) -> pygame.Vector2:
    mapping = {
        "up": pygame.Vector2(0.0, -1.0),
        "down": pygame.Vector2(0.0, 1.0),
        "left": pygame.Vector2(-1.0, 0.0),
        "right": pygame.Vector2(1.0, 0.0),
    }
    return pygame.Vector2(mapping.get(direction_name, pygame.Vector2(1.0, 0.0)))


def clamp_animation_fps(value: float) -> float:
    return max(1.0, min(24.0, float(value)))


def load_sprite_sheet_with_alpha(*path_parts: str) -> player_demo_animation.SpriteSheetLoadResult:
    return player_demo_animation.load_sprite_sheet_with_alpha(*path_parts)


def extract_sprite_sheet_grid(
    sheet: pygame.Surface,
    *,
    rows: int,
    columns: int,
) -> list[list[pygame.Surface]]:
    return player_demo_animation.extract_sprite_sheet_grid(sheet, rows=rows, columns=columns)


def anchored_frame_rect(
    frame_size: tuple[int, int],
    *,
    anchor: tuple[int, int],
    scale: float = 1.0,
    offset: tuple[int, int] = (0, 0),
) -> pygame.Rect:
    return player_demo_animation.anchored_frame_rect(
        frame_size,
        anchor=anchor,
        scale=scale,
        offset=offset,
    )


def draw_frame_center_bottom_anchored(
    surface: pygame.Surface,
    frame: pygame.Surface,
    *,
    anchor: tuple[int, int],
    scale: float = 1.0,
    offset: tuple[int, int] = (0, 0),
) -> pygame.Rect:
    return player_demo_animation.draw_frame_center_bottom_anchored(
        surface,
        frame,
        anchor=anchor,
        scale=scale,
        offset=offset,
    )


def _active_config(state: DemoState) -> AnimatedSpriteSheetConfig:
    return SPRITE_SHEET_CONFIGS[state.config_index % max(1, len(SPRITE_SHEET_CONFIGS))]


def _reload_active_sheet(state: DemoState) -> None:
    config = _active_config(state)
    parts = tuple(config.sprite_sheet_path.split("/"))
    loaded = load_sprite_sheet_with_alpha(*parts)
    state.sheet_loaded = loaded.surface is not None
    state.sheet_error = loaded.error
    state.frames_by_row = None
    state.frame_sequence = None
    state.animation_frame_index = 0
    state.animation_timer = 0.0
    state.animation_playing = True
    state.animation_preview_mode = "loop"
    state.animation_fps = config.animation_fps
    state.animation_preview_scale = config.base_display_scale
    state.animation_offset_x = config.anchor_offset[0]
    state.animation_offset_y = config.anchor_offset[1]
    state.animation_hitbox_radius = config.hitbox_radius
    state.animation_hitbox_vertical_offset = config.hitbox_vertical_offset
    state.loaded_sheet_size = None
    state.loaded_cell_size = None
    state.loaded_extraction_mode = config.extraction_mode
    state.detected_bbox_count = 0
    state.loaded_display_source_path = config.sprite_sheet_path
    state.loaded_detection_source_path = None
    if loaded.surface is None:
        return
    state.loaded_sheet_size = loaded.surface.get_size()
    extraction = _extract_frames_for_config(config, loaded.surface)
    state.loaded_extraction_mode = extraction.extraction_mode
    state.loaded_cell_size = extraction.cell_size
    state.detected_bbox_count = extraction.detected_bbox_count
    state.frames_by_row = extraction.frames_by_row
    state.frame_sequence = extraction.frame_sequence
    if config.extraction_mode == "bbox_guide" and config.bbox_guide_path:
        state.loaded_detection_source_path = config.bbox_guide_path
    if extraction.frame_sequence:
        state.sheet_loaded = True
        state.sheet_error = extraction.warning
        return
    state.sheet_loaded = False
    state.sheet_error = extraction.warning or "unable to extract animation frames"


def _extract_frames_for_config(
    config: AnimatedSpriteSheetConfig,
    sheet: pygame.Surface,
) -> FrameExtractionResult:
    if config.extraction_mode == "bbox_guide" and config.bbox_guide_path:
        guide_parts = tuple(config.bbox_guide_path.split("/"))
        guide = load_sprite_sheet_with_alpha(*guide_parts)
        if guide.surface is not None:
            bbox_frames = player_demo_animation.extract_frames_from_bbox_guide(sheet, guide.surface)
            if bbox_frames:
                return FrameExtractionResult(
                    frames_by_row=[bbox_frames],
                    frame_sequence=bbox_frames,
                    extraction_mode="bbox_guide",
                    cell_size=bbox_frames[0].get_size(),
                    detected_bbox_count=len(bbox_frames),
                    warning=None,
                )
            warning = "bbox guide loaded but no frame boxes were detected; using grid fallback"
        else:
            warning = f"bbox guide unavailable ({guide.error or 'unknown error'}); using grid fallback"
    else:
        warning = None

    grid_error = player_demo_animation.validate_sprite_sheet_grid(sheet, rows=config.rows, columns=config.columns)
    if grid_error is not None:
        return FrameExtractionResult(
            frames_by_row=None,
            frame_sequence=None,
            extraction_mode="grid",
            cell_size=None,
            detected_bbox_count=0,
            warning=grid_error if warning is None else f"{warning}; {grid_error}",
        )
    frames_by_row = extract_sprite_sheet_grid(sheet, rows=config.rows, columns=config.columns)
    frame_sequence = player_demo_animation.flatten_frames_row_major(frames_by_row)
    return FrameExtractionResult(
        frames_by_row=frames_by_row,
        frame_sequence=frame_sequence,
        extraction_mode="grid",
        cell_size=(sheet.get_width() // config.columns, sheet.get_height() // config.rows),
        detected_bbox_count=0,
        warning=warning,
    )


def handle_demo_key(state: DemoState, event: pygame.event.Event, variant_count: int) -> bool:
    if event.key == pygame.K_ESCAPE:
        return False
    if event.key == pygame.K_g:
        state.show_debug = not state.show_debug
    elif event.key == pygame.K_p:
        state.animation_playing = not state.animation_playing
    elif event.key == pygame.K_TAB:
        state.animation_preview_mode = "pose" if state.animation_preview_mode == "loop" else "loop"
        if state.animation_preview_mode == "pose":
            state.animation_frame_index = 0
            state.animation_timer = 0.0
    elif event.key == pygame.K_b:
        state.animation_fps = clamp_animation_fps(state.animation_fps + 1.0)
    elif event.key == pygame.K_v:
        state.animation_fps = clamp_animation_fps(state.animation_fps - 1.0)
    elif event.key == pygame.K_z:
        state.animation_preview_scale = max(0.4, state.animation_preview_scale - 0.05)
    elif event.key == pygame.K_x:
        state.animation_preview_scale = min(2.6, state.animation_preview_scale + 0.05)
    elif event.key == pygame.K_j:
        state.animation_offset_x -= 1
    elif event.key == pygame.K_l:
        state.animation_offset_x += 1
    elif event.key == pygame.K_i:
        state.animation_offset_y -= 1
    elif event.key == pygame.K_k:
        state.animation_offset_y += 1
    elif event.key == pygame.K_COMMA:
        state.animation_hitbox_radius = max(6.0, state.animation_hitbox_radius - 1.0)
    elif event.key == pygame.K_PERIOD:
        state.animation_hitbox_radius = min(40.0, state.animation_hitbox_radius + 1.0)
    elif event.key == pygame.K_n:
        state.animation_hitbox_vertical_offset = max(-20.0, state.animation_hitbox_vertical_offset - 1.0)
    elif event.key == pygame.K_m:
        state.animation_hitbox_vertical_offset = min(40.0, state.animation_hitbox_vertical_offset + 1.0)
    elif event.key == pygame.K_LEFTBRACKET:
        frame_count = len(state.frame_sequence) if state.frame_sequence else 0
        if frame_count > 0:
            state.animation_frame_index = (state.animation_frame_index - 1) % frame_count
    elif event.key == pygame.K_RIGHTBRACKET:
        frame_count = len(state.frame_sequence) if state.frame_sequence else 0
        if frame_count > 0:
            state.animation_frame_index = (state.animation_frame_index + 1) % frame_count
    elif event.key == pygame.K_a:
        if variant_count > 0:
            state.config_index = (state.config_index - 1) % variant_count
            _reload_active_sheet(state)
    elif event.key == pygame.K_d:
        if variant_count > 0:
            state.config_index = (state.config_index + 1) % variant_count
            _reload_active_sheet(state)
    return True


def update_row_animation(state: DemoState, delta_seconds: float) -> None:
    if state.animation_preview_mode == "pose":
        state.animation_frame_index = 0
        state.animation_timer = 0.0
        return
    if not state.animation_playing:
        return
    if not state.frame_sequence:
        return
    frame_count = len(state.frame_sequence)
    if frame_count <= 0:
        return
    state.animation_frame_index, state.animation_timer = player_demo_animation.advance_animation_loop(
        frame_index=state.animation_frame_index,
        timer=state.animation_timer,
        delta_seconds=delta_seconds,
        fps=state.animation_fps,
        frame_count=frame_count,
    )


def draw_demo_background(surface: pygame.Surface) -> None:
    top = pygame.Color(18, 27, 40)
    bottom = pygame.Color(36, 58, 78)
    for y in range(surface.get_height()):
        t = y / max(1, surface.get_height() - 1)
        color = top.lerp(bottom, t)
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))
    floor = pygame.Rect(0, int(surface.get_height() * 0.66), surface.get_width(), int(surface.get_height() * 0.34))
    pygame.draw.rect(surface, (24, 42, 58), floor)


def draw_animation_preview(surface: pygame.Surface, state: DemoState) -> None:
    if not state.frame_sequence:
        return
    frame_count = len(state.frame_sequence)
    if frame_count <= 0:
        return

    frame = state.frame_sequence[state.animation_frame_index % frame_count]
    frame_rect = draw_frame_center_bottom_anchored(
        surface,
        frame,
        anchor=BASE_RENDER_ANCHOR,
        scale=state.animation_preview_scale,
        offset=(state.animation_offset_x, state.animation_offset_y),
    )

    resolved_anchor = (
        BASE_RENDER_ANCHOR[0] + state.animation_offset_x,
        BASE_RENDER_ANCHOR[1] + state.animation_offset_y,
    )
    hitbox_center, hitbox_radius = hitbox_from_anchor(
        anchor=resolved_anchor,
        radius=state.animation_hitbox_radius,
        vertical_offset=state.animation_hitbox_vertical_offset,
    )
    pygame.draw.circle(
        surface,
        (110, 225, 255),
        (int(hitbox_center.x), int(hitbox_center.y)),
        int(hitbox_radius),
        width=2,
    )

    if state.show_debug:
        pygame.draw.line(
            surface,
            (105, 132, 156),
            (0, resolved_anchor[1]),
            (surface.get_width(), resolved_anchor[1]),
            width=1,
        )
        pygame.draw.circle(surface, (255, 110, 140), resolved_anchor, 4)
        pygame.draw.rect(surface, (246, 220, 122), frame_rect, width=1)


def draw_overlay(surface: pygame.Surface, state: DemoState) -> None:
    config = _active_config(state)
    frame_count = len(state.frame_sequence) if state.frame_sequence else 0
    font = pygame.font.Font(None, 28)
    small = pygame.font.Font(None, 22)
    lines = [
        f"Sprite Sheet: {config.sprite_sheet_path}",
        (
            "Sheet load: success"
            if state.sheet_loaded
            else f"Sheet load: unavailable ({state.sheet_error or 'unknown error'})"
        ),
        (
            f"Sheet/Grid: {state.loaded_sheet_size[0]}x{state.loaded_sheet_size[1]} "
            f"| {config.columns}x{config.rows} cells "
            f"({state.loaded_cell_size[0]}x{state.loaded_cell_size[1]})"
            if state.loaded_sheet_size and state.loaded_cell_size
            else f"Sheet/Grid: ? | {config.columns}x{config.rows} cells"
        ),
        f"Display source: {state.loaded_display_source_path or 'unknown'}",
        (
            f"Detection source: {state.loaded_detection_source_path}"
            if state.loaded_detection_source_path
            else "Detection source: grid-only"
        ),
        f"Extraction: {state.loaded_extraction_mode} | detected boxes: {state.detected_bbox_count}",
        f"Loop Mode: {config.loop_mode} ({config.frame_order})",
        f"Frame: {state.animation_frame_index}/{max(0, frame_count - 1)}",
        f"Preview mode: {state.animation_preview_mode}",
        f"Playback: {'playing' if state.animation_playing else 'paused'} @ {state.animation_fps:.1f} FPS",
        f"Tuning: scale={state.animation_preview_scale:.2f} offset=({state.animation_offset_x},{state.animation_offset_y})",
        f"Hitbox: r={state.animation_hitbox_radius:.1f} yoff={state.animation_hitbox_vertical_offset:.1f}",
    ]
    controls = [
        "Controls:",
        "A/D: previous/next sprite config",
        "P: play/pause | Tab: loop/pose preview",
        "[: previous frame | ]: next frame",
        "B/V: fps +/- | Z/X: scale -/+",
        "J/L: offset X | I/K: offset Y",
        ",/.: hitbox radius | N/M: hitbox Y offset",
        "G: toggle debug overlay | Esc: quit",
    ]

    y = 14
    for line in lines:
        text = font.render(line, True, (246, 250, 255))
        surface.blit(text, (14, y))
        y += 24
    y += 6
    for line in controls:
        text = small.render(line, True, (228, 240, 250))
        surface.blit(text, (14, y))
        y += 19


def main() -> int:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    state = DemoState()
    _reload_active_sheet(state)
    running = True

    while running:
        delta_seconds = clock.tick(TARGET_FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = handle_demo_key(state, event, len(SPRITE_SHEET_CONFIGS))
                if not running:
                    break

        update_row_animation(state, delta_seconds)
        draw_demo_background(screen)
        draw_animation_preview(screen, state)
        draw_overlay(screen, state)
        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
