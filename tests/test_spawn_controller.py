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
from enemies import BalloonEnemy, ConfettiSprayer, PinataEnemy, StreamerSnake, TrackingHazard  # noqa: E402


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
    def test_create_streamer_snake_for_spawn_sets_expected_profile(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds, rng=DeterministicRng([0.5]))
        hazard = controller.create_streamer_snake_for_spawn(
            tier=6,
            base_speed=240.0,
            flavor_tag="SWARM",
            segment_count=8,
        )
        self.assertIsInstance(hazard, StreamerSnake)
        self.assertEqual(hazard.spawn_profile["enemy_kind"], "streamer_snake")
        self.assertEqual(hazard.spawn_profile["movement_profile"], "streamer_wanderer")
        self.assertEqual(hazard.spawn_profile["tier"], 6)
        self.assertEqual(hazard.spawn_profile["flavor_tag"], "SWARM")
        self.assertEqual(hazard.segment_count, 8)

    def test_streamer_snake_variant_profile_is_configurable(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds, rng=DeterministicRng([0.5]))
        tracker = controller.create_streamer_snake_for_spawn(
            tier=8,
            base_speed=240.0,
            flavor_tag="HUNTERS",
            variant_id="tracker",
        )
        looper = controller.create_streamer_snake_for_spawn(
            tier=8,
            base_speed=240.0,
            flavor_tag="STORM",
            variant_id="looper",
        )
        self.assertEqual(tracker.variant_id, "tracker")
        self.assertEqual(looper.variant_id, "looper")
        self.assertEqual(tracker.spawn_profile["movement_profile"], "streamer_tracker")
        self.assertEqual(looper.spawn_profile["movement_profile"], "streamer_looper")

    def test_create_hazard_produces_balloon_variants(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.3,
            balloon_spawn_chance=0.4,
            rng=DeterministicRng([0.1, 0.5, 0.99]),
        )
        first = controller.create_hazard(speed=220.0)
        second = controller.create_hazard(speed=220.0)
        third = controller.create_hazard(speed=220.0)

        self.assertIsInstance(first, TrackingHazard)
        self.assertIsInstance(second, BalloonEnemy)
        self.assertIsInstance(third, PinataEnemy)
        for hazard in (first, second, third):
            self.assertIsNotNone(hazard.spawn_profile)
            self.assertEqual(hazard.spawn_profile["tier"], 1)
            self.assertEqual(hazard.spawn_profile["flavor_tag"], "STANDARD")
            self.assertIn(
                hazard.spawn_profile["movement_profile"],
                ("tracking_homing", "sprayer_glide", "balloon_drift", "pinata_heavy_drift"),
            )

    def test_spawn_profile_uses_spawn_time_level_and_flavor(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.7,
            rng=DeterministicRng([0.5]),
        )
        hazard = controller.create_hazard_for_spawn(
            tier=4,
            base_speed=240.0,
            flavor_tag="HUNTERS",
        )
        self.assertEqual(hazard.spawn_profile["tier"], 4)
        self.assertEqual(hazard.spawn_profile["flavor_tag"], "HUNTERS")
        self.assertIn(hazard.spawn_profile["enemy_kind"], ("balloon", "confetti_sprayer", "streamer_snake"))

    def test_create_hazard_can_produce_confetti_sprayer_variant(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.3,
            balloon_spawn_chance=0.4,
            rng=DeterministicRng([0.45]),
        )
        hazard = controller.create_hazard_for_spawn(
            tier=14,
            base_speed=220.0,
            flavor_tag="HUNTERS",
        )
        self.assertIsInstance(hazard, ConfettiSprayer)
        self.assertEqual(hazard.spawn_profile["enemy_kind"], "confetti_sprayer")
        self.assertEqual(hazard.spawn_profile["movement_profile"], "sprayer_glide")

    def test_create_hazard_can_produce_streamer_snake_variant(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.7,
            rng=DeterministicRng([0.5]),
        )
        hazard = controller.create_hazard_for_spawn(
            tier=12,
            base_speed=220.0,
            flavor_tag="HUNTERS",
        )
        self.assertIsInstance(hazard, StreamerSnake)
        self.assertEqual(hazard.spawn_profile["enemy_kind"], "streamer_snake")
        self.assertIn(hazard.spawn_profile["movement_profile"], ("streamer_wanderer", "streamer_tracker"))

    def test_streamer_snake_is_not_in_early_tier_spawn_mix(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.7,
            rng=DeterministicRng([0.5]),
        )
        hazard = controller.create_hazard_for_spawn(
            tier=3,
            base_speed=220.0,
            flavor_tag="STANDARD",
        )
        self.assertNotIsInstance(hazard, StreamerSnake)

    def test_streamer_snake_flavor_profiles_change_behavior(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.7,
            rng=DeterministicRng([0.5, 0.5, 0.5]),
        )
        swarm = controller.create_hazard_for_spawn(
            tier=12,
            base_speed=220.0,
            flavor_tag="SWARM",
        )
        hunters = controller.create_hazard_for_spawn(
            tier=12,
            base_speed=220.0,
            flavor_tag="HUNTERS",
        )
        storm = controller.create_hazard_for_spawn(
            tier=12,
            base_speed=220.0,
            flavor_tag="STORM",
        )
        self.assertIsInstance(swarm, StreamerSnake)
        self.assertIsInstance(hunters, StreamerSnake)
        self.assertIsInstance(storm, StreamerSnake)
        self.assertEqual(hunters.variant_id, "tracker")
        self.assertEqual(storm.variant_id, "looper")
        self.assertLess(
            int(swarm.spawn_profile["snake_segment_count"]),
            int(storm.spawn_profile["snake_segment_count"]),
        )
        self.assertLessEqual(
            int(swarm.spawn_profile["snake_segment_count"]),
            int(hunters.spawn_profile["snake_segment_count"]),
        )
        self.assertGreater(float(storm.spawn_profile["speed"]), float(swarm.spawn_profile["speed"]))

    def test_streamer_snake_chance_is_capped_during_boss_context(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(bounds)
        normal = controller._snake_target_chance_for_spawn(
            tier=20,
            flavor_tag="SWARM",
            boss_override_active=False,
        )
        boss = controller._snake_target_chance_for_spawn(
            tier=20,
            flavor_tag="SWARM",
            boss_override_active=True,
        )
        self.assertGreater(normal, boss)
        self.assertAlmostEqual(boss, controller.BOSS_SNAKE_CHANCE_CAP, places=6)

    def test_confetti_sprayer_is_rare_in_early_tiers(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.1,
            balloon_spawn_chance=0.8,
            rng=DeterministicRng([0.45]),
        )
        hazard = controller.create_hazard_for_spawn(
            tier=2,
            base_speed=220.0,
            flavor_tag="STANDARD",
        )
        self.assertNotIsInstance(hazard, ConfettiSprayer)

    def test_confetti_sprayer_chance_is_capped_during_boss_context(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.6,
        )
        normal = controller._sprayer_target_chance_for_spawn(
            tier=20,
            flavor_tag="HUNTERS",
            boss_override_active=False,
        )
        boss = controller._sprayer_target_chance_for_spawn(
            tier=20,
            flavor_tag="HUNTERS",
            boss_override_active=True,
        )
        self.assertGreater(normal, boss)
        self.assertAlmostEqual(boss, controller.BOSS_SPRAYER_CHANCE_CAP, places=6)

    def test_confetti_sprayer_flavor_profiles_change_attack_shape(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.0,
            balloon_spawn_chance=0.8,
            rng=DeterministicRng([0.05, 0.05, 0.05]),
        )
        hunters = controller.create_hazard_for_spawn(
            tier=14,
            base_speed=220.0,
            flavor_tag="HUNTERS",
        )
        storm = controller.create_hazard_for_spawn(
            tier=14,
            base_speed=220.0,
            flavor_tag="STORM",
        )
        self.assertIsInstance(hunters, ConfettiSprayer)
        self.assertIsInstance(storm, ConfettiSprayer)
        self.assertLess(hunters.spawn_profile["spray_angle"], storm.spawn_profile["spray_angle"])
        self.assertLess(hunters.spawn_profile["spray_cooldown"], 2.0)
        self.assertGreater(storm.spawn_profile["spray_projectile_count"], hunters.spawn_profile["spray_projectile_count"])

    def test_pinata_spawn_profile_is_slower_and_distinct(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.2,
            rng=DeterministicRng([0.99]),
        )
        hazard = controller.create_hazard_for_spawn(
            tier=3,
            base_speed=240.0,
            flavor_tag="STANDARD",
        )
        self.assertIsInstance(hazard, PinataEnemy)
        self.assertEqual(hazard.spawn_profile["enemy_kind"], "pinata")
        self.assertEqual(hazard.spawn_profile["movement_profile"], "pinata_heavy_drift")
        self.assertLess(float(hazard.spawn_profile["speed"]), 240.0 * 0.75)

    def test_pinata_spawn_share_increases_with_tier(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.5,
            balloon_spawn_chance=0.4,
        )
        low_tracking, low_balloon, low_pinata = controller._resolve_hazard_mix_for_spawn(
            tier=1,
            tracking_chance=0.5,
            boss_override_active=False,
        )
        high_tracking, high_balloon, high_pinata = controller._resolve_hazard_mix_for_spawn(
            tier=12,
            tracking_chance=0.5,
            boss_override_active=False,
        )
        self.assertAlmostEqual(low_tracking + low_balloon + low_pinata, 1.0, places=6)
        self.assertAlmostEqual(high_tracking + high_balloon + high_pinata, 1.0, places=6)
        self.assertLess(low_pinata, high_pinata)
        self.assertAlmostEqual(low_pinata, controller.MIN_PINATA_CHANCE, places=6)
        self.assertAlmostEqual(high_pinata, controller.MAX_PINATA_CHANCE, places=6)

    def test_boss_context_caps_pinata_spawn_share(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.2,
            balloon_spawn_chance=0.6,
        )
        _, _, normal_pinata = controller._resolve_hazard_mix_for_spawn(
            tier=20,
            tracking_chance=0.2,
            boss_override_active=False,
        )
        _, _, boss_pinata = controller._resolve_hazard_mix_for_spawn(
            tier=20,
            tracking_chance=0.2,
            boss_override_active=True,
        )
        self.assertGreater(normal_pinata, boss_pinata)
        self.assertAlmostEqual(boss_pinata, controller.BOSS_PINATA_CHANCE_CAP, places=6)

    def test_pinata_tier_variants_scale_health_and_rewards(self) -> None:
        bounds = pygame.Rect(0, 0, 1280, 720)
        controller = SpawnController(
            bounds,
            tracking_spawn_chance=0.0,
            balloon_spawn_chance=0.0,
            rng=DeterministicRng([0.99, 0.99, 0.99]),
        )
        low = controller.create_hazard_for_spawn(tier=2, base_speed=240.0, flavor_tag="STANDARD")
        mid = controller.create_hazard_for_spawn(tier=6, base_speed=240.0, flavor_tag="STANDARD")
        high = controller.create_hazard_for_spawn(tier=10, base_speed=240.0, flavor_tag="STANDARD")
        self.assertIsInstance(low, PinataEnemy)
        self.assertIsInstance(mid, PinataEnemy)
        self.assertIsInstance(high, PinataEnemy)
        self.assertEqual(low.spawn_profile["health"], 3)
        self.assertEqual(mid.spawn_profile["health"], 4)
        self.assertEqual(high.spawn_profile["health"], 5)
        self.assertEqual(low.spawn_profile["mini_spawn_count"], 0)
        self.assertEqual(mid.spawn_profile["mini_spawn_count"], 1)
        self.assertEqual(high.spawn_profile["mini_spawn_count"], 2)
        self.assertLess(low.spawn_profile["break_confetti_count"], high.spawn_profile["break_confetti_count"])

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
