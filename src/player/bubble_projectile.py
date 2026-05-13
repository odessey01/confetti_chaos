"""Bubble wand projectile with floaty drift and pop behavior."""

from __future__ import annotations

import math
import random

import pygame


class BubbleProjectile:
    def __init__(
        self,
        *,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float,
        lifetime: float,
        size: int,
        damage: int,
        pop_radius: float,
        mode: str = "wobble",
        wobble_strength: float = 0.2,
        rise_per_second: float = 8.0,
        bounce_limit: int = 0,
        orbit_center: pygame.Vector2 | None = None,
        orbit_radius: float = 48.0,
        orbit_speed_degrees: float = 160.0,
    ) -> None:
        self.position = pygame.Vector2(position)
        basis = pygame.Vector2(direction)
        self.direction = basis.normalize() if basis.length_squared() > 0.0 else pygame.Vector2(1.0, 0.0)
        self.speed = max(10.0, float(speed))
        self.lifetime = max(0.05, float(lifetime))
        self.max_lifetime = float(self.lifetime)
        self.size = max(8, int(size))
        self.damage = max(1, int(damage))
        self.pop_radius = max(float(self.size), float(pop_radius))
        self.mode = str(mode or "wobble")
        self.wobble_strength = max(0.0, float(wobble_strength))
        self.rise_per_second = float(rise_per_second)
        self.bounce_limit = max(0, int(bounce_limit))
        self.bounce_count = 0
        self._rng = random.Random()
        self._age = 0.0
        self._phase = self._rng.uniform(0.0, math.tau)
        self._wobble_frequency = self._rng.uniform(1.8, 3.2)
        self._orbital_angle = self._rng.uniform(0.0, 360.0)
        self.orbit_center = pygame.Vector2(orbit_center) if orbit_center is not None else pygame.Vector2(position)
        self.orbit_radius = max(8.0, float(orbit_radius))
        self.orbit_speed_degrees = float(orbit_speed_degrees)
        self.pending_pop = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.position.x - self.size // 2),
            int(self.position.y - self.size // 2),
            self.size,
            self.size,
        )

    def update(self, delta_seconds: float, bounds: pygame.Rect | None = None) -> None:
        dt = max(0.0, float(delta_seconds))
        self._age += dt
        self.lifetime -= dt
        if self.mode == "orbit":
            self._orbital_angle = (self._orbital_angle + (self.orbit_speed_degrees * dt)) % 360.0
            self.position = self.orbit_center + pygame.Vector2(self.orbit_radius, 0.0).rotate(self._orbital_angle)
            return
        wobble = math.sin((self._age * self._wobble_frequency * math.tau) + self._phase) * self.wobble_strength
        move_dir = self.direction.rotate(wobble * 20.0 if self.mode in {"wobble", "rising", "bouncing"} else 0.0)
        displacement = move_dir * self.speed * dt
        self.position += displacement
        if self.mode in {"rising", "wobble"}:
            self.position.y -= self.rise_per_second * dt
        if self.mode == "bouncing" and bounds is not None:
            self._apply_bounce(bounds)

    def _apply_bounce(self, bounds: pygame.Rect) -> None:
        if self.bounce_count >= self.bounce_limit:
            return
        bounced = False
        half = self.size * 0.5
        if self.position.x - half <= float(bounds.left) or self.position.x + half >= float(bounds.right):
            self.direction.x *= -1.0
            bounced = True
        if self.position.y - half <= float(bounds.top) or self.position.y + half >= float(bounds.bottom):
            self.direction.y *= -1.0
            bounced = True
        if bounced:
            if self.direction.length_squared() > 0.0:
                self.direction = self.direction.normalize()
            self.bounce_count += 1

    def is_expired(self) -> bool:
        return self.lifetime <= 0.0 or self.pending_pop

    def draw(self, surface: pygame.Surface) -> None:
        radius = max(4, self.size // 2)
        alpha = max(64, int(170 * (self.lifetime / max(0.01, self.max_lifetime))))
        bubble_surface = pygame.Surface((radius * 2 + 6, radius * 2 + 6), pygame.SRCALPHA)
        center = (radius + 3, radius + 3)
        pygame.draw.circle(bubble_surface, (178, 236, 255, alpha), center, radius, width=2)
        pygame.draw.circle(bubble_surface, (232, 252, 255, min(255, alpha + 28)), center, max(2, radius // 3))
        surface.blit(bubble_surface, (int(self.position.x - radius - 3), int(self.position.y - radius - 3)))
