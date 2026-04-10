"""Validation tests for the main-game player animation system foundation."""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.game_session import GameSession  # noqa: E402
from systems.input_controller import InputMethod  # noqa: E402
from systems.player_animation import (  # noqa: E402
    CHARACTER_ANIMATION_CONFIGS,
    AnimationClipConfig,
    CharacterAnimationConfig,
    LoadedAnimationClip,
    LoadedCharacterAnimation,
    PlayerAnimationSystem,
    _load_frame_rect_cache,
    get_character_animation_config,
    list_character_animation_configs,
    load_character_animation,
    register_character_animation_config,
)


def _stub_loader(config: CharacterAnimationConfig) -> LoadedCharacterAnimation:
    frame = pygame.Surface((16, 16), pygame.SRCALPHA)
    return LoadedCharacterAnimation(
        character_id=config.character_id,
        idle=LoadedAnimationClip(frames=(frame, frame.copy()), fps=4.0, available=True),
        walk=LoadedAnimationClip(frames=(frame, frame.copy(), frame.copy()), fps=6.0, available=True),
        base_display_scale=config.base_display_scale,
        anchor_offset=config.anchor_offset,
        hitbox_radius=config.hitbox_radius,
        hitbox_vertical_offset=config.hitbox_vertical_offset,
        flip_left=config.flip_left,
    )


def _stub_loader_with_mixed_sizes(config: CharacterAnimationConfig) -> LoadedCharacterAnimation:
    idle_frame = pygame.Surface((20, 22), pygame.SRCALPHA)
    walk_frame = pygame.Surface((32, 30), pygame.SRCALPHA)
    return LoadedCharacterAnimation(
        character_id=config.character_id,
        idle=LoadedAnimationClip(frames=(idle_frame,), fps=4.0, available=True),
        walk=LoadedAnimationClip(frames=(walk_frame,), fps=6.0, available=True),
        base_display_scale=1.0,
        anchor_offset=(0, 0),
        hitbox_radius=config.hitbox_radius,
        hitbox_vertical_offset=config.hitbox_vertical_offset,
        flip_left=config.flip_left,
    )


def _fps_driven_loader(config: CharacterAnimationConfig) -> LoadedCharacterAnimation:
    frame = pygame.Surface((16, 16), pygame.SRCALPHA)
    frames = tuple(frame.copy() for _ in range(6))
    return LoadedCharacterAnimation(
        character_id=config.character_id,
        idle=LoadedAnimationClip(frames=frames, fps=float(config.idle.fps), available=True),
        walk=LoadedAnimationClip(frames=frames, fps=float(config.walk.fps), available=True),
        base_display_scale=config.base_display_scale,
        anchor_offset=config.anchor_offset,
        hitbox_radius=config.hitbox_radius,
        hitbox_vertical_offset=config.hitbox_vertical_offset,
        flip_left=config.flip_left,
    )


class PlayerAnimationSystemValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        clip = AnimationClipConfig(sheet_path="images/player/bear/bear_idle.png", rows=1, columns=1, fps=4.0)
        self.configs = {
            "teddy_f": CharacterAnimationConfig(
                character_id="teddy_f",
                idle=clip,
                walk=clip,
            )
        }

    def test_animation_system_advances_frames_for_active_state(self) -> None:
        system = PlayerAnimationSystem(configs=self.configs, loader=_stub_loader)
        system.set_character("teddy_f")
        system.update(0.30, moving=True, facing=pygame.Vector2(1.0, 0.0))
        snap = system.snapshot()
        self.assertEqual(snap["state"], "walk")
        self.assertGreaterEqual(int(snap["frame_index"]), 1)

    def test_animation_system_switches_between_idle_and_walk(self) -> None:
        system = PlayerAnimationSystem(configs=self.configs, loader=_stub_loader)
        system.set_character("teddy_f")
        system.update(0.1, moving=True, facing=pygame.Vector2(1.0, 0.0))
        self.assertEqual(system.snapshot()["state"], "walk")
        system.update(0.1, moving=False, facing=pygame.Vector2(1.0, 0.0))
        self.assertEqual(system.snapshot()["state"], "idle")

    def test_game_session_updates_animation_system_separately_from_player_logic(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.update_playing(0.2, pygame.Vector2(1.0, 0.0), attack=False)
        snapshot = session.player_animation.snapshot()
        self.assertEqual(snapshot["state"], "walk")

    def test_game_session_keeps_idle_for_tiny_movement_input(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        tiny = session.ANIMATION_MOVE_INPUT_DEADZONE * 0.25
        session.update_playing(0.2, pygame.Vector2(tiny, 0.0), attack=False)
        snapshot = session.player_animation.snapshot()
        self.assertEqual(snapshot["state"], "idle")

    def test_main_game_bear_idle_and_walk_assets_load(self) -> None:
        config = CHARACTER_ANIMATION_CONFIGS["teddy_f"]
        loaded = load_character_animation(config)
        self.assertTrue(loaded.idle.available)
        self.assertTrue(loaded.walk.available)
        self.assertGreater(len(loaded.idle.frames), 0)
        self.assertGreater(len(loaded.walk.frames), 0)

    def test_main_game_bear_idle_and_walk_can_use_different_frame_counts(self) -> None:
        config = CHARACTER_ANIMATION_CONFIGS["teddy_f"]
        loaded = load_character_animation(config)
        self.assertTrue(loaded.idle.available)
        self.assertTrue(loaded.walk.available)
        self.assertNotEqual(len(loaded.idle.frames), len(loaded.walk.frames))

    def test_main_game_bear_cache_paths_load_frame_rects(self) -> None:
        walk_clip = CHARACTER_ANIMATION_CONFIGS["teddy_f"].walk
        assert walk_clip.frame_rects_path is not None
        loaded_cache = _load_frame_rect_cache(
            walk_clip.frame_rects_path,
            expected_sheet_path=walk_clip.sheet_path,
        )
        assert loaded_cache is not None
        rects, inset = loaded_cache
        self.assertGreater(len(rects), 0)
        self.assertGreaterEqual(inset, 0)

    def test_load_character_animation_uses_frame_rect_cache_when_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = pathlib.Path(tmpdir) / "cache.json"
            payload = {
                "version": 1,
                "sheet_path": "images/player/bear/bbox_bear_idle.png",
                "content_inset": 0,
                "frame_rects": [{"x": 0, "y": 0, "w": 12, "h": 16}],
            }
            cache_path.write_text(json.dumps(payload), encoding="utf-8")
            config = CharacterAnimationConfig(
                character_id="cached_test",
                idle=AnimationClipConfig(
                    sheet_path="images/player/bear/bbox_bear_idle.png",
                    rows=1,
                    columns=1,
                    fps=5.0,
                    extraction_mode="bbox_guide",
                    bbox_guide_path="images/player/bear/does_not_exist.png",
                    frame_rects_path=str(cache_path),
                ),
                walk=AnimationClipConfig(
                    sheet_path="images/player/bear/bbox_bear_idle.png",
                    rows=1,
                    columns=1,
                    fps=5.0,
                    extraction_mode="bbox_guide",
                    bbox_guide_path="images/player/bear/does_not_exist.png",
                    frame_rects_path=str(cache_path),
                ),
            )
            loaded = load_character_animation(config)
            self.assertTrue(loaded.idle.available)
            self.assertEqual(len(loaded.idle.frames), 1)
            self.assertEqual(loaded.idle.frames[0].get_size(), (12, 16))

    def test_invalid_frame_rect_cache_falls_back_to_bbox_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = pathlib.Path(tmpdir) / "bad_cache.json"
            cache_path.write_text("{invalid-json", encoding="utf-8")
            config = CharacterAnimationConfig(
                character_id="cache_fallback",
                idle=AnimationClipConfig(
                    sheet_path="images/player/bear/bbox_bear_walking.png",
                    rows=5,
                    columns=4,
                    fps=8.0,
                    extraction_mode="bbox_guide",
                    bbox_guide_path="images/player/bear/bbox_bear_walking.png",
                    frame_rects_path=str(cache_path),
                ),
                walk=AnimationClipConfig(
                    sheet_path="images/player/bear/bbox_bear_walking.png",
                    rows=5,
                    columns=4,
                    fps=8.0,
                    extraction_mode="bbox_guide",
                    bbox_guide_path="images/player/bear/bbox_bear_walking.png",
                    frame_rects_path=str(cache_path),
                ),
            )
            loaded = load_character_animation(config)
            self.assertTrue(loaded.idle.available)
            self.assertGreater(len(loaded.idle.frames), 1)

    def test_main_game_bear_bbox_frames_do_not_include_red_guides(self) -> None:
        config = CHARACTER_ANIMATION_CONFIGS["teddy_f"]
        loaded = load_character_animation(config)
        self.assertTrue(loaded.walk.available)
        frame = loaded.walk.frames[0]
        pixels = pygame.surfarray.pixels3d(frame)
        alpha = pygame.surfarray.pixels_alpha(frame)
        red_guide_pixels = 0
        width, height = frame.get_size()
        for x in range(width):
            for y in range(height):
                if alpha[x, y] <= 0:
                    continue
                r, g, b = pixels[x, y]
                if r >= 240 and g <= 40 and b <= 40:
                    red_guide_pixels += 1
        del pixels
        del alpha
        self.assertEqual(red_guide_pixels, 0)

    def test_missing_animation_assets_fail_gracefully(self) -> None:
        broken = CharacterAnimationConfig(
            character_id="broken",
            idle=AnimationClipConfig(sheet_path="images/player/bear/does_not_exist_idle.png", rows=4, columns=4, fps=5.0),
            walk=AnimationClipConfig(sheet_path="images/player/bear/does_not_exist_walk.png", rows=4, columns=4, fps=8.0),
        )
        loaded = load_character_animation(broken)
        self.assertFalse(loaded.idle.available)
        self.assertFalse(loaded.walk.available)

    def test_snapshot_exposes_idle_and_walk_availability(self) -> None:
        system = PlayerAnimationSystem(configs=self.configs, loader=_stub_loader)
        system.set_character("teddy_f")
        snap = system.snapshot()
        self.assertTrue(bool(snap["idle_clip_available"]))
        self.assertTrue(bool(snap["walk_clip_available"]))

    def test_frame_rect_for_player_keeps_center_bottom_anchor_across_states(self) -> None:
        system = PlayerAnimationSystem(configs=self.configs, loader=_stub_loader_with_mixed_sizes)
        system.set_character("teddy_f")
        player_rect = pygame.Rect(100, 120, 80, 80)

        system.update(0.0, moving=False, facing=pygame.Vector2(1.0, 0.0))
        idle_rect = system.frame_rect_for_player(player_rect)
        assert idle_rect is not None

        system.update(0.1, moving=True, facing=pygame.Vector2(1.0, 0.0))
        walk_rect = system.frame_rect_for_player(player_rect)
        assert walk_rect is not None

        self.assertEqual(idle_rect.midbottom, walk_rect.midbottom)

    def test_gameplay_hitbox_remains_stable_while_animation_state_changes(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(250.0, 240.0)
        idle_hitbox = session.player_collision_rect()

        session.update_playing(0.2, pygame.Vector2(1.0, 0.0), attack=False)
        walk_hitbox = session.player_collision_rect()

        session.update_playing(0.2, pygame.Vector2(0.0, 0.0), attack=False)
        post_walk_hitbox = session.player_collision_rect()

        self.assertEqual(idle_hitbox.size, walk_hitbox.size)
        self.assertEqual(walk_hitbox.size, post_walk_hitbox.size)

    def test_directional_flip_metadata_tracks_left_and_right_facing(self) -> None:
        system = PlayerAnimationSystem(configs=self.configs, loader=_stub_loader)
        system.set_character("teddy_f")

        system.update(0.1, moving=True, facing=pygame.Vector2(1.0, 0.0))
        self.assertTrue(system.should_flip_horizontal())

        system.update(0.1, moving=True, facing=pygame.Vector2(-1.0, 0.0))
        self.assertFalse(system.should_flip_horizontal())

    def test_idle_and_walk_use_separate_fps_tuning(self) -> None:
        tuned = {
            "teddy_f": CharacterAnimationConfig(
                character_id="teddy_f",
                idle=AnimationClipConfig(
                    sheet_path="images/player/bear/bear_idle.png",
                    rows=1,
                    columns=1,
                    fps=4.0,
                ),
                walk=AnimationClipConfig(
                    sheet_path="images/player/bear/bear_walking.png",
                    rows=1,
                    columns=1,
                    fps=12.0,
                ),
            )
        }
        system = PlayerAnimationSystem(configs=tuned, loader=_fps_driven_loader)
        system.set_character("teddy_f")

        system.update(0.4, moving=False, facing=pygame.Vector2(1.0, 0.0))
        idle_index = int(system.snapshot()["frame_index"])

        system.reset()
        system.update(0.4, moving=True, facing=pygame.Vector2(1.0, 0.0))
        walk_index = int(system.snapshot()["frame_index"])

        self.assertGreater(walk_index, idle_index)

    def test_animation_system_coexists_with_weapon_fire_and_projectiles(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.update_playing(0.2, pygame.Vector2(1.0, 0.0), attack=True)
        self.assertGreaterEqual(len(session.projectiles), 1)
        self.assertEqual(session.player_animation.snapshot()["state"], "walk")

    def test_animation_system_coexists_with_dodge_and_damage_rules(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=1)
        session.trigger_player_dodge(pygame.Vector2(1.0, 0.0))
        session.update_playing(0.05, pygame.Vector2(1.0, 0.0), attack=False)
        self.assertTrue(session.player.is_invulnerable)
        self.assertEqual(session.player_animation.snapshot()["state"], "walk")

    def test_animation_system_coexists_with_controller_aim_assist_launch(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_input_method(InputMethod.CONTROLLER)
        session.player.position.update(300.0, 300.0)
        hazard = pygame.Rect(460, 330, 64, 64)
        mock_hazard = type("HazardStub", (), {"rect": hazard})()
        session.hazards = [mock_hazard]  # type: ignore[assignment]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertGreaterEqual(len(session.projectiles), 1)
        self.assertEqual(session.player_animation.snapshot()["state"], "idle")

    def test_player_debug_overlay_renders_animation_debug_info_without_errors(self) -> None:
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.update_playing(0.2, pygame.Vector2(1.0, 0.0), attack=False)
        session.draw_player_debug_overlay(surface)
        self.assertIsInstance(surface, pygame.Surface)

    def test_character_animation_registry_supports_future_party_animals(self) -> None:
        base = CHARACTER_ANIMATION_CONFIGS["teddy_f"]
        future = CharacterAnimationConfig(
            character_id="raccoon_f",
            idle=base.idle,
            walk=base.walk,
            base_display_scale=base.base_display_scale,
            anchor_offset=base.anchor_offset,
            hitbox_radius=base.hitbox_radius,
            hitbox_vertical_offset=base.hitbox_vertical_offset,
            flip_left=base.flip_left,
        )
        register_character_animation_config(future)
        fetched = get_character_animation_config("raccoon_f")
        self.assertEqual(fetched.character_id, "raccoon_f")
        ids = {config.character_id for config in list_character_animation_configs()}
        self.assertIn("raccoon_f", ids)


if __name__ == "__main__":
    unittest.main()
