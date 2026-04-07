"""Player entity and movement logic for Task 2."""

from __future__ import annotations

import math

import pygame


class Player:
    def __init__(self, x: float, y: float, size: int = 40, speed: float = 320.0) -> None:
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.speed = speed
        self.color = (90, 220, 255)
        self.accent_color = (245, 250, 255)
        self.facing = pygame.Vector2(1, 0)
        self._movement_phase = 0.0
        self._movement_intensity = 0.0

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
        input_vector = pygame.Vector2(movement_input.x, movement_input.y)
        input_strength = min(input_vector.length(), 1.0)
        if input_vector.length_squared() > 0:
            self.facing = input_vector.normalize()
            movement = self.facing * self.speed * delta_seconds
            self.position += movement
            self._movement_phase += delta_seconds * 18.0
        self._movement_intensity = input_strength

        max_x = bounds.width - self.size
        max_y = bounds.height - self.size
        self.position.x = max(0, min(self.position.x, max_x))
        self.position.y = max(0, min(self.position.y, max_y))

    def draw(self, surface: pygame.Surface) -> None:
        center = pygame.Vector2(self.rect.center)
        base_radius = self.size * 0.5
        pulse = math.sin(self._movement_phase) * 0.07 * self._movement_intensity
        radius_x = max(10.0, base_radius * (1.0 + pulse))
        radius_y = max(10.0, base_radius * (1.0 - pulse))

        body_rect = pygame.Rect(0, 0, int(radius_x * 2), int(radius_y * 2))
        body_rect.center = (int(center.x), int(center.y))
        pygame.draw.ellipse(surface, self.color, body_rect)
        pygame.draw.ellipse(surface, self.accent_color, body_rect, width=2)

        face_tip = center + self.facing * (base_radius * 0.9)
        side = pygame.Vector2(-self.facing.y, self.facing.x)
        left = center + side * (base_radius * 0.32)
        right = center - side * (base_radius * 0.32)
        pygame.draw.polygon(
            surface,
            self.accent_color,
            [
                (int(face_tip.x), int(face_tip.y)),
                (int(left.x), int(left.y)),
                (int(right.x), int(right.y)),
            ],
        )
