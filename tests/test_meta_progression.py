"""Validation tests for persistent meta progression data behavior."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.meta_progression import (  # noqa: E402
    DEFAULT_UNLOCKED_CHARACTERS,
    MetaProgression,
    load_meta_progression,
    save_meta_progression,
)


class MetaProgressionValidationTests(unittest.TestCase):
    def test_missing_file_returns_default_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = pathlib.Path(tmp_dir) / "meta_progression.json"
            loaded = load_meta_progression(file_path)
            self.assertEqual(tuple(loaded.unlocked_characters), DEFAULT_UNLOCKED_CHARACTERS)
            self.assertEqual(loaded.unlock_conditions_met, [])
            self.assertEqual(loaded.total_runs_completed, 0)
            self.assertEqual(loaded.bosses_defeated, 0)
            self.assertEqual(loaded.best_score, 0)

    def test_save_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = pathlib.Path(tmp_dir) / "meta_progression.json"
            source = MetaProgression(
                unlocked_characters=["teddy_f", "bunny_f", "cat_f"],
                unlock_conditions_met=["unlock_bunny_runs", "unlock_cat_score"],
                total_runs_completed=12,
                bosses_defeated=4,
                best_score=17_500,
            )
            save_meta_progression(source, file_path)
            loaded = load_meta_progression(file_path)
            self.assertEqual(loaded.unlocked_characters, ["bunny_f", "cat_f", "teddy_f"])
            self.assertEqual(
                loaded.unlock_conditions_met,
                ["unlock_bunny_runs", "unlock_cat_score"],
            )
            self.assertEqual(loaded.total_runs_completed, 12)
            self.assertEqual(loaded.bosses_defeated, 4)
            self.assertEqual(loaded.best_score, 17_500)

    def test_corrupt_file_falls_back_to_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = pathlib.Path(tmp_dir) / "meta_progression.json"
            file_path.write_text("{invalid-json", encoding="utf-8")
            loaded = load_meta_progression(file_path)
            self.assertEqual(tuple(loaded.unlocked_characters), DEFAULT_UNLOCKED_CHARACTERS)
            self.assertEqual(loaded.unlock_conditions_met, [])
            self.assertEqual(loaded.total_runs_completed, 0)
            self.assertEqual(loaded.bosses_defeated, 0)
            self.assertEqual(loaded.best_score, 0)


if __name__ == "__main__":
    unittest.main()
