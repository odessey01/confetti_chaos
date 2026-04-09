"""Boss balloon enemy - large, durable enemy that appears on milestone levels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pygame

from .hazard import Hazard


@dataclass(frozen=True)
class BossVariantProfile:
    max_health: int
    damage_per_hit: int
    charge_duration: float
    charge_speed_multiplier: float
    max_speed_cap: float
    chase_speed_factor: float
    retarget_interval: float
    turn_response: float
    speed_surge_multiplier: float
    speed_surge_duration: float
    speed_surge_cooldown: float
    directional_charge_multiplier: float
    directional_charge_duration: float
    directional_charge_cooldown: float
    burst_spawn_cooldown: float
    burst_spawn_count: int
    phase_speed_multipliers: tuple[float, float, float]
    phase_turn_multipliers: tuple[float, float, float]
    phase_cooldown_multipliers: tuple[float, float, float]


BOSS_VARIANT_PROFILES: dict[str, BossVariantProfile] = {
    "classic": BossVariantProfile(
        max_health=5,
        damage_per_hit=1,
        charge_duration=1.5,
        charge_speed_multiplier=1.35,
        max_speed_cap=350.0,
        chase_speed_factor=0.72,
        retarget_interval=0.32,
        turn_response=3.2,
        speed_surge_multiplier=1.2,
        speed_surge_duration=1.0,
        speed_surge_cooldown=6.0,
        directional_charge_multiplier=1.4,
        directional_charge_duration=0.35,
        directional_charge_cooldown=7.2,
        burst_spawn_cooldown=8.0,
        burst_spawn_count=1,
        phase_speed_multipliers=(1.0, 1.08, 1.16),
        phase_turn_multipliers=(1.0, 1.06, 1.12),
        phase_cooldown_multipliers=(1.0, 0.92, 0.84),
    ),
    "bulwark": BossVariantProfile(
        max_health=7,
        damage_per_hit=1,
        charge_duration=1.7,
        charge_speed_multiplier=1.25,
        max_speed_cap=320.0,
        chase_speed_factor=0.66,
        retarget_interval=0.36,
        turn_response=2.8,
        speed_surge_multiplier=1.15,
        speed_surge_duration=1.1,
        speed_surge_cooldown=6.5,
        directional_charge_multiplier=1.3,
        directional_charge_duration=0.32,
        directional_charge_cooldown=7.8,
        burst_spawn_cooldown=7.0,
        burst_spawn_count=2,
        phase_speed_multipliers=(1.0, 1.06, 1.12),
        phase_turn_multipliers=(1.0, 1.05, 1.1),
        phase_cooldown_multipliers=(1.0, 0.9, 0.82),
    ),
}


class BossBalloon(Hazard):
    """A large, durable balloon enemy that requires multiple hits to defeat."""

    @staticmethod
    def resolve_profile(profile_id: str) -> tuple[str, BossVariantProfile]:
        if profile_id in BOSS_VARIANT_PROFILES:
            return profile_id, BOSS_VARIANT_PROFILES[profile_id]
        return "classic", BOSS_VARIANT_PROFILES["classic"]

    def __init__(
        self,
        speed: float,
        *,
        profile_id: str = "classic",
        max_health: int | None = None,
        damage_per_hit: int | None = None,
        size: int = 136,
    ) -> None:
        super().__init__(size, speed)
        self.profile_id, profile = self.resolve_profile(profile_id)
        self.max_health = max(1, int(profile.max_health if max_health is None else max_health))
        self.damage_per_hit = max(
            1,
            int(profile.damage_per_hit if damage_per_hit is None else damage_per_hit),
        )
        self.health = self.max_health
        self.color = (255, 100, 100)  # Red color to distinguish from normal balloons
        self.outline_color = (255, 215, 0)  # Gold outline
        
        # Charge burst behavior
        self.charge_timer = 0.0
        self.is_charging = False
        self.charge_duration = profile.charge_duration
        self.charge_speed_multiplier = profile.charge_speed_multiplier
        self.charge_color = (255, 50, 50)  # Bright red during charge
        self.max_speed_cap = profile.max_speed_cap

        # Deliberate chase behavior
        self.chase_speed_factor = profile.chase_speed_factor
        self.retarget_interval = profile.retarget_interval
        self.turn_response = profile.turn_response
        self._retarget_timer = 0.0
        self._desired_velocity = pygame.Vector2(0, 0)

        # Multi-hit feedback and duplicate-hit protection.
        self.hit_invuln_duration = 0.12
        self.hit_invuln_timer = 0.0
        self.hit_flash_duration = 0.10
        self.hit_flash_timer = 0.0
        self.hit_wobble_duration = 0.16
        self.hit_wobble_timer = 0.0

        # Ability pattern state (Task 55).
        self.speed_surge_multiplier = profile.speed_surge_multiplier
        self.speed_surge_duration = profile.speed_surge_duration
        self.speed_surge_cooldown = profile.speed_surge_cooldown
        self._speed_surge_timer = 0.0
        self._speed_surge_cooldown_timer = self.speed_surge_cooldown
        self._speed_surge_triggered = False

        self.directional_charge_multiplier = profile.directional_charge_multiplier
        self.directional_charge_duration = profile.directional_charge_duration
        self.directional_charge_cooldown = profile.directional_charge_cooldown
        self._directional_charge_timer = 0.0
        self._directional_charge_cooldown_timer = self.directional_charge_cooldown
        self._directional_charge_triggered = False

        self.burst_spawn_cooldown = profile.burst_spawn_cooldown
        self.burst_spawn_count = profile.burst_spawn_count
        self._burst_spawn_cooldown_timer = self.burst_spawn_cooldown
        self._pending_burst_spawn_count = 0

        # Phase escalation state (Task 56).
        self.current_phase = 1
        self._phase_speed_multipliers = profile.phase_speed_multipliers
        self._phase_turn_multipliers = profile.phase_turn_multipliers
        self._phase_cooldown_multipliers = profile.phase_cooldown_multipliers
        self._phase_changed_triggered = False
        self.phase_transition_flash_duration = 0.22
        self.phase_transition_flash_timer = 0.0

    def apply_hit(self) -> tuple[bool, bool]:
        """Apply one weapon hit. Returns (hit_registered, defeated)."""
        if self.hit_invuln_timer > 0.0 or self.health <= 0:
            return False, False

        self.health = max(0, self.health - self.damage_per_hit)
        self.hit_invuln_timer = self.hit_invuln_duration
        self.hit_flash_timer = self.hit_flash_duration
        self.hit_wobble_timer = self.hit_wobble_duration
        previous_phase = self.current_phase
        self.current_phase = self._phase_for_health(self.health)
        if self.current_phase > previous_phase:
            self._phase_changed_triggered = True
            self.phase_transition_flash_timer = self.phase_transition_flash_duration
        if self.health > 0:
            # Trigger charge burst
            self.is_charging = True
            self.charge_timer = self.charge_duration
            return True, False
        return True, True

    def _phase_for_health(self, health: int) -> int:
        if self.max_health <= 1:
            return 1
        ratio = health / self.max_health
        if ratio <= 0.34:
            return 3
        if ratio <= 0.67:
            return 2
        return 1

    def _phase_speed_multiplier(self) -> float:
        index = max(1, min(self.current_phase, 3)) - 1
        return self._phase_speed_multipliers[index]

    def _phase_turn_multiplier(self) -> float:
        index = max(1, min(self.current_phase, 3)) - 1
        return self._phase_turn_multipliers[index]

    def _phase_cooldown_multiplier(self) -> float:
        index = max(1, min(self.current_phase, 3)) - 1
        return self._phase_cooldown_multipliers[index]

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        """Update boss behavior including charge burst logic."""
        self.hit_invuln_timer = max(0.0, self.hit_invuln_timer - delta_seconds)
        self.hit_flash_timer = max(0.0, self.hit_flash_timer - delta_seconds)
        self.hit_wobble_timer = max(0.0, self.hit_wobble_timer - delta_seconds)
        self.phase_transition_flash_timer = max(0.0, self.phase_transition_flash_timer - delta_seconds)

        self._speed_surge_timer = max(0.0, self._speed_surge_timer - delta_seconds)
        self._speed_surge_cooldown_timer = max(0.0, self._speed_surge_cooldown_timer - delta_seconds)
        self._directional_charge_timer = max(0.0, self._directional_charge_timer - delta_seconds)
        self._directional_charge_cooldown_timer = max(0.0, self._directional_charge_cooldown_timer - delta_seconds)
        self._burst_spawn_cooldown_timer = max(0.0, self._burst_spawn_cooldown_timer - delta_seconds)

        cooldown_multiplier = self._phase_cooldown_multiplier()
        speed_surge_cooldown = self.speed_surge_cooldown * cooldown_multiplier
        directional_charge_cooldown = self.directional_charge_cooldown * cooldown_multiplier
        burst_spawn_cooldown = self.burst_spawn_cooldown * cooldown_multiplier

        if target_center is not None and self._speed_surge_cooldown_timer <= 0.0:
            self._speed_surge_timer = self.speed_surge_duration
            self._speed_surge_cooldown_timer = speed_surge_cooldown
            self._speed_surge_triggered = True

        if target_center is not None and self._directional_charge_cooldown_timer <= 0.0:
            self._directional_charge_timer = self.directional_charge_duration
            self._directional_charge_cooldown_timer = directional_charge_cooldown
            self._directional_charge_triggered = True
            center = pygame.Vector2(self.rect.center)
            to_target = target_center - center
            if to_target.length_squared() > 0:
                self._desired_velocity = to_target.normalize() * (
                    self.base_speed * self.chase_speed_factor * self.directional_charge_multiplier
                )

        if target_center is not None and self._burst_spawn_cooldown_timer <= 0.0:
            self._pending_burst_spawn_count += self.burst_spawn_count
            self._burst_spawn_cooldown_timer = burst_spawn_cooldown

        # Handle charge burst timer
        if self.is_charging:
            self.charge_timer -= delta_seconds
            if self.charge_timer <= 0:
                self.is_charging = False
                self.charge_timer = 0.0
        
        # Apply deliberate chase speed profile and optional charge burst.
        base_chase_speed = self.base_speed * self.chase_speed_factor * self._phase_speed_multiplier()
        speed_multiplier = 1.0
        if self.is_charging:
            speed_multiplier *= self.charge_speed_multiplier
        if self._speed_surge_timer > 0.0:
            speed_multiplier *= self.speed_surge_multiplier
        if self._directional_charge_timer > 0.0:
            speed_multiplier *= self.directional_charge_multiplier
        current_speed = base_chase_speed * speed_multiplier
        current_speed = min(current_speed, self.max_speed_cap)
        self.speed = current_speed

        # Reacquire target periodically instead of snapping every frame.
        self._retarget_timer += delta_seconds
        if (
            target_center is not None
            and self._directional_charge_timer <= 0.0
            and (
                self._retarget_timer >= self.retarget_interval
                or self._desired_velocity.length_squared() == 0
            )
        ):
            self._retarget_timer = 0.0
            center = pygame.Vector2(self.rect.center)
            to_target = target_center - center
            if to_target.length_squared() > 0:
                self._desired_velocity = to_target.normalize() * current_speed

        # Ease toward desired velocity so turns feel readable.
        if self._desired_velocity.length_squared() > 0:
            lerp_alpha = max(
                0.0,
                min(1.0, self.turn_response * self._phase_turn_multiplier() * delta_seconds),
            )
            self.velocity = self.velocity.lerp(self._desired_velocity, lerp_alpha)
            speed_sq = self.velocity.length_squared()
            if speed_sq > 0:
                max_speed = current_speed
                if speed_sq > (max_speed * max_speed):
                    self.velocity = self.velocity.normalize() * max_speed

        self.position += self.velocity * delta_seconds

    def consume_ability_cues(self) -> dict[str, int | bool]:
        cues = {
            "burst_spawn_count": self._pending_burst_spawn_count,
            "speed_surge_triggered": self._speed_surge_triggered,
            "directional_charge_triggered": self._directional_charge_triggered,
            "phase_changed": self._phase_changed_triggered,
            "current_phase": self.current_phase,
            "profile_id": self.profile_id,
        }
        self._pending_burst_spawn_count = 0
        self._speed_surge_triggered = False
        self._directional_charge_triggered = False
        self._phase_changed_triggered = False
        return cues

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the boss balloon with special visual effects."""
        # Flash color on hit; otherwise use charge color when charging.
        if self.phase_transition_flash_timer > 0.0:
            current_color = (255, 255, 180)
        elif self.hit_flash_timer > 0.0:
            current_color = (255, 240, 240)
        else:
            current_color = self.charge_color if self.is_charging else self.color
        wobble_scale = 1.0
        if self.hit_wobble_timer > 0.0:
            progress = 1.0 - (self.hit_wobble_timer / self.hit_wobble_duration)
            wobble_scale = 1.0 + 0.06 * (1.0 - progress)
        draw_radius = max(8, int((self.size // 2) * wobble_scale))
        
        # Draw main body
        pygame.draw.circle(surface, current_color, self.rect.center, draw_radius)
        # Draw gold outline
        pygame.draw.circle(surface, self.outline_color, self.rect.center, draw_radius, 3)
        # Draw health indicator (simple bars)
        bar_width = self.size
        bar_height = 6
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 10

        # Background bar
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Health bar
        health_width = (self.health / max(1, self.max_health)) * bar_width
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))

    def _behavior_snapshot(self) -> dict[str, Any]:
        return {
            "max_health": self.max_health,
            "damage_per_hit": self.damage_per_hit,
            "profile_id": self.profile_id,
            "charge_duration": self.charge_duration,
            "charge_speed_multiplier": self.charge_speed_multiplier,
            "max_speed_cap": self.max_speed_cap,
            "chase_speed_factor": self.chase_speed_factor,
            "retarget_interval": self.retarget_interval,
            "turn_response": self.turn_response,
            "speed_surge_multiplier": self.speed_surge_multiplier,
            "speed_surge_duration": self.speed_surge_duration,
            "speed_surge_cooldown": self.speed_surge_cooldown,
            "directional_charge_multiplier": self.directional_charge_multiplier,
            "directional_charge_duration": self.directional_charge_duration,
            "directional_charge_cooldown": self.directional_charge_cooldown,
            "burst_spawn_cooldown": self.burst_spawn_cooldown,
            "burst_spawn_count": self.burst_spawn_count,
            "current_phase": self.current_phase,
        }
