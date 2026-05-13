# TASKS.md

## Project Phase: Kazoo Beam Weapon System

Objective: Add Kazoo Beam as a new party-themed directional beam weapon that fills the sustained damage / piercing / lane control archetype, with scalable support for upgrades, evolutions, and visual variants.

Weapon fantasy:
A ridiculous party kazoo emits a concentrated musical energy beam that pierces through enemies. Evolutions transform it into rainbow lasers, sonic shockwaves, and chaotic feedback storms.

---

## Design Intent

### Gameplay Role

Kazoo Beam should fill:

* sustained directional DPS
* piercing line damage
* target focus / elite melting
* lane control
* commitment-based positioning

Compared to current weapons:

* Bottle Rocket = burst projectile chaos
* Sparkler = melee control
* Yo-Yo = roaming tether damage
* Bubble Wand = zoning / battlefield shaping
* Kazoo Beam = directional sustained pressure

Core fantasy:
"adorably annoying weaponized noise"

---

## Core Design Decisions

Initial recommended behavior:

* auto-target nearest enemy direction
  OR
* fire in player facing direction

Beam characteristics:

* short startup
* sustained duration
* cooldown between bursts
* pierces enemies
* visually loud and readable

Recommended first implementation:
**burst beam (timed pulses)**

Not:
continuous always-on beam

Reason:
simpler implementation
easier balancing
clear upgrade progression path toward continuous beam later

---

## Task 1: Add Kazoo Beam Weapon Definition [DONE]

### Objective

Introduce Kazoo Beam as a first-class weapon.

### Requirements

Add:

* weapon id:

  * `kazoo_beam`

* display name:

  * `Kazoo Beam`

Register in weapon config / definitions.

Baseline stats:

* beam damage
* beam duration
* cooldown
* beam width
* beam range
* tick interval
* pierce count (or infinite pierce)

Suggested baseline:

* medium-high damage
* medium cooldown
* medium range
* narrow beam
* short duration pulse

### Acceptance Criteria

* Kazoo Beam exists as selectable weapon
* Config loads cleanly

---

## Task 2: Implement Beam Entity / Weapon Logic [DONE]

### Objective

Create directional beam attack behavior.

### Requirements

Implement beam firing logic:

* choose firing direction
* activate beam
* remain active for beam duration
* deactivate cleanly
* enter cooldown

Beam modes should support future variants:

* pulsed beam
* continuous beam
* sweeping beam
* chained beam

Architecture should be extensible.

### Acceptance Criteria

* Beam activates and deactivates correctly
* Cooldown loop works reliably

---

## Task 3: Implement Targeting Logic [DONE]

### Objective

Determine where the beam points.

### Requirements

Choose initial targeting behavior.

Recommended:
nearest enemy auto-target

Alternative:
player facing direction

Implement:

* direction calculation
* fallback if no enemies
* stable target lock during beam duration
  OR configurable retarget behavior

Future support:

* dynamic retargeting
* beam sweep
* player-controlled aiming

### Acceptance Criteria

* Beam consistently points in intended direction
* No jittery targeting

---

## Task 4: Add Beam Collision / Damage Logic [DONE]

### Objective

Make beam damage feel satisfying and fair.

### Requirements

Implement:

* beam hitbox
* enemy intersection checks
* piercing damage
* configurable tick interval
* per-enemy tick protection
* clean dead enemy handling

Support:

* multi-target damage
* configurable range
* configurable beam width

### Acceptance Criteria

* Beam damages all valid targets in path
* Damage timing feels correct

---

## Task 5: Create Kazoo Art Assets [DONE]

### Objective

Add first visual implementation.

### Requirements

Create:

Kazoo weapon sprite:

* cute toy kazoo
* pastel party style
* transparent background
* readable at gameplay scale

Beam visuals:

* Tier 1 beam effect
* soft colorful musical beam
* simple readable line effect

Optional:

* musical note particles
* sound wave effect

Style direction:

* playful
* toy aesthetic
* rounded shapes
* clean silhouette
* plush-compatible

Register assets in loader.

### Acceptance Criteria

* Kazoo renders correctly
* Beam visuals match game style

---

## Task 6: Add Equipped Overlay Visual [DONE]

### Objective

Show Kazoo when equipped.

### Requirements

Integrate with overlay framework.

Add config:

* sprite
* anchor
* offsets
* scale
* angle
* z layer

Optional:
beam-ready pose offset

Support:

* facing direction adjustments

### Acceptance Criteria

* Kazoo appears correctly on player
* Uses shared overlay architecture

---

## Task 7: Add Beam Rendering System [DONE]

### Objective

Create visually satisfying beam effects.

### Requirements

Render beam with:

* start point at player weapon anchor
* endpoint based on range
* configurable beam width
* configurable color
* animated beam effect

Support:

* glow
* pulse
* layered beam visuals
* optional beam flicker

Future extensibility:

* rainbow beam
* thicker evolved beams
* branching effects

### Acceptance Criteria

* Beam is readable and visually satisfying

---

## Task 8: Add Kazoo Upgrade Definitions [DONE]

### Objective

Create progression path.

### Requirements

Add:

### kazoo_range_up

Effect:

* longer beam
  Tag:
* `kazoo_range`

---

### kazoo_width_up

Effect:

* wider beam
  Tag:
* `kazoo_width`

---

### kazoo_power_up

Effect:

* stronger beam damage
  Tag:
* `kazoo_power`

---

### kazoo_duration_up

Effect:

* longer beam duration
  Tag:
* `kazoo_duration`

---

### kazoo_speed_up

Effect:

* shorter cooldown / faster pulses
  Tag:
* `kazoo_speed`

---

### kazoo_chain_up

Effect:

* prepares chaining behavior
  Tag:
* `kazoo_chain`

Tune:

* weights
* stacks
* scaling

### Acceptance Criteria

* Kazoo upgrades appear during runs
* Stats scale correctly

---

## Task 9: Add Kazoo Evolutions [DONE]

### Objective

Integrate with evolution system.

### Requirements

Add:

## Rainbow Resonance

Tags:

* `kazoo_power`
* `kazoo_duration`

Behavior:

* thicker stronger rainbow beam

---

## Sonic Squeal

Tags:

* `kazoo_speed`
* `kazoo_width`

Behavior:

* rapid pulsing shock beam

---

## Feedback Loop

Tags:

* `kazoo_chain`
* `kazoo_power`

Behavior:

* beam chains to nearby enemies

---

## Party Laser

Tags:

* `kazoo_range`
* `kazoo_power`

Behavior:

* long elite-melting precision beam

---

## Disco Sweep

Tags:

* `kazoo_duration`
* `kazoo_width`

Behavior:

* sweeping rotating beam

### Acceptance Criteria

* Evolutions register successfully
* Eligibility logic recognizes them

---

## Task 10: Add Beam Sweep Support [DONE]

### Objective

Enable rotational / sweeping beam evolutions.

### Requirements

Implement optional beam movement:

* rotating angle over time
* configurable sweep speed
* configurable arc width
* stable collision updates during sweep

Future support:

* oscillation
* full circular sweep

### Acceptance Criteria

* Sweeping beam works reliably

---

## Task 11: Add VFX / Feel Polish [DONE]

### Objective

Make Kazoo Beam feel ridiculous and fun.

### Requirements

Add:

* beam startup flash
* pulse animation
* impact spark
* enemy hit feedback
* musical note particles
* sound hooks
* optional screen shake for stronger evolutions

Optional:
rainbow shimmer

### Acceptance Criteria

* Beam feels satisfying and thematic

---

## Task 12: Gameplay Balance Pass [DONE]

### Objective

Find distinct gameplay niche.

### Requirements

Playtest against:

* Bottle Rocket
* Sparkler
* Yo-Yo
* Bubble Wand

Tune:

* damage
* cooldown
* duration
* width
* range
* tick rate

Validate:

* not just “better projectile weapon”
* distinct commitment-based playstyle
* meaningful elite melting role

### Acceptance Criteria

* Kazoo Beam feels unique and balanced

---

# Suggested Implementation Order

1. Weapon definition
2. Targeting logic
3. Beam logic
4. Collision / damage
5. Beam rendering
6. Art assets
7. Overlay visuals
8. Upgrades
9. Evolutions
10. Sweep support
11. Polish
12. Balance pass

---

# Definition of Done

* Kazoo Beam is playable
* Beam fires correctly
* Targeting works
* Beam damages properly
* Overlay visuals work
* Upgrade path exists
* Evolutions are integrated
* Sweep support works
* Weapon feels distinct and fun

```
```

