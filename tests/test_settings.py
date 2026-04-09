"""Validation tests for runtime settings persistence."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.settings import RuntimeSettings, load_settings, save_settings  # noqa: E402


class SettingsValidationTests(unittest.TestCase):
    def test_save_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "settings.json"
            original = RuntimeSettings(
                music_enabled=False,
                aim_assist_enabled=False,
                selected_start_level=4,
                master_volume=0.6,
                music_volume=0.5,
                sfx_volume=0.4,
                ambient_volume=0.3,
            )
            save_settings(original, path=path)

            loaded = load_settings(path=path)
            self.assertFalse(loaded.music_enabled)
            self.assertFalse(loaded.aim_assist_enabled)
            self.assertEqual(loaded.selected_start_level, 4)
            self.assertAlmostEqual(loaded.master_volume, 0.6)
            self.assertAlmostEqual(loaded.music_volume, 0.5)
            self.assertAlmostEqual(loaded.sfx_volume, 0.4)
            self.assertAlmostEqual(loaded.ambient_volume, 0.3)

    def test_missing_file_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "settings.json"
            loaded = load_settings(path=path)
            self.assertTrue(loaded.music_enabled)
            self.assertTrue(loaded.aim_assist_enabled)
            self.assertEqual(loaded.selected_start_level, 1)
            self.assertAlmostEqual(loaded.master_volume, 0.8)
            self.assertAlmostEqual(loaded.music_volume, 0.7)
            self.assertAlmostEqual(loaded.sfx_volume, 0.9)
            self.assertAlmostEqual(loaded.ambient_volume, 0.5)

    def test_corrupt_file_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "settings.json"
            path.write_text("{bad-json", encoding="utf-8")
            loaded = load_settings(path=path)
            self.assertTrue(loaded.music_enabled)
            self.assertTrue(loaded.aim_assist_enabled)
            self.assertEqual(loaded.selected_start_level, 1)
            self.assertAlmostEqual(loaded.master_volume, 0.8)
            self.assertAlmostEqual(loaded.music_volume, 0.7)
            self.assertAlmostEqual(loaded.sfx_volume, 0.9)
            self.assertAlmostEqual(loaded.ambient_volume, 0.5)

    def test_partial_or_invalid_values_fall_back(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "settings.json"
            path.write_text(
                (
                    '{"music_enabled": false, "aim_assist_enabled": false, "selected_start_level": -3, '
                    '"master_volume": 2.0, "music_volume": -0.1, '
                    '"sfx_volume": "bad", "ambient_volume": 0.25}'
                ),
                encoding="utf-8",
            )
            loaded = load_settings(path=path)
            self.assertFalse(loaded.music_enabled)
            self.assertFalse(loaded.aim_assist_enabled)
            self.assertEqual(loaded.selected_start_level, 1)
            self.assertAlmostEqual(loaded.master_volume, 1.0)
            self.assertAlmostEqual(loaded.music_volume, 0.0)
            self.assertAlmostEqual(loaded.sfx_volume, 0.9)
            self.assertAlmostEqual(loaded.ambient_volume, 0.25)
