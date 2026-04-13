"""Validation tests for start menu navigation and actions."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from main import (  # noqa: E402
    GameState,
    StartMenuAction,
    draw_player_weapon_preview,
    execute_start_menu_action,
    next_start_level,
    next_start_menu_index,
    start_menu_action_for_index,
    ui_sfx_for_start_action,
)
from systems import GameSession  # noqa: E402
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
        self.assertEqual(next_start_menu_index(0, -1), 4)
        self.assertEqual(next_start_menu_index(4, 1), 0)

    def test_start_menu_action_mapping(self) -> None:
        self.assertEqual(start_menu_action_for_index(0), StartMenuAction.START_GAME)
        self.assertEqual(start_menu_action_for_index(1), StartMenuAction.LEVEL_SELECT)
        self.assertEqual(start_menu_action_for_index(2), StartMenuAction.TOGGLE_SOUND)
        self.assertEqual(start_menu_action_for_index(3), StartMenuAction.TOGGLE_AIM_ASSIST)
        self.assertEqual(start_menu_action_for_index(4), StartMenuAction.QUIT)
        self.assertEqual(ui_sfx_for_start_action(StartMenuAction.START_GAME), "ui_confirm")
        self.assertEqual(ui_sfx_for_start_action(StartMenuAction.LEVEL_SELECT), "ui_toggle_settings")
        self.assertEqual(ui_sfx_for_start_action(StartMenuAction.TOGGLE_SOUND), "ui_toggle_settings")
        self.assertEqual(ui_sfx_for_start_action(StartMenuAction.TOGGLE_AIM_ASSIST), "ui_toggle_settings")
        self.assertEqual(ui_sfx_for_start_action(StartMenuAction.QUIT), "ui_back")

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
        self.assertEqual(state, GameState.PLAYER_SELECT)
        self.assertTrue(running)
        self.assertEqual(session.restart_calls, 0)
        self.assertEqual(audio.start_calls, 0)
        self.assertIsNone(session.last_start_level)

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
            StartMenuAction.TOGGLE_SOUND,
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
            StartMenuAction.TOGGLE_AIM_ASSIST,
            state=GameState.MENU,
            session=session,
            runtime_settings=settings,
            audio=audio,
            visual_feedback=visual,
            save_hook=_save_hook,
        )
        self.assertEqual(state, GameState.MENU)
        self.assertTrue(running)
        self.assertFalse(settings.aim_assist_enabled)

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
        self.assertEqual(saved["count"], 3)

    def test_player_weapon_preview_draws_selected_weapon_overlay(self) -> None:
        if not pygame.get_init():
            pygame.init()
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)

        draw_player_weapon_preview(
            surface,
            session,
            variant_id="teddy_f",
            weapon_id="bottle_rocket",
            preview_size=120,
            preview_x=560.0,
            preview_y=150.0,
            delta_seconds=1.0 / 60.0,
        )

        self.assertEqual(session.active_weapon_id, "bottle_rocket")
        self.assertGreaterEqual(len(session.active_weapon_visual_overlays()), 1)
