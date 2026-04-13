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

    def test_start_menu_layout_avoids_text_overlap(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        ui = UiRenderer()
        layout = ui.menu_layout_rects(
            surface,
            title="Confetti Chaos",
            high_score=999999,
            options=("Start Game", "Level Select", "Toggle Sound", "Toggle Aim Assist", "Quit"),
            music_enabled=True,
            aim_assist_enabled=True,
            selected_start_level=99,
        )
        option_rects = list(layout["options"])
        previous = layout["title"]
        for rect in option_rects:
            self.assertLessEqual(previous.bottom, rect.top)
            previous = rect
        self.assertLessEqual(option_rects[-1].bottom, layout["high_score"].top)
        self.assertLessEqual(layout["high_score"].bottom, layout["prompt"].top)

    def test_start_menu_layout_with_weapon_label_avoids_text_overlap(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        ui = UiRenderer()
        layout = ui.menu_layout_rects(
            surface,
            title="Confetti Chaos",
            high_score=999999,
            options=("Start Game", "Level Select", "Toggle Sound", "Toggle Aim Assist", "Quit"),
            music_enabled=True,
            aim_assist_enabled=True,
            selected_start_level=99,
            selected_weapon_name="Bottle Rocket",
        )
        option_rects = list(layout["options"])
        weapon_rect = layout["weapon"]
        self.assertLessEqual(option_rects[-1].bottom, weapon_rect.top)
        self.assertLessEqual(weapon_rect.bottom, layout["high_score"].top)
        self.assertLessEqual(layout["high_score"].bottom, layout["prompt"].top)

    def test_draw_menu_renders_selected_weapon_without_errors(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        ui = UiRenderer()
        ui.draw_menu(
            surface,
            title="Confetti Chaos",
            high_score=42,
            options=("Start Game", "Level Select", "Toggle Sound", "Toggle Aim Assist", "Quit"),
            selected_index=0,
            music_enabled=True,
            aim_assist_enabled=True,
            selected_start_level=1,
            selected_weapon_name="Sparkler",
        )
        self.assertIsInstance(surface, pygame.Surface)

    def test_pause_menu_layout_avoids_text_overlap(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        ui = UiRenderer()
        layout = ui.paused_layout_rects(
            surface,
            audio_enabled=True,
            aim_assist_enabled=True,
            options=("Resume", "Restart", "Toggle Sound", "Toggle Aim Assist", "Quit to Menu"),
        )
        option_rects = list(layout["options"])
        previous = layout["title"]
        for rect in option_rects:
            self.assertLessEqual(previous.bottom, rect.top)
            previous = rect
        self.assertLessEqual(option_rects[-1].bottom, layout["prompt"].top)


if __name__ == "__main__":
    unittest.main()
