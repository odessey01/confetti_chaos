"""Projectile entity fired by the player."""

from __future__ import annotations

import pygame


class Projectile:
    """A simple projectile that travels in a direction and expires after time or bounds."""

    def __init__(
        self,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float = 500.0,
        lifetime: float = 3.0,
        size: int = 8,
    ) -> None:
        """Initialize a projectile.

        Args:
            position: Starting position (typically player center).
            direction: Unit vector for movement direction.
            speed: Pixels per second.
            lifetime: Seconds before automatic expiration.
            size: Diameter of the projectile circle.
        """
        self.position = pygame.Vector2(position)
        self.direction = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)
        self.speed = speed
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.color = (255, 255, 150)
        self.accent_color = (255, 200, 50)

    @property
    def rect(self) -> pygame.Rect:
        """Return the bounding rect for collision detection."""
        return pygame.Rect(
            int(self.position.x - self.size // 2),
            int(self.position.y - self.size // 2),
            self.size,
            self.size,
        )

    def update(self, delta_seconds: float) -> None:
        """Update position and lifetime."""
        self.position += self.direction * self.speed * delta_seconds
        self.lifetime -= delta_seconds

    def is_expired(self) -> bool:
        """Return True if projectile has reached end of lifetime."""
        return self.lifetime <= 0.0

    def is_out_of_bounds(self, bounds: pygame.Rect, margin: int = 100) -> bool:
        """Check if projectile has left the play area."""
        return (
            self.position.x < -margin
            or self.position.x > bounds.width + margin
            or self.position.y < -margin
            or self.position.y > bounds.height + margin
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the projectile as a small circle."""
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, self.color, center, self.size // 2)
        pygame.draw.circle(surface, self.accent_color, center, self.size // 2, 1)
