"""Player entity and movement logic."""

from __future__ import annotations

import pygame


class Player:
    def __init__(self, x: float, y: float, size: int = 80, speed: float = 320.0) -> None:
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.speed = speed
        self.max_health = 3
        self.current_health = 3
        self.damage_cooldown_duration = 0.75
        self._damage_cooldown_timer = 0.0
        self.visual_variant_id = "teddy_f"
        self.facing = pygame.Vector2(1, 0)
        self._movement_phase = 0.0
        self._movement_intensity = 0.0
        self._movement_juice = 0.0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)

    def reset_position(self, x: float, y: float) -> None:
        self.position.update(x, y)

    @property
    def movement_phase(self) -> float:
        return self._movement_phase

    @property
    def movement_intensity(self) -> float:
        return self._movement_intensity

    @property
    def movement_juice(self) -> float:
        return self._movement_juice

    @property
    def damage_cooldown_remaining(self) -> float:
        return self._damage_cooldown_timer

    @property
    def is_invulnerable(self) -> bool:
        return self._damage_cooldown_timer > 0.0

    def reset_health(self) -> None:
        self.current_health = self.max_health
        self._damage_cooldown_timer = 0.0

    def set_health(self, value: int) -> None:
        self.current_health = max(0, min(int(value), int(self.max_health)))

    def apply_damage(self, amount: int = 1) -> bool:
        if amount <= 0:
            return False
        if self.is_invulnerable:
            return False
        self.set_health(self.current_health - int(amount))
        self._damage_cooldown_timer = self.damage_cooldown_duration
        return True

    def update(
        self,
        delta_seconds: float,
        movement_input: pygame.Vector2,
        bounds: pygame.Rect,
    ) -> None:
        self._damage_cooldown_timer = max(0.0, self._damage_cooldown_timer - delta_seconds)
        input_vector = pygame.Vector2(movement_input.x, movement_input.y)
        input_strength = min(input_vector.length(), 1.0)
        prior_intensity = self._movement_intensity
        if input_vector.length_squared() > 0:
            self.facing = input_vector.normalize()
            movement = self.facing * self.speed * delta_seconds
            self.position += movement
            self._movement_phase += delta_seconds * 18.0
        self._movement_intensity = input_strength
        intensity_change = abs(self._movement_intensity - prior_intensity)
        self._movement_juice = max(self._movement_juice * max(0.0, 1.0 - (delta_seconds * 6.0)), 0.0)
        self._movement_juice = min(1.0, self._movement_juice + (intensity_change * 1.3))

        max_x = bounds.width - self.size
        max_y = bounds.height - self.size
        self.position.x = max(0, min(self.position.x, max_x))
        self.position.y = max(0, min(self.position.y, max_y))
