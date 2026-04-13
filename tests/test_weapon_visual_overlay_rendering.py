"""Focused integration tests for the player-attached bottle rocket overlay."""

from __future__ import annotations

import pathlib
import sys
import unittest
import types

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.game_session import GameSession  # noqa: E402


class WeaponVisualOverlayRenderingTests(unittest.TestCase):
    def test_bottle_rocket_overlay_snapshot_uses_anchor_scale_and_layer(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)

        overlays = session.active_weapon_visual_overlay_snapshot()

        self.assertEqual(len(overlays), 1)
        overlay = overlays[0]
        self.assertEqual(overlay["weapon_id"], "bottle_rocket")
        self.assertEqual(overlay["overlay_id"], "bottle_rocket_tier1")
        self.assertEqual(overlay["variant_id"], "tier1")
        self.assertEqual(overlay["anchor_name"], "weapon_mount")
        self.assertEqual(overlay["anchor"], session.player_weapon_anchor())
        self.assertEqual(overlay["draw_position"], session.player_weapon_anchor())
        self.assertEqual(overlay["scale"], 0.75)
        self.assertEqual(overlay["rotation_degrees"], -12.0)
        self.assertEqual(overlay["z_index"], 1)
        self.assertTrue(overlay["visible"])
        self.assertFalse(overlay["flip_x"])
        self.assertFalse(overlay["flip_y"])

    def test_overlay_hides_when_bottle_rocket_is_not_equipped(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_weapon("sparkler")

        self.assertEqual(session.active_weapon_visual_overlay_snapshot(), ())
        self.assertEqual(session.active_weapon_visual_variant_id(), "tier1")
        self.assertEqual(session.weapon_visual_fallback_snapshot()["reason"], "missing_asset")

    def test_overlay_anchor_tracks_player_position_and_facing(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(250.0, 180.0)
        session.player.facing = pygame.Vector2(-1.0, 0.0)

        overlay = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertEqual(overlay["anchor"], session.player_weapon_anchor())
        self.assertLess(overlay["anchor"][0], session.player.rect.centerx)
        self.assertEqual(overlay["variant_id"], "tier1")
        self.assertEqual(overlay["rotation_degrees"], -168.0)
        self.assertEqual(overlay["z_index"], -1)
        self.assertFalse(overlay["flip_x"])
        self.assertTrue(overlay["flip_y"])

    def test_overlay_uses_stronger_forward_tilt_while_moving(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.update_playing(0.1, pygame.Vector2(1.0, 0.0), attack=False)

        overlay = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertEqual(overlay["rotation_degrees"], -22.0)

    def test_overlay_rotation_tracks_vertical_facing_direction(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.facing = pygame.Vector2(0.0, -1.0)

        overlay = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertEqual(overlay["rotation_degrees"], 78.0)

    def test_overlay_rotation_tracks_diagonal_facing_direction(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.facing = pygame.Vector2(-1.0, 1.0)

        overlay = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertAlmostEqual(float(overlay["rotation_degrees"]), -123.0, delta=0.01)

    def test_overlay_uses_tier2_after_first_evolution(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session._weapon_evolution_forms["bottle_rocket"] = "burst_rocket"  # noqa: SLF001
        session._weapon_evolution_behavior_ids["bottle_rocket"] = {"burst_rocket"}  # noqa: SLF001

        overlay = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertEqual(overlay["variant_id"], "tier2")

    def test_overlay_uses_tier3_for_merged_bottle_rocket_behaviors(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session._weapon_evolution_forms["bottle_rocket"] = "burst_rocket"  # noqa: SLF001
        session._weapon_evolution_behavior_ids["bottle_rocket"] = {  # noqa: SLF001
            "burst_rocket",
            "pinball_rocket",
        }

        overlay = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertEqual(overlay["variant_id"], "tier3")

    def test_overlay_idle_bob_changes_draw_position_over_time(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        start = session.active_weapon_visual_overlay_snapshot()[0]
        session.elapsed_time = 0.0625
        later = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertNotEqual(start["draw_position"], later["draw_position"])

    def test_draw_playing_renders_overlay_without_errors(self) -> None:
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)

        session.draw_playing(surface)

        self.assertIsInstance(surface, pygame.Surface)

    def test_overlay_debug_snapshot_exposes_bounds_anchor_and_variant(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_weapon_overlay_debug(True)

        snapshot = session.weapon_overlay_debug_snapshot()

        self.assertEqual(len(snapshot), 1)
        row = snapshot[0]
        self.assertEqual(row["weapon_id"], "bottle_rocket")
        self.assertEqual(row["variant_id"], "tier1")
        self.assertEqual(row["overlay_id"], "bottle_rocket_tier1")
        self.assertIsInstance(row["draw_rect"], pygame.Rect)
        self.assertIsInstance(row["anchor_point"], tuple)
        self.assertIsInstance(row["pivot_point"], tuple)

    def test_overlay_tuning_offsets_rotation_and_scale(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        base = session.active_weapon_visual_overlay_snapshot()[0]
        session.set_weapon_overlay_tuning(
            weapon_id="bottle_rocket",
            offset_x=9.0,
            offset_y=-7.0,
            scale=0.2,
            rotation_degrees=11.0,
        )
        tuned = session.active_weapon_visual_overlay_snapshot()[0]

        self.assertNotEqual(base["draw_position"], tuned["draw_position"])
        self.assertGreater(float(tuned["scale"]), float(base["scale"]))
        self.assertGreater(float(tuned["rotation_degrees"]), float(base["rotation_degrees"]))

    def test_reload_weapon_visual_config_is_safe_noop_for_runtime(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)

        session.reload_weapon_visual_config()

        overlays = session.active_weapon_visual_overlay_snapshot()
        self.assertEqual(len(overlays), 1)

    def test_fallback_handles_no_active_weapon(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.active_weapon_id = ""
        self.assertEqual(session.active_weapon_visual_overlay_snapshot(), ())
        self.assertEqual(session.active_weapon_visual_variant_id(), "none")
        self.assertEqual(session.weapon_visual_fallback_snapshot()["reason"], "no_active_weapon")

    def test_fallback_handles_unknown_weapon_visual(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.active_weapon_id = "unknown_weapon"
        self.assertEqual(session.active_weapon_visual_overlay_snapshot(), ())
        self.assertEqual(session.active_weapon_visual_variant_id(), "none")
        self.assertEqual(session.weapon_visual_fallback_snapshot()["reason"], "unknown_weapon_visual")

    def test_equipped_weapon_source_of_truth_defaults_to_active_weapon(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        self.assertEqual(session.equipped_weapon_ids_for_visuals(), ("bottle_rocket",))

    def test_overlay_active_path_hides_player_direction_arrow(self) -> None:
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        calls: list[int] = []

        session.player_renderer._draw_direction_indicator = types.MethodType(  # type: ignore[method-assign]  # noqa: SLF001
            lambda self, s, p: calls.append(1),
            session.player_renderer,
        )

        session.draw_playing(surface)

        self.assertEqual(len(calls), 0)


if __name__ == "__main__":
    unittest.main()
