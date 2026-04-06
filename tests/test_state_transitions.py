"""Validation tests for game state transitions."""

from __future__ import annotations

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from main import GameState, transition_state  # noqa: E402


class StateTransitionValidationTests(unittest.TestCase):
    def test_transition_state_returns_expected_targets(self) -> None:
        self.assertEqual(transition_state(GameState.MENU, GameState.PLAYING), GameState.PLAYING)
        self.assertEqual(transition_state(GameState.PLAYING, GameState.GAME_OVER), GameState.GAME_OVER)
        self.assertEqual(transition_state(GameState.GAME_OVER, GameState.PLAYING), GameState.PLAYING)
