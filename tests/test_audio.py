"""Validation tests for background music toggle integration."""

from __future__ import annotations

import pathlib
import sys
import unittest
from unittest.mock import Mock, patch


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.audio import AudioManager  # noqa: E402


class AudioValidationTests(unittest.TestCase):
    @patch("systems.audio.pygame.mixer.music.stop")
    @patch("systems.audio.pygame.mixer.music.play")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_music_loop_respects_enabled_and_state(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        load_music: Mock,
        _set_volume: Mock,
        play_music: Mock,
        stop_music: Mock,
    ) -> None:
        manager = AudioManager()
        self.assertTrue(load_music.called)

        manager.sync_music_for_state("MENU")
        self.assertEqual(play_music.call_count, 1)

        # Still in music-enabled state should not restart playback repeatedly.
        manager.sync_music_for_state("PLAYING")
        self.assertEqual(play_music.call_count, 1)

        manager.set_enabled(False)
        self.assertEqual(stop_music.call_count, 1)

        manager.set_enabled(True)
        self.assertEqual(play_music.call_count, 2)

        manager.sync_music_for_state("UNKNOWN")
        self.assertEqual(stop_music.call_count, 2)

    @patch("systems.audio.pygame.mixer.music.play")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load", side_effect=OSError("missing"))
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_missing_music_file_does_not_crash(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        play_music: Mock,
    ) -> None:
        manager = AudioManager()
        manager.sync_music_for_state("MENU")
        manager.set_enabled(False)
        self.assertEqual(play_music.call_count, 0)

