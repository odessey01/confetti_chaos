"""Task 1 entry point: minimal game loop with state transitions."""

from __future__ import annotations

from enum import Enum
from typing import Callable

import pygame

from systems import (
    AudioManager,
    GameSession,
    InputController,
    RuntimeSettings,
    UiRenderer,
    VisualFeedback,
    MAX_START_LEVEL,
    MIN_START_LEVEL,
    assets_dir,
    clamp_selected_start_level,
    load_high_score,
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
START_MENU_OPTIONS = ("Start Game", "Level Select", "Toggle Music", "Quit")
PAUSE_MENU_OPTIONS = ("Resume", "Restart", "Toggle Music", "Quit to Menu")


class GameState(str, Enum):
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


class PauseMenuAction(str, Enum):
    RESUME = "Resume"
    RESTART = "Restart"
    TOGGLE_MUSIC = "Toggle Music"
    QUIT_TO_MENU = "Quit to Menu"


class StartMenuAction(str, Enum):
    START_GAME = "Start Game"
    LEVEL_SELECT = "Level Select"
    TOGGLE_MUSIC = "Toggle Music"
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
    if action == PauseMenuAction.TOGGLE_MUSIC:
        runtime_settings.music_enabled = not runtime_settings.music_enabled
        audio.set_enabled(runtime_settings.music_enabled)
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
        session.start_new_run(start_level=runtime_settings.selected_start_level)
        audio.play_start_or_restart()
        visual_feedback.trigger_state_transition()
        return transition_state(state, GameState.PLAYING), True
    if action == StartMenuAction.LEVEL_SELECT:
        runtime_settings.selected_start_level = next_start_level(
            runtime_settings.selected_start_level
        )
        save_hook(runtime_settings)
        return state, True
    if action == StartMenuAction.TOGGLE_MUSIC:
        runtime_settings.music_enabled = not runtime_settings.music_enabled
        audio.set_enabled(runtime_settings.music_enabled)
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
    ui = UiRenderer()
    visual_feedback = VisualFeedback()
    world_bounds = screen.get_rect()
    session = GameSession(world_bounds, hazard_count=HAZARD_COUNT)

    state = GameState.MENU
    audio.sync_music_for_state(state.value)
    start_menu_index = 0
    pause_menu_index = 0
    running = True
    while running:
        delta_seconds = clock.tick(TARGET_FPS) / 1000.0
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
                if state == GameState.MENU and input_controller.is_menu_up(event):
                    start_menu_index = next_start_menu_index(start_menu_index, -1)
                elif state == GameState.MENU and input_controller.is_menu_down(event):
                    start_menu_index = next_start_menu_index(start_menu_index, 1)
                elif state == GameState.MENU and input_controller.is_menu_confirm(event):
                    action = start_menu_action_for_index(start_menu_index)
                    state, running = execute_start_menu_action(
                        action,
                        state=state,
                        session=session,
                        runtime_settings=runtime_settings,
                        audio=audio,
                        visual_feedback=visual_feedback,
                    )
                elif state == GameState.MENU and input_controller.is_menu_quit(event):
                    running = False
                elif state == GameState.PLAYING and input_controller.is_pause_toggle(event):
                    state = transition_state(state, GameState.PAUSED)
                    pause_menu_index = 0
                    visual_feedback.trigger_state_transition()
                elif state == GameState.PLAYING and input_controller.is_attack(event):
                    attack = True
                elif state == GameState.PAUSED and input_controller.is_pause_menu_up(event):
                    pause_menu_index = next_pause_menu_index(pause_menu_index, -1)
                elif state == GameState.PAUSED and input_controller.is_pause_menu_down(event):
                    pause_menu_index = next_pause_menu_index(pause_menu_index, 1)
                elif state == GameState.PAUSED and input_controller.is_pause_menu_confirm(event):
                    action = pause_menu_action_for_index(pause_menu_index)
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
                elif state == GameState.GAME_OVER and input_controller.is_restart(event):
                    state = transition_state(state, GameState.PLAYING)
                    session.start_new_run(start_level=runtime_settings.selected_start_level)
                    audio.play_start_or_restart()
                    visual_feedback.trigger_state_transition()

        audio.sync_music_for_state(state.value)

        if should_update_playing(state):
            movement_input = input_controller.movement_vector()
            collided = session.update_playing(delta_seconds, movement_input, attack)
            if collided:
                audio.play_collision()
                visual_feedback.trigger_collision_feedback()
                if session.score_value > high_score:
                    high_score = session.score_value
                    save_high_score(high_score)
                state = transition_state(state, GameState.GAME_OVER)
                visual_feedback.trigger_state_transition()

            if session.boss_victory_sound_pending:
                audio.play_boss_victory()
                session.clear_boss_victory_sound_pending()

            for center in session.consume_spawn_pulse_centers():
                visual_feedback.add_spawn_pulse(center)

        visual_feedback.update(delta_seconds)

        world_surface = pygame.Surface(screen.get_size())
        world_surface.fill((20, 20, 30))

        ui.draw_score(world_surface, session.score_value)
        ui.draw_level(world_surface, session.current_level)

        if state == GameState.MENU:
            ui.draw_menu(
                world_surface,
                WINDOW_TITLE,
                high_score,
                START_MENU_OPTIONS,
                start_menu_index,
                runtime_settings.music_enabled,
                runtime_settings.selected_start_level,
            )
        elif state == GameState.PLAYING:
            session.draw_playing(world_surface)
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
            ui.draw_paused(
                world_surface,
                runtime_settings.music_enabled,
                PAUSE_MENU_OPTIONS,
                pause_menu_index,
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
