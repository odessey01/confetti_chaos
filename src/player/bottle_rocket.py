"""Bottle rocket entity fired by the player."""

from __future__ import annotations

from dataclasses import dataclass
import math

import pygame


@dataclass(frozen=True)
class BottleRocketFlightProfile:
    """Tunable flight parameters for future bottle rocket upgrade paths."""

    wobble_degrees: float = 3.4
    wobble_frequency_hz: float = 8.5
    acceleration_per_second: float = 52.0
    max_speed_multiplier: float = 1.2
    trail_emit_interval: float = 0.03
    trail_segment_lifetime: float = 0.15
    trail_segment_limit: int = 8
    decay_start_life_fraction: float = 0.5
    wobble_growth_multiplier: float = 1.9
    speed_decay_per_second: float = 120.0
    downward_arc_per_second: float = 0.5


class BottleRocket:
    """A fast bottle rocket projectile with directional visual orientation."""

    def __init__(
        self,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float = 500.0,
        lifetime: float = 3.0,
        max_travel_distance: float | None = None,
        size: int = 8,
        damage: int = 1,
        flight_profile: BottleRocketFlightProfile | None = None,
    ) -> None:
        self.flight_profile = flight_profile or BottleRocketFlightProfile()
        self.position = pygame.Vector2(position)
        self.direction = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)
        self._launch_direction = pygame.Vector2(self.direction)
        self.speed = float(speed)
        self._max_speed = float(speed) * max(1.0, float(self.flight_profile.max_speed_multiplier))
        self.lifetime = float(lifetime)
        self.max_lifetime = float(lifetime)
        self.max_travel_distance = (
            None
            if max_travel_distance is None
            else max(20.0, float(max_travel_distance))
        )
        self.distance_traveled = 0.0
        self.size = max(6, int(size))
        self.damage = max(1, int(damage))
        self._age = 0.0
        self._trail_emit_timer = 0.0
        self._trail_segments: list[tuple[pygame.Vector2, float, float]] = []
        self._last_decay_intensity = 0.0
        self.body_color = (255, 236, 190)
        self.tip_color = (255, 120, 84)
        self.fin_color = (255, 90, 130)
        self.stick_color = (214, 180, 128)
        self.trail_color = (214, 224, 232)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.position.x - self.size // 2),
            int(self.position.y - self.size // 2),
            self.size,
            self.size,
        )

    def update(self, delta_seconds: float) -> None:
        self._age += max(0.0, delta_seconds)
        self._trail_segments = [
            (position, ttl - delta_seconds, instability)
            for position, ttl, instability in self._trail_segments
            if (ttl - delta_seconds) > 0.0
        ]
        life_progress = self._normalized_life_progress()
        decay = self._decay_intensity(life_progress)
        self._last_decay_intensity = decay
        wobble_scale = 1.0 + (decay * max(0.0, self.flight_profile.wobble_growth_multiplier - 1.0))
        wobble_angle = (
            math.sin(self._age * (math.pi * 2.0) * self.flight_profile.wobble_frequency_hz)
            * self.flight_profile.wobble_degrees
            * wobble_scale
        )
        wobble_direction = self._launch_direction.rotate(wobble_angle)
        if self.flight_profile.downward_arc_per_second > 0.0 and decay > 0.0:
            wobble_direction.y += self.flight_profile.downward_arc_per_second * decay
        self.direction = wobble_direction.normalize() if wobble_direction.length_squared() > 0.0 else pygame.Vector2(1, 0)
        self.speed = min(self._max_speed, self.speed + (self.flight_profile.acceleration_per_second * delta_seconds))
        if decay > 0.0 and self.flight_profile.speed_decay_per_second > 0.0:
            min_speed = max(120.0, float(self._max_speed) * 0.62)
            self.speed = max(min_speed, self.speed - (self.flight_profile.speed_decay_per_second * decay * delta_seconds))
        displacement = self.direction * self.speed * delta_seconds
        self.position += displacement
        self.distance_traveled += displacement.length()
        self._trail_emit_timer -= max(0.0, delta_seconds)
        while self._trail_emit_timer <= 0.0:
            trail_anchor = self.position - (self.direction * (self.size * 0.8))
            self._trail_segments.append(
                (
                    pygame.Vector2(trail_anchor),
                    self.flight_profile.trail_segment_lifetime,
                    self._last_decay_intensity,
                )
            )
            if len(self._trail_segments) > self.flight_profile.trail_segment_limit:
                self._trail_segments = self._trail_segments[-self.flight_profile.trail_segment_limit :]
            self._trail_emit_timer += self.flight_profile.trail_emit_interval
        self.lifetime -= delta_seconds

    def _normalized_life_progress(self) -> float:
        if self.max_lifetime <= 0.0:
            return 1.0
        return max(0.0, min(self._age / self.max_lifetime, 1.0))

    def _decay_intensity(self, life_progress: float) -> float:
        start = max(0.0, min(1.0, float(self.flight_profile.decay_start_life_fraction)))
        if life_progress <= start:
            return 0.0
        return max(0.0, min((life_progress - start) / max(0.001, 1.0 - start), 1.0))

    def is_expired(self) -> bool:
        if self.lifetime <= 0.0:
            return True
        if self.max_travel_distance is None:
            return False
        return self.distance_traveled >= self.max_travel_distance

    def is_out_of_bounds(self, bounds: pygame.Rect, margin: int = 100) -> bool:
        return (
            self.position.x < -margin
            or self.position.x > bounds.width + margin
            or self.position.y < -margin
            or self.position.y > bounds.height + margin
        )

    def draw(self, surface: pygame.Surface) -> None:
        for trail_position, ttl, instability in self._trail_segments:
            ratio = max(0.0, min(1.0, ttl / self.flight_profile.trail_segment_lifetime))
            instability_jitter = 1.0 + (instability * 0.35)
            radius = max(1, int(((self.size * 0.35) + (self.size * 0.3 * ratio)) * instability_jitter))
            alpha = max(8, int((135 + (45 * instability)) * ratio))
            warm = (255, 196, 128)
            trail_color = (
                int(self.trail_color[0] + ((warm[0] - self.trail_color[0]) * instability)),
                int(self.trail_color[1] + ((warm[1] - self.trail_color[1]) * instability)),
                int(self.trail_color[2] + ((warm[2] - self.trail_color[2]) * instability)),
            )
            smoke = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(
                smoke,
                (trail_color[0], trail_color[1], trail_color[2], alpha),
                (radius + 1, radius + 1),
                radius,
            )
            surface.blit(smoke, (int(trail_position.x - radius - 1), int(trail_position.y - radius - 1)))

        sprite_size = max(12, self.size * 2)
        half = sprite_size // 2
        rocket_surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)

        body_length = max(6, int(self.size * 1.1))
        body_height = max(4, int(self.size * 0.55))
        body_rect = pygame.Rect(0, 0, body_length, body_height)
        body_rect.center = (half, half)
        pygame.draw.rect(rocket_surface, self.body_color, body_rect, border_radius=2)

        tip = [
            (body_rect.right + max(2, self.size // 3), half),
            (body_rect.right - 1, body_rect.top),
            (body_rect.right - 1, body_rect.bottom),
        ]
        pygame.draw.polygon(rocket_surface, self.tip_color, tip)

        tail_left = [
            (body_rect.left + 1, half),
            (body_rect.left - max(2, self.size // 3), body_rect.top + 1),
            (body_rect.left + 1, body_rect.top + 1),
        ]
        tail_right = [
            (body_rect.left + 1, half),
            (body_rect.left - max(2, self.size // 3), body_rect.bottom - 1),
            (body_rect.left + 1, body_rect.bottom - 1),
        ]
        pygame.draw.polygon(rocket_surface, self.fin_color, tail_left)
        pygame.draw.polygon(rocket_surface, self.fin_color, tail_right)

        stick_start = (body_rect.left - max(2, self.size // 2), half)
        stick_end = (body_rect.left + 1, half)
        pygame.draw.line(rocket_surface, self.stick_color, stick_start, stick_end, width=1)

        angle = -math.degrees(math.atan2(self.direction.y, self.direction.x))
        rotated = pygame.transform.rotate(rocket_surface, angle)
        draw_rect = rotated.get_rect(center=(int(self.position.x), int(self.position.y)))
        surface.blit(rotated, draw_rect)
