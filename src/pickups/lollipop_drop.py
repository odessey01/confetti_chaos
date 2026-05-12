"""World health pickup dropped from pinatas."""

from __future__ import annotations

import pygame


class LollipopDrop:
    """Simple healing pickup with lightweight animated rendering."""

    def __init__(
        self,
        position: pygame.Vector2,
        *,
        size: int = 16,
        lifetime_seconds: float = 14.0,
        fade_duration_seconds: float = 2.5,
    ) -> None:
        self.position = pygame.Vector2(position)
        self.size = max(8, int(size))
        self._pulse_phase = 0.0
        self._age_seconds = 0.0
        self._lifetime_seconds = max(0.05, float(lifetime_seconds))
        self._fade_duration_seconds = max(
            0.0, min(float(fade_duration_seconds), self._lifetime_seconds * 0.9)
        )

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
        clamped_delta = max(0.0, float(delta_seconds))
        self._age_seconds += clamped_delta
        self._pulse_phase = (self._pulse_phase + clamped_delta * 5.0) % 1.0

    def draw(self, surface: pygame.Surface) -> None:
        alpha = self.draw_alpha()
        if alpha <= 0:
            return
        pulse = 1.0 + (0.16 * abs((self._pulse_phase * 2.0) - 1.0))
        candy_radius = max(4, int((self.size * 0.42) * pulse))
        halo_radius = candy_radius + 4
        draw_size = halo_radius * 2 + 2
        draw_surface = pygame.Surface((draw_size, draw_size), pygame.SRCALPHA)
        center = (draw_size // 2, draw_size // 2)

        # Glow and candy.
        pygame.draw.circle(draw_surface, (255, 122, 176, int(72 * (alpha / 255.0))), center, halo_radius)
        pygame.draw.circle(draw_surface, (255, 98, 166, alpha), center, candy_radius)
        pygame.draw.circle(draw_surface, (255, 224, 238, alpha), center, max(2, int(candy_radius * 0.46)))

        # Stick.
        stick_top = (center[0], center[1] + candy_radius - 1)
        stick_bottom = (center[0], min(draw_size - 2, center[1] + candy_radius + max(6, self.size // 2)))
        pygame.draw.line(draw_surface, (246, 246, 246, alpha), stick_top, stick_bottom, 2)
        pygame.draw.line(
            draw_surface,
            (225, 225, 225, int(alpha * 0.75)),
            (stick_top[0] + 1, stick_top[1]),
            (stick_bottom[0] + 1, stick_bottom[1]),
            1,
        )

        world_x = int(self.position.x) - (draw_size // 2)
        world_y = int(self.position.y) - (draw_size // 2)
        surface.blit(draw_surface, (world_x, world_y))
