"""Runtime-safe path helpers for local and packaged execution."""

from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def runtime_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return project_root()


def assets_dir() -> Path:
    return runtime_root() / "assets"


def saves_dir() -> Path:
    if getattr(sys, "frozen", False):
        base = Path.home() / "confetti-chaos"
    else:
        base = project_root()
    directory = base / "saves"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def asset_path(*parts: str) -> Path:
    return assets_dir().joinpath(*parts)
