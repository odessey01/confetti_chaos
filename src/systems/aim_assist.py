"""Aim assist target evaluation and directional adjustment."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians

import pygame


@dataclass(frozen=True)
class AimAssistConfig:
    enabled: bool = True
    cone_degrees: float = 20.0
    max_distance: float = 340.0
    assist_strength: float = 0.24


@dataclass(frozen=True)
class AimAssistTarget:
    center: pygame.Vector2
    distance: float
    angle_degrees: float


class AimAssistSystem:
    """Optional controller-friendly aim nudging."""

    def __init__(self, config: AimAssistConfig | None = None) -> None:
        self.config = config or AimAssistConfig()

    def adjusted_direction(
        self,
        *,
        origin: pygame.Vector2,
        aim_direction: pygame.Vector2,
        target_centers: list[pygame.Vector2],
    ) -> pygame.Vector2:
        normalized = self._normalize_direction(aim_direction)
        if not self.config.enabled:
            return normalized
        target = self.select_target(origin=origin, aim_direction=normalized, target_centers=target_centers)
        if target is None:
            return normalized
        to_target = target.center - origin
        if to_target.length_squared() <= 0.0:
            return normalized
        target_direction = to_target.normalize()
        assist_factor = self._assist_factor(target.distance, target.angle_degrees)
        return normalized.lerp(target_direction, assist_factor).normalize()

    def select_target(
        self,
        *,
        origin: pygame.Vector2,
        aim_direction: pygame.Vector2,
        target_centers: list[pygame.Vector2],
    ) -> AimAssistTarget | None:
        normalized = self._normalize_direction(aim_direction)
        max_angle = max(1.0, float(self.config.cone_degrees))
        max_distance = max(1.0, float(self.config.max_distance))
        cosine_threshold = cos(radians(max_angle))

        candidates: list[AimAssistTarget] = []
        for center in target_centers:
            offset = pygame.Vector2(center) - origin
            distance = offset.length()
            if distance <= 0.001 or distance > max_distance:
                continue
            direction = offset / distance
            dot = max(-1.0, min(1.0, normalized.dot(direction)))
            if dot < cosine_threshold:
                continue
            angle = normalized.angle_to(direction)
            angle_abs = abs(float(angle))
            if angle_abs > max_angle:
                continue
            candidates.append(AimAssistTarget(center=pygame.Vector2(center), distance=distance, angle_degrees=angle_abs))
        if not candidates:
            return None
        candidates.sort(key=lambda c: (c.distance, c.angle_degrees))
        return candidates[0]

    def _assist_factor(self, distance: float, angle_degrees: float) -> float:
        max_angle = max(1.0, float(self.config.cone_degrees))
        max_distance = max(1.0, float(self.config.max_distance))
        distance_factor = max(0.0, 1.0 - (distance / max_distance))
        angle_factor = max(0.0, 1.0 - (angle_degrees / max_angle))
        base = max(0.0, min(float(self.config.assist_strength), 1.0))
        return max(0.0, min(base * distance_factor * angle_factor, base))

    def _normalize_direction(self, aim_direction: pygame.Vector2) -> pygame.Vector2:
        direction = pygame.Vector2(aim_direction)
        if direction.length_squared() <= 0.0:
            return pygame.Vector2(1.0, 0.0)
        return direction.normalize()
