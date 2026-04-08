"""Validation tests for shared party-animal rendering module."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from player import Player  # noqa: E402
from systems.party_animals import (  # noqa: E402
    DEFAULT_PARTY_ANIMAL_ID,
    PARTY_ANIMAL_CONFIGS_BY_ID,
    PLAYABLE_PARTY_ANIMAL_IDS,
    SHARED_PARTY_ACCESSORY_RULES,
    draw_party_animal_shape,
    get_party_animal,
)


class PartyAnimalVisualTests(unittest.TestCase):
    def test_default_party_animal_is_registered(self) -> None:
        self.assertIn(DEFAULT_PARTY_ANIMAL_ID, PARTY_ANIMAL_CONFIGS_BY_ID)
        cfg = get_party_animal(DEFAULT_PARTY_ANIMAL_ID)
        self.assertEqual(cfg.variant_id, DEFAULT_PARTY_ANIMAL_ID)
        self.assertEqual(cfg.display_name, "Teddy")

    def test_shared_accessory_rules_are_party_hat_based(self) -> None:
        self.assertEqual(SHARED_PARTY_ACCESSORY_RULES["type"], "party_hat")

    def test_playable_party_animals_are_registered(self) -> None:
        for variant_id in PLAYABLE_PARTY_ANIMAL_IDS:
            self.assertIn(variant_id, PARTY_ANIMAL_CONFIGS_BY_ID)

    def test_shape_renderer_draws_registered_variants_without_error(self) -> None:
        surface = pygame.Surface((640, 360))
        player = Player(280, 140, size=56)
        player.facing = pygame.Vector2(1.0, 0.0)
        for variant_id in ("bunny_f", "fox_f", "cat_f"):
            cfg = get_party_animal(variant_id)
            draw_party_animal_shape(
                surface,
                player=player,
                config=cfg,
                show_outline=True,
                show_shadow=True,
            )
        self.assertIsInstance(surface, pygame.Surface)


if __name__ == "__main__":
    unittest.main()
