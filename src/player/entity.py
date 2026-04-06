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

    def update(self, delta_seconds: float, keys: pygame.key.ScancodeWrapper, bounds: pygame.Rect) -> None:
        move_x = (
            float(keys[pygame.K_d] or keys[pygame.K_RIGHT])
            - float(keys[pygame.K_a] or keys[pygame.K_LEFT])
        )
        move_y = (
            float(keys[pygame.K_s] or keys[pygame.K_DOWN])
            - float(keys[pygame.K_w] or keys[pygame.K_UP])
        )

        movement = pygame.Vector2(move_x, move_y)
        if movement.length_squared() > 0:
            movement = movement.normalize() * self.speed * delta_seconds
            self.position += movement

        max_x = bounds.width - self.size
        max_y = bounds.height - self.size
        self.position.x = max(0, min(self.position.x, max_x))
        self.position.y = max(0, min(self.position.y, max_y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
