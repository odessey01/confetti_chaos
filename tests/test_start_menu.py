"""Validation tests for start menu navigation and actions."""

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
    StartMenuAction,
    execute_start_menu_action,
    next_start_level,
    next_start_menu_index,
    start_menu_action_for_index,
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
        self.start_calls = 0

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled

    def play_start_or_restart(self) -> None:
        self.start_calls += 1


class _FakeVisualFeedback:
    def __init__(self) -> None:
        self.transitions = 0

    def trigger_state_transition(self) -> None:
        self.transitions += 1


class StartMenuValidationTests(unittest.TestCase):
    def test_start_menu_index_wraps(self) -> None:
        self.assertEqual(next_start_menu_index(0, -1), 3)
        self.assertEqual(next_start_menu_index(3, 1), 0)

    def test_start_menu_action_mapping(self) -> None:
        self.assertEqual(start_menu_action_for_index(0), StartMenuAction.START_GAME)
        self.assertEqual(start_menu_action_for_index(1), StartMenuAction.LEVEL_SELECT)
        self.assertEqual(start_menu_action_for_index(2), StartMenuAction.TOGGLE_MUSIC)
        self.assertEqual(start_menu_action_for_index(3), StartMenuAction.QUIT)

    def test_level_select_cycles(self) -> None:
        self.assertEqual(next_start_level(1), 2)
        self.assertEqual(next_start_level(10), 1)

    def test_execute_start_menu_actions(self) -> None:
        session = _FakeSession()
        audio = _FakeAudio()
        visual = _FakeVisualFeedback()
        settings = RuntimeSettings(music_enabled=True, selected_start_level=4)
        saved = {"count": 0}

        def _save_hook(_settings: RuntimeSettings) -> None:
            saved["count"] += 1

        state, running = execute_start_menu_action(
            StartMenuAction.START_GAME,
            state=GameState.MENU,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual,
            save_hook=_save_hook,
        )
        self.assertEqual(state, GameState.PLAYING)
        self.assertTrue(running)
        self.assertEqual(session.restart_calls, 1)
        self.assertEqual(audio.start_calls, 1)
        self.assertEqual(session.last_start_level, 4)

        state, running = execute_start_menu_action(
            StartMenuAction.LEVEL_SELECT,
            state=GameState.MENU,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual,
            save_hook=_save_hook,
        )
        self.assertEqual(state, GameState.MENU)
        self.assertTrue(running)
        self.assertEqual(settings.selected_start_level, 5)

        state, running = execute_start_menu_action(
            StartMenuAction.TOGGLE_MUSIC,
            state=GameState.MENU,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual,
            save_hook=_save_hook,
        )
        self.assertEqual(state, GameState.MENU)
        self.assertTrue(running)
        self.assertFalse(settings.music_enabled)
        self.assertFalse(audio.enabled)

        state, running = execute_start_menu_action(
            StartMenuAction.QUIT,
            state=GameState.MENU,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual,
            save_hook=_save_hook,
        )
        self.assertEqual(state, GameState.MENU)
        self.assertFalse(running)
        self.assertEqual(saved["count"], 2)
