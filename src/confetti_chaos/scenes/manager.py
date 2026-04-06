from __future__ import annotations

from typing import Callable

from confetti_chaos.scenes.base import Scene

SceneFactory = Callable[["SceneManager"], Scene]


class SceneManager:
    def __init__(self) -> None:
        self._factories: dict[str, SceneFactory] = {}
        self._stack: list[Scene] = []
        self.should_quit = False

    def register(self, name: str, factory: SceneFactory) -> None:
        self._factories[name] = factory

    def push(self, name: str) -> Scene:
        scene = self._build(name)
        self._stack.append(scene)
        scene.on_enter()
        return scene

    def replace(self, name: str) -> Scene:
        if self._stack:
            current = self._stack.pop()
            current.on_exit()
        return self.push(name)

    def pop(self) -> None:
        if not self._stack:
            self.should_quit = True
            return

        current = self._stack.pop()
        current.on_exit()
        if not self._stack:
            self.should_quit = True

    def quit(self) -> None:
        self.should_quit = True

    @property
    def current(self) -> Scene:
        if not self._stack:
            raise RuntimeError("No active scene. Register and push a scene first.")
        return self._stack[-1]

    def _build(self, name: str) -> Scene:
        try:
            factory = self._factories[name]
        except KeyError as error:
            raise KeyError(f"Scene '{name}' has not been registered.") from error
        return factory(self)
