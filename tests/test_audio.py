"""Validation tests for centralized audio categories and music integration."""

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
from main import GameState, desired_ambient_track_for_state, desired_music_track_for_state  # noqa: E402


class AudioValidationTests(unittest.TestCase):
    @patch("systems.audio.pygame.time.get_ticks")
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_repeated_weapon_fire_is_cooldown_limited(
        self,
        _get_init: Mock,
        _init: Mock,
        sound_ctor: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        _channel: Mock,
        get_ticks: Mock,
    ) -> None:
        sound_obj = Mock()
        sound_ctor.return_value = sound_obj
        manager = AudioManager()
        get_ticks.return_value = 100
        manager.play_sfx("weapon_fire")
        get_ticks.return_value = 110
        manager.play_sfx("weapon_fire")
        get_ticks.return_value = 200
        manager.play_sfx("weapon_fire")
        self.assertEqual(sound_obj.play.call_count, 2)

    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_named_sfx_and_ambient_do_not_crash_when_missing(
        self,
        _get_init: Mock,
        _init: Mock,
        sound_ctor: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        channel_ctor: Mock,
    ) -> None:
        sound_ctor.side_effect = OSError("missing")
        channel = Mock()
        channel_ctor.return_value = channel
        manager = AudioManager()

        manager.play_sfx("weapon_fire")
        manager.play_sfx("ui_nav")
        manager.play_ambient("gameplay")
        manager.stop_ambient()
        channel.stop.assert_called()

    @patch("systems.audio.pygame.mixer.music.stop")
    @patch("systems.audio.pygame.mixer.music.play")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_music_loop_respects_enabled_and_state(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        _channel: Mock,
        load_music: Mock,
        _set_volume: Mock,
        play_music: Mock,
        stop_music: Mock,
    ) -> None:
        manager = AudioManager()
        self.assertFalse(load_music.called)

        manager.sync_music_for_state("MENU")
        self.assertTrue(load_music.called)
        self.assertEqual(play_music.call_count, 1)

        # Change to gameplay track should load and play once more.
        manager.sync_music_for_state("PLAYING")
        self.assertEqual(play_music.call_count, 2)

        # Staying in gameplay should not overlap/restart.
        manager.sync_music_for_state("PAUSED")
        self.assertEqual(play_music.call_count, 2)

        manager.set_enabled(False)
        self.assertGreaterEqual(stop_music.call_count, 1)

        manager.set_enabled(True)
        self.assertEqual(play_music.call_count, 3)

        manager.sync_music_for_state("UNKNOWN")
        self.assertGreaterEqual(stop_music.call_count, 2)

    @patch("systems.audio.pygame.mixer.music.play")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load", side_effect=OSError("missing"))
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_missing_music_file_does_not_crash(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        _channel: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        play_music: Mock,
    ) -> None:
        manager = AudioManager()
        manager.play_music("menu")
        manager.sync_music_for_state("MENU")
        manager.set_enabled(False)
        self.assertEqual(play_music.call_count, 0)

    @patch("systems.audio.pygame.mixer.music.play")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_play_music_and_stop_music_explicit_controls(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        _channel: Mock,
        load_music: Mock,
        _set_volume: Mock,
        play_music: Mock,
    ) -> None:
        manager = AudioManager()
        manager.play_music("menu")
        self.assertEqual(play_music.call_count, 1)
        manager.play_music("menu")
        self.assertEqual(play_music.call_count, 1)
        manager.stop_music()
        manager.play_music("menu")
        self.assertEqual(play_music.call_count, 2)
        self.assertTrue(load_music.called)

    @patch("systems.audio.pygame.mixer.music.play")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_boss_track_override_mapping(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        _channel: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        play_music: Mock,
    ) -> None:
        manager = AudioManager()
        self.assertEqual(desired_music_track_for_state(GameState.MENU, boss_active=False), "menu")
        self.assertEqual(desired_music_track_for_state(GameState.PLAYING, boss_active=False), "gameplay")
        self.assertEqual(desired_music_track_for_state(GameState.PLAYING, boss_active=True), "boss")
        self.assertEqual(desired_music_track_for_state(GameState.GAME_OVER, boss_active=True), "gameplay")

        manager.play_music("gameplay")
        manager.play_music("boss")
        self.assertEqual(play_music.call_count, 2)

    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_ambient_track_mapping_and_lifecycle(
        self,
        _get_init: Mock,
        _init: Mock,
        sound_ctor: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        channel_ctor: Mock,
    ) -> None:
        channel = Mock()
        sound = Mock()
        channel_ctor.return_value = channel
        sound_ctor.return_value = sound
        manager = AudioManager()

        self.assertEqual(desired_ambient_track_for_state(GameState.PLAYING), "gameplay")
        self.assertIsNone(desired_ambient_track_for_state(GameState.MENU))

        manager.play_ambient("gameplay")
        channel.play.assert_called()

        manager.stop_ambient()
        channel.stop.assert_called()

    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_apply_mix_routes_to_expected_categories(
        self,
        _get_init: Mock,
        _init: Mock,
        sound_ctor: Mock,
        channel_ctor: Mock,
        _load_music: Mock,
        music_set_volume: Mock,
    ) -> None:
        channel = Mock()
        sound = Mock()
        channel_ctor.return_value = channel
        sound_ctor.return_value = sound
        manager = AudioManager()

        manager.apply_mix(master=0.5, music=0.4, sfx=0.8, ambient=0.2)
        manager.play_music("menu")
        manager.play_sfx("ui_confirm")
        manager.play_ambient("gameplay")

        self.assertGreaterEqual(music_set_volume.call_count, 2)
        music_set_volume.assert_any_call(0.2)
        sound.set_volume.assert_any_call(0.4)
        channel.set_volume.assert_called_with(0.1)

    @patch("systems.audio.random.uniform", return_value=1.05)
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_sfx_volume_variation_is_applied_within_bounds(
        self,
        _get_init: Mock,
        _init: Mock,
        sound_ctor: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        _channel: Mock,
        _uniform: Mock,
    ) -> None:
        sound = Mock()
        sound_ctor.return_value = sound
        manager = AudioManager()
        manager.apply_mix(master=0.5, music=1.0, sfx=0.8, ambient=1.0)
        manager.play_sfx("ui_nav")
        self.assertGreaterEqual(sound.set_volume.call_count, 1)
        self.assertAlmostEqual(sound.set_volume.call_args_list[-1].args[0], 0.42, places=6)

    @patch("systems.audio.random.choice")
    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_sfx_variants_use_random_choice_when_available(
        self,
        _get_init: Mock,
        _init: Mock,
        sound_ctor: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        _channel: Mock,
        choice: Mock,
    ) -> None:
        sound = Mock()
        sound_ctor.return_value = sound
        choice.side_effect = lambda seq: seq[0]
        manager = AudioManager()
        manager.play_sfx("weapon_fire")
        self.assertTrue(choice.called)

    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_registry_prefers_categorized_paths(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        _load_music: Mock,
        _set_volume: Mock,
        _channel: Mock,
    ) -> None:
        manager = AudioManager()
        self.assertIn("audio\\sfx\\start.wav", str(manager._sfx_registry["start"][0]))
        self.assertIn(
            "audio\\music\\denis-pavlov-music-podcast-lo-fi-music-205515.mp3",
            str(manager._music_registry["menu"][0]),
        )
        self.assertIn("audio\\ambient\\ambient_gameplay.ogg", str(manager._ambient_registry["gameplay"][0]))

    @patch("systems.audio.pygame.mixer.Channel")
    @patch("systems.audio.pygame.mixer.music.set_volume")
    @patch("systems.audio.pygame.mixer.music.load")
    @patch("systems.audio.pygame.mixer.Sound")
    @patch("systems.audio.pygame.mixer.init")
    @patch("systems.audio.pygame.mixer.get_init", return_value=True)
    def test_music_load_falls_back_to_next_candidate_when_primary_missing(
        self,
        _get_init: Mock,
        _init: Mock,
        _sound: Mock,
        load_music: Mock,
        _set_volume: Mock,
        _channel: Mock,
    ) -> None:
        manager = AudioManager()
        calls = manager._music_registry["menu"]
        primary = str(calls[0])
        secondary = str(calls[1])

        def _load_side_effect(path: str) -> None:
            if path == primary:
                raise OSError("missing primary")
            if path == secondary:
                return
            raise OSError("stop after secondary")

        load_music.side_effect = _load_side_effect
        self.assertTrue(manager._load_music_track("menu"))
        self.assertEqual(load_music.call_args_list[0].args[0], primary)
        self.assertEqual(load_music.call_args_list[1].args[0], secondary)
