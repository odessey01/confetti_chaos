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

from enemies import BalloonEnemy, BossBalloon, ConfettiSpray, ConfettiSprayer, PinataEnemy, TrackingHazard  # noqa: E402
from player.projectile import Projectile  # noqa: E402
from systems.game_session import GameSession  # noqa: E402
from systems.spawn_controller import SpawnController  # noqa: E402
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

    def test_boss_chase_closes_distance_to_player(self) -> None:
        boss = BossBalloon(speed=160.0)
        boss.position = pygame.Vector2(100.0, 100.0)
        boss.velocity = pygame.Vector2(0.0, 0.0)
        target = pygame.Vector2(900.0, 500.0)

        before_distance = pygame.Vector2(boss.rect.center).distance_to(target)
        for _ in range(20):
            boss.update(0.1, target)
        after_distance = pygame.Vector2(boss.rect.center).distance_to(target)

        self.assertLess(after_distance, before_distance)

    def test_boss_turning_is_smooth_not_instant_snap(self) -> None:
        boss = BossBalloon(speed=180.0)
        boss.position = pygame.Vector2(400.0, 300.0)
        boss.velocity = pygame.Vector2(1.0, 0.0) * (boss.base_speed * boss.chase_speed_factor)

        target = pygame.Vector2(200.0, 300.0)  # opposite direction from initial velocity
        before_direction = boss.velocity.normalize()
        boss.update(0.05, target)
        after_direction = boss.velocity.normalize()

        # A smooth turn should not instantly flip to the opposite heading in one short frame.
        self.assertGreater(before_direction.dot(after_direction), -0.95)

    def test_boss_hit_uses_configurable_health_and_damage(self) -> None:
        boss = BossBalloon(speed=120.0, max_health=5, damage_per_hit=2)
        self.assertEqual(boss.health, 5)
        hit_registered, defeated = boss.apply_hit()
        self.assertTrue(hit_registered)
        self.assertFalse(defeated)
        self.assertEqual(boss.health, 3)

    def test_boss_hit_feedback_timers_decay_after_update(self) -> None:
        boss = BossBalloon(speed=120.0)
        hit_registered, defeated = boss.apply_hit()
        self.assertTrue(hit_registered)
        self.assertFalse(defeated)
        self.assertGreater(boss.hit_flash_timer, 0.0)
        self.assertGreater(boss.hit_wobble_timer, 0.0)
        self.assertGreater(boss.hit_invuln_timer, 0.0)
        boss.update(0.3, pygame.Vector2(600.0, 400.0))
        self.assertEqual(boss.hit_flash_timer, 0.0)
        self.assertEqual(boss.hit_wobble_timer, 0.0)
        self.assertEqual(boss.hit_invuln_timer, 0.0)

    def test_boss_abilities_trigger_on_timers(self) -> None:
        boss = BossBalloon(speed=120.0)
        boss.position = pygame.Vector2(300.0, 220.0)
        boss._speed_surge_cooldown_timer = 0.0
        boss._directional_charge_cooldown_timer = 0.0
        boss._burst_spawn_cooldown_timer = 0.0
        boss.update(0.1, pygame.Vector2(700.0, 420.0))
        cues = boss.consume_ability_cues()
        self.assertTrue(cues["speed_surge_triggered"])
        self.assertTrue(cues["directional_charge_triggered"])
        self.assertGreaterEqual(int(cues["burst_spawn_count"]), 1)

    def test_session_applies_boss_burst_spawn_effect(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session._boss_active = True
        session.spawn_controller.max_hazards = 1
        boss = BossBalloon(speed=120.0)
        boss.position = pygame.Vector2(100.0, 100.0)
        boss._burst_spawn_cooldown_timer = 0.0
        session.hazards = [boss]
        before_count = len(session.hazards)
        session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
        after_count = len(session.hazards)
        self.assertGreater(after_count, before_count)

    def test_boss_phase_progression_and_cues_trigger_once(self) -> None:
        boss = BossBalloon(speed=120.0, max_health=6, damage_per_hit=1)
        self.assertEqual(boss.current_phase, 1)
        for _ in range(2):
            boss.hit_invuln_timer = 0.0
            boss.apply_hit()
        cues = boss.consume_ability_cues()
        self.assertTrue(cues["phase_changed"])
        self.assertEqual(cues["current_phase"], 2)
        # Consuming again should clear one-shot phase-change cue.
        cues2 = boss.consume_ability_cues()
        self.assertFalse(cues2["phase_changed"])

        for _ in range(2):
            boss.hit_invuln_timer = 0.0
            boss.apply_hit()
        cues3 = boss.consume_ability_cues()
        self.assertTrue(cues3["phase_changed"])
        self.assertEqual(cues3["current_phase"], 3)

    def test_boss_phase_escalates_cooldown_rate(self) -> None:
        boss = BossBalloon(speed=120.0, max_health=6, damage_per_hit=1)
        phase1 = boss._phase_cooldown_multiplier()
        for _ in range(4):
            boss.hit_invuln_timer = 0.0
            boss.apply_hit()
        self.assertEqual(boss.current_phase, 3)
        phase3 = boss._phase_cooldown_multiplier()
        self.assertLess(phase3, phase1)

    def test_boss_speed_is_capped_for_fairness(self) -> None:
        boss = BossBalloon(speed=300.0)
        boss.current_phase = 3
        boss.is_charging = True
        boss._speed_surge_timer = 1.0
        boss._directional_charge_timer = 1.0
        boss.update(0.1, pygame.Vector2(900.0, 500.0))
        self.assertLessEqual(boss.speed, boss.max_speed_cap)
        self.assertLessEqual(boss.speed, 350.0)

    def test_boss_fight_enemy_count_stays_capped(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session._boss_active = True
        session.elapsed_time = 120.0
        session.score_seconds = 120.0
        session.spawn_controller.max_hazards = 20
        boss = BossBalloon(speed=120.0)
        boss.position = pygame.Vector2(100.0, 100.0)
        session.hazards = [boss]
        session.update_playing(5.0, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertLessEqual(len(session.hazards), 3)

    def test_boss_defeat_hit_window_is_predictable(self) -> None:
        boss = BossBalloon(speed=120.0, max_health=4, damage_per_hit=1)
        hits = 0
        defeated = False
        while not defeated:
            boss.hit_invuln_timer = 0.0
            _, defeated = boss.apply_hit()
            hits += 1
        self.assertEqual(hits, 4)

    def test_unknown_boss_variant_falls_back_to_classic(self) -> None:
        boss = BossBalloon(speed=120.0, profile_id="nonexistent_variant")
        self.assertEqual(boss.profile_id, "classic")

    def test_spawn_controller_applies_bulwark_variant_profile(self) -> None:
        controller = SpawnController(self.bounds, initial_hazards=0)
        boss = controller.create_boss_hazard_for_spawn(
            tier=5,
            base_speed=200.0,
            flavor_tag="SWARM",
            boss_variant_id="bulwark",
        )
        self.assertEqual(boss.profile_id, "bulwark")
        self.assertEqual(boss.max_health, 5)
        self.assertEqual(boss.damage_per_hit, 1)
        self.assertIsNotNone(boss.spawn_profile)
        self.assertEqual(boss.spawn_profile.get("boss_variant_id"), "bulwark")

    def test_game_session_boss_variant_hook_can_select_non_default_profile(self) -> None:
        class _VariantSession(GameSession):
            def _boss_variant_for_context(self, *, level: int, flavor_name: str) -> str:  # type: ignore[override]
                _ = (level, flavor_name)
                return "bulwark"

        session = _VariantSession(self.bounds, hazard_count=0)
        session.elapsed_time = 119.9
        session.score_seconds = 0.0
        session.update_playing(0.2, pygame.Vector2(0, 0), attack=False)
        bosses = [hazard for hazard in session.hazards if isinstance(hazard, BossBalloon)]
        self.assertEqual(len(bosses), 1)
        self.assertEqual(bosses[0].profile_id, "bulwark")

    def test_pinata_hit_feedback_timers_decay_after_update(self) -> None:
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        hit_registered, defeated = pinata.apply_hit()
        self.assertTrue(hit_registered)
        self.assertFalse(defeated)
        self.assertGreater(pinata.hit_flash_timer, 0.0)
        self.assertGreater(pinata.hit_wobble_timer, 0.0)
        self.assertGreater(pinata.hit_invuln_timer, 0.0)
        pinata.update(0.4, pygame.Vector2(600.0, 400.0))
        self.assertEqual(pinata.hit_flash_timer, 0.0)
        self.assertEqual(pinata.hit_wobble_timer, 0.0)
        self.assertEqual(pinata.hit_invuln_timer, 0.0)

    def test_pinata_triggered_reaction_briefly_speeds_up_on_hit(self) -> None:
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.velocity = pygame.Vector2(1.0, 0.0) * pinata.base_speed
        pinata.apply_hit()
        pinata.update(0.05, pygame.Vector2(600.0, 400.0))
        self.assertGreater(pinata.velocity.length(), pinata.base_speed)
        pinata.update(0.6, pygame.Vector2(600.0, 400.0))
        self.assertAlmostEqual(pinata.velocity.length(), pinata.base_speed, places=5)

    def test_pinata_surprise_cue_is_one_shot(self) -> None:
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.apply_hit()
        cues = pinata.consume_surprise_cues()
        self.assertTrue(cues["reaction_triggered"])
        cues_again = pinata.consume_surprise_cues()
        self.assertFalse(cues_again["reaction_triggered"])

    def test_pinata_split_spawn_uses_profile_mini_spawn_count(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        pinata = PinataEnemy(speed=120.0, max_health=3, damage_per_hit=1)
        pinata.position = pygame.Vector2(220, 220)
        pinata.health = 1
        pinata.apply_spawn_profile(
            {
                "tier": 10,
                "speed": 120.0,
                "health": 1,
                "movement_profile": "pinata_heavy_drift",
                "flavor_tag": "STANDARD",
                "enemy_kind": "pinata",
                "break_confetti_count": 22,
                "mini_spawn_count": 2,
            }
        )
        session.hazards = [pinata]
        center = pygame.Vector2(pinata.rect.center)
        session.projectiles = [
            Projectile(
                position=center,
                direction=pygame.Vector2(1, 0),
                speed=0.0,
                lifetime=2.0,
                size=8,
            )
        ]
        session._check_projectile_collisions()
        mini_balloons = [hazard for hazard in session.hazards if isinstance(hazard, BalloonEnemy)]
        self.assertEqual(len(mini_balloons), 2)
        self.assertGreaterEqual(len(session.confetti.particles), 20)

    def test_confetti_sprayer_approaches_when_far(self) -> None:
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(100.0, 100.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        target = pygame.Vector2(1000.0, 600.0)
        before = pygame.Vector2(sprayer.rect.center).distance_to(target)
        for _ in range(18):
            sprayer.update(0.1, target)
        after = pygame.Vector2(sprayer.rect.center).distance_to(target)
        self.assertLess(after, before)

    def test_confetti_sprayer_retreats_when_too_close(self) -> None:
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(550.0, 330.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        target = pygame.Vector2(600.0, 360.0)
        before = pygame.Vector2(sprayer.rect.center).distance_to(target)
        for _ in range(12):
            sprayer.update(0.1, target)
        after = pygame.Vector2(sprayer.rect.center).distance_to(target)
        self.assertGreater(after, before)

    def test_confetti_sprayer_speed_remains_bounded_and_stable(self) -> None:
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(300.0, 300.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        target = pygame.Vector2(640.0, 360.0)
        for _ in range(30):
            sprayer.update(0.05, target)
            self.assertLessEqual(sprayer.velocity.length(), sprayer.base_speed + 1e-6)

    def test_confetti_sprayer_emits_directional_spray_after_charge(self) -> None:
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(280.0, 280.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        sprayer.attack_cooldown_timer = 0.0
        target = pygame.Vector2(640.0, 360.0)
        for _ in range(12):
            sprayer.update(0.1, target)
            cues = sprayer.consume_attack_cues()
            if cues["spray_fired"]:
                directions = cues["directions"]
                self.assertGreater(len(directions), 0)
                for direction in directions:
                    self.assertGreater(pygame.Vector2(direction).length_squared(), 0.0)
                break
        else:
            self.fail("Expected confetti sprayer to emit at least one spray burst cue.")

    def test_game_session_collects_confetti_spray_projectiles(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(220.0, 220.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        sprayer.attack_cooldown_timer = 0.0
        session.hazards = [sprayer]
        for _ in range(8):
            session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
            if len(session.enemy_sprays) > 0:
                break
        self.assertGreater(len(session.enemy_sprays), 0)

    def test_confetti_sprayer_telegraphs_before_firing(self) -> None:
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(280.0, 280.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        sprayer.attack_cooldown_timer = 0.0
        target = pygame.Vector2(640.0, 360.0)
        sprayer.update(0.05, target)
        first_cues = sprayer.consume_attack_cues()
        self.assertTrue(sprayer.is_charging)
        self.assertFalse(first_cues["spray_fired"])

    def test_confetti_sprayer_cooldown_prevents_immediate_repeat_bursts(self) -> None:
        sprayer = ConfettiSprayer(speed=140.0)
        sprayer.position = pygame.Vector2(280.0, 280.0)
        sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
        sprayer.attack_cooldown_timer = 0.0
        target = pygame.Vector2(640.0, 360.0)

        fired_count = 0
        for _ in range(40):
            sprayer.update(0.05, target)
            cues = sprayer.consume_attack_cues()
            if cues["spray_fired"]:
                fired_count += 1
        self.assertLessEqual(fired_count, 1)

    def test_confetti_spray_collision_with_player_triggers_game_over(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.enemy_sprays = [
            ConfettiSpray(
                position=pygame.Vector2(session.player.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=0.5,
                size=12,
            )
        ]
        did_game_over = session.update_playing(0.05, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertTrue(did_game_over)

    def test_confetti_sprays_expire_and_cleanup_correctly(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        session.enemy_sprays = [
            ConfettiSpray(
                position=pygame.Vector2(100.0, 100.0),
                direction=pygame.Vector2(1.0, 0.0),
                speed=0.0,
                lifetime=0.05,
                size=10,
            )
        ]
        self.assertEqual(len(session.enemy_sprays), 1)
        session.update_playing(0.2, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.enemy_sprays), 0)

    def test_multiple_sprayers_respect_active_spray_cap(self) -> None:
        session = GameSession(self.bounds, hazard_count=0)
        sprayers: list[ConfettiSprayer] = []
        for index in range(6):
            sprayer = ConfettiSprayer(speed=140.0)
            sprayer.position = pygame.Vector2(120.0 + (index * 90.0), 220.0)
            sprayer.velocity = pygame.Vector2(1.0, 0.0) * sprayer.base_speed
            sprayer.attack_cooldown_timer = 0.0
            sprayer.spray_projectile_count = 8
            sprayers.append(sprayer)
        session.hazards = sprayers
        for _ in range(20):
            session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertLessEqual(len(session.enemy_sprays), session.MAX_ACTIVE_ENEMY_SPRAYS)

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
