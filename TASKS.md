# TASKS.md

## Project Phase: v1 Vertical Slice

Goal: Deliver a minimal, playable game loop that can be launched, played, failed, and restarted.

---

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


# Execution Rules for Agents

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
