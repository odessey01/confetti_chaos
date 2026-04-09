"""Validation tests for aim assist behavior and integration."""

from __future__ import annotations

import pathlib
import sys
import unittest

import pygame


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enemies import BalloonEnemy  # noqa: E402
from player import BottleRocket  # noqa: E402
from systems.aim_assist import AimAssistConfig, AimAssistSystem  # noqa: E402
from systems.game_session import GameSession  # noqa: E402
from systems.input_controller import InputController, InputMethod  # noqa: E402


class AimAssistValidationTests(unittest.TestCase):
    def test_cone_selection_ignores_targets_behind_player(self) -> None:
        system = AimAssistSystem(AimAssistConfig(enabled=True, cone_degrees=22.0, max_distance=500.0))
        origin = pygame.Vector2(0.0, 0.0)
        aim = pygame.Vector2(1.0, 0.0)
        target = system.select_target(
            origin=origin,
            aim_direction=aim,
            target_centers=[pygame.Vector2(-100.0, 0.0)],
        )
        self.assertIsNone(target)

    def test_target_selection_prefers_closest_in_cone(self) -> None:
        system = AimAssistSystem(AimAssistConfig(enabled=True, cone_degrees=30.0, max_distance=500.0))
        origin = pygame.Vector2(0.0, 0.0)
        aim = pygame.Vector2(1.0, 0.0)
        target = system.select_target(
            origin=origin,
            aim_direction=aim,
            target_centers=[pygame.Vector2(200.0, 10.0), pygame.Vector2(120.0, 9.0)],
        )
        self.assertIsNotNone(target)
        assert target is not None
        self.assertLess(target.distance, 150.0)

    def test_adjusted_direction_applies_subtle_nudge(self) -> None:
        system = AimAssistSystem(AimAssistConfig(enabled=True, cone_degrees=25.0, max_distance=500.0, assist_strength=0.3))
        origin = pygame.Vector2(0.0, 0.0)
        aim = pygame.Vector2(1.0, 0.0)
        adjusted = system.adjusted_direction(
            origin=origin,
            aim_direction=aim,
            target_centers=[pygame.Vector2(250.0, 60.0)],
        )
        self.assertGreater(adjusted.y, 0.0)
        self.assertGreater(adjusted.x, 0.7)

    def test_input_method_switches_between_keyboard_and_controller(self) -> None:
        controller = InputController()
        keyboard_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
        controller.handle_event(keyboard_event)
        self.assertEqual(controller.active_input_method(), InputMethod.KEYBOARD_MOUSE)

        joystick_event = pygame.event.Event(pygame.JOYBUTTONDOWN, {"button": 0})
        controller.handle_event(joystick_event)
        self.assertEqual(controller.active_input_method(), InputMethod.CONTROLLER)

    def test_game_session_aim_assist_enabled_for_controller_only(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(200.0, 200.0)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(460.0, 260.0)
        hazard.velocity.update(0.0, 0.0)
        session.hazards = [hazard]

        session.set_active_input_method(InputMethod.KEYBOARD_MOUSE)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        keyboard_direction = pygame.Vector2(session.projectiles[-1].direction)

        session.projectiles.clear()
        session._weapon_cooldown_timer = 0.0
        session.set_active_input_method(InputMethod.CONTROLLER)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        controller_direction = pygame.Vector2(session.projectiles[-1].direction)

        self.assertAlmostEqual(keyboard_direction.y, 0.0, places=4)
        self.assertGreater(controller_direction.y, keyboard_direction.y)

    def test_aim_assist_debug_overlay_draws_after_firing(self) -> None:
        if not pygame.get_init():
            pygame.init()
        surface = pygame.Surface((1280, 720))
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.set_active_input_method(InputMethod.CONTROLLER)
        session.set_aim_assist_user_enabled(True)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(460.0, 260.0)
        session.hazards = [hazard]
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        session.draw_aim_assist_debug_overlay(surface)
        self.assertIsInstance(surface, pygame.Surface)

    def test_controller_aim_assist_launches_bottle_rocket_toward_close_target(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(300.0, 300.0)
        session.set_active_input_method(InputMethod.CONTROLLER)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(470.0, 340.0)
        session.hazards = [hazard]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        self.assertEqual(len(session.projectiles), 1)
        rocket = session.projectiles[-1]
        self.assertIsInstance(rocket, BottleRocket)
        self.assertGreater(rocket.direction.y, 0.0)

    def test_controller_aim_assist_tracks_target_motion_between_shots(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(300.0, 300.0)
        session.set_active_input_method(InputMethod.CONTROLLER)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(500.0, 240.0)
        session.hazards = [hazard]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        first_direction = pygame.Vector2(session.projectiles[-1].direction)

        session.projectiles.clear()
        session._weapon_cooldown_timer = 0.0
        hazard.position.update(500.0, 310.0)
        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        second_direction = pygame.Vector2(session.projectiles[-1].direction)

        self.assertLess(first_direction.y, 0.0)
        self.assertGreater(second_direction.y, 0.0)

    def test_controller_aim_assist_prefers_closer_target_when_multiple_in_cone(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(300.0, 300.0)
        session.set_active_input_method(InputMethod.CONTROLLER)

        close_target = BalloonEnemy(speed=0.0)
        close_target.position.update(430.0, 350.0)
        far_target = BalloonEnemy(speed=0.0)
        far_target.position.update(560.0, 220.0)
        session.hazards = [far_target, close_target]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        rocket_direction = pygame.Vector2(session.projectiles[-1].direction)

        self.assertGreater(rocket_direction.y, 0.0)

    def test_aim_assist_applies_at_launch_only_with_decaying_rockets(self) -> None:
        session = GameSession(pygame.Rect(0, 0, 1280, 720), hazard_count=0)
        session.player.position.update(300.0, 300.0)
        session.set_active_input_method(InputMethod.CONTROLLER)
        hazard = BalloonEnemy(speed=0.0)
        hazard.position.update(500.0, 340.0)
        session.hazards = [hazard]

        session.fire_projectile(pygame.Vector2(1.0, 0.0))
        rocket = session.projectiles[-1]
        launch_direction = pygame.Vector2(rocket.direction)
        launch_direction.normalize_ip()

        # Move target far away to ensure no mid-flight retargeting occurs.
        hazard.position.update(520.0, 220.0)
        for _ in range(45):
            rocket.update(1.0 / 60.0)

        locked_launch_direction = pygame.Vector2(rocket._launch_direction)
        locked_launch_direction.normalize_ip()
        self.assertGreater(launch_direction.dot(locked_launch_direction), 0.999)
        # Flight decay/wobble can move current heading, but that is separate from launch assist.
        self.assertNotAlmostEqual(rocket.direction.y, launch_direction.y, places=3)


if __name__ == "__main__":
    unittest.main()
