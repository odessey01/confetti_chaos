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
        self._body_font = pygame.font.Font(None, 34)

    def draw_score(self, surface: pygame.Surface, score_value: int) -> None:
        score_surface = self._score_font.render(f"Score: {score_value}", True, self._score_color)
        surface.blit(score_surface, (20, 20))

    def draw_level(self, surface: pygame.Surface, level: int) -> None:
        level_surface = self._score_font.render(f"Level: {level}", True, self._score_color)
        level_rect = level_surface.get_rect(topright=(surface.get_width() - 20, 20))
        surface.blit(level_surface, level_rect)

    def draw_run_progress(
        self,
        surface: pygame.Surface,
        *,
        run_level: int,
        current_xp: int,
        xp_to_next: int,
    ) -> None:
        label = self._score_font.render(f"Run Lv {run_level}", True, self._score_color)
        surface.blit(label, (20, 62))
        bar_x = 20
        bar_y = 100
        bar_w = 260
        bar_h = 16
        pygame.draw.rect(surface, (35, 45, 58), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
        if xp_to_next > 0:
            ratio = max(0.0, min(current_xp / xp_to_next, 1.0))
        else:
            ratio = 0.0
        fill_w = int(bar_w * ratio)
        pygame.draw.rect(surface, (120, 230, 245), (bar_x, bar_y, fill_w, bar_h), border_radius=5)
        pygame.draw.rect(surface, (220, 240, 248), (bar_x, bar_y, bar_w, bar_h), width=1, border_radius=5)
        detail = self._body_font.render(f"XP {current_xp}/{xp_to_next}", True, self._prompt_color)
        surface.blit(detail, (bar_x, bar_y + 20))

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

    def draw_menu(
        self,
        surface: pygame.Surface,
        title: str,
        high_score: int,
        options: tuple[str, ...],
        selected_index: int,
        music_enabled: bool,
        selected_start_level: int,
    ) -> None:
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        title_surface = self._title_font.render(title, True, self._title_color)
        title_rect = title_surface.get_rect(center=(center_x, center_y - 120))
        surface.blit(title_surface, title_rect)

        for idx, option in enumerate(options):
            label = option
            if option == "Toggle Sound":
                label = f"Toggle Sound: {'On' if music_enabled else 'Off'}"
            elif option == "Level Select":
                label = f"Level Select: {selected_start_level}"
            color = (255, 235, 140) if idx == selected_index else self._prompt_color
            option_surface = self._prompt_font.render(label, True, color)
            option_rect = option_surface.get_rect(center=(center_x, center_y - 25 + (idx * 40)))
            surface.blit(option_surface, option_rect)

        high_score_surface = self._prompt_font.render(
            f"High Score: {high_score}",
            True,
            self._prompt_color,
        )
        high_score_rect = high_score_surface.get_rect(center=(center_x, center_y + 150))
        surface.blit(high_score_surface, high_score_rect)

        prompt_surface = self._prompt_font.render(
            "Up/Down to Navigate | Enter/A to Confirm",
            True,
            self._prompt_color,
        )
        prompt_rect = prompt_surface.get_rect(center=(center_x, center_y + 195))
        surface.blit(prompt_surface, prompt_rect)

    def draw_paused(
        self,
        surface: pygame.Surface,
        audio_enabled: bool,
        options: tuple[str, ...],
        selected_index: int,
    ) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        surface.blit(overlay, (0, 0))

        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2
        pause_surface = self._state_font.render("PAUSED", True, self._state_color)
        pause_rect = pause_surface.get_rect(center=(center_x, center_y - 120))
        surface.blit(pause_surface, pause_rect)

        for idx, option in enumerate(options):
            label = option
            if option == "Toggle Sound":
                label = f"Toggle Sound: {'On' if audio_enabled else 'Off'}"
            color = (255, 235, 140) if idx == selected_index else self._prompt_color
            option_surface = self._prompt_font.render(label, True, color)
            option_rect = option_surface.get_rect(center=(center_x, center_y - 30 + (idx * 40)))
            surface.blit(option_surface, option_rect)

        prompt = "Up/Down to Navigate | Enter/A to Confirm | P/Esc to Resume"
        prompt_surface = self._prompt_font.render(prompt, True, self._prompt_color)
        prompt_rect = prompt_surface.get_rect(center=(center_x, center_y + 150))
        surface.blit(prompt_surface, prompt_rect)

    def draw_level_up_overlay(
        self,
        surface: pygame.Surface,
        *,
        run_level: int,
        options: list[object],
        selected_index: int,
    ) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((3, 8, 14, 165))
        surface.blit(overlay, (0, 0))

        center_x = surface.get_width() // 2
        title = self._title_font.render(f"LEVEL UP! ({run_level})", True, (255, 235, 150))
        title_rect = title.get_rect(center=(center_x, 110))
        surface.blit(title, title_rect)

        subtitle = self._prompt_font.render("Choose 1 Upgrade", True, self._prompt_color)
        surface.blit(subtitle, subtitle.get_rect(center=(center_x, 160)))

        card_w = min(360, (surface.get_width() - 120) // max(1, len(options)))
        card_h = 250
        total_w = (card_w * len(options)) + (20 * max(0, len(options) - 1))
        start_x = (surface.get_width() - total_w) // 2
        y = 220
        for idx, option in enumerate(options):
            x = start_x + (idx * (card_w + 20))
            selected = idx == selected_index
            card_color = (52, 74, 96, 230) if selected else (33, 52, 70, 210)
            border_color = (255, 228, 138) if selected else (160, 190, 214)
            card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            card.fill(card_color)
            surface.blit(card, (x, y))
            pygame.draw.rect(surface, border_color, (x, y, card_w, card_h), width=2, border_radius=8)

            name = getattr(option, "name", str(option))
            desc = getattr(option, "description", "")
            effects = getattr(option, "effect_values", {})
            effect_summary = ", ".join(f"{k}: +{v:g}" for k, v in effects.items()) if effects else ""
            name_surface = self._prompt_font.render(name, True, (245, 248, 250))
            surface.blit(name_surface, (x + 14, y + 16))
            desc_surface = self._body_font.render(desc, True, (216, 229, 242))
            surface.blit(desc_surface, (x + 14, y + 70))
            summary_surface = self._body_font.render(effect_summary, True, (255, 227, 145))
            surface.blit(summary_surface, (x + 14, y + 120))

        hint = self._body_font.render("Up/Down (or Left/Right) to select, Enter/A to confirm", True, self._prompt_color)
        surface.blit(hint, hint.get_rect(center=(center_x, y + card_h + 40)))
