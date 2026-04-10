"""Validation tests for character unlock condition definitions and checks."""

from __future__ import annotations

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.character_unlocks import (  # noqa: E402
    BUNNY_UNLOCK_REQUIRED_RUNS,
    CAT_UNLOCK_REQUIRED_HIGH_SCORE,
    RACCOON_UNLOCK_REQUIRED_BOSSES,
    UnlockProgressSnapshot,
    evaluate_unlock_progress,
    get_character_unlock_condition,
    is_character_unlocked,
    is_unlock_condition_met,
    list_character_unlock_conditions,
    refresh_meta_unlock_state,
    unlock_thresholds_snapshot,
)
from systems.meta_progression import MetaProgression  # noqa: E402


class CharacterUnlockConditionValidationTests(unittest.TestCase):
    def test_expected_conditions_exist(self) -> None:
        conditions = list_character_unlock_conditions()
        by_character = {definition.character_id: definition for definition in conditions}
        self.assertIn("teddy_f", by_character)
        self.assertIn("bunny_f", by_character)
        self.assertIn("cat_f", by_character)
        self.assertIn("fox_f", by_character)

    def test_bear_unlocked_by_default(self) -> None:
        bear = get_character_unlock_condition("teddy_f")
        self.assertIsNotNone(bear)
        assert bear is not None
        self.assertTrue(bear.unlocked_by_default)
        self.assertTrue(is_unlock_condition_met(bear, UnlockProgressSnapshot()))

    def test_bunny_unlock_requires_five_runs(self) -> None:
        bunny = get_character_unlock_condition("bunny_f")
        self.assertIsNotNone(bunny)
        assert bunny is not None
        self.assertFalse(
            is_unlock_condition_met(
                bunny,
                UnlockProgressSnapshot(total_runs_completed=4),
            )
        )
        self.assertTrue(
            is_unlock_condition_met(
                bunny,
                UnlockProgressSnapshot(total_runs_completed=5),
            )
        )

    def test_cat_unlock_requires_high_score_threshold(self) -> None:
        cat = get_character_unlock_condition("cat_f")
        self.assertIsNotNone(cat)
        assert cat is not None
        self.assertFalse(
            is_unlock_condition_met(cat, UnlockProgressSnapshot(high_score=9_999))
        )
        self.assertTrue(
            is_unlock_condition_met(cat, UnlockProgressSnapshot(high_score=10_000))
        )

    def test_raccoon_unlock_requires_bosses_defeated(self) -> None:
        raccoon = get_character_unlock_condition("fox_f")
        self.assertIsNotNone(raccoon)
        assert raccoon is not None
        self.assertFalse(
            is_unlock_condition_met(raccoon, UnlockProgressSnapshot(bosses_defeated=9))
        )
        self.assertTrue(
            is_unlock_condition_met(raccoon, UnlockProgressSnapshot(bosses_defeated=10))
        )

    def test_evaluate_unlock_progress_returns_unlocked_characters_and_conditions(self) -> None:
        unlocked, met_conditions = evaluate_unlock_progress(
            UnlockProgressSnapshot(total_runs_completed=5, high_score=11_000, bosses_defeated=10)
        )
        self.assertIn("teddy_f", unlocked)
        self.assertIn("bunny_f", unlocked)
        self.assertIn("cat_f", unlocked)
        self.assertIn("fox_f", unlocked)
        self.assertIn("unlock_teddy_default", met_conditions)
        self.assertIn("unlock_bunny_runs", met_conditions)
        self.assertIn("unlock_cat_score", met_conditions)
        self.assertIn("unlock_raccoon_bosses", met_conditions)

    def test_is_character_unlocked_uses_meta_progression_state(self) -> None:
        meta = MetaProgression(unlocked_characters=["teddy_f", "bunny_f"])
        self.assertTrue(is_character_unlocked(meta, "teddy_f"))
        self.assertTrue(is_character_unlocked(meta, "bunny_f"))
        self.assertFalse(is_character_unlocked(meta, "cat_f"))

    def test_refresh_meta_unlock_state_updates_unlock_lists_from_meta_stats(self) -> None:
        meta = MetaProgression(
            unlocked_characters=["teddy_f"],
            unlock_conditions_met=[],
            total_runs_completed=BUNNY_UNLOCK_REQUIRED_RUNS,
            bosses_defeated=RACCOON_UNLOCK_REQUIRED_BOSSES,
            best_score=CAT_UNLOCK_REQUIRED_HIGH_SCORE,
        )
        changed = refresh_meta_unlock_state(meta)
        self.assertTrue(changed)
        self.assertIn("bunny_f", meta.unlocked_characters)
        self.assertIn("cat_f", meta.unlocked_characters)
        self.assertIn("fox_f", meta.unlocked_characters)
        self.assertIn("unlock_bunny_runs", meta.unlock_conditions_met)
        self.assertIn("unlock_cat_score", meta.unlock_conditions_met)
        self.assertIn("unlock_raccoon_bosses", meta.unlock_conditions_met)

    def test_unlock_thresholds_snapshot_exposes_tunable_targets(self) -> None:
        snapshot = unlock_thresholds_snapshot()
        self.assertEqual(snapshot["bunny_required_runs_completed"], BUNNY_UNLOCK_REQUIRED_RUNS)
        self.assertEqual(snapshot["cat_required_high_score"], CAT_UNLOCK_REQUIRED_HIGH_SCORE)
        self.assertEqual(snapshot["raccoon_required_bosses_defeated"], RACCOON_UNLOCK_REQUIRED_BOSSES)

    def test_end_to_end_unlock_paths_unlock_each_character(self) -> None:
        unlocked_initial, _ = evaluate_unlock_progress(UnlockProgressSnapshot())
        self.assertEqual(unlocked_initial, ("teddy_f",))

        unlocked_bunny, _ = evaluate_unlock_progress(
            UnlockProgressSnapshot(total_runs_completed=BUNNY_UNLOCK_REQUIRED_RUNS)
        )
        self.assertIn("bunny_f", unlocked_bunny)

        unlocked_cat, _ = evaluate_unlock_progress(
            UnlockProgressSnapshot(high_score=CAT_UNLOCK_REQUIRED_HIGH_SCORE)
        )
        self.assertIn("cat_f", unlocked_cat)

        unlocked_raccoon, _ = evaluate_unlock_progress(
            UnlockProgressSnapshot(bosses_defeated=RACCOON_UNLOCK_REQUIRED_BOSSES)
        )
        self.assertIn("fox_f", unlocked_raccoon)


if __name__ == "__main__":
    unittest.main()
