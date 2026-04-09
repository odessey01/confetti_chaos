"""Validation tests for character passive gameplay modifiers."""

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


class CharacterPassiveValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bounds = pygame.Rect(0, 0, 1280, 720)

    def test_bear_passive_applies_health_and_speed_tradeoff(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(player_animal_id="teddy_f")
        snapshot = session.active_character_passive_snapshot()
        self.assertEqual(snapshot["display_name"], "Bear")
        self.assertEqual(session.player.max_health, 4)
        self.assertAlmostEqual(session.player.speed, session.BASE_PLAYER_SPEED * 0.88, places=5)

    def test_bunny_passive_applies_speed_and_health_tradeoff(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(player_animal_id="bunny_f")
        snapshot = session.active_character_passive_snapshot()
        self.assertEqual(snapshot["display_name"], "Bunny")
        self.assertEqual(session.player.max_health, 2)
        self.assertAlmostEqual(session.player.speed, session.BASE_PLAYER_SPEED * 1.16, places=5)

    def test_cat_passive_increases_projectile_damage(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(player_animal_id="cat_f")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        self.assertEqual(session.projectiles[0].damage, 2)

    def test_cat_passive_increases_incoming_damage(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(player_animal_id="cat_f")
        session._apply_player_contact_damage()
        self.assertEqual(session.player.current_health, 1)

    def test_raccoon_passive_increases_xp_gain(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.start_new_run(player_animal_id="fox_f")
        base_balloon_xp = session.XP_REWARDS["balloon"]
        boosted = int(round(base_balloon_xp * (1.0 + float(session.active_character_passive_snapshot()["xp_gain_mult"]))))
        self.assertGreater(boosted, base_balloon_xp)

    def test_raccoon_passive_expands_pickup_radius(self) -> None:
        bear = GameSession(self.bounds, hazard_count=0)
        bear.start_new_run(player_animal_id="teddy_f")
        fox = GameSession(self.bounds, hazard_count=0)
        fox.start_new_run(player_animal_id="fox_f")

        bear_rect = bear.player_collision_rect()
        drop_offset = bear.XP_PICKUP_RADIUS + 8
        drop_pos = pygame.Vector2(float(bear_rect.right + drop_offset), float(bear_rect.centery))

        bear._spawn_xp_drop(drop_pos, xp_value=4)
        fox._spawn_xp_drop(drop_pos, xp_value=4)
        bear._collect_xp_drops(bear_rect)
        fox._collect_xp_drops(fox.player_collision_rect())

        self.assertEqual(len(bear.xp_drops), 1)
        self.assertEqual(len(fox.xp_drops), 0)


if __name__ == "__main__":
    unittest.main()
