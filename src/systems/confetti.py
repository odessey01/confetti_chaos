"""Lightweight confetti particle system for visual feedback."""

from __future__ import annotations

import math
import random

import pygame


class ConfettiParticle:
    """A single confetti particle that fades over time."""

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, lifetime: float = 0.6) -> None:
        """Initialize a confetti particle.

        Args:
            position: Starting position.
            velocity: Direction and speed (pixels per second).
            lifetime: Seconds before particle disappears.
        """
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = 4
        self.color = random.choice(
            [
                (255, 120, 140),  # Red-pink
                (255, 170, 90),   # Orange
                (255, 210, 110),  # Light orange
                (150, 220, 255),  # Light blue
                (190, 255, 170),  # Light green
            ]
        )

    def update(self, delta_seconds: float) -> None:
        """Update position and lifetime."""
        self.position += self.velocity * delta_seconds
        self.lifetime -= delta_seconds

    def is_expired(self) -> bool:
        """Return True if particle has reached end of lifetime."""
        return self.lifetime <= 0.0

    def get_alpha(self) -> float:
        """Return opacity as 0.0-1.0, fading over lifetime."""
        return max(0.0, self.lifetime / self.max_lifetime)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle with fading opacity."""
        if self.lifetime <= 0.0:
            return

        center = (int(self.position.x), int(self.position.y))
        alpha = max(0, int(255 * self.get_alpha()))

        # Create a temporary surface for alpha blending
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(particle_surface, (center[0] - self.size, center[1] - self.size))


class Confetti:
    """Manager for confetti particles."""

    def __init__(self) -> None:
        """Initialize the confetti system."""
        self.particles: list[ConfettiParticle] = []

    def spawn_burst(self, center: pygame.Vector2, count: int = 8) -> None:
        """Spawn a burst of confetti particles scattering outward.

        Args:
            center: Center point of the burst.
            count: Number of particles to spawn.
        """
        for _ in range(count):
            # Random angle around a circle
            angle = random.uniform(0, math.tau)
            # Random speed between 200-300 px/sec
            speed = random.uniform(200.0, 300.0)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            # Slight lifetime variation for organic feel
            lifetime = random.uniform(0.5, 0.8)

            particle = ConfettiParticle(center, velocity, lifetime=lifetime)
            self.particles.append(particle)

    def update(self, delta_seconds: float) -> None:
        """Update all particles and remove expired ones."""
        for particle in self.particles:
            particle.update(delta_seconds)

        # Remove expired particles
        self.particles = [p for p in self.particles if not p.is_expired()]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all active particles."""
        for particle in self.particles:
            particle.draw(surface)

    def is_empty(self) -> bool:
        """Return True if no particles are active."""
        return len(self.particles) == 0
