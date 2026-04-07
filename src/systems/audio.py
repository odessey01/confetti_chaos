"""Minimal audio manager with safe fallbacks."""

from __future__ import annotations

from pathlib import Path

import pygame

from .paths import asset_path


class AudioManager:
    def __init__(self) -> None:
        self._enabled = False
        self._user_enabled = True
        self._music_loaded = False
        self._music_playing = False
        self._music_should_play = False
        self._start_sound: pygame.mixer.Sound | None = None
        self._collision_sound: pygame.mixer.Sound | None = None
        self._boss_defeat_sound: pygame.mixer.Sound | None = None
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
        self._boss_defeat_sound = self._load_sound(asset_path("audio", "boss_defeat.wav"), warn=False)
        if self._boss_defeat_sound is None:
            self._boss_defeat_sound = self._start_sound
        self._music_loaded = self._load_music_track()

    def _load_sound(self, path: Path, warn: bool = True) -> pygame.mixer.Sound | None:
        try:
            return pygame.mixer.Sound(str(path))
        except (pygame.error, OSError):
            if warn:
                self._warn_once(f"Audio disabled for missing/unreadable sound: {path.name}")
            return None

    def _load_music_track(self) -> bool:
        candidates = [
            asset_path("audio", "music.ogg"),
            asset_path("audio", "music.wav"),
            asset_path("audio", "start.wav"),
        ]
        for path in candidates:
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(0.35)
                return True
            except (pygame.error, OSError):
                continue
        self._warn_once("Background music unavailable; continuing without music loop.")
        return False

    def play_start_or_restart(self) -> None:
        self._play(self._start_sound)

    def play_collision(self) -> None:
        self._play(self._collision_sound)

    def play_boss_victory(self) -> None:
        self._play(self._boss_defeat_sound)

    def set_enabled(self, enabled: bool) -> None:
        self._user_enabled = enabled
        self._sync_music_playback()

    def sync_music_for_state(self, state_name: str) -> None:
        self._music_should_play = state_name in {"MENU", "PLAYING", "PAUSED", "GAME_OVER"}
        self._sync_music_playback()

    def _play(self, sound: pygame.mixer.Sound | None) -> None:
        if not self._enabled or not self._user_enabled or sound is None:
            return
        try:
            sound.play()
        except pygame.error:
            self._warn_once("Audio playback failed; continuing without sound.")

    def _sync_music_playback(self) -> None:
        can_play_music = (
            self._enabled
            and self._user_enabled
            and self._music_loaded
            and self._music_should_play
        )
        if can_play_music and not self._music_playing:
            try:
                pygame.mixer.music.play(-1)
                self._music_playing = True
            except pygame.error:
                self._warn_once("Background music playback failed; continuing without music loop.")
                self._music_playing = False
        elif not can_play_music and self._music_playing:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
            self._music_playing = False

    def _warn_once(self, message: str) -> None:
        if not self._warning_printed:
            print(message)
            self._warning_printed = True
