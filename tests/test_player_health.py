"""Validation tests for player health and damage cooldown systems."""

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
from systems.game_session import GameSession  # noqa: E402
from systems.ui import UiRenderer  # noqa: E402


class PlayerHealthValidationTests(unittest.TestCase):
    def test_player_starts_with_full_health(self) -> None:
        player = Player(0.0, 0.0)
        self.assertEqual(player.max_health, 3)
        self.assertEqual(player.current_health, 3)

    def test_apply_damage_respects_invulnerability_window(self) -> None:
        player = Player(0.0, 0.0)
        first = player.apply_damage(1)
        second = player.apply_damage(1)
        self.assertTrue(first)
        self.assertFalse(second)
        self.assertEqual(player.current_health, 2)

    def test_health_is_clamped_to_bounds(self) -> None:
        player = Player(0.0, 0.0)
        player.set_health(99)
        self.assertEqual(player.current_health, player.max_health)
        player.set_health(-10)
        self.assertEqual(player.current_health, 0)

    def test_session_damage_audio_cue_emits_on_player_hit(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        session.player.position.update(100, 100)
        session.hazards[0].position.update(100, 100)
        session.hazards[0].velocity.update(0, 0)
        session.update_playing(0.016, pygame.Vector2(0, 0), attack=False)
        cues = session.consume_audio_cues()
        self.assertEqual(cues["player_damage_count"], 1)

    def test_health_ui_draws_without_error(self) -> None:
        if not pygame.get_init():
            pygame.init()
        surface = pygame.Surface((1280, 720))
        ui = UiRenderer()
        ui.draw_health(surface, current_health=2, max_health=3)
        self.assertIsInstance(surface, pygame.Surface)


if __name__ == "__main__":
    unittest.main()
