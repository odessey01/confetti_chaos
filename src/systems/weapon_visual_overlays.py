"""Reusable player-attached weapon visual overlay definitions.

This module intentionally stays generic so future melee, aura, orbiting, or
companion-style weapon visuals can share the same attachment model as Bottle
Rocket.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class WeaponVisualOverlayOwner(str, Enum):
    """Declares which runtime system should own overlay instances.

    We standardize on a dedicated visual manager as the default owner. That
    keeps presentation state out of the player entity and equipped weapon data
    while still letting gameplay systems request overlay changes.
    """

    PLAYER = "player"
    EQUIPPED_WEAPON = "equipped_weapon"
    VISUAL_MANAGER = "visual_manager"


DEFAULT_WEAPON_VISUAL_OVERLAY_OWNER = WeaponVisualOverlayOwner.VISUAL_MANAGER


@dataclass(frozen=True, slots=True)
class WeaponVisualOverlay:
    """A generic visual attached to a named player anchor.

    The data model is presentation-focused on purpose: it describes where and
    how to draw a weapon visual without affecting hitboxes, damage, or other
    gameplay behavior.
    """

    overlay_id: str
    sprite_path: str
    anchor_name: str
    offset_x: float = 0.0
    offset_y: float = 0.0
    rotation_degrees: float = 0.0
    scale: float = 1.0
    z_index: int = 0
    visible: bool = True
    flip_x: bool = False
    flip_y: bool = False

    def with_visibility(self, visible: bool) -> WeaponVisualOverlay:
        """Return a copy with updated visibility for lightweight state toggles."""

        return replace(self, visible=bool(visible))

    def with_transform(
        self,
        *,
        offset_x: float | None = None,
        offset_y: float | None = None,
        rotation_degrees: float | None = None,
        scale: float | None = None,
        z_index: int | None = None,
    ) -> WeaponVisualOverlay:
        """Return a copy with updated presentation-only transform fields."""

        return replace(
            self,
            offset_x=self.offset_x if offset_x is None else float(offset_x),
            offset_y=self.offset_y if offset_y is None else float(offset_y),
            rotation_degrees=(
                self.rotation_degrees
                if rotation_degrees is None
                else float(rotation_degrees)
            ),
            scale=self.scale if scale is None else max(0.0, float(scale)),
            z_index=self.z_index if z_index is None else int(z_index),
        )
