"""Validation tests for background rendering behavior."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.background import BackgroundRenderer  # noqa: E402


class BackgroundRendererValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.size = (1280, 720)

    def test_background_draws_without_black_fill_default(self) -> None:
        renderer = BackgroundRenderer(self.size, seed=7)
        surface = pygame.Surface(self.size)
        renderer.update(1 / 60, flavor_name="STANDARD")
        renderer.draw(surface, player_center=(640, 360))
        self.assertNotEqual(surface.get_at((20, 20))[:3], (0, 0, 0))

    def test_flavor_theme_switch_changes_output_palette(self) -> None:
        renderer = BackgroundRenderer(self.size, seed=11)
        surface = pygame.Surface(self.size)
        renderer.update(1 / 60, flavor_name="STANDARD")
        renderer.draw(surface, player_center=(640, 360))
        standard_pixel = surface.get_at((200, 80))[:3]
        renderer.update(1 / 60, flavor_name="HUNTERS")
        renderer.draw(surface, player_center=(640, 360))
        hunters_pixel = surface.get_at((200, 80))[:3]
        self.assertNotEqual(standard_pixel, hunters_pixel)
        self.assertEqual(renderer.active_theme_name, "HUNTERS")

    def test_particle_pool_stays_bounded_across_updates(self) -> None:
        renderer = BackgroundRenderer(self.size, seed=123)
        initial_capacity = renderer.particle_capacity
        for _ in range(180):
            renderer.update(1 / 60, flavor_name="STORM")
        self.assertEqual(renderer.particle_capacity, initial_capacity)

    def test_parallax_draw_accepts_player_offset(self) -> None:
        renderer = BackgroundRenderer(self.size, seed=5)
        surface_center = pygame.Surface(self.size)
        surface_edge = pygame.Surface(self.size)
        renderer.update(1 / 60, flavor_name="SWARM")
        renderer.draw(surface_center, player_center=(640, 360))
        renderer.draw(surface_edge, player_center=(1100, 620))
        self.assertEqual(surface_center.get_size(), surface_edge.get_size())

