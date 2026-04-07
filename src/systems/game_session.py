"""Gameplay session state and update flow."""

from __future__ import annotations

import pygame

from enemies import BalloonEnemy, BossBalloon, ConfettiSpray, ConfettiSprayer, Hazard, PinataEnemy
from player import Player
from player.projectile import Projectile
from .confetti import Confetti
from .level_config import LevelConfig, get_level_config, LEVEL_1_SPAWN_RATE
from .settings import clamp_selected_start_level
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
    MAX_ACTIVE_ENEMY_SPRAYS = 48
    SPRAYER_PROJECTILE_LIFETIME = 0.58
    SPRAYER_PROJECTILE_SIZE = 9

    def __init__(self, bounds: pygame.Rect, hazard_count: int = 1) -> None:
        self.bounds = bounds
        self.hazard_count = hazard_count
        self.spawn_controller = SpawnController(bounds, initial_hazards=hazard_count)
        self.player: Player
        self.hazards: list[Hazard]
        self.projectiles: list[Projectile]
        self.enemy_sprays: list[ConfettiSpray]
        self.confetti: Confetti
        self.score_seconds: float
        self.elapsed_time: float
        self._spawn_pulse_centers: list[tuple[int, int]]
        self._boss_active: bool = False
        self._boss_defeated: bool = False
        self._pending_balloon_hit_sfx_count: int = 0
        self._pending_balloon_pop_sfx_count: int = 0
        self._pending_level_transition_sfx: bool = False
        self._pending_boss_spawn_sfx: bool = False
        self._pending_boss_hit_sfx_count: int = 0
        self._pending_boss_defeat_sfx: bool = False
        self._pending_boss_phase_change_sfx: bool = False
        self._pending_milestone_clear_sfx: bool = False
        self._pending_confetti_celebration_sfx: bool = False
        self._pending_sprayer_charge_sfx_count: int = 0
        self._pending_sprayer_burst_sfx_count: int = 0
        self._pending_sprayer_destroy_sfx_count: int = 0
        self.start_new_run()

    @property
    def score_value(self) -> int:
        return int(self.score_seconds)

    @property
    def current_level(self) -> int:
        level_from_time = int(self.elapsed_time / self.LEVEL_UP_INTERVAL) + 1
        level_from_points = int(self.score_value / self.POINTS_PER_LEVEL) + 1
        return max(level_from_time, level_from_points) + self._start_level_offset

    @property
    def current_level_config(self) -> LevelConfig:
        return get_level_config(self.current_level)

    @property
    def difficulty_multiplier(self) -> float:
        progress = min(self.elapsed_time / self.RAMP_SECONDS, 1.0)
        return 1.0 + progress * (self.MAX_SPEED_MULTIPLIER - 1.0)

    def start_new_run(self, start_level: int = 1) -> None:
        selected_level = clamp_selected_start_level(start_level)
        self._start_level_offset = selected_level - 1
        self.player = self._create_player()
        self.spawn_controller.reset()
        self.projectiles = []
        self.enemy_sprays = []
        self.confetti = Confetti()
        self.score_seconds = 0.0
        self.elapsed_time = 0.0
        self.hazards = self._create_initial_hazards(self.player)
        self._spawn_pulse_centers: list[tuple[int, int]] = [
            hazard.rect.center for hazard in self.hazards
        ]
        self._previous_level = self.current_level
        self._boss_active = False
        self._boss_defeated_level: int | None = None
        self._boss_celebration_active = False
        self._boss_defeat_timer = 0.0
        self._boss_victory_sound_pending = False
        self._pending_balloon_hit_sfx_count = 0
        self._pending_balloon_pop_sfx_count = 0
        self._pending_level_transition_sfx = False
        self._pending_boss_spawn_sfx = False
        self._pending_boss_hit_sfx_count = 0
        self._pending_boss_defeat_sfx = False
        self._pending_boss_phase_change_sfx = False
        self._pending_milestone_clear_sfx = False
        self._pending_confetti_celebration_sfx = False
        self._pending_sprayer_charge_sfx_count = 0
        self._pending_sprayer_burst_sfx_count = 0
        self._pending_sprayer_destroy_sfx_count = 0
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
        active_sprays: list[ConfettiSpray] = []
        for spray in self.enemy_sprays:
            spray.update(delta_seconds)
            if self.player.rect.colliderect(spray.rect):
                return True
            if not spray.is_expired() and not spray.is_out_of_bounds(self.bounds):
                active_sprays.append(spray)
        self.enemy_sprays = active_sprays
        
        # Check projectile-hazard collisions
        kills = self._check_projectile_collisions()
        self.score_seconds += kills * self.KILL_BONUS_POINTS
        
        # Update confetti particles
        self.confetti.update(delta_seconds)
        
        # Get current level configuration
        level_config = self.current_level_config
        
        # Detect level change and update hazard mix
        if self.current_level != self._previous_level:
            prior_level = self._previous_level
            self._previous_level = self.current_level
            self.spawn_controller.set_tracking_chance(level_config.hazard_mix.tracking_hazard_chance)
            self.spawn_controller.set_balloon_chance(level_config.hazard_mix.balloon_enemy_chance)
            if prior_level >= 1 and self.current_level > prior_level:
                self._pending_level_transition_sfx = True
            
            # Check if this is a boss level (every 5th level)
            if (
                self.current_level % 5 == 0
                and self.current_level > 0
                and not self._boss_active
                and self._boss_defeated_level != self.current_level
            ):
                # Spawn boss
                boss_tier = self.spawn_controller.select_spawn_tier(level_config.level)
                boss_tier_config = get_level_config(boss_tier)
                boss_variant_id = self._boss_variant_for_context(
                    level=level_config.level,
                    flavor_name=level_config.flavor.name,
                )
                boss = self.spawn_controller.create_boss_hazard_for_spawn(
                    tier=boss_tier,
                    base_speed=boss_tier_config.enemy_speed * self.difficulty_multiplier,
                    flavor_tag=boss_tier_config.flavor.name,
                    boss_variant_id=boss_variant_id,
                )
                self.spawn_controller.configure_hazard(boss, player_center)
                self._capture_spawn_snapshot(boss, level_config)
                self.hazards.append(boss)
                self._spawn_pulse_centers.append(boss.rect.center)
                self.spawn_controller.record_spawn_event(
                    current_level=level_config.level,
                    active_flavor=level_config.flavor.name,
                    spawn_tier=boss_tier,
                    enemy_kind="boss_balloon",
                    boss_override_active=True,
                )
                self._boss_active = True
                self._pending_boss_spawn_sfx = True
        
        # Spawn and update hazards with level-based scaling
        # Calculate spawn rate multiplier relative to level 1 baseline
        spawn_rate_multiplier = level_config.spawn_rate / LEVEL_1_SPAWN_RATE
        
        # During boss fight, reduce spawning
        if self._boss_active:
            spawn_rate_multiplier *= 0.42  # Keep pressure fair while preserving maneuver space
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
            spawn_tier = self.spawn_controller.select_spawn_tier(level_config.level)
            spawn_tier_config = get_level_config(spawn_tier)
            hazard = self.spawn_controller.create_hazard_for_spawn_with_chances(
                tier=spawn_tier,
                base_speed=spawn_tier_config.enemy_speed * self.difficulty_multiplier,
                flavor_tag=spawn_tier_config.flavor.name,
                tracking_chance=spawn_tier_config.hazard_mix.tracking_hazard_chance,
                boss_override_active=self._boss_active,
            )
            self.spawn_controller.configure_hazard(hazard, player_center)
            self._capture_spawn_snapshot(hazard, level_config)
            self.hazards.append(hazard)
            self._spawn_pulse_centers.append(hazard.rect.center)
            self.spawn_controller.record_spawn_event(
                current_level=level_config.level,
                active_flavor=level_config.flavor.name,
                spawn_tier=spawn_tier,
                enemy_kind=str(hazard.spawn_profile["enemy_kind"]),
                boss_override_active=self._boss_active,
            )

        requested_burst_spawns = 0
        for hazard in self.hazards:
            hazard.update(delta_seconds, player_center)
            if isinstance(hazard, BossBalloon):
                cues = hazard.consume_ability_cues()
                requested_burst_spawns += int(cues["burst_spawn_count"])
                if bool(cues["phase_changed"]):
                    self._pending_boss_phase_change_sfx = True
                    self._spawn_pulse_centers.append(hazard.rect.center)
            elif isinstance(hazard, ConfettiSprayer):
                spray_cues = hazard.consume_attack_cues()
                if bool(spray_cues.get("charge_started", False)):
                    self._pending_sprayer_charge_sfx_count += 1
                if bool(spray_cues.get("spray_fired", False)):
                    spray_origin = pygame.Vector2(spray_cues["origin"])
                    projectile_speed = float(spray_cues.get("projectile_speed", 320.0))
                    available_spray_slots = max(0, self.MAX_ACTIVE_ENEMY_SPRAYS - len(self.enemy_sprays))
                    per_burst_cap = 4 if self._boss_active else 6
                    spawn_count = min(len(spray_cues["directions"]), available_spray_slots, per_burst_cap)
                    for direction in spray_cues["directions"][:spawn_count]:
                        self.enemy_sprays.append(
                            ConfettiSpray(
                                position=spray_origin,
                                direction=pygame.Vector2(direction),
                                speed=projectile_speed,
                                lifetime=self.SPRAYER_PROJECTILE_LIFETIME,
                                size=self.SPRAYER_PROJECTILE_SIZE,
                            )
                        )
                    self._spawn_pulse_centers.append(hazard.rect.center)
                    self._pending_sprayer_burst_sfx_count += 1
            if hazard.is_out_of_bounds(self.bounds):
                self.spawn_controller.configure_hazard(hazard, player_center)
                self._spawn_pulse_centers.append(hazard.rect.center)
            if self.player.rect.colliderect(hazard.rect):
                return True

        if requested_burst_spawns > 0:
            available_slots = max(0, max_enemies - len(self.hazards))
            burst_spawns = min(requested_burst_spawns, available_slots, 2)
            for _ in range(burst_spawns):
                spawn_tier = self.spawn_controller.select_spawn_tier(level_config.level)
                spawn_tier_config = get_level_config(spawn_tier)
                hazard = self.spawn_controller.create_hazard_for_spawn_with_chances(
                    tier=spawn_tier,
                    base_speed=spawn_tier_config.enemy_speed * self.difficulty_multiplier,
                    flavor_tag=spawn_tier_config.flavor.name,
                    tracking_chance=0.0,
                    boss_override_active=True,
                )
                self.spawn_controller.configure_hazard(hazard, player_center)
                self._capture_spawn_snapshot(hazard, level_config)
                self.hazards.append(hazard)
                self._spawn_pulse_centers.append(hazard.rect.center)
                self.spawn_controller.record_spawn_event(
                    current_level=level_config.level,
                    active_flavor=level_config.flavor.name,
                    spawn_tier=spawn_tier,
                    enemy_kind=str(hazard.spawn_profile["enemy_kind"]),
                    boss_override_active=True,
                )
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
        pinata_split_requests: list[dict[str, object]] = []
        
        for proj_idx, projectile in enumerate(self.projectiles):
            for hazard_idx, hazard in enumerate(self.hazards):
                if projectile.rect.colliderect(hazard.rect):
                    if proj_idx not in projectiles_to_remove:
                        projectiles_to_remove.append(proj_idx)
                    
                    # Handle boss health
                    if isinstance(hazard, BossBalloon):
                        hit_registered, defeated = hazard.apply_hit()
                        if hit_registered:
                            self._pending_balloon_hit_sfx_count += 1
                            self._pending_boss_hit_sfx_count += 1
                        if defeated:
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
                            self._pending_boss_defeat_sfx = True
                            self._pending_milestone_clear_sfx = True
                            self._pending_confetti_celebration_sfx = True
                            # Enhanced confetti burst for boss defeat
                            self._spawn_enhanced_confetti(pygame.Vector2(hazard.rect.center))
                    elif isinstance(hazard, PinataEnemy):
                        hit_registered, defeated = hazard.apply_hit()
                        if hit_registered:
                            self._pending_balloon_hit_sfx_count += 1
                        if defeated and hazard_idx not in hazards_to_remove:
                            hazards_to_remove.append(hazard_idx)
                            center = pygame.Vector2(hazard.rect.center)
                            hazard_kill_positions.append(center)
                            self._pending_balloon_pop_sfx_count += 1
                            profile = hazard.spawn_profile or {}
                            break_confetti_count = int(profile.get("break_confetti_count", 14))
                            mini_spawn_count = int(profile.get("mini_spawn_count", 0))
                            pinata_split_requests.append(
                                {
                                    "center": center,
                                    "tier": int(profile.get("tier", self.current_level)),
                                    "flavor_tag": str(
                                        profile.get("flavor_tag", self.current_level_config.flavor.name)
                                    ),
                                    "mini_spawn_count": max(0, mini_spawn_count),
                                }
                            )
                            self._spawn_pinata_break_confetti(
                                center,
                                burst_count=max(10, break_confetti_count),
                            )
                    elif isinstance(hazard, ConfettiSprayer):
                        self._pending_balloon_hit_sfx_count += 1
                        if hazard_idx not in hazards_to_remove:
                            hazards_to_remove.append(hazard_idx)
                            center = pygame.Vector2(hazard.rect.center)
                            hazard_kill_positions.append(center)
                            self._pending_balloon_pop_sfx_count += 1
                            self._pending_sprayer_destroy_sfx_count += 1
                            self._spawn_sprayer_destroy_confetti(center)
                    else:
                        # Normal hazard - instant kill
                        self._pending_balloon_hit_sfx_count += 1
                        if hazard_idx not in hazards_to_remove:
                            hazards_to_remove.append(hazard_idx)
                            hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                            self._pending_balloon_pop_sfx_count += 1
        
        # Remove in reverse order to maintain indices
        for idx in sorted(hazards_to_remove, reverse=True):
            self.hazards.pop(idx)
        
        for idx in sorted(projectiles_to_remove, reverse=True):
            self.projectiles.pop(idx)
        
        # Spawn confetti at kill locations
        for center in hazard_kill_positions:
            self.confetti.spawn_burst(center, count=8)

        if pinata_split_requests:
            self._spawn_pinata_minis(pinata_split_requests)

        return len(hazards_to_remove)

    def _spawn_enhanced_confetti(self, center: pygame.Vector2) -> None:
        """Spawn an enhanced confetti burst for boss defeats."""
        self.confetti.spawn_burst(center, count=16)

    def _spawn_pinata_break_confetti(self, center: pygame.Vector2, *, burst_count: int = 14) -> None:
        """Spawn a stronger confetti burst for pinata breaks."""
        self.confetti.spawn_burst(
            center,
            count=max(10, int(burst_count)),
            speed_min=180.0,
            speed_max=360.0,
            lifetime_min=0.7,
            lifetime_max=1.0,
        )

    def _spawn_sprayer_destroy_confetti(self, center: pygame.Vector2) -> None:
        """Spawn a distinct medium burst on sprayer destruction."""
        self.confetti.spawn_burst(
            center,
            count=11,
            speed_min=160.0,
            speed_max=300.0,
            lifetime_min=0.5,
            lifetime_max=0.85,
        )

    def _spawn_pinata_minis(self, requests: list[dict[str, object]]) -> None:
        """Spawn lightweight mini-balloons from defeated pinatas."""
        level_config = self.current_level_config
        max_enemies = min(level_config.max_simultaneous_enemies, 3) if self._boss_active else level_config.max_simultaneous_enemies
        available_slots = max(0, max_enemies - len(self.hazards))
        if available_slots <= 0:
            return

        player_center = pygame.Vector2(self.player.rect.center)
        for request in requests:
            if available_slots <= 0:
                break
            center = pygame.Vector2(request["center"])
            tier = int(request["tier"])
            flavor_tag = str(request["flavor_tag"])
            desired_count = min(max(0, int(request["mini_spawn_count"])), 2)
            spawn_count = min(desired_count, available_slots)
            for index in range(spawn_count):
                mini = self._create_pinata_mini_balloon(
                    center=center,
                    player_center=player_center,
                    tier=tier,
                    flavor_tag=flavor_tag,
                    index=index,
                    total=spawn_count,
                )
                self.hazards.append(mini)
                self._spawn_pulse_centers.append(mini.rect.center)
                self.spawn_controller.record_spawn_event(
                    current_level=level_config.level,
                    active_flavor=level_config.flavor.name,
                    spawn_tier=tier,
                    enemy_kind="mini_balloon",
                    boss_override_active=self._boss_active,
                )
                available_slots -= 1
                if available_slots <= 0:
                    break

    def _create_pinata_mini_balloon(
        self,
        *,
        center: pygame.Vector2,
        player_center: pygame.Vector2,
        tier: int,
        flavor_tag: str,
        index: int,
        total: int,
    ) -> BalloonEnemy:
        mini = BalloonEnemy(size=44, speed=205.0)
        spread = 0.0
        if total > 1:
            spread_step = 22.0
            spread = (index - ((total - 1) / 2.0)) * spread_step
        radial_offset = pygame.Vector2(8.0, 0.0).rotate((360.0 / max(total, 1)) * index)
        spawn = center + radial_offset
        aim_target = player_center + pygame.Vector2(50.0, 0.0).rotate(spread)
        if (aim_target - spawn).length_squared() <= 0.0:
            aim_target = spawn + pygame.Vector2(1.0, 0.0)
        mini.launch_toward_target(spawn, aim_target)
        profile = {
            "tier": int(tier),
            "speed": float(mini.speed),
            "health": 1,
            "movement_profile": "balloon_split",
            "flavor_tag": str(flavor_tag),
            "enemy_kind": "mini_balloon",
        }
        mini.apply_spawn_profile(profile)
        mini.capture_spawn_snapshot(level=self.current_level, flavor=flavor_tag)
        return mini

    def consume_audio_cues(self) -> dict[str, int | bool]:
        cues = {
            "balloon_hit_count": self._pending_balloon_hit_sfx_count,
            "balloon_pop_count": self._pending_balloon_pop_sfx_count,
            "level_transition": self._pending_level_transition_sfx,
            "boss_spawn": self._pending_boss_spawn_sfx,
            "boss_hit_count": self._pending_boss_hit_sfx_count,
            "boss_defeat": self._pending_boss_defeat_sfx,
            "boss_phase_change": self._pending_boss_phase_change_sfx,
            "milestone_clear": self._pending_milestone_clear_sfx,
            "confetti_celebration": self._pending_confetti_celebration_sfx,
            "sprayer_charge_count": self._pending_sprayer_charge_sfx_count,
            "sprayer_burst_count": self._pending_sprayer_burst_sfx_count,
            "sprayer_destroy_count": self._pending_sprayer_destroy_sfx_count,
        }
        self._pending_balloon_hit_sfx_count = 0
        self._pending_balloon_pop_sfx_count = 0
        self._pending_level_transition_sfx = False
        self._pending_boss_spawn_sfx = False
        self._pending_boss_hit_sfx_count = 0
        self._pending_boss_defeat_sfx = False
        self._pending_boss_phase_change_sfx = False
        self._pending_milestone_clear_sfx = False
        self._pending_confetti_celebration_sfx = False
        self._pending_sprayer_charge_sfx_count = 0
        self._pending_sprayer_burst_sfx_count = 0
        self._pending_sprayer_destroy_sfx_count = 0
        return cues

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
    def boss_active(self) -> bool:
        return self._boss_active

    @property
    def boss_defeat_bonus(self) -> int:
        return self.BOSS_BONUS_POINTS

    @property
    def boss_victory_sound_pending(self) -> bool:
        return self._boss_victory_sound_pending

    def clear_boss_victory_sound_pending(self) -> None:
        self._boss_victory_sound_pending = False

    def spawn_telemetry_snapshot(self, limit: int = 60) -> dict[str, object]:
        current = self.current_level_config
        return {
            "current_level": self.current_level,
            "active_flavor": current.flavor.name,
            "boss_override_active": self._boss_active,
            "spawn_summary": self.spawn_controller.spawn_telemetry_summary(limit=limit),
        }

    def draw_playing(self, surface: pygame.Surface) -> None:
        for hazard in self.hazards:
            hazard.draw(surface)
        for projectile in self.projectiles:
            projectile.draw(surface)
        for spray in self.enemy_sprays:
            spray.draw(surface)
        self.player.draw(surface)
        self.confetti.draw(surface)

    def _create_player(self) -> Player:
        size = 40
        spawn_x = (self.bounds.width - size) / 2
        spawn_y = (self.bounds.height - size) / 2
        return Player(spawn_x, spawn_y, size=size)

    def _create_initial_hazards(self, player: Player) -> list[Hazard]:
        spawn_speed = self._spawn_speed()
        level_config = self.current_level_config
        hazards = [
            self.spawn_controller.create_hazard_for_spawn_with_chances(
                tier=self.spawn_controller.select_spawn_tier(level_config.level),
                base_speed=spawn_speed,
                flavor_tag=level_config.flavor.name,
                tracking_chance=level_config.hazard_mix.tracking_hazard_chance,
                boss_override_active=False,
            )
            for _ in range(self.spawn_controller.initial_hazards)
        ]
        target = pygame.Vector2(player.rect.center)
        for hazard in hazards:
            self.spawn_controller.configure_hazard(hazard, target)
            self._capture_spawn_snapshot(hazard, level_config)
            self.spawn_controller.record_spawn_event(
                current_level=level_config.level,
                active_flavor=level_config.flavor.name,
                spawn_tier=int(hazard.spawn_profile["tier"]),
                enemy_kind=str(hazard.spawn_profile["enemy_kind"]),
                boss_override_active=False,
            )
        return hazards

    def _capture_spawn_snapshot(self, hazard: Hazard, level_config: LevelConfig) -> None:
        hazard.capture_spawn_snapshot(
            level=level_config.level,
            flavor=level_config.flavor.name,
        )

    def _boss_variant_for_context(self, *, level: int, flavor_name: str) -> str:
        """Hook for future multi-boss variety selection."""
        _ = (level, flavor_name)
        return "classic"
