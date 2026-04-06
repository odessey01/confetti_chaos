from __future__ import annotations

import pygame

from confetti_chaos.scenes.base import Scene


class TitleScene(Scene):
    name = "title"

    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.body_font = pygame.font.SysFont("arial", 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.manager.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.quit()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.manager.replace("gameplay")

    def update(self, dt: float) -> None:
        return

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((255, 243, 220))

        title = self.title_font.render("Confetti Chaos", True, (42, 35, 78))
        prompt = self.body_font.render("Press Enter to start", True, (66, 66, 66))
        quit_text = self.body_font.render("Press Esc to quit", True, (66, 66, 66))

        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 220)))
        surface.blit(prompt, prompt.get_rect(center=(surface.get_width() // 2, 340)))
        surface.blit(quit_text, quit_text.get_rect(center=(surface.get_width() // 2, 390)))
