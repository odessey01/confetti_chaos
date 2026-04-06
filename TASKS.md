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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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
