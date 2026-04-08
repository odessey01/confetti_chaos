"""Centralized hazard spawning logic with fairness constraints."""

from __future__ import annotations

import random
from collections import Counter, deque
from dataclasses import dataclass
from typing import Protocol

import pygame

from enemies import (
    BalloonEnemy,
    BossBalloon,
    ConfettiSprayer,
    Hazard,
    PinataEnemy,
    StreamerSnake,
    TrackingHazard,
)


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
    boss_variant_id: str | None = None
    break_confetti_count: int | None = None
    mini_spawn_count: int | None = None
    spray_cooldown: float | None = None
    spray_angle: float | None = None
    spray_projectile_count: int | None = None
    spray_projectile_speed: float | None = None
    snake_variant_id: str | None = None
    snake_segment_count: int | None = None
    snake_segment_spacing: float | None = None


@dataclass(frozen=True)
class PinataTierVariant:
    variant_id: str
    speed_multiplier: float
    health: int
    break_confetti_count: int
    mini_spawn_count: int


@dataclass(frozen=True)
class SprayerFlavorProfile:
    cooldown: float
    spray_angle: float
    projectile_count: int
    projectile_speed: float


@dataclass(frozen=True)
class SnakeFlavorProfile:
    variant_id: str
    segment_count: int
    segment_spacing: float
    speed_multiplier: float


class SpawnController:
    MIN_PINATA_CHANCE = 0.04
    MAX_PINATA_CHANCE = 0.26
    PINATA_RAMP_START_TIER = 3
    PINATA_RAMP_FULL_TIER = 12
    BOSS_PINATA_CHANCE_CAP = 0.08
    MIN_SPRAYER_CHANCE = 0.035
    MAX_SPRAYER_CHANCE = 0.22
    SPRAYER_RAMP_START_TIER = 2
    SPRAYER_RAMP_FULL_TIER = 10
    BOSS_SPRAYER_CHANCE_CAP = 0.08
    MIN_SNAKE_CHANCE = 0.0
    MAX_SNAKE_CHANCE = 0.16
    SNAKE_RAMP_START_TIER = 5
    SNAKE_RAMP_FULL_TIER = 12
    BOSS_SNAKE_CHANCE_CAP = 0.10
    SNAKE_FLAVOR_MULTIPLIERS: dict[str, float] = {
        "STANDARD": 1.0,
        "SWARM": 1.2,
        "HUNTERS": 0.95,
        "STORM": 1.12,
    }
    SNAKE_FLAVOR_PROFILES: dict[str, SnakeFlavorProfile] = {
        "STANDARD": SnakeFlavorProfile(
            variant_id="wanderer",
            segment_count=8,
            segment_spacing=18.0,
            speed_multiplier=1.0,
        ),
        "SWARM": SnakeFlavorProfile(
            variant_id="wanderer",
            segment_count=6,
            segment_spacing=15.0,
            speed_multiplier=0.94,
        ),
        "HUNTERS": SnakeFlavorProfile(
            variant_id="tracker",
            segment_count=7,
            segment_spacing=16.0,
            speed_multiplier=1.0,
        ),
        "STORM": SnakeFlavorProfile(
            variant_id="looper",
            segment_count=9,
            segment_spacing=17.0,
            speed_multiplier=1.08,
        ),
    }
    SPRAYER_FLAVOR_MULTIPLIERS: dict[str, float] = {
        "STANDARD": 1.0,
        "SWARM": 0.75,
        "HUNTERS": 1.15,
        "STORM": 1.05,
    }
    SPRAYER_FLAVOR_ATTACK_PROFILES: dict[str, SprayerFlavorProfile] = {
        "STANDARD": SprayerFlavorProfile(
            cooldown=2.0,
            spray_angle=55.0,
            projectile_count=5,
            projectile_speed=320.0,
        ),
        "SWARM": SprayerFlavorProfile(
            cooldown=2.35,
            spray_angle=50.0,
            projectile_count=4,
            projectile_speed=300.0,
        ),
        "HUNTERS": SprayerFlavorProfile(
            cooldown=1.75,
            spray_angle=36.0,
            projectile_count=5,
            projectile_speed=345.0,
        ),
        "STORM": SprayerFlavorProfile(
            cooldown=1.55,
            spray_angle=62.0,
            projectile_count=6,
            projectile_speed=335.0,
        ),
    }
    PINATA_TIER_VARIANTS: tuple[PinataTierVariant, ...] = (
        PinataTierVariant(
            variant_id="pinata_basic",
            speed_multiplier=0.58,
            health=3,
            break_confetti_count=14,
            mini_spawn_count=0,
        ),
        PinataTierVariant(
            variant_id="pinata_reinforced",
            speed_multiplier=0.60,
            health=4,
            break_confetti_count=18,
            mini_spawn_count=1,
        ),
        PinataTierVariant(
            variant_id="pinata_showstopper",
            speed_multiplier=0.62,
            health=5,
            break_confetti_count=22,
            mini_spawn_count=2,
        ),
    )

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
            boss_variant_id="classic",
        )

    def create_hazard_for_spawn(self, *, tier: int, base_speed: float, flavor_tag: str) -> Hazard:
        return self.create_hazard_for_spawn_with_chances(
            tier=tier,
            base_speed=base_speed,
            flavor_tag=flavor_tag,
            tracking_chance=self.tracking_spawn_chance,
        )

    def create_streamer_snake_for_spawn(
        self,
        *,
        tier: int,
        base_speed: float,
        flavor_tag: str,
        segment_count: int = 7,
        variant_id: str = "wanderer",
    ) -> StreamerSnake:
        resolved_variant = str(variant_id) if str(variant_id) in StreamerSnake.VARIANT_PROFILES else "wanderer"
        profile = EnemySpawnProfile(
            tier=tier,
            speed=base_speed * 0.66,
            health=1,
            movement_profile=f"streamer_{resolved_variant}",
            flavor_tag=flavor_tag,
            enemy_kind="streamer_snake",
        )
        snake = StreamerSnake(
            speed=profile.speed,
            segment_count=segment_count,
            variant_id=resolved_variant,
        )
        snake.apply_spawn_profile(self._profile_to_dict(profile))
        return snake

    def create_hazard_for_spawn_with_chances(
        self,
        *,
        tier: int,
        base_speed: float,
        flavor_tag: str,
        tracking_chance: float,
        boss_override_active: bool = False,
    ) -> Hazard:
        tracking_share, balloon_share, pinata_share = self._resolve_hazard_mix_for_spawn(
            tier=tier,
            tracking_chance=tracking_chance,
            boss_override_active=boss_override_active,
        )
        sprayer_target = self._sprayer_target_chance_for_spawn(
            tier=tier,
            flavor_tag=flavor_tag,
            boss_override_active=boss_override_active,
        )
        sprayer_share = min(balloon_share, max(0.0, sprayer_target))
        balloon_share -= sprayer_share
        snake_target = self._snake_target_chance_for_spawn(
            tier=tier,
            flavor_tag=flavor_tag,
            boss_override_active=boss_override_active,
        )
        snake_share = min(balloon_share, max(0.0, snake_target))
        balloon_share -= snake_share
        roll = self._rng.random()
        tracking_threshold = tracking_share
        sprayer_threshold = tracking_threshold + sprayer_share
        snake_threshold = sprayer_threshold + snake_share
        balloon_threshold = snake_threshold + balloon_share
        if roll < tracking_threshold:
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * 0.7,
                health=1,
                movement_profile="tracking_homing",
                flavor_tag=flavor_tag,
                enemy_kind="tracking",
            )
            hazard = TrackingHazard(speed=profile.speed)
        elif roll < sprayer_threshold:
            sprayer_attack = self._sprayer_attack_profile_for_flavor(flavor_tag)
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * 0.68,
                health=1,
                movement_profile="sprayer_glide",
                flavor_tag=flavor_tag,
                enemy_kind="confetti_sprayer",
                spray_cooldown=sprayer_attack.cooldown,
                spray_angle=sprayer_attack.spray_angle,
                spray_projectile_count=sprayer_attack.projectile_count,
                spray_projectile_speed=sprayer_attack.projectile_speed,
            )
            hazard = ConfettiSprayer(speed=profile.speed)
            hazard.configure_attack_profile(
                cooldown=sprayer_attack.cooldown,
                spray_angle=sprayer_attack.spray_angle,
                projectile_count=sprayer_attack.projectile_count,
                projectile_speed=sprayer_attack.projectile_speed,
            )
        elif roll < snake_threshold:
            snake_flavor_profile = self._snake_profile_for_flavor(flavor_tag, tier=tier)
            snake_variant = snake_flavor_profile.variant_id
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * 0.62 * snake_flavor_profile.speed_multiplier,
                health=1,
                movement_profile=f"streamer_{snake_variant}",
                flavor_tag=flavor_tag,
                enemy_kind="streamer_snake",
                snake_variant_id=snake_variant,
                snake_segment_count=snake_flavor_profile.segment_count,
                snake_segment_spacing=snake_flavor_profile.segment_spacing,
            )
            hazard = StreamerSnake(
                speed=profile.speed,
                segment_count=snake_flavor_profile.segment_count,
                segment_spacing=snake_flavor_profile.segment_spacing,
                variant_id=snake_variant,
            )
        elif roll < balloon_threshold:
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * 0.75,
                health=1,
                movement_profile="balloon_drift",
                flavor_tag=flavor_tag,
                enemy_kind="balloon",
            )
            hazard = BalloonEnemy(speed=profile.speed)
        else:
            pinata_variant = self._pinata_variant_for_tier(tier)
            profile = EnemySpawnProfile(
                tier=tier,
                speed=base_speed * pinata_variant.speed_multiplier,
                health=pinata_variant.health,
                movement_profile="pinata_heavy_drift",
                flavor_tag=flavor_tag,
                enemy_kind="pinata",
                break_confetti_count=pinata_variant.break_confetti_count,
                mini_spawn_count=pinata_variant.mini_spawn_count,
            )
            hazard = PinataEnemy(speed=profile.speed, max_health=profile.health, damage_per_hit=1)
        hazard.apply_spawn_profile(self._profile_to_dict(profile))
        return hazard

    def _pinata_variant_for_tier(self, tier: int) -> PinataTierVariant:
        clamped_tier = max(1, int(tier))
        if clamped_tier >= 9:
            return self.PINATA_TIER_VARIANTS[2]
        if clamped_tier >= 5:
            return self.PINATA_TIER_VARIANTS[1]
        return self.PINATA_TIER_VARIANTS[0]

    def _resolve_hazard_mix_for_spawn(
        self,
        *,
        tier: int,
        tracking_chance: float,
        boss_override_active: bool,
    ) -> tuple[float, float, float]:
        tracking_base = max(0.0, min(tracking_chance, 1.0))
        balloon_base = max(0.0, min(self.balloon_spawn_chance, 1.0))
        non_pinata_total = tracking_base + balloon_base

        pinata_target = self._pinata_target_chance_for_tier(
            tier=tier,
            boss_override_active=boss_override_active,
        )
        pinata_share = max(0.0, min(pinata_target, 1.0))
        remaining_share = 1.0 - pinata_share

        if non_pinata_total <= 0.0:
            return 0.0, remaining_share, pinata_share

        scale = remaining_share / non_pinata_total
        tracking_share = tracking_base * scale
        balloon_share = balloon_base * scale
        return tracking_share, balloon_share, pinata_share

    def _pinata_target_chance_for_tier(
        self,
        *,
        tier: int,
        boss_override_active: bool,
    ) -> float:
        clamped_tier = max(1, int(tier))
        if clamped_tier <= self.PINATA_RAMP_START_TIER:
            chance = self.MIN_PINATA_CHANCE
        else:
            tier_span = max(1, self.PINATA_RAMP_FULL_TIER - self.PINATA_RAMP_START_TIER)
            progress = min(
                max((clamped_tier - self.PINATA_RAMP_START_TIER) / tier_span, 0.0),
                1.0,
            )
            chance = self.MIN_PINATA_CHANCE + (
                (self.MAX_PINATA_CHANCE - self.MIN_PINATA_CHANCE) * progress
            )
        if boss_override_active:
            return min(chance, self.BOSS_PINATA_CHANCE_CAP)
        return chance

    def _sprayer_target_chance_for_spawn(
        self,
        *,
        tier: int,
        flavor_tag: str,
        boss_override_active: bool,
    ) -> float:
        clamped_tier = max(1, int(tier))
        if clamped_tier <= self.SPRAYER_RAMP_START_TIER:
            base_chance = self.MIN_SPRAYER_CHANCE
        else:
            tier_span = max(1, self.SPRAYER_RAMP_FULL_TIER - self.SPRAYER_RAMP_START_TIER)
            progress = min(
                max((clamped_tier - self.SPRAYER_RAMP_START_TIER) / tier_span, 0.0),
                1.0,
            )
            base_chance = self.MIN_SPRAYER_CHANCE + (
                (self.MAX_SPRAYER_CHANCE - self.MIN_SPRAYER_CHANCE) * progress
            )
        flavor_multiplier = self.SPRAYER_FLAVOR_MULTIPLIERS.get(str(flavor_tag), 1.0)
        chance = base_chance * max(0.0, float(flavor_multiplier))
        if boss_override_active:
            return min(chance, self.BOSS_SPRAYER_CHANCE_CAP)
        return chance

    def _snake_target_chance_for_spawn(
        self,
        *,
        tier: int,
        flavor_tag: str,
        boss_override_active: bool,
    ) -> float:
        clamped_tier = max(1, int(tier))
        if clamped_tier < self.SNAKE_RAMP_START_TIER:
            chance = self.MIN_SNAKE_CHANCE
        else:
            tier_span = max(1, self.SNAKE_RAMP_FULL_TIER - self.SNAKE_RAMP_START_TIER)
            progress = min(
                max((clamped_tier - self.SNAKE_RAMP_START_TIER) / tier_span, 0.0),
                1.0,
            )
            chance = self.MIN_SNAKE_CHANCE + (
                (self.MAX_SNAKE_CHANCE - self.MIN_SNAKE_CHANCE) * progress
            )
        flavor_multiplier = self.SNAKE_FLAVOR_MULTIPLIERS.get(str(flavor_tag), 1.0)
        chance *= max(0.0, float(flavor_multiplier))
        if boss_override_active:
            return min(chance, self.BOSS_SNAKE_CHANCE_CAP)
        return chance

    def _snake_profile_for_flavor(self, flavor_tag: str, *, tier: int) -> SnakeFlavorProfile:
        base = self.SNAKE_FLAVOR_PROFILES.get(
            str(flavor_tag),
            self.SNAKE_FLAVOR_PROFILES["STANDARD"],
        )
        clamped_tier = max(1, int(tier))
        if base.variant_id == "wanderer" and clamped_tier >= 12:
            return SnakeFlavorProfile(
                variant_id="tracker",
                segment_count=max(6, base.segment_count - 1),
                segment_spacing=max(14.0, base.segment_spacing),
                speed_multiplier=base.speed_multiplier,
            )
        return base

    def _sprayer_attack_profile_for_flavor(self, flavor_tag: str) -> SprayerFlavorProfile:
        return self.SPRAYER_FLAVOR_ATTACK_PROFILES.get(
            str(flavor_tag),
            self.SPRAYER_FLAVOR_ATTACK_PROFILES["STANDARD"],
        )

    def create_boss_hazard_for_spawn(
        self,
        *,
        tier: int,
        base_speed: float,
        flavor_tag: str,
        boss_variant_id: str = "classic",
    ) -> BossBalloon:
        resolved_variant_id, variant_profile = BossBalloon.resolve_profile(boss_variant_id)
        profile = EnemySpawnProfile(
            tier=tier,
            speed=base_speed * 0.5,
            health=variant_profile.max_health,
            movement_profile="boss_charge",
            flavor_tag=flavor_tag,
            enemy_kind="boss_balloon",
            boss_variant_id=resolved_variant_id,
        )
        boss = BossBalloon(
            speed=profile.speed,
            profile_id=resolved_variant_id,
            max_health=variant_profile.max_health,
            damage_per_hit=variant_profile.damage_per_hit,
        )
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
        payload: dict[str, object] = {
            "tier": profile.tier,
            "speed": profile.speed,
            "health": profile.health,
            "movement_profile": profile.movement_profile,
            "flavor_tag": profile.flavor_tag,
            "enemy_kind": profile.enemy_kind,
        }
        if profile.boss_variant_id is not None:
            payload["boss_variant_id"] = profile.boss_variant_id
        if profile.break_confetti_count is not None:
            payload["break_confetti_count"] = profile.break_confetti_count
        if profile.mini_spawn_count is not None:
            payload["mini_spawn_count"] = profile.mini_spawn_count
        if profile.spray_cooldown is not None:
            payload["spray_cooldown"] = profile.spray_cooldown
        if profile.spray_angle is not None:
            payload["spray_angle"] = profile.spray_angle
        if profile.spray_projectile_count is not None:
            payload["spray_projectile_count"] = profile.spray_projectile_count
        if profile.spray_projectile_speed is not None:
            payload["spray_projectile_speed"] = profile.spray_projectile_speed
        if profile.snake_variant_id is not None:
            payload["snake_variant_id"] = profile.snake_variant_id
        if profile.snake_segment_count is not None:
            payload["snake_segment_count"] = profile.snake_segment_count
        if profile.snake_segment_spacing is not None:
            payload["snake_segment_spacing"] = profile.snake_segment_spacing
        return payload

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
