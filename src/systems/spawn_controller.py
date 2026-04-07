"""Centralized hazard spawning logic with fairness constraints."""

from __future__ import annotations

import random
from collections import Counter, deque
from dataclasses import dataclass
from typing import Protocol

import pygame

from enemies import BalloonEnemy, BossBalloon, Hazard, TrackingHazard


class RandomLike(Protocol):
    def choice(self, seq: tuple[str, ...] | list[str]) -> str:
        ...

    def random(self) -> float:
        ...

    def uniform(self, a: float, b: float) -> float:
        ...


@dataclass(frozen=True)
class EnemySpawnProfile:
    tier: int
    speed: float
    health: int
    movement_profile: str
    flavor_tag: str
    enemy_kind: str


class SpawnController:
    def __init__(
        self,
        bounds: pygame.Rect,
        *,
        initial_hazards: int = 1,
        max_hazards: int = 6,
        base_spawn_interval: float = 2.2,
        min_spawn_interval: float = 0.75,
        safe_spawn_distance: float = 220.0,
        tracking_spawn_chance: float = 0.35,
        balloon_spawn_chance: float = 0.35,
        tier_weight_template: dict[str, float] | None = None,
        older_tier_decay_start_level: int = 8,
        older_tier_retire_level: int = 16,
        previous_tier_decay_start_level: int = 14,
        previous_tier_retire_level: int = 24,
        telemetry_enabled: bool = True,
        max_telemetry_events: int = 180,
        rng: RandomLike | None = None,
    ) -> None:
        self.bounds = bounds
        self.initial_hazards = initial_hazards
        self.max_hazards = max_hazards
        self.base_spawn_interval = base_spawn_interval
        self.min_spawn_interval = min_spawn_interval
        self.safe_spawn_distance = safe_spawn_distance
        self.tracking_spawn_chance = tracking_spawn_chance
        self.balloon_spawn_chance = balloon_spawn_chance
        self.tier_weight_template = self._normalize_tier_weight_template(tier_weight_template)
        self.older_tier_decay_start_level = older_tier_decay_start_level
        self.older_tier_retire_level = older_tier_retire_level
        self.previous_tier_decay_start_level = previous_tier_decay_start_level
        self.previous_tier_retire_level = previous_tier_retire_level
        self.telemetry_enabled = telemetry_enabled
        self._spawn_telemetry: deque[dict[str, object]] = deque(maxlen=max_telemetry_events)
        self._rng = rng if rng is not None else random.Random()
        self._spawn_timer = 0.0

    def reset(self) -> None:
        self._spawn_timer = 0.0
        self._spawn_telemetry.clear()

    def set_tracking_chance(self, chance: float) -> None:
        """Set the probability of spawning a tracking hazard."""
        self.tracking_spawn_chance = max(0.0, min(chance, 1.0))

    def set_balloon_chance(self, chance: float) -> None:
        """Set the probability of spawning a balloon enemy."""
        self.balloon_spawn_chance = max(0.0, min(chance, 1.0))

    def spawn_count_for_frame(
        self,
        delta_seconds: float,
        difficulty_multiplier: float,
        active_hazard_count: int,
        spawn_rate_multiplier: float = 1.0,
    ) -> int:
        self._spawn_timer += delta_seconds
        interval = self.current_spawn_interval(difficulty_multiplier, spawn_rate_multiplier)

        spawn_count = 0
        while (
            self._spawn_timer >= interval
            and active_hazard_count + spawn_count < self.max_hazards
        ):
            self._spawn_timer -= interval
            spawn_count += 1
        return spawn_count

    def current_spawn_interval(self, difficulty_multiplier: float, spawn_rate_multiplier: float = 1.0) -> float:
        combined_multiplier = max(difficulty_multiplier * spawn_rate_multiplier, 1.0)
        interval = self.base_spawn_interval / combined_multiplier
        return max(self.min_spawn_interval, interval)

    def configure_hazard(
        self,
        hazard: Hazard,
        player_center: pygame.Vector2,
    ) -> None:
        spawn = self.sample_spawn_position(player_center, hazard.size)
        hazard.launch_toward_target(spawn, player_center)

    def create_hazard(self, speed: float) -> Hazard:
        return self.create_hazard_for_spawn(
            tier=1,
            base_speed=speed,
            flavor_tag="STANDARD",
        )

    def create_boss_hazard(self, speed: float) -> BossBalloon:
        """Create a boss balloon enemy."""
        return self.create_boss_hazard_for_spawn(
            tier=1,
            base_speed=speed,
            flavor_tag="STANDARD",
        )

    def create_hazard_for_spawn(self, *, tier: int, base_speed: float, flavor_tag: str) -> Hazard:
        return self.create_hazard_for_spawn_with_chances(
            tier=tier,
            base_speed=base_speed,
            flavor_tag=flavor_tag,
            tracking_chance=self.tracking_spawn_chance,
        )

    def create_hazard_for_spawn_with_chances(
        self,
        *,
        tier: int,
        base_speed: float,
        flavor_tag: str,
        tracking_chance: float,
    ) -> Hazard:
        roll = self._rng.random()
        if roll < max(0.0, min(tracking_chance, 1.0)):
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * 0.7,
                health=1,
                movement_profile="tracking_homing",
                flavor_tag=flavor_tag,
                enemy_kind="tracking",
            )
            hazard = TrackingHazard(speed=profile.speed)
        else:
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * 0.75,
                health=1,
                movement_profile="balloon_drift",
                flavor_tag=flavor_tag,
                enemy_kind="balloon",
            )
            hazard = BalloonEnemy(speed=profile.speed)
        hazard.apply_spawn_profile(self._profile_to_dict(profile))
        return hazard

    def create_boss_hazard_for_spawn(self, *, tier: int, base_speed: float, flavor_tag: str) -> BossBalloon:
        profile = EnemySpawnProfile(
            tier=tier,
            speed=base_speed * 0.5,
            health=3,
            movement_profile="boss_charge",
            flavor_tag=flavor_tag,
            enemy_kind="boss_balloon",
        )
        boss = BossBalloon(speed=profile.speed)
        boss.apply_spawn_profile(self._profile_to_dict(profile))
        return boss

    def select_spawn_tier(self, current_level: int) -> int:
        pool = self._tier_pool_for_level(current_level)
        total_weight = sum(weight for _, weight in pool)
        if total_weight <= 0.0:
            return max(1, current_level)
        roll = self._rng.random() * total_weight
        cumulative = 0.0
        for tier, weight in pool:
            cumulative += weight
            if roll <= cumulative:
                return tier
        return pool[-1][0]

    def _tier_pool_for_level(self, current_level: int) -> list[tuple[int, float]]:
        level = max(1, current_level)
        weights = self._effective_tier_weights(level)
        newest = weights["newest"]
        previous = weights["previous"]
        older = weights["older"]
        if level == 1:
            return [(1, 1.0)]
        if level == 2:
            return [(2, newest), (1, previous + older)]
        pool = [(level, newest), (level - 1, previous), (level - 2, older)]
        return [(tier, weight) for tier, weight in pool if weight > 0.0]

    def _profile_to_dict(self, profile: EnemySpawnProfile) -> dict[str, object]:
        return {
            "tier": profile.tier,
            "speed": profile.speed,
            "health": profile.health,
            "movement_profile": profile.movement_profile,
            "flavor_tag": profile.flavor_tag,
            "enemy_kind": profile.enemy_kind,
        }

    def _normalize_tier_weight_template(
        self,
        template: dict[str, float] | None,
    ) -> dict[str, float]:
        source = template or {"newest": 0.55, "previous": 0.30, "older": 0.15}
        newest = max(0.0, float(source.get("newest", 0.55)))
        previous = max(0.0, float(source.get("previous", 0.30)))
        older = max(0.0, float(source.get("older", 0.15)))
        total = newest + previous + older
        if total <= 0.0:
            return {"newest": 1.0, "previous": 0.0, "older": 0.0}
        return {
            "newest": newest / total,
            "previous": previous / total,
            "older": older / total,
        }

    def _effective_tier_weights(self, level: int) -> dict[str, float]:
        newest = self.tier_weight_template["newest"]
        previous = self.tier_weight_template["previous"]
        older = self.tier_weight_template["older"]

        older *= self._decay_factor(
            level=level,
            start_level=self.older_tier_decay_start_level,
            retire_level=self.older_tier_retire_level,
        )
        previous *= self._decay_factor(
            level=level,
            start_level=self.previous_tier_decay_start_level,
            retire_level=self.previous_tier_retire_level,
        )

        total = newest + previous + older
        if total <= 0.0:
            return {"newest": 1.0, "previous": 0.0, "older": 0.0}
        return {
            "newest": newest / total,
            "previous": previous / total,
            "older": older / total,
        }

    def _decay_factor(self, *, level: int, start_level: int, retire_level: int) -> float:
        if level < start_level:
            return 1.0
        if level >= retire_level:
            return 0.0
        span = max(1, retire_level - start_level)
        progressed = level - start_level
        return max(0.0, 1.0 - (progressed / span))

    def record_spawn_event(
        self,
        *,
        current_level: int,
        active_flavor: str,
        spawn_tier: int,
        enemy_kind: str,
        boss_override_active: bool,
    ) -> None:
        if not self.telemetry_enabled:
            return
        self._spawn_telemetry.append(
            {
                "current_level": int(current_level),
                "active_flavor": str(active_flavor),
                "spawn_tier": int(spawn_tier),
                "enemy_kind": str(enemy_kind),
                "boss_override_active": bool(boss_override_active),
            }
        )

    def spawn_telemetry_summary(self, limit: int = 60) -> dict[str, object]:
        if limit <= 0:
            return {
                "events_considered": 0,
                "tier_distribution": {},
                "enemy_kind_distribution": {},
                "boss_override_events": 0,
            }
        events = list(self._spawn_telemetry)[-limit:]
        tier_counts: Counter[int] = Counter(int(event["spawn_tier"]) for event in events)
        kind_counts: Counter[str] = Counter(str(event["enemy_kind"]) for event in events)
        total = len(events)
        tier_distribution = (
            {tier: count / total for tier, count in sorted(tier_counts.items())}
            if total > 0
            else {}
        )
        enemy_kind_distribution = (
            {kind: count / total for kind, count in sorted(kind_counts.items())}
            if total > 0
            else {}
        )
        boss_override_events = sum(
            1 for event in events if bool(event["boss_override_active"])
        )
        return {
            "events_considered": total,
            "tier_distribution": tier_distribution,
            "enemy_kind_distribution": enemy_kind_distribution,
            "boss_override_events": boss_override_events,
        }

    def sample_spawn_position(
        self,
        player_center: pygame.Vector2,
        hazard_size: int,
    ) -> pygame.Vector2:
        for _ in range(24):
            spawn = self._random_edge_spawn(hazard_size)
            if spawn.distance_to(player_center) >= self.safe_spawn_distance + (hazard_size / 2):
                return spawn
        return self._farthest_edge_spawn(player_center, hazard_size)

    def _random_edge_spawn(self, hazard_size: int) -> pygame.Vector2:
        side = self._rng.choice(("left", "right", "top", "bottom"))
        max_x = max(self.bounds.width - hazard_size, 0)
        max_y = max(self.bounds.height - hazard_size, 0)

        if side == "left":
            return pygame.Vector2(-hazard_size, self._rng.uniform(0, max_y))
        if side == "right":
            return pygame.Vector2(self.bounds.width, self._rng.uniform(0, max_y))
        if side == "top":
            return pygame.Vector2(self._rng.uniform(0, max_x), -hazard_size)
        return pygame.Vector2(self._rng.uniform(0, max_x), self.bounds.height)

    def _farthest_edge_spawn(
        self,
        player_center: pygame.Vector2,
        hazard_size: int,
    ) -> pygame.Vector2:
        max_x = max(self.bounds.width - hazard_size, 0)
        max_y = max(self.bounds.height - hazard_size, 0)

        candidates = [
            pygame.Vector2(-hazard_size, max_y / 2),
            pygame.Vector2(self.bounds.width, max_y / 2),
            pygame.Vector2(max_x / 2, -hazard_size),
            pygame.Vector2(max_x / 2, self.bounds.height),
        ]
        return max(candidates, key=lambda point: point.distance_to(player_center))
