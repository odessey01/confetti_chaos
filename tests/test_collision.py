"""Validation tests for collision behavior."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.game_session import GameSession  # noqa: E402


class CollisionValidationTests(unittest.TestCase):
    def test_collision_returns_true_when_player_and_hazard_overlap(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        session = GameSession(bounds, hazard_count=1)
        session.player.position.update(100, 100)
        session.hazards[0].position.update(100, 100)
        session.hazards[0].velocity.update(0, 0)

        collided = session.update_playing(0.016, pygame.Vector2(0, 0))

        self.assertTrue(collided)
