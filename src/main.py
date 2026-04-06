"""Task 1 entry point: minimal game loop with state transitions."""

from __future__ import annotations

from enum import Enum

import pygame

from systems import (
    AudioManager,
    GameSession,
    InputController,
    RuntimeSettings,
    UiRenderer,
    VisualFeedback,
    assets_dir,
    load_high_score,
    save_high_score,
    saves_dir,
)


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Confetti Chaos"
TARGET_FPS = 60
HAZARD_COUNT = 1


class GameState(str, Enum):
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


def transition_state(current: GameState, target: GameState) -> GameState:
    if current != target:
        print(f"STATE: {current.value} -> {target.value}")
    return target


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
    runtime_settings = RuntimeSettings()
    ui = UiRenderer()
    visual_feedback = VisualFeedback()
    world_bounds = screen.get_rect()
    session = GameSession(world_bounds, hazard_count=HAZARD_COUNT)

    state = GameState.MENU
    running = True
    while running:
        delta_seconds = clock.tick(TARGET_FPS) / 1000.0
        for event in pygame.event.get():
            input_controller.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    runtime_settings.audio_enabled = not runtime_settings.audio_enabled
                    audio.set_enabled(runtime_settings.audio_enabled)
                if state == GameState.MENU and input_controller.is_menu_confirm(event):
                    state = transition_state(state, GameState.PLAYING)
                    session.start_new_run()
                    audio.play_start_or_restart()
                    visual_feedback.trigger_state_transition()
                elif state == GameState.MENU and input_controller.is_menu_quit(event):
                    running = False
                elif state == GameState.PLAYING and input_controller.is_pause_toggle(event):
                    state = transition_state(state, GameState.PAUSED)
                    visual_feedback.trigger_state_transition()
                elif state == GameState.PAUSED and input_controller.is_pause_toggle(event):
                    state = transition_state(state, GameState.PLAYING)
                    visual_feedback.trigger_state_transition()
                elif state == GameState.GAME_OVER and input_controller.is_restart(event):
                    state = transition_state(state, GameState.PLAYING)
                    session.start_new_run()
                    audio.play_start_or_restart()
                    visual_feedback.trigger_state_transition()

        if state == GameState.PLAYING:
            movement_input = input_controller.movement_vector()
            collided = session.update_playing(delta_seconds, movement_input)
            if collided:
                audio.play_collision()
                visual_feedback.trigger_collision_feedback()
                if session.score_value > high_score:
                    high_score = session.score_value
                    save_high_score(high_score)
                state = transition_state(state, GameState.GAME_OVER)
                visual_feedback.trigger_state_transition()

            for center in session.consume_spawn_pulse_centers():
                visual_feedback.add_spawn_pulse(center)

        visual_feedback.update(delta_seconds)

        world_surface = pygame.Surface(screen.get_size())
        world_surface.fill((20, 20, 30))

        ui.draw_score(world_surface, session.score_value)

        if state == GameState.MENU:
            ui.draw_menu(world_surface, WINDOW_TITLE, high_score)
        elif state == GameState.PLAYING:
            label = "PLAYING: Move (WASD/Arrows or Left Stick)"
            session.draw_playing(world_surface)
            ui.draw_state_text(world_surface, label)
        elif state == GameState.PAUSED:
            session.draw_playing(world_surface)
            ui.draw_paused(world_surface, runtime_settings.audio_enabled)
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

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
