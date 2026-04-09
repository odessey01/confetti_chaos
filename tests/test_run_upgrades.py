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

from systems.run_upgrades import RunUpgradeSystem  # noqa: E402


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
        self.assertFalse(upgrades.is_valid_choice("projectile_damage_up", active_weapon_id="sparkler"))
        self.assertFalse(upgrades.is_valid_choice("projectile_cap_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_range_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_damage_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("sparkler_arc_up", active_weapon_id="sparkler"))
        self.assertTrue(upgrades.is_valid_choice("projectile_speed_up", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_range_up", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_damage_up", active_weapon_id="bottle_rocket"))
        self.assertFalse(upgrades.is_valid_choice("sparkler_arc_up", active_weapon_id="bottle_rocket"))

    def test_generate_choices_for_sparkler_excludes_projectile_only_upgrades(self) -> None:
        upgrades = RunUpgradeSystem(rng=random.Random(23))
        saw_sparkler_specific = False
        for _ in range(40):
            choices = upgrades.generate_choices(count=3, active_weapon_id="sparkler")
            ids = {choice.id for choice in choices}
            self.assertNotIn("projectile_speed_up", ids)
            self.assertNotIn("projectile_damage_up", ids)
            self.assertNotIn("projectile_cap_up", ids)
            if {"sparkler_range_up", "sparkler_damage_up", "sparkler_arc_up"} & ids:
                saw_sparkler_specific = True
        self.assertTrue(saw_sparkler_specific)
