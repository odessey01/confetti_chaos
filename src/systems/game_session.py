"""Gameplay session state and update flow."""

from __future__ import annotations

import pygame

from enemies import Hazard
from player import Player
from .spawn_controller import SpawnController


class GameSession:
    BASE_HAZARD_SPEED = 220.0
    MAX_SPEED_MULTIPLIER = 2.1
    RAMP_SECONDS = 75.0

    def __init__(self, bounds: pygame.Rect, hazard_count: int = 1) -> None:
        self.bounds = bounds
        self.hazard_count = hazard_count
        self.spawn_controller = SpawnController(bounds, initial_hazards=hazard_count)
        self.player: Player
        self.hazards: list[Hazard]
        self.score_seconds: float
        self.start_new_run()

    @property
    def score_value(self) -> int:
        return int(self.score_seconds)

    @property
    def difficulty_multiplier(self) -> float:
        progress = min(self.score_seconds / self.RAMP_SECONDS, 1.0)
        return 1.0 + progress * (self.MAX_SPEED_MULTIPLIER - 1.0)

    def start_new_run(self) -> None:
        self.player = self._create_player()
        self.spawn_controller.reset()
        self.hazards = self._create_initial_hazards(self.player)
        self.score_seconds = 0.0

    def update_playing(self, delta_seconds: float, keys: pygame.key.ScancodeWrapper) -> bool:
        self.score_seconds += delta_seconds
        self.player.update(delta_seconds, keys, self.bounds)
        player_center = pygame.Vector2(self.player.rect.center)
        target_hazard_speed = self.BASE_HAZARD_SPEED * self.difficulty_multiplier
        spawn_count = self.spawn_controller.spawn_count_for_frame(
            delta_seconds,
            self.difficulty_multiplier,
            len(self.hazards),
        )
        for _ in range(spawn_count):
            hazard = Hazard(speed=target_hazard_speed)
            self.spawn_controller.configure_hazard(hazard, player_center)
            self.hazards.append(hazard)

        for hazard in self.hazards:
            hazard.set_speed(target_hazard_speed)
            hazard.update(delta_seconds)
            if hazard.is_out_of_bounds(self.bounds):
                self.spawn_controller.configure_hazard(hazard, player_center)
            if self.player.rect.colliderect(hazard.rect):
                return True
        return False

    def draw_playing(self, surface: pygame.Surface) -> None:
        for hazard in self.hazards:
            hazard.draw(surface)
        self.player.draw(surface)

    def _create_player(self) -> Player:
        size = 40
        spawn_x = (self.bounds.width - size) / 2
        spawn_y = (self.bounds.height - size) / 2
        return Player(spawn_x, spawn_y, size=size)

    def _create_initial_hazards(self, player: Player) -> list[Hazard]:
        hazards = [Hazard(speed=self.BASE_HAZARD_SPEED) for _ in range(self.spawn_controller.initial_hazards)]
        target = pygame.Vector2(player.rect.center)
        for hazard in hazards:
            self.spawn_controller.configure_hazard(hazard, target)
        return hazards
