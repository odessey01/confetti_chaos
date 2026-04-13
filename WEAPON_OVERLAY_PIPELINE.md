# Weapon Overlay Pipeline

This document explains how player-attached weapon overlays are wired in the runtime.

## 1) Where weapon overlay sprites live

- Overlay sprite assets live under `assets/images/weapons/...`.
- Current Bottle Rocket Tier 1 art is at:
  - `assets/images/weapons/bottle_rocket/tier1.png`

## 2) How weapon sprites are registered

- Asset registration is data-driven in:
  - `src/systems/weapon_visual_assets.py`
- Add a `WeaponVisualAssetDefinition` entry to `WEAPON_VISUAL_ASSETS`.
- Key fields:
  - `asset_id`: stable ID used by visual variants
  - `sprite_path`: path under `assets/`
  - `pivot`: intended mount pivot reference (for future fine alignment work)

## 3) How anchors work

- Named player-local anchors are defined in:
  - `src/systems/player_visual_anchors.py`
- Runtime anchor resolution supports facing-aware mirroring.
- Current default weapon anchor is `weapon_mount`.
- `GameSession.player_weapon_anchor()` resolves the world-space anchor position each frame.

## 4) How visual variants are selected

- Variant definitions and selection rules live in:
  - `src/systems/weapon_visuals.py`
- Runtime resolution flow:
  1. `GameSession.equipped_weapon_ids_for_visuals()` returns overlay-eligible weapons.
  2. `GameSession.weapon_visual_variant_id_for_weapon()` resolves the active variant by rules.
  3. `GameSession._resolve_overlay_for_weapon()` builds the final `WeaponVisualOverlay`.
  4. `GameSession.draw_playing()` renders overlays behind/in front of player by `z_index`.
- Missing or unknown visuals fail gracefully:
  - no active weapon -> `no_active_weapon`
  - unknown visual config -> `unknown_weapon_visual`
  - missing registered asset -> `missing_asset`
  - inspect with `GameSession.weapon_visual_fallback_snapshot()`

## 5) Bottle Rocket naming conventions

- Variant key format: `<weapon_id>:<tier_id>`
  - Examples:
    - `bottle_rocket:tier1`
    - `bottle_rocket:tier2`
    - `bottle_rocket:tier3`
- Asset IDs follow the same readable style:
  - `bottle_rocket_tier1`
- Rule tables should list higher tiers first when using min-threshold matching.

## 6) How future weapons plug in

1. Add weapon art in `assets/images/weapons/<weapon_name>/...`.
2. Register assets in `WEAPON_VISUAL_ASSETS` (`weapon_visual_assets.py`).
3. Add one or more variant definitions in `WEAPON_VISUAL_VARIANTS` (`weapon_visuals.py`).
4. Add selection rules in `WEAPON_VISUAL_VARIANT_RULES`.
5. Ensure anchor choice and offsets are authored in player-local terms.
6. Add focused tests under `tests/test_weapon_visuals.py` and `tests/test_weapon_visual_overlay_rendering.py`.

## 7) Example: Register a new overlay variant

```python
# src/systems/weapon_visual_assets.py
WEAPON_VISUAL_ASSETS["sparkler_tier2"] = WeaponVisualAssetDefinition(
    asset_id="sparkler_tier2",
    sprite_path="images/weapons/sparkler/tier2.png",
    pivot=(16, 28),
)

# src/systems/weapon_visuals.py
WEAPON_VISUAL_VARIANTS["sparkler:tier2"] = WeaponVisualVariantDefinition(
    variant_id="tier2",
    weapon_id="sparkler",
    default_overlay_sprite="sparkler_tier2",
    anchor_name="weapon_mount",
    offsets_by_facing={"right": (0.0, -6.0), "left": (0.0, -6.0)},
    scale=0.8,
    draw_layer=1,
    rotation_rule=WeaponVisualRotationRule(
        idle_angle_degrees=-8.0,
        moving_angle_degrees=-14.0,
        mirror_angle_with_facing=True,
        flip_with_facing=True,
    ),
)

WEAPON_VISUAL_VARIANT_RULES["sparkler"] = (
    WeaponVisualVariantRule(variant_id="tier2", min_evolution_count=1),
    WeaponVisualVariantRule(variant_id="tier1", min_evolution_count=0),
)
```

