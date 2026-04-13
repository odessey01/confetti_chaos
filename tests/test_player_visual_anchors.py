"""Focused tests for named player-local visual anchors."""

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
from systems.player_visual_anchors import (  # noqa: E402
    DEFAULT_PLAYER_WEAPON_ANCHOR,
    get_player_visual_anchor,
    player_render_anchor,
    resolve_player_visual_anchor,
)


class PlayerVisualAnchorTests(unittest.TestCase):
    def test_player_render_anchor_uses_center_bottom_origin(self) -> None:
        player = Player(200, 140, size=80)

        self.assertEqual(player_render_anchor(player), (240, 220))

    def test_weapon_mount_flips_when_player_faces_left(self) -> None:
        player = Player(200, 140, size=80)
        player.facing = pygame.Vector2(1.0, 0.0)
        right_anchor = resolve_player_visual_anchor(player, DEFAULT_PLAYER_WEAPON_ANCHOR)

        player.facing = pygame.Vector2(-1.0, 0.0)
        left_anchor = resolve_player_visual_anchor(player, DEFAULT_PLAYER_WEAPON_ANCHOR)

        self.assertEqual(right_anchor[1], left_anchor[1])
        self.assertGreater(right_anchor[0], player.rect.centerx)
        self.assertLess(left_anchor[0], player.rect.centerx)

    def test_unknown_anchor_falls_back_to_default_weapon_mount(self) -> None:
        default_anchor = get_player_visual_anchor(DEFAULT_PLAYER_WEAPON_ANCHOR)
        fallback_anchor = get_player_visual_anchor("unknown_anchor")

        self.assertEqual(fallback_anchor, default_anchor)


if __name__ == "__main__":
    unittest.main()
