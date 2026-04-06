# GAME_VISION.md

## 1. Game Overview

**Working Title:** TBD
**Genre:** 2D (choose: Roguelike / Arcade / Survival / Puzzle / Narrative)
**Platform:** PC (Steam)
**Engine/Framework:** Python (Pygame / Arcade / Panda3D - TBD)

**High Concept:**
A short, repeatable gameplay loop where the player:

* Enters a contained environment
* Performs a core action repeatedly
* Responds to increasing challenge
* Either succeeds (progression) or fails (restart loop)

> The game should be easy to learn in under 30 seconds but offer depth through repetition and mastery.

---

## 2. Core Gameplay Loop

1. Player spawns into the game world
2. Player performs primary action (move / interact / avoid / attack)
3. Game introduces pressure (enemy / timer / hazard / resource constraint)
4. Player adapts or fails
5. Outcome:

   * Success → score/progression increases
   * Failure → restart quickly

**Design Principle:** Fast restarts (<3 seconds)

---

## 3. Player Experience Goals

* Immediate responsiveness (tight controls)
* Clear visual feedback for all actions
* Increasing tension over time
* “One more try” replayability
* Minimal friction (no complex menus or setup)

---

## 4. Visual & Artistic Direction

* Style: Minimalist / Tonalist / Atmospheric 

* Color Palette:

  * Limited palette
  * Strong contrast for gameplay elements
  * Backgrounds should not compete with gameplay

* Camera:

  * Fixed 2D view (top-down or side view)
  * No complex camera movement in v1

---

## 5. Technical Constraints

* Target: 60 FPS minimum

* Resolution: 1280x720 minimum (scalable to 1080p)

* Input:

  * Keyboard required
  * Controller support (future phase)

* Architecture:

  * Modular systems (no monolithic files)
  * Clear separation:

    * input
    * player
    * enemies
    * physics
    * rendering
    * UI
    * game state

---

## 6. Scope (v1 - Vertical Slice)

The first playable version MUST include:

* One playable scene/level
* Player movement
* One core mechanic (e.g., dodge, shoot, collect)
* One enemy or hazard type
* Basic collision system
* Score tracking
* Game over + restart loop

**Non-goals (v1):**

* No advanced menus
* No multiplayer
* No complex AI
* No large content systems

---

## 7. Progression & Systems (Post-v1)

* Multiple enemy types
* Difficulty scaling
* Power-ups or upgrades
* Persistent progression (optional)
* Audio polish
* Controller support

---

## 8. AI Agent Development Rules

When modifying this project, the AI must:

1. Read this file before making changes
2. Preserve the core gameplay loop
3. Avoid adding unnecessary complexity
4. Keep code modular and readable
5. Do NOT introduce new frameworks without approval
6. Do NOT expand scope beyond current phase
7. Provide:

   * clear plan before implementation
   * list of files to modify
   * verification steps after changes

---

## 9. Definition of Done (for any feature)

A feature is complete when:

* It works in-game without errors
* It does not break existing systems
* It includes basic test or validation steps
* It aligns with performance targets
* It matches the core gameplay loop

---

## 10. Packaging Goal (Steam)

The final game must:

* Run as a standalone executable (no Python required on user machine)
* Support full-screen and windowed mode
* Handle input reliably
* Exit cleanly with no crashes

---

## 11. Guiding Philosophy

> Build small, finish fast, iterate often.

* Prefer simple systems that work over complex systems that don’t
* Prioritize feel over features
* Keep the game shippable at all times

---
