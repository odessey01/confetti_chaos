"""Validation tests for bottle rocket movement behavior."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from player import BottleRocket, BottleRocketFlightProfile  # noqa: E402
from enemies import PinataEnemy  # noqa: E402
from systems.game_session import GameSession  # noqa: E402


class BottleRocketMovementTests(unittest.TestCase):
    def test_bottle_rocket_accelerates_but_respects_speed_cap(self) -> None:
        rocket = BottleRocket(
            position=pygame.Vector2(100.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=400.0,
            lifetime=3.0,
            size=8,
            damage=1,
        )

        for _ in range(120):
            rocket.update(1.0 / 60.0)

        self.assertGreater(rocket.speed, 400.0)
        self.assertLessEqual(
            rocket.speed,
            400.0 * BottleRocketFlightProfile().max_speed_multiplier + 0.001,
        )

    def test_bottle_rocket_wobble_stays_forward_and_readable(self) -> None:
        rocket = BottleRocket(
            position=pygame.Vector2(100.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=500.0,
            lifetime=3.0,
            size=8,
            damage=1,
        )

        observed_nonzero_wobble = False
        for _ in range(90):
            rocket.update(1.0 / 60.0)
            self.assertGreater(rocket.direction.x, 0.95)
            if abs(rocket.direction.y) > 0.001:
                observed_nonzero_wobble = True

        self.assertTrue(observed_nonzero_wobble)

    def test_bottle_rocket_emits_short_lived_trail_segments(self) -> None:
        rocket = BottleRocket(
            position=pygame.Vector2(100.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=500.0,
            lifetime=3.0,
            size=8,
            damage=1,
        )

        for _ in range(20):
            rocket.update(1.0 / 60.0)
        self.assertGreater(len(rocket._trail_segments), 0)

        rocket._trail_emit_timer = 999.0
        for _ in range(30):
            rocket.update(1.0 / 20.0)
        self.assertEqual(len(rocket._trail_segments), 0)

    def test_trail_segments_capture_late_flight_instability(self) -> None:
        profile = BottleRocketFlightProfile(
            decay_start_life_fraction=0.2,
            downward_arc_per_second=0.6,
            speed_decay_per_second=180.0,
        )
        rocket = BottleRocket(
            position=pygame.Vector2(100.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=450.0,
            lifetime=1.0,
            size=8,
            damage=1,
            flight_profile=profile,
        )
        for _ in range(45):
            rocket.update(1.0 / 60.0)
        instabilities = [segment[2] for segment in rocket._trail_segments]
        self.assertTrue(instabilities)
        self.assertGreater(max(instabilities), 0.0)

    def test_bottle_rocket_supports_custom_flight_profile(self) -> None:
        profile = BottleRocketFlightProfile(
            wobble_degrees=0.0,
            wobble_frequency_hz=5.0,
            acceleration_per_second=0.0,
            max_speed_multiplier=1.0,
            trail_emit_interval=0.2,
            trail_segment_lifetime=0.1,
            trail_segment_limit=2,
        )
        rocket = BottleRocket(
            position=pygame.Vector2(100.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=420.0,
            lifetime=2.0,
            size=8,
            damage=1,
            flight_profile=profile,
        )

        rocket.update(0.1)

        self.assertAlmostEqual(rocket.speed, 420.0, places=5)
        self.assertAlmostEqual(rocket.direction.y, 0.0, places=5)
        self.assertLessEqual(len(rocket._trail_segments), 2)

    def test_bottle_rocket_expires_after_max_travel_distance(self) -> None:
        rocket = BottleRocket(
            position=pygame.Vector2(100.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=500.0,
            lifetime=8.0,
            max_travel_distance=120.0,
            size=8,
            damage=1,
        )
        for _ in range(60):
            rocket.update(1.0 / 60.0)
            if rocket.is_expired():
                break
        self.assertTrue(rocket.is_expired())
        self.assertGreaterEqual(rocket.distance_traveled, 120.0)

    def test_bottle_rocket_decay_reduces_speed_and_adds_late_arc(self) -> None:
        profile = BottleRocketFlightProfile(
            wobble_degrees=0.0,
            wobble_frequency_hz=5.0,
            acceleration_per_second=0.0,
            max_speed_multiplier=1.0,
            decay_start_life_fraction=0.25,
            speed_decay_per_second=220.0,
            downward_arc_per_second=0.8,
        )
        rocket = BottleRocket(
            position=pygame.Vector2(120.0, 100.0),
            direction=pygame.Vector2(1.0, 0.0),
            speed=520.0,
            lifetime=1.0,
            size=8,
            damage=1,
            flight_profile=profile,
        )
        early_speed = rocket.speed
        for _ in range(20):
            rocket.update(1.0 / 60.0)
        mid_y = rocket.direction.y
        for _ in range(35):
            rocket.update(1.0 / 60.0)
        self.assertLess(rocket.speed, early_speed)
        self.assertGreater(rocket.direction.y, mid_y)


class BottleRocketCombatValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bounds = pygame.Rect(0, 0, 1280, 720)

    def test_bottle_rocket_applies_configured_damage_and_is_removed_on_hit(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.position = pygame.Vector2(260.0, 260.0)
        session.hazards = [pinata]
        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(pinata.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=1.0,
                size=8,
                damage=2,
            )
        ]

        session._check_projectile_collisions()

        self.assertEqual(len(session.projectiles), 0)
        self.assertEqual(pinata.health, 1)

    def test_bottle_rocket_cleans_up_when_out_of_bounds(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(-150.0, 150.0),
                direction=pygame.Vector2(-1.0, 0.0),
                speed=100.0,
                lifetime=2.0,
                size=8,
                damage=1,
            )
        ]

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)

        self.assertEqual(len(session.projectiles), 0)

    def test_end_of_range_explosion_uses_direct_hit_only_damage_rules(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.position = pygame.Vector2(260.0, 260.0)
        session.hazards = [pinata]
        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(pinata.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=0.01,
                size=8,
                damage=2,
            )
        ]
        session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.hazards), 1)
        self.assertEqual(pinata.health, 3)

    def test_game_session_applies_tuned_bottle_rocket_range_and_flight_profile(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        rocket = session.projectiles[0]
        self.assertAlmostEqual(rocket.max_travel_distance or 0.0, session.BOTTLE_ROCKET_MAX_TRAVEL_DISTANCE)
        self.assertAlmostEqual(rocket.flight_profile.decay_start_life_fraction, session.BOTTLE_ROCKET_DECAY_START_FRACTION)
        self.assertAlmostEqual(rocket.flight_profile.speed_decay_per_second, session.BOTTLE_ROCKET_DECAY_SPEED_PER_SECOND)

    def test_end_of_range_feedback_is_distinct_from_direct_hit_feedback(self) -> None:
        center = pygame.Vector2(320.0, 240.0)
        direct_hit_session = GameSession(self.bounds, hazard_count=0)
        direct_hit_session._spawn_bottle_rocket_impact_feedback(center, impact_scale=1.0, end_of_range=False)
        direct_count = len(direct_hit_session.confetti.particles)

        end_of_range_session = GameSession(self.bounds, hazard_count=0)
        end_of_range_session._spawn_bottle_rocket_impact_feedback(center, impact_scale=1.0, end_of_range=True)
        range_count = len(end_of_range_session.confetti.particles)

        self.assertNotEqual(direct_count, range_count)
        self.assertGreater(range_count, direct_count)

    def test_bottle_rocket_balance_profile_stays_readable_under_decay(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.player.position.update(280.0, 280.0)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        rocket = session.projectiles[-1]

        min_forward_x = 1.0
        max_abs_y = 0.0
        for _ in range(180):
            rocket.update(1.0 / 60.0)
            min_forward_x = min(min_forward_x, rocket.direction.x)
            max_abs_y = max(max_abs_y, abs(rocket.direction.y))
            if rocket.is_expired():
                break

        self.assertGreater(min_forward_x, 0.82)
        self.assertLess(max_abs_y, 0.56)
        self.assertTrue(rocket.is_expired())


if __name__ == "__main__":
    unittest.main()
