"""Validation tests for pause menu behavior and actions."""

from __future__ import annotations

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from main import (  # noqa: E402
    GameState,
    PauseMenuAction,
    execute_pause_menu_action,
    next_pause_menu_index,
    pause_menu_action_for_index,
    should_update_playing,
    ui_sfx_for_pause_action,
)
from systems.settings import RuntimeSettings  # noqa: E402


class _FakeSession:
    def __init__(self) -> None:
        self.restart_calls = 0
        self.last_start_level: int | None = None

    def start_new_run(self, start_level: int = 1) -> None:
        self.restart_calls += 1
        self.last_start_level = start_level


class _FakeAudio:
    def __init__(self) -> None:
        self.enabled = True
        self.restart_sound_calls = 0

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled

    def play_start_or_restart(self) -> None:
        self.restart_sound_calls += 1


class _FakeVisualFeedback:
    def __init__(self) -> None:
        self.transition_calls = 0

    def trigger_state_transition(self) -> None:
        self.transition_calls += 1


class PauseMenuValidationTests(unittest.TestCase):
    def test_pause_menu_index_wraps(self) -> None:
        self.assertEqual(next_pause_menu_index(0, -1), 3)
        self.assertEqual(next_pause_menu_index(3, 1), 0)

    def test_pause_menu_action_mapping(self) -> None:
        self.assertEqual(pause_menu_action_for_index(0), PauseMenuAction.RESUME)
        self.assertEqual(pause_menu_action_for_index(1), PauseMenuAction.RESTART)
        self.assertEqual(pause_menu_action_for_index(2), PauseMenuAction.TOGGLE_SOUND)
        self.assertEqual(pause_menu_action_for_index(3), PauseMenuAction.QUIT_TO_MENU)
        self.assertEqual(ui_sfx_for_pause_action(PauseMenuAction.RESUME), "ui_resume")
        self.assertEqual(ui_sfx_for_pause_action(PauseMenuAction.RESTART), "ui_confirm")
        self.assertEqual(ui_sfx_for_pause_action(PauseMenuAction.TOGGLE_SOUND), "ui_toggle_settings")
        self.assertEqual(ui_sfx_for_pause_action(PauseMenuAction.QUIT_TO_MENU), "ui_back")

    def test_should_update_playing_freeze_gate(self) -> None:
        self.assertTrue(should_update_playing(GameState.PLAYING))
        self.assertFalse(should_update_playing(GameState.PAUSED))
        self.assertFalse(should_update_playing(GameState.LEVEL_UP))

    def test_execute_pause_actions(self) -> None:
        session = _FakeSession()
        audio = _FakeAudio()
        visual_feedback = _FakeVisualFeedback()
        settings = RuntimeSettings(music_enabled=True, selected_start_level=3)
        saved = {"count": 0}

        def _save_hook(_settings: RuntimeSettings) -> None:
            saved["count"] += 1

        resumed = execute_pause_menu_action(
            PauseMenuAction.RESUME,
            state=GameState.PAUSED,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual_feedback,
            save_hook=_save_hook,
        )
        self.assertEqual(resumed, GameState.PLAYING)

        restarted = execute_pause_menu_action(
            PauseMenuAction.RESTART,
            state=GameState.PAUSED,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual_feedback,
            save_hook=_save_hook,
        )
        self.assertEqual(restarted, GameState.PLAYING)
        self.assertEqual(session.restart_calls, 1)
        self.assertEqual(session.last_start_level, 3)
        self.assertEqual(audio.restart_sound_calls, 1)

        toggled = execute_pause_menu_action(
            PauseMenuAction.TOGGLE_SOUND,
            state=GameState.PAUSED,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual_feedback,
            save_hook=_save_hook,
        )
        self.assertEqual(toggled, GameState.PAUSED)
        self.assertFalse(settings.music_enabled)
        self.assertFalse(audio.enabled)
        self.assertEqual(saved["count"], 1)

        menu_state = execute_pause_menu_action(
            PauseMenuAction.QUIT_TO_MENU,
            state=GameState.PAUSED,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual_feedback,
            save_hook=_save_hook,
        )
        self.assertEqual(menu_state, GameState.MENU)
        self.assertGreaterEqual(visual_feedback.transition_calls, 3)
