"""Shape-based plush variant framework for player visual exploration."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from player import Player


@dataclass(frozen=True)
class TeddyShapeVariant:
    variant_id: str
    name: str
    silhouette_type: str
    proportion_style: str
    readability_focus: str
    style_notes: str
    head_scale: float
    ear_scale: float
    body_width_scale: float
    body_height_scale: float
    cheek_scale: float
    hat_scale: float
    animal_type: str = "teddy"
    ear_type: str = "round"
    plush_family_role: str = "baseline"
    accessory_style: str = "party_hat"
    hat_enabled: bool = True


SOFTER_PLUSH_STYLE_GUIDE: dict[str, str] = {
    "proportions": "Big head, small body. Keep head as visual anchor.",
    "shape_language": "Use soft rounded forms and plush-like mass transitions.",
    "face": "Minimal face: dot eyes and tiny nose only.",
    "silhouette": "Clear species cues through ear shape first, not fine details.",
    "accessory": "Use one shared simple party hat treatment across the plush family.",
    "clarity": "Preserve bright outline contrast and avoid noisy detail.",
}


SHARED_PLUSH_ACCESSORY_RULES: dict[str, str] = {
    "type": "party_hat",
    "placement": "center-top with slight facing-aware tilt",
    "scale": "small and consistent so silhouette stays readable",
    "constraint": "never cover eyes or primary ear silhouette",
}


TEDDY_SHAPE_VARIANTS: tuple[TeddyShapeVariant, ...] = (
    TeddyShapeVariant(
        variant_id="teddy_a",
        name="Option A - Classic Round Plush",
        silhouette_type="Round head + compact oval body",
        proportion_style="Balanced plush baseline",
        readability_focus="Strong simple silhouette",
        style_notes="Friendly default teddy with minimal features.",
        head_scale=1.00,
        ear_scale=1.00,
        body_width_scale=1.00,
        body_height_scale=0.92,
        cheek_scale=0.00,
        hat_scale=0.85,
        plush_family_role="baseline",
    ),
    TeddyShapeVariant(
        variant_id="teddy_b",
        name="Option B - Big-Head Chibi",
        silhouette_type="Large head, tiny body",
        proportion_style="Exaggerated playful proportions",
        readability_focus="Head as dominant anchor",
        style_notes="Chibi-forward personality with oversized top mass.",
        head_scale=1.20,
        ear_scale=1.12,
        body_width_scale=0.74,
        body_height_scale=0.68,
        cheek_scale=0.18,
        hat_scale=0.75,
        plush_family_role="baseline",
    ),
    TeddyShapeVariant(
        variant_id="teddy_c",
        name="Option C - Gameplay Compact",
        silhouette_type="Compact profile with clear ear separation",
        proportion_style="Utility-first compact framing",
        readability_focus="Maximum movement readability",
        style_notes="Reduced noise and width for gameplay clarity.",
        head_scale=0.90,
        ear_scale=0.92,
        body_width_scale=0.86,
        body_height_scale=0.82,
        cheek_scale=0.00,
        hat_scale=0.72,
        plush_family_role="baseline",
    ),
    TeddyShapeVariant(
        variant_id="teddy_d",
        name="Option D - Party Hat Hero",
        silhouette_type="Classic plush with prominent hat",
        proportion_style="Party identity emphasis",
        readability_focus="Theme-forward while keeping face clear",
        style_notes="Larger hat accent for strong party tone.",
        head_scale=1.02,
        ear_scale=1.00,
        body_width_scale=0.96,
        body_height_scale=0.88,
        cheek_scale=0.06,
        hat_scale=1.20,
        plush_family_role="baseline",
    ),
    TeddyShapeVariant(
        variant_id="teddy_e",
        name="Option E - Taller Plush",
        silhouette_type="Big head + taller narrow body",
        proportion_style="Vertical plush variation",
        readability_focus="Distinct vertical profile",
        style_notes="Subtle tall body for silhouette comparison.",
        head_scale=1.06,
        ear_scale=0.96,
        body_width_scale=0.78,
        body_height_scale=1.10,
        cheek_scale=0.04,
        hat_scale=0.82,
        plush_family_role="baseline",
    ),
    TeddyShapeVariant(
        variant_id="teddy_f",
        name="Option F - Softer Plush Deluxe Teddy",
        silhouette_type="Option A round plush with softer transitions",
        proportion_style="Softened baseline plush",
        readability_focus="Maintain Option A clarity with extra softness",
        style_notes="Softer cheeks and rounder mass transitions.",
        head_scale=1.03,
        ear_scale=0.98,
        body_width_scale=1.02,
        body_height_scale=0.95,
        cheek_scale=0.15,
        hat_scale=0.84,
        animal_type="teddy",
        ear_type="round",
        plush_family_role="style_anchor",
    ),
    TeddyShapeVariant(
        variant_id="teddy_g",
        name="Option G - Hero Plush",
        silhouette_type="Option A base with stronger chest posture",
        proportion_style="Confident protagonist stance",
        readability_focus="Heroic shape without noise",
        style_notes="Slightly stronger torso and intentional hat stance.",
        head_scale=1.00,
        ear_scale=1.00,
        body_width_scale=1.08,
        body_height_scale=0.96,
        cheek_scale=0.04,
        hat_scale=0.88,
        plush_family_role="stylized",
    ),
    TeddyShapeVariant(
        variant_id="teddy_h",
        name="Option H - Extra Cute Chibi Plush",
        silhouette_type="Option A pushed toward cute/chibi proportions",
        proportion_style="Slightly bigger head, smaller body",
        readability_focus="Cuteness while preserving motion readability",
        style_notes="Increased head dominance and gentle ear emphasis.",
        head_scale=1.12,
        ear_scale=1.10,
        body_width_scale=0.86,
        body_height_scale=0.78,
        cheek_scale=0.22,
        hat_scale=0.76,
        plush_family_role="stylized",
    ),
    TeddyShapeVariant(
        variant_id="teddy_i",
        name="Option I - Party Plush Star",
        silhouette_type="Option A baseline with stronger party accent",
        proportion_style="Theme-forward but clean",
        readability_focus="Party identity with player-first readability",
        style_notes="Brighter hat and tiny bow accent feel.",
        head_scale=1.01,
        ear_scale=1.00,
        body_width_scale=0.98,
        body_height_scale=0.90,
        cheek_scale=0.06,
        hat_scale=1.24,
        plush_family_role="stylized",
    ),
    TeddyShapeVariant(
        variant_id="teddy_j",
        name="Option J - Clean Premium Plush",
        silhouette_type="Option A refined minimal placement",
        proportion_style="Simple, polished premium framing",
        readability_focus="Maximum cleanliness under scaling",
        style_notes="Minimal details with precise spacing.",
        head_scale=0.99,
        ear_scale=0.96,
        body_width_scale=0.94,
        body_height_scale=0.90,
        cheek_scale=0.00,
        hat_scale=0.78,
        plush_family_role="stylized",
    ),
    TeddyShapeVariant(
        variant_id="bunny_f",
        name="Softer Plush Deluxe Bunny",
        silhouette_type="Large plush head + small body + long rounded ears",
        proportion_style="Softer plush deluxe family",
        readability_focus="Long-ear silhouette readability",
        style_notes="Rounded long ears keep bunny identity clear at gameplay size.",
        head_scale=1.04,
        ear_scale=1.10,
        body_width_scale=0.92,
        body_height_scale=0.86,
        cheek_scale=0.12,
        hat_scale=0.82,
        animal_type="bunny",
        ear_type="long_round",
        plush_family_role="new_plush_cast",
    ),
    TeddyShapeVariant(
        variant_id="fox_f",
        name="Softer Plush Deluxe Fox",
        silhouette_type="Large plush head + small body + soft triangular ears",
        proportion_style="Softer plush deluxe family",
        readability_focus="Fox ear silhouette without sharp noise",
        style_notes="Soft triangular ears and warm tones signal fox while staying plush.",
        head_scale=1.03,
        ear_scale=1.02,
        body_width_scale=0.90,
        body_height_scale=0.85,
        cheek_scale=0.08,
        hat_scale=0.82,
        animal_type="fox",
        ear_type="soft_tri",
        plush_family_role="new_plush_cast",
    ),
    TeddyShapeVariant(
        variant_id="cat_f",
        name="Softer Plush Deluxe Cat",
        silhouette_type="Large plush head + small body + compact soft cat ears",
        proportion_style="Softer plush deluxe family",
        readability_focus="Compact cat silhouette distinction",
        style_notes="Compact ears and cooler palette keep cat distinct from fox.",
        head_scale=1.01,
        ear_scale=0.98,
        body_width_scale=0.90,
        body_height_scale=0.84,
        cheek_scale=0.06,
        hat_scale=0.82,
        animal_type="cat",
        ear_type="compact_tri",
        plush_family_role="new_plush_cast",
    ),
)


STYLIZED_TEDDY_VARIANT_IDS: tuple[str, ...] = (
    "teddy_f",
    "teddy_g",
    "teddy_h",
    "teddy_i",
    "teddy_j",
)


SOFTER_PLUSH_DELUXE_VARIANT_IDS: tuple[str, ...] = (
    "teddy_f",
    "bunny_f",
    "fox_f",
    "cat_f",
)


TEDDY_FINALIST_NOTES: dict[str, str] = {
    "teddy_a": "Baseline winner for readability and simplicity.",
    "teddy_g": "Heroic silhouette with strong protagonist feel.",
    "teddy_j": "Premium clean profile that scales exceptionally well.",
}


PLUSH_CAST_CANDIDATE_NOTES: dict[str, str] = {
    "teddy_f": "Style anchor for softer plush deluxe direction.",
    "bunny_f": "Strong long-ear silhouette and friendly contrast.",
    "fox_f": "Distinct fox identity while preserving plush softness.",
    "cat_f": "Compact cat profile with strong gameplay readability.",
}


def get_style_guide_lines() -> tuple[str, ...]:
    return tuple(f"{key}: {value}" for key, value in SOFTER_PLUSH_STYLE_GUIDE.items())


def draw_teddy_shape_variant(
    surface: pygame.Surface,
    *,
    player: Player,
    variant: TeddyShapeVariant,
    anchor: tuple[int, int],
    offset: tuple[int, int],
    show_outline: bool,
    show_shadow: bool,
) -> None:
    center_anchor = pygame.Vector2(anchor[0] + offset[0], anchor[1] + offset[1])
    facing = pygame.Vector2(player.facing)
    if facing.length_squared() <= 0.0:
        facing = pygame.Vector2(1.0, 0.0)
    else:
        facing = facing.normalize()
    side = pygame.Vector2(-facing.y, facing.x)

    base = float(player.size)
    bounce = math.sin(player.movement_phase * 0.58) * (player.movement_intensity * 2.5)
    bounce += player.movement_juice * 1.4
    center_anchor.y -= bounce

    body_w = max(16.0, base * 0.58 * variant.body_width_scale)
    body_h = max(14.0, base * 0.50 * variant.body_height_scale)
    body_center = center_anchor - pygame.Vector2(0.0, body_h * 0.52)

    head_r = max(12.0, base * 0.31 * variant.head_scale)
    head_center = body_center - pygame.Vector2(0.0, (body_h * 0.50) + (head_r * 0.68))

    palette = _palette_for_variant(variant.variant_id)
    outline_width = 2 if show_outline else 0

    _draw_ears(surface, head_center, head_r, variant, palette, outline_width)

    body_rect = pygame.Rect(0, 0, int(body_w), int(body_h))
    body_rect.center = (int(body_center.x), int(body_center.y))
    pygame.draw.ellipse(surface, palette["body"], body_rect)
    inner_body = body_rect.inflate(-max(4, int(body_w * 0.24)), -max(4, int(body_h * 0.26)))
    pygame.draw.ellipse(surface, palette["inner"], inner_body)
    if outline_width > 0:
        pygame.draw.ellipse(surface, palette["outline"], body_rect, width=outline_width)

    pygame.draw.circle(surface, palette["body"], (int(head_center.x), int(head_center.y)), int(head_r))
    if outline_width > 0:
        pygame.draw.circle(surface, palette["outline"], (int(head_center.x), int(head_center.y)), int(head_r), width=outline_width)

    face_center = head_center + (facing * (head_r * 0.08)) + (side * (head_r * 0.02))
    eye_offset_x = head_r * 0.24
    eye_y = face_center.y - (head_r * 0.12)
    eye_r = max(2.0, head_r * 0.10)
    pygame.draw.circle(surface, palette["eye"], (int(face_center.x - eye_offset_x), int(eye_y)), int(eye_r))
    pygame.draw.circle(surface, palette["eye"], (int(face_center.x + eye_offset_x), int(eye_y)), int(eye_r))

    if variant.cheek_scale > 0.0:
        cheek_r = max(2.0, head_r * 0.10 * (1.0 + variant.cheek_scale))
        cheek_y = eye_y + (head_r * 0.23)
        pygame.draw.circle(surface, palette["cheek"], (int(face_center.x - (eye_offset_x * 1.05)), int(cheek_y)), int(cheek_r))
        pygame.draw.circle(surface, palette["cheek"], (int(face_center.x + (eye_offset_x * 1.05)), int(cheek_y)), int(cheek_r))

    nose_center = face_center + (facing * (head_r * 0.13)) + pygame.Vector2(0.0, head_r * 0.16)
    pygame.draw.circle(surface, palette["eye"], (int(nose_center.x), int(nose_center.y)), max(2, int(head_r * 0.09)))

    if variant.hat_enabled and variant.accessory_style == "party_hat":
        _draw_party_hat(surface, head_center, head_r, facing, variant, palette, outline_width)


def _draw_ears(
    surface: pygame.Surface,
    head_center: pygame.Vector2,
    head_r: float,
    variant: TeddyShapeVariant,
    palette: dict[str, tuple[int, int, int]],
    outline_width: int,
) -> None:
    ear_r = max(5.0, head_r * 0.30 * variant.ear_scale)
    if variant.ear_type == "round":
        ear_offset_x = head_r * 0.56
        ear_offset_y = head_r * 0.68
        for sign in (-1.0, 1.0):
            ear_center = head_center + pygame.Vector2(sign * ear_offset_x, -ear_offset_y)
            pygame.draw.circle(surface, palette["body"], (int(ear_center.x), int(ear_center.y)), int(ear_r))
            if outline_width > 0:
                pygame.draw.circle(surface, palette["outline"], (int(ear_center.x), int(ear_center.y)), int(ear_r), width=outline_width)
            inner_r = max(2.0, ear_r * 0.52)
            pygame.draw.circle(surface, palette["inner_ear"], (int(ear_center.x), int(ear_center.y)), int(inner_r))
        return

    if variant.ear_type == "long_round":
        ear_w = max(8.0, head_r * 0.42 * variant.ear_scale)
        ear_h = max(14.0, head_r * 1.22 * variant.ear_scale)
        ear_offset_x = head_r * 0.45
        ear_base_y = head_r * 1.44
        for sign in (-1.0, 1.0):
            rect = pygame.Rect(0, 0, int(ear_w), int(ear_h))
            rect.midbottom = (int(head_center.x + sign * ear_offset_x), int(head_center.y - ear_base_y))
            pygame.draw.ellipse(surface, palette["body"], rect)
            if outline_width > 0:
                pygame.draw.ellipse(surface, palette["outline"], rect, width=outline_width)
            inner = rect.inflate(-max(2, int(ear_w * 0.35)), -max(4, int(ear_h * 0.30)))
            pygame.draw.ellipse(surface, palette["inner_ear"], inner)
        return

    if variant.ear_type in ("soft_tri", "compact_tri"):
        height_factor = 0.82 if variant.ear_type == "soft_tri" else 0.62
        width_factor = 0.72 if variant.ear_type == "soft_tri" else 0.62
        ear_w = max(8.0, head_r * width_factor * variant.ear_scale)
        ear_h = max(8.0, head_r * height_factor * variant.ear_scale)
        ear_offset_x = head_r * (0.54 if variant.ear_type == "soft_tri" else 0.48)
        ear_offset_y = head_r * (0.66 if variant.ear_type == "soft_tri" else 0.60)
        for sign in (-1.0, 1.0):
            apex = (int(head_center.x + sign * ear_offset_x), int(head_center.y - ear_offset_y - ear_h))
            left = (int(head_center.x + sign * (ear_offset_x - (ear_w * 0.5))), int(head_center.y - ear_offset_y))
            right = (int(head_center.x + sign * (ear_offset_x + (ear_w * 0.5))), int(head_center.y - ear_offset_y))
            pygame.draw.polygon(surface, palette["body"], [apex, left, right])
            if outline_width > 0:
                pygame.draw.polygon(surface, palette["outline"], [apex, left, right], width=outline_width)
            inner_apex = (int((apex[0] + left[0] + right[0]) / 3), int(apex[1] + (ear_h * 0.35)))
            inner_left = (int((left[0] + apex[0]) / 2), int(left[1] - (ear_h * 0.10)))
            inner_right = (int((right[0] + apex[0]) / 2), int(right[1] - (ear_h * 0.10)))
            pygame.draw.polygon(surface, palette["inner_ear"], [inner_apex, inner_left, inner_right])
        return

    # fallback
    ear_offset_x = head_r * 0.56
    ear_offset_y = head_r * 0.68
    for sign in (-1.0, 1.0):
        ear_center = head_center + pygame.Vector2(sign * ear_offset_x, -ear_offset_y)
        pygame.draw.circle(surface, palette["body"], (int(ear_center.x), int(ear_center.y)), int(ear_r))


def _draw_party_hat(
    surface: pygame.Surface,
    head_center: pygame.Vector2,
    head_r: float,
    facing: pygame.Vector2,
    variant: TeddyShapeVariant,
    palette: dict[str, tuple[int, int, int]],
    outline_width: int,
) -> None:
    hat_anchor = head_center - (facing * (head_r * 0.06)) - pygame.Vector2(0.0, head_r * 1.02)
    hat_half_w = head_r * 0.30 * variant.hat_scale
    hat_h = head_r * 0.72 * variant.hat_scale
    tilt = max(-0.6, min(0.6, facing.x * 0.45))
    tip_vec = pygame.Vector2(0.0, -hat_h).rotate_rad(tilt)
    brim_vec = pygame.Vector2(hat_half_w, 0.0).rotate_rad(tilt)
    hat_tip = hat_anchor + tip_vec
    hat_left = hat_anchor - brim_vec
    hat_right = hat_anchor + brim_vec
    pygame.draw.polygon(
        surface,
        palette["hat"],
        [(int(hat_tip.x), int(hat_tip.y)), (int(hat_left.x), int(hat_left.y)), (int(hat_right.x), int(hat_right.y))],
    )
    if outline_width > 0:
        pygame.draw.polygon(
            surface,
            palette["outline"],
            [(int(hat_tip.x), int(hat_tip.y)), (int(hat_left.x), int(hat_left.y)), (int(hat_right.x), int(hat_right.y))],
            width=outline_width,
        )
    pygame.draw.circle(surface, palette["hat_pom"], (int(hat_tip.x), int(hat_tip.y)), max(2, int(head_r * 0.10)))


def _palette_for_variant(variant_id: str) -> dict[str, tuple[int, int, int]]:
    base = {
        "body": (215, 162, 114),
        "inner": (236, 198, 152),
        "outline": (250, 245, 234),
        "inner_ear": (247, 217, 182),
        "eye": (42, 34, 29),
        "hat": (90, 200, 255),
        "hat_pom": (255, 110, 145),
        "cheek": (255, 177, 188),
    }
    if variant_id == "teddy_b":
        base["body"] = (225, 174, 124)
        base["inner"] = (244, 206, 160)
    elif variant_id == "teddy_c":
        base["body"] = (206, 154, 110)
        base["inner"] = (232, 193, 149)
        base["hat"] = (120, 216, 255)
    elif variant_id == "teddy_d":
        base["hat"] = (255, 178, 88)
        base["hat_pom"] = (255, 92, 132)
    elif variant_id == "teddy_e":
        base["body"] = (219, 168, 120)
        base["inner"] = (239, 201, 156)
    elif variant_id == "teddy_f":
        base["body"] = (222, 171, 126)
        base["inner"] = (244, 210, 170)
        base["cheek"] = (255, 188, 198)
    elif variant_id == "teddy_g":
        base["body"] = (208, 156, 111)
        base["inner"] = (233, 194, 149)
        base["hat"] = (80, 184, 255)
    elif variant_id == "teddy_h":
        base["body"] = (228, 180, 135)
        base["inner"] = (248, 214, 176)
        base["inner_ear"] = (255, 228, 198)
        base["cheek"] = (255, 196, 204)
    elif variant_id == "teddy_i":
        base["hat"] = (255, 165, 78)
        base["hat_pom"] = (255, 84, 124)
        base["cheek"] = (255, 182, 194)
    elif variant_id == "teddy_j":
        base["body"] = (212, 162, 118)
        base["inner"] = (236, 198, 154)
        base["hat"] = (104, 198, 245)
        base["hat_pom"] = (255, 112, 142)
    elif variant_id == "bunny_f":
        base["body"] = (223, 181, 170)
        base["inner"] = (246, 220, 212)
        base["inner_ear"] = (255, 204, 214)
        base["hat"] = (108, 204, 247)
    elif variant_id == "fox_f":
        base["body"] = (233, 151, 102)
        base["inner"] = (252, 215, 179)
        base["inner_ear"] = (255, 224, 197)
        base["hat"] = (96, 191, 245)
    elif variant_id == "cat_f":
        base["body"] = (172, 178, 206)
        base["inner"] = (219, 223, 242)
        base["inner_ear"] = (246, 214, 232)
        base["hat"] = (120, 205, 250)
    return base
