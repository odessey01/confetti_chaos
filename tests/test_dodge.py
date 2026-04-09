"""Validation tests for dodge movement foundation."""

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
from enemies.balloon_enemy import BalloonEnemy  # noqa: E402
from systems.game_session import GameSession  # noqa: E402
from systems.input_controller import InputController  # noqa: E402
from systems.party_animals import PLAYABLE_PARTY_ANIMAL_IDS  # noqa: E402


class DodgeValidationTests(unittest.TestCase):
    def test_player_dodge_moves_player_quickly_in_facing_direction(self) -> None:
        player = Player(100.0, 100.0, size=80, speed=320.0)
        started = player.try_start_dodge(pygame.Vector2(1.0, 0.0))
        self.assertTrue(started)
        start_x = player.position.x
        player.update(player.dodge_duration, pygame.Vector2(0.0, 0.0), pygame.Rect(0, 0, 2000, 2000))
        self.assertGreater(player.position.x - start_x, 80.0)
        self.assertFalse(player.is_dodging)

    def test_player_cannot_start_new_dodge_while_already_dodging(self) -> None:
        player = Player(100.0, 100.0, size=80, speed=320.0)
        self.assertTrue(player.try_start_dodge(pygame.Vector2(1.0, 0.0)))
        self.assertFalse(player.try_start_dodge(pygame.Vector2(0.0, 1.0)))

    def test_player_dodge_respects_cooldown(self) -> None:
        player = Player(100.0, 100.0, size=80, speed=320.0)
        self.assertTrue(player.try_start_dodge(pygame.Vector2(1.0, 0.0)))
        player.update(player.dodge_duration, pygame.Vector2(0.0, 0.0), pygame.Rect(0, 0, 2000, 2000))
        self.assertGreater(player.dodge_cooldown_remaining, 0.0)
        self.assertFalse(player.try_start_dodge(pygame.Vector2(1.0, 0.0)))
        player.update(player.dodge_cooldown_duration, pygame.Vector2(0.0, 0.0), pygame.Rect(0, 0, 2000, 2000))
        self.assertTrue(player.try_start_dodge(pygame.Vector2(1.0, 0.0)))

    def test_player_cannot_dodge_when_dead(self) -> None:
        player = Player(100.0, 100.0, size=80, speed=320.0)
        player.set_health(0)
        self.assertFalse(player.try_start_dodge(pygame.Vector2(1.0, 0.0)))

    def test_dodge_invulnerability_window_is_shorter_than_dodge(self) -> None:
        player = Player(100.0, 100.0, size=80, speed=320.0)
        player.try_start_dodge(pygame.Vector2(1.0, 0.0))
        self.assertTrue(player.is_invulnerable)
        player.update(0.1, pygame.Vector2(0.0, 0.0), pygame.Rect(0, 0, 2000, 2000))
        self.assertFalse(player.is_invulnerable)
        self.assertTrue(player.is_dodging)

    def test_dodge_invulnerability_prevents_contact_damage_briefly(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="bunny_f")
        session.player.position.update(100.0, 100.0)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(100.0, 100.0)
        hazard.velocity.update(0.0, 0.0)
        session.hazards = [hazard]
        session.trigger_player_dodge(pygame.Vector2(1.0, 0.0))

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(session.player.current_health, session.player.max_health)

    def test_game_session_exposes_dodge_trigger(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        before_particles = len(session.confetti.particles)
        triggered = session.trigger_player_dodge(pygame.Vector2(1.0, 0.0))
        self.assertTrue(triggered)
        self.assertTrue(session.player.is_dodging)
        self.assertGreater(len(session.confetti.particles), before_particles)

    def test_input_controller_dodge_binding_recognizes_shift(self) -> None:
        controller = InputController()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LSHIFT})
        self.assertTrue(controller.is_dodge(event))

    def test_input_controller_weapon_toggle_recognizes_keyboard_and_controller(self) -> None:
        controller = InputController()
        keyboard_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_t})
        self.assertTrue(controller.is_weapon_toggle(keyboard_event))
        controller_event = pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 4})
        self.assertTrue(controller.is_weapon_toggle(controller_event))

    def test_dodge_is_available_for_all_playable_characters(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        baseline_duration = session.player.dodge_duration
        baseline_distance = session.player.dodge_distance
        for character_id in PLAYABLE_PARTY_ANIMAL_IDS:
            session.start_new_run(player_animal_id=character_id)
            self.assertTrue(session.trigger_player_dodge(pygame.Vector2(1.0, 0.0)))
            self.assertAlmostEqual(session.player.dodge_duration, baseline_duration, places=6)
            self.assertAlmostEqual(session.player.dodge_distance, baseline_distance, places=6)


if __name__ == "__main__":
    unittest.main()
