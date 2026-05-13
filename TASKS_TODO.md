# TASKS.md

## Project Phase: Boss Expansion — Aeolus, Keeper of Winds

---

## Task 1: Create Boss Design Specification

### Objective

Define Aeolus as a memorable first boss with clear identity, mechanics, and progression role.

### Requirements

Create `BOSS_AEOLUS.md`

Include:

**Lore Identity**

* Title: *Aeolus, Keeper of Winds*
* First lieutenant of Helios
* Mythic force corrupted by Helios’ endless inflation
* Embodiment of wind, pressure, and chaotic uplift

**Theme**

* wind
* storms
* pressure
* forced movement
* airborne chaos
* balloon manipulation

**Visual Identity**
Design Aeolus as:

* massive ornate balloon construct
* unmistakable boss silhouette
* whimsical but threatening
* mythic party aesthetic

Visual concepts:

* central mask / face core
* balloon cloud body
* streamer tendrils
* party blower / whistle motif
* floating helium canisters
* glowing pressure core

**Gameplay Identity**
Aeolus should:

* control player movement
* dominate space
* punish static positioning
* create escalating battlefield chaos

**Fight Structure**
Define:

* Phase 1
* Phase 2
* Enrage / final phase

### Acceptance Criteria

* Boss spec exists
* Fight identity clearly differs from normal enemies

---

## Task 2: Implement Boss Encounter Framework

### Objective

Create reusable boss encounter infrastructure.

### Requirements

Create:
`boss_manager.py`

Responsibilities:

* encounter lifecycle
* boss registration
* spawn triggers
* active encounter state
* victory cleanup
* failure cleanup

Behavior:

* trigger boss spawn on timer / milestone
* pause normal escalation
* optionally reduce regular enemy density
* manage intro / active / defeated states

### Acceptance Criteria

* Boss encounters can be triggered reliably
* Existing game loop remains stable
* Framework supports future bosses

---

## Task 3: Implement Aeolus Base Boss Entity

### Objective

Create the core Aeolus boss entity.

### Requirements

Create:
`entities/bosses/aeolus.py`

Implement:

* health pool
* movement
* collision
* damage handling
* death behavior
* optional invulnerability states

Behavior:

* slow floating motion
* intentional repositioning
* prefers strategic distance from player
* visible “thinking” movement rather than random drift

### Acceptance Criteria

* Aeolus spawns
* Moves intentionally
* Can take damage
* Can be defeated

---

## Task 4: Implement Wind Pressure Signature Attack

### Objective

Create Aeolus’ defining attack.

### Requirements

Attack concept:
Aeolus unleashes directional wind pressure.

Effects:

* pushes player
* disrupts movement
* creates positional danger
* punishes careless standing still

Implementation ideas:

* telegraphed cone blast
* sweeping gust attack
* directional pressure wave

Configurable:

* cooldown
* force
* range
* duration
* telegraph timing

### Acceptance Criteria

* Wind attack functions reliably
* Telegraph is readable
* Attack feels unique

---

## Task 5: Implement Balloon Summon Attack

### Objective

Give Aeolus battlefield control via minions.

### Requirements

Attack concept:
Aeolus inflates reinforcements mid-fight.

Behavior:

* summon themed balloon enemies
* configurable summon count
* cooldown controlled
* integrate with existing enemy systems

Visual ideas:

* inflation effect
* pressure pulse
* balloon pop materialization

### Acceptance Criteria

* Summons spawn correctly
* Summoned enemies behave normally
* Fight pressure increases appropriately

---

## Task 6: Implement Storm Ring Hazard

### Objective

Create area denial mechanics.

### Requirements

Attack concept:
Aeolus creates rotating wind / balloon hazards.

Behavior:

* orbit around boss
* damage on contact
* create movement pressure
* deny close-range camping

Visual options:

* spinning mini balloons
* wind blades
* confetti vortex fragments

### Acceptance Criteria

* Hazard rotates correctly
* Collision works
* Performance remains stable

---

## Task 7: Implement Phase Transition System

### Objective

Create escalating boss phases.

### Requirements

Health threshold triggers:

* 70%
* 35%

Transition behavior:

* brief invulnerability
* visual phase shift
* dramatic feedback
* attack pattern escalation

Examples:

**Phase 2**

* faster wind attacks
* increased summon frequency
* larger hazard pressure

**Final Phase**

* aggressive repositioning
* shorter cooldowns
* overlapping attack patterns
* more chaotic movement pressure

### Acceptance Criteria

* Transitions trigger reliably
* Fight escalation is clearly visible

---

## Task 8: Add Boss UI

### Objective

Improve encounter readability.

### Requirements

Add:

* boss health bar
* boss nameplate
* intro title card
* optional phase indicator

Display:
**AEOLUS, KEEPER OF WINDS**

### Acceptance Criteria

* UI appears during fight
* UI clears after encounter
* Presentation feels polished

---

## Task 9: Add Boss Intro Event

### Objective

Make boss arrival memorable.

### Requirements

Create encounter intro sequence:

* spawn pause
* dramatic entrance
* storm visual burst
* balloon swirl materialization
* optional slow-motion emphasis
* sound effect hooks

Goal:
Boss should feel like an event.

### Acceptance Criteria

* Intro triggers correctly
* No gameplay lockups
* Entrance feels impactful

---

## Task 10: Add Boss Rewards

### Objective

Make victory meaningful.

### Requirements

On defeat:
drop one or more:

* large XP burst
* mythic collectible
* weapon evolution material
* progression currency
* unlock token

Optional first-clear rewards:

* character unlock
* permanent upgrade
* new weapon availability

### Acceptance Criteria

* Reward always granted
* Reward feels significant

---

## Task 11: Add Placeholder Boss Art

### Objective

Support gameplay iteration before final art pass.

### Requirements

Create placeholder visuals:

* large readable silhouette
* unique color palette
* obvious attack visuals
* clear boss readability

### Acceptance Criteria

* Boss is visually distinguishable
* Placeholder supports testing

---

## Task 12: Balance First Boss Experience

### Objective

Tune Aeolus into a fair but memorable first boss.

### Requirements

Tune:

* health
* damage
* movement speed
* summon density
* attack cooldowns
* telegraph timing
* phase thresholds

Design goals:
Player should learn:

* movement matters
* spacing matters
* telegraphs can be read
* bosses escalate
* survival requires adaptation

Avoid:

* stat sponge feel
* unfair burst damage
* unreadable chaos

### Acceptance Criteria

* Fight feels challenging but fair
* First clear is achievable
* Boss feels memorable
