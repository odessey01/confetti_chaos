"""Centralized hazard spawning logic with fairness constraints."""

from __future__ import annotations

import random
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
        self._rng = rng if rng is not None else random.Random()
        self._spawn_timer = 0.0

    def reset(self) -> None:
        self._spawn_timer = 0.0

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
        roll = self._rng.random()
        if roll < self.tracking_spawn_chance:
            return TrackingHazard(speed=speed * 0.7)  # Reduced from 0.82
        return BalloonEnemy(speed=speed * 0.75)

    def create_boss_hazard(self, speed: float) -> BossBalloon:
        """Create a boss balloon enemy."""
        return BossBalloon(speed=speed * 0.5)  # Boss moves slower

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
