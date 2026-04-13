"""Focused tests for data-driven weapon visual definitions."""

from __future__ import annotations

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.weapon_visuals import (  # noqa: E402
    get_weapon_visual_variant,
    resolve_weapon_visual_variant_id,
    weapon_ids_with_visuals,
)


class WeaponVisualDefinitionTests(unittest.TestCase):
    def test_bottle_rocket_named_variants_are_registered(self) -> None:
        tier1 = get_weapon_visual_variant("bottle_rocket", "tier1")
        tier2 = get_weapon_visual_variant("bottle_rocket", "tier2")
        tier3 = get_weapon_visual_variant("bottle_rocket", "tier3")

        self.assertIsNotNone(tier1)
        self.assertIsNotNone(tier2)
        self.assertIsNotNone(tier3)

    def test_tier1_visual_definition_contains_required_fields(self) -> None:
        variant = get_weapon_visual_variant("bottle_rocket", "tier1")

        self.assertIsNotNone(variant)
        assert variant is not None
        self.assertEqual(variant.weapon_id, "bottle_rocket")
        self.assertEqual(variant.default_overlay_sprite, "bottle_rocket_tier1")
        self.assertEqual(variant.anchor_name, "weapon_mount")
        self.assertIn("left", variant.offsets_by_facing)
        self.assertIn("right", variant.offsets_by_facing)
        self.assertGreater(variant.scale, 0.0)
        self.assertEqual(variant.draw_layer, 1)
        self.assertIsNotNone(variant.animation_profile)
        self.assertIsNotNone(variant.vfx_hook_id)
        self.assertIsNotNone(variant.trail_hook_id)

    def test_variant_resolver_uses_evolution_count_tiers(self) -> None:
        self.assertEqual(
            resolve_weapon_visual_variant_id("bottle_rocket", evolution_count=0),
            "tier1",
        )
        self.assertEqual(
            resolve_weapon_visual_variant_id("bottle_rocket", evolution_count=1),
            "tier2",
        )
        self.assertEqual(
            resolve_weapon_visual_variant_id("bottle_rocket", evolution_count=2),
            "tier3",
        )

    def test_registry_is_multi_weapon_ready_with_placeholder_sparkler(self) -> None:
        sparkler = get_weapon_visual_variant("sparkler", "tier1")
        self.assertIsNotNone(sparkler)
        assert sparkler is not None
        self.assertEqual(sparkler.default_overlay_sprite, "sparkler_tier1_placeholder")
        self.assertEqual(resolve_weapon_visual_variant_id("sparkler", evolution_count=0), "tier1")
        self.assertIn("bottle_rocket", weapon_ids_with_visuals())
        self.assertIn("sparkler", weapon_ids_with_visuals())


if __name__ == "__main__":
    unittest.main()
