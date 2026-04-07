"""Validation tests for run XP progression and level-up integration."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enemies import BalloonEnemy, BossBalloon  # noqa: E402
from player.projectile import Projectile  # noqa: E402
from systems.game_session import GameSession  # noqa: E402
from systems.run_progression import RunProgression  # noqa: E402


class RunProgressionValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bounds = pygame.Rect(0, 0, 1280, 720)

    def test_progression_gains_levels_and_carries_remainder(self) -> None:
        progression = RunProgression(base_xp_to_next=100, growth_factor=1.2)
        progression.reset()
        gained = progression.gain_xp(250)
        self.assertEqual(gained, 2)
        self.assertEqual(progression.run_level, 3)
        self.assertGreaterEqual(progression.xp, 0)
        self.assertGreater(progression.xp_to_next_level, 100)

    def test_progression_reset_restores_defaults(self) -> None:
        progression = RunProgression(base_xp_to_next=90, growth_factor=1.3)
        progression.gain_xp(900)
        progression.reset()
        self.assertEqual(progression.run_level, 1)
        self.assertEqual(progression.xp, 0)
        self.assertEqual(progression.pending_level_ups, 0)
        self.assertEqual(progression.xp_to_next_level, 90)

    def test_game_session_awards_xp_for_enemy_kills(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        balloon = BalloonEnemy(speed=120.0)
        balloon.position = pygame.Vector2(220, 220)
        session.hazards = [balloon]
        session.projectiles = [
            Projectile(
                position=pygame.Vector2(balloon.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        before_xp = session.run_progress_snapshot()["xp"]
        session._check_projectile_collisions()
        after_xp = session.run_progress_snapshot()["xp"]
        self.assertGreater(after_xp, before_xp)

    def test_boss_defeat_grants_large_xp_bonus(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        boss = BossBalloon(speed=120.0, max_health=2, damage_per_hit=1)
        boss.position = pygame.Vector2(220, 220)
        session.hazards = [boss]
        center = pygame.Vector2(boss.rect.center)
        session.projectiles = [
            Projectile(position=center, direction=pygame.Vector2(1, 0), speed=0.0, lifetime=2.0, size=8, damage=2)
        ]
        before_snapshot = session.run_progress_snapshot()
        session._check_projectile_collisions()
        after_snapshot = session.run_progress_snapshot()
        self.assertGreaterEqual(int(after_snapshot["run_level"]), int(before_snapshot["run_level"]))
        self.assertTrue(
            int(after_snapshot["xp"]) > int(before_snapshot["xp"])
            or int(after_snapshot["run_level"]) > int(before_snapshot["run_level"])
        )

    def test_projectile_cap_starts_at_three_active_and_blocks_fourth(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        self.assertEqual(session.max_active_projectiles, 3)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        session._weapon_cooldown_timer = 0.0
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        session._weapon_cooldown_timer = 0.0
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 3)
        session._weapon_cooldown_timer = 0.0
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 3)

        session.projectiles[0].lifetime = 0.0
        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        session._weapon_cooldown_timer = 0.0
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 3)

    def test_projectile_cap_upgrade_increases_cap_to_max_five(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        effects = session.run_upgrades.effects_snapshot()
        session._apply_player_upgrade_effects(effects)
        self.assertEqual(session.max_active_projectiles, 3)

        session.run_upgrades.stacks["projectile_cap_up"] = 1
        session._apply_player_upgrade_effects(session.run_upgrades.effects_snapshot())
        self.assertEqual(session.max_active_projectiles, 4)

        session.run_upgrades.stacks["projectile_cap_up"] = 2
        session._apply_player_upgrade_effects(session.run_upgrades.effects_snapshot())
        self.assertEqual(session.max_active_projectiles, 5)
        self.assertFalse(session.run_upgrades.is_valid_choice("projectile_cap_up"))
