# TASKS.md

## Project Phase: Bottle Rocket Visual Overlay System

Goal: Implement the bottle rocket as a player-attached visual overlay that can evolve over time, while keeping the system extensible for future weapon visuals, additional rocket tiers, and other weapon types.

---

## 1. Define the visual overlay architecture

### Objective
Create a reusable framework for weapon visuals that can be attached to the player without hardcoding Bottle Rocket-specific behavior everywhere.

### Tasks
- [x] Add a `WeaponVisualOverlay` concept to represent a visual attached to the player
- [x] Decide where overlay ownership should live:
  - [ ] player entity
  - [ ] equipped weapon instance
  - [x] a dedicated visual manager
- [x] Define a clean data model for overlays with fields such as:
  - [x] `overlay_id`
  - [x] `sprite_path`
  - [x] `anchor_name`
  - [x] `offset_x`
  - [x] `offset_y`
  - [x] `rotation_degrees`
  - [x] `scale`
  - [x] `z_index`
  - [x] `visible`
- [x] Keep the model generic so it can support non-rocket overlays later
- [x] Add comments documenting the intended use for future weapon visuals

### Acceptance Criteria
- There is a reusable overlay abstraction
- Bottle Rocket can use it without forcing future weapons into a custom one-off path

---

## 2. Add a player weapon anchor system

### Objective
Give the player a stable attachment point for the rocket overlay.

### Tasks
- [x] Add a named weapon anchor for the player sprite, such as `weapon_hand_right` or `weapon_mount`
- [x] Define the anchor in player-local space so it moves with the player
- [x] Make the anchor work with the current facing direction
- [x] Ensure the anchor can support flipping for left/right facing if needed
- [x] Add debug rendering option to display the anchor point during development
- [x] Document anchor coordinates for each player state if animation-specific offsets are needed later

### Acceptance Criteria
- The player has a stable anchor point for weapon overlays
- The anchor follows player movement and facing correctly

---

## 3. Import and register the Tier 1 bottle rocket asset

### Objective
Add the generated rocket art as the first overlay-capable weapon visual.

### Tasks
- [x] Add the Tier 1 bottle rocket image to the project asset structure
- [x] Place it in a weapon visuals folder with room for future tiers, for example:
  - [x] `assets/weapons/bottle_rocket/tier1.png`
- [x] Normalize the sprite size and pivot so it aligns consistently in-game
- [x] Remove or crop unnecessary whitespace if needed
- [x] Confirm transparency renders correctly
- [x] Register the asset in any asset-loading or manifest system used by the game

### Acceptance Criteria
- The Tier 1 rocket sprite is imported and accessible at runtime
- The sprite renders cleanly with transparent background

---

## 4. Render the rocket as a player overlay

### Objective
Attach the rocket sprite to the player visually rather than treating it as part of the base player sprite.

### Tasks
- [x] Render the rocket overlay relative to the player anchor each frame
- [x] Add configurable offset values so the rocket sits naturally in the player's hand / mount position
- [x] Add configurable draw order so the rocket can appear:
  - [x] behind player
  - [x] in front of player
  - [x] based on facing direction if desired
- [x] Add basic scale control so the overlay size can be tuned without editing the source asset
- [x] Make the overlay hide when the weapon is unequipped or inactive
- [x] Ensure the overlay updates with player movement and animation without jitter

### Acceptance Criteria
- The rocket appears attached to the player in a believable position
- It can be moved, scaled, and layered via config rather than hardcoded constants

---

## 5. Add facing and rotation support

### Objective
Make the rocket visually align with player direction and leave room for future aiming support.

### Tasks
- [x] Add logic so the rocket can flip or rotate based on player facing
- [x] Decide whether Bottle Rocket should:
  - [x] stay fixed in a carried pose
  - [ ] point toward aim direction
  - [x] tilt slightly while moving
- [x] Implement a simple initial behavior, such as:
  - [x] fixed carry angle when idle
  - [x] slight forward tilt while moving
- [x] Store angle/flip behavior in configuration so future weapons can define their own rules
- [x] Ensure visuals still look correct when mirrored

### Acceptance Criteria
- The rocket visually matches player facing
- Orientation behavior is configurable for future weapon overlays

---

## 6. Create a Bottle Rocket visual definition file

### Objective
Separate visual configuration from gameplay logic so new rocket tiers and future weapons can be added easily.

### Tasks
- [x] Add a config structure for weapon visuals, such as `weapon_visuals.py`, JSON, or YAML
- [x] Create a Bottle Rocket visual definition entry with fields such as:
  - [x] `weapon_id`
  - [x] `default_overlay_sprite`
  - [x] `anchor_name`
  - [x] `offsets_by_facing`
  - [x] `rotation_rules`
  - [x] `scale`
  - [x] `draw_layer`
- [x] Support multiple named visual variants, starting with:
  - [x] `tier1`
  - [x] `tier2`
  - [x] `tier3`
- [x] Keep the config generic enough to support Sparkler and future weapons
- [x] Add TODO placeholders for future VFX and trail hooks

### Acceptance Criteria
- Bottle Rocket overlay visuals are driven by data/config
- New tiers can be added by registering new variants, not rewriting runtime code

---

## 7. Support evolution-driven visual variants

### Objective
Allow the rocket overlay to visually upgrade as the player evolves the weapon.

### Tasks
- [x] Add a resolver that determines which bottle rocket visual variant should be active
- [x] Start with simple mapping rules:
  - [x] default weapon uses `tier1`
  - [x] first evolution uses `tier2`
  - [x] advanced / merged evolution state uses `tier3`
- [x] Make the resolver data-driven instead of hardcoded to exact evolution IDs
- [x] Add support for future rules such as:
  - [x] based on evolution count
  - [x] based on tags
  - [x] based on specific evolution form
- [x] Swap overlay sprite at runtime when the visual tier changes
- [x] Ensure sprite changes do not cause flicker or stale asset references

### Acceptance Criteria
- Bottle Rocket can switch between multiple visual tiers
- The variant selection logic is extensible for future rocket art and weapons

---

## 8. Add overlay animation hooks for future polish

### Objective
Prepare the system for subtle animation without requiring full implementation right away.

### Tasks
- [x] Add optional overlay animation properties such as:
  - [x] bob amplitude
  - [x] bob speed
  - [x] idle sway
  - [x] recoil offset
  - [x] firing flash hook
- [x] Implement at least one simple animation, such as a subtle idle bob or sway
- [x] Keep animation behavior optional and data-driven
- [x] Make sure the overlay can receive fire/reload/evolution events later
- [x] Add TODO hooks for trail, glow, and confetti particle attachments

### Acceptance Criteria
- The overlay system can support simple motion and future effects
- At least one basic motion effect works for the Bottle Rocket

---

## 9. Add extensibility for multiple weapon overlays

### Objective
Prevent the system from becoming Bottle Rocket-only.

### Tasks
- [x] Design the overlay manager to support other weapon types later
- [x] Ensure overlays are keyed by `weapon_id` or equivalent, not by special-case Bottle Rocket logic
- [x] Support registration of multiple overlay definitions
- [x] Make sure overlay rendering can be reused for Sparkler and future party weapons
- [x] Avoid direct references like `if weapon_id == "bottle_rocket"` in shared rendering code where possible
- [x] Add one example placeholder config entry for a future weapon, even if no asset exists yet

### Acceptance Criteria
- The overlay framework clearly supports future weapons
- Shared code remains generic

---

## 10. Add debug and tuning tools

### Objective
Make it easy to line up the rocket visually and tune it without repeated code edits.

### Tasks
- [x] Add a debug toggle to show:
  - [x] player anchor point
  - [x] overlay bounds
  - [x] overlay pivot point
- [x] Add temporary hot-reload or easy config reload if your engine supports it
- [x] Log or display the currently active overlay variant
- [x] Add quick tuning controls or easy constants for:
  - [x] offset x/y
  - [x] scale
  - [x] rotation
- [x] Capture recommended tuned values in config after alignment is correct

### Acceptance Criteria
- Overlay alignment can be tuned quickly
- Debug tools make visual setup easier for future overlays

---

## 11. Connect overlay visuals to equipped weapon state

### Objective
Ensure the correct overlay appears only when the Bottle Rocket is the relevant active/equipped weapon.

### Tasks
- [x] Identify the current source of truth for equipped or active weapon
- [x] Show the Bottle Rocket overlay only when Bottle Rocket is equipped / selected / active
- [x] Hide or swap overlay when the player changes weapon
- [x] Ensure the system behaves correctly if the player can hold multiple weapons
- [x] Define fallback behavior for:
  - [x] no active weapon
  - [x] unknown weapon visual
  - [x] missing asset

### Acceptance Criteria
- The Bottle Rocket overlay appears only in the right gameplay state
- Missing visuals fail gracefully

---

## 12. Document the overlay pipeline

### Objective
Make it easy to add Tier 2, Tier 3, and future weapon overlays later.

### Tasks
- [x] Add a short markdown doc explaining:
  - [x] where weapon overlay sprites live
  - [x] how they are registered
  - [x] how anchors work
  - [x] how visual variants are selected
- [x] Document naming conventions for bottle rocket variants
- [x] Document how future weapons should plug into the system
- [x] Add a small example showing how to register a new overlay variant

### Acceptance Criteria
- Another developer can add a new weapon overlay without reverse engineering the system

---

## Suggested Implementation Order

1. Define reusable overlay architecture
2. Add player weapon anchor
3. Import Tier 1 bottle rocket asset
4. Render rocket as overlay on the player
5. Add facing/rotation support
6. Create data-driven weapon visual definitions
7. Add evolution-driven variant selection
8. Add basic animation hooks
9. Add debug/tuning tools
10. Connect to equipped weapon state
11. Document the pipeline

---

## Definition of Done

- [x] Tier 1 bottle rocket renders as a player overlay
- [x] Overlay uses a reusable architecture, not a one-off implementation
- [x] Overlay positioning is anchor-based and configurable
- [x] Visual variants can be added for future rocket tiers
- [x] Runtime can swap bottle rocket visuals based on evolution state
- [x] Shared code is extensible for future weapon overlays
- [x] Debug tools and documentation are in place
