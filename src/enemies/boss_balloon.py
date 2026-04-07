"""Boss balloon enemy - large, durable enemy that appears on milestone levels."""

from __future__ import annotations

from typing import Any

import pygame

from .hazard import Hazard


class BossBalloon(Hazard):
    """A large, durable balloon enemy that requires multiple hits to defeat."""

    def __init__(self, speed: float) -> None:
        # Boss is 2x the size of normal balloons
        size = 136  # 68 * 2
        super().__init__(size, speed)
        self.health = 3  # Requires 3 hits to defeat
        self.color = (255, 100, 100)  # Red color to distinguish from normal balloons
        self.outline_color = (255, 215, 0)  # Gold outline
        
        # Charge burst behavior
        self.charge_timer = 0.0
        self.is_charging = False
        self.charge_duration = 1.5  # seconds
        self.charge_speed_multiplier = 1.5
        self.charge_color = (255, 50, 50)  # Bright red during charge

    def take_damage(self) -> bool:
        """Reduce health by 1 and trigger charge burst. Return True if defeated."""
        self.health -= 1
        if self.health > 0:
            # Trigger charge burst
            self.is_charging = True
            self.charge_timer = self.charge_duration
        return self.health <= 0

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        """Update boss behavior including charge burst logic."""
        # Handle charge burst timer
        if self.is_charging:
            self.charge_timer -= delta_seconds
            if self.charge_timer <= 0:
                self.is_charging = False
                self.charge_timer = 0.0
        
        # Apply charge speed multiplier
        current_speed = self.base_speed * self.charge_speed_multiplier if self.is_charging else self.base_speed
        self.speed = current_speed
        
        # Update movement (inherit from parent)
        super().update(delta_seconds, target_center)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the boss balloon with special visual effects."""
        # Use charge color when charging
        current_color = self.charge_color if self.is_charging else self.color
        
        # Draw main body
        pygame.draw.circle(surface, current_color, self.rect.center, self.size // 2)
        # Draw gold outline
        pygame.draw.circle(surface, self.outline_color, self.rect.center, self.size // 2, 3)
        # Draw health indicator (simple bars)
        bar_width = self.size
        bar_height = 6
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 10

        # Background bar
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Health bar
        health_width = (self.health / 3) * bar_width
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))

    def _behavior_snapshot(self) -> dict[str, Any]:
        return {
            "charge_duration": self.charge_duration,
            "charge_speed_multiplier": self.charge_speed_multiplier,
        }
