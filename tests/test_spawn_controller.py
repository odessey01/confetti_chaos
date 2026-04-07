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
from enemies import BalloonEnemy, TrackingHazard  # noqa: E402


class DeterministicRng:
    def __init__(self, random_values: list[float] | None = None) -> None:
        self._random_values = random_values if random_values is not None else [0.1, 0.9]
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
    def test_create_hazard_produces_balloon_variants(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.3,
            balloon_spawn_chance=0.4,
            rng=DeterministicRng([0.1, 0.5, 0.9]),
        )
        first = controller.create_hazard(speed=220.0)
        second = controller.create_hazard(speed=220.0)
        third = controller.create_hazard(speed=220.0)

        self.assertIsInstance(first, TrackingHazard)
        self.assertIsInstance(second, BalloonEnemy)
        self.assertIsInstance(third, BalloonEnemy)
        for hazard in (first, second, third):
            self.assertIsNotNone(hazard.spawn_profile)
            self.assertEqual(hazard.spawn_profile["tier"], 1)
            self.assertEqual(hazard.spawn_profile["flavor_tag"], "STANDARD")
            self.assertIn(
                hazard.spawn_profile["movement_profile"],
                ("tracking_homing", "balloon_drift"),
            )

    def test_spawn_profile_uses_spawn_time_level_and_flavor(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds, rng=DeterministicRng([0.9]))
        hazard = controller.create_hazard_for_spawn(
            tier=4,
            base_speed=240.0,
            flavor_tag="HUNTERS",
        )
        self.assertEqual(hazard.spawn_profile["tier"], 4)
        self.assertEqual(hazard.spawn_profile["flavor_tag"], "HUNTERS")
        self.assertEqual(hazard.spawn_profile["enemy_kind"], "balloon")

    def test_select_spawn_tier_returns_mixed_pool_for_mid_game(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            rng=DeterministicRng([0.10, 0.70, 0.95]),
            tier_weight_template={"newest": 0.55, "previous": 0.30, "older": 0.15},
        )
        self.assertEqual(controller.select_spawn_tier(6), 6)
        self.assertEqual(controller.select_spawn_tier(6), 5)
        self.assertEqual(controller.select_spawn_tier(6), 4)

    def test_tier_pool_decay_retires_older_tiers_over_time(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tier_weight_template={"newest": 0.55, "previous": 0.30, "older": 0.15},
            older_tier_decay_start_level=8,
            older_tier_retire_level=10,
            previous_tier_decay_start_level=12,
            previous_tier_retire_level=14,
        )

        early_pool = controller._tier_pool_for_level(7)
        self.assertEqual([tier for tier, _ in early_pool], [7, 6, 5])

        mid_pool = controller._tier_pool_for_level(9)
        self.assertEqual([tier for tier, _ in mid_pool], [9, 8, 7])

        older_retired_pool = controller._tier_pool_for_level(10)
        self.assertEqual([tier for tier, _ in older_retired_pool], [10, 9])

        previous_retired_pool = controller._tier_pool_for_level(14)
        self.assertEqual([tier for tier, _ in previous_retired_pool], [14])

    def test_spawn_positions_respect_safe_distance(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds, safe_spawn_distance=220.0)
        player_center = pygame.Vector2(640, 360)

        for _ in range(50):
            spawn = controller.sample_spawn_position(player_center, hazard_size=68)
            self.assertGreaterEqual(
                spawn.distance_to(player_center),
                220.0 + (68 / 2),
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

    def test_spawn_telemetry_summary_reports_tier_and_kind_distribution(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds)
        controller.record_spawn_event(
            current_level=5,
            active_flavor="SWARM",
            spawn_tier=5,
            enemy_kind="tracking",
            boss_override_active=False,
        )
        controller.record_spawn_event(
            current_level=5,
            active_flavor="SWARM",
            spawn_tier=4,
            enemy_kind="balloon",
            boss_override_active=False,
        )
        controller.record_spawn_event(
            current_level=5,
            active_flavor="SWARM",
            spawn_tier=5,
            enemy_kind="boss_balloon",
            boss_override_active=True,
        )

        summary = controller.spawn_telemetry_summary(limit=10)
        self.assertEqual(summary["events_considered"], 3)
        self.assertAlmostEqual(summary["tier_distribution"][5], 2 / 3, places=6)
        self.assertAlmostEqual(summary["tier_distribution"][4], 1 / 3, places=6)
        self.assertAlmostEqual(summary["enemy_kind_distribution"]["tracking"], 1 / 3, places=6)
        self.assertAlmostEqual(summary["enemy_kind_distribution"]["balloon"], 1 / 3, places=6)
        self.assertAlmostEqual(summary["enemy_kind_distribution"]["boss_balloon"], 1 / 3, places=6)
        self.assertEqual(summary["boss_override_events"], 1)
