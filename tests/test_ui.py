"""Validation tests for UI rendering helpers."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.ui import UiRenderer  # noqa: E402


class UiRendererValidationTests(unittest.TestCase):
    def test_weapon_evolution_state_renders_for_base_and_evolved_forms(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        ui = UiRenderer()
        ui.draw_weapon_evolution_state(
            surface,
            weapon_name="Sparkler",
            evolved_form_id=None,
        )
        ui.draw_weapon_evolution_state(
            surface,
            weapon_name="Sparkler",
            evolved_form_id="spark_aura",
        )
        self.assertIsInstance(surface, pygame.Surface)


if __name__ == "__main__":
    unittest.main()
