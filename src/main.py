"""Task 1 entry point: minimal game loop with state transitions."""

from __future__ import annotations

from enum import Enum
from typing import Callable

import pygame

from systems import (
    AudioManager,
    BackgroundRenderer,
    GameSession,
    InputController,
    PLAYABLE_PARTY_ANIMAL_IDS,
    RuntimeSettings,
    UiRenderer,
    VisualFeedback,
    MAX_START_LEVEL,
    MIN_START_LEVEL,
    assets_dir,
    clamp_selected_start_level,
    get_character_passive,
    load_high_score,
    get_party_animal,
    get_weapon_definition,
    load_settings,
    save_high_score,
    save_settings,
    saves_dir,
)


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Confetti Chaos"
TARGET_FPS = 60
HAZARD_COUNT = 1
LEVEL_UP_CONFIRM_DELAY_SECONDS = 0.35
LEVEL_UP_EXIT_INVULNERABILITY_SECONDS = 1.0
START_MENU_OPTIONS = ("Start Game", "Level Select", "Toggle Sound", "Toggle Aim Assist", "Quit")
PAUSE_MENU_OPTIONS = ("Resume", "Restart", "Toggle Sound", "Toggle Aim Assist", "Quit to Menu")
PLAYER_SELECT_NOTES = {
    "teddy_f": "",
    "bunny_f": "Soft hopper",
    "fox_f": "Clever plush",
    "cat_f": "Cozy cat",
}
ENABLED_PLAYER_SELECT_IDS: tuple[str, ...] = ("teddy_f",)


class GameState(str, Enum):
    MENU = "MENU"
    PLAYER_SELECT = "PLAYER_SELECT"
    PLAYING = "PLAYING"
    LEVEL_UP = "LEVEL_UP"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


class PauseMenuAction(str, Enum):
    RESUME = "Resume"
    RESTART = "Restart"
    TOGGLE_SOUND = "Toggle Sound"
    TOGGLE_AIM_ASSIST = "Toggle Aim Assist"
    QUIT_TO_MENU = "Quit to Menu"


class StartMenuAction(str, Enum):
    START_GAME = "Start Game"
    LEVEL_SELECT = "Level Select"
    TOGGLE_SOUND = "Toggle Sound"
    TOGGLE_AIM_ASSIST = "Toggle Aim Assist"
    QUIT = "Quit"


def transition_state(current: GameState, target: GameState) -> GameState:
    if current != target:
        print(f"STATE: {current.value} -> {target.value}")
    return target


def next_start_menu_index(current_index: int, direction: int) -> int:
    option_count = len(START_MENU_OPTIONS)
    if option_count == 0:
        return 0
    return (current_index + direction) % option_count


def start_menu_action_for_index(index: int) -> StartMenuAction:
    return StartMenuAction(START_MENU_OPTIONS[index % len(START_MENU_OPTIONS)])


def next_start_level(current_level: int) -> int:
    clamped = clamp_selected_start_level(current_level)
    if clamped >= MAX_START_LEVEL:
        return MIN_START_LEVEL
    return clamped + 1


def next_pause_menu_index(current_index: int, direction: int) -> int:
    option_count = len(PAUSE_MENU_OPTIONS)
    if option_count == 0:
        return 0
    return (current_index + direction) % option_count


def pause_menu_action_for_index(index: int) -> PauseMenuAction:
    return PauseMenuAction(PAUSE_MENU_OPTIONS[index % len(PAUSE_MENU_OPTIONS)])


def should_update_playing(state: GameState) -> bool:
    return state == GameState.PLAYING


def next_choice_index(current_index: int, direction: int, option_count: int) -> int:
    if option_count <= 0:
        return 0
    return (current_index + direction) % option_count


def next_player_select_index(current_index: int, direction: int, selectable: tuple[bool, ...]) -> int:
    option_count = len(selectable)
    if option_count <= 0:
        return 0
    if not any(selectable):
        return 0
    step = -1 if direction < 0 else 1
    index = current_index
    for _ in range(option_count):
        index = (index + step) % option_count
        if selectable[index]:
            return index
    return current_index


def desired_music_track_for_state(state: GameState, *, boss_active: bool) -> str | None:
    if state in (GameState.MENU, GameState.PLAYER_SELECT):
        return "menu"
    if state == GameState.PLAYING:
        return "boss" if boss_active else "gameplay"
    if state in (GameState.PAUSED, GameState.GAME_OVER, GameState.LEVEL_UP):
        return "gameplay"
    return None


def desired_ambient_track_for_state(state: GameState) -> str | None:
    if state == GameState.PLAYING:
        return "gameplay"
    return None


def ui_sfx_for_start_action(action: StartMenuAction) -> str:
    mapping = {
        StartMenuAction.START_GAME: "ui_confirm",
        StartMenuAction.LEVEL_SELECT: "ui_toggle_settings",
        StartMenuAction.TOGGLE_SOUND: "ui_toggle_settings",
        StartMenuAction.TOGGLE_AIM_ASSIST: "ui_toggle_settings",
        StartMenuAction.QUIT: "ui_back",
    }
    return mapping[action]


def ui_sfx_for_pause_action(action: PauseMenuAction) -> str:
    mapping = {
        PauseMenuAction.RESUME: "ui_resume",
        PauseMenuAction.RESTART: "ui_confirm",
        PauseMenuAction.TOGGLE_SOUND: "ui_toggle_settings",
        PauseMenuAction.TOGGLE_AIM_ASSIST: "ui_toggle_settings",
        PauseMenuAction.QUIT_TO_MENU: "ui_back",
    }
    return mapping[action]


def execute_pause_menu_action(
    action: PauseMenuAction,
    *,
    state: GameState,
    session: GameSession,
    runtime_settings: RuntimeSettings,
    audio: AudioManager,
    visual_feedback: VisualFeedback,
    save_hook: Callable[[RuntimeSettings], None] = save_settings,
) -> GameState:
    if action == PauseMenuAction.RESUME:
        visual_feedback.trigger_state_transition()
        return transition_state(state, GameState.PLAYING)
    if action == PauseMenuAction.RESTART:
        session.start_new_run(start_level=runtime_settings.selected_start_level)
        audio.play_start_or_restart()
        visual_feedback.trigger_state_transition()
        return transition_state(state, GameState.PLAYING)
    if action == PauseMenuAction.TOGGLE_SOUND:
        runtime_settings.music_enabled = not runtime_settings.music_enabled
        audio.set_enabled(runtime_settings.music_enabled)
        save_hook(runtime_settings)
        return state
    if action == PauseMenuAction.TOGGLE_AIM_ASSIST:
        runtime_settings.aim_assist_enabled = not runtime_settings.aim_assist_enabled
        save_hook(runtime_settings)
        return state
    if action == PauseMenuAction.QUIT_TO_MENU:
        visual_feedback.trigger_state_transition()
        return transition_state(state, GameState.MENU)
    return state


def execute_start_menu_action(
    action: StartMenuAction,
    *,
    state: GameState,
    session: GameSession,
    runtime_settings: RuntimeSettings,
    audio: AudioManager,
    visual_feedback: VisualFeedback,
    save_hook: Callable[[RuntimeSettings], None] = save_settings,
) -> tuple[GameState, bool]:
    if action == StartMenuAction.START_GAME:
        visual_feedback.trigger_state_transition()
        return transition_state(state, GameState.PLAYER_SELECT), True
    if action == StartMenuAction.LEVEL_SELECT:
        runtime_settings.selected_start_level = next_start_level(
            runtime_settings.selected_start_level
        )
        save_hook(runtime_settings)
        return state, True
    if action == StartMenuAction.TOGGLE_SOUND:
        runtime_settings.music_enabled = not runtime_settings.music_enabled
        audio.set_enabled(runtime_settings.music_enabled)
        save_hook(runtime_settings)
        return state, True
    if action == StartMenuAction.TOGGLE_AIM_ASSIST:
        runtime_settings.aim_assist_enabled = not runtime_settings.aim_assist_enabled
        save_hook(runtime_settings)
        return state, True
    if action == StartMenuAction.QUIT:
        return state, False
    return state, True


def main() -> int:
    assets_dir().mkdir(parents=True, exist_ok=True)
    saves_dir()
    high_score = load_high_score()

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    audio = AudioManager()
    input_controller = InputController()
    runtime_settings = load_settings()
    audio.set_enabled(runtime_settings.music_enabled)
    audio.apply_mix(
        master=runtime_settings.master_volume,
        music=runtime_settings.music_volume,
        sfx=runtime_settings.sfx_volume,
        ambient=runtime_settings.ambient_volume,
    )
    ui = UiRenderer()
    visual_feedback = VisualFeedback()
    background = BackgroundRenderer((WINDOW_WIDTH, WINDOW_HEIGHT))
    world_bounds = screen.get_rect()
    session = GameSession(world_bounds, hazard_count=HAZARD_COUNT)
    player_select_ids: tuple[str, ...] = (
        PLAYABLE_PARTY_ANIMAL_IDS if PLAYABLE_PARTY_ANIMAL_IDS else ("teddy_f",)
    )
    player_select_enabled: tuple[bool, ...] = tuple(
        get_party_animal(variant_id).variant_id in ENABLED_PLAYER_SELECT_IDS
        for variant_id in player_select_ids
    )

    state = GameState.PLAYER_SELECT
    track = desired_music_track_for_state(state, boss_active=False)
    if track is None:
        audio.stop_music()
    else:
        audio.play_music(track)
    ambient_track = desired_ambient_track_for_state(state)
    if ambient_track is None:
        audio.stop_ambient()
    else:
        audio.play_ambient(ambient_track)
    start_menu_index = 0
    player_select_index = (
        player_select_enabled.index(True) if any(player_select_enabled) else 0
    )
    pause_menu_index = 0
    selected_weapon_id = "bottle_rocket"
    level_up_choice_index = 0
    level_up_input_lock_timer = 0.0
    show_player_debug = False
    running = True
    while running:
        delta_seconds = clock.tick(TARGET_FPS) / 1000.0
        level_up_input_lock_timer = max(0.0, level_up_input_lock_timer - delta_seconds)
        attack = False
        for event in pygame.event.get():
            input_controller.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.KEYDOWN, pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    runtime_settings.music_enabled = not runtime_settings.music_enabled
                    audio.set_enabled(runtime_settings.music_enabled)
                    save_settings(runtime_settings)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                    show_player_debug = not show_player_debug
                if state == GameState.MENU and input_controller.is_menu_up(event):
                    start_menu_index = next_start_menu_index(start_menu_index, -1)
                    audio.play_sfx("ui_nav")
                elif state == GameState.MENU and input_controller.is_menu_down(event):
                    start_menu_index = next_start_menu_index(start_menu_index, 1)
                    audio.play_sfx("ui_nav")
                elif state == GameState.MENU and input_controller.is_menu_confirm(event):
                    action = start_menu_action_for_index(start_menu_index)
                    audio.play_sfx(ui_sfx_for_start_action(action))
                    state, running = execute_start_menu_action(
                        action,
                        state=state,
                        session=session,
                        runtime_settings=runtime_settings,
                        audio=audio,
                        visual_feedback=visual_feedback,
                    )
                elif state == GameState.MENU and input_controller.is_menu_quit(event):
                    audio.play_sfx("ui_back")
                    running = False
                elif state == GameState.PLAYING and input_controller.is_pause_toggle(event):
                    state = transition_state(state, GameState.PAUSED)
                    pause_menu_index = 0
                    audio.play_sfx("ui_pause")
                    visual_feedback.trigger_state_transition()
                elif state == GameState.PLAYING and input_controller.is_attack(event):
                    attack = True
                elif state == GameState.PLAYING and input_controller.is_dodge(event):
                    session.trigger_player_dodge(input_controller.movement_vector())
                elif state == GameState.PLAYING and input_controller.is_super_activate(event):
                    session.try_activate_super()
                elif state == GameState.PLAYER_SELECT and input_controller.is_menu_up(event):
                    player_select_index = next_player_select_index(player_select_index, -1, player_select_enabled)
                    audio.play_sfx("ui_nav")
                elif state == GameState.PLAYER_SELECT and input_controller.is_menu_down(event):
                    player_select_index = next_player_select_index(player_select_index, 1, player_select_enabled)
                    audio.play_sfx("ui_nav")
                elif state == GameState.PLAYER_SELECT and input_controller.is_menu_left(event):
                    player_select_index = next_player_select_index(player_select_index, -1, player_select_enabled)
                    audio.play_sfx("ui_nav")
                elif state == GameState.PLAYER_SELECT and input_controller.is_menu_right(event):
                    player_select_index = next_player_select_index(player_select_index, 1, player_select_enabled)
                    audio.play_sfx("ui_nav")
                elif state == GameState.PLAYER_SELECT and input_controller.is_menu_confirm(event):
                    if not player_select_enabled[player_select_index]:
                        audio.play_sfx("ui_back")
                        continue
                    selected_variant = (
                        player_select_ids[player_select_index]
                        if player_select_ids
                        else "teddy_f"
                    )
                    selected_variant = get_party_animal(selected_variant).variant_id
                    session.start_new_run(
                        start_level=runtime_settings.selected_start_level,
                        player_animal_id=selected_variant,
                        weapon_id=selected_weapon_id,
                    )
                    audio.play_start_or_restart()
                    audio.play_sfx("ui_confirm")
                    visual_feedback.trigger_state_transition()
                    state = transition_state(state, GameState.PLAYING)
                elif state == GameState.PLAYER_SELECT and input_controller.is_menu_quit(event):
                    audio.play_sfx("ui_back")
                    state = transition_state(state, GameState.MENU)
                elif state == GameState.PLAYER_SELECT and input_controller.is_weapon_toggle(event):
                    selected_weapon_id = "sparkler" if selected_weapon_id == "bottle_rocket" else "bottle_rocket"
                    audio.play_sfx("ui_toggle_settings")
                elif state == GameState.PAUSED and input_controller.is_pause_menu_up(event):
                    pause_menu_index = next_pause_menu_index(pause_menu_index, -1)
                    audio.play_sfx("ui_nav")
                elif state == GameState.PAUSED and input_controller.is_pause_menu_down(event):
                    pause_menu_index = next_pause_menu_index(pause_menu_index, 1)
                    audio.play_sfx("ui_nav")
                elif state == GameState.PAUSED and input_controller.is_pause_menu_confirm(event):
                    action = pause_menu_action_for_index(pause_menu_index)
                    audio.play_sfx(ui_sfx_for_pause_action(action))
                    state = execute_pause_menu_action(
                        action,
                        state=state,
                        session=session,
                        runtime_settings=runtime_settings,
                        audio=audio,
                        visual_feedback=visual_feedback,
                    )
                elif state == GameState.PAUSED and input_controller.is_pause_toggle(event):
                    state = execute_pause_menu_action(
                        PauseMenuAction.RESUME,
                        state=state,
                        session=session,
                        runtime_settings=runtime_settings,
                        audio=audio,
                        visual_feedback=visual_feedback,
                    )
                    audio.play_sfx("ui_resume")
                elif state == GameState.LEVEL_UP and input_controller.is_menu_up(event):
                    option_count = len(session.current_upgrade_choices())
                    level_up_choice_index = next_choice_index(level_up_choice_index, -1, option_count)
                    audio.play_sfx("ui_nav")
                elif state == GameState.LEVEL_UP and input_controller.is_menu_down(event):
                    option_count = len(session.current_upgrade_choices())
                    level_up_choice_index = next_choice_index(level_up_choice_index, 1, option_count)
                    audio.play_sfx("ui_nav")
                elif state == GameState.LEVEL_UP and input_controller.is_menu_left(event):
                    option_count = len(session.current_upgrade_choices())
                    level_up_choice_index = next_choice_index(level_up_choice_index, -1, option_count)
                    audio.play_sfx("ui_nav")
                elif state == GameState.LEVEL_UP and input_controller.is_menu_right(event):
                    option_count = len(session.current_upgrade_choices())
                    level_up_choice_index = next_choice_index(level_up_choice_index, 1, option_count)
                    audio.play_sfx("ui_nav")
                elif state == GameState.LEVEL_UP and input_controller.is_menu_confirm(event):
                    if level_up_input_lock_timer <= 0.0 and session.apply_upgrade_choice_by_index(level_up_choice_index):
                        audio.play_sfx("ui_confirm")
                        if session.pending_run_level_ups > 0:
                            session.ensure_upgrade_choices()
                            level_up_choice_index = 0
                            level_up_input_lock_timer = LEVEL_UP_CONFIRM_DELAY_SECONDS
                        else:
                            state = transition_state(state, GameState.PLAYING)
                            session.player.grant_invulnerability(LEVEL_UP_EXIT_INVULNERABILITY_SECONDS)
                            level_up_input_lock_timer = 0.0
                elif state == GameState.GAME_OVER and input_controller.is_restart(event):
                    audio.play_sfx("ui_confirm")
                    state = transition_state(state, GameState.PLAYING)
                    session.start_new_run(start_level=runtime_settings.selected_start_level)
                    audio.play_start_or_restart()
                    visual_feedback.trigger_state_transition()

        audio.apply_mix(
            master=runtime_settings.master_volume,
            music=runtime_settings.music_volume,
            sfx=runtime_settings.sfx_volume,
            ambient=runtime_settings.ambient_volume,
        )
        session.set_active_input_method(input_controller.active_input_method())
        session.set_aim_assist_user_enabled(runtime_settings.aim_assist_enabled)

        track = desired_music_track_for_state(state, boss_active=session.boss_active)
        if track is None:
            audio.stop_music()
        else:
            audio.play_music(track)
        ambient_track = desired_ambient_track_for_state(state)
        if ambient_track is None:
            audio.stop_ambient()
        else:
            audio.play_ambient(ambient_track)

        if should_update_playing(state):
            movement_input = input_controller.movement_vector()
            player_died = session.update_playing(delta_seconds, movement_input, attack)
            if player_died:
                audio.play_sfx("player_damage_or_death")
                if session.score_value > high_score:
                    high_score = session.score_value
                    save_high_score(high_score)
                state = transition_state(state, GameState.GAME_OVER)
                visual_feedback.trigger_state_transition()

            audio_cues = session.consume_audio_cues()
            if audio_cues["level_transition"]:
                audio.play_sfx("level_transition")
            if audio_cues["boss_spawn"]:
                audio.play_sfx("boss_spawn")
            for _ in range(min(4, int(audio_cues["balloon_hit_count"]))):
                audio.play_sfx("balloon_hit")
            for _ in range(min(4, int(audio_cues["balloon_pop_count"]))):
                audio.play_sfx("balloon_pop")
            for _ in range(min(3, int(audio_cues["boss_hit_count"]))):
                audio.play_sfx("boss_hit")
            if audio_cues["boss_defeat"]:
                audio.play_sfx("boss_defeat")
            if audio_cues["boss_phase_change"]:
                audio.play_sfx("milestone_clear")
            if audio_cues["milestone_clear"]:
                audio.play_sfx("milestone_clear")
            if audio_cues["confetti_celebration"]:
                audio.play_sfx("confetti_celebration")
            for _ in range(min(3, int(audio_cues["sprayer_charge_count"]))):
                audio.play_sfx("ui_nav")
            for _ in range(min(3, int(audio_cues["sprayer_burst_count"]))):
                audio.play_sfx("balloon_pop")
            for _ in range(min(3, int(audio_cues["sprayer_destroy_count"]))):
                audio.play_sfx("balloon_pop")
            for _ in range(min(3, int(audio_cues["player_damage_count"]))):
                audio.play_sfx("player_damage_or_death")
                visual_feedback.trigger_collision_feedback()
            for _ in range(min(2, int(audio_cues["super_activate_count"]))):
                audio.play_sfx("milestone_clear")
            for _ in range(min(4, int(audio_cues["bottle_rocket_launch_count"]))):
                audio.play_sfx("weapon_fire")
            for _ in range(min(4, int(audio_cues["bottle_rocket_impact_count"]))):
                audio.play_sfx("balloon_pop")
            for _ in range(min(4, int(audio_cues["sparkler_swing_count"]))):
                audio.play_sfx("weapon_fire")
            for _ in range(min(4, int(audio_cues["sparkler_hit_count"]))):
                audio.play_sfx("balloon_hit")
            for _ in range(min(6, int(audio_cues["xp_pickup_count"]))):
                audio.play_sfx("ui_nav")

            for center in session.consume_spawn_pulse_centers():
                visual_feedback.add_spawn_pulse(center)

            if session.pending_run_level_ups > 0:
                choices = session.ensure_upgrade_choices()
                if choices:
                    level_up_choice_index = 0
                    state = transition_state(state, GameState.LEVEL_UP)
                    level_up_input_lock_timer = LEVEL_UP_CONFIRM_DELAY_SECONDS

        visual_feedback.update(delta_seconds)

        world_surface = pygame.Surface(screen.get_size())
        if state in (GameState.PLAYING, GameState.PAUSED, GameState.LEVEL_UP):
            flavor_name = session.current_level_config.flavor.name
            player_center = session.player.rect.center
        else:
            flavor_name = "STANDARD"
            player_center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        background.update(delta_seconds, flavor_name=flavor_name)
        background.draw(world_surface, player_center=player_center)

        if state == GameState.MENU:
            ui.draw_menu(
                world_surface,
                WINDOW_TITLE,
                high_score,
                START_MENU_OPTIONS,
                start_menu_index,
                runtime_settings.music_enabled,
                runtime_settings.aim_assist_enabled,
                runtime_settings.selected_start_level,
            )
        elif state == GameState.PLAYER_SELECT:
            selected_key = player_select_ids[player_select_index] if player_select_ids else "teddy_f"
            selected_variant_id = get_party_animal(selected_key).variant_id
            selected_variant = get_party_animal(selected_variant_id)
            preview_size = 140
            preview_x = (WINDOW_WIDTH - preview_size) / 2
            preview_y = 180
            session.player.position.update(preview_x, preview_y)
            session.player.size = preview_size
            session.player.visual_variant_id = selected_variant_id
            session.player._movement_intensity = 0.25
            session.player._movement_juice = 0.1
            session.player._movement_phase += delta_seconds * 4.0
            session.player_animation.set_character(selected_variant_id)
            session.player_animation.update(
                delta_seconds,
                moving=False,
                facing=pygame.Vector2(1.0, 0.0),
            )
            preview_frame = session.player_animation.current_frame()
            preview_rect = session.player_animation.frame_rect_for_player(session.player.rect)
            if preview_frame is not None and selected_variant_id == "teddy_f":
                preview_rect = preview_frame.get_rect()
                preview_rect.midbottom = session.player.rect.midbottom
            session.player_renderer.draw(
                world_surface,
                session.player,
                animation_frame=preview_frame,
                animation_rect=preview_rect,
                animation_flip_x=session.player_animation.should_flip_horizontal(),
            )
            session.player.size = 80
            selected_note = PLAYER_SELECT_NOTES.get(selected_variant_id, "")
            passive = get_character_passive(selected_variant_id)
            option_names = (
                tuple(get_party_animal(v).display_name for v in player_select_ids)
                if player_select_ids
                else ("Barry",)
            )
            ui.draw_player_select(
                world_surface,
                selected_index=player_select_index,
                options=option_names,
                option_enabled=player_select_enabled,
                selected_name=selected_variant.display_name,
                selected_note=selected_note,
                passive_bonus=passive.passive_bonus,
                passive_drawback=passive.passive_drawback,
                passive_summary=("Tougher, Slower" if selected_variant_id == "teddy_f" else None),
                selected_weapon_name=get_weapon_definition(selected_weapon_id).display_name,
            )
        elif state == GameState.PLAYING:
            session.draw_playing(world_surface)
            ui.draw_score(world_surface, session.score_value)
            ui.draw_health(
                world_surface,
                current_health=session.player.current_health,
                max_health=session.player.max_health,
            )
            run_snapshot = session.run_progress_snapshot()
            ui.draw_run_progress(
                world_surface,
                run_level=int(run_snapshot["run_level"]),
                current_xp=int(run_snapshot["xp"]),
                xp_to_next=int(run_snapshot["xp_to_next_level"]),
            )
            super_snapshot = session.super_snapshot()
            ui.draw_super_meter(
                world_surface,
                charge=int(super_snapshot["charge"]),
                max_charge=int(super_snapshot["max_charge"]),
                ready=bool(super_snapshot["ready"]),
            )
            if show_player_debug:
                session.draw_player_debug_overlay(world_surface)
                session.draw_aim_assist_debug_overlay(world_surface)
            if session.boss_celebration_active:
                ui.draw_boss_victory(world_surface, session.boss_defeat_bonus)
            else:
                label = "PLAYING: Move (WASD/Arrows or Left Stick)"
                # Fade out instructions after 3 seconds, with fade starting at 2.5 seconds
                if session.elapsed_time < 3.0:
                    fade_alpha = max(0.0, (3.0 - session.elapsed_time) / 0.5)
                    ui.draw_state_text(world_surface, label, alpha=fade_alpha)
        elif state == GameState.PAUSED:
            session.draw_playing(world_surface)
            ui.draw_score(world_surface, session.score_value)
            ui.draw_health(
                world_surface,
                current_health=session.player.current_health,
                max_health=session.player.max_health,
            )
            run_snapshot = session.run_progress_snapshot()
            ui.draw_run_progress(
                world_surface,
                run_level=int(run_snapshot["run_level"]),
                current_xp=int(run_snapshot["xp"]),
                xp_to_next=int(run_snapshot["xp_to_next_level"]),
            )
            super_snapshot = session.super_snapshot()
            ui.draw_super_meter(
                world_surface,
                charge=int(super_snapshot["charge"]),
                max_charge=int(super_snapshot["max_charge"]),
                ready=bool(super_snapshot["ready"]),
            )
            if show_player_debug:
                session.draw_player_debug_overlay(world_surface)
                session.draw_aim_assist_debug_overlay(world_surface)
            ui.draw_paused(
                world_surface,
                runtime_settings.music_enabled,
                runtime_settings.aim_assist_enabled,
                PAUSE_MENU_OPTIONS,
                pause_menu_index,
            )
        elif state == GameState.LEVEL_UP:
            session.draw_playing(world_surface)
            ui.draw_score(world_surface, session.score_value)
            ui.draw_health(
                world_surface,
                current_health=session.player.current_health,
                max_health=session.player.max_health,
            )
            run_snapshot = session.run_progress_snapshot()
            ui.draw_run_progress(
                world_surface,
                run_level=int(run_snapshot["run_level"]),
                current_xp=int(run_snapshot["xp"]),
                xp_to_next=int(run_snapshot["xp_to_next_level"]),
            )
            super_snapshot = session.super_snapshot()
            ui.draw_super_meter(
                world_surface,
                charge=int(super_snapshot["charge"]),
                max_charge=int(super_snapshot["max_charge"]),
                ready=bool(super_snapshot["ready"]),
            )
            if show_player_debug:
                session.draw_player_debug_overlay(world_surface)
                session.draw_aim_assist_debug_overlay(world_surface)
            ui.draw_level_up_overlay(
                world_surface,
                run_level=session.run_level,
                options=session.current_upgrade_choices(),
                selected_index=level_up_choice_index,
            )
        else:
            label = (
                f"GAME OVER: Score {session.score_value} | High Score {high_score} "
                "- Press R or Space to Restart"
            )
            ui.draw_state_text(world_surface, label)

        visual_feedback.draw_overlays(world_surface)

        shake_x, shake_y = visual_feedback.camera_offset()
        screen.fill((12, 12, 16))
        screen.blit(world_surface, (shake_x, shake_y))

        pygame.display.flip()

    save_settings(runtime_settings)
    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
