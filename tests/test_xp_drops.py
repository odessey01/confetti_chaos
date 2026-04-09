"""Validation tests for XP drop world entities."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pickups import XpDrop  # noqa: E402
from systems.game_session import GameSession  # noqa: E402


class XpDropValidationTests(unittest.TestCase):
    def test_xp_drop_stores_xp_value_and_rect(self) -> None:
        drop = XpDrop(pygame.Vector2(120.0, 210.0), xp_value=7)
        self.assertEqual(drop.xp_value, 7)
        self.assertEqual(drop.rect.center, (120, 210))

    def test_session_can_spawn_world_xp_drop_entity(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session._spawn_xp_drop(pygame.Vector2(300.0, 220.0), xp_value=5)
        self.assertEqual(len(session.xp_drops), 1)
        self.assertEqual(session.xp_drops[0].xp_value, 5)

    def test_xp_drop_draw_supports_multiple_value_tiers(self) -> None:
        surface = pygame.Surface((320, 240), pygame.SRCALPHA)
        drops = (
            XpDrop(pygame.Vector2(50.0, 80.0), xp_value=2),
            XpDrop(pygame.Vector2(120.0, 80.0), xp_value=7),
            XpDrop(pygame.Vector2(190.0, 80.0), xp_value=15),
        )
        for drop in drops:
            drop.update(0.016)
            drop.draw(surface)
        self.assertIsInstance(surface, pygame.Surface)

    def test_collecting_xp_drop_awards_xp_and_removes_drop(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        player_center = pygame.Vector2(session.player_collision_rect().center)
        session._spawn_xp_drop(player_center, xp_value=6)
        before = session.run_progress_snapshot()
        session._collect_xp_drops(session.player_collision_rect())
        after = session.run_progress_snapshot()
        self.assertEqual(len(session.xp_drops), 0)
        self.assertGreaterEqual(int(after["xp"]), int(before["xp"]) + 6)
        cues = session.consume_audio_cues()
        self.assertGreaterEqual(int(cues["xp_pickup_count"]), 1)

    def test_enemy_xp_values_are_centralized_and_tiered(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        values = session.XP_DROP_VALUES
        required_kinds = (
            "balloon",
            "pinata",
            "confetti_sprayer",
            "streamer_snake",
            "boss_balloon",
        )
        for kind in required_kinds:
            self.assertIn(kind, values)
            self.assertGreater(values[kind], 0)
        self.assertLessEqual(values["balloon"], values["pinata"])
        self.assertLessEqual(values["balloon"], values["confetti_sprayer"])
        self.assertLessEqual(values["balloon"], values["streamer_snake"])
        self.assertGreater(values["boss_balloon"], values["pinata"])

    def test_xp_drop_expires_after_lifetime(self) -> None:
        drop = XpDrop(
            pygame.Vector2(100.0, 100.0),
            xp_value=4,
            lifetime_seconds=0.05,
            fade_duration_seconds=0.02,
        )
        self.assertFalse(drop.is_expired())
        drop.update(0.06)
        self.assertTrue(drop.is_expired())
        self.assertEqual(drop.draw_alpha(), 0)

    def test_session_removes_expired_xp_drops(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.xp_drops = [
            XpDrop(pygame.Vector2(300.0, 200.0), xp_value=3, lifetime_seconds=0.01),
            XpDrop(pygame.Vector2(500.0, 200.0), xp_value=5, lifetime_seconds=1.0),
        ]
        session.update_playing(0.05, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.xp_drops), 1)
        self.assertEqual(session.xp_drops[0].xp_value, 5)

    def test_pickup_radius_collects_without_direct_overlap(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        player_rect = session.player_collision_rect()
        drop_x = player_rect.right + max(4, session.XP_PICKUP_RADIUS - 2)
        drop_pos = pygame.Vector2(float(drop_x), float(player_rect.centery))
        session._spawn_xp_drop(drop_pos, xp_value=4)
        before_xp = int(session.run_progress_snapshot()["xp"])
        session._collect_xp_drops(player_rect)
        after_xp = int(session.run_progress_snapshot()["xp"])
        self.assertEqual(len(session.xp_drops), 0)
        self.assertGreaterEqual(after_xp, before_xp + 4)

    def test_xp_drop_magnetism_pulls_toward_player(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        player_center = pygame.Vector2(session.player_collision_rect().center)
        start_pos = player_center + pygame.Vector2(session.XP_MAGNET_RADIUS - 8.0, 0.0)
        drop = XpDrop(start_pos, xp_value=3, lifetime_seconds=1.0)
        session.xp_drops = [drop]
        before_distance = (player_center - drop.position).length()
        session._apply_xp_drop_magnetism(player_center, 0.2)
        after_distance = (player_center - drop.position).length()
        self.assertLess(after_distance, before_distance)

    def test_higher_xp_drop_spawns_with_larger_visual_size(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        low = session._xp_drop_size_for_value(session.XP_DROP_VALUES["balloon"])
        high = session._xp_drop_size_for_value(session.XP_DROP_VALUES["boss_balloon"])
        self.assertGreater(high, low)


if __name__ == "__main__":
    unittest.main()
