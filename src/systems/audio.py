"""Minimal audio manager with safe fallbacks."""

from __future__ import annotations

from pathlib import Path

import pygame

from .paths import asset_path


class AudioManager:
    def __init__(self) -> None:
        self._enabled = False
        self._start_sound: pygame.mixer.Sound | None = None
        self._collision_sound: pygame.mixer.Sound | None = None
        self._warning_printed = False
        self._initialize()

    def _initialize(self) -> None:
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            self._enabled = True
        except pygame.error:
            self._warn_once("Audio disabled: mixer initialization failed.")
            return

        self._start_sound = self._load_sound(asset_path("audio", "start.wav"))
        self._collision_sound = self._load_sound(asset_path("audio", "collision.wav"))

    def _load_sound(self, path: Path) -> pygame.mixer.Sound | None:
        try:
            return pygame.mixer.Sound(str(path))
        except (pygame.error, OSError):
            self._warn_once(f"Audio disabled for missing/unreadable sound: {path.name}")
            return None

    def play_start_or_restart(self) -> None:
        self._play(self._start_sound)

    def play_collision(self) -> None:
        self._play(self._collision_sound)

    def _play(self, sound: pygame.mixer.Sound | None) -> None:
        if not self._enabled or sound is None:
            return
        try:
            sound.play()
        except pygame.error:
            self._warn_once("Audio playback failed; continuing without sound.")

    def _warn_once(self, message: str) -> None:
        if not self._warning_printed:
            print(message)
            self._warning_printed = True
