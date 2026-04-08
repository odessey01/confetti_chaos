# TECH_SPEC.md

## 1. Overview

Confetti Chaos is a 2D survivor-style arcade roguelite built with Python + Pygame.

Current implemented gameplay pillars:

* continuous spawning with mixed enemy ecosystem
* time/score/level-based run pressure scaling
* boss encounters with phases and ability cues
* run XP + level-up upgrade flow (1 of 3 choices)
* centralized audio, settings, and background systems

Architecture priorities:

* simple, modular systems
* clear data-driven tuning points
* stable 60 FPS gameplay target
* keep game shippable at all times

---

## 2. Technology Stack

* Language: Python 3.10+
* Framework: Pygame 2.x
* Tests: pytest
* Packaging: PyInstaller (active workflow via `build.ps1`)
* Data format: JSON for settings/persistent values

---

## 3. Current Project Structure

```text
src/
  main.py
  enemies/
    hazard.py
    tracking_hazard.py
    balloon_enemy.py
    pinata_enemy.py
    confetti_sprayer.py
    confetti_spray.py
    streamer_snake.py
    boss_balloon.py
  player/
    player.py
    projectile.py
  systems/
    game_session.py
    spawn_controller.py
    level_config.py
    run_progression.py
    run_upgrades.py
    audio.py
    background.py
    settings.py
    ui.py
    visual_feedback.py
    confetti.py
tests/
docs/
assets/
```

Notes:

* System boundaries are module-level rather than deep folder nesting.
* Enemy behavior and spawn tuning are centralized under `enemies/` + `systems/spawn_controller.py`.

---

## 4. Runtime Loop and State Model

Target frame rate: 60 FPS.

Primary states:

* `MENU`
* `PLAYING`
* `LEVEL_UP`
* `PAUSED`
* `GAME_OVER`

State rules:

* exactly one active state at a time
* transitions are explicit
* `LEVEL_UP` and `PAUSED` freeze active gameplay simulation

High-level loop:

```text
poll input/events
apply state transitions
update active simulation (if PLAYING)
consume gameplay/audio cues
draw world + ui + overlays
present frame
```

---

## 5. Enemy and Hazard System

Implemented enemy families:

* Tracking Hazard (homing pressure)
* Balloon Enemy (baseline drift pressure)
* Pinata Enemy (multi-hit reward target + split behavior)
* Confetti Sprayer (telegraphed directional ranged hazard)
* Streamer Snake (head + trailing body hazard)
* Boss Balloon (multi-phase milestone encounter)

Core enemy rules:

* spawn-time profile assignment
* spawn snapshot persistence (no retroactive mutation when level changes)
* enemy-specific behavior snapshots for telemetry/debug readability

---

## 6. Spawn, Tier, and Flavor System

`SpawnController` owns:

* spawn intervals and hazard caps
* mixed-tier pool selection and weight decay
* per-kind spawn shares (tracking/balloon/pinata/sprayer/snake)
* boss-context caps for special enemies
* flavor-based behavior tuning profiles
* spawn telemetry summaries

Flavor set:

* `STANDARD`
* `SWARM`
* `HUNTERS`
* `STORM`

Flavor effects can tune:

* spawn probabilities
* attack cadence/shape (sprayer)
* movement profile/segment profile (streamer snake)
* pacing characteristics

---

## 7. Boss System

Boss encounters occur on milestone levels and support:

* chase behavior with smooth turning
* configurable health/damage
* phased escalation
* ability cues (e.g., burst spawns, surges, charge patterns)
* defeat celebration window and bonus rewards

Fairness controls include:

* enemy-count and special-spawn caps during boss context
* bounded speed/turning and cooldown-driven ability cadence

---

## 8. Run Progression and Upgrades

Run progression is independent of stage level progression.

Tracks:

* run level
* run XP
* pending level-ups

Level-up flow:

1. gain XP from kill events
2. enqueue level-up
3. enter `LEVEL_UP`
4. choose 1 of 3 valid upgrades
5. apply effect immediately and resume

Upgrade system:

* centralized definitions with metadata + caps
* validity filtering (avoid capped/invalid options)
* weighted selection support
* stackable effects with bounded outcomes

---

## 9. Player and Weapon System

Player currently supports:

* responsive movement
* directional firing
* upgrade-modified speed/combat stats

Weapon behavior:

* cooldown-limited projectile firing
* active projectile cap (current baseline starts at 3; upgrades increase to max 5)
* projectile damage/speed/fire-rate modified by run upgrades

---

## 10. Collision and Combat Rules

Collision coverage:

* player vs enemy bodies/hazards (including snake head/body and sprayer projectiles)
* projectile vs enemies

Combat correctness rules:

* prevent rapid duplicate hits via invulnerability windows on multi-hit enemies
* clamp per-frame event effects to avoid runaway stacking
* clean expiration/removal for projectiles, sprays, and transient hazards

---

## 11. Audio System

Centralized `AudioManager` supports:

* `SFX`
* `music`
* `ambient`

Runtime controls:

* enable/disable sound
* per-category volume mix (`master/music/sfx/ambient`)
* robust fallback behavior for missing or unavailable assets/devices

Audio cues are emitted by gameplay systems and consumed in main loop for decoupled playback.

---

## 12. Settings and Persistence

Persistent settings include:

* sound enabled toggle
* selected start level
* volume mix values

Rules:

* load on startup with defaults
* save on runtime changes and shutdown
* safe fallback on missing/corrupt files

Additional persistence:

* high score load/save

---

## 13. Rendering and Visual Layers

Current render order:

1. background renderer (theme + ambient/parallax layers)
2. world entities (enemies/projectiles/player/confetti)
3. UI overlays and state screens
4. visual feedback overlays (pulses/shake/transitions)

Readability goals:

* player/enemy contrast preserved over background effects
* effects are expressive but not gameplay-obscuring

---

## 14. Testing and Build Workflow

Primary validation commands:

* run game: `python src/main.py`
* run tests: `pytest -q`
* build package: `.\build.ps1`

Definition of acceptance for feature work:

* tests pass
* no runtime errors in core flows
* no regression to progression/spawn/collision/state systems

---

## 15. Current Scope vs Next Scope

Current implemented scope includes:

* enemy ecosystem through Streamer Snake balance pass (Tasks 91-99)
* progression + upgrades phase 1
* audio/background foundation and polish passes

Next planned scope (from `TASKS.md`, as of 2026-04-07):

* Tasks 100-106: player visual refactor + party-animal presentation pass
* decouple player rendering from logic
* directional facing/juice/color variants/sprite fallback/clarity pass

---

## 16. Coding and Agent Rules

* keep modules focused and readable
* avoid unnecessary abstractions/framework additions
* make smallest safe change for each task
* always plan before implementation
* verify with tests/runtime checks before completion

---

## 17. Non-Goals (Current Phase)

Do not add in this phase unless explicitly scoped:

* multiplayer/networking
* heavy physics/inventory/equipment systems
* broad metaprogression economy
* large content pipelines beyond current vertical-slice roadmap

---

## 18. Guiding Principle

> Keep it simple, readable, performant, and fun.

* prioritize gameplay feel and clarity
* keep systems data-driven and easy to tune
* preserve fast iteration velocity with a playable build at all times
