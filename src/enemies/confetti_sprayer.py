"""Confetti sprayer enemy with a readable cannon-like facing direction."""

from __future__ import annotations

import math
from typing import Any

import pygame

from .hazard import Hazard


class ConfettiSprayer(Hazard):
    def __init__(self, size: int = 62, speed: float = 135.0) -> None:
        super().__init__(size=size, speed=speed)
        self.base_speed = speed
        self.color = (85, 225, 170)
        self.accent_color = (250, 250, 210)
        self.nozzle_color = (60, 80, 95)
        self._facing = pygame.Vector2(1.0, 0.0)
        self.preferred_distance = 260.0
        self.distance_tolerance = 75.0
        self.retarget_interval = 0.7
        self.retarget_timer = 0.0
        self.turn_response = 4.2
        self._desired_velocity = pygame.Vector2(0.0, 0.0)
        self._orbit_sign = 1.0
        self.attack_cooldown = 2.0
        self.attack_cooldown_timer = 1.1
        self.charge_duration = 0.35
        self.charge_timer = 0.0
        self.is_charging = False
        self.spray_projectile_count = 5
        self.spray_angle = 55.0
        self.spray_projectile_speed = 320.0
        self._pending_spray_burst: dict[str, object] | None = None
        self._pending_charge_started = False
        self._charge_facing = pygame.Vector2(1.0, 0.0)
        self.release_flash_duration = 0.14
        self.release_flash_timer = 0.0

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        super().launch_toward_target(spawn, target_center)
        if self.velocity.length_squared() > 0.0:
            self._facing = self.velocity.normalize()
            self._desired_velocity = self.velocity
        self.retarget_timer = 0.0
        self.is_charging = False
        self.charge_timer = 0.0
        self.attack_cooldown_timer = min(self.attack_cooldown_timer, self.attack_cooldown)

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self.release_flash_timer = max(0.0, self.release_flash_timer - delta_seconds)
        if target_center is not None:
            self.attack_cooldown_timer = max(0.0, self.attack_cooldown_timer - delta_seconds)
            if self.is_charging:
                self.charge_timer = max(0.0, self.charge_timer - delta_seconds)
                slow_blend = min(max(delta_seconds * 7.0, 0.0), 1.0)
                self.velocity = self.velocity.lerp(pygame.Vector2(0.0, 0.0), slow_blend)
                if self.charge_timer <= 0.0:
                    self.is_charging = False
                    self._queue_spray_burst()
                    self.attack_cooldown_timer = self.attack_cooldown
            elif self.attack_cooldown_timer <= 0.0:
                self.is_charging = True
                self.charge_timer = self.charge_duration
                self._charge_facing = self._facing if self._facing.length_squared() > 0.0 else pygame.Vector2(1.0, 0.0)
                self._pending_charge_started = True

            if not self.is_charging:
                self.retarget_timer -= delta_seconds
                if self.retarget_timer <= 0.0:
                    self.retarget_timer = self.retarget_interval
                    self._desired_velocity = self._compute_desired_velocity(target_center)
                    self._orbit_sign *= -1.0
                blend = min(max(delta_seconds * self.turn_response, 0.0), 1.0)
                self.velocity = self.velocity.lerp(self._desired_velocity, blend)
                if self.velocity.length_squared() > 0.0:
                    self.velocity = self.velocity.normalize() * self.base_speed

        self.position += self.velocity * delta_seconds
        if self.is_charging:
            self._facing = self._charge_facing.normalize()
        elif self.velocity.length_squared() > 0.0:
            self._facing = self.velocity.normalize()

    def consume_attack_cues(self) -> dict[str, object]:
        cues = self._pending_spray_burst or {
            "spray_fired": False,
            "origin": pygame.Vector2(self.rect.center),
            "directions": [],
            "projectile_speed": self.spray_projectile_speed,
        }
        cues["charge_started"] = self._pending_charge_started
        self._pending_charge_started = False
        self._pending_spray_burst = None
        return cues

    def configure_attack_profile(
        self,
        *,
        cooldown: float,
        spray_angle: float,
        projectile_count: int,
        projectile_speed: float,
    ) -> None:
        self.attack_cooldown = max(0.6, float(cooldown))
        self.spray_angle = max(10.0, float(spray_angle))
        self.spray_projectile_count = max(1, int(projectile_count))
        self.spray_projectile_speed = max(120.0, float(projectile_speed))

    def _queue_spray_burst(self) -> None:
        facing = self._charge_facing if self._charge_facing.length_squared() > 0.0 else self._facing
        if facing.length_squared() <= 0.0:
            facing = pygame.Vector2(1.0, 0.0)
        facing = facing.normalize()
        directions: list[pygame.Vector2] = []
        count = max(1, int(self.spray_projectile_count))
        spread = max(0.0, float(self.spray_angle))
        for i in range(count):
            if count == 1:
                angle = 0.0
            else:
                angle = -spread / 2.0 + (spread * (i / (count - 1)))
            directions.append(facing.rotate(angle))
        self._pending_spray_burst = {
            "spray_fired": True,
            "origin": pygame.Vector2(self.rect.center),
            "directions": directions,
            "projectile_speed": self.spray_projectile_speed,
        }
        self.release_flash_timer = self.release_flash_duration

    def _compute_desired_velocity(self, target_center: pygame.Vector2) -> pygame.Vector2:
        center = pygame.Vector2(self.rect.center)
        to_player = target_center - center
        if to_player.length_squared() <= 0.0:
            return pygame.Vector2(1.0, 0.0) * self.base_speed
        distance = to_player.length()
        direction_to_player = to_player.normalize()
        strafe = pygame.Vector2(-direction_to_player.y, direction_to_player.x) * self._orbit_sign

        if distance > self.preferred_distance + self.distance_tolerance:
            desired_dir = direction_to_player
        elif distance < self.preferred_distance - self.distance_tolerance:
            desired_dir = -direction_to_player
        else:
            desired_dir = (strafe * 0.78) + (direction_to_player * 0.22)
            if desired_dir.length_squared() > 0.0:
                desired_dir = desired_dir.normalize()
            else:
                desired_dir = strafe
        return desired_dir * self.base_speed

    def draw(self, surface: pygame.Surface) -> None:
        center = pygame.Vector2(self.rect.center)
        radius = max(10.0, self.size / 2.0)
        facing = self._facing if self._facing.length_squared() > 0.0 else pygame.Vector2(1.0, 0.0)
        facing = facing.normalize()
        side = pygame.Vector2(-facing.y, facing.x)

        rear = center - (facing * (radius * 0.55))
        body_front = center + (facing * (radius * 0.25))
        body_half_width = radius * 0.45
        body_points = [
            rear - (side * body_half_width),
            rear + (side * body_half_width),
            body_front + (side * body_half_width),
            body_front - (side * body_half_width),
        ]
        body_color = (255, 240, 180) if self.is_charging else self.color
        pygame.draw.polygon(surface, body_color, body_points)
        pygame.draw.polygon(surface, (245, 250, 240), body_points, width=2)

        nozzle_base = body_front
        nozzle_tip = nozzle_base + (facing * (radius * 0.85))
        nozzle_half_width = radius * 0.22
        nozzle_points = [
            nozzle_base - (side * nozzle_half_width),
            nozzle_base + (side * nozzle_half_width),
            nozzle_tip + (side * (nozzle_half_width * 0.6)),
            nozzle_tip - (side * (nozzle_half_width * 0.6)),
        ]
        pygame.draw.polygon(surface, self.nozzle_color, nozzle_points)

        ring_center = center - (facing * (radius * 0.12))
        ring_radius = max(6, int(radius * 0.22))
        pygame.draw.circle(
            surface,
            self.accent_color,
            (int(ring_center.x), int(ring_center.y)),
            ring_radius,
            width=2,
        )

        nozzle_opening_center = nozzle_tip + (facing * 1.5)
        nozzle_fill = (250, 245, 165) if self.release_flash_timer > 0.0 else (35, 45, 55)
        pygame.draw.circle(
            surface,
            nozzle_fill,
            (int(nozzle_opening_center.x), int(nozzle_opening_center.y)),
            max(3, int(radius * 0.12)),
        )

    def _behavior_snapshot(self) -> dict[str, Any]:
        facing_angle = math.degrees(math.atan2(self._facing.y, self._facing.x))
        return {
            "facing_angle": facing_angle,
            "preferred_distance": self.preferred_distance,
            "distance_tolerance": self.distance_tolerance,
            "attack_cooldown": self.attack_cooldown,
            "spray_angle": self.spray_angle,
            "spray_projectile_count": self.spray_projectile_count,
            "spray_projectile_speed": self.spray_projectile_speed,
        }
