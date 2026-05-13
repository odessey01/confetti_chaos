"""Validation tests for weapon definition registry and session weapon routing."""

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
from enemies import BalloonEnemy, BossBalloon  # noqa: E402
from systems.weapons import (  # noqa: E402
    DEFAULT_WEAPON_ID,
    SparklerAttackProfile,
    WEAPON_TYPE_MELEE,
    WEAPON_TYPE_PROJECTILE,
    get_weapon_definition,
    list_weapon_definitions,
)


class WeaponSystemValidationTests(unittest.TestCase):
    def test_weapon_registry_contains_core_weapons(self) -> None:
        ids = {weapon.weapon_id for weapon in list_weapon_definitions()}
        self.assertIn("bottle_rocket", ids)
        self.assertIn("sparkler", ids)
        self.assertIn("yoyo", ids)
        self.assertIn("bubble_wand", ids)
        self.assertIn("kazoo_beam", ids)

    def test_sparkler_definition_is_melee_with_tunable_fields(self) -> None:
        sparkler = get_weapon_definition("sparkler")
        self.assertEqual(sparkler.weapon_type, WEAPON_TYPE_MELEE)
        self.assertGreaterEqual(sparkler.base_damage, 1)
        self.assertGreater(sparkler.effective_range, 0.0)
        self.assertGreater(sparkler.attack_cooldown_seconds, 0.0)

    def test_bottle_rocket_definition_is_projectile(self) -> None:
        bottle = get_weapon_definition("bottle_rocket")
        self.assertEqual(bottle.weapon_type, WEAPON_TYPE_PROJECTILE)
        sparkler = get_weapon_definition("sparkler")
        self.assertGreater(bottle.effective_range, sparkler.effective_range)
        self.assertLessEqual(bottle.attack_cooldown_seconds, sparkler.attack_cooldown_seconds)

    def test_yoyo_definition_has_outbound_and_return_stats(self) -> None:
        yoyo = get_weapon_definition("yoyo")
        self.assertEqual(yoyo.weapon_type, WEAPON_TYPE_PROJECTILE)
        self.assertGreater(yoyo.travel_speed, 0.0)
        self.assertGreater(yoyo.return_speed, 0.0)
        self.assertGreater(yoyo.effective_range, 0.0)
        self.assertGreaterEqual(yoyo.active_cap, 1)
        self.assertGreater(yoyo.per_enemy_hit_cooldown, 0.0)

    def test_bubble_wand_definition_is_projectile_with_control_baseline(self) -> None:
        bubble_wand = get_weapon_definition("bubble_wand")
        self.assertEqual(bubble_wand.weapon_type, WEAPON_TYPE_PROJECTILE)
        self.assertGreaterEqual(bubble_wand.base_damage, 1)
        self.assertGreater(bubble_wand.effective_range, 0.0)
        self.assertGreater(bubble_wand.attack_cooldown_seconds, 0.0)
        self.assertGreater(bubble_wand.travel_speed, 0.0)
        self.assertGreaterEqual(bubble_wand.active_cap, 3)

    def test_kazoo_beam_definition_has_beam_baseline_stats(self) -> None:
        kazoo = get_weapon_definition("kazoo_beam")
        self.assertEqual(kazoo.weapon_type, WEAPON_TYPE_PROJECTILE)
        self.assertGreaterEqual(kazoo.base_damage, 1)
        self.assertGreater(kazoo.effective_range, 0.0)
        self.assertGreater(kazoo.attack_cooldown_seconds, 0.0)

    def test_bubble_wand_spawns_bubble_projectile(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bubble_wand")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 3)
        self.assertEqual(session.projectiles[0].__class__.__name__, "BubbleProjectile")

    def test_bubble_wand_pop_hits_nearby_hazard(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bubble_wand")
        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(session.player.rect.centerx + 16.0, session.player.rect.centery)
        session.hazards = [enemy]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        for _ in range(28):
            session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
            if len(session.hazards) == 0:
                break
        self.assertEqual(len(session.hazards), 0)

    def test_kazoo_beam_activates_then_expires(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("kazoo_beam")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertTrue(bool(session.kazoo_beam_snapshot()["active"]))
        for _ in range(80):
            session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
            if not bool(session.kazoo_beam_snapshot()["active"]):
                break
        self.assertFalse(bool(session.kazoo_beam_snapshot()["active"]))

    def test_kazoo_beam_auto_targets_nearest_enemy_when_no_input_direction(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("kazoo_beam")
        close_enemy = BalloonEnemy(speed=0.0)
        far_enemy = BalloonEnemy(speed=0.0)
        close_enemy.position = pygame.Vector2(session.player.rect.centerx + 90.0, session.player.rect.centery)
        far_enemy.position = pygame.Vector2(session.player.rect.centerx + 220.0, session.player.rect.centery + 160.0)
        session.hazards = [far_enemy, close_enemy]
        session.fire_projectile(pygame.Vector2(0.0, 0.0))
        direction = session.kazoo_beam_snapshot()["direction"]
        assert isinstance(direction, tuple)
        self.assertGreater(float(direction[0]), 0.5)

    def test_yoyo_launches_and_returns_to_player(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("yoyo")
        session.player.position.update(300.0, 300.0)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        for _ in range(60):
            session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
            if len(session.projectiles) == 0:
                break
        self.assertEqual(len(session.projectiles), 0)

    def test_yoyo_overlay_hides_while_deployed_and_returns_after_catch(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("yoyo")
        self.assertGreaterEqual(len(session.active_weapon_visual_overlay_snapshot()), 1)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(session.active_weapon_visual_overlay_snapshot(), ())
        for _ in range(70):
            session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
            if len(session.projectiles) == 0:
                break
        self.assertGreaterEqual(len(session.active_weapon_visual_overlay_snapshot()), 1)

    def test_yoyo_orbit_mode_replaces_deploy_and_deals_contact_damage(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("yoyo")
        session._weapon_evolution_forms["yoyo"] = "orbit_yoyo_storm"  # noqa: SLF001
        session._weapon_evolution_behavior_ids["yoyo"] = {"orbit_yoyo_storm"}  # noqa: SLF001
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 0)

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(
            session.player.rect.centerx + session.ORBITING_YOYO_RADIUS,
            session.player.rect.centery,
        )
        session.hazards = [enemy]
        session.update_playing(0.05, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.hazards), 0)

    def test_yoyo_balance_sits_between_sparkler_and_bottle_rocket_ranges(self) -> None:
        bottle = get_weapon_definition("bottle_rocket")
        sparkler = get_weapon_definition("sparkler")
        yoyo = get_weapon_definition("yoyo")
        self.assertGreater(yoyo.effective_range, sparkler.effective_range)
        self.assertLess(yoyo.effective_range, bottle.effective_range)
        self.assertGreater(yoyo.attack_cooldown_seconds, sparkler.attack_cooldown_seconds)

    def test_orbit_yoyo_contact_cooldown_limits_rapid_repeat_hits(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("yoyo")
        session._weapon_evolution_forms["yoyo"] = "orbit_yoyo_storm"  # noqa: SLF001
        session._weapon_evolution_behavior_ids["yoyo"] = {"orbit_yoyo_storm"}  # noqa: SLF001
        boss = BossBalloon(speed=0.0, max_health=6, damage_per_hit=1)
        boss.position = pygame.Vector2(
            session.player.rect.centerx + session.ORBITING_YOYO_RADIUS,
            session.player.rect.centery,
        )
        session.hazards = [boss]
        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        health_after_first = boss.health
        session.update_playing(0.05, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(boss.health, health_after_first)

    def test_game_session_defaults_to_registry_default_weapon(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        self.assertEqual(session.active_weapon_id, DEFAULT_WEAPON_ID)
        self.assertEqual(session.active_weapon_snapshot()["weapon_id"], DEFAULT_WEAPON_ID)

    def test_setting_invalid_weapon_falls_back_to_default(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("not_a_weapon")
        self.assertEqual(session.active_weapon_id, DEFAULT_WEAPON_ID)

    def test_sparkler_attack_route_uses_melee_hook_without_projectile_spawn(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        before_confetti = len(session.confetti.particles)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 0)
        self.assertGreater(session._weapon_cooldown_timer, 0.0)
        self.assertGreater(len(session.confetti.particles), before_confetti)

    def test_sparkler_attack_shape_is_directional_forward_cone(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        snapshot = session.sparkler_attack_snapshot()
        origin = snapshot["origin"]
        tip_left = snapshot["tip_left"]
        tip_right = snapshot["tip_right"]
        assert isinstance(origin, pygame.Vector2)
        assert isinstance(tip_left, pygame.Vector2)
        assert isinstance(tip_right, pygame.Vector2)
        self.assertGreater(tip_left.x, origin.x)
        self.assertGreater(tip_right.x, origin.x)
        self.assertLess(float(snapshot["sweep_start_degrees"]), float(snapshot["sweep_end_degrees"]))

    def test_sparkler_attack_shape_points_up_when_aiming_up(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        session.fire_projectile(pygame.Vector2(0.0, -1.0))
        snapshot = session.sparkler_attack_snapshot()
        origin = snapshot["origin"]
        tip_left = snapshot["tip_left"]
        tip_right = snapshot["tip_right"]
        assert isinstance(origin, pygame.Vector2)
        assert isinstance(tip_left, pygame.Vector2)
        assert isinstance(tip_right, pygame.Vector2)
        self.assertLess(tip_left.y, origin.y)
        self.assertLess(tip_right.y, origin.y)

    def test_sparkler_attack_shape_points_down_when_aiming_down(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        session.fire_projectile(pygame.Vector2(0.0, 1.0))
        snapshot = session.sparkler_attack_snapshot()
        origin = snapshot["origin"]
        tip_left = snapshot["tip_left"]
        tip_right = snapshot["tip_right"]
        assert isinstance(origin, pygame.Vector2)
        assert isinstance(tip_left, pygame.Vector2)
        assert isinstance(tip_right, pygame.Vector2)
        self.assertGreater(tip_left.y, origin.y)
        self.assertGreater(tip_right.y, origin.y)

    def test_sparkler_attack_cadence_blocks_spam_and_allows_repeat_after_cooldown(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        first_snapshot = session.sparkler_attack_snapshot()
        first_count = int(first_snapshot["swing_count"])
        self.assertGreater(first_count, 0)

        # Immediate retry should be blocked by cooldown.
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        blocked_snapshot = session.sparkler_attack_snapshot()
        self.assertEqual(int(blocked_snapshot["swing_count"]), first_count)

        # After cooldown elapses, attack should trigger again.
        session.update_playing(0.3, pygame.Vector2(0.0, 0.0), attack=False)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        second_snapshot = session.sparkler_attack_snapshot()
        self.assertGreater(int(second_snapshot["swing_count"]), first_count)

    def test_fire_rate_upgrade_reduces_sparkler_cooldown(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        baseline = session._weapon_cooldown_timer

        session._weapon_cooldown_timer = 0.0
        session.run_upgrades.stacks["fire_rate_up"] = 2
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        upgraded = session._weapon_cooldown_timer
        self.assertLess(upgraded, baseline)

    def test_sparkler_hits_enemy_in_front(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        enemy = BalloonEnemy(speed=0.0)
        enemy.position.update(360.0, 300.0)
        session.hazards = [enemy]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 0)

    def test_sparkler_does_not_hit_enemy_behind_player(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        enemy = BalloonEnemy(speed=0.0)
        enemy.position.update(220.0, 300.0)
        session.hazards = [enemy]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 1)

    def test_sparkler_does_not_hit_enemy_too_close_inside_arc_hole(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        enemy = BalloonEnemy(speed=0.0)
        enemy.rect.center = (
            int(session.player.rect.centerx + 24),
            int(session.player.rect.centery),
        )
        enemy.position.update(float(enemy.rect.x), float(enemy.rect.y))
        session.hazards = [enemy]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 1)

    def test_sparkler_hits_enemy_just_outside_inner_arc_hole(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        enemy = BalloonEnemy(speed=0.0, size=34)
        target_center_x = int(session.player.rect.centerx + 34)
        target_center_y = int(session.player.rect.centery)
        enemy.position.update(float(target_center_x - (enemy.size / 2)), float(target_center_y - (enemy.size / 2)))
        session.hazards = [enemy]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 0)

    def test_sparkler_can_hit_enemy_body_even_if_center_is_outside_cone(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        enemy = BalloonEnemy(size=100, speed=0.0)
        center_x = session.player.rect.centerx + 70
        center_y = session.player.rect.centery + 90
        enemy.position.update(float(center_x - 50), float(center_y - 50))
        session.hazards = [enemy]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 0)

    def test_sparkler_can_hit_multiple_enemies_in_same_swing(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        e1 = BalloonEnemy(speed=0.0)
        e1.position.update(360.0, 286.0)
        e2 = BalloonEnemy(speed=0.0)
        e2.position.update(364.0, 314.0)
        session.hazards = [e1, e2]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 0)

    def test_sparkler_visual_attack_overlay_draws_and_expires(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertTrue(session.sparkler_attack_snapshot())
        session.draw_playing(surface)
        self.assertIsInstance(surface, pygame.Surface)
        session.update_playing(0.2, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(session.sparkler_attack_snapshot(), {})

    def test_sparkler_visual_snapshot_tracks_swing_progress_window(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        snapshot = session.sparkler_attack_snapshot()
        self.assertIn("sweep_start_degrees", snapshot)
        self.assertIn("sweep_end_degrees", snapshot)
        start_expiry = float(snapshot["expires_in"])
        session.update_playing(0.04, pygame.Vector2(0.0, 0.0), attack=False)
        mid_expiry = float(session.sparkler_attack_snapshot()["expires_in"])
        self.assertLess(mid_expiry, start_expiry)

    def test_sparkler_uses_player_facing_when_input_direction_is_zero(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.facing = pygame.Vector2(-1.0, 0.0)
        session.fire_projectile(pygame.Vector2(0.0, 0.0))
        direction = session.sparkler_attack_snapshot()["direction"]
        assert isinstance(direction, pygame.Vector2)
        self.assertLess(direction.x, 0.0)

    def test_sparkler_falls_back_to_last_attack_direction(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        # First attack with bottle rocket to set last non-zero attack direction.
        session.set_active_weapon("bottle_rocket")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        session.projectiles.clear()
        session._weapon_cooldown_timer = 0.0
        # Zero-out current facing and trigger sparkler with zero input.
        session.set_active_weapon("sparkler")
        session.player.facing = pygame.Vector2(0.0, 0.0)
        session.fire_projectile(pygame.Vector2(0.0, 0.0))
        direction = session.sparkler_attack_snapshot()["direction"]
        assert isinstance(direction, pygame.Vector2)
        self.assertGreater(direction.x, 0.0)

    def test_sparkler_profile_hook_can_extend_attack_range_without_refactor(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        far_enemy = BalloonEnemy(speed=0.0)
        # Outside baseline sparkler range but inside extended profile range.
        far_enemy.position.update(415.0, 300.0)
        session.hazards = [far_enemy]
        session._current_sparkler_attack_profile = (  # type: ignore[method-assign]
            lambda: SparklerAttackProfile(range_bonus=40.0)
        )
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.hazards), 0)

    def test_sparkler_range_upgrade_increases_swing_range_snapshot(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        baseline_range = float(session.sparkler_attack_snapshot()["range"])
        session._weapon_cooldown_timer = 0.0
        session.run_upgrades.stacks["sparkler_range_up"] = 1
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        upgraded_range = float(session.sparkler_attack_snapshot()["range"])
        self.assertGreater(upgraded_range, baseline_range)

    def test_sparkler_damage_upgrade_increases_melee_hit_damage(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.player.position.update(300.0, 300.0)
        boss = BossBalloon(speed=0.0, max_health=6, damage_per_hit=1)
        boss.position.update(350.0, 300.0)
        session.hazards = [boss]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        baseline_health = boss.health
        self.assertEqual(baseline_health, 4)
        session.update_playing(0.2, pygame.Vector2(0.0, 0.0), attack=False)
        session._weapon_cooldown_timer = 0.0
        session.run_upgrades.stacks["sparkler_damage_up"] = 1
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(boss.health, baseline_health - 3)

    def test_sparkler_arc_upgrade_increases_swing_cone_snapshot(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        baseline_cone = float(session.sparkler_attack_snapshot()["cone_degrees"])
        session._weapon_cooldown_timer = 0.0
        session.run_upgrades.stacks["sparkler_arc_up"] = 1
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        upgraded_cone = float(session.sparkler_attack_snapshot()["cone_degrees"])
        self.assertGreater(upgraded_cone, baseline_cone)


if __name__ == "__main__":
    unittest.main()
