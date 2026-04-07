"""Centralized audio manager with SFX, music, and ambient categories."""

from __future__ import annotations

from pathlib import Path
import random

import pygame

from .paths import asset_path


class AudioManager:
    def __init__(self) -> None:
        self._enabled = False
        self._user_enabled = True
        self._music_loaded = False
        self._music_playing = False
        self._music_should_play = False
        self._desired_music_track: str | None = None
        self._current_music_track: str | None = None
        self._ambient_channel: pygame.mixer.Channel | None = None
        self._ambient_playing = False
        self._current_ambient_track: str | None = None
        self._sfx_cache: dict[str, pygame.mixer.Sound] = {}
        self._sfx_path_cache: dict[Path, pygame.mixer.Sound] = {}
        self._ambient_cache: dict[str, pygame.mixer.Sound] = {}
        self._last_sfx_played_at_ms: dict[str, int] = {}
        self._sfx_cooldown_ms = {
            "weapon_fire": 60,
            "balloon_hit": 35,
            "balloon_pop": 45,
            "ui_nav": 95,
        }
        self._sfx_volume_variation = {
            "weapon_fire": 0.08,
            "balloon_pop": 0.07,
            "ui_nav": 0.05,
        }
        self._sfx_variant_enabled = {"weapon_fire", "balloon_pop", "ui_nav"}

        def _candidates(category: str, *names: str) -> list[Path]:
            paths: list[Path] = []
            for name in names:
                paths.append(asset_path("audio", category, name))
                paths.append(asset_path("audio", name))
            # Keep deterministic order while dropping duplicates.
            return list(dict.fromkeys(paths))

        self._sfx_registry = {
            "start": _candidates("sfx", "start.wav"),
            "collision": _candidates("sfx", "collision.wav"),
            "boss_defeat": _candidates("sfx", "boss_defeat.wav", "start.wav"),
            "boss_spawn": _candidates("sfx", "boss_spawn.wav", "level_transition.wav"),
            "boss_hit": _candidates("sfx", "boss_hit.wav", "balloon_hit.wav", "collision.wav"),
            "milestone_clear": _candidates("sfx", "milestone_clear.wav", "level_transition.wav", "start.wav"),
            "confetti_celebration": _candidates("sfx", "confetti_celebration.wav", "boss_defeat.wav", "start.wav"),
            "weapon_fire": _candidates("sfx", "weapon_fire_1.wav", "weapon_fire_2.wav", "weapon_fire.wav", "start.wav"),
            "balloon_hit": _candidates("sfx", "balloon_hit.wav", "collision.wav"),
            "balloon_pop": _candidates("sfx", "balloon_pop_1.wav", "balloon_pop_2.wav", "balloon_pop.wav", "collision.wav"),
            "player_damage_or_death": _candidates("sfx", "player_damage.wav", "collision.wav"),
            "level_transition": _candidates("sfx", "level_transition.wav", "start.wav"),
            "ui_nav": _candidates("sfx", "ui_nav_1.wav", "ui_nav_2.wav", "ui_nav.wav", "start.wav"),
            "ui_confirm": _candidates("sfx", "ui_confirm.wav", "start.wav"),
            "ui_back": _candidates("sfx", "ui_back.wav", "start.wav"),
            "ui_pause": _candidates("sfx", "ui_pause.wav", "start.wav"),
            "ui_resume": _candidates("sfx", "ui_resume.wav", "start.wav"),
            "ui_toggle_settings": _candidates("sfx", "ui_toggle.wav", "start.wav"),
        }
        self._music_registry = {
            "menu": _candidates(
                "music",
                "denis-pavlov-music-podcast-lo-fi-music-205515.mp3",
                "music_menu.ogg",
                "music_menu.wav",
                "music.ogg",
                "music.wav",
            ),
            "gameplay": _candidates(
                "music",
                "denis-pavlov-music-podcast-lo-fi-music-205515.mp3",
                "music_gameplay.ogg",
                "music_gameplay.wav",
                "music.ogg",
                "music.wav",
            ),
            "boss": _candidates(
                "music",
                "music_boss.ogg",
                "music_boss.wav",
                "denis-pavlov-music-podcast-lo-fi-music-205515.mp3",
                "music_gameplay.ogg",
                "music.ogg",
            ),
        }
        self._ambient_registry = {
            "gameplay": _candidates(
                "ambient",
                "ambient_gameplay.ogg",
                "ambient_gameplay.wav",
            )
        }
        self._warning_printed = False
        self._master_volume = 0.8
        self._music_volume = 0.7
        self._sfx_volume = 0.9
        self._ambient_volume = 0.5
        self._initialize()

    @staticmethod
    def _clamp_volume(value: float) -> float:
        return max(0.0, min(float(value), 1.0))

    def _effective_music_volume(self) -> float:
        return self._master_volume * self._music_volume

    def _effective_sfx_volume(self) -> float:
        return self._master_volume * self._sfx_volume

    def _effective_ambient_volume(self) -> float:
        return self._master_volume * self._ambient_volume

    def _initialize(self) -> None:
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            self._enabled = True
        except pygame.error:
            self._warn_once("Audio disabled: mixer initialization failed.")
            return

        self._ambient_channel = self._try_create_ambient_channel(channel_id=2)
        self._prime_sfx_cache()

    def _load_sound(self, path: Path, warn: bool = True) -> pygame.mixer.Sound | None:
        try:
            return pygame.mixer.Sound(str(path))
        except (pygame.error, OSError):
            if warn:
                self._warn_once(f"Audio disabled for missing/unreadable sound: {path.name}")
            return None

    def _try_create_ambient_channel(self, channel_id: int) -> pygame.mixer.Channel | None:
        try:
            return pygame.mixer.Channel(channel_id)
        except pygame.error:
            return None

    def _prime_sfx_cache(self) -> None:
        for name in ("start", "collision", "boss_defeat"):
            sound = self._load_named_sound(name, category="sfx", warn=False)
            if sound is not None:
                self._sfx_cache[name] = sound

    def _resolve_paths(self, name: str, *, category: str) -> list[Path]:
        if category == "sfx":
            return self._sfx_registry.get(name, [])
        if category == "music":
            return self._music_registry.get(name, [])
        if category == "ambient":
            return self._ambient_registry.get(name, [])
        return []

    def _load_named_sound(self, name: str, *, category: str, warn: bool = True) -> pygame.mixer.Sound | None:
        if category == "sfx":
            return self._load_sfx_sound(name, warn=warn)
        cache = self._sfx_cache if category == "sfx" else self._ambient_cache
        if name in cache:
            return cache[name]
        for path in self._resolve_paths(name, category=category):
            sound = self._load_sound(path, warn=False)
            if sound is not None:
                cache[name] = sound
                return sound
        if warn:
            self._warn_once(f"Audio asset missing for {category}: {name}")
        return None

    def _load_sfx_sound(self, name: str, *, warn: bool = True) -> pygame.mixer.Sound | None:
        paths = self._resolve_paths(name, category="sfx")
        if not paths:
            if warn:
                self._warn_once(f"Audio asset missing for sfx: {name}")
            return None

        loaded_candidates: list[pygame.mixer.Sound] = []
        for path in paths:
            sound = self._sfx_path_cache.get(path)
            if sound is None:
                sound = self._load_sound(path, warn=False)
                if sound is not None:
                    self._sfx_path_cache[path] = sound
            if sound is not None:
                loaded_candidates.append(sound)

        if not loaded_candidates:
            if warn:
                self._warn_once(f"Audio asset missing for sfx: {name}")
            return None

        if name in self._sfx_variant_enabled and len(loaded_candidates) > 1:
            return random.choice(loaded_candidates)
        return loaded_candidates[0]

    def _sfx_playback_volume(self, name: str) -> float:
        base_volume = self._effective_sfx_volume()
        jitter = self._sfx_volume_variation.get(name, 0.0)
        if jitter <= 0.0:
            return base_volume
        multiplier = random.uniform(1.0 - jitter, 1.0 + jitter)
        return self._clamp_volume(base_volume * multiplier)

    def _load_music_track(self, track: str) -> bool:
        for path in self._resolve_paths(track, category="music"):
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(self._effective_music_volume())
                return True
            except (pygame.error, OSError):
                continue
        self._warn_once(f"Background music unavailable for track: {track}")
        return False

    def play_start_or_restart(self) -> None:
        self.play_sfx("start")

    def play_collision(self) -> None:
        self.play_sfx("collision")

    def play_boss_victory(self) -> None:
        self.play_sfx("boss_defeat")

    def set_enabled(self, enabled: bool) -> None:
        self._user_enabled = enabled
        self._sync_music_playback()
        if not self._user_enabled:
            self.stop_ambient()

    def apply_mix(self, *, master: float, music: float, sfx: float, ambient: float) -> None:
        self._master_volume = self._clamp_volume(master)
        self._music_volume = self._clamp_volume(music)
        self._sfx_volume = self._clamp_volume(sfx)
        self._ambient_volume = self._clamp_volume(ambient)
        self._apply_live_mix()

    def _apply_live_mix(self) -> None:
        if not self._enabled:
            return
        try:
            pygame.mixer.music.set_volume(self._effective_music_volume())
        except pygame.error:
            pass
        if self._ambient_channel is not None:
            try:
                self._ambient_channel.set_volume(self._effective_ambient_volume())
            except pygame.error:
                pass

    def sync_music_for_state(self, state_name: str) -> None:
        self._music_should_play = state_name in {"MENU", "PLAYING", "PAUSED", "GAME_OVER"}
        desired_track = "menu" if state_name == "MENU" else "gameplay"
        if self._music_should_play:
            self.play_music(desired_track)
        else:
            self._desired_music_track = None
            self.stop_music()

    def play_sfx(self, name: str) -> None:
        if self._is_sfx_on_cooldown(name):
            return
        sound = self._load_named_sound(name, category="sfx")
        self._play(sound, volume=self._sfx_playback_volume(name))
        self._last_sfx_played_at_ms[name] = pygame.time.get_ticks()

    def play_music(self, track: str) -> None:
        self._desired_music_track = track
        if not self._enabled or not self._user_enabled:
            return
        if self._music_playing and self._current_music_track == track:
            return
        if not self._load_music_track(track):
            self._music_loaded = False
            self._music_playing = False
            return
        self._music_loaded = True
        try:
            pygame.mixer.music.play(-1)
            self._music_playing = True
            self._current_music_track = track
        except pygame.error:
            self._warn_once("Background music playback failed; continuing without music loop.")
            self._music_playing = False
            self._current_music_track = None

    def stop_music(self) -> None:
        if not self._music_playing:
            self._current_music_track = None
            return
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
        self._music_playing = False
        self._current_music_track = None

    def play_ambient(self, track: str) -> None:
        if not self._enabled or not self._user_enabled:
            return
        if self._ambient_playing and self._current_ambient_track == track:
            return
        sound = self._load_named_sound(track, category="ambient")
        if sound is None:
            return
        if self._ambient_channel is None:
            self._ambient_channel = self._try_create_ambient_channel(channel_id=2)
        if self._ambient_channel is None:
            self._warn_once("Ambient channel unavailable; continuing without ambient loop.")
            return
        try:
            self._ambient_channel.set_volume(self._effective_ambient_volume())
            self._ambient_channel.play(sound, loops=-1)
            self._ambient_playing = True
            self._current_ambient_track = track
        except pygame.error:
            self._warn_once("Ambient playback failed; continuing without ambient loop.")

    def stop_ambient(self) -> None:
        if self._ambient_channel is not None:
            try:
                self._ambient_channel.stop()
            except pygame.error:
                pass
        self._ambient_playing = False
        self._current_ambient_track = None

    def _play(self, sound: pygame.mixer.Sound | None, *, volume: float | None = None) -> None:
        if not self._enabled or not self._user_enabled or sound is None:
            return
        try:
            sound.set_volume(self._effective_sfx_volume() if volume is None else self._clamp_volume(volume))
            sound.play()
        except pygame.error:
            self._warn_once("Audio playback failed; continuing without sound.")

    def _is_sfx_on_cooldown(self, name: str) -> bool:
        cooldown = self._sfx_cooldown_ms.get(name, 0)
        if cooldown <= 0:
            return False
        last = self._last_sfx_played_at_ms.get(name)
        if last is None:
            return False
        return (pygame.time.get_ticks() - last) < cooldown

    def _sync_music_playback(self) -> None:
        if not self._enabled or not self._user_enabled:
            self.stop_music()
            return
        if self._music_should_play and self._desired_music_track is not None:
            self.play_music(self._desired_music_track)
        elif not self._music_should_play:
            self.stop_music()

    def _warn_once(self, message: str) -> None:
        if not self._warning_printed:
            print(message)
            self._warning_printed = True
