"""Validation tests for upgrade model, choice generation, and filtering."""

from __future__ import annotations

import pathlib
import random
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.run_upgrades import (  # noqa: E402
    RunUpgradeSystem,
    missing_tags_in_upgrade_pool,
    upgrade_ids_by_tag,
    upgrade_tag_pool,
)


class RunUpgradeSystemValidationTests(unittest.TestCase):
    def test_generate_choices_returns_up_to_three_unique_valid_options(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(7))
        choices = upgrades.generate_choices(count=3)
        self.assertGreaterEqual(len(choices), 1)
        self.assertLessEqual(len(choices), 3)
        ids = [choice.id for choice in choices]
        self.assertEqual(len(ids), len(set(ids)))
        for upgrade_id in ids:
            self.assertTrue(upgrades.is_valid_choice(upgrade_id))

    def test_apply_choice_increments_stack_and_effects(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(11))
        upgrades.current_choices = upgrades.generate_choices(count=3)
        picked = upgrades.current_choices[0]
        self.assertTrue(upgrades.apply_choice(picked.id))
        self.assertEqual(upgrades.stack_count(picked.id), 1)
        effects = upgrades.effects_snapshot()
        self.assertGreater(len(effects), 0)

    def test_capped_upgrade_becomes_invalid(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(17))
        upgrades.stacks["projectile_cap_up"] = 2
        self.assertFalse(upgrades.is_valid_choice("projectile_cap_up"))

    def test_projectile_upgrades_are_invalid_for_sparkler_weapon_context(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(19))
        self.assertFalse(upgrades.is_valid_choice("projectile_speed_up", active_weapon_id="sparkler"))
        self.assertFalse(upgrades.is_valid_choice("ricochet_rounds", active_weapon_id="sparkler"))
        self.assertFalse(upgrades.is_valid_choice("projectile_damage_up", active_weapon_id="sparkler"))
        self.assertFalse(upgrades.is_valid_choice("projectile_cap_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_range_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_damage_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_arc_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_duration_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("projectile_speed_up", active_weapon_id="bottle_rocket"))
        self.assertTrue(upgrades.is_valid_choice("ricochet_rounds", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_range_up", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_damage_up", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_arc_up", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_duration_up", active_weapon_id="bottle_rocket"))

    def test_generate_choices_for_sparkler_excludes_projectile_only_upgrades(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(23))
        saw_sparkler_specific = False
        for _ in range(40):
            choices = upgrades.generate_choices(count=3, active_weapon_id="sparkler")
            ids = {choice.id for choice in choices}
            self.assertNotIn("projectile_speed_up", ids)
            self.assertNotIn("ricochet_rounds", ids)
            self.assertNotIn("projectile_damage_up", ids)
            self.assertNotIn("projectile_cap_up", ids)
            if {"sparkler_range_up", "sparkler_damage_up", "sparkler_arc_up", "sparkler_duration_up"} & ids:
                saw_sparkler_specific = True
        self.assertTrue(saw_sparkler_specific)

    def test_upgrade_tags_are_queryable_and_tracked_after_apply(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(31))
        self.assertIn("rocket_split", upgrades.tags_for_upgrade("projectile_cap_up"))
        self.assertEqual(upgrades.tags_for_upgrade("projectile_speed_up"), ("rocket_speed",))
        self.assertIn("rocket_bounce", upgrades.tags_for_upgrade("ricochet_rounds"))
        self.assertIn("rocket_sticky", upgrades.tags_for_upgrade("enemy_slow"))
        self.assertIn("sparkler_range", upgrades.tags_for_upgrade("sparkler_range_up"))
        self.assertIn("sparkler_orbit", upgrades.tags_for_upgrade("sparkler_arc_up"))
        self.assertEqual(upgrades.tags_for_upgrade("sparkler_arc_up"), ("sparkler_orbit",))
        self.assertIn("sparkler_persistence", upgrades.tags_for_upgrade("sparkler_duration_up"))

        upgrades.apply_choice("projectile_cap_up", active_weapon_id="bottle_rocket")
        upgrades.apply_choice("ricochet_rounds", active_weapon_id="bottle_rocket")
        upgrades.apply_choice("enemy_slow")
        upgrades.apply_choice("sparkler_arc_up", active_weapon_id="sparkler")
        upgrades.apply_choice("sparkler_duration_up", active_weapon_id="sparkler")

        acquired = set(upgrades.acquired_tags())
        self.assertIn("rocket_split", acquired)
        self.assertIn("rocket_bounce", acquired)
        self.assertIn("rocket_sticky", acquired)
        self.assertIn("sparkler_orbit", acquired)
        self.assertIn("sparkler_persistence", acquired)
        self.assertTrue(upgrades.has_tag("rocket_split"))
        self.assertTrue(
            upgrades.has_all_tags(
                ("rocket_split", "rocket_bounce", "rocket_sticky", "sparkler_orbit", "sparkler_persistence")
            )
        )

    def test_upgrade_state_tracks_acquired_upgrade_ids(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(37))
        upgrades.apply_choice("move_speed_up")
        upgrades.apply_choice("fire_rate_up")
        acquired = upgrades.acquired_upgrade_ids()
        self.assertIn("move_speed_up", acquired)
        self.assertIn("fire_rate_up", acquired)

    def test_upgrade_tag_pool_helpers_expose_expected_tags_and_sources(self) -> None:
        pool = set(upgrade_tag_pool())
        self.assertIn("rocket_explosion", pool)
        self.assertIn("rocket_split", pool)
        self.assertIn("rocket_sticky", pool)
        self.assertIn("rocket_bounce", pool)
        self.assertIn("sparkler_range", pool)
        self.assertIn("sparkler_orbit", pool)
        self.assertIn("sparkler_persistence", pool)
        by_tag = upgrade_ids_by_tag()
        self.assertIn("confetti_burst_up", by_tag.get("rocket_explosion", ()))
        self.assertIn("projectile_cap_up", by_tag.get("rocket_split", ()))
        self.assertIn("enemy_slow", by_tag.get("rocket_sticky", ()))
        self.assertIn("ricochet_rounds", by_tag.get("rocket_bounce", ()))
        self.assertIn("sparkler_arc_up", by_tag.get("sparkler_orbit", ()))
        self.assertIn("sparkler_duration_up", by_tag.get("sparkler_persistence", ()))
        self.assertEqual(
            missing_tags_in_upgrade_pool(
                {
                    "rocket_explosion",
                    "rocket_split",
                    "rocket_sticky",
                    "rocket_bounce",
                    "sparkler_range",
                    "sparkler_orbit",
                    "sparkler_persistence",
                }
            ),
            (),
        )

    def test_evolution_tagged_options_are_offered_more_often_with_bias(self) -> None:
        draws = 250
        with_bias = RunUpgradeSystem(rng=random.Random(101))
        with_bias.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        with_bias_hits = 0
        for _ in range(draws):
            ids = {
                choice.id
                for choice in with_bias.generate_choices(
                    count=3,
                    active_weapon_id="bottle_rocket",
                )
            }
            if "projectile_cap_up" in ids:
                with_bias_hits += 1

        without_bias = RunUpgradeSystem(rng=random.Random(101))
        without_bias.apply_choice("confetti_burst_up", active_weapon_id="bottle_rocket")
        without_bias_hits = 0
        for _ in range(draws):
            ids = {
                choice.id
                for choice in without_bias.generate_choices(
                    count=3,
                    active_weapon_id="bottle_rocket",
                    evolution_exclude_ids=("burst_rocket", "big_pop_rocket", "piercing_rocket"),
                )
            }
            if "projectile_cap_up" in ids:
                without_bias_hits += 1

        self.assertGreater(with_bias_hits, without_bias_hits)
