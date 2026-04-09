"""Validation tests for player renderer animation frame integration."""

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
from systems.player_visual import PlayerRenderer  # noqa: E402


class PlayerRendererAnimationTests(unittest.TestCase):
    def test_renderer_draws_animation_frame_when_provided(self) -> None:
        surface = pygame.Surface((320, 240), pygame.SRCALPHA)
        renderer = PlayerRenderer()
        player = Player(100, 100, size=80)
        frame = pygame.Surface((24, 24), pygame.SRCALPHA)
        frame.fill((240, 120, 110, 255))
        rect = pygame.Rect(110, 90, 48, 48)

        mode = renderer.draw(
            surface,
            player,
            animation_frame=frame,
            animation_rect=rect,
            animation_flip_x=False,
        )

        self.assertEqual(mode, "animated")

    def test_renderer_falls_back_without_animation_frame(self) -> None:
        surface = pygame.Surface((320, 240), pygame.SRCALPHA)
        renderer = PlayerRenderer()
        player = Player(100, 100, size=80)
        mode = renderer.draw(surface, player)
        self.assertIn(mode, {"shape", "sprite"})


if __name__ == "__main__":
    unittest.main()
