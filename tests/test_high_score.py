"""Validation tests for high score persistence behavior."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.high_score import load_high_score, save_high_score  # noqa: E402


class HighScoreValidationTests(unittest.TestCase):
    def test_missing_file_defaults_to_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = pathlib.Path(tmp_dir) / "high_score.json"
            self.assertEqual(load_high_score(file_path), 0)

    def test_save_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = pathlib.Path(tmp_dir) / "high_score.json"
            save_high_score(42, file_path)
            self.assertEqual(load_high_score(file_path), 42)

    def test_corrupt_file_falls_back_to_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = pathlib.Path(tmp_dir) / "high_score.json"
            file_path.write_text("{not-valid-json", encoding="utf-8")
            self.assertEqual(load_high_score(file_path), 0)
