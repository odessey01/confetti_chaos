"""Runtime-adjustable settings for in-session controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuntimeSettings:
    audio_enabled: bool = True
    # Placeholder hook for future settings expansion.
    window_mode: str = "windowed"
