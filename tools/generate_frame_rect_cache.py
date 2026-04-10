"""Generate animation frame-rect cache JSON files from bbox guide sheets.

Usage:
  python tools/generate_frame_rect_cache.py
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pygame


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.player_animation import _detect_bbox_rects, _safe_load_sheet  # noqa: E402


def _build_payload(sheet_path: str, guide_path: str) -> dict[str, object]:
    guide = _safe_load_sheet(guide_path)
    if guide is None:
        raise RuntimeError(f"Unable to load guide sheet: {guide_path}")
    rects = _detect_bbox_rects(guide)
    if len(rects) == 0:
        raise RuntimeError(f"No bbox rects detected in: {guide_path}")
    return {
        "version": 1,
        "sheet_path": sheet_path,
        "content_inset": 1,
        "frame_rects": [
            {"x": int(rect.x), "y": int(rect.y), "w": int(rect.width), "h": int(rect.height)}
            for rect in rects
        ],
    }


def _write_cache(relative_output: str, payload: dict[str, object]) -> None:
    output = ROOT / "assets" / Path(relative_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


def main() -> int:
    pygame.init()
    try:
        entries = (
            (
                "images/player/bear/bbox_bear_walking.png",
                "images/player/bear/bbox_bear_walking.png",
                "images/player/bear/bbox_bear_walking.frames.json",
            ),
            (
                "images/player/bear/bbox_bear_idle.png",
                "images/player/bear/bbox_bear_idle.png",
                "images/player/bear/bbox_bear_idle.frames.json",
            ),
        )
        for sheet_path, guide_path, output_path in entries:
            payload = _build_payload(sheet_path, guide_path)
            _write_cache(output_path, payload)
        return 0
    finally:
        pygame.quit()


if __name__ == "__main__":
    raise SystemExit(main())
