"""Player entity and movement logic."""

from __future__ import annotations

import pygame


class Player:
    def __init__(self, x: float, y: float, size: int = 80, speed: float = 320.0) -> None:
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.speed = speed
        self.dodge_duration = 0.14
        self.dodge_distance = 130.0
        self.dodge_cooldown_duration = 0.9
        self.dodge_invulnerability_duration = 0.08
        self.max_health = 3
        self.current_health = 3
        self.damage_cooldown_duration = 0.75
        self._damage_cooldown_timer = 0.0
        self.visual_variant_id = "teddy_f"
        self.facing = pygame.Vector2(1, 0)
        self._is_dodging = False
        self._dodge_timer = 0.0
        self._dodge_cooldown_timer = 0.0
        self._dodge_invulnerability_timer = 0.0
        self._dodge_velocity = pygame.Vector2(0, 0)
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
        return self._damage_cooldown_timer > 0.0 or self._dodge_invulnerability_timer > 0.0

    @property
    def is_dodging(self) -> bool:
        return self._is_dodging

    @property
    def dodge_time_remaining(self) -> float:
        return self._dodge_timer

    @property
    def dodge_cooldown_remaining(self) -> float:
        return self._dodge_cooldown_timer

    def reset_health(self) -> None:
        self.current_health = self.max_health
        self._damage_cooldown_timer = 0.0

    def grant_invulnerability(self, duration: float) -> None:
        self._damage_cooldown_timer = max(self._damage_cooldown_timer, max(0.0, float(duration)))

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

    def try_start_dodge(self, movement_input: pygame.Vector2) -> bool:
        if self.current_health <= 0:
            return False
        if self._is_dodging:
            return False
        if self._dodge_cooldown_timer > 0.0:
            return False
        direction = pygame.Vector2(movement_input.x, movement_input.y)
        if direction.length_squared() <= 0.0:
            direction = pygame.Vector2(self.facing)
        if direction.length_squared() <= 0.0:
            direction = pygame.Vector2(1, 0)
        direction = direction.normalize()
        self.facing = pygame.Vector2(direction)
        self._is_dodging = True
        self._dodge_timer = self.dodge_duration
        self._dodge_cooldown_timer = self.dodge_cooldown_duration
        self._dodge_invulnerability_timer = self.dodge_invulnerability_duration
        dodge_speed = self.dodge_distance / max(self.dodge_duration, 0.001)
        self._dodge_velocity = direction * dodge_speed
        return True

    def update(
        self,
        delta_seconds: float,
        movement_input: pygame.Vector2,
        bounds: pygame.Rect,
    ) -> None:
        self._damage_cooldown_timer = max(0.0, self._damage_cooldown_timer - delta_seconds)
        self._dodge_cooldown_timer = max(0.0, self._dodge_cooldown_timer - delta_seconds)
        self._dodge_invulnerability_timer = max(
            0.0,
            self._dodge_invulnerability_timer - delta_seconds,
        )
        input_vector = pygame.Vector2(movement_input.x, movement_input.y)
        input_strength = min(input_vector.length(), 1.0)
        prior_intensity = self._movement_intensity
        if self._is_dodging:
            self.position += self._dodge_velocity * delta_seconds
            self._dodge_timer = max(0.0, self._dodge_timer - delta_seconds)
            self._movement_phase += delta_seconds * 26.0
            if self._dodge_timer <= 0.0:
                self._is_dodging = False
                self._dodge_velocity.update(0.0, 0.0)
        elif input_vector.length_squared() > 0:
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
