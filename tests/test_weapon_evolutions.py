"""Validation tests for weapon evolution definitions and trigger checks."""

from __future__ import annotations

import pathlib
import random
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.game_session import GameSession  # noqa: E402
from systems.run_upgrades import RunUpgradeSystem, UpgradeDefinition  # noqa: E402
from enemies import BalloonEnemy  # noqa: E402
from player import BottleRocket  # noqa: E402
from systems.weapon_evolutions import (  # noqa: E402
    WeaponEvolutionTracker,
    eligible_weapon_evolutions,
    list_weapon_evolutions,
    preview_weapon_evolutions_with_added_tags,
)
from systems.run_upgrades import missing_tags_in_upgrade_pool, upgrade_ids_by_tag  # noqa: E402


class WeaponEvolutionValidationTests(unittest.TestCase):
    def test_evolution_definitions_cover_bottle_and_sparkler_paths(self) -> None:
        definitions = list_weapon_evolutions()
        ids = {item.evolution_id for item in definitions}
        self.assertIn("burst_rocket", ids)
        self.assertIn("big_pop_rocket", ids)
        self.assertIn("wide_arc_sparkler", ids)
        self.assertIn("spark_aura", ids)

    def test_all_evolution_required_tags_exist_in_upgrade_pool(self) -> None:
        definitions = list_weapon_evolutions()
        required_tags: set[str] = set()
        for definition in definitions:
            self.assertGreater(len(definition.required_tags), 0)
            required_tags.update(definition.required_tags)
        missing = missing_tags_in_upgrade_pool(required_tags)
        self.assertEqual(missing, ())

    def test_each_required_tag_maps_to_at_least_one_upgrade(self) -> None:
        definitions = list_weapon_evolutions()
        required_tags = {tag for definition in definitions for tag in definition.required_tags}
        tag_to_upgrades = upgrade_ids_by_tag()
        for tag in required_tags:
            self.assertGreaterEqual(len(tag_to_upgrades.get(tag, ())), 1)

    def test_eligible_evolution_resolves_from_required_tags(self) -> None:
        eligible = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split"),
        )
        resolved = {item.evolution_id for item in eligible}
        self.assertIn("burst_rocket", resolved)
        self.assertNotIn("big_pop_rocket", resolved)

    def test_preview_evolutions_with_added_tags_predicts_trigger(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion",),
            added_tags=("rocket_split",),
        )
        resolved = {item.evolution_id for item in preview}
        self.assertIn("burst_rocket", resolved)
        self.assertNotIn("big_pop_rocket", resolved)

    def test_preview_evolutions_respects_excluded_triggered_ids(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range",),
            added_tags=("sparkler_speed",),
            exclude_evolution_ids=("wide_arc_sparkler",),
        )
        self.assertEqual(preview, [])

    def test_tracker_triggers_each_evolution_only_once(self) -> None:
        tracker = WeaponEvolutionTracker()
        first = tracker.check_for_new(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range", "sparkler_speed"),
        )
        second = tracker.check_for_new(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range", "sparkler_speed"),
        )
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 0)
        pending = tracker.consume_pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(tracker.consume_pending(), [])

    def test_tracker_limits_new_evolution_to_one_per_check_for_balance(self) -> None:
        tracker = WeaponEvolutionTracker()
        resolved = tracker.check_for_new(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split", "rocket_power"),
        )
        self.assertEqual(len(resolved), 1)

    def test_game_session_upgrade_apply_runs_evolution_check(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session.run_upgrades = RunUpgradeSystem(rng=random.Random(41))
        session.run_upgrades.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        session.run_upgrades.apply_choice("projectile_cap_up", active_weapon_id="bottle_rocket")
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="move_speed_up",
                name="Quick Feet",
                description="+Move speed.",
                category="player",
                effect_values={},
            )
        ]
        self.assertTrue(session.apply_upgrade_choice_by_index(0))
        snapshot = session.weapon_evolution_snapshot()
        triggered = set(snapshot["triggered_evolution_ids"])
        self.assertIn("burst_rocket", triggered)
        forms = snapshot["active_forms_by_weapon"]
        self.assertEqual(forms.get("bottle_rocket"), "burst_rocket")

    def test_game_session_sparkler_tags_trigger_wide_arc_evolution(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.run_upgrades = RunUpgradeSystem(rng=random.Random(43))
        session.run_upgrades.apply_choice("sparkler_range_up", active_weapon_id="sparkler")
        session.run_upgrades.apply_choice("fire_rate_up", active_weapon_id="sparkler")
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="move_speed_up",
                name="Quick Feet",
                description="+Move speed.",
                category="player",
                effect_values={},
            )
        ]
        self.assertTrue(session.apply_upgrade_choice_by_index(0))
        snapshot = session.weapon_evolution_snapshot()
        forms = snapshot["active_forms_by_weapon"]
        self.assertEqual(forms.get("sparkler"), "wide_arc_sparkler")

    def test_game_session_upgrade_choice_previews_flag_evolution_paths(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session.run_upgrades = RunUpgradeSystem(rng=random.Random(53))
        session.run_upgrades.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="projectile_cap_up",
                name="Extra Chamber",
                description="+1 active rocket (max 5).",
                category="weapon",
                effect_values={"projectile_cap_bonus": 1.0},
                tags=("rocket_split",),
            ),
            UpgradeDefinition(
                id="move_speed_up",
                name="Quick Feet",
                description="+Move speed.",
                category="player",
                effect_values={"move_speed_mult": 0.09},
            ),
        ]
        previews = session.current_upgrade_choice_previews()
        self.assertEqual(len(previews), 2)
        self.assertTrue(bool(previews[0]["leads_to_evolution"]))
        self.assertIn("burst_rocket", previews[0]["evolution_ids"])
        self.assertFalse(bool(previews[1]["leads_to_evolution"]))

    def test_evolution_trigger_emits_feedback_audio_cue(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session.run_upgrades = RunUpgradeSystem(rng=random.Random(47))
        session.run_upgrades.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        session.run_upgrades.apply_choice("projectile_cap_up", active_weapon_id="bottle_rocket")
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="move_speed_up",
                name="Quick Feet",
                description="+Move speed.",
                category="player",
                effect_values={},
            )
        ]
        self.assertTrue(session.apply_upgrade_choice_by_index(0))
        cues = session.consume_audio_cues()
        self.assertGreaterEqual(int(cues["evolution_count"]), 1)
        self.assertGreater(float(session._evolution_feedback_timer), 0.0)  # noqa: SLF001

    def test_evolution_feedback_applies_brief_pause(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session._trigger_evolution_feedback("Burst Rocket")  # noqa: SLF001
        before_time = session.elapsed_time
        session.update_playing(0.05, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertAlmostEqual(session.elapsed_time, before_time, places=5)

    def test_evolved_bottle_rocket_form_modifies_projectile_damage(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "burst_rocket"  # noqa: SLF001
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        self.assertGreaterEqual(session.projectiles[0].damage, 2)
        self.assertEqual(getattr(session.projectiles[0], "evolution_form_id", ""), "burst_rocket")

    def test_evolved_sparkler_form_modifies_swing_shape_snapshot(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        baseline = session.sparkler_attack_snapshot()
        baseline_range = float(baseline["range"])
        baseline_cone = float(baseline["cone_degrees"])

        session.update_playing(0.3, pygame.Vector2(0.0, 0.0), attack=False)
        session._weapon_cooldown_timer = 0.0  # noqa: SLF001
        session._weapon_evolution_forms["sparkler"] = "wide_arc_sparkler"  # noqa: SLF001
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        evolved = session.sparkler_attack_snapshot()
        self.assertGreater(float(evolved["range"]), baseline_range)
        self.assertGreater(float(evolved["cone_degrees"]), baseline_cone)

    def test_burst_rocket_spawns_fragments_on_expiration(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "burst_rocket"  # noqa: SLF001
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        session.projectiles[0].lifetime = 0.0
        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertGreaterEqual(len(session.projectiles), 2)
        self.assertTrue(any(bool(getattr(p, "is_burst_fragment", False)) for p in session.projectiles))

    def test_big_pop_rocket_aoe_hits_nearby_enemies_only(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "big_pop_rocket"  # noqa: SLF001
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        session.projectiles[0].position = pygame.Vector2(380.0, 320.0)
        session.projectiles[0].lifetime = 0.0

        near_enemy = BalloonEnemy(speed=0.0)
        near_enemy.position = pygame.Vector2(390.0, 320.0)
        far_enemy = BalloonEnemy(speed=0.0)
        far_enemy.position = pygame.Vector2(560.0, 320.0)
        session.hazards = [near_enemy, far_enemy]

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.hazards), 1)
        remaining_center = session.hazards[0].rect.centerx
        self.assertGreater(remaining_center, 500)

    def test_big_pop_rocket_direct_hit_and_aoe_no_index_error(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "big_pop_rocket"  # noqa: SLF001

        near_enemy = BalloonEnemy(speed=0.0)
        near_enemy.position = pygame.Vector2(420.0, 320.0)
        also_near_enemy = BalloonEnemy(speed=0.0)
        also_near_enemy.position = pygame.Vector2(450.0, 320.0)
        session.hazards = [near_enemy, also_near_enemy]

        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(420.0, 320.0),
                direction=pygame.Vector2(1.0, 0.0),
                speed=280.0,
                lifetime=0.4,
                max_travel_distance=600.0,
                damage=1,
            )
        ]
        setattr(session.projectiles[0], "evolution_form_id", "big_pop_rocket")

        # Regression: this used to fail with "IndexError: pop index out of range".
        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.hazards), 0)

    def test_spark_aura_replaces_swing_and_ticks_radial_damage(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "spark_aura"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(
            session.player.rect.centerx + 40.0,
            session.player.rect.centery,
        )
        session.hazards = [enemy]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(session.sparkler_attack_snapshot(), {})
        self.assertEqual(len(session.hazards), 1)

        session.update_playing(session.SPARK_AURA_TICK_INTERVAL + 0.01, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.hazards), 0)


if __name__ == "__main__":
    unittest.main()
