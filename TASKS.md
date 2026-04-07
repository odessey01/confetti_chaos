# TASKS.md

## Project Phase: v1 Vertical Slice

Goal: Deliver a minimal, playable game loop that can be launched, played, failed, and restarted.

---

## Task 34 – Enemy Snapshot Persistence on Level Transition

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

## Task 39 – Settings System Foundation

**Status:** DONE

### Objective

Create a centralized system to manage game settings.

### Requirements

* Create a settings module (e.g., `systems/settings.py`)

* Store settings such as:

  * music_enabled (bool)
  * selected_start_level (int)

* Provide:

  * load settings from file
  * save settings to file
  * default fallback values

* Use simple format (JSON recommended)

### Acceptance Criteria

* Settings load on game start
* Settings persist between sessions
* Missing or corrupt file does not crash the game

---

## Task 40 – Pause Menu Overlay

**Status:** DONE

### Objective

Add an interactive pause menu with selectable options.

### Requirements

* Trigger pause with key (Esc or P)

* Freeze gameplay updates while paused

* Display overlay with options:

  * Resume
  * Restart
  * Toggle Music
  * Quit to Menu

* Basic navigation:

  * keyboard up/down
  * confirm selection

### Acceptance Criteria

* Gameplay fully pauses (no movement/spawn updates)
* Menu is responsive and readable
* Resume returns to exact prior state

---

## Task 41 – Start Menu Enhancements

**Status:** DONE

### Objective

Expand main menu to include configurable options.

### Requirements

* Add menu options:

  * Start Game
  * Level Select
  * Toggle Music
  * Quit

* Show current setting values (e.g., Music: ON/OFF)

### Acceptance Criteria

* Menu displays options clearly
* User can navigate and select options
* Selected settings reflect immediately

---

## Task 42 – Level Select Feature

**Status:** DONE

### Objective

Allow player to choose starting level.

### Requirements

* Add level selection UI:

  * simple increment/decrement or list

* Apply selected level when starting game

* Clamp values to valid range

* Integrate with progression system

### Acceptance Criteria

* Player can start at selected level
* Game initializes correctly at that level
* No progression bugs or crashes

---

## Task 43 – Music Toggle Integration

**Status:** DONE

### Objective

Control background music through settings.

### Requirements

* Add background music system (basic loop)

* Respect `music_enabled` setting:

  * do not play if disabled
  * stop/start when toggled

* Ensure:

  * no crashes if audio missing
  * no overlapping tracks

### Acceptance Criteria

* Music toggles correctly from menus
* Setting persists across sessions
* Audio behavior is stable and predictable

## Task 44 – Audio System Foundation

**Status:** TODO

### Objective

Create a centralized audio system for music, sound effects, and ambient loops.

### Requirements

* Add an audio manager module

* Support separate channels or categories for:

  * sound effects
  * music
  * ambient audio

* Provide simple methods such as:

  * play_sfx(name)
  * play_music(track)
  * stop_music()
  * play_ambient(track)
  * stop_ambient()

* Integrate with existing settings:

  * music enabled
  * future sound enabled / volume controls

* Fail gracefully if an audio asset is missing

### Acceptance Criteria

* Audio playback is controlled from one system
* Missing files do not crash the game
* Music, ambience, and SFX can be managed independently

---

## Task 45 – Core Gameplay Sound Effects

**Status:** TODO

### Objective

Add essential gameplay sound effects to improve feedback and responsiveness.

### Requirements

* Add sound effects for at least:

  * player weapon fire
  * balloon hit
  * balloon pop / kill
  * player damage or death
  * level transition

* Ensure sounds are short, readable, and not overly harsh

* Avoid excessive overlap or distortion during heavy action

### Acceptance Criteria

* Core gameplay events all have clear sound feedback
* Sounds trigger reliably at the correct moments
* Repeated gameplay actions do not produce broken or overwhelming audio

---

## Task 46 – Menu & UI Audio

**Status:** TODO

### Objective

Add audio feedback for menus and interface interactions.

### Requirements

* Add sounds for:

  * menu navigation
  * selection / confirm
  * back / cancel
  * pause and resume
  * settings toggle

* Keep UI sounds subtle and distinct from combat audio

### Acceptance Criteria

* Menu interactions feel more responsive
* UI sounds are clear but not distracting
* Menu audio remains consistent across start, pause, and game over flows

---

## Task 47 – Ambient Music System

**Status:** TODO

### Objective

Introduce background music that supports the tone of gameplay.

### Requirements

* Add looping music playback for gameplay

* Support at least:

  * main menu music
  * gameplay music
  * boss or milestone music placeholder

* Music should transition cleanly between states

* Respect music enabled setting at all times

### Acceptance Criteria

* Music plays in the correct game states
* Music does not overlap incorrectly across transitions
* Toggling music on/off works reliably during runtime

---

## Task 48 – Ambient Sound Layer

**Status:** TODO

### Objective

Add environmental ambience to give the game more atmosphere.

### Requirements

* Add a lightweight ambient layer for gameplay, such as:

  * wind
  * soft room tone
  * subtle floating/party atmosphere
  * tonal background texture

* Ambient layer should sit underneath music and SFX

* Allow ambient audio to be enabled/disabled through the audio system

### Acceptance Criteria

* Gameplay feels more alive and immersive
* Ambient audio does not interfere with core gameplay sounds
* Ambient layer can be started/stopped cleanly with game state changes

---

## Task 49 – Audio Mixing & Volume Controls

**Status:** TODO

### Objective

Make the audio suite controllable and balanced.

### Requirements

* Add separate volume settings for:

  * master volume
  * music volume
  * SFX volume
  * ambient volume

* Persist volume settings between sessions

* Apply settings dynamically without restart if possible

### Acceptance Criteria

* Volume controls affect the correct audio categories
* Settings persist across sessions
* Audio balance is noticeably improved during playtesting

---

## Task 50 – Boss & Special Event Audio Pass

**Status:** TODO

### Objective

Create more impactful sound design for boss fights and milestone events.

### Requirements

* Add distinct audio for:

  * boss spawn
  * boss hit
  * boss defeat
  * milestone / level clear
  * enhanced confetti celebration

* Boss audio should feel bigger and more dramatic than standard enemy sounds

### Acceptance Criteria

* Boss encounters sound distinct from normal gameplay
* Milestone events feel more rewarding
* Special event audio enhances excitement without overwhelming the mix

---

## Task 51 – Audio Asset Organization & Fallback Rules

**Status:** TODO

### Objective

Keep audio assets maintainable and safe for iteration.

### Requirements

* Organize assets into folders such as:

  * assets/audio/sfx/
  * assets/audio/music/
  * assets/audio/ambient/

* Add a consistent naming convention

* Define fallback behavior when:

  * a sound is missing
  * a track fails to load
  * audio device is unavailable

### Acceptance Criteria

* Audio assets are easy to find and maintain
* Missing or broken files do not disrupt gameplay
* Audio system remains stable in partial-content states

---

## Task 52 – Audio Polish & Repetition Control

**Status:** TODO

### Objective

Reduce fatigue and improve long-session listening quality.

### Requirements

* Add basic protections against repetitive or harsh playback:

  * slight random pitch or volume variation where supported
  * cooldown on repeated UI sounds
  * multiple variants for common sounds if available

* Review high-frequency sounds such as:

  * weapon fire
  * balloon pops
  * menu movement

### Acceptance Criteria

* Frequently repeated sounds feel less fatiguing
* Audio remains pleasant during extended play
* Repetition control does not break timing or clarity


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
