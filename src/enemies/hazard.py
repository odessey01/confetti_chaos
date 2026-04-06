"""Hazard entity for the dodge/avoid core mechanic."""

from __future__ import annotations

import random

import pygame


class Hazard:
    def __init__(self, size: int = 34, speed: float = 220.0) -> None:
        self.size = size
        self.speed = speed
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.color = (255, 100, 100)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)

    def reset_toward_target(self, bounds: pygame.Rect, target_center: pygame.Vector2) -> None:
        side = random.choice(("left", "right", "top", "bottom"))

        if side == "left":
            spawn = pygame.Vector2(-self.size, random.uniform(0, bounds.height - self.size))
        elif side == "right":
            spawn = pygame.Vector2(bounds.width, random.uniform(0, bounds.height - self.size))
        elif side == "top":
            spawn = pygame.Vector2(random.uniform(0, bounds.width - self.size), -self.size)
        else:
            spawn = pygame.Vector2(random.uniform(0, bounds.width - self.size), bounds.height)

        to_target = target_center - spawn
        if to_target.length_squared() == 0:
            to_target = pygame.Vector2(1, 0)
        self.position = spawn
        self.velocity = to_target.normalize() * self.speed

    def update(self, delta_seconds: float) -> None:
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
