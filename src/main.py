"""Task 0 entry point: minimal runnable Pygame window loop."""

from __future__ import annotations

import sys

import pygame


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Confetti Chaos"
TARGET_FPS = 60


def main() -> int:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 30))
        pygame.display.flip()
        clock.tick(TARGET_FPS)

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
