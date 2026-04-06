"""A slower hazard that periodically re-aims toward the player."""

from __future__ import annotations

import pygame

from .hazard import Hazard


class TrackingHazard(Hazard):
    def __init__(
        self,
        size: int = 30,
        speed: float = 170.0,
        retarget_interval: float = 0.75,
        max_retargets: int = 7,
    ) -> None:
        super().__init__(size=size, speed=speed)
        self.base_speed = speed
        self.retarget_interval = retarget_interval
        self.max_retargets = max_retargets
        self._retarget_timer = 0.0
        self._retarget_count = 0
        self.color = (120, 255, 170)

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        super().launch_toward_target(spawn, target_center)
        self._retarget_timer = 0.0
        self._retarget_count = 0

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self._retarget_timer += delta_seconds
        if (
            target_center is not None
            and self._retarget_count < self.max_retargets
            and self._retarget_timer >= self.retarget_interval
        ):
            self._retarget_timer = 0.0
            direction = target_center - self.position
            if direction.length_squared() > 0:
                self.velocity = direction.normalize() * self.speed
                self._retarget_count += 1
        super().update(delta_seconds, target_center)
