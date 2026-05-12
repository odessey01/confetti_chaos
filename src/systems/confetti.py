"""Lightweight confetti particle system for visual feedback."""

from __future__ import annotations

import math
import random

import pygame


class ConfettiParticle:
    """A single confetti particle that fades over time."""

    def __init__(
        self,
        position: pygame.Vector2,
        velocity: pygame.Vector2,
        lifetime: float = 0.6,
        *,
        size: int = 4,
        color: tuple[int, int, int] | None = None,
    ) -> None:
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
        self.size = max(2, int(size))
        self.color = color or random.choice(
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

    def spawn_burst(
        self,
        center: pygame.Vector2,
        count: int = 8,
        *,
        speed_min: float = 200.0,
        speed_max: float = 300.0,
        lifetime_min: float = 0.5,
        lifetime_max: float = 0.8,
    ) -> None:
        """Spawn a burst of confetti particles scattering outward.

        Args:
            center: Center point of the burst.
            count: Number of particles to spawn.
        """
        for _ in range(count):
            # Random angle around a circle
            angle = random.uniform(0, math.tau)
            # Random speed between configured bounds
            speed = random.uniform(speed_min, speed_max)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            # Slight lifetime variation for organic feel
            lifetime = random.uniform(lifetime_min, lifetime_max)

            particle = ConfettiParticle(center, velocity, lifetime=lifetime)
            self.particles.append(particle)

    def spawn_starburst(
        self,
        center: pygame.Vector2,
        *,
        spoke_count: int = 26,
        particles_per_spoke: int = 3,
    ) -> None:
        """Spawn a large, colorful radial burst used for super activation."""
        vivid_palette = [
            (255, 70, 110),
            (255, 140, 40),
            (255, 220, 70),
            (120, 245, 110),
            (60, 225, 245),
            (120, 160, 255),
            (255, 120, 240),
        ]
        safe_spokes = max(8, int(spoke_count))
        safe_per_spoke = max(1, int(particles_per_spoke))
        origin = pygame.Vector2(center)

        for spoke_idx in range(safe_spokes):
            base_angle = (math.tau * spoke_idx) / safe_spokes
            for _ in range(safe_per_spoke):
                angle = base_angle + random.uniform(-0.08, 0.08)
                speed = random.uniform(260.0, 520.0)
                velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
                lifetime = random.uniform(0.42, 0.78)
                particle = ConfettiParticle(
                    origin,
                    velocity,
                    lifetime=lifetime,
                    size=random.randint(4, 7),
                    color=random.choice(vivid_palette),
                )
                self.particles.append(particle)

        # Fill in between spokes so the burst feels dense and celebratory.
        fill_count = max(18, safe_spokes // 2)
        for _ in range(fill_count):
            angle = random.uniform(0.0, math.tau)
            speed = random.uniform(180.0, 360.0)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            lifetime = random.uniform(0.35, 0.62)
            particle = ConfettiParticle(
                origin,
                velocity,
                lifetime=lifetime,
                size=random.randint(3, 6),
                color=random.choice(vivid_palette),
            )
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
