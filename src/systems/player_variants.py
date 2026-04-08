"""Reusable player visual variant definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerVisualVariant:
    variant_id: str
    name: str
    body_color: tuple[int, int, int]
    inner_body_color: tuple[int, int, int]
    outline_color: tuple[int, int, int]
    ear_inner_color: tuple[int, int, int]
    eye_color: tuple[int, int, int]
    hat_color: tuple[int, int, int]
    hat_pom_color: tuple[int, int, int]
    ear_scale: float
    style_notes: str
    render_source: str
    sprite_asset_path: str | None = None
    hat_enabled: bool = True
    prefers_sprite: bool = False


PLAYER_VARIANTS: tuple[PlayerVisualVariant, ...] = (
    PlayerVisualVariant(
        variant_id="bear",
        name="Bear",
        body_color=(205, 155, 110),
        inner_body_color=(226, 184, 145),
        outline_color=(250, 245, 232),
        ear_inner_color=(242, 208, 176),
        eye_color=(40, 36, 31),
        hat_color=(88, 196, 255),
        hat_pom_color=(255, 102, 128),
        ear_scale=1.0,
        style_notes="Rounded teddy proportions with warm tones.",
        render_source="shape-based",
    ),
    PlayerVisualVariant(
        variant_id="bunny",
        name="Bunny",
        body_color=(231, 204, 255),
        inner_body_color=(242, 224, 255),
        outline_color=(252, 246, 255),
        ear_inner_color=(255, 231, 244),
        eye_color=(50, 34, 69),
        hat_color=(112, 217, 255),
        hat_pom_color=(255, 118, 184),
        ear_scale=1.25,
        style_notes="Long-ear silhouette with bright pastel contrast.",
        render_source="shape-based",
    ),
    PlayerVisualVariant(
        variant_id="fox",
        name="Fox",
        body_color=(255, 170, 104),
        inner_body_color=(255, 203, 153),
        outline_color=(255, 247, 231),
        ear_inner_color=(255, 224, 201),
        eye_color=(44, 30, 24),
        hat_color=(85, 220, 250),
        hat_pom_color=(255, 95, 123),
        ear_scale=0.92,
        style_notes="Sharp-faced fox palette tuned for high readability.",
        render_source="sprite/shape fallback",
        sprite_asset_path="images/player_fox.png",
        prefers_sprite=True,
    ),
    PlayerVisualVariant(
        variant_id="cat",
        name="Cat",
        body_color=(148, 210, 255),
        inner_body_color=(186, 228, 255),
        outline_color=(241, 251, 255),
        ear_inner_color=(221, 241, 255),
        eye_color=(24, 44, 56),
        hat_color=(255, 178, 95),
        hat_pom_color=(255, 100, 140),
        ear_scale=1.05,
        style_notes="Cool-toned cat style with crisp face contrast.",
        render_source="shape-based",
    ),
    PlayerVisualVariant(
        variant_id="dog",
        name="Dog",
        body_color=(252, 202, 126),
        inner_body_color=(255, 221, 160),
        outline_color=(255, 247, 232),
        ear_inner_color=(255, 226, 179),
        eye_color=(45, 38, 29),
        hat_color=(96, 205, 255),
        hat_pom_color=(255, 100, 151),
        ear_scale=0.9,
        style_notes="Friendly dog variant with chunkier, grounded palette.",
        render_source="shape-based",
    ),
)


PLAYER_VARIANTS_BY_ID: dict[str, PlayerVisualVariant] = {
    variant.variant_id: variant for variant in PLAYER_VARIANTS
}

