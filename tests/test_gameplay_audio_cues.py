"""Validation tests for gameplay-triggered audio cues."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enemies import BalloonEnemy, BossBalloon, ConfettiSprayer, PinataEnemy  # noqa: E402
from player.projectile import Projectile  # noqa: E402
from systems.game_session import GameSession  # noqa: E402


class GameplayAudioCueValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bounds = pygame.Rect(0, 0, 1280, 720)

    def test_level_transition_sets_audio_cue(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.spawn_controller.max_hazards = 0
        session.score_seconds = 0.0
        session.run_progression.gain_xp(session.run_progression.xp_to_next_level)

        session.update_playing(1.0, pygame.Vector2(0, 0), attack=False)
        cues = session.consume_audio_cues()
        self.assertTrue(cues["level_transition"])
        self.assertFalse(cues["boss_spawn"])

    def test_projectile_hit_and_pop_generate_audio_cues(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        hazard = BalloonEnemy(speed=150.0)
        hazard.position = pygame.Vector2(180, 180)
        projectile = Projectile(
            position=pygame.Vector2(190, 190),
            direction=pygame.Vector2(1, 0),
            speed=0.0,
            lifetime=2.0,
            size=8,
        )
        session.hazards = [hazard]
        session.projectiles = [projectile]

        session._check_projectile_collisions()
        cues = session.consume_audio_cues()
        self.assertEqual(cues["balloon_hit_count"], 1)
        self.assertEqual(cues["balloon_pop_count"], 1)
        self.assertEqual(cues["bottle_rocket_impact_count"], 1)

    def test_bottle_rocket_launch_emits_feedback_cue_and_recoil(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.player.position.update(300.0, 300.0)
        original_x = session.player.position.x
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        cues = session.consume_audio_cues()
        self.assertEqual(cues["bottle_rocket_launch_count"], 1)
        self.assertGreater(len(session.confetti.particles), 0)
        self.assertLess(session.player.position.x, original_x)

    def test_bottle_rocket_expiration_emits_impact_feedback(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.projectiles = [
            Projectile(
                position=pygame.Vector2(300.0, 300.0),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=0.01,
                size=8,
            )
        ]
        session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
        cues = session.consume_audio_cues()
        self.assertEqual(cues["bottle_rocket_impact_count"], 1)
        self.assertGreater(len(session.confetti.particles), 0)

    def test_sparkler_swing_and_hit_emit_audio_cues(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(360.0, 300.0)
        session.hazards = [hazard]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        cues = session.consume_audio_cues()
        self.assertEqual(cues["sparkler_swing_count"], 1)
        self.assertGreaterEqual(cues["sparkler_hit_count"], 1)

    def test_boss_spawn_sets_audio_cue(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        for _ in range(4):
            session.run_progression.gain_xp(session.run_progression.xp_to_next_level)
        session.score_seconds = 0.0
        session.update_playing(0.2, pygame.Vector2(0, 0), attack=False)

        cues = session.consume_audio_cues()
        self.assertTrue(cues["boss_spawn"])

    def test_boss_hit_and_defeat_set_special_event_cues(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        boss = BossBalloon(speed=120.0)
        boss.position = pygame.Vector2(180, 180)
        session.hazards = [boss]

        def _spawn_projectile() -> Projectile:
            center = pygame.Vector2(boss.rect.center)
            return Projectile(
                position=center,
                direction=pygame.Vector2(1, 0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )

        total_hits = boss.max_health
        for _ in range(total_hits - 1):
            session.projectiles = [_spawn_projectile()]
            session._check_projectile_collisions()
            boss.update(0.2, pygame.Vector2(session.player.rect.center))
        # Defeating hit
        session.projectiles = [_spawn_projectile()]
        session._check_projectile_collisions()

        cues = session.consume_audio_cues()
        self.assertEqual(cues["boss_hit_count"], total_hits)
        self.assertTrue(cues["boss_defeat"])
        self.assertTrue(cues["milestone_clear"])
        self.assertTrue(cues["confetti_celebration"])

    def test_boss_duplicate_overlap_hits_are_prevented(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        boss = BossBalloon(speed=120.0)
        boss.position = pygame.Vector2(180, 180)
        session.hazards = [boss]
        center = pygame.Vector2(boss.rect.center)
        session.projectiles = [
            Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8),
            Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8),
        ]
        session._check_projectile_collisions()
        cues = session.consume_audio_cues()
        self.assertEqual(cues["boss_hit_count"], 1)

    def test_boss_phase_change_sets_session_audio_cue(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session._boss_active = True
        boss = BossBalloon(speed=120.0, max_health=6, damage_per_hit=1)
        boss.position = pygame.Vector2(220, 220)
        boss.health = 5  # one hit will cross to phase 2 threshold
        session.hazards = [boss]
        center = pygame.Vector2(boss.rect.center)
        session.projectiles = [
            Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8),
        ]
        session.update_playing(0.1, pygame.Vector2(0, 0), attack=False)
        cues = session.consume_audio_cues()
        self.assertTrue(cues["boss_phase_change"])

    def test_pinata_requires_multiple_hits_before_pop(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.position = pygame.Vector2(220, 220)
        session.hazards = [pinata]

        def _projectile_at_pinata() -> Projectile:
            center = pygame.Vector2(pinata.rect.center)
            return Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8)

        # Hit 1
        session.projectiles = [_projectile_at_pinata()]
        session._check_projectile_collisions()
        pinata.update(0.2, pygame.Vector2(session.player.rect.center))
        # Hit 2
        session.projectiles = [_projectile_at_pinata()]
        session._check_projectile_collisions()
        pinata.update(0.2, pygame.Vector2(session.player.rect.center))
        # Hit 3 defeat
        session.projectiles = [_projectile_at_pinata()]
        session._check_projectile_collisions()

        cues = session.consume_audio_cues()
        self.assertEqual(cues["balloon_hit_count"], 3)
        self.assertEqual(cues["balloon_pop_count"], 1)

    def test_pinata_duplicate_overlap_hits_are_prevented(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.position = pygame.Vector2(220, 220)
        session.hazards = [pinata]
        center = pygame.Vector2(pinata.rect.center)
        session.projectiles = [
            Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8),
            Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8),
        ]
        session._check_projectile_collisions()
        cues = session.consume_audio_cues()
        self.assertEqual(cues["balloon_hit_count"], 1)

    def test_pinata_break_spawns_more_confetti_than_balloon_pop(self) -> None:
        # Baseline balloon pop confetti count
        balloon_session = GameSession(self.bounds, hazard_count=0)
        balloon = BalloonEnemy(speed=120.0)
        balloon.position = pygame.Vector2(220, 220)
        balloon_session.hazards = [balloon]
        balloon_session.projectiles = [
            Projectile(
                position=pygame.Vector2(balloon.rect.center),
                direction=pygame.Vector2(1, 0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        balloon_session._check_projectile_collisions()
        balloon_particles = len(balloon_session.confetti.particles)

        # Pinata break should produce a larger confetti effect
        pinata_session = GameSession(self.bounds, hazard_count=0)
        pinata = PinataEnemy(speed=120.0, max_health=2, damage_per_hit=1)
        pinata.position = pygame.Vector2(220, 220)
        pinata_session.hazards = [pinata]
        pinata_session.projectiles = [
            Projectile(
                position=pygame.Vector2(pinata.rect.center),
                direction=pygame.Vector2(1, 0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        pinata_session._check_projectile_collisions()
        pinata.update(0.2, pygame.Vector2(pinata_session.player.rect.center))
        pinata_session.projectiles = [
            Projectile(
                position=pygame.Vector2(pinata.rect.center),
                direction=pygame.Vector2(1, 0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        pinata_session._check_projectile_collisions()
        pinata_particles = len(pinata_session.confetti.particles)
        self.assertGreater(pinata_particles, balloon_particles)

    def test_sprayer_charge_and_burst_emit_audio_cues(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(220.0, 220.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        sprayer.attack_cooldown_timer = 0.0
        session.hazards = [sprayer]
        charge_seen = False
        burst_seen = False
        for _ in range(12):
            session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
            cues = session.consume_audio_cues()
            if cues["sprayer_charge_count"] > 0:
                charge_seen = True
            if cues["sprayer_burst_count"] > 0:
                burst_seen = True
            if charge_seen and burst_seen:
                break
        self.assertTrue(charge_seen)
        self.assertTrue(burst_seen)

    def test_sprayer_destruction_emits_audio_cue(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(220.0, 220.0)
        session.hazards = [sprayer]
        session.projectiles = [
            Projectile(
                position=pygame.Vector2(sprayer.rect.center),
                direction=pygame.Vector2(1, 0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        session._check_projectile_collisions()
        cues = session.consume_audio_cues()
        self.assertEqual(cues["sprayer_destroy_count"], 1)
