"""Task 1 entry point: minimal game loop with state transitions."""

from __future__ import annotations

from enum import Enum

import pygame

from systems import (
    AudioManager,
    GameSession,
    UiRenderer,
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
    ui = UiRenderer()
    world_bounds = screen.get_rect()
    session = GameSession(world_bounds, hazard_count=HAZARD_COUNT)

    state = GameState.MENU
    running = True
    while running:
        delta_seconds = clock.tick(TARGET_FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == GameState.MENU and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    state = transition_state(state, GameState.PLAYING)
                    session.start_new_run()
                    audio.play_start_or_restart()
                elif state == GameState.MENU and event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                elif state == GameState.GAME_OVER and event.key in (pygame.K_r, pygame.K_SPACE):
                    state = transition_state(state, GameState.PLAYING)
                    session.start_new_run()
                    audio.play_start_or_restart()

        if state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            collided = session.update_playing(delta_seconds, keys)
            if collided:
                audio.play_collision()
                if session.score_value > high_score:
                    high_score = session.score_value
                    save_high_score(high_score)
                state = transition_state(state, GameState.GAME_OVER)

        screen.fill((20, 20, 30))

        ui.draw_score(screen, session.score_value)

        if state == GameState.MENU:
            ui.draw_menu(screen, WINDOW_TITLE, high_score)
        elif state == GameState.PLAYING:
            label = "PLAYING: Avoid hazards (WASD/Arrows)"
            session.draw_playing(screen)
            ui.draw_state_text(screen, label)
        else:
            label = (
                f"GAME OVER: Score {session.score_value} | High Score {high_score} "
                "- Press R or Space to Restart"
            )
            ui.draw_state_text(screen, label)

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
