"""Unified keyboard/controller input handling."""

from __future__ import annotations

import pygame


class InputMethod:
    KEYBOARD_MOUSE = "keyboard_mouse"
    CONTROLLER = "controller"


class InputController:
    def __init__(self) -> None:
        self._deadzone = 0.2
        self._joystick: pygame.joystick.Joystick | None = None
        self._last_input_method = InputMethod.KEYBOARD_MOUSE
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        self._refresh_joystick()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self._last_input_method = InputMethod.KEYBOARD_MOUSE
        elif event.type in (
            pygame.JOYAXISMOTION,
            pygame.JOYBUTTONDOWN,
            pygame.JOYBUTTONUP,
            pygame.JOYHATMOTION,
        ):
            self._last_input_method = InputMethod.CONTROLLER
        if event.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
            self._refresh_joystick()

    def active_input_method(self) -> str:
        return self._last_input_method

    def movement_vector(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        keyboard_x = float(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - float(
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        keyboard_y = float(keys[pygame.K_s] or keys[pygame.K_DOWN]) - float(
            keys[pygame.K_w] or keys[pygame.K_UP]
        )
        movement = pygame.Vector2(keyboard_x, keyboard_y)

        joystick_vector = self._joystick_vector()
        if joystick_vector.length_squared() > movement.length_squared():
            movement = joystick_vector
        return movement

    def is_menu_confirm(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_SPACE, pygame.K_RETURN)
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (0, 7)
        )

    def is_menu_quit(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_q, pygame.K_ESCAPE)
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == 6
        )

    def is_menu_up(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_UP, pygame.K_w)
        ) or (
            event.type == pygame.JOYHATMOTION
            and event.value[1] > 0
        )

    def is_menu_down(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_DOWN, pygame.K_s)
        ) or (
            event.type == pygame.JOYHATMOTION
            and event.value[1] < 0
        )

    def is_menu_left(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_LEFT, pygame.K_a)
        ) or (
            event.type == pygame.JOYHATMOTION
            and event.value[0] < 0
        )

    def is_menu_right(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_RIGHT, pygame.K_d)
        ) or (
            event.type == pygame.JOYHATMOTION
            and event.value[0] > 0
        )

    def is_restart(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_r, pygame.K_SPACE)
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (0, 7)
        )

    def is_pause_toggle(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_p, pygame.K_ESCAPE)
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (7, 6)
        )

    def is_attack(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (0, 1)
        )

    def is_dodge(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT)
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (1, 2)
        )

    def is_super_activate(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_q, pygame.K_e)
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (3, 4)
        )

    def is_weapon_toggle(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_t
        ) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button in (4, 5)
        )

    def is_pause_menu_up(self, event: pygame.event.Event) -> bool:
        return self.is_menu_up(event)

    def is_pause_menu_down(self, event: pygame.event.Event) -> bool:
        return self.is_menu_down(event)

    def is_pause_menu_confirm(self, event: pygame.event.Event) -> bool:
        return self.is_menu_confirm(event)

    def _refresh_joystick(self) -> None:
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            self._joystick = joystick
        else:
            self._joystick = None

    def _joystick_vector(self) -> pygame.Vector2:
        if self._joystick is None:
            return pygame.Vector2(0, 0)

        x_axis = self._apply_deadzone(self._joystick.get_axis(0))
        y_axis = self._apply_deadzone(self._joystick.get_axis(1))
        hat_x, hat_y = self._joystick.get_hat(0) if self._joystick.get_numhats() > 0 else (0, 0)

        x = x_axis if abs(x_axis) >= abs(hat_x) else float(hat_x)
        y = y_axis if abs(y_axis) >= abs(hat_y) else float(-hat_y)
        vector = pygame.Vector2(x, y)
        if vector.length_squared() > 1.0:
            vector = vector.normalize()
        return vector

    def _apply_deadzone(self, value: float) -> float:
        return 0.0 if abs(value) < self._deadzone else float(value)
