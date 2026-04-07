"""A floaty balloon enemy with gentle bobbing motion."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

from .hazard import Hazard


class BalloonEnemy(Hazard):
    def __init__(self, size: int = 68, speed: float = 155.0) -> None:
        super().__init__(size=size, speed=speed)
        self.base_speed = speed
        self._time = 0.0
        self._phase = random.uniform(0.0, math.tau)
        self._bob_strength = 42.0
        self._bob_frequency = 3.8
        self._float_axis = pygame.Vector2(0, 1)
        self.color = random.choice(
            [
                (255, 120, 140),
                (255, 170, 90),
                (255, 210, 110),
                (150, 220, 255),
                (190, 255, 170),
            ]
        )

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        super().launch_toward_target(spawn, target_center)
        self._time = 0.0
        if self.velocity.length_squared() > 0:
            direction = self.velocity.normalize()
            self._float_axis = pygame.Vector2(-direction.y, direction.x)
            # Keep the drift slightly varied while still predictable.
            if random.random() < 0.5:
                self._float_axis *= -1

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self._time += delta_seconds
        bob_component = math.sin(self._phase + self._time * self._bob_frequency) * self._bob_strength
        self.position += self.velocity * delta_seconds
        self.position += self._float_axis * (bob_component * delta_seconds)

    def draw(self, surface: pygame.Surface) -> None:
        center = self.rect.center
        radius = max(8, self.size // 2)
        pygame.draw.circle(surface, self.color, center, radius)
        pygame.draw.circle(surface, (250, 250, 255), center, radius, 2)
        knot_top = (center[0], center[1] + radius - 2)
        knot_left = (center[0] - 4, center[1] + radius + 6)
        knot_right = (center[0] + 4, center[1] + radius + 6)
        pygame.draw.polygon(surface, (240, 240, 245), [knot_top, knot_left, knot_right])

    def _behavior_snapshot(self) -> dict[str, Any]:
        return {
            "bob_strength": self._bob_strength,
            "bob_frequency": self._bob_frequency,
            "phase": self._phase,
        }
