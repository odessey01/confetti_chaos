"""Validation tests for spawn controller behavior."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.spawn_controller import SpawnController  # noqa: E402
from enemies import Hazard, TrackingHazard  # noqa: E402


class DeterministicRng:
    def __init__(self) -> None:
        self._random_values = [0.1, 0.9]
        self._random_idx = 0

    def random(self) -> float:
        value = self._random_values[self._random_idx % len(self._random_values)]
        self._random_idx += 1
        return value

    def choice(self, seq: tuple[str, ...] | list[str]) -> str:
        return seq[0]

    def uniform(self, a: float, b: float) -> float:
        return (a + b) / 2.0


class SpawnControllerValidationTests(unittest.TestCase):
    def test_create_hazard_produces_distinct_types(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds, tracking_spawn_chance=0.5, rng=DeterministicRng())
        first = controller.create_hazard(speed=220.0)
        second = controller.create_hazard(speed=220.0)

        self.assertIsInstance(first, TrackingHazard)
        self.assertIsInstance(second, Hazard)

    def test_spawn_positions_respect_safe_distance(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds, safe_spawn_distance=220.0)
        player_center = pygame.Vector2(640, 360)

        for _ in range(50):
            spawn = controller.sample_spawn_position(player_center, hazard_size=34)
            self.assertGreaterEqual(
                spawn.distance_to(player_center),
                220.0 + (34 / 2),
            )

    def test_spawn_timing_scales_with_difficulty_and_is_bounded(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            max_hazards=6,
            base_spawn_interval=2.0,
            min_spawn_interval=0.8,
        )

        controller.reset()
        # 2.5s at easy difficulty should schedule one spawn.
        self.assertEqual(controller.spawn_count_for_frame(2.5, 1.0, active_hazard_count=1), 1)

        controller.reset()
        # Harder difficulty lowers interval and should schedule more spawns.
        self.assertGreaterEqual(
            controller.spawn_count_for_frame(2.5, 2.0, active_hazard_count=1),
            2,
        )

        controller.reset()
        # Spawn count never exceeds available capacity to max_hazards.
        self.assertEqual(
            controller.spawn_count_for_frame(10.0, 5.0, active_hazard_count=5),
            1,
        )
