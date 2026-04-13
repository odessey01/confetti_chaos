"""Focused tests for the reusable weapon visual overlay model."""

from __future__ import annotations

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.weapon_visual_overlays import (  # noqa: E402
    DEFAULT_WEAPON_VISUAL_OVERLAY_OWNER,
    WeaponVisualOverlay,
    WeaponVisualOverlayOwner,
)


class WeaponVisualOverlayTests(unittest.TestCase):
    def test_default_owner_prefers_visual_manager(self) -> None:
        self.assertEqual(
            DEFAULT_WEAPON_VISUAL_OVERLAY_OWNER,
            WeaponVisualOverlayOwner.VISUAL_MANAGER,
        )

    def test_overlay_supports_generic_non_rocket_configuration(self) -> None:
        overlay = WeaponVisualOverlay(
            overlay_id="sparkler_aura_tier_1",
            sprite_path="images/weapons/sparkler/aura_tier_1.png",
            anchor_name="weapon_mount",
            offset_x=6.0,
            offset_y=-12.0,
            rotation_degrees=18.0,
            scale=0.85,
            z_index=3,
            visible=False,
        )

        self.assertEqual(overlay.overlay_id, "sparkler_aura_tier_1")
        self.assertEqual(overlay.anchor_name, "weapon_mount")
        self.assertEqual(overlay.scale, 0.85)
        self.assertFalse(overlay.visible)

    def test_overlay_transform_helpers_return_updated_copies(self) -> None:
        overlay = WeaponVisualOverlay(
            overlay_id="bottle_rocket_tier_1",
            sprite_path="images/weapons/bottle_rocket/tier_1.png",
            anchor_name="weapon_hand_right",
        )

        transformed = overlay.with_transform(
            offset_x=10.0,
            offset_y=-4.0,
            rotation_degrees=30.0,
            scale=1.25,
            z_index=5,
        ).with_visibility(False)

        self.assertEqual(overlay.offset_x, 0.0)
        self.assertTrue(overlay.visible)
        self.assertEqual(transformed.offset_x, 10.0)
        self.assertEqual(transformed.offset_y, -4.0)
        self.assertEqual(transformed.rotation_degrees, 30.0)
        self.assertEqual(transformed.scale, 1.25)
        self.assertEqual(transformed.z_index, 5)
        self.assertFalse(transformed.visible)


if __name__ == "__main__":
    unittest.main()
