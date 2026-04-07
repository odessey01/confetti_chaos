"""Gameplay session state and update flow."""

from __future__ import annotations

import pygame

from enemies import BossBalloon, Hazard
from player import Player
from player.projectile import Projectile
from .confetti import Confetti
from .level_config import LevelConfig, get_level_config, LEVEL_1_SPAWN_RATE
from .spawn_controller import SpawnController


class GameSession:
    BASE_HAZARD_SPEED = 220.0
    MAX_SPEED_MULTIPLIER = 2.1
    RAMP_SECONDS = 75.0
    KILL_BONUS_POINTS = 50
    BOSS_BONUS_POINTS = 1000
    BOSS_CELEBRATION_TIME = 1.5
    LEVEL_UP_INTERVAL = 30.0
    POINTS_PER_LEVEL = 500

    def __init__(self, bounds: pygame.Rect, hazard_count: int = 1) -> None:
        self.bounds = bounds
        self.hazard_count = hazard_count
        self.spawn_controller = SpawnController(bounds, initial_hazards=hazard_count)
        self.player: Player
        self.hazards: list[Hazard]
        self.projectiles: list[Projectile]
        self.confetti: Confetti
        self.score_seconds: float
        self.elapsed_time: float
        self._spawn_pulse_centers: list[tuple[int, int]]
        self._boss_active: bool = False
        self._boss_defeated: bool = False
        self.start_new_run()

    @property
    def score_value(self) -> int:
        return int(self.score_seconds)

    @property
    def current_level(self) -> int:
        level_from_time = int(self.elapsed_time / self.LEVEL_UP_INTERVAL) + 1
        level_from_points = int(self.score_value / self.POINTS_PER_LEVEL) + 1
        return max(level_from_time, level_from_points)

    @property
    def current_level_config(self) -> LevelConfig:
        return get_level_config(self.current_level)

    @property
    def difficulty_multiplier(self) -> float:
        progress = min(self.elapsed_time / self.RAMP_SECONDS, 1.0)
        return 1.0 + progress * (self.MAX_SPEED_MULTIPLIER - 1.0)

    def start_new_run(self) -> None:
        self.player = self._create_player()
        self.spawn_controller.reset()
        self.projectiles = []
        self.confetti = Confetti()
        self.score_seconds = 0.0
        self.elapsed_time = 0.0
        self.hazards = self._create_initial_hazards(self.player)
        self._spawn_pulse_centers: list[tuple[int, int]] = [
            hazard.rect.center for hazard in self.hazards
        ]
        self._previous_level = 0
        self._boss_active = False
        self._boss_defeated_level: int | None = None
        self._boss_celebration_active = False
        self._boss_defeat_timer = 0.0
        self._boss_victory_sound_pending = False
        # Configure initial hazard mix for level 1
        level_config = self.current_level_config
        self.spawn_controller.set_tracking_chance(level_config.hazard_mix.tracking_hazard_chance)
        self.spawn_controller.set_balloon_chance(level_config.hazard_mix.balloon_enemy_chance)
        self._boss_defeated_level = None
        self._boss_celebration_active = False
        self._boss_defeat_timer = 0.0
        self._boss_victory_sound_pending = False

    def update_playing(self, delta_seconds: float, movement_input: pygame.Vector2, attack: bool = False) -> bool:
        if self._boss_celebration_active:
            self._boss_defeat_timer -= delta_seconds
            self.confetti.update(delta_seconds)
            if self._boss_defeat_timer <= 0.0:
                self._complete_boss_celebration()
            return False

        self.elapsed_time += delta_seconds
        self.score_seconds += delta_seconds
        self.player.update(delta_seconds, movement_input, self.bounds)
        player_center = pygame.Vector2(self.player.rect.center)
        
        # Handle attack input
        if attack:
            self.fire_projectile(self.player.facing)
        
        # Update projectiles
        self.projectiles = [p for p in self.projectiles if not p.is_expired() and not p.is_out_of_bounds(self.bounds)]
        for projectile in self.projectiles:
            projectile.update(delta_seconds)
        
        # Check projectile-hazard collisions
        kills = self._check_projectile_collisions()
        self.score_seconds += kills * self.KILL_BONUS_POINTS
        
        # Update confetti particles
        self.confetti.update(delta_seconds)
        
        # Get current level configuration
        level_config = self.current_level_config
        
        # Detect level change and update hazard mix
        if self.current_level != self._previous_level:
            self._previous_level = self.current_level
            self.spawn_controller.set_tracking_chance(level_config.hazard_mix.tracking_hazard_chance)
            self.spawn_controller.set_balloon_chance(level_config.hazard_mix.balloon_enemy_chance)
            
            # Check if this is a boss level (every 5th level)
            if (
                self.current_level % 5 == 0
                and self.current_level > 0
                and not self._boss_active
                and self._boss_defeated_level != self.current_level
            ):
                # Spawn boss
                boss = self.spawn_controller.create_boss_hazard(speed=self._spawn_speed())
                boss.rect.center = self.player.rect.center  # Spawn at player position
                self.hazards.append(boss)
                self._spawn_pulse_centers.append(boss.rect.center)
                self._boss_active = True
        
        # Spawn and update hazards with level-based scaling
        # Calculate spawn rate multiplier relative to level 1 baseline
        spawn_rate_multiplier = level_config.spawn_rate / LEVEL_1_SPAWN_RATE
        
        # During boss fight, reduce spawning
        if self._boss_active:
            spawn_rate_multiplier *= 0.5  # Halve spawn rate during boss
            max_enemies = min(level_config.max_simultaneous_enemies, 3)  # Cap at 3 during boss
        else:
            max_enemies = level_config.max_simultaneous_enemies
        
        spawn_count = self.spawn_controller.spawn_count_for_frame(
            delta_seconds,
            self.difficulty_multiplier,
            len(self.hazards),
            spawn_rate_multiplier=spawn_rate_multiplier,
        )
        
        # Only spawn if under the level's max simultaneous enemies cap
        for _ in range(spawn_count):
            if len(self.hazards) >= max_enemies:
                break
            hazard = self.spawn_controller.create_hazard(speed=self._spawn_speed())
            self.spawn_controller.configure_hazard(hazard, player_center)
            self.hazards.append(hazard)
            self._spawn_pulse_centers.append(hazard.rect.center)

        for hazard in self.hazards:
            hazard.update(delta_seconds, player_center)
            if hazard.is_out_of_bounds(self.bounds):
                self.spawn_controller.configure_hazard(hazard, player_center)
                self._spawn_pulse_centers.append(hazard.rect.center)
            if self.player.rect.colliderect(hazard.rect):
                return True
        return False

    def fire_projectile(self, direction: pygame.Vector2) -> None:
        """Fire a projectile in the given direction from the player center."""
        player_center = pygame.Vector2(self.player.rect.center)
        projectile = Projectile(
            position=player_center,
            direction=direction,
            speed=500.0,
            lifetime=3.0,
            size=8,
        )
        self.projectiles.append(projectile)

    def _check_projectile_collisions(self) -> int:
        """Check projectile-hazard collisions and remove entities on hit.
        
        Returns:
            Number of hazards killed in this frame.
        """
        hazards_to_remove = []
        projectiles_to_remove = []
        hazard_kill_positions = []
        
        for proj_idx, projectile in enumerate(self.projectiles):
            for hazard_idx, hazard in enumerate(self.hazards):
                if projectile.rect.colliderect(hazard.rect):
                    if proj_idx not in projectiles_to_remove:
                        projectiles_to_remove.append(proj_idx)
                    
                    # Handle boss health
                    if isinstance(hazard, BossBalloon):
                        if hazard.take_damage():
                            # Boss defeated - award bonus and enhanced feedback
                            hazards_to_remove.append(hazard_idx)
                            hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                            self.score_seconds += self.BOSS_BONUS_POINTS
                            self._boss_active = False
                            self._boss_defeated = True
                            self._boss_defeated_level = self.current_level
                            self._boss_celebration_active = True
                            self._boss_defeat_timer = self.BOSS_CELEBRATION_TIME
                            self._boss_victory_sound_pending = True
                            # Enhanced confetti burst for boss defeat
                            self._spawn_enhanced_confetti(pygame.Vector2(hazard.rect.center))
                    else:
                        # Normal hazard - instant kill
                        if hazard_idx not in hazards_to_remove:
                            hazards_to_remove.append(hazard_idx)
                            hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
        
        # Remove in reverse order to maintain indices
        for idx in sorted(hazards_to_remove, reverse=True):
            self.hazards.pop(idx)
        
        for idx in sorted(projectiles_to_remove, reverse=True):
            self.projectiles.pop(idx)
        
        # Spawn confetti at kill locations
        for center in hazard_kill_positions:
            self.confetti.spawn_burst(center, count=8)
        
        return len(hazards_to_remove)

    def _spawn_enhanced_confetti(self, center: pygame.Vector2) -> None:
        """Spawn an enhanced confetti burst for boss defeats."""
        self.confetti.spawn_burst(center, count=16)

    def consume_spawn_pulse_centers(self) -> list[tuple[int, int]]:
        centers = list(self._spawn_pulse_centers)
        self._spawn_pulse_centers.clear()
        return centers

    def _spawn_speed(self) -> float:
        """Return the speed used for newly spawned hazards at the current level."""
        return self.current_level_config.enemy_speed * self.difficulty_multiplier

    def _complete_boss_celebration(self) -> None:
        """Complete the boss defeat celebration and advance to the next level."""
        next_level_threshold = self.current_level * self.LEVEL_UP_INTERVAL
        self.elapsed_time = max(self.elapsed_time, float(next_level_threshold))
        self._boss_celebration_active = False
        self._boss_defeat_timer = 0.0

    @property
    def boss_celebration_active(self) -> bool:
        return self._boss_celebration_active

    @property
    def boss_defeat_bonus(self) -> int:
        return self.BOSS_BONUS_POINTS

    @property
    def boss_victory_sound_pending(self) -> bool:
        return self._boss_victory_sound_pending

    def clear_boss_victory_sound_pending(self) -> None:
        self._boss_victory_sound_pending = False

    def draw_playing(self, surface: pygame.Surface) -> None:
        for hazard in self.hazards:
            hazard.draw(surface)
        for projectile in self.projectiles:
            projectile.draw(surface)
        self.player.draw(surface)
        self.confetti.draw(surface)

    def _create_player(self) -> Player:
        size = 40
        spawn_x = (self.bounds.width - size) / 2
        spawn_y = (self.bounds.height - size) / 2
        return Player(spawn_x, spawn_y, size=size)

    def _create_initial_hazards(self, player: Player) -> list[Hazard]:
        spawn_speed = self._spawn_speed()
        hazards = [
            self.spawn_controller.create_hazard(speed=spawn_speed)
            for _ in range(self.spawn_controller.initial_hazards)
        ]
        target = pygame.Vector2(player.rect.center)
        for hazard in hazards:
            self.spawn_controller.configure_hazard(hazard, target)
        return hazards
