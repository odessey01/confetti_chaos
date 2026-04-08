# Teddy Integration Path

## Goal
Move the selected teddy shape variant from `playerdemo.py` into main gameplay with minimal refactor.

## Reusable pieces
- Variant definitions and notes:
  - `src/systems/teddy_shape_variants.py`
- Reusable teddy shape renderer:
  - `draw_teddy_shape_variant(...)`
- Existing player state inputs already compatible:
  - `Player.facing`
  - `Player.movement_phase`
  - `Player.movement_intensity`
  - `Player.movement_juice`

## Integration steps
1. Add selected teddy variant id to main player config (or settings).
2. In `src/systems/player_visual.py`, call `draw_teddy_shape_variant(...)` when selected.
3. Reuse existing clarity toggles and bounds behavior from current player renderer.
4. Keep demo-only controls in `playerdemo.py` and do not import them into main loop.

## Notes
- Demo tuning controls (offset/hitbox/debug hotkeys) remain sandbox-only.
- The teddy shape renderer is intentionally input-agnostic and can be reused directly.
