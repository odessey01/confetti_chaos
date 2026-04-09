"""Validation tests for super ability framework."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.character_supers import CHARACTER_SUPER_PROFILES  # noqa: E402
from systems.game_session import GameSession  # noqa: E402
from systems.input_controller import InputController  # noqa: E402
from systems.party_animals import PLAYABLE_PARTY_ANIMAL_IDS  # noqa: E402
from systems.ui import UiRenderer  # noqa: E402
from enemies import BalloonEnemy, BossBalloon  # noqa: E402
from player.projectile import Projectile  # noqa: E402


class SuperSystemValidationTests(unittest.TestCase):
    def test_every_playable_character_has_a_super_profile(self) -> None:
        for character_id in PLAYABLE_PARTY_ANIMAL_IDS:
            self.assertIn(character_id, CHARACTER_SUPER_PROFILES)

    def test_super_charge_resets_on_new_run(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.add_super_charge(50)
        self.assertEqual(session.super_charge, 50)
        session.start_new_run(player_animal_id="cat_f")
        self.assertEqual(session.super_charge, 0)
        self.assertEqual(session.super_snapshot()["character_id"], "cat_f")

    def test_super_activation_requires_full_charge(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        self.assertIsNone(session.try_activate_super())
        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        super_id = session.try_activate_super()
        self.assertIsInstance(super_id, str)
        self.assertEqual(session.super_charge, 0)

    def test_input_controller_super_binding_recognizes_q(self) -> None:
        controller = InputController()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_q})
        self.assertTrue(controller.is_super_activate(event))

    def test_enemy_kill_contributes_super_charge(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        balloon = BalloonEnemy(speed=120.0)
        balloon.position = pygame.Vector2(220.0, 220.0)
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
        session._check_projectile_collisions()
        self.assertGreater(session.super_charge, 0)

    def test_boss_hit_contributes_super_charge_without_defeat(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        boss = BossBalloon(speed=120.0, max_health=3, damage_per_hit=1)
        boss.position = pygame.Vector2(220.0, 220.0)
        session.hazards = [boss]
        session.projectiles = [
            Projectile(
                position=pygame.Vector2(boss.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        session._check_projectile_collisions()
        self.assertGreater(session.super_charge, 0)

    def test_bear_roar_super_pushes_nearby_enemies(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="teddy_f")
        session.player.position.update(300.0, 200.0)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(340.0, 220.0)
        hazard.velocity.update(0.0, 0.0)
        session.hazards = [hazard]

        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        before_distance = pygame.Vector2(hazard.rect.center).distance_to(pygame.Vector2(session.player.rect.center))
        activated = session.try_activate_super()
        after_distance = pygame.Vector2(hazard.rect.center).distance_to(pygame.Vector2(session.player.rect.center))

        self.assertEqual(activated, "bear_roar")
        self.assertGreater(after_distance - before_distance, 40.0)
        self.assertGreater(hazard.velocity.length(), 120.0)
        self.assertTrue(session.player.is_invulnerable)

    def test_bear_roar_applies_inner_radius_chip_damage_to_boss(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="teddy_f")
        session.player.position.update(300.0, 200.0)
        boss = BossBalloon(speed=0.0, max_health=5, damage_per_hit=1)
        boss.position.update(340.0, 210.0)
        boss.velocity.update(0.0, 0.0)
        session.hazards = [boss]

        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        before_health = boss.health
        activated = session.try_activate_super()

        self.assertEqual(activated, "bear_roar")
        self.assertLess(boss.health, before_health)

    def test_bunny_mega_hop_super_repositions_and_grants_invulnerability(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="bunny_f")
        start_x = session.player.position.x
        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        activated = session.try_activate_super()
        self.assertEqual(activated, "bunny_mega_hop")
        self.assertGreater(session.player.position.x, start_x)
        self.assertTrue(session.player.is_invulnerable)

    def test_cat_frenzy_super_boosts_projectile_damage_temporarily(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="cat_f")
        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        activated = session.try_activate_super()
        self.assertEqual(activated, "cat_frenzy")

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        frenzy_damage = session.projectiles[0].damage

        session.projectiles.clear()
        session._weapon_cooldown_timer = 0.0
        session.update_playing(session.CAT_FRENZY_DURATION + 0.1, pygame.Vector2(0.0, 0.0), attack=False)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        normal_damage = session.projectiles[0].damage
        self.assertGreater(frenzy_damage, normal_damage)

    def test_raccoon_chaos_drop_grants_bonus_xp_and_score(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="fox_f")
        before = session.run_progress_snapshot()
        before_score = session.score_value

        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        activated = session.try_activate_super()

        after = session.run_progress_snapshot()
        self.assertEqual(activated, "raccoon_chaos_drop")
        self.assertGreaterEqual(int(after["run_level"]), int(before["run_level"]))
        self.assertTrue(
            int(after["xp"]) > int(before["xp"])
            or int(after["run_level"]) > int(before["run_level"])
        )
        self.assertGreater(session.score_value, before_score)

    def test_super_meter_ui_draws_from_snapshot(self) -> None:
        if not pygame.get_init():
            pygame.init()
        surface = pygame.Surface((1280, 720))
        ui = UiRenderer()
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        snapshot = session.super_snapshot()
        ui.draw_super_meter(
            surface,
            charge=int(snapshot["charge"]),
            max_charge=int(snapshot["max_charge"]),
            ready=bool(snapshot["ready"]),
        )
        self.assertIsInstance(surface, pygame.Surface)

    def test_super_activation_emits_audio_cue(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.start_new_run(player_animal_id="teddy_f")
        session.add_super_charge(int(session.super_snapshot()["max_charge"]))
        session.try_activate_super()
        cues = session.consume_audio_cues()
        self.assertEqual(int(cues["super_activate_count"]), 1)

    def test_super_cannot_be_spammed_without_recharge(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        max_charge = int(session.super_snapshot()["max_charge"])
        session.add_super_charge(max_charge)
        self.assertIsNotNone(session.try_activate_super())
        self.assertIsNone(session.try_activate_super())

    def test_single_enemy_event_does_not_instantly_fill_super_meter(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        balloon = BalloonEnemy(speed=120.0)
        balloon.position = pygame.Vector2(220.0, 220.0)
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
        session._check_projectile_collisions()
        snapshot = session.super_snapshot()
        self.assertFalse(bool(snapshot["ready"]))
        self.assertLess(int(snapshot["charge"]), int(snapshot["max_charge"]))


if __name__ == "__main__":
    unittest.main()
