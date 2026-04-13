"""Gameplay session state and update flow."""

from __future__ import annotations

import math
import importlib

import pygame

from enemies import (
    BalloonEnemy,
    BossBalloon,
    ConfettiSpray,
    ConfettiSprayer,
    Hazard,
    PinataEnemy,
    StreamerSnake,
)
from pickups import XpDrop
from player import BottleRocket, BottleRocketFlightProfile, Player
from .aim_assist import AimAssistConfig, AimAssistSystem
from .character_passives import CharacterPassiveProfile, get_character_passive
from .character_supers import CharacterSuperProfile, get_character_super
from .confetti import Confetti
from .level_config import LevelConfig, get_level_config, LEVEL_1_SPAWN_RATE
from .run_progression import RunProgression
from .run_upgrades import RunUpgradeSystem, UpgradeDefinition
from .settings import clamp_selected_start_level
from .party_animals import DEFAULT_PARTY_ANIMAL_ID, get_party_animal
from .player_animation import PlayerAnimationSystem
from .player_visual_anchors import DEFAULT_PLAYER_WEAPON_ANCHOR, resolve_player_visual_anchor
from .player_visual import PlayerRenderer
from . import weapon_visual_assets as weapon_visual_assets_module
from . import weapon_visuals as weapon_visuals_module
from .weapon_visual_overlay_renderer import WeaponVisualOverlayRenderer
from .weapon_visual_overlays import WeaponVisualOverlay
from .spawn_controller import SpawnController
from .weapons import (
    DEFAULT_WEAPON_ID,
    SparklerAttackProfile,
    WeaponDefinition,
    get_weapon_definition,
)
from .weapon_evolutions import WeaponEvolutionTracker, preview_weapon_evolutions_with_added_tags


class GameSession:
    BASE_HAZARD_SPEED = 220.0
    MAX_SPEED_MULTIPLIER = 1.7
    SPEED_RAMP_LEVEL_SPAN = 12
    KILL_BONUS_POINTS = 50
    BOSS_BONUS_POINTS = 1000
    BOSS_LEVEL_INTERVAL = 10
    BOSS_CELEBRATION_TIME = 1.5
    BASE_PLAYER_SPEED = 320.0
    ANIMATION_MOVE_INPUT_DEADZONE = 0.18
    BASE_PROJECTILE_SPEED = 540.0
    BASE_FIRE_COOLDOWN = 0.18
    BOTTLE_ROCKET_LIFETIME = 2.2
    BOTTLE_ROCKET_MAX_TRAVEL_DISTANCE = 1120.0
    BOTTLE_ROCKET_WOBBLE_DEGREES = 3.2
    BOTTLE_ROCKET_WOBBLE_FREQUENCY_HZ = 8.4
    BOTTLE_ROCKET_ACCEL_PER_SECOND = 48.0
    BOTTLE_ROCKET_MAX_SPEED_MULTIPLIER = 1.16
    BOTTLE_ROCKET_DECAY_START_FRACTION = 0.46
    BOTTLE_ROCKET_DECAY_SPEED_PER_SECOND = 118.0
    BOTTLE_ROCKET_DOWNWARD_ARC_PER_SECOND = 0.48
    BOTTLE_ROCKET_EXPLOSION_DAMAGE_MODE = "direct_hit_only"
    BOTTLE_ROCKET_EXPLOSION_RADIUS = 0.0
    BURST_ROCKET_FRAGMENT_COUNT = 2
    BURST_ROCKET_FRAGMENT_SPREAD_DEGREES = 20.0
    BURST_ROCKET_FRAGMENT_LIFETIME = 0.55
    BURST_ROCKET_FRAGMENT_MAX_TRAVEL_DISTANCE = 260.0
    BURST_ROCKET_FRAGMENT_SPEED_MULT = 0.85
    BIG_POP_ROCKET_RADIUS = 84.0
    DELAYED_BLAST_FUSE_SECONDS = 0.5
    DELAYED_BLAST_BUILDUP_WINDOW = 0.16
    PINBALL_ROCKET_MAX_BOUNCES = 3
    PINBALL_ROCKET_SEARCH_RADIUS = 320.0
    SPARKLER_SWEEP_CONE_DEGREES = 82.0
    SPARKLER_ARC_INNER_RADIUS_RATIO = 0.24
    SPARKLER_SWEEP_DURATION = 0.08
    ORBITING_SPARK_COUNT = 3
    ORBITING_SPARK_RADIUS = 98.0
    ORBITING_SPARK_CONTACT_RADIUS = 20.0
    ORBITING_SPARK_DAMAGE = 1
    ORBITING_SPARK_ROTATION_DEGREES_PER_SECOND = 210.0
    ORBITING_SPARK_CONTACT_COOLDOWN = 0.2
    ORBITING_SPARK_TRAIL_STEPS = 4
    ORBITING_SPARK_TRAIL_ANGLE_STEP = 12.0
    SPARK_AURA_RADIUS = 128.0
    SPARK_AURA_TICK_INTERVAL = 0.3
    SPARK_AURA_DAMAGE = 1
    MAX_ACTIVE_ENEMY_SPRAYS = 48
    SPRAYER_PROJECTILE_LIFETIME = 0.58
    SPRAYER_PROJECTILE_SIZE = 9
    PLAYER_HITBOX_SCALE = 0.75
    XP_PICKUP_RADIUS = 18
    XP_MAGNET_RADIUS = 120.0
    XP_MAGNET_SPEED = 380.0
    XP_DROP_LIFETIME_SECONDS = 16.0
    XP_DROP_FADE_DURATION_SECONDS = 2.5
    XP_DROP_SIZE_MIN = 12
    XP_DROP_SIZE_MAX = 20
    DODGE_AFFECTED_BY_PASSIVES = False
    AIM_ASSIST_CONTROLLER_ENABLED = True
    AIM_ASSIST_KEYBOARD_ENABLED = False
    XP_DROP_VALUES: dict[str, int] = {
        "tracking": 3,
        "balloon": 3,
        "mini_balloon": 2,
        "pinata": 6,
        "streamer_snake": 6,
        "confetti_sprayer": 7,
        "boss_balloon": 18,
    }
    XP_REWARDS: dict[str, int] = XP_DROP_VALUES
    SUPER_CHARGE_REWARDS: dict[str, int] = {
        "tracking": 6,
        "balloon": 6,
        "mini_balloon": 5,
        "pinata": 10,
        "streamer_snake": 10,
        "confetti_sprayer": 11,
        "boss_balloon": 26,
    }
    SUPER_CHARGE_PER_BOSS_HIT = 3
    CAT_FRENZY_DURATION = 4.0
    CAT_FRENZY_DAMAGE_BONUS = 1
    CAT_FRENZY_FIRE_RATE_BONUS = 0.35
    BEAR_ROAR_RADIUS = 360.0
    BEAR_ROAR_MAX_PUSH_DISTANCE = 170.0
    BEAR_ROAR_MAX_PUSH_SPEED = 620.0
    BEAR_ROAR_INVULNERABILITY_DURATION = 0.45
    BEAR_ROAR_DAMAGE_RADIUS = 150.0
    BEAR_ROAR_BOSS_CHIP_DAMAGE = 1
    RACCOON_CHAOS_DROP_XP_BONUS = 16
    RACCOON_CHAOS_DROP_SCORE_BONUS = 120

    def __init__(self, bounds: pygame.Rect, hazard_count: int = 1) -> None:
        self.bounds = bounds
        self.hazard_count = hazard_count
        self.spawn_controller = SpawnController(bounds, initial_hazards=hazard_count)
        self.player: Player
        self.hazards: list[Hazard]
        self.projectiles: list[BottleRocket]
        self.enemy_sprays: list[ConfettiSpray]
        self.xp_drops: list[XpDrop]
        self.confetti: Confetti
        self.score_seconds: float
        self.elapsed_time: float
        self.run_progression = RunProgression()
        self.run_upgrades = RunUpgradeSystem()
        self.player_renderer = PlayerRenderer()
        self.player_animation = PlayerAnimationSystem()
        self.weapon_overlay_renderer = WeaponVisualOverlayRenderer()
        self._weapon_overlay_event_times: dict[str, float] = {}
        self._weapon_overlay_tuning_by_weapon: dict[str, dict[str, float]] = {}
        self._show_weapon_overlay_debug = False
        self._active_input_method = "keyboard_mouse"
        self._aim_assist_user_enabled = True
        self._aim_assist = AimAssistSystem(config=AimAssistConfig(enabled=False))
        self._aim_assist_debug: dict[str, object] = {}
        self._sparkler_attack_debug: dict[str, object] = {}
        self._sparkler_swing_count = 0
        self._orbiting_spark_angle_degrees = 0.0
        self._orbiting_spark_contact_cooldowns: dict[int, float] = {}
        self._spark_aura_tick_timer = 0.0
        self._last_attack_direction = pygame.Vector2(1.0, 0.0)
        self.active_weapon_id = DEFAULT_WEAPON_ID
        self._active_weapon_definition: WeaponDefinition = get_weapon_definition(DEFAULT_WEAPON_ID)
        self.active_player_animal_id = DEFAULT_PARTY_ANIMAL_ID
        self.active_character_passive_id = DEFAULT_PARTY_ANIMAL_ID
        self._active_character_passive: CharacterPassiveProfile = get_character_passive(
            DEFAULT_PARTY_ANIMAL_ID
        )
        self.active_character_super_id = DEFAULT_PARTY_ANIMAL_ID
        self._active_character_super: CharacterSuperProfile = get_character_super(
            DEFAULT_PARTY_ANIMAL_ID
        )
        self._super_charge = 0
        self._character_max_health_bonus = 0
        self._character_move_speed_mult = 0.0
        self._character_outgoing_damage_bonus = 0
        self._character_incoming_damage_mult = 1.0
        self._character_xp_gain_mult = 0.0
        self._character_pickup_radius_bonus = 0.0
        self._character_xp_magnet_mult = 0.0
        self._current_upgrade_choices: list[UpgradeDefinition] = []
        self._weapon_evolution_tracker = WeaponEvolutionTracker()
        self._weapon_evolution_forms: dict[str, str] = {}
        self._weapon_evolution_behavior_ids: dict[str, set[str]] = {}
        self._sticky_rocket_target_ids: set[int] = set()
        self.max_active_projectiles = 3
        self._weapon_cooldown_timer = 0.0
        self._bonus_score_points = 0.0
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
        self._pending_player_damage_sfx_count: int = 0
        self._pending_super_activate_sfx_count = 0
        self._pending_bottle_rocket_launch_sfx_count = 0
        self._pending_bottle_rocket_impact_sfx_count = 0
        self._pending_sparkler_swing_sfx_count = 0
        self._pending_sparkler_hit_sfx_count = 0
        self._pending_xp_pickup_sfx_count = 0
        self._pending_evolution_sfx_count = 0
        self._evolution_feedback_timer = 0.0
        self._evolution_feedback_label = ""
        self._evolution_pause_timer = 0.0
        self._dodge_trail_timer = 0.0
        self._cat_frenzy_timer = 0.0
        self._debug_font: pygame.font.Font | None = None
        self.start_new_run()

    @property
    def score_value(self) -> int:
        return int(self.score_seconds + self._bonus_score_points)

    @property
    def current_level(self) -> int:
        return max(1, self.run_progression.run_level) + self._start_level_offset

    @property
    def current_level_config(self) -> LevelConfig:
        return get_level_config(self.current_level)

    @property
    def difficulty_multiplier(self) -> float:
        level_progress = max(0, self.current_level - 1)
        progress = min(level_progress / max(1, self.SPEED_RAMP_LEVEL_SPAN), 1.0)
        return 1.0 + progress * (self.MAX_SPEED_MULTIPLIER - 1.0)

    def start_new_run(
        self,
        start_level: int = 1,
        player_animal_id: str | None = None,
        weapon_id: str | None = None,
    ) -> None:
        selected_level = clamp_selected_start_level(start_level)
        selected_animal = get_party_animal(player_animal_id or self.active_player_animal_id)
        passive = get_character_passive(selected_animal.variant_id)
        super_profile = get_character_super(selected_animal.variant_id)
        self.active_player_animal_id = selected_animal.variant_id
        self.active_character_passive_id = passive.character_id
        self._active_character_passive = passive
        self.active_character_super_id = super_profile.character_id
        self._active_character_super = super_profile
        self._super_charge = 0
        self._start_level_offset = selected_level - 1
        self.set_active_weapon(weapon_id or self.active_weapon_id)
        self.player = self._create_player()
        self.player_animation.set_character(self.active_player_animal_id)
        self.player_animation.reset()
        self._apply_character_passive_profile(self._active_character_passive)
        self.spawn_controller.reset()
        self.projectiles = []
        self.enemy_sprays = []
        self.xp_drops = []
        self.confetti = Confetti()
        self.run_progression.reset()
        self.run_upgrades.reset()
        self._current_upgrade_choices = []
        self._weapon_evolution_tracker.reset()
        self._weapon_evolution_forms = {}
        self._weapon_evolution_behavior_ids = {}
        self._weapon_overlay_event_times = {}
        self._weapon_overlay_tuning_by_weapon = {}
        self._sticky_rocket_target_ids = set()
        self.max_active_projectiles = 3
        self._weapon_cooldown_timer = 0.0
        self._bonus_score_points = 0.0
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
        self._pending_player_damage_sfx_count = 0
        self._pending_super_activate_sfx_count = 0
        self._pending_bottle_rocket_launch_sfx_count = 0
        self._pending_bottle_rocket_impact_sfx_count = 0
        self._pending_sparkler_swing_sfx_count = 0
        self._pending_sparkler_hit_sfx_count = 0
        self._pending_xp_pickup_sfx_count = 0
        self._pending_evolution_sfx_count = 0
        self._evolution_feedback_timer = 0.0
        self._evolution_feedback_label = ""
        self._evolution_pause_timer = 0.0
        self._dodge_trail_timer = 0.0
        self._cat_frenzy_timer = 0.0
        self._sparkler_attack_debug = {}
        self._sparkler_swing_count = 0
        self._orbiting_spark_angle_degrees = 0.0
        self._orbiting_spark_contact_cooldowns = {}
        self._spark_aura_tick_timer = 0.0
        self._last_attack_direction = pygame.Vector2(1.0, 0.0)
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
        self._evolution_feedback_timer = max(0.0, self._evolution_feedback_timer - max(0.0, delta_seconds))
        if self._evolution_feedback_timer <= 0.0:
            self._evolution_feedback_label = ""
        if self._evolution_pause_timer > 0.0:
            self._evolution_pause_timer = max(0.0, self._evolution_pause_timer - max(0.0, delta_seconds))
            self.confetti.update(delta_seconds)
            return False

        self.elapsed_time += delta_seconds
        self.score_seconds += delta_seconds
        self._weapon_cooldown_timer = max(0.0, self._weapon_cooldown_timer - delta_seconds)
        if self._sparkler_attack_debug:
            expires = float(self._sparkler_attack_debug.get("expires_in", 0.0))
            expires = max(0.0, expires - max(0.0, delta_seconds))
            self._sparkler_attack_debug["expires_in"] = expires
            if expires <= 0.0:
                self._sparkler_attack_debug = {}
        effects = self.run_upgrades.effects_snapshot()
        self._apply_player_upgrade_effects(effects)
        player_was_invulnerable = self.player.is_invulnerable
        self.player.update(delta_seconds, movement_input, self.bounds)
        movement_strength = pygame.Vector2(movement_input).length()
        movement_active = bool(movement_strength >= self.ANIMATION_MOVE_INPUT_DEADZONE) or bool(
            self.player.is_dodging
        )
        self.player_animation.update(
            delta_seconds,
            moving=movement_active,
            facing=pygame.Vector2(self.player.facing),
        )
        player_center = pygame.Vector2(self.player.rect.center)
        player_collision_rect = self.player_collision_rect()
        player_contact_damage_enabled = not player_was_invulnerable
        self._dodge_trail_timer = max(0.0, self._dodge_trail_timer - delta_seconds)
        self._cat_frenzy_timer = max(0.0, self._cat_frenzy_timer - delta_seconds)
        if self.player.is_dodging and self._dodge_trail_timer <= 0.0:
            self.confetti.spawn_burst(player_center, count=2, speed_min=80.0, speed_max=150.0, lifetime_min=0.2, lifetime_max=0.35)
            self._dodge_trail_timer = 0.04
        self._update_orbiting_sparks(delta_seconds)
        self._update_spark_aura(delta_seconds)
        
        # Handle attack input
        if attack:
            self.fire_projectile(self.player.facing)
        
        # Update projectiles
        active_projectiles: list[BottleRocket] = []
        for projectile in self.projectiles:
            if bool(getattr(projectile, "is_sticky_attached", False)):
                if self._update_delayed_blast_projectile(projectile, delta_seconds):
                    continue
                active_projectiles.append(projectile)
                continue
            projectile.update(delta_seconds)
            if projectile.is_expired() or projectile.is_out_of_bounds(self.bounds):
                evolved_impact_scale = self._bottle_rocket_impact_scale(projectile)
                self._spawn_bottle_rocket_impact_feedback(
                    pygame.Vector2(projectile.position),
                    impact_scale=0.85 * evolved_impact_scale,
                    end_of_range=True,
                )
                self._maybe_spawn_burst_rocket_fragments(projectile, pygame.Vector2(projectile.position))
                self._maybe_apply_big_pop_aoe(projectile, pygame.Vector2(projectile.position))
                self._pending_bottle_rocket_impact_sfx_count += 1
                continue
            active_projectiles.append(projectile)
        self.projectiles = active_projectiles
        active_sprays: list[ConfettiSpray] = []
        for spray in self.enemy_sprays:
            spray.update(delta_seconds)
            if player_contact_damage_enabled and player_collision_rect.colliderect(spray.rect):
                if self._apply_player_contact_damage():
                    return True
            if not spray.is_expired() and not spray.is_out_of_bounds(self.bounds):
                active_sprays.append(spray)
        self.enemy_sprays = active_sprays
        active_drops: list[XpDrop] = []
        for drop in self.xp_drops:
            drop.update(delta_seconds)
            if not drop.is_expired():
                active_drops.append(drop)
        self.xp_drops = active_drops
        self._apply_xp_drop_magnetism(player_center, delta_seconds)
        self._collect_xp_drops(player_collision_rect)
        
        # Check projectile-hazard collisions
        kills = self._check_projectile_collisions()
        kill_points_multiplier = self._score_multiplier_from_effects(effects)
        self.score_seconds += (kills * self.KILL_BONUS_POINTS) * kill_points_multiplier
        
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
            
            # Check if this is a boss level (every 10th level)
            if (
                self.current_level % self.BOSS_LEVEL_INTERVAL == 0
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
                base_speed=self._spawn_speed_with_upgrade_modifiers(
                    spawn_tier_config.enemy_speed * self.difficulty_multiplier
                ),
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
            if isinstance(hazard, StreamerSnake):
                if player_contact_damage_enabled and hazard.collides_with_rect(player_collision_rect):
                    if self._apply_player_contact_damage():
                        return True
            elif player_contact_damage_enabled and player_collision_rect.colliderect(hazard.rect):
                if self._apply_player_contact_damage():
                    return True

        if requested_burst_spawns > 0:
            available_slots = max(0, max_enemies - len(self.hazards))
            burst_spawns = min(requested_burst_spawns, available_slots, 2)
            for _ in range(burst_spawns):
                spawn_tier = self.spawn_controller.select_spawn_tier(level_config.level)
                spawn_tier_config = get_level_config(spawn_tier)
                hazard = self.spawn_controller.create_hazard_for_spawn_with_chances(
                    tier=spawn_tier,
                    base_speed=self._spawn_speed_with_upgrade_modifiers(
                        spawn_tier_config.enemy_speed * self.difficulty_multiplier
                    ),
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

        self._sync_attached_delayed_blast_projectiles()
        return False

    def fire_projectile(self, direction: pygame.Vector2) -> None:
        """Compatibility wrapper for active-weapon attack dispatch."""
        self.fire_active_weapon(direction)

    def set_active_weapon(self, weapon_id: str | None) -> None:
        definition = get_weapon_definition(weapon_id)
        self.active_weapon_id = definition.weapon_id
        self._active_weapon_definition = definition

    def active_weapon_snapshot(self) -> dict[str, int | float | str]:
        weapon = self._active_weapon_definition
        return {
            "weapon_id": weapon.weapon_id,
            "display_name": weapon.display_name,
            "weapon_type": weapon.weapon_type,
            "base_damage": int(weapon.base_damage),
            "effective_range": float(weapon.effective_range),
            "attack_cooldown_seconds": float(weapon.attack_cooldown_seconds),
        }

    def fire_active_weapon(self, direction: pygame.Vector2) -> None:
        weapon = self._active_weapon_definition
        if weapon.weapon_id == "sparkler":
            self.fire_sparkler(direction)
            return
        self.fire_bottle_rocket(direction)

    def fire_bottle_rocket(self, direction: pygame.Vector2) -> None:
        """Fire a bottle rocket in the given direction from the player center."""
        if self._weapon_cooldown_timer > 0.0:
            return
        if len(self.projectiles) >= self.max_active_projectiles:
            return
        player_center = pygame.Vector2(self.player.rect.center)
        resolved_direction = self._resolve_fire_direction(player_center, pygame.Vector2(direction))
        self._last_attack_direction = pygame.Vector2(resolved_direction)
        effects = self.run_upgrades.effects_snapshot()
        evolution_form_id = self._active_weapon_form_id("bottle_rocket")
        behavior_ids = self._weapon_behavior_ids("bottle_rocket")
        rocket_speed = self.BASE_PROJECTILE_SPEED * (1.0 + effects.get("projectile_speed_mult", 0.0))
        if "burst_rocket" in behavior_ids:
            rocket_speed *= 1.06
        if "big_pop_rocket" in behavior_ids:
            rocket_speed *= 1.03
        rocket_damage = (
            1
            + int(effects.get("projectile_damage", 0.0))
            + self._character_outgoing_damage_bonus
        )
        if behavior_ids & {"burst_rocket", "big_pop_rocket"}:
            rocket_damage += 1
        if self._cat_frenzy_timer > 0.0:
            rocket_damage += self.CAT_FRENZY_DAMAGE_BONUS
        rocket_damage = max(1, int(rocket_damage))
        fire_rate_mult = max(0.0, effects.get("fire_rate_mult", 0.0))
        if self._cat_frenzy_timer > 0.0:
            fire_rate_mult += self.CAT_FRENZY_FIRE_RATE_BONUS
        self._weapon_cooldown_timer = max(0.06, self.BASE_FIRE_COOLDOWN * (1.0 - fire_rate_mult))
        rocket = BottleRocket(
            position=player_center,
            direction=resolved_direction,
            speed=rocket_speed,
            lifetime=self.BOTTLE_ROCKET_LIFETIME,
            max_travel_distance=self.BOTTLE_ROCKET_MAX_TRAVEL_DISTANCE,
            size=8,
            damage=rocket_damage,
            flight_profile=self._current_bottle_rocket_flight_profile(),
        )
        if evolution_form_id is not None:
            setattr(rocket, "evolution_form_id", evolution_form_id)
        if behavior_ids:
            setattr(rocket, "evolution_behavior_ids", tuple(sorted(behavior_ids)))
        if "pinball_rocket" in behavior_ids:
            setattr(rocket, "pinball_bounces_remaining", int(self.PINBALL_ROCKET_MAX_BOUNCES))
            setattr(rocket, "pinball_hit_target_ids", set())
        self.projectiles.append(rocket)
        self.record_weapon_overlay_event("fire")
        self._spawn_bottle_rocket_launch_feedback(player_center, resolved_direction)
        self._pending_bottle_rocket_launch_sfx_count += 1
        self._apply_bottle_rocket_recoil(resolved_direction)

    def fire_sparkler(self, direction: pygame.Vector2) -> None:
        """Temporary sparkler melee hook for weapon-system foundation."""
        if self._weapon_cooldown_timer > 0.0:
            return
        weapon = self._active_weapon_definition
        effects = self.run_upgrades.effects_snapshot()
        profile = self._current_sparkler_attack_profile()
        cooldown = float(weapon.attack_cooldown_seconds) * max(0.35, float(profile.cooldown_multiplier))
        fire_rate_mult = max(0.0, effects.get("fire_rate_mult", 0.0))
        self._weapon_cooldown_timer = max(0.06, cooldown * max(0.2, 1.0 - fire_rate_mult))
        facing = self._resolve_sparkler_attack_direction(pygame.Vector2(direction))
        self._last_attack_direction = pygame.Vector2(facing)
        attack_range_bonus = max(0.0, effects.get("sparkler_range_bonus", 0.0))
        cone_bonus = max(0.0, effects.get("sparkler_cone_bonus_degrees", 0.0))
        damage_bonus = max(0, int(effects.get("sparkler_damage_bonus", 0.0)))
        evolution_form_id = self._active_weapon_form_id("sparkler")
        if evolution_form_id in ("orbiting_sparklers", "spark_aura"):
            return
        attack_range = max(
            24.0,
            float(weapon.effective_range) + float(profile.range_bonus) + float(attack_range_bonus),
        )
        cone_degrees = max(
            10.0,
            self.SPARKLER_SWEEP_CONE_DEGREES + float(profile.cone_bonus_degrees) + float(cone_bonus),
        )
        attack_damage = max(1, int(weapon.base_damage) + int(profile.damage_bonus) + int(damage_bonus))
        if evolution_form_id == "wide_arc_sparkler":
            attack_range += 16.0
            cone_degrees += 14.0
            attack_damage += 1
        elif evolution_form_id == "spark_aura":
            attack_range += 10.0
            cone_degrees += 10.0
            attack_damage += 1
        center = pygame.Vector2(self.player.rect.center) + (facing * 34.0)
        swing = self._sparkler_attack_shape(
            origin=pygame.Vector2(self.player.rect.center),
            direction=facing,
            attack_range=attack_range,
            cone_degrees=cone_degrees,
        )
        self._sparkler_attack_debug = {
            "origin": swing["origin"],
            "direction": swing["direction"],
            "cone_degrees": float(swing["cone_degrees"]),
            "range": float(swing["range"]),
            "inner_range": float(swing["inner_range"]),
            "tip_left": swing["tip_left"],
            "tip_right": swing["tip_right"],
            "expires_in": self.SPARKLER_SWEEP_DURATION,
            "swing_count": self._sparkler_swing_count + 1,
        }
        self._sparkler_swing_count += 1
        self._pending_sparkler_swing_sfx_count += 1
        self._apply_sparkler_melee_hits(
            origin=pygame.Vector2(self.player.rect.center),
            direction=facing,
            damage=attack_damage,
            attack_range=attack_range,
            cone_degrees=cone_degrees,
        )
        self.confetti.spawn_burst(
            center,
            count=4,
            speed_min=85.0,
            speed_max=140.0,
            lifetime_min=0.1,
            lifetime_max=0.18,
        )
        tip_center = pygame.Vector2(self.player.rect.center) + (facing * attack_range)
        tip_left = swing["tip_left"]
        tip_right = swing["tip_right"]
        if isinstance(tip_left, pygame.Vector2):
            self.confetti.spawn_burst(
                tip_left,
                count=2,
                speed_min=140.0,
                speed_max=230.0,
                lifetime_min=0.08,
                lifetime_max=0.16,
            )
        if isinstance(tip_right, pygame.Vector2):
            self.confetti.spawn_burst(
                tip_right,
                count=2,
                speed_min=140.0,
                speed_max=230.0,
                lifetime_min=0.08,
                lifetime_max=0.16,
            )
        self.confetti.spawn_burst(
            tip_center,
            count=3,
            speed_min=160.0,
            speed_max=260.0,
            lifetime_min=0.08,
            lifetime_max=0.16,
        )

    def sparkler_attack_snapshot(self) -> dict[str, object]:
        return dict(self._sparkler_attack_debug)

    def _resolve_sparkler_attack_direction(self, base_direction: pygame.Vector2) -> pygame.Vector2:
        candidate = pygame.Vector2(base_direction)
        if candidate.length_squared() <= 0.0:
            candidate = pygame.Vector2(self.player.facing)
        if candidate.length_squared() <= 0.0:
            candidate = pygame.Vector2(self._last_attack_direction)
        if candidate.length_squared() <= 0.0:
            candidate = pygame.Vector2(1.0, 0.0)
        return candidate.normalize()

    def _current_sparkler_attack_profile(self) -> SparklerAttackProfile:
        """Future hook for sparkler evolution/upgrade paths."""
        return SparklerAttackProfile()

    def _apply_sparkler_melee_hits(
        self,
        *,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        damage: int,
        attack_range: float,
        cone_degrees: float,
    ) -> None:
        hazards_to_remove: list[int] = []
        hazard_kill_positions: list[pygame.Vector2] = []
        hazard_kill_kinds: list[str] = []
        pinata_split_requests: list[dict[str, object]] = []
        super_charge_gained = 0
        sparkler_hit_contacts = 0

        for hazard_idx, hazard in enumerate(self.hazards):
            candidate_points = self._sparkler_target_points(hazard.rect)
            if not any(
                self._target_in_attack_arc(
                    origin=origin,
                    target=point,
                    direction=direction,
                    attack_range=attack_range,
                    cone_degrees=cone_degrees,
                )
                for point in candidate_points
            ):
                continue

            if isinstance(hazard, BossBalloon):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=damage,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                    self._pending_boss_hit_sfx_count += hit_count
                    super_charge_gained += hit_count * self.SUPER_CHARGE_PER_BOSS_HIT
                    sparkler_hit_contacts += 1
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                    self._bonus_score_points += self.BOSS_BONUS_POINTS * self._score_multiplier_from_effects(
                        self.run_upgrades.effects_snapshot()
                    )
                    hazard_kill_kinds.append("boss_balloon")
                    self._boss_active = False
                    self._boss_defeated = True
                    self._boss_defeated_level = self.current_level
                    self._boss_celebration_active = True
                    self._boss_defeat_timer = self.BOSS_CELEBRATION_TIME
                    self._boss_victory_sound_pending = True
                    self._pending_boss_defeat_sfx = True
                    self._pending_milestone_clear_sfx = True
                    self._pending_confetti_celebration_sfx = True
                    self._spawn_enhanced_confetti(pygame.Vector2(hazard.rect.center))
            elif isinstance(hazard, PinataEnemy):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=damage,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                    sparkler_hit_contacts += 1
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    center = pygame.Vector2(hazard.rect.center)
                    hazard_kill_positions.append(center)
                    hazard_kill_kinds.append("pinata")
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
                sparkler_hit_contacts += 1
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    center = pygame.Vector2(hazard.rect.center)
                    hazard_kill_positions.append(center)
                    hazard_kill_kinds.append("confetti_sprayer")
                    self._pending_balloon_pop_sfx_count += 1
                    self._pending_sprayer_destroy_sfx_count += 1
                    self._spawn_sprayer_destroy_confetti(center)
            elif isinstance(hazard, StreamerSnake):
                self._pending_balloon_hit_sfx_count += 1
                sparkler_hit_contacts += 1
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    center = pygame.Vector2(hazard.rect.center)
                    hazard_kill_positions.append(center)
                    hazard_kill_kinds.append("streamer_snake")
                    self._pending_balloon_pop_sfx_count += 1
                    self._spawn_streamer_snake_break_confetti(center)
            else:
                self._pending_balloon_hit_sfx_count += 1
                sparkler_hit_contacts += 1
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                    kind = str((hazard.spawn_profile or {}).get("enemy_kind", "balloon"))
                    hazard_kill_kinds.append(kind)
                    self._pending_balloon_pop_sfx_count += 1

        for idx in sorted(hazards_to_remove, reverse=True):
            self.hazards.pop(idx)

        for center in hazard_kill_positions:
            self.confetti.spawn_burst(center, count=8 + self._confetti_bonus_count())

        if pinata_split_requests:
            self._spawn_pinata_minis(pinata_split_requests)
        if hazard_kill_kinds:
            self._spawn_xp_drops_for_kills(hazard_kill_positions, hazard_kill_kinds)
            self.score_seconds += len(hazard_kill_kinds) * self.KILL_BONUS_POINTS * self._score_multiplier_from_effects(
                self.run_upgrades.effects_snapshot()
            )
            super_charge_gained += sum(
                self.SUPER_CHARGE_REWARDS.get(kind, 6) for kind in hazard_kill_kinds
            )
        if super_charge_gained > 0:
            self.add_super_charge(super_charge_gained)
        if sparkler_hit_contacts > 0:
            self._pending_sparkler_hit_sfx_count += sparkler_hit_contacts

    def _update_spark_aura(self, delta_seconds: float) -> None:
        if self.active_weapon_id != "sparkler":
            self._spark_aura_tick_timer = 0.0
            return
        if self._active_weapon_form_id("sparkler") != "spark_aura":
            self._spark_aura_tick_timer = 0.0
            return
        self._spark_aura_tick_timer += max(0.0, float(delta_seconds))
        while self._spark_aura_tick_timer >= self.SPARK_AURA_TICK_INTERVAL:
            self._spark_aura_tick_timer -= self.SPARK_AURA_TICK_INTERVAL
            self._apply_spark_aura_tick()

    def _update_orbiting_sparks(self, delta_seconds: float) -> None:
        if self.active_weapon_id != "sparkler":
            self._orbiting_spark_contact_cooldowns.clear()
            return
        if self._active_weapon_form_id("sparkler") != "orbiting_sparklers":
            self._orbiting_spark_contact_cooldowns.clear()
            return
        self._orbiting_spark_angle_degrees = (
            self._orbiting_spark_angle_degrees
            + (self.ORBITING_SPARK_ROTATION_DEGREES_PER_SECOND * max(0.0, float(delta_seconds)))
        ) % 360.0
        self._orbiting_spark_contact_cooldowns = {
            hazard_id: max(0.0, cooldown - max(0.0, float(delta_seconds)))
            for hazard_id, cooldown in self._orbiting_spark_contact_cooldowns.items()
            if cooldown > max(0.0, float(delta_seconds))
        }
        self._apply_orbiting_spark_contacts()

    def _orbiting_spark_positions(self) -> tuple[pygame.Vector2, ...]:
        center = pygame.Vector2(self.player.rect.center)
        count = max(1, int(self.ORBITING_SPARK_COUNT))
        step_degrees = 360.0 / count
        return tuple(
            center
            + pygame.Vector2(self.ORBITING_SPARK_RADIUS, 0.0).rotate(
                self._orbiting_spark_angle_degrees + (step_degrees * index)
            )
            for index in range(count)
        )

    def _apply_orbiting_spark_contacts(self) -> None:
        spark_positions = self._orbiting_spark_positions()
        hazards_to_remove: list[int] = []
        hazard_kill_positions: list[pygame.Vector2] = []
        hazard_kill_kinds: list[str] = []
        pinata_split_requests: list[dict[str, object]] = []
        super_charge_gained = 0
        contacts = 0

        for hazard_idx, hazard in enumerate(self.hazards):
            hazard_id = id(hazard)
            if self._orbiting_spark_contact_cooldowns.get(hazard_id, 0.0) > 0.0:
                continue
            if not any(
                self._orbiting_spark_intersects_rect(position, hazard.rect, self.ORBITING_SPARK_CONTACT_RADIUS)
                for position in spark_positions
            ):
                continue

            contacts += 1
            self._orbiting_spark_contact_cooldowns[hazard_id] = self.ORBITING_SPARK_CONTACT_COOLDOWN
            hazard_center = pygame.Vector2(hazard.rect.center)
            if isinstance(hazard, BossBalloon):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=self.ORBITING_SPARK_DAMAGE,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                    self._pending_boss_hit_sfx_count += hit_count
                    super_charge_gained += hit_count * self.SUPER_CHARGE_PER_BOSS_HIT
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(hazard_center)
                    hazard_kill_kinds.append("boss_balloon")
                    self._bonus_score_points += self.BOSS_BONUS_POINTS * self._score_multiplier_from_effects(
                        self.run_upgrades.effects_snapshot()
                    )
                    self._boss_active = False
                    self._boss_defeated = True
                    self._boss_defeated_level = self.current_level
                    self._boss_celebration_active = True
                    self._boss_defeat_timer = self.BOSS_CELEBRATION_TIME
                    self._boss_victory_sound_pending = True
                    self._pending_boss_defeat_sfx = True
                    self._pending_milestone_clear_sfx = True
                    self._pending_confetti_celebration_sfx = True
                    self._spawn_enhanced_confetti(hazard_center)
                continue

            if isinstance(hazard, PinataEnemy):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=self.ORBITING_SPARK_DAMAGE,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(hazard_center)
                    hazard_kill_kinds.append("pinata")
                    self._pending_balloon_pop_sfx_count += 1
                    profile = hazard.spawn_profile or {}
                    pinata_split_requests.append(
                        {
                            "center": hazard_center,
                            "tier": int(profile.get("tier", self.current_level)),
                            "flavor_tag": str(
                                profile.get("flavor_tag", self.current_level_config.flavor.name)
                            ),
                            "mini_spawn_count": max(0, int(profile.get("mini_spawn_count", 0))),
                        }
                    )
                    self._spawn_pinata_break_confetti(
                        hazard_center,
                        burst_count=max(10, int(profile.get("break_confetti_count", 14))),
                    )
                continue

            self._pending_balloon_hit_sfx_count += 1
            if isinstance(hazard, ConfettiSprayer):
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(hazard_center)
                    hazard_kill_kinds.append("confetti_sprayer")
                    self._pending_balloon_pop_sfx_count += 1
                    self._pending_sprayer_destroy_sfx_count += 1
                    self._spawn_sprayer_destroy_confetti(hazard_center)
                continue
            if isinstance(hazard, StreamerSnake):
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(hazard_center)
                    hazard_kill_kinds.append("streamer_snake")
                    self._pending_balloon_pop_sfx_count += 1
                    self._spawn_streamer_snake_break_confetti(hazard_center)
                continue
            if hazard_idx not in hazards_to_remove:
                hazards_to_remove.append(hazard_idx)
                hazard_kill_positions.append(hazard_center)
                hazard_kill_kinds.append(str((hazard.spawn_profile or {}).get("enemy_kind", "balloon")))
                self._pending_balloon_pop_sfx_count += 1

        for idx in sorted(hazards_to_remove, reverse=True):
            self._orbiting_spark_contact_cooldowns.pop(id(self.hazards[idx]), None)
            self.hazards.pop(idx)

        if pinata_split_requests:
            self._spawn_pinata_minis(pinata_split_requests)
        if hazard_kill_kinds:
            self._spawn_xp_drops_for_kills(hazard_kill_positions, hazard_kill_kinds)
            self.score_seconds += len(hazard_kill_kinds) * self.KILL_BONUS_POINTS * self._score_multiplier_from_effects(
                self.run_upgrades.effects_snapshot()
            )
            super_charge_gained += sum(self.SUPER_CHARGE_REWARDS.get(kind, 6) for kind in hazard_kill_kinds)
            for kill_pos in hazard_kill_positions:
                self.confetti.spawn_burst(
                    kill_pos,
                    count=5 + self._confetti_bonus_count(),
                    speed_min=105.0,
                    speed_max=185.0,
                    lifetime_min=0.14,
                    lifetime_max=0.24,
                )
        if super_charge_gained > 0:
            self.add_super_charge(super_charge_gained)
        if contacts > 0:
            self._pending_sparkler_hit_sfx_count += contacts

    def _orbiting_spark_intersects_rect(
        self,
        position: pygame.Vector2,
        rect: pygame.Rect,
        contact_radius: float,
    ) -> bool:
        closest_x = max(rect.left, min(int(position.x), rect.right))
        closest_y = max(rect.top, min(int(position.y), rect.bottom))
        closest_point = pygame.Vector2(float(closest_x), float(closest_y))
        return position.distance_squared_to(closest_point) <= float(contact_radius) ** 2

    def _apply_spark_aura_tick(self) -> None:
        center = pygame.Vector2(self.player.rect.center)
        aura_radius = self._current_spark_aura_radius()
        hazards_to_remove: list[int] = []
        hazard_kill_positions: list[pygame.Vector2] = []
        hazard_kill_kinds: list[str] = []
        super_charge_gained = 0
        contacts = 0
        for hazard_idx, hazard in enumerate(self.hazards):
            hazard_center = pygame.Vector2(hazard.rect.center)
            if center.distance_to(hazard_center) > aura_radius:
                continue
            contacts += 1
            if isinstance(hazard, BossBalloon):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=self.SPARK_AURA_DAMAGE,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                    self._pending_boss_hit_sfx_count += hit_count
                    super_charge_gained += hit_count * self.SUPER_CHARGE_PER_BOSS_HIT
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(hazard_center)
                    hazard_kill_kinds.append("boss_balloon")
                    self._bonus_score_points += self.BOSS_BONUS_POINTS * self._score_multiplier_from_effects(
                        self.run_upgrades.effects_snapshot()
                    )
                    self._boss_active = False
                    self._boss_defeated = True
                    self._boss_defeated_level = self.current_level
                    self._boss_celebration_active = True
                    self._boss_defeat_timer = self.BOSS_CELEBRATION_TIME
                    self._boss_victory_sound_pending = True
                    self._pending_boss_defeat_sfx = True
                    self._pending_milestone_clear_sfx = True
                    self._pending_confetti_celebration_sfx = True
                    self._spawn_enhanced_confetti(hazard_center)
                continue

            if isinstance(hazard, PinataEnemy):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=self.SPARK_AURA_DAMAGE,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(hazard_center)
                    hazard_kill_kinds.append("pinata")
                    self._pending_balloon_pop_sfx_count += 1
                continue

            self._pending_balloon_hit_sfx_count += 1
            if hazard_idx not in hazards_to_remove:
                hazards_to_remove.append(hazard_idx)
                hazard_kill_positions.append(hazard_center)
                hazard_kind = str((hazard.spawn_profile or {}).get("enemy_kind", "balloon"))
                hazard_kill_kinds.append(hazard_kind)
                self._pending_balloon_pop_sfx_count += 1

        for idx in sorted(hazards_to_remove, reverse=True):
            self.hazards.pop(idx)

        if hazard_kill_kinds:
            self._spawn_xp_drops_for_kills(hazard_kill_positions, hazard_kill_kinds)
            self.score_seconds += len(hazard_kill_kinds) * self.KILL_BONUS_POINTS * self._score_multiplier_from_effects(
                self.run_upgrades.effects_snapshot()
            )
            super_charge_gained += sum(self.SUPER_CHARGE_REWARDS.get(kind, 6) for kind in hazard_kill_kinds)
            for kill_pos in hazard_kill_positions:
                self.confetti.spawn_burst(
                    kill_pos,
                    count=6 + self._confetti_bonus_count(),
                    speed_min=120.0,
                    speed_max=220.0,
                    lifetime_min=0.18,
                    lifetime_max=0.3,
                )
        if super_charge_gained > 0:
            self.add_super_charge(super_charge_gained)
        if contacts > 0:
            self._pending_sparkler_hit_sfx_count += contacts

    def _current_spark_aura_radius(self) -> float:
        effects = self.run_upgrades.effects_snapshot()
        range_bonus = max(0.0, float(effects.get("sparkler_range_bonus", 0.0)))
        return self.SPARK_AURA_RADIUS + range_bonus

    def _target_in_attack_arc(
        self,
        *,
        origin: pygame.Vector2,
        target: pygame.Vector2,
        direction: pygame.Vector2,
        attack_range: float,
        cone_degrees: float,
    ) -> bool:
        to_target = pygame.Vector2(target) - pygame.Vector2(origin)
        distance = to_target.length()
        outer_range = max(24.0, float(attack_range))
        inner_range = outer_range * max(0.0, min(self.SPARKLER_ARC_INNER_RADIUS_RATIO, 0.9))
        if distance <= inner_range or distance > outer_range:
            return False
        target_dir = to_target.normalize()
        facing_dir = pygame.Vector2(direction)
        if facing_dir.length_squared() <= 0.0:
            facing_dir = pygame.Vector2(1.0, 0.0)
        else:
            facing_dir = facing_dir.normalize()
        dot = max(-1.0, min(1.0, facing_dir.dot(target_dir)))
        angle = abs(math.degrees(math.acos(dot)))
        return angle <= (max(5.0, float(cone_degrees)) * 0.5)

    def _sparkler_target_points(self, rect: pygame.Rect) -> tuple[pygame.Vector2, ...]:
        """Sample points across enemy body for melee overlap checks."""
        center = pygame.Vector2(rect.center)
        return (
            center,
            pygame.Vector2(rect.midtop),
            pygame.Vector2(rect.midbottom),
            pygame.Vector2(rect.midleft),
            pygame.Vector2(rect.midright),
            pygame.Vector2(rect.topleft),
            pygame.Vector2(rect.topright),
            pygame.Vector2(rect.bottomleft),
            pygame.Vector2(rect.bottomright),
        )

    def _sparkler_attack_shape(
        self,
        *,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        attack_range: float,
        cone_degrees: float,
    ) -> dict[str, object]:
        half_cone = max(5.0, float(cone_degrees) * 0.5)
        outer_range = max(24.0, float(attack_range))
        inner_range = outer_range * max(0.0, min(self.SPARKLER_ARC_INNER_RADIUS_RATIO, 0.9))
        tip_left = origin + (direction.rotate(-half_cone) * outer_range)
        tip_right = origin + (direction.rotate(half_cone) * outer_range)
        return {
            "origin": pygame.Vector2(origin),
            "direction": pygame.Vector2(direction),
            "range": outer_range,
            "inner_range": inner_range,
            "cone_degrees": float(cone_degrees),
            "tip_left": tip_left,
            "tip_right": tip_right,
        }

    def _draw_sparkler_attack_visual(self, surface: pygame.Surface) -> None:
        if not self._sparkler_attack_debug:
            return
        expires = float(self._sparkler_attack_debug.get("expires_in", 0.0))
        if expires <= 0.0:
            return
        origin = self._sparkler_attack_debug.get("origin")
        direction = self._sparkler_attack_debug.get("direction")
        cone_degrees = float(self._sparkler_attack_debug.get("cone_degrees", 0.0))
        outer_range = float(self._sparkler_attack_debug.get("range", 0.0))
        inner_range = float(self._sparkler_attack_debug.get("inner_range", 0.0))
        if not isinstance(origin, pygame.Vector2):
            return
        if not isinstance(direction, pygame.Vector2):
            return
        if direction.length_squared() <= 0.0 or outer_range <= 0.0:
            return
        facing = direction.normalize()

        strength = max(0.0, min(expires / self.SPARKLER_SWEEP_DURATION, 1.0))
        glow_alpha = int(110 + (95 * strength))
        core_alpha = int(190 + (60 * strength))
        swing_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        outer_points = self._sparkler_arc_points(
            origin=origin,
            direction=facing,
            radius=outer_range,
            cone_degrees=cone_degrees,
            segments=18,
        )
        inner_points = self._sparkler_arc_points(
            origin=origin,
            direction=facing,
            radius=max(2.0, inner_range),
            cone_degrees=cone_degrees,
            segments=18,
        )
        if len(outer_points) >= 2:
            pygame.draw.lines(
                swing_surface,
                (255, 170, 70, glow_alpha),
                False,
                outer_points,
                width=max(8, int((outer_range - inner_range) * 0.5)),
            )
            pygame.draw.lines(
                swing_surface,
                (255, 228, 130, core_alpha),
                False,
                outer_points,
                width=3,
            )
            pygame.draw.lines(
                swing_surface,
                (255, 250, 232, min(255, core_alpha + 14)),
                False,
                outer_points,
                width=1,
            )
        if inner_range > 2.0 and len(inner_points) >= 2:
            pygame.draw.lines(
                swing_surface,
                (255, 146, 72, core_alpha),
                False,
                inner_points,
                width=2,
            )

        # Spark crackles distributed across the arc for a celebratory sparkler feel.
        swing_seed = int(self._sparkler_attack_debug.get("swing_count", 0))
        for index, point in enumerate(outer_points):
            if index % 2 != 0:
                continue
            phase = abs(math.sin((swing_seed * 0.9) + (index * 0.55)))
            sparkle_alpha = int((120 + (130 * phase)) * strength)
            if sparkle_alpha <= 0:
                continue
            sparkle_radius = 1 + int(phase * 2.0)
            pygame.draw.circle(
                swing_surface,
                (255, 244, 196, min(255, sparkle_alpha)),
                (int(point[0]), int(point[1])),
                sparkle_radius,
            )

        # Sparkler baton/wand segment near the player's hand.
        baton_start = origin + (facing * max(4.0, inner_range * 0.28))
        baton_end = origin + (facing * max(14.0, inner_range * 0.92))
        pygame.draw.line(
            swing_surface,
            (84, 58, 36, int(180 * strength)),
            baton_start,
            baton_end,
            width=4,
        )
        pygame.draw.line(
            swing_surface,
            (255, 236, 154, int(220 * strength)),
            baton_start,
            baton_end,
            width=2,
        )
        baton_tip = baton_end + (facing * 2.0)
        pygame.draw.circle(
            swing_surface,
            (255, 248, 210, int(230 * strength)),
            (int(baton_tip.x), int(baton_tip.y)),
            3,
        )
        surface.blit(swing_surface, (0, 0))

    def _sparkler_arc_points(
        self,
        *,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        radius: float,
        cone_degrees: float,
        segments: int = 14,
    ) -> list[tuple[float, float]]:
        half_cone = max(5.0, float(cone_degrees) * 0.5)
        clamped_segments = max(4, int(segments))
        step = (half_cone * 2.0) / float(clamped_segments)
        points: list[tuple[float, float]] = []
        for index in range(clamped_segments + 1):
            angle = -half_cone + (step * index)
            point = pygame.Vector2(origin) + (pygame.Vector2(direction).rotate(angle) * radius)
            points.append((point.x, point.y))
        return points

    def _resolve_fire_direction(self, origin: pygame.Vector2, base_direction: pygame.Vector2) -> pygame.Vector2:
        target_centers = [pygame.Vector2(hazard.rect.center) for hazard in self.hazards]
        target = self._aim_assist.select_target(
            origin=origin,
            aim_direction=base_direction,
            target_centers=target_centers,
        )
        adjusted = self._aim_assist.adjusted_direction(
            origin=origin,
            aim_direction=base_direction,
            target_centers=target_centers,
        )
        self._aim_assist_debug = {
            "origin": pygame.Vector2(origin),
            "base_direction": pygame.Vector2(base_direction).normalize() if pygame.Vector2(base_direction).length_squared() > 0 else pygame.Vector2(1.0, 0.0),
            "adjusted_direction": pygame.Vector2(adjusted),
            "target_center": pygame.Vector2(target.center) if target is not None else None,
            "enabled": bool(self._aim_assist.config.enabled),
            "cone_degrees": float(self._aim_assist.config.cone_degrees),
            "max_distance": float(self._aim_assist.config.max_distance),
        }
        return adjusted

    def trigger_player_dodge(self, movement_input: pygame.Vector2) -> bool:
        triggered = self.player.try_start_dodge(movement_input)
        if triggered:
            center = pygame.Vector2(self.player.rect.center)
            self.confetti.spawn_burst(center, count=8, speed_min=150.0, speed_max=260.0, lifetime_min=0.25, lifetime_max=0.45)
            self._spawn_pulse_centers.append((int(center.x), int(center.y)))
        return triggered

    def set_active_input_method(self, input_method: str) -> None:
        self._active_input_method = str(input_method)
        self._refresh_aim_assist_config()

    def set_aim_assist_user_enabled(self, enabled: bool) -> None:
        self._aim_assist_user_enabled = bool(enabled)
        self._refresh_aim_assist_config()

    def _refresh_aim_assist_config(self) -> None:
        controller_active = self._active_input_method == "controller"
        input_default = self.AIM_ASSIST_CONTROLLER_ENABLED if controller_active else self.AIM_ASSIST_KEYBOARD_ENABLED
        enabled = bool(self._aim_assist_user_enabled and input_default)
        self._aim_assist.config = AimAssistConfig(
            enabled=enabled,
            cone_degrees=self._aim_assist.config.cone_degrees,
            max_distance=self._aim_assist.config.max_distance,
            assist_strength=self._aim_assist.config.assist_strength,
        )

    def draw_aim_assist_debug_overlay(self, surface: pygame.Surface) -> None:
        if not self._aim_assist_debug:
            return
        origin = self._aim_assist_debug.get("origin")
        base_direction = self._aim_assist_debug.get("base_direction")
        adjusted_direction = self._aim_assist_debug.get("adjusted_direction")
        target_center = self._aim_assist_debug.get("target_center")
        if not isinstance(origin, pygame.Vector2) or not isinstance(base_direction, pygame.Vector2):
            return

        max_distance = float(self._aim_assist_debug.get("max_distance", 0.0))
        cone_degrees = float(self._aim_assist_debug.get("cone_degrees", 0.0))
        enabled = bool(self._aim_assist_debug.get("enabled", False))
        color = (130, 235, 255) if enabled else (120, 120, 130)

        left = base_direction.rotate(-cone_degrees) * max_distance
        right = base_direction.rotate(cone_degrees) * max_distance
        pygame.draw.line(surface, color, origin, origin + left, width=1)
        pygame.draw.line(surface, color, origin, origin + right, width=1)
        pygame.draw.circle(surface, color, (int(origin.x), int(origin.y)), int(max_distance), width=1)

        if isinstance(adjusted_direction, pygame.Vector2):
            pygame.draw.line(surface, (255, 230, 150), origin, origin + (adjusted_direction * 130.0), width=2)
        pygame.draw.line(surface, (180, 210, 255), origin, origin + (base_direction * 120.0), width=1)
        if isinstance(target_center, pygame.Vector2):
            pygame.draw.circle(surface, (255, 130, 130), (int(target_center.x), int(target_center.y)), 8, width=2)

    @property
    def pending_run_level_ups(self) -> int:
        return self.run_progression.pending_level_ups

    @property
    def run_level(self) -> int:
        return self.run_progression.run_level

    def run_progress_snapshot(self) -> dict[str, int | float]:
        return self.run_progression.snapshot()

    def current_upgrade_choices(self) -> list[UpgradeDefinition]:
        return list(self._current_upgrade_choices)

    def current_upgrade_choice_previews(self) -> list[dict[str, object]]:
        acquired_tags = self.run_upgrades.acquired_tags()
        triggered_ids = self._weapon_evolution_tracker.triggered_ids()
        previews: list[dict[str, object]] = []
        for option in self._current_upgrade_choices:
            preview_evolutions = []
            allow_additional_evolution = (
                self.active_weapon_id not in self._weapon_evolution_forms
                or self.active_weapon_id == "bottle_rocket"
            )
            if allow_additional_evolution:
                preview_evolutions = preview_weapon_evolutions_with_added_tags(
                    weapon_id=self.active_weapon_id,
                    acquired_tags=acquired_tags,
                    added_tags=option.tags,
                    exclude_evolution_ids=triggered_ids,
                )
            evolution_ids = tuple(item.evolution_id for item in preview_evolutions)
            previews.append(
                {
                    "id": option.id,
                    "name": option.name,
                    "description": option.description,
                    "leads_to_evolution": bool(preview_evolutions),
                    "evolution_ids": evolution_ids,
                }
            )
        return previews

    def ensure_upgrade_choices(self) -> list[UpgradeDefinition]:
        if not self._current_upgrade_choices:
            self._current_upgrade_choices = self.run_upgrades.generate_choices(
                count=3,
                active_weapon_id=self.active_weapon_id,
                evolution_exclude_ids=self._weapon_evolution_tracker.triggered_ids(),
            )
            if not self._current_upgrade_choices and self.run_progression.pending_level_ups > 0:
                self.run_progression.consume_pending_level_up()
        return list(self._current_upgrade_choices)

    def apply_upgrade_choice_by_index(self, index: int) -> bool:
        if not self._current_upgrade_choices:
            return False
        if index < 0 or index >= len(self._current_upgrade_choices):
            return False
        chosen = self._current_upgrade_choices[index]
        if not self.run_upgrades.apply_choice(chosen.id, active_weapon_id=self.active_weapon_id):
            return False
        new_evolutions = []
        allow_additional_evolution = (
            self.active_weapon_id not in self._weapon_evolution_forms
            or self.active_weapon_id == "bottle_rocket"
        )
        if allow_additional_evolution:
            new_evolutions = self._weapon_evolution_tracker.check_for_new(
                weapon_id=self.active_weapon_id,
                acquired_tags=self.run_upgrades.acquired_tags(),
            )
        activated_labels: list[str] = []
        for evolution in new_evolutions:
            behavior_ids = self._weapon_evolution_behavior_ids.setdefault(evolution.weapon_id, set())
            behavior_ids.add(evolution.result_form_id)
            if evolution.weapon_id not in self._weapon_evolution_forms:
                self._weapon_evolution_forms[evolution.weapon_id] = evolution.result_form_id
            self.record_weapon_overlay_event("evolution")
            activated_labels.append(evolution.result_form_id.replace("_", " ").title())
        if activated_labels:
            self._trigger_evolution_feedback(activated_labels[0])
        self.run_progression.consume_pending_level_up()
        self._current_upgrade_choices = []
        return True

    def weapon_evolution_snapshot(self) -> dict[str, object]:
        return {
            "triggered_evolution_ids": self._weapon_evolution_tracker.triggered_ids(),
            "active_forms_by_weapon": dict(self._weapon_evolution_forms),
            "active_behavior_ids_by_weapon": {
                weapon_id: tuple(sorted(ids))
                for weapon_id, ids in self._weapon_evolution_behavior_ids.items()
            },
        }

    def _active_weapon_form_id(self, weapon_id: str) -> str | None:
        return self._weapon_evolution_forms.get(str(weapon_id))

    def _weapon_behavior_ids(self, weapon_id: str) -> set[str]:
        resolved_weapon_id = str(weapon_id)
        behavior_ids = set(self._weapon_evolution_behavior_ids.get(resolved_weapon_id, set()))
        active_form_id = self._active_weapon_form_id(resolved_weapon_id)
        if active_form_id:
            behavior_ids.add(active_form_id)
        return behavior_ids

    def _projectile_has_bottle_rocket_behavior(self, projectile: BottleRocket, behavior_id: str) -> bool:
        behavior_ids = {
            str(item)
            for item in getattr(projectile, "evolution_behavior_ids", ())
        }
        form_id = str(getattr(projectile, "evolution_form_id", "") or "")
        if form_id:
            behavior_ids.add(form_id)
        return str(behavior_id) in behavior_ids

    def _bottle_rocket_impact_scale(self, projectile: BottleRocket) -> float:
        if self._projectile_has_bottle_rocket_behavior(projectile, "big_pop_rocket"):
            return 1.35
        if self._projectile_has_bottle_rocket_behavior(projectile, "burst_rocket"):
            return 1.15
        if self._projectile_has_bottle_rocket_behavior(projectile, "delayed_blast_rocket"):
            return 1.2
        if self._projectile_has_bottle_rocket_behavior(projectile, "pinball_rocket"):
            return 1.1
        return 1.0

    def _find_pinball_bounce_target(self, projectile: BottleRocket, hit_hazard: Hazard) -> Hazard | None:
        origin = pygame.Vector2(hit_hazard.rect.center)
        hit_target_ids = {int(item) for item in getattr(projectile, "pinball_hit_target_ids", set())}

        def _closest(*, allow_previously_hit: bool) -> Hazard | None:
            closest_target: Hazard | None = None
            closest_distance = float("inf")
            for candidate in self.hazards:
                if candidate is hit_hazard:
                    continue
                candidate_id = id(candidate)
                if not allow_previously_hit and candidate_id in hit_target_ids:
                    continue
                candidate_center = pygame.Vector2(candidate.rect.center)
                distance = origin.distance_to(candidate_center)
                if distance > self.PINBALL_ROCKET_SEARCH_RADIUS:
                    continue
                if distance < closest_distance:
                    closest_distance = distance
                    closest_target = candidate
            return closest_target

        return _closest(allow_previously_hit=False) or _closest(allow_previously_hit=True)

    def _try_redirect_pinball_rocket(self, projectile: BottleRocket, hit_hazard: Hazard) -> bool:
        if not self._projectile_has_bottle_rocket_behavior(projectile, "pinball_rocket"):
            return False
        bounces_remaining = int(getattr(projectile, "pinball_bounces_remaining", 0))
        if bounces_remaining <= 0:
            return False
        hit_target_ids = {int(item) for item in getattr(projectile, "pinball_hit_target_ids", set())}
        hit_target_ids.add(id(hit_hazard))
        setattr(projectile, "pinball_hit_target_ids", hit_target_ids)
        next_target = self._find_pinball_bounce_target(projectile, hit_hazard)
        if next_target is None:
            return False
        bounce_origin = pygame.Vector2(hit_hazard.rect.center)
        target_center = pygame.Vector2(next_target.rect.center)
        redirect = target_center - bounce_origin
        if redirect.length_squared() <= 0.0:
            return False
        redirect = redirect.normalize()
        projectile.direction = pygame.Vector2(redirect)
        projectile.position = bounce_origin + (redirect * max(16.0, float(hit_hazard.rect.width) * 0.65))
        setattr(projectile, "pinball_bounces_remaining", bounces_remaining - 1)
        return True

    def _try_attach_delayed_blast_rocket(self, projectile: BottleRocket, hazard: Hazard) -> bool:
        if not self._projectile_has_bottle_rocket_behavior(projectile, "delayed_blast_rocket"):
            return False
        target_id = id(hazard)
        if target_id in self._sticky_rocket_target_ids:
            return False
        self._sticky_rocket_target_ids.add(target_id)
        sticky_position = pygame.Vector2(hazard.rect.center)
        projectile.position = pygame.Vector2(sticky_position)
        setattr(projectile, "is_sticky_attached", True)
        setattr(projectile, "sticky_target", hazard)
        setattr(projectile, "sticky_target_id", target_id)
        setattr(projectile, "sticky_fuse_duration", float(self.DELAYED_BLAST_FUSE_SECONDS))
        setattr(projectile, "sticky_timer_remaining", float(self.DELAYED_BLAST_FUSE_SECONDS))
        setattr(projectile, "sticky_last_position", pygame.Vector2(sticky_position))
        setattr(projectile, "sticky_buildup_triggered", False)
        return True

    def _release_delayed_blast_target(self, projectile: BottleRocket) -> None:
        target_id = getattr(projectile, "sticky_target_id", None)
        if target_id is not None:
            self._sticky_rocket_target_ids.discard(int(target_id))
        setattr(projectile, "sticky_target", None)
        setattr(projectile, "sticky_target_id", None)

    def _update_delayed_blast_projectile(self, projectile: BottleRocket, delta_seconds: float) -> bool:
        target = getattr(projectile, "sticky_target", None)
        if target in self.hazards:
            sticky_position = pygame.Vector2(target.rect.center)
            projectile.position = pygame.Vector2(sticky_position)
            setattr(projectile, "sticky_last_position", pygame.Vector2(sticky_position))
        projectile._age += max(0.0, delta_seconds)  # type: ignore[attr-defined]
        sticky_timer_remaining = max(
            0.0,
            float(getattr(projectile, "sticky_timer_remaining", self.DELAYED_BLAST_FUSE_SECONDS)) - max(0.0, delta_seconds),
        )
        setattr(projectile, "sticky_timer_remaining", sticky_timer_remaining)
        if (
            sticky_timer_remaining <= (self.DELAYED_BLAST_BUILDUP_WINDOW + 1e-6)
            and not bool(getattr(projectile, "sticky_buildup_triggered", False))
        ):
            buildup_center = pygame.Vector2(getattr(projectile, "sticky_last_position", projectile.position))
            self.confetti.spawn_burst(
                buildup_center,
                count=5,
                speed_min=60.0,
                speed_max=130.0,
                lifetime_min=0.42,
                lifetime_max=0.58,
            )
            self._spawn_pulse_centers.append((int(buildup_center.x), int(buildup_center.y)))
            setattr(projectile, "sticky_buildup_triggered", True)
        if sticky_timer_remaining > 0.0 and target in self.hazards:
            return False
        self._detonate_delayed_blast_rocket(projectile)
        return True

    def _sync_attached_delayed_blast_projectiles(self) -> None:
        for projectile in self.projectiles:
            if not bool(getattr(projectile, "is_sticky_attached", False)):
                continue
            target = getattr(projectile, "sticky_target", None)
            if target not in self.hazards:
                continue
            sticky_position = pygame.Vector2(target.rect.center)
            projectile.position = pygame.Vector2(sticky_position)
            setattr(projectile, "sticky_last_position", pygame.Vector2(sticky_position))

    def _detonate_delayed_blast_rocket(self, projectile: BottleRocket) -> None:
        target = getattr(projectile, "sticky_target", None)
        center = pygame.Vector2(getattr(projectile, "sticky_last_position", projectile.position))
        if target in self.hazards:
            center = pygame.Vector2(target.rect.center)
        self._release_delayed_blast_target(projectile)
        setattr(projectile, "is_sticky_attached", False)
        self._spawn_bottle_rocket_impact_feedback(center, impact_scale=1.2, end_of_range=False)
        self._pending_bottle_rocket_impact_sfx_count += 1

        if target not in self.hazards:
            return

        damage = int(getattr(projectile, "damage", 1))
        if isinstance(target, BossBalloon):
            hit_count, defeated = self._apply_damage_to_multi_hit_enemy(target, projectile_damage=damage)
            if hit_count > 0:
                self._pending_balloon_hit_sfx_count += hit_count
                self._pending_boss_hit_sfx_count += hit_count
                self.add_super_charge(hit_count * self.SUPER_CHARGE_PER_BOSS_HIT)
            if defeated:
                self._bonus_score_points += self.BOSS_BONUS_POINTS * self._score_multiplier_from_effects(
                    self.run_upgrades.effects_snapshot()
                )
                self.hazards.remove(target)
                self._spawn_xp_drops_for_kills([pygame.Vector2(center)], ["boss_balloon"])
                self._boss_active = False
                self._boss_defeated = True
                self._boss_defeated_level = self.current_level
                self._boss_celebration_active = True
                self._boss_defeat_timer = self.BOSS_CELEBRATION_TIME
                self._boss_victory_sound_pending = True
                self._pending_boss_defeat_sfx = True
                self._pending_milestone_clear_sfx = True
                self._pending_confetti_celebration_sfx = True
                self._spawn_enhanced_confetti(center)
            return

        if isinstance(target, PinataEnemy):
            hit_count, defeated = self._apply_damage_to_multi_hit_enemy(target, projectile_damage=damage)
            if hit_count > 0:
                self._pending_balloon_hit_sfx_count += hit_count
            if defeated:
                profile = target.spawn_profile or {}
                self.hazards.remove(target)
                self._spawn_xp_drops_for_kills([pygame.Vector2(center)], ["pinata"])
                self._pending_balloon_pop_sfx_count += 1
                self._spawn_pinata_break_confetti(
                    center,
                    burst_count=max(10, int(profile.get("break_confetti_count", 14))),
                )
                self._spawn_pinata_minis(
                    [
                        {
                            "center": pygame.Vector2(center),
                            "tier": int(profile.get("tier", self.current_level)),
                            "flavor_tag": str(profile.get("flavor_tag", self.current_level_config.flavor.name)),
                            "mini_spawn_count": max(0, int(profile.get("mini_spawn_count", 0))),
                        }
                    ]
                )
            return

        self._pending_balloon_hit_sfx_count += 1
        self._pending_balloon_pop_sfx_count += 1
        if isinstance(target, ConfettiSprayer):
            self._pending_sprayer_destroy_sfx_count += 1
            self._spawn_sprayer_destroy_confetti(center)
            enemy_kind = "confetti_sprayer"
        elif isinstance(target, StreamerSnake):
            self._spawn_streamer_snake_break_confetti(center)
            enemy_kind = "streamer_snake"
        else:
            enemy_kind = str((target.spawn_profile or {}).get("enemy_kind", "balloon"))

        self.hazards.remove(target)
        self._spawn_xp_drops_for_kills([pygame.Vector2(center)], [enemy_kind])
        self.add_super_charge(self.SUPER_CHARGE_REWARDS.get(enemy_kind, 6))

    def _trigger_evolution_feedback(self, label: str) -> None:
        self._pending_evolution_sfx_count += 1
        self._evolution_feedback_timer = 1.15
        self._evolution_feedback_label = str(label)
        self._evolution_pause_timer = max(self._evolution_pause_timer, 0.12)
        center = pygame.Vector2(self.player.rect.center)
        self.confetti.spawn_burst(
            center,
            count=22 + self._confetti_bonus_count(),
            speed_min=210.0,
            speed_max=360.0,
            lifetime_min=0.28,
            lifetime_max=0.46,
        )
        self._spawn_pulse_centers.append((int(center.x), int(center.y)))

    def _maybe_spawn_burst_rocket_fragments(
        self,
        projectile: BottleRocket,
        center: pygame.Vector2,
    ) -> None:
        if not self._projectile_has_bottle_rocket_behavior(projectile, "burst_rocket"):
            return
        if bool(getattr(projectile, "is_burst_fragment", False)):
            return
        base_direction = pygame.Vector2(projectile.direction)
        if base_direction.length_squared() <= 0.0:
            base_direction = pygame.Vector2(1.0, 0.0)
        else:
            base_direction = base_direction.normalize()

        fragment_count = max(2, int(self.BURST_ROCKET_FRAGMENT_COUNT))
        half_spread = max(6.0, float(self.BURST_ROCKET_FRAGMENT_SPREAD_DEGREES) * 0.5)
        if fragment_count <= 1:
            angles = (0.0,)
        else:
            step = (half_spread * 2.0) / max(1, fragment_count - 1)
            angles = tuple((-half_spread + (step * index)) for index in range(fragment_count))

        base_damage = max(1, int(getattr(projectile, "damage", 1)) - 1)
        base_speed = max(180.0, float(projectile.speed) * self.BURST_ROCKET_FRAGMENT_SPEED_MULT)
        for angle in angles:
            fragment = BottleRocket(
                position=pygame.Vector2(center),
                direction=base_direction.rotate(angle),
                speed=base_speed,
                lifetime=self.BURST_ROCKET_FRAGMENT_LIFETIME,
                max_travel_distance=self.BURST_ROCKET_FRAGMENT_MAX_TRAVEL_DISTANCE,
                size=6,
                damage=base_damage,
                flight_profile=self._current_bottle_rocket_flight_profile(),
            )
            setattr(fragment, "is_burst_fragment", True)
            self.projectiles.append(fragment)

    def _maybe_apply_big_pop_aoe(self, projectile: BottleRocket, center: pygame.Vector2) -> None:
        if not self._projectile_has_bottle_rocket_behavior(projectile, "big_pop_rocket"):
            return
        center_vec = pygame.Vector2(center)
        hazards_to_remove: list[int] = []
        hazard_kill_positions: list[pygame.Vector2] = []
        hazard_kill_kinds: list[str] = []
        for hazard_idx, hazard in enumerate(self.hazards):
            if isinstance(hazard, (BossBalloon, PinataEnemy)):
                continue
            hazard_center = pygame.Vector2(hazard.rect.center)
            if center_vec.distance_to(hazard_center) > self.BIG_POP_ROCKET_RADIUS:
                continue
            hazards_to_remove.append(hazard_idx)
            hazard_kill_positions.append(hazard_center)
            hazard_kind = str((hazard.spawn_profile or {}).get("enemy_kind", "balloon"))
            hazard_kill_kinds.append(hazard_kind)
            self._pending_balloon_pop_sfx_count += 1
            if isinstance(hazard, ConfettiSprayer):
                self._pending_sprayer_destroy_sfx_count += 1
                self._spawn_sprayer_destroy_confetti(hazard_center)
            elif isinstance(hazard, StreamerSnake):
                self._spawn_streamer_snake_break_confetti(hazard_center)

        if not hazards_to_remove:
            return

        self._pending_balloon_hit_sfx_count += len(hazards_to_remove)
        for idx in sorted(set(hazards_to_remove), reverse=True):
            self.hazards.pop(idx)

        self._spawn_xp_drops_for_kills(hazard_kill_positions, hazard_kill_kinds)
        self.score_seconds += len(hazard_kill_kinds) * self.KILL_BONUS_POINTS * self._score_multiplier_from_effects(
            self.run_upgrades.effects_snapshot()
        )
        self.add_super_charge(
            sum(self.SUPER_CHARGE_REWARDS.get(kind, 6) for kind in hazard_kill_kinds)
        )
        for kill_pos in hazard_kill_positions:
            self.confetti.spawn_burst(
                kill_pos,
                count=8 + self._confetti_bonus_count(),
                speed_min=160.0,
                speed_max=290.0,
                lifetime_min=0.22,
                lifetime_max=0.38,
            )

    def _check_projectile_collisions(self) -> int:
        """Check projectile-hazard collisions and remove entities on hit.
        
        Returns:
            Number of hazards killed in this frame.
        """
        hazards_to_remove_ids: set[int] = set()
        hazards_to_remove: list[object] = []
        projectiles_to_remove = []
        hazard_kill_positions = []
        hazard_kill_kinds: list[str] = []
        pinata_split_requests: list[dict[str, object]] = []
        super_charge_gained = 0
        
        for proj_idx, projectile in enumerate(self.projectiles):
            if bool(getattr(projectile, "is_sticky_attached", False)):
                continue
            for hazard_idx, hazard in enumerate(self.hazards):
                if projectile.rect.colliderect(hazard.rect):
                    did_pinball_bounce = self._try_redirect_pinball_rocket(projectile, hazard)
                    if self._try_attach_delayed_blast_rocket(projectile, hazard):
                        break
                    should_emit_impact_feedback = proj_idx not in projectiles_to_remove or did_pinball_bounce
                    if proj_idx not in projectiles_to_remove and not did_pinball_bounce:
                        projectiles_to_remove.append(proj_idx)
                    if should_emit_impact_feedback:
                        evolved_impact_scale = self._bottle_rocket_impact_scale(projectile)
                        self._spawn_bottle_rocket_impact_feedback(
                            pygame.Vector2(projectile.position),
                            impact_scale=1.0 * evolved_impact_scale,
                            end_of_range=False,
                        )
                        self._maybe_spawn_burst_rocket_fragments(projectile, pygame.Vector2(projectile.position))
                        self._maybe_apply_big_pop_aoe(projectile, pygame.Vector2(projectile.position))
                        self._pending_bottle_rocket_impact_sfx_count += 1
                    
                    # Handle boss health
                    if isinstance(hazard, BossBalloon):
                        hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                            hazard,
                            projectile_damage=int(getattr(projectile, "damage", 1)),
                        )
                        if hit_count > 0:
                            self._pending_balloon_hit_sfx_count += hit_count
                            self._pending_boss_hit_sfx_count += hit_count
                            super_charge_gained += hit_count * self.SUPER_CHARGE_PER_BOSS_HIT
                        if defeated:
                            # Boss defeated - award bonus and enhanced feedback
                            hazard_id = id(hazard)
                            if hazard_id not in hazards_to_remove_ids:
                                hazards_to_remove_ids.add(hazard_id)
                                hazards_to_remove.append(hazard)
                                hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                                self._bonus_score_points += self.BOSS_BONUS_POINTS * self._score_multiplier_from_effects(
                                    self.run_upgrades.effects_snapshot()
                                )
                                hazard_kill_kinds.append("boss_balloon")
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
                        hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                            hazard,
                            projectile_damage=int(getattr(projectile, "damage", 1)),
                        )
                        if hit_count > 0:
                            self._pending_balloon_hit_sfx_count += hit_count
                        hazard_id = id(hazard)
                        if defeated and hazard_id not in hazards_to_remove_ids:
                            hazards_to_remove_ids.add(hazard_id)
                            hazards_to_remove.append(hazard)
                            center = pygame.Vector2(hazard.rect.center)
                            hazard_kill_positions.append(center)
                            hazard_kill_kinds.append("pinata")
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
                        hazard_id = id(hazard)
                        if hazard_id not in hazards_to_remove_ids:
                            hazards_to_remove_ids.add(hazard_id)
                            hazards_to_remove.append(hazard)
                            center = pygame.Vector2(hazard.rect.center)
                            hazard_kill_positions.append(center)
                            hazard_kill_kinds.append("confetti_sprayer")
                            self._pending_balloon_pop_sfx_count += 1
                            self._pending_sprayer_destroy_sfx_count += 1
                            self._spawn_sprayer_destroy_confetti(center)
                    elif isinstance(hazard, StreamerSnake):
                        self._pending_balloon_hit_sfx_count += 1
                        hazard_id = id(hazard)
                        if hazard_id not in hazards_to_remove_ids:
                            hazards_to_remove_ids.add(hazard_id)
                            hazards_to_remove.append(hazard)
                            center = pygame.Vector2(hazard.rect.center)
                            hazard_kill_positions.append(center)
                            hazard_kill_kinds.append("streamer_snake")
                            self._pending_balloon_pop_sfx_count += 1
                            self._spawn_streamer_snake_break_confetti(center)
                    else:
                        # Normal hazard - instant kill
                        self._pending_balloon_hit_sfx_count += 1
                        hazard_id = id(hazard)
                        if hazard_id not in hazards_to_remove_ids:
                            hazards_to_remove_ids.add(hazard_id)
                            hazards_to_remove.append(hazard)
                            hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                            kind = str((hazard.spawn_profile or {}).get("enemy_kind", "balloon"))
                            hazard_kill_kinds.append(kind)
                            self._pending_balloon_pop_sfx_count += 1
                    if did_pinball_bounce:
                        break
        
        removed_hazard_count = 0
        for hazard in hazards_to_remove:
            if hazard in self.hazards:
                self.hazards.remove(hazard)
                removed_hazard_count += 1
        
        for idx in sorted(projectiles_to_remove, reverse=True):
            self.projectiles.pop(idx)
        
        # Spawn confetti at kill locations
        for center in hazard_kill_positions:
            self.confetti.spawn_burst(center, count=8 + self._confetti_bonus_count())

        if pinata_split_requests:
            self._spawn_pinata_minis(pinata_split_requests)
        if hazard_kill_kinds:
            self._spawn_xp_drops_for_kills(hazard_kill_positions, hazard_kill_kinds)
            super_charge_gained += sum(
                self.SUPER_CHARGE_REWARDS.get(kind, 6) for kind in hazard_kill_kinds
            )
        if super_charge_gained > 0:
            self.add_super_charge(super_charge_gained)

        return removed_hazard_count

    def _apply_damage_to_multi_hit_enemy(self, hazard: object, *, projectile_damage: int) -> tuple[int, bool]:
        hits_registered = 0
        defeated = False
        for idx in range(max(1, int(projectile_damage))):
            if idx > 0 and hasattr(hazard, "hit_invuln_timer"):
                setattr(hazard, "hit_invuln_timer", 0.0)
            hit_registered, defeated = hazard.apply_hit()  # type: ignore[attr-defined]
            if hit_registered:
                hits_registered += 1
            if defeated:
                break
        return hits_registered, defeated

    def _apply_player_upgrade_effects(self, effects: dict[str, float]) -> None:
        move_speed_mult = max(0.0, effects.get("move_speed_mult", 0.0))
        self.player.speed = self.BASE_PLAYER_SPEED * (
            1.0 + move_speed_mult + self._character_move_speed_mult
        )
        projectile_cap_bonus = max(0, int(effects.get("projectile_cap_bonus", 0.0)))
        self.max_active_projectiles = min(5, 3 + projectile_cap_bonus)

    def _spawn_speed_with_upgrade_modifiers(self, base_speed: float) -> float:
        effects = self.run_upgrades.effects_snapshot()
        enemy_speed_reduction = max(0.0, min(0.45, effects.get("enemy_speed_reduction", 0.0)))
        return base_speed * (1.0 - enemy_speed_reduction)

    def _spawn_xp_drops_for_kills(
        self,
        positions: list[pygame.Vector2],
        enemy_kinds: list[str],
    ) -> None:
        for center, kind in zip(positions, enemy_kinds):
            base_xp = int(self.XP_DROP_VALUES.get(kind, 10))
            xp_value = max(1, int(round(base_xp * (1.0 + self._character_xp_gain_mult))))
            self._spawn_xp_drop(center, xp_value=xp_value)

    def _spawn_xp_drop(self, center: pygame.Vector2, *, xp_value: int) -> None:
        self.xp_drops.append(
            XpDrop(
                pygame.Vector2(center),
                xp_value=xp_value,
                size=self._xp_drop_size_for_value(xp_value),
                lifetime_seconds=self.XP_DROP_LIFETIME_SECONDS,
                fade_duration_seconds=self.XP_DROP_FADE_DURATION_SECONDS,
            )
        )

    def _xp_drop_size_for_value(self, xp_value: int) -> int:
        max_reward = max(1, max(self.XP_DROP_VALUES.values()))
        ratio = max(0.0, min(float(xp_value) / float(max_reward), 1.0))
        return int(
            round(
                self.XP_DROP_SIZE_MIN
                + (self.XP_DROP_SIZE_MAX - self.XP_DROP_SIZE_MIN) * ratio
            )
        )

    def _collect_xp_drops(self, player_collision_rect: pygame.Rect) -> None:
        if not self.xp_drops:
            return
        pickup_rect = player_collision_rect.inflate(
            int((self.XP_PICKUP_RADIUS + self._character_pickup_radius_bonus) * 2),
            int((self.XP_PICKUP_RADIUS + self._character_pickup_radius_bonus) * 2),
        )
        remaining: list[XpDrop] = []
        for drop in self.xp_drops:
            if drop.is_expired():
                continue
            if pickup_rect.colliderect(drop.rect):
                self.run_progression.gain_xp(drop.xp_value)
                self.confetti.spawn_burst(
                    pygame.Vector2(drop.position),
                    count=3,
                    speed_min=70.0,
                    speed_max=130.0,
                    lifetime_min=0.14,
                    lifetime_max=0.24,
                )
                self._spawn_pulse_centers.append((int(drop.position.x), int(drop.position.y)))
                self._pending_xp_pickup_sfx_count += 1
                continue
            remaining.append(drop)
        self.xp_drops = remaining

    def _apply_xp_drop_magnetism(self, player_center: pygame.Vector2, delta_seconds: float) -> None:
        if not self.xp_drops:
            return
        clamped_delta = max(0.0, float(delta_seconds))
        magnet_radius = self.XP_MAGNET_RADIUS + self._character_pickup_radius_bonus
        magnet_speed = self.XP_MAGNET_SPEED * (1.0 + self._character_xp_magnet_mult)
        for drop in self.xp_drops:
            offset = player_center - drop.position
            distance = offset.length()
            if distance <= 0.001 or distance > magnet_radius:
                continue
            direction = offset / distance
            pull_scale = 1.0 - (distance / magnet_radius)
            step = magnet_speed * pull_scale * clamped_delta
            if step >= distance:
                drop.position = pygame.Vector2(player_center)
                continue
            drop.position += direction * step

    def _score_multiplier_from_effects(self, effects: dict[str, float]) -> float:
        return 1.0 + max(0.0, effects.get("score_mult", 0.0))

    def _spawn_enhanced_confetti(self, center: pygame.Vector2) -> None:
        """Spawn an enhanced confetti burst for boss defeats."""
        self.confetti.spawn_burst(center, count=16 + self._confetti_bonus_count())

    def _spawn_pinata_break_confetti(self, center: pygame.Vector2, *, burst_count: int = 14) -> None:
        """Spawn a stronger confetti burst for pinata breaks."""
        self.confetti.spawn_burst(
            center,
            count=max(10, int(burst_count) + self._confetti_bonus_count()),
            speed_min=180.0,
            speed_max=360.0,
            lifetime_min=0.7,
            lifetime_max=1.0,
        )

    def _spawn_sprayer_destroy_confetti(self, center: pygame.Vector2) -> None:
        """Spawn a distinct medium burst on sprayer destruction."""
        self.confetti.spawn_burst(
            center,
            count=11 + self._confetti_bonus_count(),
            speed_min=160.0,
            speed_max=300.0,
            lifetime_min=0.5,
            lifetime_max=0.85,
        )

    def _spawn_streamer_snake_break_confetti(self, center: pygame.Vector2) -> None:
        """Spawn a colorful ribbon-like burst on streamer snake destruction."""
        self.confetti.spawn_burst(
            center,
            count=13 + self._confetti_bonus_count(),
            speed_min=170.0,
            speed_max=330.0,
            lifetime_min=0.55,
            lifetime_max=0.9,
        )

    def _confetti_bonus_count(self) -> int:
        effects = self.run_upgrades.effects_snapshot()
        return max(0, int(effects.get("confetti_bonus", 0.0)))

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
            "player_damage_count": self._pending_player_damage_sfx_count,
            "super_activate_count": self._pending_super_activate_sfx_count,
            "bottle_rocket_launch_count": self._pending_bottle_rocket_launch_sfx_count,
            "bottle_rocket_impact_count": self._pending_bottle_rocket_impact_sfx_count,
            "sparkler_swing_count": self._pending_sparkler_swing_sfx_count,
            "sparkler_hit_count": self._pending_sparkler_hit_sfx_count,
            "xp_pickup_count": self._pending_xp_pickup_sfx_count,
            "evolution_count": self._pending_evolution_sfx_count,
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
        self._pending_player_damage_sfx_count = 0
        self._pending_super_activate_sfx_count = 0
        self._pending_bottle_rocket_launch_sfx_count = 0
        self._pending_bottle_rocket_impact_sfx_count = 0
        self._pending_sparkler_swing_sfx_count = 0
        self._pending_sparkler_hit_sfx_count = 0
        self._pending_xp_pickup_sfx_count = 0
        self._pending_evolution_sfx_count = 0
        return cues

    def consume_spawn_pulse_centers(self) -> list[tuple[int, int]]:
        centers = list(self._spawn_pulse_centers)
        self._spawn_pulse_centers.clear()
        return centers

    def _spawn_speed(self) -> float:
        """Return the speed used for newly spawned hazards at the current level."""
        return self.current_level_config.enemy_speed * self.difficulty_multiplier

    def _complete_boss_celebration(self) -> None:
        """Complete the boss defeat celebration and resume normal gameplay flow."""
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
        for drop in self.xp_drops:
            drop.draw(surface)
        overlays = self.active_weapon_visual_overlays()
        for overlay in overlays:
            if overlay.z_index < 0:
                self.weapon_overlay_renderer.draw_overlay(surface, self.player, overlay)
        animation_frame = self.player_animation.current_frame()
        animation_rect = self.player_animation.frame_rect_for_player(self.player.rect)
        self.player_renderer.draw(
            surface,
            self.player,
            animation_frame=animation_frame,
            animation_rect=animation_rect,
            animation_flip_x=self.player_animation.should_flip_horizontal(),
            show_direction_indicator=(len(overlays) == 0),
        )
        for overlay in overlays:
            if overlay.z_index >= 0:
                self.weapon_overlay_renderer.draw_overlay(surface, self.player, overlay)
        if self._show_weapon_overlay_debug:
            self._draw_weapon_overlay_debug(surface)
        self._draw_orbiting_sparks_visual(surface)
        self._draw_spark_aura_visual(surface)
        self._draw_sparkler_attack_visual(surface)
        self._draw_evolution_feedback_overlay(surface)
        self.confetti.draw(surface)

    def player_render_anchor(self) -> tuple[int, int]:
        return (self.player.rect.centerx, self.player.rect.bottom)

    def player_weapon_anchor(
        self,
        anchor_name: str = DEFAULT_PLAYER_WEAPON_ANCHOR,
    ) -> tuple[int, int]:
        return resolve_player_visual_anchor(self.player, anchor_name)

    def active_weapon_visual_overlays(self) -> tuple[WeaponVisualOverlay, ...]:
        overlays: list[WeaponVisualOverlay] = []
        for weapon_id in self.equipped_weapon_ids_for_visuals():
            overlay = self._resolve_overlay_for_weapon(weapon_id)
            if overlay is not None:
                overlays.append(overlay)
        return tuple(overlays)

    def equipped_weapon_ids_for_visuals(self) -> tuple[str, ...]:
        """Source of truth for overlay-eligible equipped weapons.

        Today we only expose the active weapon, but this helper is the
        intentional extension point if loadouts add multiple concurrent weapons.
        """
        weapon_id = str(getattr(self, "active_weapon_id", "") or "").strip()
        if not weapon_id:
            return ()
        return (weapon_id,)

    def _resolve_overlay_for_weapon(self, weapon_id: str) -> WeaponVisualOverlay | None:
        behavior_ids = self._weapon_behavior_ids(weapon_id)
        variant_id = self.weapon_visual_variant_id_for_weapon(weapon_id)
        if variant_id == "none":
            return None
        variant = weapon_visuals_module.get_weapon_visual_variant(weapon_id, variant_id)
        if variant is None:
            return None
        asset = weapon_visual_assets_module.get_weapon_visual_asset(variant.default_overlay_sprite)
        if asset is None:
            return None
        moving = self.player.movement_intensity >= self.ANIMATION_MOVE_INPUT_DEADZONE or self.player.is_dodging
        facing_left = self.player.facing.x < 0.0
        facing_key = "left" if facing_left else "right"
        offset_x, offset_y = variant.offsets_by_facing.get(facing_key, (0.0, 0.0))
        facing_vector = pygame.Vector2(self.player.facing)
        if facing_vector.length_squared() <= 0.0:
            facing_vector = pygame.Vector2(1.0, 0.0)
        else:
            facing_vector = facing_vector.normalize()
        base_angle = -math.degrees(math.atan2(facing_vector.y, facing_vector.x))
        tilt_angle = (
            variant.rotation_rule.moving_angle_degrees
            if moving
            else variant.rotation_rule.idle_angle_degrees
        )
        if variant.rotation_rule.mirror_angle_with_facing and facing_vector.x < 0.0:
            tilt_angle *= -1.0
        angle = base_angle + tilt_angle
        animation_profile = variant.animation_profile
        if animation_profile is not None:
            if animation_profile.bob_amplitude > 0.0 and animation_profile.bob_speed > 0.0:
                bob = math.sin(self.elapsed_time * animation_profile.bob_speed * math.tau)
                offset_y += bob * animation_profile.bob_amplitude
            if animation_profile.idle_sway_degrees > 0.0 and not moving:
                sway = math.sin(self.elapsed_time * max(0.5, animation_profile.bob_speed) * math.pi)
                angle += sway * animation_profile.idle_sway_degrees
        tuning = self._weapon_overlay_tuning_by_weapon.get(weapon_id, {})
        offset_x += float(tuning.get("offset_x", 0.0))
        offset_y += float(tuning.get("offset_y", 0.0))
        angle += float(tuning.get("rotation_degrees", 0.0))
        scale = float(variant.scale) + float(tuning.get("scale", 0.0))
        z_index = -abs(int(variant.draw_layer)) if facing_left else abs(int(variant.draw_layer))
        return WeaponVisualOverlay(
            overlay_id=asset.asset_id,
            sprite_path=asset.sprite_path,
            anchor_name=variant.anchor_name,
            offset_x=float(offset_x),
            offset_y=float(offset_y),
            rotation_degrees=float(angle),
            scale=max(0.05, float(scale)),
            z_index=z_index,
            visible=True,
            # Direction-based rotation already handles left/right orientation.
            # Extra sprite mirroring here can invert the visual when facing left.
            flip_x=False,
            flip_y=bool(facing_left),
        )

    def active_weapon_visual_overlay_snapshot(self) -> tuple[dict[str, object], ...]:
        snapshots: list[dict[str, object]] = []
        for overlay in self.active_weapon_visual_overlays():
            anchor = self.player_weapon_anchor(overlay.anchor_name)
            snapshots.append(
                {
                    "overlay_id": overlay.overlay_id,
                    "variant_id": self.active_weapon_visual_variant_id(),
                    "weapon_id": str(self.active_weapon_id),
                    "anchor_name": overlay.anchor_name,
                    "anchor": anchor,
                    "draw_position": (
                        int(round(anchor[0] + overlay.offset_x)),
                        int(round(anchor[1] + overlay.offset_y)),
                    ),
                    "scale": float(overlay.scale),
                    "rotation_degrees": float(overlay.rotation_degrees),
                    "z_index": int(overlay.z_index),
                    "visible": bool(overlay.visible),
                    "flip_x": bool(overlay.flip_x),
                    "flip_y": bool(overlay.flip_y),
                }
            )
        return tuple(snapshots)

    def active_weapon_visual_variant_id(self) -> str:
        return self.weapon_visual_variant_id_for_weapon(str(self.active_weapon_id))

    def weapon_visual_variant_id_for_weapon(self, weapon_id: str) -> str:
        resolved_weapon_id = str(weapon_id or "").strip()
        if not resolved_weapon_id:
            return "none"
        behavior_ids = self._weapon_behavior_ids(resolved_weapon_id)
        resolved = weapon_visuals_module.resolve_weapon_visual_variant_id(
            resolved_weapon_id,
            evolution_count=len(behavior_ids),
            active_form_id=self._active_weapon_form_id(resolved_weapon_id),
        )
        if resolved is not None:
            return resolved
        # Fallback: explicit tier1 variant if registered for this weapon.
        if weapon_visuals_module.get_weapon_visual_variant(resolved_weapon_id, "tier1") is not None:
            return "tier1"
        return "none"

    def weapon_visual_fallback_snapshot(self) -> dict[str, object]:
        weapon_id = str(getattr(self, "active_weapon_id", "") or "").strip()
        if not weapon_id:
            return {
                "weapon_id": "",
                "reason": "no_active_weapon",
            }
        variant_id = self.weapon_visual_variant_id_for_weapon(weapon_id)
        if variant_id == "none":
            return {
                "weapon_id": weapon_id,
                "reason": "unknown_weapon_visual",
            }
        variant = weapon_visuals_module.get_weapon_visual_variant(weapon_id, variant_id)
        if variant is None:
            return {
                "weapon_id": weapon_id,
                "reason": "unknown_weapon_visual",
            }
        asset = weapon_visual_assets_module.get_weapon_visual_asset(variant.default_overlay_sprite)
        if asset is None:
            return {
                "weapon_id": weapon_id,
                "variant_id": variant_id,
                "reason": "missing_asset",
            }
        return (
            {
                "weapon_id": weapon_id,
                "variant_id": variant_id,
                "reason": "ok",
            }
        )

    def record_weapon_overlay_event(self, event_name: str) -> None:
        self._weapon_overlay_event_times[str(event_name)] = float(self.elapsed_time)

    def set_weapon_overlay_debug(self, enabled: bool) -> bool:
        self._show_weapon_overlay_debug = bool(enabled)
        return self._show_weapon_overlay_debug

    def toggle_weapon_overlay_debug(self) -> bool:
        self._show_weapon_overlay_debug = not self._show_weapon_overlay_debug
        return self._show_weapon_overlay_debug

    def set_weapon_overlay_tuning(
        self,
        *,
        weapon_id: str,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
        scale: float = 0.0,
        rotation_degrees: float = 0.0,
    ) -> None:
        self._weapon_overlay_tuning_by_weapon[str(weapon_id)] = {
            "offset_x": float(offset_x),
            "offset_y": float(offset_y),
            "scale": float(scale),
            "rotation_degrees": float(rotation_degrees),
        }

    def clear_weapon_overlay_tuning(self, weapon_id: str | None = None) -> None:
        if weapon_id is None:
            self._weapon_overlay_tuning_by_weapon.clear()
            return
        self._weapon_overlay_tuning_by_weapon.pop(str(weapon_id), None)

    def reload_weapon_visual_config(self) -> None:
        importlib.reload(weapon_visual_assets_module)
        importlib.reload(weapon_visuals_module)
        self.weapon_overlay_renderer.clear_cache()

    def weapon_overlay_debug_snapshot(self) -> tuple[dict[str, object], ...]:
        snapshots: list[dict[str, object]] = []
        for overlay in self.active_weapon_visual_overlays():
            info = self.weapon_overlay_renderer.debug_info_for_overlay(self.player, overlay)
            if info is None:
                continue
            snapshots.append(
                {
                    "weapon_id": str(self.active_weapon_id),
                    "variant_id": self.active_weapon_visual_variant_id(),
                    "overlay_id": info.overlay_id,
                    "anchor_point": info.anchor_point,
                    "pivot_point": info.pivot_point,
                    "draw_rect": pygame.Rect(info.draw_rect),
                }
            )
        return tuple(snapshots)

    def player_collision_rect(self) -> pygame.Rect:
        """Return the fixed gameplay hitbox, intentionally independent of animation frames."""
        base = self.player.rect
        scaled_width = max(1, int(round(base.width * self.PLAYER_HITBOX_SCALE)))
        scaled_height = max(1, int(round(base.height * self.PLAYER_HITBOX_SCALE)))
        return pygame.Rect(
            base.centerx - (scaled_width // 2),
            base.centery - (scaled_height // 2),
            scaled_width,
            scaled_height,
        )

    def player_hitbox_circle(self) -> tuple[pygame.Vector2, float]:
        collision_rect = self.player_collision_rect()
        center = pygame.Vector2(collision_rect.center)
        radius = max(8.0, min(float(collision_rect.width), float(collision_rect.height)) * 0.5)
        return center, radius

    def draw_player_debug_overlay(self, surface: pygame.Surface) -> None:
        anchor = self.player_render_anchor()
        weapon_anchor = self.player_weapon_anchor()
        hitbox_center, hitbox_radius = self.player_hitbox_circle()
        animation_rect = self.player_animation.frame_rect_for_player(self.player.rect)
        animation_snapshot = self.player_animation.snapshot()
        pygame.draw.circle(surface, (255, 96, 140), anchor, 4)
        pygame.draw.line(surface, (255, 184, 96), anchor, weapon_anchor, width=2)
        pygame.draw.circle(surface, (255, 184, 96), weapon_anchor, 4)
        pygame.draw.circle(
            surface,
            (116, 222, 255),
            (int(hitbox_center.x), int(hitbox_center.y)),
            int(hitbox_radius),
            width=2,
        )
        pygame.draw.rect(surface, (246, 220, 122), self.player.rect, width=1)
        pygame.draw.rect(surface, (116, 222, 255), self.player_collision_rect(), width=1)
        if animation_rect is not None:
            pygame.draw.rect(surface, (126, 238, 166), animation_rect, width=1)
        variant = get_party_animal(getattr(self.player, "visual_variant_id", None))
        if not pygame.font.get_init():
            pygame.font.init()
        if self._debug_font is None:
            self._debug_font = pygame.font.Font(None, 24)
        label = f"Player Debug: {variant.variant_id} ({variant.animal_name})"
        text = self._debug_font.render(label, True, (244, 248, 252))
        surface.blit(text, (14, 14))
        anim_label = (
            "Anim Debug: "
            f"{animation_snapshot['state']} "
            f"frame {animation_snapshot['frame_index']}/{max(0, int(animation_snapshot['frame_count']) - 1)} "
            f"flip={animation_snapshot['flip_x']}"
        )
        anim_text = self._debug_font.render(anim_label, True, (208, 248, 226))
        surface.blit(anim_text, (14, 36))
        anchor_label = f"Weapon Anchor: {weapon_anchor[0]}, {weapon_anchor[1]}"
        anchor_text = self._debug_font.render(anchor_label, True, (255, 232, 184))
        surface.blit(anchor_text, (14, 58))

    def _draw_weapon_overlay_debug(self, surface: pygame.Surface) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        if self._debug_font is None:
            self._debug_font = pygame.font.Font(None, 24)
        debug_rows = self.weapon_overlay_debug_snapshot()
        if not debug_rows:
            label = f"Overlay Debug: {self.active_weapon_id} variant={self.active_weapon_visual_variant_id()} (none)"
            text = self._debug_font.render(label, True, (255, 224, 160))
            surface.blit(text, (14, 82))
            return
        for index, row in enumerate(debug_rows):
            draw_rect = row["draw_rect"]
            assert isinstance(draw_rect, pygame.Rect)
            anchor_point = row["anchor_point"]
            pivot_point = row["pivot_point"]
            assert isinstance(anchor_point, tuple)
            assert isinstance(pivot_point, tuple)
            pygame.draw.rect(surface, (126, 238, 166), draw_rect, width=1)
            pygame.draw.circle(surface, (255, 96, 140), (int(anchor_point[0]), int(anchor_point[1])), 3)
            pygame.draw.circle(surface, (248, 222, 76), (int(pivot_point[0]), int(pivot_point[1])), 3)
            line = (
                f"Overlay Debug: {row['weapon_id']} variant={row['variant_id']} "
                f"id={row['overlay_id']}"
            )
            text = self._debug_font.render(line, True, (255, 224, 160))
            surface.blit(text, (14, 82 + (index * 18)))

    def _draw_spark_aura_visual(self, surface: pygame.Surface) -> None:
        if self.active_weapon_id != "sparkler":
            return
        if self._active_weapon_form_id("sparkler") != "spark_aura":
            return
        center = pygame.Vector2(self.player.rect.center)
        progress = self._spark_aura_tick_timer / max(0.001, self.SPARK_AURA_TICK_INTERVAL)
        pulse = 0.88 + (0.12 * abs((progress * 2.0) - 1.0))
        radius = int(self._current_spark_aura_radius() * pulse)
        outer_shock_radius = int(self._current_spark_aura_radius() * (0.96 + (0.08 * progress)))
        aura_surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        aura_center = (radius + 2, radius + 2)
        pygame.draw.circle(aura_surface, (255, 160, 82, 38), aura_center, radius)
        pygame.draw.circle(aura_surface, (255, 196, 104, 54), aura_center, max(12, int(radius * 0.92)), width=3)
        pygame.draw.circle(aura_surface, (255, 232, 152, 110), aura_center, max(8, int(radius * 0.74)), width=2)
        pygame.draw.circle(aura_surface, (255, 248, 210, 148), aura_center, max(6, int(radius * 0.52)), width=1)
        pulse_alpha = int(52 + (92 * (1.0 - progress)))
        pygame.draw.circle(
            aura_surface,
            (255, 236, 176, pulse_alpha),
            aura_center,
            min(radius, max(14, outer_shock_radius)),
            width=2,
        )
        for crackle_index in range(10):
            angle = (progress * 180.0) + (crackle_index * 36.0)
            crackle_radius = radius * (0.62 + (0.08 * math.sin(math.radians(angle * 2.0))))
            crackle_position = pygame.Vector2(aura_center) + pygame.Vector2(crackle_radius, 0.0).rotate(angle)
            pygame.draw.circle(
                aura_surface,
                (255, 246, 204, 92),
                (int(crackle_position.x), int(crackle_position.y)),
                2,
            )
        surface.blit(aura_surface, (int(center.x) - radius - 2, int(center.y) - radius - 2))

    def _draw_orbiting_sparks_visual(self, surface: pygame.Surface) -> None:
        if self.active_weapon_id != "sparkler":
            return
        if self._active_weapon_form_id("sparkler") != "orbiting_sparklers":
            return
        orbit_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        orbit_center = pygame.Vector2(self.player.rect.center)
        pulse = 0.86 + (0.14 * abs(math.sin(math.radians(self._orbiting_spark_angle_degrees * 1.4))))
        ring_radius = int(self.ORBITING_SPARK_RADIUS * pulse)
        pygame.draw.circle(
            orbit_surface,
            (255, 198, 110, 24),
            (int(orbit_center.x), int(orbit_center.y)),
            ring_radius,
            width=1,
        )
        pygame.draw.circle(
            orbit_surface,
            (255, 236, 170, 18),
            (int(orbit_center.x), int(orbit_center.y)),
            max(8, ring_radius - 8),
            width=1,
        )
        for spark_index, spark_position in enumerate(self._orbiting_spark_positions()):
            base_phase = self._orbiting_spark_angle_degrees + ((360.0 / max(1, self.ORBITING_SPARK_COUNT)) * spark_index)
            previous_position = pygame.Vector2(spark_position)
            for trail_step in range(1, self.ORBITING_SPARK_TRAIL_STEPS + 1):
                trail_phase = base_phase - (self.ORBITING_SPARK_TRAIL_ANGLE_STEP * trail_step)
                trail_radius = self.ORBITING_SPARK_RADIUS - (trail_step * 2.0)
                trail_position = orbit_center + pygame.Vector2(max(12.0, trail_radius), 0.0).rotate(trail_phase)
                trail_alpha = max(18, 90 - (trail_step * 16))
                trail_width = max(1, 5 - trail_step)
                pygame.draw.line(
                    orbit_surface,
                    (255, 170, 92, trail_alpha),
                    trail_position,
                    previous_position,
                    width=trail_width,
                )
                pygame.draw.circle(
                    orbit_surface,
                    (255, 208, 132, max(12, trail_alpha - 10)),
                    (int(trail_position.x), int(trail_position.y)),
                    max(1, 5 - trail_step),
                )
                previous_position = trail_position
            pygame.draw.circle(
                orbit_surface,
                (255, 154, 72, 42),
                (int(spark_position.x), int(spark_position.y)),
                16,
            )
            pygame.draw.circle(
                orbit_surface,
                (255, 182, 84, 112),
                (int(spark_position.x), int(spark_position.y)),
                11,
            )
            pygame.draw.circle(
                orbit_surface,
                (255, 236, 156, 214),
                (int(spark_position.x), int(spark_position.y)),
                7,
            )
            pygame.draw.circle(
                orbit_surface,
                (255, 250, 226, 255),
                (int(spark_position.x), int(spark_position.y)),
                2,
            )
            pygame.draw.line(
                orbit_surface,
                (255, 248, 214, 180),
                (int(spark_position.x) - 3, int(spark_position.y)),
                (int(spark_position.x) + 3, int(spark_position.y)),
                width=1,
            )
            pygame.draw.line(
                orbit_surface,
                (255, 248, 214, 180),
                (int(spark_position.x), int(spark_position.y) - 3),
                (int(spark_position.x), int(spark_position.y) + 3),
                width=1,
            )
        surface.blit(orbit_surface, (0, 0))

    def _draw_evolution_feedback_overlay(self, surface: pygame.Surface) -> None:
        if self._evolution_feedback_timer <= 0.0 or not self._evolution_feedback_label:
            return
        if not pygame.font.get_init():
            pygame.font.init()
        if self._debug_font is None:
            self._debug_font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 44)
        subtitle_font = pygame.font.Font(None, 28)
        alpha = int(255 * min(1.0, self._evolution_feedback_timer / 1.15))
        title = title_font.render("EVOLVED", True, (255, 232, 156))
        subtitle = subtitle_font.render(self._evolution_feedback_label, True, (255, 248, 220))
        title.set_alpha(alpha)
        subtitle.set_alpha(alpha)
        title_rect = title.get_rect(center=(surface.get_width() // 2, 76))
        subtitle_rect = subtitle.get_rect(center=(surface.get_width() // 2, 106))
        shadow = pygame.Surface((title_rect.width + 24, subtitle_rect.height + 28), pygame.SRCALPHA)
        shadow.fill((24, 16, 8, int(alpha * 0.42)))
        shadow_rect = shadow.get_rect(center=(surface.get_width() // 2, 90))
        surface.blit(shadow, shadow_rect)
        surface.blit(title, title_rect)
        surface.blit(subtitle, subtitle_rect)

    def _create_player(self) -> Player:
        size = 80
        spawn_x = (self.bounds.width - size) / 2
        spawn_y = (self.bounds.height - size) / 2
        player = Player(spawn_x, spawn_y, size=size, speed=self.BASE_PLAYER_SPEED)
        player.visual_variant_id = self.active_player_animal_id
        player.reset_health()
        return player

    def _apply_character_passive_profile(self, profile: CharacterPassiveProfile) -> None:
        self._character_max_health_bonus = int(profile.max_health_bonus)
        self._character_move_speed_mult = float(profile.move_speed_mult)
        self._character_outgoing_damage_bonus = int(profile.outgoing_damage_bonus)
        self._character_incoming_damage_mult = max(0.0, float(profile.incoming_damage_mult))
        self._character_xp_gain_mult = max(0.0, float(profile.xp_gain_mult))
        self._character_pickup_radius_bonus = max(0.0, float(profile.pickup_radius_bonus))
        self._character_xp_magnet_mult = max(0.0, float(profile.xp_magnet_mult))

        self.player.max_health = max(1, 3 + self._character_max_health_bonus)
        self.player.reset_health()
        self.player.speed = self.BASE_PLAYER_SPEED * (1.0 + self._character_move_speed_mult)

    def active_character_passive_snapshot(self) -> dict[str, int | float | str]:
        profile = self._active_character_passive
        return {
            "character_id": profile.character_id,
            "display_name": profile.display_name,
            "passive_bonus": profile.passive_bonus,
            "passive_drawback": profile.passive_drawback,
            "max_health_bonus": self._character_max_health_bonus,
            "move_speed_mult": self._character_move_speed_mult,
            "outgoing_damage_bonus": self._character_outgoing_damage_bonus,
            "incoming_damage_mult": self._character_incoming_damage_mult,
            "xp_gain_mult": self._character_xp_gain_mult,
            "pickup_radius_bonus": self._character_pickup_radius_bonus,
            "xp_magnet_mult": self._character_xp_magnet_mult,
        }

    @property
    def super_charge(self) -> int:
        return int(self._super_charge)

    def super_snapshot(self) -> dict[str, int | str | bool | float]:
        profile = self._active_character_super
        max_charge = max(1, int(profile.max_charge))
        charge = max(0, min(int(self._super_charge), max_charge))
        return {
            "character_id": profile.character_id,
            "super_id": profile.super_id,
            "super_name": profile.super_name,
            "activation_behavior": profile.activation_behavior,
            "charge": charge,
            "max_charge": max_charge,
            "ready": charge >= max_charge,
            "progress_fraction": charge / max_charge,
        }

    def add_super_charge(self, amount: int) -> int:
        gained = max(0, int(amount))
        if gained <= 0:
            return 0
        max_charge = max(1, int(self._active_character_super.max_charge))
        previous = int(self._super_charge)
        self._super_charge = max(0, min(previous + gained, max_charge))
        return int(self._super_charge) - previous

    def can_activate_super(self) -> bool:
        return int(self._super_charge) >= max(1, int(self._active_character_super.max_charge))

    def try_activate_super(self) -> str | None:
        if not self.can_activate_super():
            return None
        super_id = self._active_character_super.super_id
        self._super_charge = 0
        self._activate_super_effect(super_id)
        self._pending_super_activate_sfx_count += 1
        return super_id

    def _activate_super_effect(self, super_id: str) -> None:
        if super_id == "bear_roar":
            self._activate_bear_roar()
        elif super_id == "bunny_mega_hop":
            self._activate_bunny_mega_hop()
        elif super_id == "cat_frenzy":
            self._activate_cat_frenzy()
        elif super_id == "raccoon_chaos_drop":
            self._activate_raccoon_chaos_drop()

    def _activate_bear_roar(self) -> None:
        center = pygame.Vector2(self.player.rect.center)
        self.player.grant_invulnerability(self.BEAR_ROAR_INVULNERABILITY_DURATION)
        hazards_to_remove: list[int] = []
        hazard_kill_positions: list[pygame.Vector2] = []
        hazard_kill_kinds: list[str] = []

        for hazard_idx, hazard in enumerate(self.hazards):
            hazard_center = pygame.Vector2(hazard.rect.center)
            to_hazard = hazard_center - center
            distance = to_hazard.length()
            if distance <= 0.001 or distance > self.BEAR_ROAR_RADIUS:
                continue
            direction = to_hazard.normalize()
            falloff = max(0.2, 1.0 - (distance / self.BEAR_ROAR_RADIUS))
            push_distance = self.BEAR_ROAR_MAX_PUSH_DISTANCE * falloff
            hazard.position += direction * push_distance
            if hasattr(hazard, "velocity"):
                hazard.velocity = hazard.velocity + (direction * (self.BEAR_ROAR_MAX_PUSH_SPEED * falloff))  # type: ignore[attr-defined]

            if distance > self.BEAR_ROAR_DAMAGE_RADIUS:
                continue

            if isinstance(hazard, BossBalloon):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=self.BEAR_ROAR_BOSS_CHIP_DAMAGE,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                    self._pending_boss_hit_sfx_count += hit_count
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                    hazard_kill_kinds.append("boss_balloon")
                continue

            if isinstance(hazard, PinataEnemy):
                hit_count, defeated = self._apply_damage_to_multi_hit_enemy(
                    hazard,
                    projectile_damage=1,
                )
                if hit_count > 0:
                    self._pending_balloon_hit_sfx_count += hit_count
                if defeated and hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                    hazard_kill_kinds.append("pinata")
                    self._pending_balloon_pop_sfx_count += 1
                    profile = hazard.spawn_profile or {}
                    self._spawn_pinata_break_confetti(
                        pygame.Vector2(hazard.rect.center),
                        burst_count=max(10, int(profile.get("break_confetti_count", 14))),
                    )
                continue

            if isinstance(hazard, ConfettiSprayer):
                self._pending_balloon_hit_sfx_count += 1
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    center_pos = pygame.Vector2(hazard.rect.center)
                    hazard_kill_positions.append(center_pos)
                    hazard_kill_kinds.append("confetti_sprayer")
                    self._pending_balloon_pop_sfx_count += 1
                    self._pending_sprayer_destroy_sfx_count += 1
                    self._spawn_sprayer_destroy_confetti(center_pos)
                continue

            if isinstance(hazard, StreamerSnake):
                self._pending_balloon_hit_sfx_count += 1
                if hazard_idx not in hazards_to_remove:
                    hazards_to_remove.append(hazard_idx)
                    center_pos = pygame.Vector2(hazard.rect.center)
                    hazard_kill_positions.append(center_pos)
                    hazard_kill_kinds.append("streamer_snake")
                    self._pending_balloon_pop_sfx_count += 1
                    self._spawn_streamer_snake_break_confetti(center_pos)
                continue

            self._pending_balloon_hit_sfx_count += 1
            if hazard_idx not in hazards_to_remove:
                hazards_to_remove.append(hazard_idx)
                hazard_kill_positions.append(pygame.Vector2(hazard.rect.center))
                hazard_kill_kinds.append(
                    str((hazard.spawn_profile or {}).get("enemy_kind", "balloon"))
                )
                self._pending_balloon_pop_sfx_count += 1

        for idx in sorted(hazards_to_remove, reverse=True):
            self.hazards.pop(idx)

        if hazard_kill_kinds:
            self._spawn_xp_drops_for_kills(hazard_kill_positions, hazard_kill_kinds)
            self.score_seconds += len(hazard_kill_kinds) * self.KILL_BONUS_POINTS * self._score_multiplier_from_effects(
                self.run_upgrades.effects_snapshot()
            )

        for kill_pos in hazard_kill_positions:
            self.confetti.spawn_burst(
                kill_pos,
                count=8 + self._confetti_bonus_count(),
                speed_min=170.0,
                speed_max=310.0,
                lifetime_min=0.25,
                lifetime_max=0.45,
            )

        self.confetti.spawn_burst(
            center,
            count=28 + self._confetti_bonus_count(),
            speed_min=260.0,
            speed_max=430.0,
            lifetime_min=0.35,
            lifetime_max=0.6,
        )
        self.confetti.spawn_burst(
            center,
            count=14 + self._confetti_bonus_count(),
            speed_min=120.0,
            speed_max=220.0,
            lifetime_min=0.2,
            lifetime_max=0.34,
        )
        self._spawn_pulse_centers.append((int(center.x), int(center.y)))
        self._spawn_pulse_centers.append((int(center.x), int(center.y)))

    def _activate_bunny_mega_hop(self) -> None:
        facing = pygame.Vector2(self.player.facing)
        if facing.length_squared() <= 0.0:
            facing = pygame.Vector2(1.0, 0.0)
        else:
            facing = facing.normalize()

        hop_distance = 220.0
        self.player.position += facing * hop_distance
        max_x = self.bounds.width - self.player.size
        max_y = self.bounds.height - self.player.size
        self.player.position.x = max(0.0, min(self.player.position.x, max_x))
        self.player.position.y = max(0.0, min(self.player.position.y, max_y))
        self.player.grant_invulnerability(0.35)

        landing = pygame.Vector2(self.player.rect.center)
        radius = 180.0
        max_push_speed = 420.0
        for hazard in self.hazards:
            hazard_center = pygame.Vector2(hazard.rect.center)
            to_hazard = hazard_center - landing
            distance = to_hazard.length()
            if distance <= 0.001 or distance > radius:
                continue
            direction = to_hazard.normalize()
            falloff = 1.0 - (distance / radius)
            if hasattr(hazard, "velocity"):
                hazard.velocity = hazard.velocity + (direction * (max_push_speed * falloff))  # type: ignore[attr-defined]
            hazard.position += direction * (55.0 * falloff)

        self.confetti.spawn_burst(
            landing,
            count=22 + self._confetti_bonus_count(),
            speed_min=240.0,
            speed_max=400.0,
            lifetime_min=0.35,
            lifetime_max=0.65,
        )
        self._spawn_pulse_centers.append((int(landing.x), int(landing.y)))

    def _activate_cat_frenzy(self) -> None:
        self._cat_frenzy_timer = self.CAT_FRENZY_DURATION
        center = pygame.Vector2(self.player.rect.center)
        self.confetti.spawn_burst(
            center,
            count=16 + self._confetti_bonus_count(),
            speed_min=180.0,
            speed_max=320.0,
            lifetime_min=0.3,
            lifetime_max=0.55,
        )
        self._spawn_pulse_centers.append((int(center.x), int(center.y)))

    def _activate_raccoon_chaos_drop(self) -> None:
        center = pygame.Vector2(self.player.rect.center)
        self.run_progression.gain_xp(self.RACCOON_CHAOS_DROP_XP_BONUS)
        self._bonus_score_points += self.RACCOON_CHAOS_DROP_SCORE_BONUS * self._score_multiplier_from_effects(
            self.run_upgrades.effects_snapshot()
        )

        radius = 210.0
        max_push_speed = 280.0
        for hazard in self.hazards:
            hazard_center = pygame.Vector2(hazard.rect.center)
            offset = hazard_center - center
            distance = offset.length()
            if distance <= 0.001 or distance > radius:
                continue
            direction = offset.normalize()
            falloff = 1.0 - (distance / radius)
            if hasattr(hazard, "velocity"):
                hazard.velocity = hazard.velocity + (direction * (max_push_speed * falloff))  # type: ignore[attr-defined]
            hazard.position += direction * (35.0 * falloff)

        self.confetti.spawn_burst(
            center,
            count=20 + self._confetti_bonus_count(),
            speed_min=190.0,
            speed_max=340.0,
            lifetime_min=0.35,
            lifetime_max=0.6,
        )
        self._spawn_pulse_centers.append((int(center.x), int(center.y)))

    def _spawn_bottle_rocket_launch_feedback(
        self,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
    ) -> None:
        direction_vector = (
            pygame.Vector2(direction).normalize()
            if pygame.Vector2(direction).length_squared() > 0.0
            else pygame.Vector2(1.0, 0.0)
        )
        muzzle_point = origin + (direction_vector * 20.0)
        self.confetti.spawn_burst(
            muzzle_point,
            count=5,
            speed_min=90.0,
            speed_max=160.0,
            lifetime_min=0.12,
            lifetime_max=0.2,
        )
        self._spawn_pulse_centers.append((int(muzzle_point.x), int(muzzle_point.y)))

    def _spawn_bottle_rocket_impact_feedback(
        self,
        center: pygame.Vector2,
        *,
        impact_scale: float = 1.0,
        end_of_range: bool = False,
    ) -> None:
        scale = max(0.5, float(impact_scale))
        if end_of_range:
            self.confetti.spawn_burst(
                center,
                count=max(4, int(6 * scale)),
                speed_min=105.0 * scale,
                speed_max=195.0 * scale,
                lifetime_min=0.14,
                lifetime_max=0.24,
            )
            self.confetti.spawn_burst(
                center,
                count=max(3, int(4 * scale)),
                speed_min=185.0 * scale,
                speed_max=295.0 * scale,
                lifetime_min=0.12,
                lifetime_max=0.2,
            )
        else:
            self.confetti.spawn_burst(
                center,
                count=max(4, int(7 * scale)),
                speed_min=120.0 * scale,
                speed_max=220.0 * scale,
                lifetime_min=0.12,
                lifetime_max=0.24,
            )
        self._spawn_pulse_centers.append((int(center.x), int(center.y)))

    def _apply_bottle_rocket_recoil(self, direction: pygame.Vector2) -> None:
        direction_vector = (
            pygame.Vector2(direction).normalize()
            if pygame.Vector2(direction).length_squared() > 0.0
            else pygame.Vector2(1.0, 0.0)
        )
        self.player.position -= direction_vector * 4.0
        max_x = self.bounds.width - self.player.size
        max_y = self.bounds.height - self.player.size
        self.player.position.x = max(0.0, min(self.player.position.x, max_x))
        self.player.position.y = max(0.0, min(self.player.position.y, max_y))

    def _current_bottle_rocket_flight_profile(self) -> BottleRocketFlightProfile:
        """Hook for future bottle rocket upgrades that alter flight behavior."""
        return BottleRocketFlightProfile(
            wobble_degrees=self.BOTTLE_ROCKET_WOBBLE_DEGREES,
            wobble_frequency_hz=self.BOTTLE_ROCKET_WOBBLE_FREQUENCY_HZ,
            acceleration_per_second=self.BOTTLE_ROCKET_ACCEL_PER_SECOND,
            max_speed_multiplier=self.BOTTLE_ROCKET_MAX_SPEED_MULTIPLIER,
            decay_start_life_fraction=self.BOTTLE_ROCKET_DECAY_START_FRACTION,
            speed_decay_per_second=self.BOTTLE_ROCKET_DECAY_SPEED_PER_SECOND,
            downward_arc_per_second=self.BOTTLE_ROCKET_DOWNWARD_ARC_PER_SECOND,
        )

    def _apply_player_contact_damage(self) -> bool:
        incoming_damage = max(1, int(round(1 * self._character_incoming_damage_mult)))
        took_damage = self.player.apply_damage(incoming_damage)
        if took_damage:
            self._pending_player_damage_sfx_count += 1
        return self.player.current_health <= 0

    def _create_initial_hazards(self, player: Player) -> list[Hazard]:
        spawn_speed = self._spawn_speed()
        level_config = self.current_level_config
        hazards = [
            self.spawn_controller.create_hazard_for_spawn_with_chances(
                tier=self.spawn_controller.select_spawn_tier(level_config.level),
                base_speed=self._spawn_speed_with_upgrade_modifiers(spawn_speed),
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
