"""Focused tests for weapon visual asset registration."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.paths import asset_path  # noqa: E402
from systems.weapon_visual_assets import (  # noqa: E402
    get_weapon_visual_asset,
    load_weapon_visual_asset,
)


class WeaponVisualAssetTests(unittest.TestCase):
    def test_bottle_rocket_tier1_asset_is_registered(self) -> None:
        asset = get_weapon_visual_asset("bottle_rocket_tier1")

        self.assertIsNotNone(asset)
        assert asset is not None
        self.assertEqual(asset.sprite_path, "images/weapons/bottle_rocket/tier1.png")
        self.assertEqual(asset.pivot, (18, 32))

    def test_bottle_rocket_tier1_asset_exists_and_loads_with_alpha(self) -> None:
        path = asset_path("images", "weapons", "bottle_rocket", "tier1.png")
        self.assertTrue(path.exists())

        sprite = load_weapon_visual_asset("bottle_rocket_tier1")
        self.assertIsNotNone(sprite)
        assert sprite is not None
        self.assertGreater(sprite.get_width(), 0)
        self.assertGreater(sprite.get_height(), 0)
        self.assertIsNotNone(sprite.get_alpha())


if __name__ == "__main__":
    unittest.main()
