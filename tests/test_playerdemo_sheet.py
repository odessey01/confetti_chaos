"""Validation tests for player demo sprite sheet extraction."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from playerdemo import DemoState, cycle_row_index, extract_sprite_sheet_grid, update_row_animation  # noqa: E402
from playerdemo import anchored_frame_rect  # noqa: E402
from playerdemo import ANIMATED_PREVIEW_HITBOX_RADIUS, ANIMATED_PREVIEW_HITBOX_VERTICAL_OFFSET  # noqa: E402
from playerdemo import SPRITE_SHEET_CONFIGS, handle_demo_key  # noqa: E402
from systems import player_demo_animation  # noqa: E402
from systems.player_demo_sprite import BEAR_IDLE_ANIMATION_CONFIG, BEAR_WALKING_ANIMATION_CONFIG  # noqa: E402


class PlayerDemoSheetExtractionTests(unittest.TestCase):
    def test_extract_sprite_sheet_grid_returns_rows_and_columns(self) -> None:
        sheet = pygame.Surface((64, 48), pygame.SRCALPHA)
        frames = extract_sprite_sheet_grid(sheet, rows=3, columns=4)

        self.assertEqual(len(frames), 3)
        self.assertTrue(all(len(row) == 4 for row in frames))
        self.assertEqual(frames[0][0].get_width(), 16)
        self.assertEqual(frames[0][0].get_height(), 16)

    def test_cycle_row_index_wraps_within_bounds(self) -> None:
        self.assertEqual(cycle_row_index(0, -1, 4), 3)
        self.assertEqual(cycle_row_index(3, 1, 4), 0)

    def test_update_row_animation_advances_frame_with_time(self) -> None:
        state = DemoState()
        state.frame_sequence = [pygame.Surface((8, 8), pygame.SRCALPHA) for _ in range(4)]
        state.animation_fps = 10.0
        state.animation_playing = True
        state.animation_frame_index = 0

        update_row_animation(state, 0.11)

        self.assertEqual(state.animation_frame_index, 1)

    def test_update_row_animation_respects_pause(self) -> None:
        state = DemoState()
        state.frame_sequence = [pygame.Surface((8, 8), pygame.SRCALPHA) for _ in range(4)]
        state.animation_fps = 10.0
        state.animation_playing = False
        state.animation_frame_index = 2

        update_row_animation(state, 0.5)

        self.assertEqual(state.animation_frame_index, 2)

    def test_anchored_frame_rect_uses_center_bottom_anchor(self) -> None:
        rect = anchored_frame_rect((20, 10), anchor=(100, 80), scale=2.0)
        self.assertEqual(rect.width, 40)
        self.assertEqual(rect.height, 20)
        self.assertEqual(rect.midbottom, (100, 80))

    def test_demo_state_uses_fixed_animation_hitbox_defaults(self) -> None:
        state = DemoState()
        self.assertEqual(state.animation_hitbox_radius, ANIMATED_PREVIEW_HITBOX_RADIUS)
        self.assertEqual(state.animation_hitbox_vertical_offset, ANIMATED_PREVIEW_HITBOX_VERTICAL_OFFSET)

    def test_handle_demo_key_toggles_debug_overlay(self) -> None:
        state = DemoState()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_g})
        keep_running = handle_demo_key(state, event, variant_count=1)
        self.assertTrue(keep_running)
        self.assertTrue(state.show_debug)

    def test_handle_demo_key_updates_animation_preview_tuning_controls(self) -> None:
        state = DemoState()
        scale_before = state.animation_preview_scale
        radius_before = state.animation_hitbox_radius

        handle_demo_key(state, pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_x}), variant_count=1)
        handle_demo_key(state, pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_PERIOD}), variant_count=1)

        self.assertGreater(state.animation_preview_scale, scale_before)
        self.assertGreater(state.animation_hitbox_radius, radius_before)

    def test_bear_walking_animation_config_contains_reusable_fields(self) -> None:
        config = BEAR_WALKING_ANIMATION_CONFIG
        self.assertTrue(config.sprite_sheet_path.endswith(".png"))
        self.assertGreaterEqual(config.rows, 1)
        self.assertGreaterEqual(config.columns, 1)
        self.assertEqual(config.loop_mode, "full_sheet_loop")
        self.assertEqual(config.frame_order, "row_major")

    def test_bear_idle_animation_config_contains_reusable_fields(self) -> None:
        config = BEAR_IDLE_ANIMATION_CONFIG
        self.assertTrue(config.sprite_sheet_path.endswith("bbox_bear_idle.png"))
        self.assertGreaterEqual(config.rows, 1)
        self.assertGreaterEqual(config.columns, 1)
        self.assertEqual(config.loop_mode, "full_sheet_loop")
        self.assertEqual(config.frame_order, "row_major")

    def test_animation_runtime_helper_advances_frames(self) -> None:
        next_index, next_timer = player_demo_animation.advance_animation_loop(
            frame_index=0,
            timer=0.0,
            delta_seconds=0.26,
            fps=8.0,
            frame_count=4,
        )
        self.assertEqual(next_index, 2)
        self.assertGreaterEqual(next_timer, 0.0)

    def test_handle_demo_key_toggles_animation_idle_walk_mode(self) -> None:
        state = DemoState()
        self.assertEqual(state.animation_preview_mode, "loop")
        handle_demo_key(state, pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_TAB}), variant_count=1)
        self.assertEqual(state.animation_preview_mode, "pose")

    def test_update_row_animation_keeps_idle_on_stable_frame(self) -> None:
        state = DemoState()
        state.frame_sequence = [pygame.Surface((8, 8), pygame.SRCALPHA) for _ in range(4)]
        state.animation_preview_mode = "pose"
        state.animation_frame_index = 3

        update_row_animation(state, 0.5)

        self.assertEqual(state.animation_frame_index, 0)

    def test_flatten_frames_row_major_creates_loop_sequence(self) -> None:
        frames_by_row = [
            [pygame.Surface((4, 4), pygame.SRCALPHA), pygame.Surface((4, 4), pygame.SRCALPHA)],
            [pygame.Surface((4, 4), pygame.SRCALPHA), pygame.Surface((4, 4), pygame.SRCALPHA)],
        ]
        flattened = player_demo_animation.flatten_frames_row_major(frames_by_row)
        self.assertEqual(len(flattened), 4)

    def test_playerdemo_exposes_multiple_sprite_sheet_configs(self) -> None:
        self.assertGreaterEqual(len(SPRITE_SHEET_CONFIGS), 2)
        paths = {config.sprite_sheet_path for config in SPRITE_SHEET_CONFIGS}
        self.assertIn(BEAR_WALKING_ANIMATION_CONFIG.sprite_sheet_path, paths)
        self.assertIn(BEAR_IDLE_ANIMATION_CONFIG.sprite_sheet_path, paths)

    def test_handle_demo_key_can_switch_to_next_sprite_config(self) -> None:
        state = DemoState()
        handle_demo_key(state, pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d}), variant_count=2)
        self.assertEqual(state.config_index, 1)

    def test_bbox_animation_sources_can_have_different_frame_counts(self) -> None:
        if not pygame.get_init():
            pygame.init()
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((1, 1))
        walking_sheet = player_demo_animation.load_sprite_sheet_with_alpha(
            "images",
            "player",
            "bear",
            "bbox_bear_walking.png",
        ).surface
        idle_sheet = player_demo_animation.load_sprite_sheet_with_alpha(
            "images",
            "player",
            "bear",
            "bbox_bear_idle.png",
        ).surface
        assert walking_sheet is not None
        assert idle_sheet is not None

        walking_frames = player_demo_animation.extract_frames_from_bbox_guide(walking_sheet, walking_sheet)
        idle_frames = player_demo_animation.extract_frames_from_bbox_guide(idle_sheet, idle_sheet)

        self.assertGreater(len(walking_frames), 0)
        self.assertGreater(len(idle_frames), 0)
        self.assertNotEqual(len(walking_frames), len(idle_frames))


if __name__ == "__main__":
    unittest.main()
