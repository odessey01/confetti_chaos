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
from enemies import BalloonEnemy, PinataEnemy  # noqa: E402
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
        self.assertIn("delayed_blast_rocket", ids)
        self.assertIn("pinball_rocket", ids)
        self.assertIn("chain_rocket", ids)
        self.assertIn("piercing_rocket", ids)
        self.assertIn("wide_arc_sparkler", ids)
        self.assertIn("orbiting_sparklers", ids)
        self.assertIn("spark_aura", ids)
        self.assertIn("flare_whip", ids)
        self.assertIn("ember_ring", ids)

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

    def test_all_current_evolutions_express_recommended_weapon_level_three(self) -> None:
        definitions = list_weapon_evolutions()
        self.assertTrue(definitions)
        for definition in definitions:
            self.assertEqual(definition.required_weapon_level, 3)

    def test_new_evolution_tags_are_available_in_upgrade_pool(self) -> None:
        missing = missing_tags_in_upgrade_pool(
            {
                "rocket_sticky",
                "rocket_bounce",
                "sparkler_orbit",
                "sparkler_persistence",
            }
        )
        self.assertEqual(missing, ())

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

    def test_new_evolution_conditions_resolve_from_required_tags(self) -> None:
        bottle_eligible = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=(
                "rocket_explosion",
                "rocket_sticky",
                "rocket_bounce",
                "rocket_speed",
                "rocket_power",
                "rocket_split",
            ),
        )
        bottle_ids = {item.evolution_id for item in bottle_eligible}
        self.assertIn("delayed_blast_rocket", bottle_ids)
        self.assertIn("pinball_rocket", bottle_ids)
        self.assertIn("chain_rocket", bottle_ids)
        self.assertIn("piercing_rocket", bottle_ids)

        sparkler_eligible = eligible_weapon_evolutions(
            weapon_id="sparkler",
            acquired_tags=("sparkler_orbit", "sparkler_speed", "sparkler_range", "sparkler_persistence"),
        )
        sparkler_ids = {item.evolution_id for item in sparkler_eligible}
        self.assertIn("orbiting_sparklers", sparkler_ids)
        self.assertIn("spark_aura", sparkler_ids)
        self.assertIn("flare_whip", sparkler_ids)
        self.assertIn("ember_ring", sparkler_ids)

    def test_preview_evolutions_supports_new_tag_pairs(self) -> None:
        bottle_preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion",),
            added_tags=("rocket_sticky",),
        )
        bottle_ids = {item.evolution_id for item in bottle_preview}
        self.assertIn("delayed_blast_rocket", bottle_ids)

        sparkler_preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="sparkler",
            acquired_tags=("sparkler_speed",),
            added_tags=("sparkler_orbit",),
        )
        sparkler_ids = {item.evolution_id for item in sparkler_preview}
        self.assertIn("orbiting_sparklers", sparkler_ids)

    def test_pinball_rocket_is_not_unlocked_by_projectile_speed_up_alone(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="bottle_rocket",
            acquired_tags=(),
            added_tags=("rocket_speed",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertNotIn("pinball_rocket", preview_ids)

    def test_pinball_rocket_is_unlocked_by_ricochet_rounds_and_fire_rate(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_bounce",),
            added_tags=("rocket_speed",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertIn("pinball_rocket", preview_ids)

    def test_chain_rocket_is_unlocked_by_speed_and_power(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_speed",),
            added_tags=("rocket_power",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertIn("chain_rocket", preview_ids)

    def test_piercing_rocket_is_unlocked_by_speed_and_split(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_speed",),
            added_tags=("rocket_split",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertIn("piercing_rocket", preview_ids)

    def test_spark_aura_is_not_unlocked_by_sparkler_arc_and_range_alone(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range",),
            added_tags=("sparkler_orbit",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertNotIn("spark_aura", preview_ids)

    def test_spark_aura_is_unlocked_by_sparkler_duration_and_range(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range",),
            added_tags=("sparkler_persistence",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertIn("spark_aura", preview_ids)

    def test_flare_whip_is_unlocked_by_orbit_and_range(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="sparkler",
            acquired_tags=("sparkler_orbit",),
            added_tags=("sparkler_range",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertIn("flare_whip", preview_ids)

    def test_ember_ring_is_unlocked_by_persistence_and_speed(self) -> None:
        preview = preview_weapon_evolutions_with_added_tags(
            weapon_id="sparkler",
            acquired_tags=("sparkler_persistence",),
            added_tags=("sparkler_speed",),
        )
        preview_ids = {item.evolution_id for item in preview}
        self.assertIn("ember_ring", preview_ids)

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

    def test_tracker_blocks_conflicting_second_evolution_for_same_weapon(self) -> None:
        tracker = WeaponEvolutionTracker()
        first = tracker.check_for_new(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range", "sparkler_speed"),
        )
        second = tracker.check_for_new(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range", "sparkler_speed", "sparkler_orbit", "sparkler_persistence"),
        )
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])
        self.assertTrue(tracker.has_triggered_weapon("sparkler"))

    def test_tracker_allows_bottle_rocket_to_gain_additional_compatible_evolutions(self) -> None:
        tracker = WeaponEvolutionTracker()
        first = tracker.check_for_new(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split"),
        )
        second = tracker.check_for_new(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split", "rocket_sticky"),
        )
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(first[0].result_form_id, "burst_rocket")
        self.assertEqual(second[0].result_form_id, "delayed_blast_rocket")

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

    def test_game_session_stops_previewing_conflicting_evolutions_after_weapon_evolves(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "wide_arc_sparkler"  # noqa: SLF001
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="sparkler_arc_up",
                name="Orbit Arc",
                description="+Sparkler arc width.",
                category="weapon",
                effect_values={"sparkler_cone_bonus_degrees": 10.0},
                tags=("sparkler_orbit", "sparkler_persistence"),
            )
        ]
        previews = session.current_upgrade_choice_previews()
        self.assertEqual(len(previews), 1)
        self.assertFalse(bool(previews[0]["leads_to_evolution"]))
        self.assertEqual(previews[0]["evolution_ids"], ())

    def test_game_session_continues_previewing_compatible_bottle_rocket_behaviors(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "burst_rocket"  # noqa: SLF001
        session._weapon_evolution_behavior_ids["bottle_rocket"] = {"burst_rocket"}  # noqa: SLF001
        session.run_upgrades.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="enemy_slow",
                name="Sticky Floor",
                description="-Enemy move speed.",
                category="control",
                effect_values={"enemy_speed_reduction": 0.06},
                tags=("rocket_sticky",),
            )
        ]
        previews = session.current_upgrade_choice_previews()
        self.assertEqual(len(previews), 1)
        self.assertTrue(bool(previews[0]["leads_to_evolution"]))
        self.assertIn("delayed_blast_rocket", previews[0]["evolution_ids"])

    def test_game_session_merges_compatible_bottle_rocket_behaviors_without_replacing_form(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session.run_upgrades.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="projectile_cap_up",
                name="Extra Chamber",
                description="+1 active rocket (max 5).",
                category="weapon",
                effect_values={"projectile_cap_bonus": 1.0},
                tags=("rocket_split",),
            )
        ]
        self.assertTrue(session.apply_upgrade_choice_by_index(0))

        session._current_upgrade_choices = [  # noqa: SLF001
            UpgradeDefinition(
                id="enemy_slow",
                name="Sticky Floor",
                description="-Enemy move speed.",
                category="control",
                effect_values={"enemy_speed_reduction": 0.06},
                tags=("rocket_sticky",),
            )
        ]
        self.assertTrue(session.apply_upgrade_choice_by_index(0))

        snapshot = session.weapon_evolution_snapshot()
        self.assertEqual(snapshot["active_forms_by_weapon"].get("bottle_rocket"), "burst_rocket")
        self.assertIn(
            "delayed_blast_rocket",
            snapshot["active_behavior_ids_by_weapon"].get("bottle_rocket", ()),
        )

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(getattr(session.projectiles[0], "evolution_form_id", ""), "burst_rocket")
        self.assertIn(
            "delayed_blast_rocket",
            getattr(session.projectiles[0], "evolution_behavior_ids", ()),
        )

    def test_new_evolution_balance_constants_preserve_distinct_roles(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        self.assertLess(session.DELAYED_BLAST_FUSE_SECONDS, session.BOTTLE_ROCKET_LIFETIME)
        self.assertGreaterEqual(session.PINBALL_ROCKET_MAX_BOUNCES, 3)
        self.assertGreater(session.PINBALL_ROCKET_SEARCH_RADIUS, 300.0)
        self.assertGreater(session.SPARK_AURA_RADIUS, session.ORBITING_SPARK_RADIUS)
        self.assertLessEqual(session.ORBITING_SPARK_CONTACT_COOLDOWN, session.SPARK_AURA_TICK_INTERVAL)

    def test_rocket_focused_builds_resolve_to_distinct_evolutions(self) -> None:
        burst = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split"),
        )
        sticky = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_sticky"),
        )
        pinball = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_bounce", "rocket_speed"),
        )
        chain = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_speed", "rocket_power"),
        )
        piercing = eligible_weapon_evolutions(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_speed", "rocket_split"),
        )
        self.assertEqual({item.result_form_id for item in burst}, {"burst_rocket"})
        self.assertEqual({item.result_form_id for item in sticky}, {"delayed_blast_rocket"})
        self.assertEqual({item.result_form_id for item in pinball}, {"pinball_rocket"})
        self.assertEqual({item.result_form_id for item in chain}, {"chain_rocket"})
        self.assertEqual({item.result_form_id for item in piercing}, {"piercing_rocket"})

    def test_bottle_rocket_has_six_paths_with_two_non_explosion_routes(self) -> None:
        definitions = [item for item in list_weapon_evolutions() if item.weapon_id == "bottle_rocket"]
        self.assertGreaterEqual(len(definitions), 6)
        non_explosion = [
            item for item in definitions if "rocket_explosion" not in set(item.required_tags)
        ]
        self.assertGreaterEqual(len(non_explosion), 2)

    def test_sparkler_focused_builds_resolve_to_distinct_evolutions(self) -> None:
        wide_arc = eligible_weapon_evolutions(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range", "sparkler_speed"),
        )
        orbit = eligible_weapon_evolutions(
            weapon_id="sparkler",
            acquired_tags=("sparkler_orbit", "sparkler_speed"),
        )
        aura = eligible_weapon_evolutions(
            weapon_id="sparkler",
            acquired_tags=("sparkler_range", "sparkler_persistence"),
        )
        flare_whip = eligible_weapon_evolutions(
            weapon_id="sparkler",
            acquired_tags=("sparkler_orbit", "sparkler_range"),
        )
        ember_ring = eligible_weapon_evolutions(
            weapon_id="sparkler",
            acquired_tags=("sparkler_persistence", "sparkler_speed"),
        )
        self.assertEqual({item.result_form_id for item in wide_arc}, {"wide_arc_sparkler"})
        self.assertEqual({item.result_form_id for item in orbit}, {"orbiting_sparklers"})
        self.assertEqual({item.result_form_id for item in aura}, {"spark_aura"})
        self.assertEqual({item.result_form_id for item in flare_whip}, {"flare_whip"})
        self.assertEqual({item.result_form_id for item in ember_ring}, {"ember_ring"})

    def test_sparkler_has_five_distinct_stance_paths(self) -> None:
        definitions = [item for item in list_weapon_evolutions() if item.weapon_id == "sparkler"]
        self.assertGreaterEqual(len(definitions), 5)

    def test_mixed_build_validation_keeps_one_active_form_per_weapon(self) -> None:
        bottle_tracker = WeaponEvolutionTracker()
        sparkler_tracker = WeaponEvolutionTracker()

        bottle_first = bottle_tracker.check_for_new(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split", "rocket_power", "rocket_sticky"),
        )
        bottle_second = bottle_tracker.check_for_new(
            weapon_id="bottle_rocket",
            acquired_tags=("rocket_explosion", "rocket_split", "rocket_power", "rocket_sticky", "rocket_bounce", "rocket_speed"),
        )
        sparkler_first = sparkler_tracker.check_for_new(
            weapon_id="sparkler",
            acquired_tags=("sparkler_orbit", "sparkler_speed", "sparkler_range", "sparkler_persistence"),
        )
        sparkler_second = sparkler_tracker.check_for_new(
            weapon_id="sparkler",
            acquired_tags=("sparkler_orbit", "sparkler_speed", "sparkler_range", "sparkler_persistence"),
        )

        self.assertEqual(len(bottle_first), 1)
        self.assertEqual(len(bottle_second), 1)
        self.assertEqual(len(sparkler_first), 1)
        self.assertEqual(sparkler_second, [])

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

    def test_delayed_blast_rocket_attaches_then_detonates_after_fuse(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "delayed_blast_rocket"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(430.0, 320.0)
        session.hazards = [enemy]

        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(enemy.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=280.0,
                lifetime=0.6,
                max_travel_distance=600.0,
                damage=1,
            )
        ]
        setattr(session.projectiles[0], "evolution_form_id", "delayed_blast_rocket")

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.projectiles), 1)
        self.assertTrue(bool(getattr(session.projectiles[0], "is_sticky_attached", False)))
        self.assertEqual(len(session.hazards), 1)

        session.update_playing(session.DELAYED_BLAST_FUSE_SECONDS + 0.01, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.projectiles), 0)
        self.assertEqual(len(session.hazards), 0)

    def test_delayed_blast_rocket_tracks_attached_enemy_position(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "delayed_blast_rocket"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(420.0, 320.0)
        session.hazards = [enemy]

        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(enemy.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=280.0,
                lifetime=0.6,
                max_travel_distance=600.0,
                damage=1,
            )
        ]
        setattr(session.projectiles[0], "evolution_form_id", "delayed_blast_rocket")

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        enemy.position = pygame.Vector2(520.0, 360.0)
        session.update_playing(0.1, pygame.Vector2(0.0, 0.0), attack=False)
        projectile_center = pygame.Vector2(session.projectiles[0].rect.center)
        enemy_center = pygame.Vector2(enemy.rect.center)
        self.assertLessEqual(projectile_center.distance_to(enemy_center), 4.0)

    def test_delayed_blast_rocket_prevents_duplicate_attachment_on_same_enemy(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "delayed_blast_rocket"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(430.0, 320.0)
        session.hazards = [enemy]

        first = BottleRocket(
            position=pygame.Vector2(enemy.rect.center),
            direction=pygame.Vector2(1.0, 0.0),
            speed=280.0,
            lifetime=0.6,
            max_travel_distance=600.0,
            damage=1,
        )
        second = BottleRocket(
            position=pygame.Vector2(enemy.rect.center),
            direction=pygame.Vector2(1.0, 0.0),
            speed=280.0,
            lifetime=0.6,
            max_travel_distance=600.0,
            damage=1,
        )
        setattr(first, "evolution_form_id", "delayed_blast_rocket")
        setattr(second, "evolution_form_id", "delayed_blast_rocket")
        session.projectiles = [first, second]

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        attached_count = sum(bool(getattr(projectile, "is_sticky_attached", False)) for projectile in session.projectiles)
        self.assertEqual(attached_count, 1)

    def test_delayed_blast_rocket_triggers_buildup_feedback_before_detonation(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "delayed_blast_rocket"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(430.0, 320.0)
        session.hazards = [enemy]
        session.projectiles = [
            BottleRocket(
                position=pygame.Vector2(enemy.rect.center),
                direction=pygame.Vector2(1.0, 0.0),
                speed=280.0,
                lifetime=0.6,
                max_travel_distance=600.0,
                damage=1,
            )
        ]
        setattr(session.projectiles[0], "evolution_form_id", "delayed_blast_rocket")

        session.update_playing(0.016, pygame.Vector2(0.0, 0.0), attack=False)
        particle_count_before = len(session.confetti.particles)
        session.update_playing(
            session.DELAYED_BLAST_FUSE_SECONDS - session.DELAYED_BLAST_BUILDUP_WINDOW,
            pygame.Vector2(0.0, 0.0),
            attack=False,
        )
        self.assertGreater(len(session.confetti.particles), particle_count_before)
        self.assertTrue(bool(getattr(session.projectiles[0], "sticky_buildup_triggered", False)))

    def test_pinball_rocket_redirects_to_nearby_enemy_and_stays_active(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "pinball_rocket"  # noqa: SLF001

        first_enemy = BalloonEnemy(speed=0.0)
        first_enemy.position = pygame.Vector2(420.0, 320.0)
        second_enemy = BalloonEnemy(speed=0.0)
        second_enemy.position = pygame.Vector2(500.0, 320.0)
        session.hazards = [first_enemy, second_enemy]

        rocket = BottleRocket(
            position=pygame.Vector2(first_enemy.rect.center),
            direction=pygame.Vector2(1.0, 0.0),
            speed=280.0,
            lifetime=0.6,
            max_travel_distance=600.0,
            damage=1,
        )
        setattr(rocket, "evolution_form_id", "pinball_rocket")
        setattr(rocket, "pinball_bounces_remaining", 2)
        session.projectiles = [rocket]

        session._check_projectile_collisions()
        self.assertEqual(len(session.projectiles), 1)
        self.assertEqual(len(session.hazards), 1)
        self.assertLessEqual(int(getattr(session.projectiles[0], "pinball_bounces_remaining", 0)), 1)
        self.assertGreater(session.projectiles[0].direction.x, 0.0)

    def test_pinball_rocket_expires_after_bounce_limit_is_spent(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "pinball_rocket"  # noqa: SLF001

        first_enemy = BalloonEnemy(speed=0.0)
        first_enemy.position = pygame.Vector2(420.0, 320.0)
        second_enemy = BalloonEnemy(speed=0.0)
        second_enemy.position = pygame.Vector2(500.0, 320.0)
        third_enemy = BalloonEnemy(speed=0.0)
        third_enemy.position = pygame.Vector2(580.0, 320.0)
        session.hazards = [first_enemy, second_enemy, third_enemy]

        rocket = BottleRocket(
            position=pygame.Vector2(first_enemy.rect.center),
            direction=pygame.Vector2(1.0, 0.0),
            speed=280.0,
            lifetime=0.6,
            max_travel_distance=600.0,
            damage=1,
        )
        setattr(rocket, "evolution_form_id", "pinball_rocket")
        setattr(rocket, "pinball_bounces_remaining", 2)
        session.projectiles = [rocket]

        session._check_projectile_collisions()
        session.projectiles[0].position = pygame.Vector2(second_enemy.rect.center)
        session._check_projectile_collisions()
        self.assertEqual(len(session.projectiles), 1)
        self.assertEqual(int(getattr(session.projectiles[0], "pinball_bounces_remaining", 0)), 0)

        session.projectiles[0].position = pygame.Vector2(third_enemy.rect.center)
        session._check_projectile_collisions()
        self.assertEqual(len(session.projectiles), 0)

    def test_pinball_rocket_prefers_unvisited_target_when_multiple_candidates_exist(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "pinball_rocket"  # noqa: SLF001

        first_enemy = PinataEnemy(speed=0.0, max_health=3, damage_per_hit=1)
        first_enemy.position = pygame.Vector2(420.0, 320.0)
        second_enemy = BalloonEnemy(speed=0.0)
        second_enemy.position = pygame.Vector2(500.0, 320.0)
        third_enemy = BalloonEnemy(speed=0.0)
        third_enemy.position = pygame.Vector2(620.0, 320.0)
        session.hazards = [first_enemy, second_enemy, third_enemy]

        rocket = BottleRocket(
            position=pygame.Vector2(first_enemy.rect.center),
            direction=pygame.Vector2(1.0, 0.0),
            speed=280.0,
            lifetime=0.6,
            max_travel_distance=600.0,
            damage=1,
        )
        setattr(rocket, "evolution_form_id", "pinball_rocket")
        setattr(rocket, "pinball_bounces_remaining", 2)
        setattr(rocket, "pinball_hit_target_ids", set())
        session.projectiles = [rocket]

        session._check_projectile_collisions()
        session.projectiles[0].position = pygame.Vector2(second_enemy.rect.center)
        session._check_projectile_collisions()
        self.assertEqual(len(session.projectiles), 1)
        self.assertGreater(session.projectiles[0].direction.x, 0.0)
        self.assertIn(id(first_enemy), getattr(session.projectiles[0], "pinball_hit_target_ids", set()))

    def test_pinball_rocket_expires_when_no_valid_next_target_exists(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("bottle_rocket")
        session._weapon_evolution_forms["bottle_rocket"] = "pinball_rocket"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(420.0, 320.0)
        session.hazards = [enemy]

        rocket = BottleRocket(
            position=pygame.Vector2(enemy.rect.center),
            direction=pygame.Vector2(1.0, 0.0),
            speed=280.0,
            lifetime=0.6,
            max_travel_distance=600.0,
            damage=1,
        )
        setattr(rocket, "evolution_form_id", "pinball_rocket")
        setattr(rocket, "pinball_bounces_remaining", 2)
        setattr(rocket, "pinball_hit_target_ids", set())
        session.projectiles = [rocket]

        session._check_projectile_collisions()
        self.assertEqual(len(session.projectiles), 0)

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

    def test_spark_aura_radius_scales_with_range_upgrade(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "spark_aura"  # noqa: SLF001

        baseline_radius = session._current_spark_aura_radius()  # noqa: SLF001
        session.run_upgrades.stacks["sparkler_range_up"] = 1
        upgraded_radius = session._current_spark_aura_radius()  # noqa: SLF001

        self.assertGreater(upgraded_radius, baseline_radius)

    def test_spark_aura_visual_draws_visible_radius_feedback(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "spark_aura"  # noqa: SLF001
        session._spark_aura_tick_timer = session.SPARK_AURA_TICK_INTERVAL * 0.5  # noqa: SLF001

        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session.draw_playing(surface)

        center = pygame.Vector2(session.player.rect.center)
        visible_samples = 0
        aura_radius = session._current_spark_aura_radius()  # noqa: SLF001
        for sample_index in range(12):
            sample_position = center + pygame.Vector2(aura_radius * 0.75, 0.0).rotate(sample_index * 30.0)
            if surface.get_at((int(sample_position.x), int(sample_position.y))).a > 0:
                visible_samples += 1
        self.assertGreater(visible_samples, 0)

    def test_orbiting_sparklers_rotate_while_maintaining_fixed_radius(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "orbiting_sparklers"  # noqa: SLF001

        before = session._orbiting_spark_positions()  # noqa: SLF001
        before_distances = [
            position.distance_to(pygame.Vector2(session.player.rect.center)) for position in before
        ]

        session.update_playing(0.2, pygame.Vector2(0.0, 0.0), attack=False)

        after = session._orbiting_spark_positions()  # noqa: SLF001
        after_distances = [
            position.distance_to(pygame.Vector2(session.player.rect.center)) for position in after
        ]
        self.assertNotEqual(
            [(round(position.x, 2), round(position.y, 2)) for position in before],
            [(round(position.x, 2), round(position.y, 2)) for position in after],
        )
        for distance in before_distances + after_distances:
            self.assertAlmostEqual(distance, session.ORBITING_SPARK_RADIUS, places=2)

    def test_orbiting_sparklers_replace_swing_and_damage_on_contact(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "orbiting_sparklers"  # noqa: SLF001

        enemy = BalloonEnemy(speed=0.0)
        enemy.position = pygame.Vector2(
            session.player.rect.centerx + session.ORBITING_SPARK_RADIUS,
            session.player.rect.centery,
        )
        session.hazards = [enemy]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(session.sparkler_attack_snapshot(), {})
        self.assertEqual(len(session.hazards), 1)

        session.update_playing(0.01, pygame.Vector2(0.0, 0.0), attack=False)
        self.assertEqual(len(session.hazards), 0)

    def test_orbiting_spark_visual_draws_visible_glow_and_trails(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")
        session._weapon_evolution_forms["sparkler"] = "orbiting_sparklers"  # noqa: SLF001
        session._orbiting_spark_angle_degrees = 24.0  # noqa: SLF001

        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session.draw_playing(surface)

        spark_position = session._orbiting_spark_positions()[0]  # noqa: SLF001
        sampled_alpha = surface.get_at((int(spark_position.x), int(spark_position.y))).a
        orbit_pixels_visible = 0
        orbit_center = pygame.Vector2(session.player.rect.center)
        for sample_index in range(12):
            sample_position = orbit_center + pygame.Vector2(session.ORBITING_SPARK_RADIUS, 0.0).rotate(
                sample_index * 30.0
            )
            if surface.get_at((int(sample_position.x), int(sample_position.y))).a > 0:
                orbit_pixels_visible += 1
        self.assertGreater(sampled_alpha, 0)
        self.assertGreater(orbit_pixels_visible, 0)


if __name__ == "__main__":
    unittest.main()
