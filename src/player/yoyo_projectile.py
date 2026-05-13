"""Yo-Yo projectile with outbound and return state machine."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame


YOYO_STATE_OUTWARD = "outward"
YOYO_STATE_PAUSE = "pause"
YOYO_STATE_RETURNING = "returning"
YOYO_STATE_COMPLETE = "complete"


@dataclass
class YoyoProjectile:
    origin: pygame.Vector2
    direction: pygame.Vector2
    max_distance: float
    travel_speed: float
    return_speed: float
    damage: int
    hit_cooldown_seconds: float = 0.2
    hover_pause_seconds: float = 0.0
    radius: int = 9
    state: str = YOYO_STATE_OUTWARD
    _pause_timer: float = 0.0
    _distance_out: float = 0.0
    _hit_cooldowns: dict[int, float] = field(default_factory=dict)
    _trail_points: list[pygame.Vector2] = field(default_factory=list)

    def __post_init__(self) -> None:
        direction = pygame.Vector2(self.direction)
        if direction.length_squared() <= 0.0:
            direction = pygame.Vector2(1.0, 0.0)
        self.direction = direction.normalize()
        self.position = pygame.Vector2(self.origin)
        self._trail_points = [pygame.Vector2(self.position)]

    @property
    def rect(self) -> pygame.Rect:
        diameter = self.radius * 2
        rect = pygame.Rect(0, 0, diameter, diameter)
        rect.center = (int(self.position.x), int(self.position.y))
        return rect

    def can_hit_target(self, target_id: int) -> bool:
        return self._hit_cooldowns.get(int(target_id), 0.0) <= 0.0

    def register_hit(self, target_id: int) -> None:
        self._hit_cooldowns[int(target_id)] = max(0.0, float(self.hit_cooldown_seconds))

    def update(self, delta_seconds: float, *, anchor: pygame.Vector2) -> None:
        delta = max(0.0, float(delta_seconds))
        self._hit_cooldowns = {
            target_id: max(0.0, cooldown - delta)
            for target_id, cooldown in self._hit_cooldowns.items()
            if cooldown > delta
        }
        if self.state == YOYO_STATE_COMPLETE:
            return
        self._trail_points.append(pygame.Vector2(self.position))
        if len(self._trail_points) > 8:
            self._trail_points = self._trail_points[-8:]
        if self.state == YOYO_STATE_OUTWARD:
            step = self.direction * (self.travel_speed * delta)
            self.position += step
            self._distance_out += step.length()
            if self._distance_out >= max(24.0, float(self.max_distance)):
                if self.hover_pause_seconds > 0.0:
                    self.state = YOYO_STATE_PAUSE
                    self._pause_timer = float(self.hover_pause_seconds)
                else:
                    self.state = YOYO_STATE_RETURNING
            return
        if self.state == YOYO_STATE_PAUSE:
            self._pause_timer = max(0.0, self._pause_timer - delta)
            if self._pause_timer <= 0.0:
                self.state = YOYO_STATE_RETURNING
            return
        if self.state == YOYO_STATE_RETURNING:
            to_anchor = pygame.Vector2(anchor) - self.position
            distance = to_anchor.length()
            if distance <= max(10.0, self.return_speed * delta):
                self.position = pygame.Vector2(anchor)
                self.state = YOYO_STATE_COMPLETE
                return
            self.position += to_anchor.normalize() * (self.return_speed * delta)

    def draw(self, surface: pygame.Surface) -> None:
        if self.state == YOYO_STATE_COMPLETE:
            return
        if len(self._trail_points) >= 2:
            for index in range(1, len(self._trail_points)):
                start = self._trail_points[index - 1]
                end = self._trail_points[index]
                alpha = max(30, min(170, int((index / max(1, len(self._trail_points) - 1)) * 170)))
                trail_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                pygame.draw.line(
                    trail_surface,
                    (255, 182, 220, alpha),
                    (int(start.x), int(start.y)),
                    (int(end.x), int(end.y)),
                    width=2,
                )
                surface.blit(trail_surface, (0, 0))
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, (244, 132, 186), center, self.radius)
        pygame.draw.circle(surface, (255, 236, 244), center, max(2, self.radius - 3), width=2)
