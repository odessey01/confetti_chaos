from __future__ import annotations

import pygame

from confetti_chaos.scenes.base import Scene


class GameplayScene(Scene):
    name = "gameplay"

    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.font = pygame.font.SysFont("arial", 30)
        self.elapsed = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.manager.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.replace("title")

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((214, 248, 255))
        headline = self.font.render("Gameplay scene placeholder", True, (30, 59, 91))
        details = self.font.render(
            f"Elapsed time: {self.elapsed:0.1f}s",
            True,
            (30, 59, 91),
        )
        hint = self.font.render("Press Esc to return to title", True, (30, 59, 91))

        surface.blit(headline, headline.get_rect(center=(surface.get_width() // 2, 260)))
        surface.blit(details, details.get_rect(center=(surface.get_width() // 2, 320)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 380)))
