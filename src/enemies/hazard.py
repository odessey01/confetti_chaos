"""Hazard entity for the dodge/avoid core mechanic."""

from __future__ import annotations

import pygame


class Hazard:
    def __init__(self, size: int = 34, speed: float = 220.0) -> None:
        self.size = size
        self.speed = speed
        self.base_speed = speed
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.color = (255, 100, 100)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        to_target = target_center - spawn
        if to_target.length_squared() == 0:
            to_target = pygame.Vector2(1, 0)
        self.position = spawn
        self.velocity = to_target.normalize() * self.speed

    def set_speed(self, speed: float) -> None:
        self.speed = speed
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize() * self.speed

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self.position += self.velocity * delta_seconds

    def is_out_of_bounds(self, bounds: pygame.Rect, margin: int = 80) -> bool:
        return (
            self.position.x < -self.size - margin
            or self.position.x > bounds.width + margin
            or self.position.y < -self.size - margin
            or self.position.y > bounds.height + margin
        )

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
