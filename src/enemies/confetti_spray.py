"""Short-lived confetti spray projectile used by confetti sprayer enemies."""

from __future__ import annotations

import pygame


class ConfettiSpray:
    def __init__(
        self,
        *,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float = 320.0,
        lifetime: float = 0.65,
        size: int = 10,
    ) -> None:
        self.position = pygame.Vector2(position)
        if direction.length_squared() <= 0.0:
            direction = pygame.Vector2(1.0, 0.0)
        self.velocity = direction.normalize() * speed
        self.lifetime = lifetime
        self.size = size
        self.color = (235, 245, 140)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)

    def update(self, delta_seconds: float) -> None:
        self.lifetime = max(0.0, self.lifetime - delta_seconds)
        self.position += self.velocity * delta_seconds

    def is_expired(self) -> bool:
        return self.lifetime <= 0.0

    def is_out_of_bounds(self, bounds: pygame.Rect, margin: int = 64) -> bool:
        return (
            self.position.x < -margin
            or self.position.x > bounds.width + margin
            or self.position.y < -margin
            or self.position.y > bounds.height + margin
        )

    def draw(self, surface: pygame.Surface) -> None:
        center = self.rect.center
        radius = max(3, self.size // 2)
        pygame.draw.circle(surface, self.color, center, radius)
