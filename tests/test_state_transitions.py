"""Validation tests for game state transitions."""

from __future__ import annotations

import pathlib
import sys
import unittest
from unittest.mock import patch


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from main import (  # noqa: E402
    GameState,
    demo_mode_enabled_from_runtime,
    should_end_demo_run_after_boss_defeat,
    transition_state,
)


class StateTransitionValidationTests(unittest.TestCase):
    def test_transition_state_returns_expected_targets(self) -> None:
        self.assertEqual(transition_state(GameState.MENU, GameState.PLAYING), GameState.PLAYING)
        self.assertEqual(transition_state(GameState.PLAYING, GameState.GAME_OVER), GameState.GAME_OVER)
        self.assertEqual(transition_state(GameState.GAME_OVER, GameState.PLAYING), GameState.PLAYING)

    def test_demo_mode_resolver_enables_from_cli_flag(self) -> None:
        with patch("main.is_demo_mode_enabled", return_value=False):
            self.assertTrue(
                demo_mode_enabled_from_runtime(
                    argv=("--demo-mode",),
                    env={},
                )
            )

    def test_demo_mode_resolver_enables_from_env_var(self) -> None:
        with patch("main.is_demo_mode_enabled", return_value=False):
            self.assertTrue(
                demo_mode_enabled_from_runtime(
                    argv=(),
                    env={"CONFETTI_CHAOS_DEMO_MODE": "1"},
                )
            )
            self.assertTrue(
                demo_mode_enabled_from_runtime(
                    argv=(),
                    env={"CONFETTI_CHAOS_DEMO_MODE": "true"},
                )
            )

    def test_demo_mode_resolver_falls_back_to_packaged_marker(self) -> None:
        with patch("main.is_demo_mode_enabled", return_value=True):
            self.assertTrue(
                demo_mode_enabled_from_runtime(
                    argv=(),
                    env={},
                )
            )
        with patch("main.is_demo_mode_enabled", return_value=False):
            self.assertFalse(
                demo_mode_enabled_from_runtime(
                    argv=(),
                    env={},
                )
            )

    def test_demo_mode_completion_condition_requires_boss_defeat_at_target_level(self) -> None:
        self.assertFalse(
            should_end_demo_run_after_boss_defeat(
                demo_mode_enabled=False,
                current_level=10,
                boss_defeat_triggered=True,
            )
        )
        self.assertFalse(
            should_end_demo_run_after_boss_defeat(
                demo_mode_enabled=True,
                current_level=9,
                boss_defeat_triggered=True,
            )
        )
        self.assertFalse(
            should_end_demo_run_after_boss_defeat(
                demo_mode_enabled=True,
                current_level=10,
                boss_defeat_triggered=False,
            )
        )
        self.assertTrue(
            should_end_demo_run_after_boss_defeat(
                demo_mode_enabled=True,
                current_level=10,
                boss_defeat_triggered=True,
            )
        )
