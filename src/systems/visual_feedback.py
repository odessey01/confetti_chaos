"""Lightweight visual feedback effects for gameplay clarity."""

from __future__ import annotations

import random

import pygame


class VisualFeedback:
    def __init__(self) -> None:
        self._flash_timer = 0.0
        self._flash_duration = 0.14
        self._fade_timer = 0.0
        self._fade_duration = 0.26
        self._shake_timer = 0.0
        self._shake_duration = 0.18
        self._shake_amplitude = 5.0
        self._spawn_pulses: list[dict[str, object]] = []

    def update(self, delta_seconds: float) -> None:
        self._flash_timer = max(0.0, self._flash_timer - delta_seconds)
        self._fade_timer = max(0.0, self._fade_timer - delta_seconds)
        self._shake_timer = max(0.0, self._shake_timer - delta_seconds)

        next_pulses: list[dict[str, object]] = []
        for pulse in self._spawn_pulses:
            remaining = float(pulse["remaining"]) - delta_seconds
            if remaining > 0:
                pulse["remaining"] = remaining
                next_pulses.append(pulse)
        self._spawn_pulses = next_pulses

    def trigger_collision_feedback(self) -> None:
        self._flash_timer = self._flash_duration
        self._shake_timer = self._shake_duration
        self._fade_timer = self._fade_duration

    def trigger_state_transition(self) -> None:
        self._fade_timer = self._fade_duration

    def add_spawn_pulse(self, center: tuple[int, int]) -> None:
        self._spawn_pulses.append(
            {
                "center": center,
                "remaining": 0.22,
                "duration": 0.22,
            }
        )

    def camera_offset(self) -> tuple[int, int]:
        if self._shake_timer <= 0:
            return (0, 0)
        progress = self._shake_timer / self._shake_duration
        amp = self._shake_amplitude * progress
        x = int(random.uniform(-amp, amp))
        y = int(random.uniform(-amp, amp))
        return (x, y)

    def draw_overlays(self, surface: pygame.Surface) -> None:
        if self._fade_timer > 0:
            alpha = int(120 * (self._fade_timer / self._fade_duration))
            fade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            fade.fill((15, 15, 20, alpha))
            surface.blit(fade, (0, 0))

        if self._flash_timer > 0:
            alpha = int(140 * (self._flash_timer / self._flash_duration))
            flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash.fill((255, 110, 110, alpha))
            surface.blit(flash, (0, 0))

        for pulse in self._spawn_pulses:
            remaining = float(pulse["remaining"])
            duration = float(pulse["duration"])
            center = tuple(pulse["center"])  # type: ignore[arg-type]
            progress = 1.0 - (remaining / duration)
            radius = int(12 + 24 * progress)
            alpha = int(130 * (1.0 - progress))
            if alpha <= 0:
                continue
            width = max(1, int(3 - 2 * progress))
            color = (255, 190, 120, alpha)
            ring = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(ring, color, center, max(1, radius), width)
            surface.blit(ring, (0, 0))
