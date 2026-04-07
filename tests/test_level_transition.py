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

from enemies import BalloonEnemy, BossBalloon, TrackingHazard  # noqa: E402
from systems.game_session import GameSession  # noqa: E402
from systems.settings import MAX_START_LEVEL, MIN_START_LEVEL, clamp_selected_start_level  # noqa: E402


class LevelTransitionPersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bounds = pygame.Rect(0, 0, 1280, 720)

    def test_active_hazard_retains_speed_after_level_up(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        hazard = BalloonEnemy(speed=155.0)
        hazard.position = pygame.Vector2(100, 100)
        hazard.velocity = pygame.Vector2(1, 0) * hazard.speed
        level_config = session.current_level_config
        hazard.capture_spawn_snapshot(level=level_config.level, flavor=level_config.flavor.name)
        session.hazards = [hazard]

        initial_speed = hazard.speed
        initial_snapshot = dict(hazard.spawn_snapshot or {})
        initial_profile = dict(hazard.spawn_profile or {})
        session.elapsed_time = 29.9
        session.score_seconds = 29.9

        session.update_playing(2.5, pygame.Vector2(0, 0), attack=False)

        self.assertAlmostEqual(initial_speed, hazard.speed, places=6)
        self.assertEqual(initial_snapshot, hazard.spawn_snapshot)
        self.assertEqual(initial_profile, hazard.spawn_profile)

    def test_active_boss_health_and_tracking_behavior_persist_through_level_up(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)

        tracker = TrackingHazard(speed=170.0, retarget_interval=1.25, max_retargets=5)
        tracker.position = pygame.Vector2(120, 120)
        tracker.velocity = pygame.Vector2(0, 0)
        tracker.capture_spawn_snapshot(
            level=session.current_level_config.level,
            flavor=session.current_level_config.flavor.name,
        )

        boss = BossBalloon(speed=110.0)
        boss.health = 2
        boss.position = pygame.Vector2(220, 220)
        boss.velocity = pygame.Vector2(0, 0)
        boss.capture_spawn_snapshot(
            level=session.current_level_config.level,
            flavor=session.current_level_config.flavor.name,
        )

        tracker_behavior = (tracker.retarget_interval, tracker.max_retargets)
        boss_health = boss.health
        session.hazards = [tracker, boss]

        session.elapsed_time = 29.9
        session.score_seconds = 29.9
        session.update_playing(2.5, pygame.Vector2(0, 0), attack=False)

        self.assertEqual((tracker.retarget_interval, tracker.max_retargets), tracker_behavior)
        self.assertEqual(boss.health, boss_health)

    def test_newly_spawned_enemy_gets_new_level_snapshot_only(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        old_level_config = session.current_level_config

        existing = BalloonEnemy(speed=140.0)
        existing.position = pygame.Vector2(150, 150)
        existing.velocity = pygame.Vector2(0, 0)
        existing.capture_spawn_snapshot(
            level=old_level_config.level,
            flavor=old_level_config.flavor.name,
        )
        session.hazards = [existing]

        session.elapsed_time = 29.9
        session.score_seconds = 29.9
        session.update_playing(2.5, pygame.Vector2(0, 0), attack=False)

        spawned = [hazard for hazard in session.hazards if hazard is not existing]
        self.assertGreaterEqual(len(spawned), 1)
        self.assertEqual(existing.spawn_snapshot["level"], 1)
        self.assertEqual(existing.spawn_profile["tier"], 1)
        for hazard in spawned:
            self.assertIsNotNone(hazard.spawn_snapshot)
            self.assertEqual(hazard.spawn_snapshot["level"], 2)
            self.assertIsNotNone(hazard.spawn_profile)
            self.assertIn(hazard.spawn_profile["tier"], (1, 2))

    def test_boss_spawns_with_velocity_and_moves(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.elapsed_time = 119.9
        session.score_seconds = 0.0

        session.update_playing(0.2, pygame.Vector2(0, 0), attack=False)

        bosses = [hazard for hazard in session.hazards if isinstance(hazard, BossBalloon)]
        self.assertEqual(len(bosses), 1)
        boss = bosses[0]
        self.assertGreater(boss.velocity.length_squared(), 0.0)

        before = boss.position.copy()
        session.update_playing(0.2, pygame.Vector2(0, 0), attack=False)
        self.assertNotEqual(before, boss.position)

    def test_spawn_telemetry_snapshot_exposes_level_flavor_and_boss_context(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        snapshot = session.spawn_telemetry_snapshot(limit=20)
        self.assertIn("current_level", snapshot)
        self.assertIn("active_flavor", snapshot)
        self.assertIn("boss_override_active", snapshot)
        self.assertIn("spawn_summary", snapshot)
        self.assertGreaterEqual(snapshot["spawn_summary"]["events_considered"], 0)

    def test_start_new_run_uses_selected_start_level(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(start_level=4)
        self.assertEqual(session.current_level, 4)

    def test_start_level_is_clamped_to_valid_range(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(start_level=999)
        self.assertEqual(session.current_level, MAX_START_LEVEL)
        session.start_new_run(start_level=-5)
        self.assertEqual(session.current_level, MIN_START_LEVEL)
        self.assertEqual(clamp_selected_start_level(0), MIN_START_LEVEL)
