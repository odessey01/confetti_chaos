"""Standalone teddy shape demo sandbox for player visual exploration."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from player import Player
from systems.player_demo_sprite import hitbox_from_anchor
from systems.teddy_shape_variants import (
    PLUSH_CAST_CANDIDATE_NOTES,
    SHARED_PLUSH_ACCESSORY_RULES,
    SOFTER_PLUSH_DELUXE_VARIANT_IDS,
    STYLIZED_TEDDY_VARIANT_IDS,
    TEDDY_FINALIST_NOTES,
    TEDDY_SHAPE_VARIANTS,
    draw_teddy_shape_variant,
)


WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
WINDOW_TITLE = "Confetti Chaos - Teddy Shape Demo"
TARGET_FPS = 60
BASE_PLAYER_SIZE = 112


@dataclass
class DemoState:
    variant_index: int = 0
    demo_scale: float = 1.0
    preview_mode: str = "idle"
    forced_direction: str | None = None
    show_outline: bool = True
    show_shadow: bool = True
    show_debug: bool = False
    elapsed: float = 0.0
    render_mode_label: str = "shape-teddy"
    sprite_offset_x: int = 0
    sprite_offset_y: int = 0
    hitbox_radius_adjust: float = 0.0
    hitbox_vertical_adjust: float = 0.0


def cycle_variant_index(current_index: int, direction: int, count: int) -> int:
    if count <= 0:
        return 0
    return (current_index + direction) % count


def clamp_scale(scale: float) -> float:
    return max(0.6, min(2.2, scale))


def draw_demo_background(surface: pygame.Surface) -> None:
    top = pygame.Color(18, 27, 40)
    bottom = pygame.Color(36, 58, 78)
    for y in range(surface.get_height()):
        t = y / max(1, surface.get_height() - 1)
        color = top.lerp(bottom, t)
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))
    floor = pygame.Rect(0, int(surface.get_height() * 0.66), surface.get_width(), int(surface.get_height() * 0.34))
    pygame.draw.rect(surface, (24, 42, 58), floor)


def current_variant(state: DemoState):
    return TEDDY_SHAPE_VARIANTS[state.variant_index]


def direction_to_facing(direction_name: str) -> pygame.Vector2:
    mapping = {
        "up": pygame.Vector2(0.0, -1.0),
        "down": pygame.Vector2(0.0, 1.0),
        "left": pygame.Vector2(-1.0, 0.0),
        "right": pygame.Vector2(1.0, 0.0),
    }
    return pygame.Vector2(mapping.get(direction_name, pygame.Vector2(1.0, 0.0)))


def apply_preview_pose(player: Player, state: DemoState, delta_seconds: float) -> None:
    state.elapsed += delta_seconds
    if state.forced_direction is not None:
        player.facing = direction_to_facing(state.forced_direction)
        player._movement_intensity = 0.85 if state.preview_mode == "move" else 0.15
        player._movement_juice = 0.7 if state.preview_mode == "move" else 0.0
        player._movement_phase += delta_seconds * (18.0 if state.preview_mode == "move" else 6.0)
        return

    if state.preview_mode == "idle":
        player.facing.update(1.0, 0.0)
        player._movement_intensity = 0.1
        player._movement_juice = max(0.0, player.movement_juice * 0.92)
        player._movement_phase += delta_seconds * 6.0
        return

    player.facing.update(math.cos(state.elapsed * 1.8), math.sin(state.elapsed * 1.8) * 0.35)
    if player.facing.length_squared() <= 0.0:
        player.facing.update(1.0, 0.0)
    else:
        player.facing = player.facing.normalize()
    player._movement_intensity = 0.95
    player._movement_juice = 0.75 + (0.2 * math.sin(state.elapsed * 3.2))
    player._movement_phase += delta_seconds * 18.0


def _facing_label(facing: pygame.Vector2) -> str:
    if abs(facing.x) > abs(facing.y):
        return "left" if facing.x < 0.0 else "right"
    return "up" if facing.y < 0.0 else "down"


def draw_overlay(surface: pygame.Surface, state: DemoState, player: Player, *, facing_label: str) -> None:
    variant = current_variant(state)
    is_stylized = variant.variant_id in STYLIZED_TEDDY_VARIANT_IDS
    is_plush_cast = variant.variant_id in SOFTER_PLUSH_DELUXE_VARIANT_IDS
    if is_plush_cast:
        candidate_note = PLUSH_CAST_CANDIDATE_NOTES.get(variant.variant_id, "Candidate note pending.")
    else:
        candidate_note = TEDDY_FINALIST_NOTES.get(variant.variant_id, "Not shortlisted yet.")

    family = "Softer Plush Deluxe Cast" if is_plush_cast else "Option A Stylization" if is_stylized else "Baseline Exploration"
    accessory_rule = SHARED_PLUSH_ACCESSORY_RULES["type"]

    font = pygame.font.Font(None, 28)
    small = pygame.font.Font(None, 22)
    lines = [
        f"Variant: {variant.name} ({variant.variant_id})",
        f"Animal: {variant.animal_type} | Family role: {variant.plush_family_role}",
        f"Family: {family}",
        f"Mode: {state.preview_mode} | Render: {state.render_mode_label} | Scale: {state.demo_scale:.2f}x",
        f"Facing: {facing_label} | Direction mode: {state.forced_direction or 'auto'}",
        f"Silhouette: {variant.silhouette_type}",
        f"Ear type: {variant.ear_type} | Accessory: {accessory_rule}",
        f"Readability focus: {variant.readability_focus}",
        f"Style notes: {variant.style_notes}",
        f"Candidate note: {candidate_note}",
        f"Tuning: offset=({state.sprite_offset_x},{state.sprite_offset_y}) hitbox_r={state.hitbox_radius_adjust:+.1f} hitbox_y={state.hitbox_vertical_adjust:+.1f}",
    ]
    controls = [
        "Controls:",
        "A/D: cycle options | 1-0: direct variant (first ten)",
        "Space: toggle idle/move",
        "Arrow keys: force direction | C: clear direction",
        "+/-: scale",
        "J/L: offset X | I/K: offset Y",
        ",/.: hitbox radius | N/M: hitbox Y offset",
        "O: outline | H: shadow | G: debug overlay | Esc: quit",
    ]

    y = 14
    for line in lines:
        text = font.render(line, True, (246, 250, 255))
        surface.blit(text, (14, y))
        y += 24

    y += 6
    for line in controls:
        text = small.render(line, True, (228, 240, 250))
        surface.blit(text, (14, y))
        y += 19

    indicator = pygame.Rect(0, 0, int(player.size * 0.36), int(player.size * 0.36))
    indicator.center = (player.rect.centerx, player.rect.centery + int(player.size * 1.1))
    pygame.draw.rect(surface, (238, 248, 255), indicator, border_radius=6)


def handle_demo_key(state: DemoState, event: pygame.event.Event, variant_count: int) -> bool:
    if event.key == pygame.K_ESCAPE:
        return False
    if event.key == pygame.K_a:
        state.variant_index = cycle_variant_index(state.variant_index, -1, variant_count)
    elif event.key == pygame.K_d:
        state.variant_index = cycle_variant_index(state.variant_index, 1, variant_count)
    elif event.key in (pygame.K_SPACE,):
        state.preview_mode = "move" if state.preview_mode == "idle" else "idle"
    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
        state.demo_scale = clamp_scale(state.demo_scale + 0.1)
    elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
        state.demo_scale = clamp_scale(state.demo_scale - 0.1)
    elif event.key == pygame.K_o:
        state.show_outline = not state.show_outline
    elif event.key == pygame.K_h:
        state.show_shadow = not state.show_shadow
    elif event.key == pygame.K_g:
        state.show_debug = not state.show_debug
    elif event.key == pygame.K_j:
        state.sprite_offset_x -= 1
    elif event.key == pygame.K_l:
        state.sprite_offset_x += 1
    elif event.key == pygame.K_i:
        state.sprite_offset_y -= 1
    elif event.key == pygame.K_k:
        state.sprite_offset_y += 1
    elif event.key == pygame.K_COMMA:
        state.hitbox_radius_adjust = max(-14.0, state.hitbox_radius_adjust - 1.0)
    elif event.key == pygame.K_PERIOD:
        state.hitbox_radius_adjust = min(22.0, state.hitbox_radius_adjust + 1.0)
    elif event.key == pygame.K_n:
        state.hitbox_vertical_adjust = max(-24.0, state.hitbox_vertical_adjust - 1.0)
    elif event.key == pygame.K_m:
        state.hitbox_vertical_adjust = min(24.0, state.hitbox_vertical_adjust + 1.0)
    elif event.key == pygame.K_UP:
        state.forced_direction = "up"
    elif event.key == pygame.K_DOWN:
        state.forced_direction = "down"
    elif event.key == pygame.K_LEFT:
        state.forced_direction = "left"
    elif event.key == pygame.K_RIGHT:
        state.forced_direction = "right"
    elif event.key == pygame.K_c:
        state.forced_direction = None
    elif event.key in (
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6,
        pygame.K_7,
        pygame.K_8,
        pygame.K_9,
        pygame.K_0,
    ):
        if event.key == pygame.K_0:
            slot = 9
        else:
            slot = event.key - pygame.K_1
        if 0 <= slot < variant_count:
            state.variant_index = slot
    return True


def main() -> int:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    player = Player(
        (WINDOW_WIDTH - BASE_PLAYER_SIZE) / 2,
        (WINDOW_HEIGHT - BASE_PLAYER_SIZE) / 2,
        size=BASE_PLAYER_SIZE,
    )
    state = DemoState()
    running = True

    while running:
        delta_seconds = clock.tick(TARGET_FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = handle_demo_key(state, event, len(TEDDY_SHAPE_VARIANTS))
                if not running:
                    break

        variant = current_variant(state)
        player.visual_variant_id = variant.variant_id
        player.size = max(24, int(BASE_PLAYER_SIZE * state.demo_scale))
        player.position.update((WINDOW_WIDTH - player.size) / 2, (WINDOW_HEIGHT - player.size) / 2)
        apply_preview_pose(player, state, delta_seconds)

        draw_demo_background(screen)
        anchor = (player.rect.centerx, player.rect.bottom)
        draw_teddy_shape_variant(
            screen,
            player=player,
            variant=variant,
            anchor=anchor,
            offset=(state.sprite_offset_x, state.sprite_offset_y),
            show_outline=state.show_outline,
            show_shadow=state.show_shadow,
        )
        state.render_mode_label = "shape-teddy"

        if state.show_debug:
            pygame.draw.circle(screen, (255, 110, 140), anchor, 4)
            hitbox_center, hitbox_radius = hitbox_from_anchor(
                anchor=(anchor[0] + state.sprite_offset_x, anchor[1] + state.sprite_offset_y),
                radius=20.0 + state.hitbox_radius_adjust,
                vertical_offset=22.0 + state.hitbox_vertical_adjust,
            )
            pygame.draw.circle(
                screen,
                (120, 225, 255),
                (int(hitbox_center.x), int(hitbox_center.y)),
                int(hitbox_radius),
                width=2,
            )

        draw_overlay(screen, state, player, facing_label=_facing_label(player.facing))
        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
