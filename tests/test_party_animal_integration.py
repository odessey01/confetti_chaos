"""Integration checks for main-game party animal wiring."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.game_session import GameSession  # noqa: E402


class PartyAnimalIntegrationTests(unittest.TestCase):
    def test_default_player_variant_is_softer_plush_teddy(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        self.assertEqual(session.player.visual_variant_id, "teddy_f")

    def test_player_anchor_and_hitbox_are_stable(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        anchor = session.player_render_anchor()
        hitbox_center, hitbox_radius = session.player_hitbox_circle()
        self.assertEqual(anchor[0], session.player.rect.centerx)
        self.assertEqual(anchor[1], session.player.rect.bottom)
        self.assertEqual((hitbox_center.x, hitbox_center.y), session.player.rect.center)
        self.assertGreater(hitbox_radius, 0.0)

    def test_start_new_run_applies_selected_player_animal(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        session.start_new_run(player_animal_id="bunny_f")
        self.assertEqual(session.active_player_animal_id, "bunny_f")
        self.assertEqual(session.player.visual_variant_id, "bunny_f")

    def test_start_new_run_falls_back_to_teddy_on_invalid_selection(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        session.start_new_run(player_animal_id="invalid_variant")
        self.assertEqual(session.active_player_animal_id, "teddy_f")
        self.assertEqual(session.player.visual_variant_id, "teddy_f")

    def test_debug_overlay_draws(self) -> None:
        if not pygame.get_init():
            pygame.init()
        surface = pygame.Surface((1280, 720))
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        session.draw_player_debug_overlay(surface)
        self.assertIsInstance(surface, pygame.Surface)


if __name__ == "__main__":
    unittest.main()
