"""Task 1 entry point: minimal game loop with state transitions."""

from __future__ import annotations

from enum import Enum

import pygame

from enemies import Hazard
from player import Player


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


def create_player() -> Player:
    size = 40
    spawn_x = (WINDOW_WIDTH - size) / 2
    spawn_y = (WINDOW_HEIGHT - size) / 2
    return Player(spawn_x, spawn_y, size=size)


def create_hazards(bounds: pygame.Rect, player: Player) -> list[Hazard]:
    hazards = [Hazard() for _ in range(HAZARD_COUNT)]
    target = pygame.Vector2(player.rect.center)
    for hazard in hazards:
        hazard.reset_toward_target(bounds, target)
    return hazards


def main() -> int:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)
    world_bounds = screen.get_rect()
    player = create_player()
    hazards = create_hazards(world_bounds, player)

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
                    player = create_player()
                    hazards = create_hazards(world_bounds, player)
                elif state == GameState.PLAYING and event.key == pygame.K_k:
                    state = transition_state(state, GameState.GAME_OVER)
                elif state == GameState.GAME_OVER and event.key in (pygame.K_r, pygame.K_SPACE):
                    state = transition_state(state, GameState.PLAYING)
                    player = create_player()
                    hazards = create_hazards(world_bounds, player)

        if state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            player.update(delta_seconds, keys, world_bounds)
            player_center = pygame.Vector2(player.rect.center)
            for hazard in hazards:
                hazard.update(delta_seconds)
                if hazard.is_out_of_bounds(world_bounds):
                    hazard.reset_toward_target(world_bounds, player_center)
                if player.rect.colliderect(hazard.rect):
                    state = transition_state(state, GameState.GAME_OVER)
                    break

        screen.fill((20, 20, 30))

        if state == GameState.MENU:
            label = "MENU: Press Space or Enter to Start"
        elif state == GameState.PLAYING:
            label = "PLAYING: Avoid hazards (WASD/Arrows)"
            for hazard in hazards:
                hazard.draw(screen)
            player.draw(screen)
        else:
            label = "GAME OVER: Press R or Space to Restart"

        text_surface = font.render(label, True, (235, 235, 235))
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
