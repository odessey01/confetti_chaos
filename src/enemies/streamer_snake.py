"""Streamer snake enemy composed of a head and trailing body segments."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import pygame

from .hazard import Hazard


@dataclass(frozen=True)
class SnakeBehaviorProfile:
    variant_id: str
    chase_weight: float
    drift_weight: float
    retarget_interval: float
    turn_response: float
    loop_strength: float


class StreamerSnake(Hazard):
    VARIANT_PROFILES: dict[str, SnakeBehaviorProfile] = {
        "wanderer": SnakeBehaviorProfile(
            variant_id="wanderer",
            chase_weight=0.55,
            drift_weight=0.45,
            retarget_interval=0.34,
            turn_response=4.7,
            loop_strength=0.0,
        ),
        "tracker": SnakeBehaviorProfile(
            variant_id="tracker",
            chase_weight=0.86,
            drift_weight=0.14,
            retarget_interval=0.19,
            turn_response=6.1,
            loop_strength=0.0,
        ),
        "looper": SnakeBehaviorProfile(
            variant_id="looper",
            chase_weight=0.52,
            drift_weight=0.48,
            retarget_interval=0.24,
            turn_response=5.0,
            loop_strength=18.0,
        ),
    }

    def __init__(
        self,
        size: int = 54,
        speed: float = 145.0,
        *,
        segment_count: int = 7,
        segment_spacing: float = 18.0,
        variant_id: str = "wanderer",
    ) -> None:
        super().__init__(size=size, speed=speed)
        self.base_speed = speed
        self.color = (255, 150, 90)
        self.segment_count = max(3, int(segment_count))
        self.segment_spacing = max(8.0, float(segment_spacing))
        self.segment_radius = max(4, int(size * 0.18))
        self._head_center = pygame.Vector2(0.0, 0.0)
        self._segment_centers = [pygame.Vector2(0.0, 0.0) for _ in range(self.segment_count)]
        self._path_points: list[pygame.Vector2] = [pygame.Vector2(0.0, 0.0)]
        self._desired_velocity = pygame.Vector2(0.0, 0.0)
        self.retarget_interval = 0.25
        self.retarget_timer = 0.0
        self.turn_response = 5.4
        self._drift_sign = 1.0
        self._drift_timer = random.uniform(0.45, 1.0)
        self._tail_history_segments = self.segment_count + 3
        self.body_collision_radius_scale = 0.78
        self.variant_id = "wanderer"
        self._behavior_profile = self.VARIANT_PROFILES["wanderer"]
        self.configure_variant(variant_id)

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        super().launch_toward_target(spawn, target_center)
        self._head_center = pygame.Vector2(self.rect.center)
        self._segment_centers = [pygame.Vector2(self._head_center) for _ in range(self.segment_count)]
        self._path_points = [pygame.Vector2(self._head_center)]
        self._desired_velocity = pygame.Vector2(self.velocity)
        self.retarget_timer = 0.0

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        if target_center is not None:
            self.retarget_timer -= delta_seconds
            if self.retarget_timer <= 0.0:
                self.retarget_timer = self.retarget_interval
                self._drift_timer -= delta_seconds
                if self._drift_timer <= 0.0:
                    self._drift_timer = random.uniform(0.45, 1.0)
                    self._drift_sign *= -1.0
                self._desired_velocity = self._compute_desired_velocity(target_center)
            blend = min(max(delta_seconds * self.turn_response, 0.0), 1.0)
            self.velocity = self.velocity.lerp(self._desired_velocity, blend)
            if self.velocity.length_squared() > 0.0:
                self.velocity = self.velocity.normalize() * self.base_speed
        self.position += self.velocity * delta_seconds
        self._head_center = pygame.Vector2(self.rect.center)
        self._record_path_point(self._head_center)

        if not self._segment_centers:
            return
        for idx in range(len(self._segment_centers)):
            follow_distance = (idx + 1) * self.segment_spacing
            self._segment_centers[idx] = self._point_at_path_distance(follow_distance)

    def segment_centers(self) -> list[pygame.Vector2]:
        return [pygame.Vector2(point) for point in self._segment_centers]

    def collides_with_rect(self, target_rect: pygame.Rect) -> bool:
        if self.rect.colliderect(target_rect):
            return True
        for idx, center in enumerate(self._segment_centers):
            ratio = max(0.25, 1.0 - (idx * 0.1))
            radius = max(2, int(self.segment_radius * ratio * self.body_collision_radius_scale))
            if _rect_collides_circle(target_rect, center, radius):
                return True
        return False

    def configure_variant(self, variant_id: str) -> None:
        profile = self.VARIANT_PROFILES.get(str(variant_id), self.VARIANT_PROFILES["wanderer"])
        self.variant_id = profile.variant_id
        self._behavior_profile = profile
        self.retarget_interval = profile.retarget_interval
        self.turn_response = profile.turn_response

    def draw(self, surface: pygame.Surface) -> None:
        head_center = (int(self._head_center.x), int(self._head_center.y))
        points = [self._head_center] + self._segment_centers
        for idx in range(len(points) - 1):
            start = points[idx]
            end = points[idx + 1]
            width = max(2, int(self.segment_radius * (1.15 - (idx * 0.08))))
            gradient = min(1.0, idx / max(1, len(points) - 2))
            ribbon_color = _lerp_color((255, 235, 120), (255, 150, 95), gradient)
            pygame.draw.line(
                surface,
                ribbon_color,
                (int(start.x), int(start.y)),
                (int(end.x), int(end.y)),
                width,
            )
        pygame.draw.circle(surface, self.color, head_center, max(9, self.size // 2))
        pygame.draw.circle(surface, (255, 245, 235), head_center, max(9, self.size // 2), 2)
        for idx, center in enumerate(self._segment_centers):
            ratio = max(0.25, 1.0 - (idx * 0.1))
            radius = max(3, int(self.segment_radius * ratio))
            gradient = min(1.0, idx / max(1, len(self._segment_centers) - 1))
            segment_color = _lerp_color((255, 220, 110), (250, 125, 95), gradient)
            pygame.draw.circle(
                surface,
                segment_color,
                (int(center.x), int(center.y)),
                radius,
            )

    def _behavior_snapshot(self) -> dict[str, Any]:
        return {
            "segment_count": self.segment_count,
            "segment_spacing": self.segment_spacing,
            "retarget_interval": self.retarget_interval,
            "turn_response": self.turn_response,
            "variant_id": self.variant_id,
        }

    def _compute_desired_velocity(self, target_center: pygame.Vector2) -> pygame.Vector2:
        center = pygame.Vector2(self.rect.center)
        to_target = target_center - center
        if to_target.length_squared() <= 0.0:
            if self.velocity.length_squared() > 0.0:
                return self.velocity.normalize() * self.base_speed
            return pygame.Vector2(1.0, 0.0) * self.base_speed
        chase_dir = to_target.normalize()
        drift_dir = pygame.Vector2(-chase_dir.y, chase_dir.x) * self._drift_sign
        desired_dir = (
            (chase_dir * self._behavior_profile.chase_weight)
            + (drift_dir * self._behavior_profile.drift_weight)
        )
        if self._behavior_profile.loop_strength > 0.0:
            desired_dir = desired_dir.rotate(self._behavior_profile.loop_strength * self._drift_sign)
        if desired_dir.length_squared() <= 0.0:
            desired_dir = chase_dir
        return desired_dir.normalize() * self.base_speed

    def _record_path_point(self, head_center: pygame.Vector2) -> None:
        if not self._path_points:
            self._path_points = [pygame.Vector2(head_center)]
            return
        if self._path_points[0].distance_to(head_center) >= 1.0:
            self._path_points.insert(0, pygame.Vector2(head_center))
        max_tail_length = self.max_tail_length
        consumed = 0.0
        keep_until = len(self._path_points)
        for idx in range(len(self._path_points) - 1):
            consumed += self._path_points[idx].distance_to(self._path_points[idx + 1])
            if consumed > max_tail_length:
                keep_until = idx + 2
                break
        if keep_until < len(self._path_points):
            self._path_points = self._path_points[:keep_until]

    def _point_at_path_distance(self, distance: float) -> pygame.Vector2:
        if not self._path_points:
            return pygame.Vector2(self._head_center)
        remaining = max(0.0, float(distance))
        for idx in range(len(self._path_points) - 1):
            start = self._path_points[idx]
            end = self._path_points[idx + 1]
            segment_length = start.distance_to(end)
            if segment_length <= 0.0:
                continue
            if remaining <= segment_length:
                t = remaining / segment_length
                return start.lerp(end, t)
            remaining -= segment_length
        return pygame.Vector2(self._path_points[-1])

    @property
    def max_tail_length(self) -> float:
        return self._tail_history_segments * self.segment_spacing


def _rect_collides_circle(rect: pygame.Rect, center: pygame.Vector2, radius: float) -> bool:
    closest_x = max(rect.left, min(center.x, rect.right))
    closest_y = max(rect.top, min(center.y, rect.bottom))
    dx = center.x - closest_x
    dy = center.y - closest_y
    return (dx * dx) + (dy * dy) <= (radius * radius)


def _lerp_color(start: tuple[int, int, int], end: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    clamped = min(1.0, max(0.0, float(t)))
    return (
        int(start[0] + ((end[0] - start[0]) * clamped)),
        int(start[1] + ((end[1] - start[1]) * clamped)),
        int(start[2] + ((end[2] - start[2]) * clamped)),
    )
