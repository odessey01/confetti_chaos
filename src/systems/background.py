"""Background rendering system with themed gradients and lightweight ambient layers."""

from __future__ import annotations

from dataclasses import dataclass
import random

import pygame


@dataclass(frozen=True)
class BackgroundTheme:
    top_color: tuple[int, int, int]
    mid_color: tuple[int, int, int]
    bottom_color: tuple[int, int, int]
    texture_tint: tuple[int, int, int, int]
    ambient_color: tuple[int, int, int, int]
    density_multiplier: float
    drift_multiplier: float


@dataclass
class AmbientParticle:
    x: float
    y: float
    vx: float
    vy: float
    radius: int
    layer: int


class BackgroundRenderer:
    """Renders a cached gradient background plus ambient depth layers."""

    LAYER_PARALLAX = (0.08, 0.18, 0.34)
    LAYER_COUNT = (24, 18, 14)

    THEMES: dict[str, BackgroundTheme] = {
        "STANDARD": BackgroundTheme(
            top_color=(12, 33, 44),
            mid_color=(20, 52, 68),
            bottom_color=(42, 73, 92),
            texture_tint=(218, 235, 246, 14),
            ambient_color=(215, 238, 248, 48),
            density_multiplier=1.0,
            drift_multiplier=1.0,
        ),
        "SWARM": BackgroundTheme(
            top_color=(17, 44, 58),
            mid_color=(29, 71, 91),
            bottom_color=(56, 94, 117),
            texture_tint=(226, 246, 255, 18),
            ambient_color=(225, 245, 255, 56),
            density_multiplier=1.18,
            drift_multiplier=1.1,
        ),
        "HUNTERS": BackgroundTheme(
            top_color=(7, 18, 26),
            mid_color=(14, 34, 47),
            bottom_color=(33, 51, 66),
            texture_tint=(185, 213, 232, 12),
            ambient_color=(196, 220, 240, 40),
            density_multiplier=0.85,
            drift_multiplier=0.92,
        ),
        "STORM": BackgroundTheme(
            top_color=(12, 28, 40),
            mid_color=(21, 56, 77),
            bottom_color=(50, 87, 113),
            texture_tint=(228, 246, 255, 20),
            ambient_color=(232, 247, 255, 62),
            density_multiplier=1.25,
            drift_multiplier=1.24,
        ),
    }

    def __init__(self, size: tuple[int, int], *, seed: int = 1337) -> None:
        self._rng = random.Random(seed)
        self._size = size
        self._theme_name = "STANDARD"
        self._theme = self.THEMES[self._theme_name]
        self._gradient_cache: dict[tuple[object, ...], pygame.Surface] = {}
        self._texture_cache: dict[tuple[object, ...], pygame.Surface] = {}
        self._ambient_surface = pygame.Surface(size, pygame.SRCALPHA)
        self._particles: list[AmbientParticle] = []
        self._initialize_particles()

    @property
    def active_theme_name(self) -> str:
        return self._theme_name

    @property
    def particle_capacity(self) -> int:
        return len(self._particles)

    def update(
        self,
        delta_seconds: float,
        *,
        flavor_name: str = "STANDARD",
    ) -> None:
        self._set_theme(flavor_name)
        width, height = self._size
        for particle in self._particles:
            layer_speed = (1.0 + (particle.layer * 0.22)) * self._theme.drift_multiplier
            particle.x += particle.vx * delta_seconds * layer_speed
            particle.y += particle.vy * delta_seconds * layer_speed
            if particle.x < -8:
                particle.x = width + self._rng.uniform(0.0, 8.0)
            elif particle.x > width + 8:
                particle.x = -self._rng.uniform(0.0, 8.0)
            if particle.y < -8:
                particle.y = height + self._rng.uniform(0.0, 8.0)
            elif particle.y > height + 8:
                particle.y = -self._rng.uniform(0.0, 8.0)

    def draw(
        self,
        surface: pygame.Surface,
        *,
        player_center: tuple[int, int] | None = None,
    ) -> None:
        self._ensure_size((surface.get_width(), surface.get_height()))
        gradient = self._gradient_surface()
        texture = self._texture_surface()
        surface.blit(gradient, (0, 0))
        surface.blit(texture, (0, 0))
        self._draw_ambient(surface, player_center=player_center)

    def _set_theme(self, flavor_name: str) -> None:
        resolved = flavor_name if flavor_name in self.THEMES else "STANDARD"
        if resolved == self._theme_name:
            return
        self._theme_name = resolved
        self._theme = self.THEMES[resolved]

    def _ensure_size(self, size: tuple[int, int]) -> None:
        if size == self._size:
            return
        self._size = size
        self._ambient_surface = pygame.Surface(size, pygame.SRCALPHA)
        self._gradient_cache.clear()
        self._texture_cache.clear()
        self._initialize_particles()

    def _initialize_particles(self) -> None:
        width, height = self._size
        self._particles = []
        for layer, count in enumerate(self.LAYER_COUNT):
            for _ in range(count):
                self._particles.append(
                    AmbientParticle(
                        x=self._rng.uniform(0.0, width),
                        y=self._rng.uniform(0.0, height),
                        vx=self._rng.uniform(-10.0, 10.0),
                        vy=self._rng.uniform(4.0, 18.0),
                        radius=1 + layer,
                        layer=layer,
                    )
                )

    def _gradient_surface(self) -> pygame.Surface:
        width, height = self._size
        key = (width, height, self._theme_name, "gradient")
        cached = self._gradient_cache.get(key)
        if cached is not None:
            return cached
        gradient = pygame.Surface((width, height)).convert()
        for y in range(height):
            t = y / max(1, height - 1)
            if t < 0.5:
                local_t = t / 0.5
                color = self._lerp_color(self._theme.top_color, self._theme.mid_color, local_t)
            else:
                local_t = (t - 0.5) / 0.5
                color = self._lerp_color(self._theme.mid_color, self._theme.bottom_color, local_t)
            pygame.draw.line(gradient, color, (0, y), (width, y))
        self._gradient_cache[key] = gradient
        return gradient

    def _texture_surface(self) -> pygame.Surface:
        width, height = self._size
        key = (width, height, self._theme_name, "texture")
        cached = self._texture_cache.get(key)
        if cached is not None:
            return cached
        texture = pygame.Surface((width, height), pygame.SRCALPHA)
        tint = self._theme.texture_tint
        sample_count = max(120, int((width * height) / 3800))
        for _ in range(sample_count):
            x = self._rng.randrange(0, width)
            y = self._rng.randrange(0, height)
            radius = self._rng.choice((1, 1, 2))
            pygame.draw.circle(texture, tint, (x, y), radius)
        self._texture_cache[key] = texture
        return texture

    def _draw_ambient(
        self,
        surface: pygame.Surface,
        *,
        player_center: tuple[int, int] | None,
    ) -> None:
        width, height = self._size
        self._ambient_surface.fill((0, 0, 0, 0))
        if player_center is None:
            px = width / 2
            py = height / 2
        else:
            px, py = float(player_center[0]), float(player_center[1])
        offset_x = ((px - (width / 2)) / max(1.0, width / 2))
        offset_y = ((py - (height / 2)) / max(1.0, height / 2))
        active_counts = [max(1, int(c * self._theme.density_multiplier)) for c in self.LAYER_COUNT]
        draw_limits = {
            layer: min(active_counts[layer], self.LAYER_COUNT[layer])
            for layer in range(len(self.LAYER_COUNT))
        }
        drawn_per_layer = [0, 0, 0]
        for particle in self._particles:
            layer = particle.layer
            if drawn_per_layer[layer] >= draw_limits[layer]:
                continue
            parallax = self.LAYER_PARALLAX[layer]
            draw_x = int(particle.x - (offset_x * parallax * 20.0))
            draw_y = int(particle.y - (offset_y * parallax * 14.0))
            pygame.draw.circle(
                self._ambient_surface,
                self._theme.ambient_color,
                (draw_x, draw_y),
                particle.radius,
            )
            drawn_per_layer[layer] += 1
        surface.blit(self._ambient_surface, (0, 0))

    def _lerp_color(
        self,
        a: tuple[int, int, int],
        b: tuple[int, int, int],
        t: float,
    ) -> tuple[int, int, int]:
        clamped = max(0.0, min(1.0, t))
        return (
            int(a[0] + (b[0] - a[0]) * clamped),
            int(a[1] + (b[1] - a[1]) * clamped),
            int(a[2] + (b[2] - a[2]) * clamped),
        )
