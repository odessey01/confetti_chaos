"""World XP pickup entity."""

from __future__ import annotations

import pygame


class XpDrop:
    """Lightweight XP pickup that can be collected by the player."""

    def __init__(
        self,
        position: pygame.Vector2,
        *,
        xp_value: int,
        size: int = 14,
        lifetime_seconds: float = 18.0,
        fade_duration_seconds: float = 3.0,
    ) -> None:
        self.position = pygame.Vector2(position)
        self.xp_value = max(1, int(xp_value))
        self.size = max(6, int(size))
        self._pulse_phase = 0.0
        self._age_seconds = 0.0
        self._lifetime_seconds = max(0.05, float(lifetime_seconds))
        self._fade_duration_seconds = max(
            0.0, min(float(fade_duration_seconds), self._lifetime_seconds * 0.9)
        )
        if self.xp_value >= 12:
            self._core_color = (255, 222, 110)
            self._glow_color = (255, 160, 76)
        elif self.xp_value >= 6:
            self._core_color = (166, 244, 255)
            self._glow_color = (86, 196, 255)
        else:
            self._core_color = (174, 255, 194)
            self._glow_color = (98, 220, 150)

    @property
    def rect(self) -> pygame.Rect:
        half = self.size // 2
        return pygame.Rect(
            int(self.position.x - half),
            int(self.position.y - half),
            self.size,
            self.size,
        )

    def is_expired(self) -> bool:
        return self._age_seconds >= self._lifetime_seconds

    def draw_alpha(self) -> int:
        if self._fade_duration_seconds <= 0.0:
            return 255
        fade_start = self._lifetime_seconds - self._fade_duration_seconds
        if self._age_seconds <= fade_start:
            return 255
        remaining = max(0.0, self._lifetime_seconds - self._age_seconds)
        return max(0, min(255, int((remaining / self._fade_duration_seconds) * 255.0)))

    def update(self, delta_seconds: float) -> None:
        clamped_delta = max(0.0, delta_seconds)
        self._age_seconds += clamped_delta
        self._pulse_phase = (self._pulse_phase + clamped_delta * 6.0) % 1.0

    def draw(self, surface: pygame.Surface) -> None:
        alpha = self.draw_alpha()
        if alpha <= 0:
            return
        pulse = 1.0 + (0.18 * abs((self._pulse_phase * 2.0) - 1.0))
        radius = max(4, int((self.size * 0.5) * pulse))
        halo_radius = radius + max(2, self.size // 4)
        draw_size = halo_radius * 2
        draw_surface = pygame.Surface((draw_size, draw_size), pygame.SRCALPHA)
        draw_center = (halo_radius, halo_radius)

        pygame.draw.circle(
            draw_surface,
            (*self._glow_color, int(78 * (alpha / 255.0))),
            draw_center,
            halo_radius,
        )
        pygame.draw.circle(draw_surface, (*self._glow_color, alpha), draw_center, radius)
        pygame.draw.circle(
            draw_surface,
            (*self._core_color, alpha),
            draw_center,
            max(2, int(radius * 0.58)),
        )
        pygame.draw.circle(draw_surface, (38, 58, 92, alpha), draw_center, radius, width=1)

        sparkle_extent = max(3, radius // 2)
        sparkle_color = (250, 252, 255)
        pygame.draw.line(
            draw_surface,
            (*sparkle_color, alpha),
            (draw_center[0] - sparkle_extent, draw_center[1]),
            (draw_center[0] + sparkle_extent, draw_center[1]),
            1,
        )
        pygame.draw.line(
            draw_surface,
            (*sparkle_color, alpha),
            (draw_center[0], draw_center[1] - sparkle_extent),
            (draw_center[0], draw_center[1] + sparkle_extent),
            1,
        )
        center = (int(self.position.x), int(self.position.y))
        surface.blit(draw_surface, (center[0] - halo_radius, center[1] - halo_radius))
