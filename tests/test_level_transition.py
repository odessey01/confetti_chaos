"""Validation tests for enemy persistence across level transitions."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enemies import BalloonEnemy  # noqa: E402
from systems.game_session import GameSession  # noqa: E402


class LevelTransitionPersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bounds = pygame.Rect(0, 0, 1280, 720)

    def test_active_hazard_retains_speed_after_level_up(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        hazard = BalloonEnemy(speed=155.0)
        hazard.position = pygame.Vector2(100, 100)
        hazard.velocity = pygame.Vector2(1, 0) * hazard.speed
        session.hazards = [hazard]

        initial_speed = hazard.speed
        session.elapsed_time = 29.9
        session.score_seconds = 29.9

        session.update_playing(2.5, pygame.Vector2(0, 0), attack=False)

        self.assertAlmostEqual(initial_speed, hazard.speed, places=6)
