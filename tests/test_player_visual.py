"""Validation tests for player renderer animation frame integration."""

from __future__ import annotations

import pathlib
import sys
import unittest
import types

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

    def test_renderer_uses_bunny_visual_scale_override(self) -> None:
        renderer = PlayerRenderer()
        player = Player(100, 100, size=80)
        player.visual_variant_id = "bunny_f"
        self.assertEqual(renderer._visual_scale_for_player(player), 0.5)  # noqa: SLF001

    def test_renderer_can_hide_direction_indicator(self) -> None:
        surface = pygame.Surface((320, 240), pygame.SRCALPHA)
        renderer = PlayerRenderer()
        player = Player(100, 100, size=80)
        frame = pygame.Surface((24, 24), pygame.SRCALPHA)
        frame.fill((240, 120, 110, 255))
        rect = pygame.Rect(110, 90, 48, 48)
        calls: list[int] = []

        def _fake_indicator(_surface: pygame.Surface, _player: Player) -> None:
            calls.append(1)

        renderer._draw_direction_indicator = types.MethodType(  # type: ignore[method-assign]  # noqa: SLF001
            lambda self, s, p: _fake_indicator(s, p),
            renderer,
        )
        renderer.draw(
            surface,
            player,
            animation_frame=frame,
            animation_rect=rect,
            show_direction_indicator=False,
        )
        self.assertEqual(len(calls), 0)

    def test_renderer_shows_direction_indicator_by_default(self) -> None:
        surface = pygame.Surface((320, 240), pygame.SRCALPHA)
        renderer = PlayerRenderer()
        player = Player(100, 100, size=80)
        frame = pygame.Surface((24, 24), pygame.SRCALPHA)
        frame.fill((240, 120, 110, 255))
        rect = pygame.Rect(110, 90, 48, 48)
        calls: list[int] = []

        def _fake_indicator(_surface: pygame.Surface, _player: Player) -> None:
            calls.append(1)

        renderer._draw_direction_indicator = types.MethodType(  # type: ignore[method-assign]  # noqa: SLF001
            lambda self, s, p: _fake_indicator(s, p),
            renderer,
        )
        renderer.draw(
            surface,
            player,
            animation_frame=frame,
            animation_rect=rect,
        )
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
