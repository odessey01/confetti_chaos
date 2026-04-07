"""A heavier party pinata enemy with deliberate drifting motion."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

from .hazard import Hazard


class PinataEnemy(Hazard):
    def __init__(
        self,
        size: int = 78,
        speed: float = 120.0,
        *,
        max_health: int = 3,
        damage_per_hit: int = 1,
    ) -> None:
        super().__init__(size=size, speed=speed)
        self.base_speed = speed
        self.max_health = max(2, int(max_health))
        self.damage_per_hit = max(1, int(damage_per_hit))
        self.health = self.max_health
        self._time = 0.0
        self._phase = random.uniform(0.0, math.tau)
        self._drift_strength = 26.0
        self._drift_frequency = 1.9
        self._drift_axis = pygame.Vector2(0, 1)
        self.color = random.choice(
            [
                (170, 70, 220),
                (70, 170, 210),
                (230, 140, 40),
            ]
        )
        self.hit_invuln_duration = 0.12
        self.hit_invuln_timer = 0.0
        self.hit_flash_duration = 0.12
        self.hit_flash_timer = 0.0
        self.hit_wobble_duration = 0.2
        self.hit_wobble_timer = 0.0
        # Surprise behavior: briefly surges speed when hit.
        self.surprise_speed_multiplier = 1.55
        self.surprise_duration = 0.45
        self.surprise_timer = 0.0
        self._surprise_triggered = False

    def apply_hit(self) -> tuple[bool, bool]:
        """Apply one hit; returns (hit_registered, defeated)."""
        if self.hit_invuln_timer > 0.0 or self.health <= 0:
            return False, False
        self.health = max(0, self.health - self.damage_per_hit)
        self.hit_invuln_timer = self.hit_invuln_duration
        self.hit_flash_timer = self.hit_flash_duration
        self.hit_wobble_timer = self.hit_wobble_duration
        self.surprise_timer = self.surprise_duration
        self._surprise_triggered = True
        return True, self.health <= 0

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        super().launch_toward_target(spawn, target_center)
        self._time = 0.0
        if self.velocity.length_squared() > 0:
            direction = self.velocity.normalize()
            self._drift_axis = pygame.Vector2(-direction.y, direction.x)
            if random.random() < 0.5:
                self._drift_axis *= -1

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self.hit_invuln_timer = max(0.0, self.hit_invuln_timer - delta_seconds)
        self.hit_flash_timer = max(0.0, self.hit_flash_timer - delta_seconds)
        self.hit_wobble_timer = max(0.0, self.hit_wobble_timer - delta_seconds)
        self.surprise_timer = max(0.0, self.surprise_timer - delta_seconds)
        current_speed = self.base_speed * (
            self.surprise_speed_multiplier if self.surprise_timer > 0.0 else 1.0
        )
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize() * current_speed
        self._time += delta_seconds
        drift_component = math.sin(self._phase + self._time * self._drift_frequency) * self._drift_strength
        self.position += self.velocity * delta_seconds
        self.position += self._drift_axis * (drift_component * delta_seconds)

    def consume_surprise_cues(self) -> dict[str, bool]:
        cues = {"reaction_triggered": self._surprise_triggered}
        self._surprise_triggered = False
        return cues

    def draw(self, surface: pygame.Surface) -> None:
        center = self.rect.center
        radius = max(10, self.size // 2)
        wobble_scale = 1.0
        if self.hit_wobble_timer > 0.0:
            progress = 1.0 - (self.hit_wobble_timer / self.hit_wobble_duration)
            wobble_scale = 1.0 + (1.0 - progress) * 0.07
        radius = max(10, int(radius * wobble_scale))
        top = (center[0], center[1] - radius)
        right = (center[0] + radius, center[1])
        bottom = (center[0], center[1] + radius)
        left = (center[0] - radius, center[1])
        fill_color = (255, 230, 210) if self.hit_flash_timer > 0.0 else self.color
        pygame.draw.polygon(surface, fill_color, [top, right, bottom, left])
        pygame.draw.polygon(surface, (250, 245, 215), [top, right, bottom, left], width=2)
        stripe_y = center[1]
        pygame.draw.line(
            surface,
            (255, 230, 140),
            (center[0] - radius + 6, stripe_y),
            (center[0] + radius - 6, stripe_y),
            3,
        )
        # Simple crack lines intensify with damage.
        damage_level = self.max_health - self.health
        if damage_level > 0:
            crack_color = (60, 40, 40)
            pygame.draw.line(
                surface,
                crack_color,
                (center[0] - radius // 3, center[1] - radius // 3),
                (center[0] + radius // 6, center[1] + radius // 8),
                2,
            )
        if damage_level > 1:
            pygame.draw.line(
                surface,
                crack_color,
                (center[0] - radius // 8, center[1] + radius // 5),
                (center[0] + radius // 3, center[1] - radius // 6),
                2,
            )

    def _behavior_snapshot(self) -> dict[str, Any]:
        return {
            "drift_strength": self._drift_strength,
            "drift_frequency": self._drift_frequency,
            "phase": self._phase,
            "max_health": self.max_health,
            "damage_per_hit": self.damage_per_hit,
            "surprise_speed_multiplier": self.surprise_speed_multiplier,
            "surprise_duration": self.surprise_duration,
        }
