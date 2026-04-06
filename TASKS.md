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
