from __future__ import annotations

import pygame

from confetti_chaos.save_data import load_save, save_game
from confetti_chaos.scenes import GameplayScene, SceneManager, TitleScene
from confetti_chaos.settings import load_settings


def run() -> None:
    settings = load_settings()
    save_data = load_save()

    pygame.init()
    pygame.display.set_caption(settings.title)

    flags = pygame.FULLSCREEN if settings.fullscreen else 0
    screen = pygame.display.set_mode(settings.window_size, flags)
    clock = pygame.time.Clock()

    scene_manager = SceneManager()
    scene_manager.register("title", TitleScene)
    scene_manager.register("gameplay", GameplayScene)
    scene_manager.push(settings.starting_scene)

    while not scene_manager.should_quit:
        dt = clock.tick(settings.fps) / 1000.0

        for event in pygame.event.get():
            scene_manager.current.handle_event(event)

        scene_manager.current.update(dt)
        scene_manager.current.render(screen)
        pygame.display.flip()

    save_data.last_scene = scene_manager.current.name if not scene_manager.should_quit else "title"
    save_game(save_data)
    pygame.quit()
