## Task 179 – Player Health System (Core State)

**Status:** DONE

### Objective

Introduce a simple health system for the player.

### Requirements

* Add player health properties:

  * `max_health` (default: 3)
  * `current_health`

* Initialize player with full health at start of run

* Reset health on new run

* Keep health system separate from rendering/UI

### Acceptance Criteria

* Player starts each run with 3 health
* Health value updates correctly in memory
* System is independent from UI implementation

---

## Task 180 – Damage Handling (Enemy → Player)

**Status:** DONE

### Objective

Reduce player health when colliding with enemies or hazards.

### Requirements

* On collision with:

  * enemies (balloons, piñatas, snakes, etc.)
  * hazard effects (sprayers, etc.)

* Reduce health by **1 per valid hit**

* Add short damage cooldown (invulnerability window), e.g.:

  * 0.5–1.0 seconds

* Prevent multiple hits per frame or rapid stacking damage

### Acceptance Criteria

* Player loses exactly 1 health per hit event
* Player does not instantly lose all health from a single overlap
* Damage cooldown works reliably

---

## Task 181 – Player Death Trigger

**Status:** DONE

### Objective

End the run when player health reaches zero.

### Requirements

* When `current_health <= 0`:

  * trigger GAME_OVER state

* Ensure:

  * gameplay stops
  * no further damage processing occurs
  * transition is clean and consistent

### Acceptance Criteria

* Player death reliably triggers GAME_OVER
* No negative health values persist
* No state corruption after death

---

## Task 182 – Lollipop Health UI (Display System)

**Status:** DONE

### Objective

Represent player health visually using lollipop icons.

### Requirements

* Display up to 3 lollipop icons on screen

* Each lollipop represents 1 health

* Layout:

  * top-left or top-right of screen
  * consistent spacing

* Use:

  * simple shapes OR placeholder sprite initially

### Acceptance Criteria

* Player health is clearly visible via lollipops
* UI updates immediately when health changes
* Icons are readable during gameplay

---

## Task 183 – Health Loss Feedback (Visual Juice)

**Status:** DONE

### Objective

Provide clear feedback when the player takes damage.

### Requirements

* Add one or more effects:

  * player flash (red/white)
  * brief screen shake
  * small confetti burst (negative tone)
  * lollipop icon briefly animates or disappears

* Keep effects short and non-intrusive

### Acceptance Criteria

* Player can clearly tell when damage occurs
* Feedback feels responsive and satisfying
* Effects do not obscure gameplay

---

## Task 184 – Invulnerability Feedback (Damage Cooldown Indicator)

**Status:** DONE

### Objective

Visually indicate when the player is temporarily invulnerable.

### Requirements

* During damage cooldown:

  * slight flicker OR
  * reduced opacity OR
  * color shift

* Ensure effect ends cleanly after cooldown

### Acceptance Criteria

* Player can visually identify invulnerability window
* No confusion about when damage can occur again
* Effect is subtle but noticeable

---

## Task 185 – Health Bounds & Safety Checks

**Status:** DONE

### Objective

Ensure health system remains stable and bounded.

### Requirements

* Clamp health:

  * minimum: 0
  * maximum: `max_health`

* Prevent:

  * negative values
  * overflow beyond max

* Ensure all systems respect these limits

### Acceptance Criteria

* Health values always remain within valid bounds
* No edge-case bugs with repeated damage
* System behaves consistently under stress

---

## Task 186 – Health System Integration with Existing Systems

**Status:** DONE

### Objective

Ensure health system works correctly with all enemy types and game states.

### Requirements

* Validate interactions with:

  * balloons
  * piñatas
  * sprayers
  * streamer snakes
  * bosses

* Ensure:

  * damage applies consistently
  * invulnerability applies globally
  * no duplicate damage sources conflict

### Acceptance Criteria

* All enemy types correctly reduce health
* No double-hit or missed-hit inconsistencies
* System behaves predictably across gameplay scenarios

---

## Task 187 – Lollipop Asset Integration (Optional Upgrade)

**Status:** DONE

### Objective

Replace placeholder health indicators with themed lollipop visuals.

### Requirements

* Add lollipop sprite(s) to assets

* Support:

  * full (active health)
  * empty (lost health) OR hidden

* Maintain visual clarity at gameplay scale

### Acceptance Criteria

* Lollipop visuals are clear and on-theme
* UI feels cohesive with game aesthetic
* Assets integrate cleanly into UI system

---

## Task 188 – Health Balance Pass (3 HP Tuning)

**Status:** DONE

### Objective

Tune gameplay around low-health, high-tension design.

### Requirements

* Validate:

  * how often player gets hit
  * fairness of enemy collisions
  * usefulness of invulnerability window

* Adjust if needed:

  * hitbox size
  * damage cooldown duration
  * enemy contact frequency

### Acceptance Criteria

* 3 HP feels challenging but fair
* Deaths feel deserved, not random
* Health system supports fast, replayable runs

---

# Execution Rules for Agents

For each task:

1. Read `GAME_VISION.md` and `AGENTS.md`
2. Propose a plan BEFORE coding
3. List files to create/modify
4. Implement only the current task
5. Verify:
   - run the main game
   - check for errors
6. Summarize changes clearly

---

## Notes

- Do NOT skip tasks
- Do NOT expand scope
- Keep implementations simple
- Reuse the shared party animal system
- Prioritize readability, cohesion, and low-friction extensibility
- Do not introduce gameplay stat differences unless explicitly planned later
