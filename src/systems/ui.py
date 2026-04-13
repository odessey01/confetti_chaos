"""Minimal UI renderer for score and game state text."""

from __future__ import annotations

import pygame

from .paths import asset_path


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
        self._health_icon_cache: dict[str, pygame.Surface | None] = {}

    @staticmethod
    def _stack_centered_rects(
        surfaces: list[pygame.Surface],
        *,
        center_x: int,
        start_y: int,
        spacing: int,
    ) -> list[pygame.Rect]:
        rects: list[pygame.Rect] = []
        current_y = int(start_y)
        for item in surfaces:
            rect = item.get_rect(center=(center_x, current_y + (item.get_height() // 2)))
            rects.append(rect)
            current_y = rect.bottom + int(spacing)
        return rects

    def draw_score(self, surface: pygame.Surface, score_value: int) -> None:
        score_surface = self._score_font.render(f"Score: {score_value}", True, self._score_color)
        surface.blit(score_surface, (20, 20))

    def draw_level(self, surface: pygame.Surface, level: int) -> None:
        level_surface = self._score_font.render(f"Level: {level}", True, self._score_color)
        level_rect = level_surface.get_rect(topright=(surface.get_width() - 20, 20))
        surface.blit(level_surface, level_rect)

    def draw_health(self, surface: pygame.Surface, *, current_health: int, max_health: int) -> None:
        icon_size = 26
        spacing = 10
        start_x = surface.get_width() - 24 - ((icon_size + spacing) * max_health)
        y = 66
        for index in range(max_health):
            is_full = index < current_health
            self._draw_lollipop_icon(
                surface,
                x=start_x + (index * (icon_size + spacing)),
                y=y,
                size=icon_size,
                full=is_full,
            )

    def _draw_lollipop_icon(self, surface: pygame.Surface, *, x: int, y: int, size: int, full: bool) -> None:
        icon = self._health_icon(full, size)
        if icon is not None:
            surface.blit(icon, (x, y))
            return
        candy_color = (255, 122, 176) if full else (88, 98, 112)
        stick_color = (244, 236, 214) if full else (130, 136, 144)
        center = (x + size // 2, y + size // 2 - 2)
        radius = max(6, size // 3)
        pygame.draw.circle(surface, candy_color, center, radius)
        pygame.draw.circle(surface, (244, 244, 248), center, radius, width=2)
        pygame.draw.rect(surface, stick_color, (center[0] - 2, center[1] + radius - 1, 4, max(8, size // 2)), border_radius=2)

    def _health_icon(self, full: bool, size: int) -> pygame.Surface | None:
        key = f"{'full' if full else 'empty'}:{size}"
        if key in self._health_icon_cache:
            return self._health_icon_cache[key]
        filename = "lollipop_full.png" if full else "lollipop_empty.png"
        path = asset_path("images", "ui", filename)
        try:
            image = pygame.image.load(str(path))
            scaled = pygame.transform.smoothscale(image, (size, size))
            self._health_icon_cache[key] = scaled
            return scaled
        except (pygame.error, FileNotFoundError, OSError):
            self._health_icon_cache[key] = None
            return None

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

    def draw_super_meter(
        self,
        surface: pygame.Surface,
        *,
        charge: int,
        max_charge: int,
        ready: bool,
    ) -> None:
        label_text = "Super READY" if ready else "Super"
        label_color = (255, 236, 142) if ready else self._score_color
        label = self._score_font.render(label_text, True, label_color)
        surface.blit(label, (20, 130))

        bar_x = 20
        bar_y = 168
        bar_w = 260
        bar_h = 14
        pygame.draw.rect(surface, (35, 45, 58), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
        if max_charge > 0:
            ratio = max(0.0, min(charge / max_charge, 1.0))
        else:
            ratio = 0.0
        fill_w = int(bar_w * ratio)
        fill_color = (255, 215, 105) if ready else (165, 205, 255)
        pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill_w, bar_h), border_radius=5)
        pygame.draw.rect(surface, (220, 240, 248), (bar_x, bar_y, bar_w, bar_h), width=1, border_radius=5)
        detail = self._body_font.render(f"{charge}/{max_charge}", True, self._prompt_color)
        surface.blit(detail, (bar_x, bar_y + 18))

    def draw_weapon_evolution_state(
        self,
        surface: pygame.Surface,
        *,
        weapon_name: str,
        evolved_form_id: str | None,
    ) -> None:
        weapon_label = self._body_font.render(f"Weapon: {weapon_name}", True, (236, 242, 252))
        weapon_rect = weapon_label.get_rect(topright=(surface.get_width() - 20, 22))
        surface.blit(weapon_label, weapon_rect)
        if not evolved_form_id:
            form_label = self._body_font.render("Form: Base", True, (170, 186, 206))
        else:
            pretty_form = str(evolved_form_id).replace("_", " ").title()
            form_label = self._body_font.render(f"Form: {pretty_form}", True, (255, 226, 138))
        form_rect = form_label.get_rect(topright=(surface.get_width() - 20, 50))
        surface.blit(form_label, form_rect)

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

    def draw_unlock_notification(self, surface: pygame.Surface, text: str, *, alpha: float = 1.0) -> None:
        banner = pygame.Surface((min(760, surface.get_width() - 80), 62), pygame.SRCALPHA)
        banner.fill((24, 44, 36, int(180 * max(0.0, min(alpha, 1.0)))))
        banner_rect = banner.get_rect(center=(surface.get_width() // 2, 48))
        surface.blit(banner, banner_rect)
        label = self._body_font.render(text, True, (214, 255, 210))
        label.set_alpha(max(0, min(255, int(255 * alpha))))
        label_rect = label.get_rect(center=banner_rect.center)
        surface.blit(label, label_rect)

    def menu_layout_rects(
        self,
        surface: pygame.Surface,
        *,
        title: str,
        high_score: int,
        options: tuple[str, ...],
        music_enabled: bool,
        aim_assist_enabled: bool,
        selected_start_level: int,
        selected_weapon_name: str | None = None,
    ) -> dict[str, pygame.Rect | list[pygame.Rect]]:
        center_x = surface.get_width() // 2
        title_surface = self._title_font.render(title, True, self._title_color)
        option_surfaces: list[pygame.Surface] = []
        for option in options:
            label = option
            if option == "Toggle Sound":
                label = f"Toggle Sound: {'On' if music_enabled else 'Off'}"
            elif option == "Toggle Aim Assist":
                label = f"Toggle Aim Assist: {'On' if aim_assist_enabled else 'Off'}"
            elif option == "Level Select":
                label = f"Level Select: {selected_start_level}"
            option_surfaces.append(self._prompt_font.render(label, True, self._prompt_color))

        high_score_surface = self._prompt_font.render(
            f"High Score: {high_score}",
            True,
            self._prompt_color,
        )
        prompt_surface = self._prompt_font.render(
            "Up/Down to Navigate | Enter/A to Confirm",
            True,
            self._prompt_color,
        )
        title_rect = title_surface.get_rect(midtop=(center_x, 48))
        prompt_rect = prompt_surface.get_rect(midbottom=(center_x, surface.get_height() - 28))
        high_score_rect = high_score_surface.get_rect(midbottom=(center_x, prompt_rect.top - 18))
        weapon_surface = (
            self._body_font.render(f"Weapon: {selected_weapon_name}", True, (255, 228, 150))
            if selected_weapon_name
            else None
        )
        weapon_rect: pygame.Rect | None = None
        if weapon_surface is not None:
            weapon_rect = weapon_surface.get_rect(midbottom=(center_x, high_score_rect.top - 12))

        available_top = title_rect.bottom + 34
        available_bottom = (weapon_rect.top - 16) if weapon_rect is not None else (high_score_rect.top - 26)
        option_spacing = 14
        option_total_height = sum(item.get_height() for item in option_surfaces)
        if len(option_surfaces) > 1:
            option_total_height += option_spacing * (len(option_surfaces) - 1)
        options_start_y = available_top
        if available_bottom > available_top and option_total_height < (available_bottom - available_top):
            options_start_y = available_top + ((available_bottom - available_top - option_total_height) // 2)
        option_rects = self._stack_centered_rects(
            option_surfaces,
            center_x=center_x,
            start_y=options_start_y,
            spacing=option_spacing,
        )
        result: dict[str, pygame.Rect | list[pygame.Rect]] = {
            "title": title_rect,
            "options": option_rects,
            "high_score": high_score_rect,
            "prompt": prompt_rect,
        }
        if weapon_rect is not None:
            result["weapon"] = weapon_rect
        return result

    def paused_layout_rects(
        self,
        surface: pygame.Surface,
        *,
        audio_enabled: bool,
        aim_assist_enabled: bool,
        options: tuple[str, ...],
    ) -> dict[str, pygame.Rect | list[pygame.Rect]]:
        center_x = surface.get_width() // 2
        pause_surface = self._state_font.render("PAUSED", True, self._state_color)
        option_surfaces: list[pygame.Surface] = []
        for option in options:
            label = option
            if option == "Toggle Sound":
                label = f"Toggle Sound: {'On' if audio_enabled else 'Off'}"
            elif option == "Toggle Aim Assist":
                label = f"Toggle Aim Assist: {'On' if aim_assist_enabled else 'Off'}"
            option_surfaces.append(self._prompt_font.render(label, True, self._prompt_color))
        prompt_surface = self._prompt_font.render(
            "Up/Down to Navigate | Enter/A to Confirm | P/Esc to Resume",
            True,
            self._prompt_color,
        )
        pause_rect = pause_surface.get_rect(midtop=(center_x, 120))
        prompt_rect = prompt_surface.get_rect(midbottom=(center_x, surface.get_height() - 34))
        available_top = pause_rect.bottom + 28
        available_bottom = prompt_rect.top - 26
        option_spacing = 14
        option_total_height = sum(item.get_height() for item in option_surfaces)
        if len(option_surfaces) > 1:
            option_total_height += option_spacing * (len(option_surfaces) - 1)
        options_start_y = available_top
        if available_bottom > available_top and option_total_height < (available_bottom - available_top):
            options_start_y = available_top + ((available_bottom - available_top - option_total_height) // 2)
        option_rects = self._stack_centered_rects(
            option_surfaces,
            center_x=center_x,
            start_y=options_start_y,
            spacing=option_spacing,
        )
        return {
            "title": pause_rect,
            "options": option_rects,
            "prompt": prompt_rect,
        }

    def draw_menu(
        self,
        surface: pygame.Surface,
        title: str,
        high_score: int,
        options: tuple[str, ...],
        selected_index: int,
        music_enabled: bool,
        aim_assist_enabled: bool,
        selected_start_level: int,
        selected_weapon_name: str | None = None,
    ) -> None:
        title_surface = self._title_font.render(title, True, self._title_color)
        option_surfaces: list[pygame.Surface] = []
        for idx, option in enumerate(options):
            label = option
            if option == "Toggle Sound":
                label = f"Toggle Sound: {'On' if music_enabled else 'Off'}"
            elif option == "Toggle Aim Assist":
                label = f"Toggle Aim Assist: {'On' if aim_assist_enabled else 'Off'}"
            elif option == "Level Select":
                label = f"Level Select: {selected_start_level}"
            color = (255, 235, 140) if idx == selected_index else self._prompt_color
            option_surfaces.append(self._prompt_font.render(label, True, color))

        high_score_surface = self._prompt_font.render(
            f"High Score: {high_score}",
            True,
            self._prompt_color,
        )
        prompt_surface = self._prompt_font.render(
            "Up/Down to Navigate | Enter/A to Confirm",
            True,
            self._prompt_color,
        )
        weapon_surface = (
            self._body_font.render(f"Weapon: {selected_weapon_name}", True, (255, 228, 150))
            if selected_weapon_name
            else None
        )

        layout = self.menu_layout_rects(
            surface,
            title=title,
            high_score=high_score,
            options=options,
            music_enabled=music_enabled,
            aim_assist_enabled=aim_assist_enabled,
            selected_start_level=selected_start_level,
            selected_weapon_name=selected_weapon_name,
        )
        title_rect = layout["title"]
        high_score_rect = layout["high_score"]
        prompt_rect = layout["prompt"]
        option_rects = layout["options"]

        surface.blit(title_surface, title_rect)
        for option_surface, option_rect in zip(option_surfaces, option_rects):
            surface.blit(option_surface, option_rect)
        if weapon_surface is not None and "weapon" in layout:
            surface.blit(weapon_surface, layout["weapon"])
        surface.blit(high_score_surface, high_score_rect)
        surface.blit(prompt_surface, prompt_rect)

    def draw_player_select(
        self,
        surface: pygame.Surface,
        *,
        selected_index: int,
        options: tuple[str, ...],
        option_enabled: tuple[bool, ...] | None = None,
        selected_name: str,
        selected_note: str,
        passive_bonus: str,
        passive_drawback: str,
        passive_summary: str | None = None,
        selected_weapon_name: str | None = None,
        selected_locked: bool = False,
        selected_unlock_hint: str = "",
    ) -> None:
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        title_surface = self._title_font.render("Choose Your Party Animal", True, self._title_color)
        title_rect = title_surface.get_rect(center=(center_x, 90))
        surface.blit(title_surface, title_rect)

        enabled_flags = (
            option_enabled
            if option_enabled is not None and len(option_enabled) == len(options)
            else tuple(True for _ in options)
        )
        for idx, name in enumerate(options):
            enabled = bool(enabled_flags[idx])
            label = name if enabled else f"{name} (Locked)"
            if not enabled:
                color = (126, 134, 146)
            elif idx == selected_index:
                color = (255, 235, 140)
            else:
                color = self._prompt_color
            item = self._prompt_font.render(label, True, color)
            item_rect = item.get_rect(center=(center_x, center_y + 186 + (idx * 36)))
            surface.blit(item, item_rect)

        selected_color = (186, 192, 202) if selected_locked else (245, 248, 250)
        selected_label = self._prompt_font.render(f"Selected: {selected_name}", True, selected_color)
        selected_label_rect = selected_label.get_rect(center=(center_x, center_y + 26))
        surface.blit(selected_label, selected_label_rect)

        text_y = center_y + 58
        if selected_locked and selected_unlock_hint:
            lock_surface = self._body_font.render(f"Unlock: {selected_unlock_hint}", True, (255, 206, 164))
            lock_rect = lock_surface.get_rect(center=(center_x, text_y))
            surface.blit(lock_surface, lock_rect)
            text_y += 32
        if selected_note:
            note_surface = self._body_font.render(selected_note, True, self._prompt_color)
            note_rect = note_surface.get_rect(center=(center_x, text_y))
            surface.blit(note_surface, note_rect)
            text_y += 32

        if passive_summary:
            summary_surface = self._body_font.render(passive_summary, True, (235, 240, 248))
            summary_rect = summary_surface.get_rect(center=(center_x, text_y))
            surface.blit(summary_surface, summary_rect)
            text_y += 30
        else:
            bonus_surface = self._body_font.render(f"Bonus: {passive_bonus}", True, (168, 238, 180))
            bonus_rect = bonus_surface.get_rect(center=(center_x, text_y))
            surface.blit(bonus_surface, bonus_rect)
            text_y += 30

            drawback_surface = self._body_font.render(f"Drawback: {passive_drawback}", True, (255, 190, 190))
            drawback_rect = drawback_surface.get_rect(center=(center_x, text_y + 28))
            surface.blit(drawback_surface, drawback_rect)
            text_y += 28

        if selected_weapon_name:
            weapon_surface = self._body_font.render(f"Weapon: {selected_weapon_name}", True, (255, 228, 150))
            weapon_rect = weapon_surface.get_rect(center=(center_x, text_y + 30))
            surface.blit(weapon_surface, weapon_rect)

        prompt_surface = self._prompt_font.render(
            "Left/Right or A/D to choose | T or LB/RB to toggle weapon | Enter/Space to start",
            True,
            self._prompt_color,
        )
        prompt_rect = prompt_surface.get_rect(center=(center_x, surface.get_height() - 48))
        surface.blit(prompt_surface, prompt_rect)

    def draw_paused(
        self,
        surface: pygame.Surface,
        audio_enabled: bool,
        aim_assist_enabled: bool,
        options: tuple[str, ...],
        selected_index: int,
    ) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        surface.blit(overlay, (0, 0))

        pause_surface = self._state_font.render("PAUSED", True, self._state_color)
        option_surfaces: list[pygame.Surface] = []
        for idx, option in enumerate(options):
            label = option
            if option == "Toggle Sound":
                label = f"Toggle Sound: {'On' if audio_enabled else 'Off'}"
            elif option == "Toggle Aim Assist":
                label = f"Toggle Aim Assist: {'On' if aim_assist_enabled else 'Off'}"
            color = (255, 235, 140) if idx == selected_index else self._prompt_color
            option_surfaces.append(self._prompt_font.render(label, True, color))

        prompt = "Up/Down to Navigate | Enter/A to Confirm | P/Esc to Resume"
        prompt_surface = self._prompt_font.render(prompt, True, self._prompt_color)
        layout = self.paused_layout_rects(
            surface,
            audio_enabled=audio_enabled,
            aim_assist_enabled=aim_assist_enabled,
            options=options,
        )
        pause_rect = layout["title"]
        prompt_rect = layout["prompt"]
        option_rects = layout["options"]
        surface.blit(pause_surface, pause_rect)
        for option_surface, option_rect in zip(option_surfaces, option_rects):
            surface.blit(option_surface, option_rect)
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

        subtitle = self._prompt_font.render("Pick 1 Upgrade", True, self._prompt_color)
        surface.blit(subtitle, subtitle.get_rect(center=(center_x, 160)))

        card_w = min(360, (surface.get_width() - 120) // max(1, len(options)))
        card_h = 250
        total_w = (card_w * len(options)) + (20 * max(0, len(options) - 1))
        start_x = (surface.get_width() - total_w) // 2
        y = 220
        for idx, option in enumerate(options):
            x = start_x + (idx * (card_w + 20))
            selected = idx == selected_index
            option_data = option if isinstance(option, dict) else {}
            leads_to_evolution = bool(option_data.get("leads_to_evolution", False))
            card_color = (52, 74, 96, 230) if selected else (33, 52, 70, 210)
            if leads_to_evolution:
                card_color = (68, 86, 62, 232) if selected else (46, 64, 48, 216)
            border_color = (255, 228, 138) if selected else (160, 190, 214)
            if leads_to_evolution:
                border_color = (186, 255, 166) if selected else (132, 208, 154)
            card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            card.fill(card_color)
            surface.blit(card, (x, y))
            pygame.draw.rect(surface, border_color, (x, y, card_w, card_h), width=2, border_radius=8)

            name = str(option_data.get("name", getattr(option, "name", str(option))))
            desc = str(option_data.get("description", getattr(option, "description", "")))
            name_surface = self._prompt_font.render(name, True, (245, 248, 250))
            surface.blit(name_surface, (x + 14, y + 16))
            desc_surface = self._body_font.render(desc, True, (216, 229, 242))
            surface.blit(desc_surface, (x + 14, y + 82))
            if leads_to_evolution:
                evo_badge = self._body_font.render("EVOLUTION", True, (214, 255, 198))
                evo_rect = evo_badge.get_rect(topright=(x + card_w - 12, y + 16))
                surface.blit(evo_badge, evo_rect)

        hint = self._body_font.render("Arrows/Stick to choose, Enter/A to confirm", True, self._prompt_color)
        surface.blit(hint, hint.get_rect(center=(center_x, y + card_h + 40)))
