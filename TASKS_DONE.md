# TASKS.md

## Project Phase: v1 Vertical Slice

Goal: Deliver a minimal, playable game loop that can be launched, played, failed, and restarted.

---

## Task 0 – Project Setup

**Status:** DONE

### Objective

Create initial project structure and runnable game entry point.

### Requirements

* Create folder structure:

  * `src/`
  * `src/systems/`
  * `src/player/`
  * `src/enemies/`
  * `assets/`
  * `tests/`

* Create:

  * `src/main.py`
  * basic game loop (window opens, runs, closes cleanly)

* Choose framework:

  * Default: `pygame`

### Acceptance Criteria

* Running `python src/main.py` opens a window
* No errors in console
* Clean exit on close

---

## Task 1 – Game Loop & State Management

**Status:** DONE

### Objective

Implement a basic game state system.

### Requirements

* Create game states:

  * `MENU`
  * `PLAYING`
  * `GAME_OVER`

* Implement state transitions:

  * Start → PLAYING
  * Death → GAME_OVER
  * Restart → PLAYING

### Acceptance Criteria

* Game can transition between states without crashing
* State changes are clearly logged or visible

---

## Task 2 – Player Movement

**Status:** DONE

### Objective

Add controllable player entity.

### Requirements

* Player object/module
* Movement using keyboard:

  * WASD or arrow keys
* Smooth movement (no grid snapping)

### Acceptance Criteria

* Player moves responsively
* Movement feels immediate (no lag)
* Player remains within screen bounds

---

## Task 3 – Core Mechanic (Dodge or Avoid)

**Status:** DONE

### Objective

Implement the primary gameplay mechanic.

### Requirements

* Choose mechanic:

  * Default: avoid incoming enemies/hazards

* Spawn at least one hazard type

* Hazards move toward or across the player

### Acceptance Criteria

* Hazards appear and move
* Player must actively avoid them
* Interaction creates tension

---

## Task 4 – Collision System

**Status:** DONE

### Objective

Detect interactions between player and hazards.

### Requirements

* Implement collision detection
* On collision:

  * Trigger GAME_OVER state

### Acceptance Criteria

* Collision is accurate and consistent
* Game reliably ends on contact

---

## Task 5 – Score System

**Status:** DONE

### Objective

Track player performance.

### Requirements

* Score increases over time or survival
* Display score on screen

### Acceptance Criteria

* Score updates in real time
* Score resets on restart

---

## Task 6 – Game Over + Restart Loop

**Status:** DONE

### Objective

Enable fast replay loop.

### Requirements

* Display "Game Over"
* Show final score
* Restart input (e.g., press R or Space)

### Acceptance Criteria

* Restart happens in <3 seconds
* Game resets cleanly (no lingering state)

---

## Task 7 – Basic UI Layer

**Status:** DONE

### Objective

Add minimal UI elements.

### Requirements

* Render:

  * Score
  * Game state text (Start / Game Over)

### Acceptance Criteria

* UI is readable and not intrusive
* No performance impact

---

## Task 8 – Basic Structure Refactor

**Status:** DONE

### Objective

Clean up code for modularity.

### Requirements

* Separate logic into modules:

  * player
  * enemies
  * systems
* Remove duplicated code

### Acceptance Criteria

* No single file > ~300 lines
* Clear separation of concerns

---

## Task 9 – Basic Testing / Validation

**Status:** DONE

### Objective

Ensure stability of core systems.

### Requirements

* Add at least:

  * one test or validation for collision
  * one test or validation for state transitions

### Acceptance Criteria

* Tests run without failure
* No runtime crashes during normal play

---

## Task 10 – Pre-Packaging Prep

**Status:** DONE

### Objective

Prepare project for packaging.

### Requirements

* Ensure:

  * no hardcoded paths
  * assets load correctly
  * game runs from root

### Acceptance Criteria

* Game runs from clean environment
* Ready for PyInstaller step

---

## Task 11 – Difficulty Scaling

**Status:** DONE

### Objective

Make the game become more challenging over time.

### Requirements

* Increase hazard/enemy pressure gradually

* Scale one or more of:

  * spawn rate
  * movement speed
  * number of simultaneous hazards

* Keep early game fair

* Avoid sudden, unfair spikes

### Acceptance Criteria

* Game difficulty clearly ramps up over time
* Early gameplay is manageable
* Difficulty feels intentional, not random

---

## Task 12 – Spawn System Refactor

**Status:** DONE

### Objective

Create a cleaner and more controllable spawning system.

### Requirements

* Centralize hazard/enemy spawning logic
* Support configurable spawn timing
* Prevent impossible or unfair spawn locations
* Make spawn parameters easy to tune

### Acceptance Criteria

* Spawn behavior is predictable and adjustable
* No hazards spawn directly on the player
* Spawn logic is separated from main loop

---

## Task 13 – Main Menu Polish

**Status:** DONE

### Objective

Turn the start flow into a more complete player experience.

### Requirements

* Add a simple title screen

* Show:

  * game title
  * start prompt
  * quit prompt

* Ensure transition into gameplay is smooth

### Acceptance Criteria

* Menu is clear and readable
* Player can start or quit without confusion
* State transition from menu to gameplay is reliable

---

## Task 14 – High Score Persistence

**Status:** DONE

### Objective

Save player progress between runs.

### Requirements

* Save high score locally
* Load high score on startup
* Display high score in menu or game over screen
* Handle missing save file safely

### Acceptance Criteria

* High score persists between sessions
* Game does not crash if save file is missing or corrupt
* High score display updates correctly

---

## Task 15 – Audio Pass (Minimal)

**Status:** DONE

### Objective

Add basic sound feedback to improve feel.

### Requirements

* Add at least:

  * one sound for collision/game over
  * one sound for menu start or restart

* Keep implementation simple

* Allow game to run even if audio assets are unavailable

### Acceptance Criteria

* Sounds play at the correct moments
* Missing or failed audio load does not crash the game
* Audio improves feedback without becoming distracting

## Milestone – Prototype Complete
At this point the game should feel like a real, replayable product rather than a technical demo.

## Task 16 – Visual Feedback & Juice Pass

**Status:** DONE

### Objective

Improve clarity and game feel through simple visual feedback.

### Requirements

* Add visual feedback for:

  * player hit / death
  * hazard spawn or movement emphasis
  * state transitions (menu → play, play → game over)

* Consider lightweight effects such as:

  * flash on collision
  * brief screen shake
  * fade in/out text
  * simple particle burst

* Keep effects minimal and performance-friendly

### Acceptance Criteria

* Important gameplay events are more visible
* Visual feedback improves feel without clutter
* No noticeable performance drop

---

## Task 17 – Second Hazard or Enemy Type

**Status:** DONE

### Objective

Increase gameplay variety with an additional challenge type.

### Requirements

* Add one new hazard/enemy behavior distinct from the first

* Examples:

  * faster but fragile hazard
  * slower tracking hazard
  * hazard with intermittent movement
  * obstacle that constrains movement

* Ensure both hazard types can appear during gameplay

* Balance for fairness and readability

### Acceptance Criteria

* New hazard type is visually and behaviorally distinct
* Gameplay variety is noticeably improved
* Combined hazard behavior remains fair and playable

---

## Task 18 – Pause & Basic Settings

**Status:** DONE

### Objective

Add a minimal pause flow and player control over basic settings.

### Requirements

* Add pause toggle (e.g., Esc or P)

* While paused:

  * stop gameplay updates
  * show pause message or overlay

* Add basic settings support for:

  * audio on/off or volume placeholder
  * window mode placeholder or future config hook

### Acceptance Criteria

* Player can pause and resume reliably
* No gameplay state corruption while paused
* Settings structure exists and can be extended later

---

## Task 19 – Controller Support

**Status:** DONE

### Objective

Prepare the game for a more Steam-friendly input experience.

### Requirements

* Add basic controller/gamepad input support

* Support at minimum:

  * movement
  * start/restart
  * menu confirm

* Preserve keyboard support

* Ensure input handling remains modular

### Acceptance Criteria

* Game is playable with either keyboard or controller
* Input prompts or behavior remain clear
* No regression to keyboard controls

---

## Task 20 – Packaging & Release Prep

**Status:** DONE

### Objective

Create a repeatable build path for local release testing.

### Requirements

* Add packaging configuration for standalone build

* Validate:

  * assets are bundled correctly
  * executable launches cleanly
  * save/high score behavior works in packaged build

* Document build steps

* Add release checklist for local validation

### Acceptance Criteria

* A standalone build can be created successfully
* Packaged game runs without requiring local Python install
* Build steps are documented clearly for future Steam upload workflow

## Task 21 – Player Avatar (Visual + Identity)

**Status:** DONE

### Objective

Replace placeholder player with a defined avatar.

### Requirements

* Create a simple but recognizable player avatar:

  * shape-based (circle, triangle, or custom sprite)
  * distinct color from enemies

* Add:

  * facing direction (optional but preferred)
  * slight movement feedback (e.g., subtle scale or rotation)

* Keep implementation lightweight (no animation system yet)

### Acceptance Criteria

* Player is visually distinct and readable at all times
* Movement feels slightly more “alive” than a static object
* No impact to performance or controls

---

## Task 22 – Balloon Enemies

**Status:** DONE

### Objective

Introduce a themed enemy type: balloons.

### Requirements

* Replace or extend hazards with balloon enemies:

  * circular shape
  * bright, varied colors
  * slight float/bob movement

* Behavior:

  * drift toward player OR float across screen
  * predictable but slightly varied motion

* Spawn system should support multiple balloons

### Acceptance Criteria

* Balloons are visually distinct and readable
* Movement feels light/floaty (not rigid)
* Multiple balloons can exist simultaneously without issues

---

## Task 23 – Weapon System (Basic Attack)

**Status:** DONE

### Objective

Allow the player to actively fight back.

### Requirements

* Add a basic weapon:

  * default: directional projectile (e.g., small bullet or dart)

* Input:

  * key press (e.g., space or mouse click)

* Behavior:

  * projectile travels in a direction
  * disappears on impact or after time

* Limit complexity:

  * no ammo system
  * no upgrades (yet)

### Acceptance Criteria

* Player can fire reliably
* Projectiles behave consistently
* No performance issues with multiple projectiles

---

## Task 24 – Enemy Hit & Kill System

**Status:** DONE

### Objective

Enable interaction between weapons and enemies.

### Requirements

* Detect collision between projectile and balloon

* On hit:

  * remove balloon
  * increment score

* Ensure:

  * no duplicate hit events
  * clean removal of entities

### Acceptance Criteria

* Balloons are destroyed on hit
* Score increases correctly
* No lingering or “ghost” entities

---

## Task 25 – Confetti Effect on Kill

**Status:** DONE

### Objective

Add satisfying visual feedback when enemies are destroyed.

### Requirements

* On balloon pop:

  * spawn simple confetti particles
  * use small colored shapes (no heavy system)

* Behavior:

  * particles scatter outward briefly
  * fade or disappear after short duration

* Keep system lightweight:

  * limit particle count
  * no physics engine required

### Acceptance Criteria

* Confetti triggers on every kill
* Effect feels satisfying but not overwhelming
* No noticeable performance impact

## Task 26 – Level System (Basic Progression)

**Status:** DONE

### Objective

Introduce a level-based progression system.

### Requirements

* Add level counter (starting at Level 1)

* Increase level based on:

  * time survived OR
  * score threshold

* Display current level on screen

### Acceptance Criteria

* Level increases during gameplay
* Level is clearly visible to player
* No disruption to existing game loop

---

## Task 27 – Level Configuration System

**Status:** DONE

### Objective

Define how each level behaves using configurable parameters.

### Requirements

* Create a level configuration structure (e.g., dict or class):

  * spawn rate
  * enemy speed
  * max enemies
  * enemy types allowed

* Scale values per level (linear or slight curve)

Example:

* Level 1: slow, sparse
* Level 5: moderate
* Level 10+: fast, dense

### Acceptance Criteria

* Each level feels progressively harder
* Values are easy to tweak in one place
* No hardcoded values scattered across code

---

## Task 28 – Dynamic Spawn Scaling

**Status:** DONE

### Objective

Make spawning responsive to level difficulty.

### Requirements

* Modify spawn system to:

  * reference current level config
  * adjust spawn timing and count dynamically

* Ensure:

  * no overwhelming spikes
  * no impossible situations

### Acceptance Criteria

* Spawn behavior clearly changes with level
* Difficulty feels smooth and intentional
* No sudden unfair difficulty jumps

## Task 29 – Level Flavor System

**Status:** DONE

### Objective

Give groups of levels distinct gameplay identities.

### Requirements

* Introduce a "flavor" concept for levels

* Each flavor modifies spawn and behavior patterns without requiring a new map system

* Initial flavors:

  * **Standard**: balanced enemy mix and pacing
  * **Swarm**: many smaller or lighter balloons, higher spawn count
  * **Hunters**: fewer balloons, faster tracking or more direct pursuit
  * **Storm**: burst spawning, denser pressure windows

* Assign flavors by level or by weighted selection

* Flavor logic should remain data-driven and easy to tune

### Acceptance Criteria

* Different levels feel meaningfully different
* Flavors are easy to identify during gameplay
* Flavor behavior is configurable from one place

---

## Task 30 – Flavor-Aware Level Generation

**Status:** DONE

### Objective

Make level generation use both difficulty scaling and flavor rules.

### Requirements

* Extend level generation/config system so that each level includes:

  * difficulty parameters
  * assigned flavor
  * spawn pattern adjustments

* Ensure flavor affects:

  * spawn timing
  * enemy count
  * enemy movement tendencies
  * allowed enemy mix

* Preserve fairness and readability

### Acceptance Criteria

* Generated levels reflect both progression and flavor
* Difficulty scaling remains smooth
* No flavor creates impossible or unfair scenarios

---

## Task 31 – Boss Balloon Design & Spawn Logic

**Status:** TODO

### Objective

Introduce a boss balloon encounter at milestone levels.

### Requirements

* Add a boss balloon enemy type

* Boss appears on milestone levels:

  * default: every 5th level

* Boss should be visually distinct:

  * larger size
  * special color palette
  * unique movement or presence

* Boss encounter should alter normal flow:

  * reduced standard spawns OR controlled support spawns during boss fight

### Acceptance Criteria

* Boss balloon spawns reliably on milestone levels
* Boss is immediately recognizable
* Boss encounter feels like a special event, not just a larger normal enemy

---

## Task 32 – Boss Balloon Combat & Defeat Flow

**Status:** TODO

### Objective

Make the boss balloon a real combat encounter.

### Requirements

* Give boss balloon a simple health system

* Boss requires multiple hits to defeat

* Add at least one boss-specific behavior:

  * charge burst
  * mini-balloon spawn
  * directional sweep
  * temporary speed increase after being hit

* On defeat:

  * grant score bonus
  * trigger stronger visual feedback
  * advance cleanly back into standard progression

### Acceptance Criteria

* Boss survives multiple hits
* Boss behavior feels distinct from regular balloons
* Boss defeat is satisfying and does not break progression flow

---

## Task 33 – Boss Celebration & Progression Transition

**Status:** TODO

### Objective

Reward the player and reinforce progression after boss completion.

### Requirements

* On boss defeat:

  * trigger enhanced confetti effect
  * display level clear or boss defeated message
  * briefly pause or transition before next level

* Add lightweight milestone feedback such as:

  * text banner
  * sound cue
  * score bonus summary

* Ensure next level starts cleanly

### Acceptance Criteria

* Boss defeat feels like a milestone
* Transition to the next level is clear and polished
* No state bugs or leftover boss entities persist after transition

## Task 34 – Enemy Snapshot Persistence on Level Transition

**Status:** TODO

### Objective

Ensure enemies already on screen keep their current attributes when the level changes.

### Requirements

* When a level transition occurs, existing enemies must retain:

  * current speed
  * current health
  * current behavior parameters
  * any flavor-specific traits assigned at spawn

* Level-up logic should affect only:

  * newly spawned enemies
  * future spawn rules

* Prevent retroactive mutation of active enemy instances

### Acceptance Criteria

* Enemies already on screen do not suddenly change behavior on level-up
* Only newly spawned enemies reflect the new level configuration
* Level transitions feel smooth and readable

---

## Task 35 – Spawn-Time Enemy Attribute Assignment

**Status:** TODO

### Objective

Assign enemy difficulty and behavior at the moment of spawn rather than recalculating from global level state.

### Requirements

* Each enemy instance should receive a spawn-time attribute set, such as:

  * tier
  * speed
  * health
  * movement profile
  * flavor tag

* Store these values on the enemy instance

* Avoid referencing current global level for per-frame enemy scaling

### Acceptance Criteria

* Enemy behavior is determined at spawn and remains stable
* Attribute assignment is modular and easy to inspect
* No active enemy changes stats due to later level increases

---

## Task 36 – Partial Tier Advancement Per Level

**Status:** TODO

### Objective

Flatten the power curve by allowing each level to introduce only some stronger enemies rather than upgrading the whole field.

### Requirements

* On each level increase, only a portion of newly spawned enemies should use the newest tier/config

* Remaining newly spawned enemies should come from one or more earlier tiers

* Add configurable weighting for spawn tiers, for example:

  * newest tier
  * previous tier
  * older fallback tier

* Keep logic flexible and data-driven

### Acceptance Criteria

* Level progression feels smoother and less spiky
* New difficulty enters gradually rather than all at once
* Enemy populations show a mix of tiers during mid-to-late levels

---

## Task 37 – Tier Pool Decay for Older Enemies

**Status:** TODO

### Objective

Allow lower-tier enemies to gradually drop out of the spawn pool as the player progresses.

### Requirements

* Add tier retirement or reduced weighting logic

* Older enemy tiers should:

  * remain common in early progression
  * become less common in later progression
  * eventually drop out when no longer useful

* Support configurable cutoffs or weighted decay

### Acceptance Criteria

* Early-tier enemies fade out naturally over time
* Spawn pool remains readable and intentionally paced
* Difficulty increases without overcrowding the game with obsolete enemy types

---

## Task 38 – Mixed-Tier Spawn Balancing & Telemetry

**Status:** TODO

### Objective

Validate that mixed-tier spawning creates a smooth and fair difficulty curve.

### Requirements

* Add lightweight debugging or logging for spawned enemy tiers

* Make it easy to inspect:

  * current level
  * active flavor
  * spawn tier distribution
  * boss level overrides if applicable

* Tune spawn weights so the game avoids:

  * abrupt spikes
  * excessively weak late-game waves
  * confusing mixtures that feel random

### Acceptance Criteria

* Tier mix can be observed and tuned easily
* Difficulty ramps feel intentional in playtesting
* Spawn distribution supports both variety and fairness


## Execution Rules for Agents

For each task:

1. Read `GAME_VISION.md` and `AGENTS.md`
2. Propose a plan BEFORE coding
3. List files to create/modify
4. Implement only the current task
5. Verify via:

   * running the game
   * checking for errors
6. Summarize changes clearly

---

## Notes

* Do NOT skip tasks
* Do NOT expand scope beyond current task
* Keep implementations simple and functional
* Prioritize playability over perfection

---
