from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame

    from confetti_chaos.scenes.manager import SceneManager


class Scene(ABC):
    name = "scene"

    def __init__(self, manager: "SceneManager") -> None:
        self.manager = manager

    def on_enter(self) -> None:
        """Hook called when the scene becomes active."""

    def on_exit(self) -> None:
        """Hook called when the scene is replaced or popped."""

    @abstractmethod
    def handle_event(self, event: "pygame.event.Event") -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self, surface: "pygame.Surface") -> None:
        raise NotImplementedError
