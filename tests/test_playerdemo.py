"""Validation tests for teddy shape demo infrastructure."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from player import Player  # noqa: E402
from playerdemo import clamp_scale, cycle_variant_index, direction_to_facing  # noqa: E402
from systems.player_demo_sprite import (  # noqa: E402
    direction_to_sprite_mapping,
    hitbox_from_anchor,
    rect_from_center_bottom_anchor,
)
from systems.teddy_shape_variants import (  # noqa: E402
    PLUSH_CAST_CANDIDATE_NOTES,
    SHARED_PLUSH_ACCESSORY_RULES,
    SOFTER_PLUSH_DELUXE_VARIANT_IDS,
    SOFTER_PLUSH_STYLE_GUIDE,
    STYLIZED_TEDDY_VARIANT_IDS,
    TEDDY_FINALIST_NOTES,
    TEDDY_SHAPE_VARIANTS,
    draw_teddy_shape_variant,
)


class PlayerDemoValidationTests(unittest.TestCase):
    def test_teddy_variant_framework_has_stylized_exploration_set(self) -> None:
        self.assertEqual(len(TEDDY_SHAPE_VARIANTS), 13)
        self.assertEqual(len(STYLIZED_TEDDY_VARIANT_IDS), 5)
        for variant in TEDDY_SHAPE_VARIANTS:
            self.assertTrue(variant.name)
            self.assertTrue(variant.silhouette_type)
            self.assertTrue(variant.proportion_style)
            self.assertTrue(variant.readability_focus)

    def test_softer_plush_style_guide_defined(self) -> None:
        required = {"proportions", "shape_language", "face", "silhouette", "accessory", "clarity"}
        self.assertTrue(required.issubset(set(SOFTER_PLUSH_STYLE_GUIDE.keys())))
        self.assertEqual(SHARED_PLUSH_ACCESSORY_RULES["type"], "party_hat")

    def test_softer_plush_cast_contains_teddy_bunny_fox_cat(self) -> None:
        self.assertEqual(len(SOFTER_PLUSH_DELUXE_VARIANT_IDS), 4)
        self.assertIn("teddy_f", SOFTER_PLUSH_DELUXE_VARIANT_IDS)
        self.assertIn("bunny_f", SOFTER_PLUSH_DELUXE_VARIANT_IDS)
        self.assertIn("fox_f", SOFTER_PLUSH_DELUXE_VARIANT_IDS)
        self.assertIn("cat_f", SOFTER_PLUSH_DELUXE_VARIANT_IDS)

    def test_cycle_variant_index_wraps(self) -> None:
        self.assertEqual(cycle_variant_index(0, -1, 13), 12)
        self.assertEqual(cycle_variant_index(12, 1, 13), 0)
        self.assertEqual(cycle_variant_index(2, 1, 13), 3)

    def test_clamp_scale_bounds(self) -> None:
        self.assertEqual(clamp_scale(0.1), 0.6)
        self.assertEqual(clamp_scale(10.0), 2.2)
        self.assertEqual(clamp_scale(1.3), 1.3)

    def test_direction_to_facing_mapping(self) -> None:
        self.assertEqual(direction_to_facing("up"), pygame.Vector2(0.0, -1.0))
        self.assertEqual(direction_to_facing("down"), pygame.Vector2(0.0, 1.0))
        self.assertEqual(direction_to_facing("left"), pygame.Vector2(-1.0, 0.0))
        self.assertEqual(direction_to_facing("right"), pygame.Vector2(1.0, 0.0))

    def test_direction_to_sprite_mapping_matches_expected_faces(self) -> None:
        self.assertEqual(direction_to_sprite_mapping(pygame.Vector2(0, 1)), ("front", False))
        self.assertEqual(direction_to_sprite_mapping(pygame.Vector2(0, -1)), ("rear", False))
        self.assertEqual(direction_to_sprite_mapping(pygame.Vector2(1, 0)), ("side", False))
        self.assertEqual(direction_to_sprite_mapping(pygame.Vector2(-1, 0)), ("side", True))

    def test_rect_from_center_bottom_anchor_aligns_midbottom(self) -> None:
        rect = rect_from_center_bottom_anchor(
            anchor=(320, 240),
            sprite_size=(96, 96),
            offset=(4, -6),
        )
        self.assertEqual(rect.midbottom, (324, 234))

    def test_hitbox_from_anchor_returns_tunable_center_and_radius(self) -> None:
        center, radius = hitbox_from_anchor(
            anchor=(100.0, 200.0),
            radius=20.0,
            vertical_offset=18.0,
        )
        self.assertEqual((center.x, center.y), (100.0, 182.0))
        self.assertEqual(radius, 20.0)

    def test_teddy_shape_renderer_draws_without_errors(self) -> None:
        surface = pygame.Surface((640, 360))
        player = Player(280, 140, size=56)
        player.facing = pygame.Vector2(1.0, 0.0)
        player._movement_intensity = 0.75
        player._movement_juice = 0.6
        player._movement_phase = 1.4
        for variant_id in ("teddy_f", "bunny_f", "fox_f", "cat_f"):
            variant = next(v for v in TEDDY_SHAPE_VARIANTS if v.variant_id == variant_id)
            draw_teddy_shape_variant(
                surface,
                player=player,
                variant=variant,
                anchor=(320, 220),
                offset=(0, 0),
                show_outline=True,
                show_shadow=True,
            )
        self.assertIsInstance(surface, pygame.Surface)

    def test_candidate_notes_cover_plush_cast(self) -> None:
        self.assertIn("teddy_f", PLUSH_CAST_CANDIDATE_NOTES)
        self.assertIn("bunny_f", PLUSH_CAST_CANDIDATE_NOTES)
        self.assertIn("fox_f", PLUSH_CAST_CANDIDATE_NOTES)
        self.assertIn("cat_f", PLUSH_CAST_CANDIDATE_NOTES)

    def test_original_finalist_notes_preserved(self) -> None:
        self.assertIn("teddy_a", TEDDY_FINALIST_NOTES)
        self.assertIn("teddy_g", TEDDY_FINALIST_NOTES)
        self.assertIn("teddy_j", TEDDY_FINALIST_NOTES)


if __name__ == "__main__":
    unittest.main()
