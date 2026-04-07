"""Minimal UI renderer for score and game state text."""

from __future__ import annotations

import pygame


class UiRenderer:
    def __init__(self) -> None:
        self._score_font = pygame.font.Font(None, 42)
        self._title_font = pygame.font.Font(None, 92)
        self._prompt_font = pygame.font.Font(None, 44)
        self._state_font = pygame.font.Font(None, 48)
        self._score_color = (245, 235, 120)
        self._title_color = (255, 255, 255)
        self._prompt_color = (205, 220, 240)
        self._state_color = (235, 235, 235)

    def draw_score(self, surface: pygame.Surface, score_value: int) -> None:
        score_surface = self._score_font.render(f"Score: {score_value}", True, self._score_color)
        surface.blit(score_surface, (20, 20))

    def draw_level(self, surface: pygame.Surface, level: int) -> None:
        level_surface = self._score_font.render(f"Level: {level}", True, self._score_color)
        level_rect = level_surface.get_rect(topright=(surface.get_width() - 20, 20))
        surface.blit(level_surface, level_rect)

    def draw_boss_victory(self, surface: pygame.Surface, bonus: int) -> None:
        title_surface = self._title_font.render("BOSS DEFEATED!", True, (255, 215, 120))
        title_rect = title_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 40))
        surface.blit(title_surface, title_rect)

        bonus_surface = self._state_font.render(f"+{bonus} Bonus", True, self._score_color)
        bonus_rect = bonus_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 30))
        surface.blit(bonus_surface, bonus_rect)

    def draw_state_text(self, surface: pygame.Surface, text: str, alpha: float = 1.0) -> None:
        text_surface = self._state_font.render(text, True, self._state_color)
        
        # Apply alpha blending if alpha < 1.0
        if alpha < 1.0:
            text_surface.set_alpha(max(0, int(255 * alpha)))
        
        text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text_surface, text_rect)

    def draw_menu(self, surface: pygame.Surface, title: str, high_score: int) -> None:
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        title_surface = self._title_font.render(title, True, self._title_color)
        title_rect = title_surface.get_rect(center=(center_x, center_y - 120))
        surface.blit(title_surface, title_rect)

        start_surface = self._prompt_font.render(
            "Press Enter/Space or Gamepad A/Start",
            True,
            self._prompt_color,
        )
        start_rect = start_surface.get_rect(center=(center_x, center_y - 20))
        surface.blit(start_surface, start_rect)

        quit_surface = self._prompt_font.render(
            "Press Q/Esc or Gamepad Back to Quit",
            True,
            self._prompt_color,
        )
        quit_rect = quit_surface.get_rect(center=(center_x, center_y + 30))
        surface.blit(quit_surface, quit_rect)

        high_score_surface = self._prompt_font.render(
            f"High Score: {high_score}",
            True,
            self._prompt_color,
        )
        high_score_rect = high_score_surface.get_rect(center=(center_x, center_y + 90))
        surface.blit(high_score_surface, high_score_rect)

    def draw_paused(self, surface: pygame.Surface, audio_enabled: bool) -> None:
        pause_surface = self._state_font.render("PAUSED", True, self._state_color)
        pause_rect = pause_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 20))
        surface.blit(pause_surface, pause_rect)

        prompt = "Press P/Esc or Gamepad Start/Back to Resume"
        prompt_surface = self._prompt_font.render(prompt, True, self._prompt_color)
        prompt_rect = prompt_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 20))
        surface.blit(prompt_surface, prompt_rect)

        audio_label = f"Audio: {'On' if audio_enabled else 'Off'} (Press M to Toggle)"
        audio_surface = self._prompt_font.render(audio_label, True, self._prompt_color)
        audio_rect = audio_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 60))
        surface.blit(audio_surface, audio_rect)
