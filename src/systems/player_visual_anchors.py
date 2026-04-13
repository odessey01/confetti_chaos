"""Named player-local anchors for weapon and accessory visuals."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from player import Player


@dataclass(frozen=True, slots=True)
class PlayerVisualAnchorDefinition:
    """Describe a named anchor relative to the player's render origin.

    Anchor offsets are authored from the center-bottom player render origin.
    If animation-specific offsets become necessary later, this definition is
    the intended place to extend them without changing overlay callers.
    """

    anchor_name: str
    offset_x: float
    offset_y: float
    flip_with_facing: bool = True


PLAYER_VISUAL_ANCHORS: dict[str, PlayerVisualAnchorDefinition] = {
    "weapon_mount": PlayerVisualAnchorDefinition(
        anchor_name="weapon_mount",
        offset_x=18.0,
        offset_y=-30.0,
        flip_with_facing=True,
    ),
    # Authored from the right-hand side and mirrored when the player faces left.
    "weapon_hand_right": PlayerVisualAnchorDefinition(
        anchor_name="weapon_hand_right",
        offset_x=18.0,
        offset_y=-30.0,
        flip_with_facing=True,
    ),
}


DEFAULT_PLAYER_WEAPON_ANCHOR = "weapon_mount"


def list_player_visual_anchors() -> tuple[PlayerVisualAnchorDefinition, ...]:
    return tuple(PLAYER_VISUAL_ANCHORS.values())


def get_player_visual_anchor(anchor_name: str) -> PlayerVisualAnchorDefinition:
    selected = PLAYER_VISUAL_ANCHORS.get(str(anchor_name))
    if selected is not None:
        return selected
    return PLAYER_VISUAL_ANCHORS[DEFAULT_PLAYER_WEAPON_ANCHOR]


def player_render_anchor(player: Player) -> tuple[int, int]:
    """Return the stable center-bottom origin used for player-local visuals."""

    return (player.rect.centerx, player.rect.bottom)


def resolve_player_visual_anchor(player: Player, anchor_name: str) -> tuple[int, int]:
    """Resolve a named anchor in world space using the player's facing direction."""

    definition = get_player_visual_anchor(anchor_name)
    base_x, base_y = player_render_anchor(player)
    facing = pygame.Vector2(getattr(player, "facing", pygame.Vector2(1.0, 0.0)))
    facing_sign = -1.0 if facing.x < -0.15 else 1.0
    offset_x = definition.offset_x * facing_sign if definition.flip_with_facing else definition.offset_x
    return (
        int(round(base_x + offset_x)),
        int(round(base_y + definition.offset_y)),
    )
