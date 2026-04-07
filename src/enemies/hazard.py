"""Hazard entity for the dodge/avoid core mechanic."""

from __future__ import annotations

from typing import Any

import pygame


class Hazard:
    def __init__(self, size: int = 34, speed: float = 220.0) -> None:
        self.size = size
        self.speed = speed
        self.base_speed = speed
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.color = (255, 100, 100)
        self.spawn_profile: dict[str, Any] | None = None
        self.spawn_snapshot: dict[str, Any] | None = None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        to_target = target_center - spawn
        if to_target.length_squared() == 0:
            to_target = pygame.Vector2(1, 0)
        self.position = spawn
        self.velocity = to_target.normalize() * self.speed

    def set_speed(self, speed: float) -> None:
        self.speed = speed
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize() * self.speed

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self.position += self.velocity * delta_seconds

    def is_out_of_bounds(self, bounds: pygame.Rect, margin: int = 80) -> bool:
        return (
            self.position.x < -self.size - margin
            or self.position.x > bounds.width + margin
            or self.position.y < -self.size - margin
            or self.position.y > bounds.height + margin
        )

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)

    def apply_spawn_profile(self, profile: dict[str, Any]) -> None:
        """Assign immutable-at-runtime spawn attributes to this enemy instance."""
        self.spawn_profile = dict(profile)
        self.set_speed(float(profile["speed"]))
        self.base_speed = self.speed
        if "health" in profile and hasattr(self, "health"):
            self.health = int(profile["health"])

    def capture_spawn_snapshot(self, *, level: int, flavor: str) -> None:
        """Capture spawn-time attributes once; active enemies keep this stable snapshot."""
        if self.spawn_snapshot is not None:
            return
        if self.spawn_profile is None:
            self.spawn_profile = {
                "tier": level,
                "speed": float(self.speed),
                "health": int(getattr(self, "health", 0)),
                "movement_profile": "default",
                "flavor_tag": flavor,
                "enemy_kind": self.__class__.__name__.lower(),
            }
        tier = level
        movement_profile = "default"
        enemy_kind = "hazard"
        if self.spawn_profile is not None:
            tier = int(self.spawn_profile.get("tier", tier))
            flavor = str(self.spawn_profile.get("flavor_tag", flavor))
            movement_profile = str(self.spawn_profile.get("movement_profile", movement_profile))
            enemy_kind = str(self.spawn_profile.get("enemy_kind", enemy_kind))
        self.spawn_snapshot = {
            "level": level,
            "tier": tier,
            "flavor": flavor,
            "speed": float(self.speed),
            "health": int(getattr(self, "health", 0)),
            "movement_profile": movement_profile,
            "enemy_kind": enemy_kind,
            "behavior": self._behavior_snapshot(),
            "traits": {"size": self.size, "color": tuple(self.color)},
        }

    def _behavior_snapshot(self) -> dict[str, Any]:
        return {}
