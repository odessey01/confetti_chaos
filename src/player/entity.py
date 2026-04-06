"""Player entity and movement logic for Task 2."""

from __future__ import annotations

import pygame


class Player:
    def __init__(self, x: float, y: float, size: int = 40, speed: float = 320.0) -> None:
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.speed = speed
        self.color = (90, 220, 255)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)

    def reset_position(self, x: float, y: float) -> None:
        self.position.update(x, y)

    def update(
        self,
        delta_seconds: float,
        movement_input: pygame.Vector2,
        bounds: pygame.Rect,
    ) -> None:
        movement = pygame.Vector2(movement_input.x, movement_input.y)
        if movement.length_squared() > 0:
            movement = movement.normalize() * self.speed * delta_seconds
            self.position += movement

        max_x = bounds.width - self.size
        max_y = bounds.height - self.size
        self.position.x = max(0, min(self.position.x, max_x))
        self.position.y = max(0, min(self.position.y, max_y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
