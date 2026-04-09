"""Backward-compatible projectile alias for the bottle rocket weapon."""

from __future__ import annotations

from .bottle_rocket import BottleRocket


class Projectile(BottleRocket):
    """Compatibility alias while systems migrate to bottle rocket naming."""
