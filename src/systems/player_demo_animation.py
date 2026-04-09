"""Reusable animated sprite-sheet helpers for demo and future integration."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from .paths import asset_path


@dataclass(frozen=True)
class SpriteSheetLoadResult:
    surface: pygame.Surface | None
    path: str
    error: str | None = None


def load_sprite_sheet_with_alpha(*path_parts: str) -> SpriteSheetLoadResult:
    sheet_path = asset_path(*path_parts)
    try:
        loaded = pygame.image.load(str(sheet_path))
        return SpriteSheetLoadResult(surface=loaded.convert_alpha(), path=str(sheet_path), error=None)
    except (pygame.error, FileNotFoundError, OSError) as exc:
        return SpriteSheetLoadResult(surface=None, path=str(sheet_path), error=str(exc))


def extract_sprite_sheet_grid(
    sheet: pygame.Surface,
    *,
    rows: int,
    columns: int,
) -> list[list[pygame.Surface]]:
    safe_rows = max(1, int(rows))
    safe_columns = max(1, int(columns))
    cell_width = sheet.get_width() // safe_columns
    cell_height = sheet.get_height() // safe_rows
    if cell_width <= 0 or cell_height <= 0:
        return []

    frames: list[list[pygame.Surface]] = []
    for row_index in range(safe_rows):
        row_frames: list[pygame.Surface] = []
        for column_index in range(safe_columns):
            rect = pygame.Rect(
                column_index * cell_width,
                row_index * cell_height,
                cell_width,
                cell_height,
            )
            row_frames.append(sheet.subsurface(rect).copy())
        frames.append(row_frames)
    return frames


def validate_sprite_sheet_grid(
    sheet: pygame.Surface,
    *,
    rows: int,
    columns: int,
) -> str | None:
    safe_rows = max(1, int(rows))
    safe_columns = max(1, int(columns))
    width = sheet.get_width()
    height = sheet.get_height()
    if width % safe_columns != 0 or height % safe_rows != 0:
        return (
            f"sheet size {width}x{height} is not divisible by "
            f"{safe_columns} columns x {safe_rows} rows"
        )
    cell_width = width // safe_columns
    cell_height = height // safe_rows
    if cell_width <= 0 or cell_height <= 0:
        return "invalid grid cell size resolved to zero"
    return None


def flatten_frames_row_major(frames_by_row: list[list[pygame.Surface]]) -> list[pygame.Surface]:
    sequence: list[pygame.Surface] = []
    for row in frames_by_row:
        sequence.extend(row)
    return sequence


def detect_bbox_frame_rects(
    guide_sheet: pygame.Surface,
    *,
    bbox_color: tuple[int, int, int, int] = (255, 0, 0, 255),
    color_tolerance: tuple[int, int, int, int] = (30, 60, 60, 255),
    min_size: tuple[int, int] = (24, 24),
) -> list[pygame.Rect]:
    mask = pygame.mask.from_threshold(guide_sheet, bbox_color, color_tolerance)
    raw_rects = mask.get_bounding_rects()
    filtered = [
        rect
        for rect in raw_rects
        if rect.width >= int(min_size[0]) and rect.height >= int(min_size[1])
    ]
    if not filtered:
        return []
    return _sort_rects_row_major(filtered)


def extract_frames_from_bbox_guide(
    target_sheet: pygame.Surface,
    guide_sheet: pygame.Surface,
) -> list[pygame.Surface]:
    guide_rects = detect_bbox_frame_rects(guide_sheet)
    if not guide_rects:
        return []
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
    return frames


def _sort_rects_row_major(rects: list[pygame.Rect]) -> list[pygame.Rect]:
    if not rects:
        return []
    sorted_by_y = sorted(rects, key=lambda rect: rect.centery)
    average_height = sum(rect.height for rect in sorted_by_y) / max(1, len(sorted_by_y))
    row_tolerance = max(6.0, average_height * 0.5)

    rows: list[list[pygame.Rect]] = []
    row_centers: list[float] = []
    for rect in sorted_by_y:
        attached = False
        for index, center in enumerate(row_centers):
            if abs(rect.centery - center) <= row_tolerance:
                rows[index].append(rect)
                count = len(rows[index])
                row_centers[index] = ((center * (count - 1)) + rect.centery) / count
                attached = True
                break
        if not attached:
            rows.append([rect])
            row_centers.append(float(rect.centery))

    ordered: list[pygame.Rect] = []
    rows_with_centers = sorted(zip(row_centers, rows), key=lambda item: item[0])
    for _, row_rects in rows_with_centers:
        ordered.extend(sorted(row_rects, key=lambda rect: rect.x))
    return ordered


def _inset_rect_for_bbox_content(rect: pygame.Rect) -> pygame.Rect:
    if rect.width < 3 or rect.height < 3:
        return rect
    return rect.inflate(-2, -2)


def _clear_bbox_red_pixels(frame: pygame.Surface) -> None:
    width, height = frame.get_size()
    if width <= 0 or height <= 0:
        return
    pixels = pygame.surfarray.pixels3d(frame)
    alpha = pygame.surfarray.pixels_alpha(frame)
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r >= 240 and g <= 40 and b <= 40 and alpha[x, y] > 0:
                alpha[x, y] = 0
    del pixels
    del alpha


def resolve_direction_mapping(
    direction: str,
    *,
    mapping: dict[str, dict[str, int | bool]],
    row_count: int,
) -> tuple[int, bool]:
    entry = mapping.get(direction, mapping.get("down", {"row": 0, "flip": False}))
    row = int(entry.get("row", 0))
    if row_count > 0:
        row = max(0, min(row, row_count - 1))
    else:
        row = 0
    return row, bool(entry.get("flip", False))


def anchored_frame_rect(
    frame_size: tuple[int, int],
    *,
    anchor: tuple[int, int],
    scale: float = 1.0,
    offset: tuple[int, int] = (0, 0),
) -> pygame.Rect:
    width = max(1, int(round(frame_size[0] * max(0.1, scale))))
    height = max(1, int(round(frame_size[1] * max(0.1, scale))))
    rect = pygame.Rect(0, 0, width, height)
    rect.midbottom = (anchor[0] + int(offset[0]), anchor[1] + int(offset[1]))
    return rect


def draw_frame_center_bottom_anchored(
    surface: pygame.Surface,
    frame: pygame.Surface,
    *,
    anchor: tuple[int, int],
    scale: float = 1.0,
    offset: tuple[int, int] = (0, 0),
) -> pygame.Rect:
    target = anchored_frame_rect(
        frame.get_size(),
        anchor=anchor,
        scale=scale,
        offset=offset,
    )
    scaled = pygame.transform.smoothscale(frame, target.size)
    surface.blit(scaled, target)
    return target


def advance_animation_loop(
    *,
    frame_index: int,
    timer: float,
    delta_seconds: float,
    fps: float,
    frame_count: int,
) -> tuple[int, float]:
    if frame_count <= 0:
        return 0, 0.0
    frame_duration = 1.0 / max(1.0, float(fps))
    updated_timer = timer + max(0.0, delta_seconds)
    updated_index = max(0, int(frame_index)) % frame_count
    while updated_timer >= frame_duration:
        updated_timer -= frame_duration
        updated_index = (updated_index + 1) % frame_count
    return updated_index, updated_timer
