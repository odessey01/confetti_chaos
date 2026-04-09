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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

**Status:** DONE

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

--- 

## Task 53 – Boss Core Behavior (Chase System)

**Status:** DONE

### Objective

Give boss balloons a distinct presence through active pursuit behavior.

### Requirements

* Implement chase logic:

  * boss moves toward player position
  * slower, more deliberate movement than normal enemies
  * smooth tracking (no jitter)

* Add slight variation:

  * delayed reaction OR
  * easing/acceleration toward player

* Ensure boss movement is readable and avoid instant direction snapping

### Acceptance Criteria

* Boss consistently tracks player
* Movement feels intentional, not erratic
* Player can understand and react to boss behavior

---

## Task 54 – Boss Health System (Multi-Hit Combat)

**Status:** DONE

### Objective

Make bosses durable and require sustained interaction.

### Requirements

* Add health system to boss:

  * configurable max HP
  * damage per hit from player weapon

* Add visual feedback for damage:

  * flash
  * slight size change or wobble

* Prevent rapid duplicate hit registration

### Acceptance Criteria

* Boss requires multiple hits to defeat
* Damage feedback is visible and clear
* No double-counting or missed hits

---

## Task 55 – Boss Attack Patterns (Surprise Effects)

**Status:** DONE

### Objective

Introduce simple but varied boss abilities to create dynamic encounters.

### Requirements

* Implement at least 2–3 boss effects, such as:

  * **Burst Spawn**: releases smaller balloons periodically
  * **Speed Surge**: temporary increase in movement speed
  * **Directional Charge**: quick movement toward player
  * **Area Pressure**: temporarily increases spawn rate nearby

* Trigger effects:

  * on timer OR
  * on damage thresholds

* Keep each effect simple and readable

### Acceptance Criteria

* Boss uses abilities during encounter
* Effects are noticeable but fair
* Player can adapt and respond to each behavior

---

## Task 56 – Boss Phase System (Escalation)

**Status:** DONE

### Objective

Make boss fights evolve as the player progresses through them.

### Requirements

* Divide boss health into phases (e.g., 2–3 stages)

* On phase change:

  * increase aggression OR
  * unlock new behavior OR
  * modify movement speed

* Add clear phase transition feedback:

  * visual cue
  * brief pause or effect

### Acceptance Criteria

* Boss behavior changes during fight
* Phase transitions are noticeable
* Difficulty increases without becoming chaotic

---

## Task 57 – Boss Balance & Fairness Pass

**Status:** DONE

### Objective

Ensure boss encounters are challenging but not frustrating.

### Requirements

* Tune:

  * boss speed vs player speed
  * attack frequency
  * health values
  * support enemy spawns

* Ensure:

  * player always has space to maneuver
  * no unavoidable damage scenarios
  * encounter length is reasonable

* Validate across multiple levels and flavors

### Acceptance Criteria

* Boss fights feel fair and winnable
* Difficulty aligns with progression level
* No “unavoidable death” situations occur

---

## Task 58 – Boss Variety Hooks (Extensibility)

**Status:** DONE

### Objective

Prepare the system to support multiple boss types in the future.

### Requirements

* Structure boss logic so behaviors can be:

  * swapped
  * combined
  * extended

* Support configuration such as:

  * different health pools
  * different ability sets
  * flavor-specific bosses

* Avoid hardcoding a single boss implementation

### Acceptance Criteria

* Boss system is modular and extendable
* New boss variants can be added with minimal changes
* Existing boss logic remains stable

--- 

## Task 59 – Piñata Enemy Type (Base Implementation)

**Status:** DONE

### Objective

Introduce a new enemy type distinct from balloons.

### Requirements

* Create piñata enemy:

  * visually distinct (larger, more angular or textured)
  * different color palette from balloons

* Movement:

  * slower than balloons
  * more deliberate or slightly drifting

* Integrate into existing enemy system and spawn system

### Acceptance Criteria

* Piñata enemies spawn correctly
* They are clearly distinguishable from balloons
* Movement feels heavier and intentional

---

## Task 60 – Piñata Health & Durability

**Status:** DONE

### Objective

Make piñata enemies require multiple hits.

### Requirements

* Assign higher health than balloons

* Add damage feedback:

  * wobble
  * crack/flash effect
  * slight visual degradation (optional)

* Prevent rapid duplicate hits

### Acceptance Criteria

* Piñatas take multiple hits to destroy
* Damage feedback is visible and satisfying
* Combat interaction feels intentional

---

## Task 61 – Piñata Break Effect (Enhanced Confetti)

**Status:** DONE

### Objective

Make piñata destruction a rewarding visual event.

### Requirements

* On destruction:

  * spawn a larger confetti burst than normal balloons
  * use varied colors and spread

* Optional:

  * slightly longer particle lifetime
  * directional burst effect

### Acceptance Criteria

* Piñata destruction feels more rewarding than balloons
* Confetti effect is clearly elevated but not overwhelming
* Performance remains stable

---

## Task 62 – Piñata Surprise Behavior

**Status:** DONE

### Objective

Add a unique twist to piñata enemies.

### Requirements

Implement at least one:

* **Split Effect**: releases smaller balloons on destruction

* **Delayed Burst**: slight delay before breaking into confetti

* **Triggered Reaction**: briefly speeds up when hit

* Keep behavior simple and readable

### Acceptance Criteria

* Piñatas behave differently from balloons
* Behavior adds interest without confusion
* Player can understand cause and effect

---

## Task 63 – Spawn Integration & Balance

**Status:** DONE

### Objective

Integrate piñatas into level progression and spawn systems.

### Requirements

* Add piñatas to spawn pool:

  * low frequency initially
  * increase presence at higher levels

* Integrate with:

  * tier system
  * flavor system
  * boss levels (optional limited inclusion)

* Ensure:

  * they do not overwhelm gameplay
  * they feel like special targets

### Acceptance Criteria

* Piñatas appear at appropriate frequency
* They enhance gameplay variety
* Difficulty remains fair and readable

---

## Task 64 – Piñata Tier Variants (Optional Extension)

**Status:** DONE

### Objective

Allow piñatas to evolve with progression.

### Requirements

* Support tier-based variations such as:

  * higher health
  * stronger break effects
  * additional mini-enemy spawns

* Keep implementation lightweight and data-driven

### Acceptance Criteria

* Piñatas scale naturally with progression
* Variants remain recognizable
* System integrates cleanly with existing tier logic

## Task 65 – Confetti Sprayer Enemy (Base Implementation)

**Status:** DONE

### Objective

Introduce a new enemy type that creates directional pressure through confetti spray attacks.

### Requirements

* Create a new enemy type: **Confetti Sprayer**

* Make it visually distinct from balloons and piñatas

* Suggested visual traits:

  * party cannon / cone / tube-like body
  * brighter accent colors
  * readable facing direction

* Integrate into existing enemy and spawn systems

### Acceptance Criteria

* Confetti Sprayers spawn correctly
* They are clearly distinguishable from other enemy types
* Their orientation or facing direction is readable during gameplay

---

## Task 66 – Sprayer Movement & Positioning Behavior

**Status:** DONE

### Objective

Give Confetti Sprayers movement that supports their attack role.

### Requirements

* Implement movement behavior that is different from standard balloons

* Suggested behavior:

  * slow drift
  * short repositioning movement
  * partial tracking toward player without full chase

* Sprayers should create space for attacks rather than constantly collide with player

* Avoid overly erratic motion

### Acceptance Criteria

* Sprayers move in a stable and readable way
* Their movement supports attack setup
* They feel different from chase-focused enemies

---

## Task 67 – Confetti Spray Attack System

**Status:** DONE

### Objective

Allow Confetti Sprayers to fire directional confetti bursts.

### Requirements

* Add a spray attack that emits particles or projectiles in:

  * a cone
  * a short arc
  * or a directional line

* Attack should:

  * trigger on timer or cooldown
  * respect enemy facing direction
  * have visible startup or tell before firing

* Keep implementation lightweight and readable

### Acceptance Criteria

* Sprayers fire confetti attacks reliably
* Attack direction is understandable to the player
* Startup and release feel fair and visible

---

## Task 68 – Confetti Spray Hazard Interaction

**Status:** DONE

### Objective

Define how confetti spray affects gameplay and player danger.

### Requirements

* Determine how spray causes pressure, such as:

  * direct player damage
  * temporary hazard zone
  * short-lived damaging particles

* Add collision or overlap handling between spray effect and player

* Ensure spray lifetime is limited and cleaned up correctly

### Acceptance Criteria

* Spray creates a meaningful gameplay threat
* Hazard behavior is consistent and fair
* Spray effects do not linger incorrectly after expiration

---

## Task 69 – Telegraphing, Cooldowns, and Fairness

**Status:** DONE

### Objective

Make Confetti Sprayer attacks readable and avoid cheap hits.

### Requirements

* Add telegraphing before spray attack, such as:

  * brief pause
  * body flash
  * facing lock
  * charge animation or color change

* Add attack cooldown between sprays

* Prevent overlapping attack spam from a single enemy

### Acceptance Criteria

* Player can recognize when a spray attack is about to happen
* Confetti Sprayers feel dangerous but fair
* Attack cadence is readable and tunable

---

## Task 70 – Spawn Integration & Difficulty Scaling

**Status:** DONE

### Objective

Integrate Confetti Sprayers into progression, tiers, and level flavors.

### Requirements

* Add Confetti Sprayers to the spawn pool

* Control when they appear:

  * rare in early levels
  * more common later
  * adjustable by flavor/tier

* Ensure only newly spawned sprayers reflect new level/tier values

* Support mixed-tier progression with existing spawn rules

### Acceptance Criteria

* Sprayers appear at appropriate stages of progression
* Their frequency scales without overwhelming the player
* Spawn behavior remains consistent with current tier system

---

## Task 71 – Flavor Integration for Confetti Sprayers

**Status:** DONE

### Objective

Make Confetti Sprayers interact meaningfully with level flavor rules.

### Requirements

* Define how sprayers behave under different level flavors, for example:

  * **Standard**: balanced spray timing
  * **Swarm**: fewer sprayers, lighter spray pressure
  * **Hunters**: more directed, accurate spray behavior
  * **Storm**: denser bursts or faster cooldowns

* Keep flavor modifications data-driven and easy to tune

### Acceptance Criteria

* Sprayers feel different across flavors without becoming unpredictable
* Flavor-specific behavior is noticeable in gameplay
* Balance remains fair and readable

---

## Task 72 – Confetti Sprayer Visual & Audio Feedback

**Status:** DONE

### Objective

Improve clarity and satisfaction of Confetti Sprayer interactions.

### Requirements

* Add visual feedback for:

  * spray charge-up
  * spray release
  * taking damage
  * destruction

* Add audio hooks if audio system exists:

  * spray burst sound
  * charge-up sound
  * destruction sound

* Keep effects lightweight and performance-friendly

### Acceptance Criteria

* Sprayer attacks are easier to read
* Destroying a sprayer feels satisfying
* Feedback improves clarity without clutter

---

## Task 73 – Confetti Sprayer Balance & Playtest Pass

**Status:** DONE

### Objective

Tune Confetti Sprayers so they add spatial challenge without dominating gameplay.

### Requirements

* Tune:

  * movement speed
  * attack frequency
  * spray width
  * spray lifetime
  * spawn frequency

* Validate interaction with:

  * balloons
  * piñatas
  * bosses
  * level transitions
  * mixed-tier spawns

* Ensure multiple sprayers on screen remain manageable

### Acceptance Criteria

* Sprayers add a new tactical challenge
* They do not create unavoidable damage situations
* Gameplay remains fast, readable, and fun


## Task 74 – Background Rendering System

**Status:** DONE

### Objective

Replace the black screen with a simple, extensible background system.

### Requirements

* Create a background rendering layer

* Support:

  * solid color
  * gradient (preferred)
  * optional texture overlay

* Ensure background renders behind all gameplay elements

* Keep implementation lightweight

### Acceptance Criteria

* Game no longer uses a plain black background
* Background renders consistently without affecting performance
* System is easy to extend later

---

## Task 75 – Themed Background (Initial Style)

**Status:** DONE

### Objective

Define a visual identity for the game environment.

### Requirements

* Implement a base theme, such as:

  * soft gradient (dark teal → muted blue → dusk tone)
  * low-contrast palette

* Add subtle variation:

  * noise texture
  * light color shifts

* Ensure:

  * enemies and projectiles remain highly visible
  * contrast is preserved

### Acceptance Criteria

* Background has a cohesive visual style
* Gameplay elements remain clear and readable
* No visual clutter

---

## Task 76 – Ambient Background Elements

**Status:** DONE

### Objective

Add subtle motion to make the world feel alive.

### Requirements

* Add lightweight ambient elements such as:

  * slow drifting confetti pieces
  * floating particles
  * soft shapes or blobs

* Movement should be:

  * slow
  * non-interactive
  * low opacity

### Acceptance Criteria

* Background feels dynamic but not distracting
* Elements do not interfere with gameplay readability
* Performance remains stable

---

## Task 77 – Depth Layering (Parallax Lite)

**Status:** DONE

### Objective

Create a sense of depth without adding complexity.

### Requirements

* Introduce 2–3 background layers:

  * base layer (static)
  * mid layer (slow movement)
  * foreground ambient layer (slightly faster)

* Optional:

  * subtle parallax based on player movement

* Keep math simple and efficient

### Acceptance Criteria

* Scene has a sense of depth
* Movement feels smooth and subtle
* No impact on gameplay performance

---

## Task 78 – Level Flavor Visual Integration

**Status:** DONE

### Objective

Tie environment visuals to level flavor system.

### Requirements

* Adjust background based on level flavor:

  * **Standard** → neutral tones
  * **Swarm** → slightly brighter, busier particles
  * **Hunters** → darker, higher contrast
  * **Storm** → more active background motion or color shifts

* Keep changes subtle, not overwhelming

### Acceptance Criteria

* Player can feel a difference between flavors visually
* Visual changes reinforce gameplay identity
* No loss of readability

---

## Task 79 – Background Performance & Cleanup

**Status:** DONE

### Objective

Ensure environment system remains efficient and stable.

### Requirements

* Limit number of background elements
* Reuse or pool particles where possible
* Ensure:

  * no memory leaks
  * no excessive draw calls
  * no frame drops

### Acceptance Criteria

* Background system has negligible performance impact
* No buildup of unused objects over time
* System remains stable during long play sessions

## Task 80 – Run Progression System Foundation

**Status:** DONE

### Objective

Create the core progression framework for leveling up during a run.

### Requirements

* Add player progression values for the current run:

  * current level
  * current XP
  * XP required for next level

* Define a simple XP growth formula

* Reset progression values correctly at the start of a new run

* Keep this system separate from stage/level progression

### Acceptance Criteria

* Player can gain XP during a run
* Run level increases when XP threshold is reached
* Progression resets cleanly on restart

---

## Task 81 – XP Source Integration

**Status:** DONE

### Objective

Define how the player earns XP during gameplay.

### Requirements

* Award XP from gameplay events such as:

  * enemy kills
  * piñata kills
  * boss defeat bonus

* Allow different enemy types to grant different XP values

* Keep XP values configurable and easy to tune

### Acceptance Criteria

* XP is awarded reliably on qualifying events
* Different enemy types can give different XP rewards
* XP gain feels consistent and visible in normal play

---

## Task 82 – XP Bar & Run Level UI

**Status:** DONE

### Objective

Make progression visible and readable during gameplay.

### Requirements

* Add UI elements for:

  * current run level
  * XP bar showing progress toward next level

* Position UI so it does not interfere with score, health, or gameplay readability

* Update UI in real time as XP is gained

### Acceptance Criteria

* Player can clearly see current run level
* XP bar updates immediately and accurately
* UI remains readable during active gameplay

---

## Task 83 – Level-Up Trigger & Game Pause Flow

**Status:** DONE

### Objective

Pause active gameplay and enter an upgrade selection state when the player levels up.

### Requirements

* When XP threshold is met:

  * trigger level-up event
  * pause or freeze gameplay updates
  * open upgrade selection overlay

* Ensure the level-up state is distinct from pause/menu states

* Prevent enemy movement, attacks, and spawn updates while choosing an upgrade

### Acceptance Criteria

* Level-up reliably interrupts gameplay
* Upgrade selection appears cleanly without state corruption
* Gameplay resumes correctly after choice is made

---

## Task 84 – Upgrade Data Model

**Status:** DONE

### Objective

Create a clean, data-driven structure for run upgrades.

### Requirements

* Define upgrade data including:

  * id
  * name
  * description
  * category
  * effect values
  * optional max stack or cap

* Keep upgrade definitions centralized and easy to extend

* Support repeatable and non-repeatable upgrades

### Acceptance Criteria

* Upgrades are defined in one clear location
* New upgrades can be added without rewriting core logic
* Upgrade metadata is usable by both logic and UI

---

## Task 85 – Upgrade Selection System (Choose 1 of 3)

**Status:** DONE

### Objective

Present a set of upgrade choices to the player when leveling up.

### Requirements

* On level-up, show 3 upgrade choices
* Randomly select from valid upgrade pool
* Avoid invalid or duplicate choices where possible
* Allow keyboard/controller-friendly selection flow

### Acceptance Criteria

* Player is presented with 3 valid upgrade options
* Selection input is reliable and readable
* Upgrade choice closes the overlay and resumes gameplay

---

## Task 86 – Initial Upgrade Pool (Phase 1 Set)

**Status:** DONE

### Objective

Create the first small set of run upgrades.

### Requirements

* Add an initial upgrade pool of approximately 6–10 upgrades

* Focus on simple, high-clarity modifiers such as:

  * movement speed increase
  * fire rate increase
  * projectile speed increase
  * additional projectile
  * larger confetti burst radius
  * score gain bonus
  * enemy slow effect (light)
  * stronger projectile damage

* Keep effects simple and immediately noticeable

### Acceptance Criteria

* Upgrade pool is varied enough to support meaningful choice
* Each upgrade produces a noticeable gameplay effect
* No upgrade requires a large new subsystem to function

---

## Task 87 – Upgrade Application Logic

**Status:** DONE

### Objective

Apply chosen upgrades cleanly to active gameplay systems.

### Requirements

* Implement logic to apply upgrade effects to relevant systems:

  * player movement
  * weapon/projectiles
  * score systems
  * enemy interactions

* Ensure stacked upgrades behave correctly

* Prevent broken values or runaway effects through sensible caps where needed

### Acceptance Criteria

* Chosen upgrades immediately affect gameplay
* Stacking behavior is predictable and stable
* No upgrade causes crashes or invalid state

---

## Task 88 – Upgrade UI Presentation & Readability

**Status:** DONE

### Objective

Make upgrade choices understandable and appealing.

### Requirements

* Display for each upgrade:

  * name
  * short description
  * clear effect summary

* Highlight current selection

* Keep overlay visually clean and fast to read

* Maintain readability over the game background

### Acceptance Criteria

* Upgrade screen is easy to understand quickly
* Players can make a choice without confusion
* UI presentation supports repeated use during a run

---

## Task 89 – Duplicate Rules, Weighting, and Validity Filtering

**Status:** DONE

### Objective

Improve the quality of upgrade choice generation.

### Requirements

* Prevent choices that are:

  * invalid for current state
  * already capped
  * meaningless duplicates in the same choice set

* Add simple weighting support so some upgrades can be:

  * common
  * uncommon
  * situational

* Ensure the selection system still works when the pool becomes constrained

### Acceptance Criteria

* Upgrade choices remain useful across the run
* Capped or invalid upgrades do not appear unnecessarily
* Choice quality feels intentional rather than random

---

## Task 90 – Phase 1 Progression Balance Pass

**Status:** DONE

### Objective

Tune the first progression loop so leveling up feels rewarding and well-paced.

### Requirements

* Tune:

  * XP gain rates
  * XP thresholds
  * frequency of level-ups
  * strength of starting upgrades
  * upgrade stacking limits

* Validate progression across:

  * early run
  * mid run
  * boss encounters

### Acceptance Criteria

* Player levels up often enough to feel rewarded
* Upgrades create noticeable power growth without trivializing the run
* Progression pacing feels appropriate for a survivor-style game

## Task 91 – Streamer Snake Enemy (Base Implementation)

**Status:** DONE

### Objective

Introduce a ribbon-like enemy composed of a moving head and trailing body segments.

### Requirements

* Create a new enemy type: **Streamer Snake**

* Structure:

  * head (primary entity)
  * trailing segments (linked or generated positions)

* Visually distinct:

  * ribbon/streamer appearance
  * continuous or segmented body
  * bright, flowing colors

* Integrate into existing enemy system

### Acceptance Criteria

* Streamer Snake spawns correctly
* Head and body are visually connected
* Enemy is clearly distinguishable from other types

---

## Task 92 – Snake Movement & Path Tracking

**Status:** DONE

### Objective

Create smooth, flowing movement for the snake head and trailing segments.

### Requirements

* Head movement:

  * similar to balloon drift OR light chase behavior
  * smooth directional changes (no snapping)

* Body behavior:

  * follow previous positions of the head
  * maintain spacing between segments
  * create a natural trailing curve

* Avoid jitter and overlapping segments

### Acceptance Criteria

* Snake movement appears fluid and continuous
* Body follows head naturally
* Movement feels distinct from other enemies

---

## Task 93 – Body Collision & Hazard Behavior

**Status:** DONE

### Objective

Make the snake body a meaningful gameplay hazard.

### Requirements

* Define collision behavior:

  * player collision with head or body causes damage

* Ensure:

  * consistent hit detection across segments
  * no duplicate damage stacking per frame

* Optional:

  * head deals more damage than body (configurable)

### Acceptance Criteria

* Snake body acts as a continuous hazard
* Collisions are accurate and fair
* Player interaction is consistent and readable

---

## Task 94 – Tail Persistence & Fade System

**Status:** DONE

### Objective

Control how long the snake trail remains active.

### Requirements

* Define tail behavior:

  * fixed number of segments OR
  * time-based fade-out

* Ensure:

  * tail does not grow indefinitely
  * old segments are removed cleanly

* Optional:

  * slight fade or shrink effect on older segments

### Acceptance Criteria

* Tail length remains controlled and predictable
* Old segments are removed without artifacts
* Visual trail remains readable

---

## Task 95 – Snake Behavior Variants

**Status:** DONE

### Objective

Add variation to streamer snake behavior.

### Requirements

Implement at least one variant:

* **Wanderer**: slow drifting, long trailing tail

* **Tracker**: lightly follows player

* **Looper**: moves in curved or circular patterns

* Keep behavior simple and configurable

### Acceptance Criteria

* Snake variants feel different in gameplay
* Behavior differences are noticeable but readable
* Variants integrate with existing systems

---

## Task 96 – Spawn Integration & Tier Scaling

**Status:** DONE

### Objective

Integrate streamer snakes into progression and spawn systems.

### Requirements

* Add snakes to spawn pool:

  * introduced mid-progression
  * scaled frequency based on level/tier

* Support:

  * mixed-tier spawning
  * spawn-time attribute assignment

* Ensure only newly spawned snakes reflect new level/tier values

### Acceptance Criteria

* Snakes appear at appropriate difficulty stages
* Spawn frequency is balanced
* Integration does not disrupt existing enemy ecosystem

---

## Task 97 – Flavor System Integration

**Status:** DONE

### Objective

Make streamer snakes interact with level flavors.

### Requirements

* Define behavior adjustments per flavor:

  * **Standard**: balanced movement
  * **Swarm**: shorter snakes, more instances
  * **Hunters**: tighter tracking behavior
  * **Storm**: faster movement, denser trails

* Keep changes data-driven and tunable

### Acceptance Criteria

* Snakes behave differently across flavors
* Changes are noticeable but not chaotic
* Balance remains fair

---

## Task 98 – Visual & Feedback Polish

**Status:** DONE

### Objective

Enhance readability and visual appeal of streamer snakes.

### Requirements

* Add:

  * subtle color gradients along the body
  * motion smoothing or easing
  * destruction feedback (confetti burst or ribbon break)

* Ensure strong contrast against background

### Acceptance Criteria

* Snake visuals are clear and appealing
* Movement is easy to track visually
* Destruction feels satisfying

---

## Task 99 – Balance & Playtest Pass

**Status:** DONE

### Objective

Ensure streamer snakes add meaningful challenge without overwhelming gameplay.

### Requirements

* Tune:

  * movement speed
  * tail length
  * spawn frequency
  * collision behavior

* Validate interactions with:

  * balloons
  * piñatas
  * sprayers
  * bosses

* Ensure:

  * no unavoidable traps
  * player always has escape paths

### Acceptance Criteria

* Snakes add spatial challenge and pathing decisions
* Difficulty remains fair and readable
* Gameplay remains fast and fluid

# TASKS.md

## Project Phase: v1 Vertical Slice

Goal: Deliver a minimal, playable game loop that can be launched, played, failed, and restarted.

---

## Task 100 – Player Visual System Refactor

**Status:** DONE

### Objective

Separate player rendering from gameplay logic to support visual upgrades.

### Requirements

* Extract rendering logic from player movement/logic
* Create a dedicated player render function or module
* Ensure visuals can be swapped without affecting gameplay behavior

### Acceptance Criteria

* Player logic and rendering are decoupled
* Visual updates can be made independently of movement/combat systems
* No regression in gameplay behavior

---

## Task 101 – Party Animal Base Design (Shape Version)

**Status:** DONE

### Objective

Create a simple stuffed-animal-style player using shapes.

### Requirements

* Replace current player visual with:

  * rounded body (circle/oval)
  * two small ears
  * simple eyes
  * optional party hat

* Use clear color palette distinct from enemies

* Maintain strong contrast against background

### Acceptance Criteria

* Player visually reads as a character, not a placeholder
* Design is clean and recognizable at gameplay scale
* No impact to performance

---

## Task 102 – Directional Facing & Orientation

**Status:** DONE

### Objective

Make the player feel more alive through directional feedback.

### Requirements

* Player should visually respond to movement direction:

  * slight rotation OR
  * facing indicator (eyes, hat tilt, etc.)

* Avoid complex animation systems

* Keep transitions smooth

### Acceptance Criteria

* Player direction is visually readable
* Movement feels more responsive and expressive
* No jitter or snapping artifacts

---

## Task 103 – Movement Feedback (Juice)

**Status:** DONE

### Objective

Add subtle visual feedback to enhance player feel.

### Requirements

* Add lightweight effects such as:

  * slight squash/stretch on movement
  * tiny bounce or bob
  * subtle scaling on acceleration

* Keep effects minimal and performant

### Acceptance Criteria

* Player feels more responsive and alive
* Effects are noticeable but not distracting
* No performance degradation

---

## Task 104 – Player Color Variants System

**Status:** DONE

### Objective

Support multiple player styles for variation and future customization.

### Requirements

* Allow player visuals to support:

  * different colors
  * minor variations (ear shape, hat color)

* Structure system so variants can be easily added

### Acceptance Criteria

* Player color can be changed without code duplication
* Variants are visually distinct
* System is extensible for future skins

---

## Task 105 – Sprite Integration (Optional Upgrade Path)

**Status:** DONE

### Objective

Enable transition from shape-based visuals to sprite-based rendering.

### Requirements

* Add support for loading a player sprite
* Fallback to shape-based rendering if sprite is unavailable
* Ensure sprite aligns with player hitbox and movement

### Acceptance Criteria

* Sprite can replace shape-based player cleanly
* No gameplay logic depends on rendering method
* System supports future visual upgrades

---

## Task 106 – Player Visual Clarity & Contrast Pass

**Status:** DONE

### Objective

Ensure the player remains readable during chaotic gameplay.

### Requirements

* Validate visibility against:

  * background
  * confetti effects
  * enemy colors

* Adjust:

  * outline
  * brightness
  * contrast

* Ensure player is always easy to track

### Acceptance Criteria

* Player remains visible in all gameplay situations
* Visual clarity is maintained during high particle density
* No confusion between player and enemies

## Task 107 – Create `playerdemo.py` Sandbox Entry Point

**Status:** DONE

### Objective

Create a small standalone demo file for testing protagonist visual options outside the main game.

### Requirements

* Add a new file:

  * `src/playerdemo.py`

* The demo should:

  * open a window
  * render a neutral background
  * display one selected party animal character
  * allow clean exit

* Keep it independent from the main gameplay loop wherever practical

### Acceptance Criteria

* Running `python src/playerdemo.py` launches a dedicated player visual demo
* Demo runs without starting the full game
* File is simple and safe to iterate on

---

## Task 108 – Create Player Visual Variant Interface

**Status:** DONE

### Objective

Define a clean structure for multiple party animal visual options.

### Requirements

* Support multiple selectable player variants, such as:

  * bear
  * bunny
  * fox
  * cat
  * dog

* Each variant should define:

  * name
  * render method or sprite source
  * color palette
  * optional visual traits (ears, tail, hat, face layout)

* Keep visuals swappable without affecting gameplay logic

### Acceptance Criteria

* Variants are defined in one clear place
* New party animals can be added easily
* Demo can switch between variants without code duplication

---

## Task 109 – Add Variant Cycling Controls

**Status:** DONE

### Objective

Allow quick comparison of party animal options in the demo.

### Requirements

* Add controls to cycle through available variants:

  * left/right arrow keys OR A/D
  * optional number key shortcuts

* Display current selected variant name on screen

* Ensure switching is immediate and stable

### Acceptance Criteria

* User can move through all variants quickly
* Current variant name is always visible
* Switching does not require restarting the demo

---

## Task 110 – Add Basic Presentation Poses

**Status:** DONE

### Objective

Show each party animal in a more useful presentation state than a static sprite only.

### Requirements

* Support at least one or two simple visual states:

  * idle
  * move/facing preview

* Optional:

  * slight bounce
  * subtle turn
  * alternate facing direction

* Keep this lightweight and focused on visual evaluation

### Acceptance Criteria

* Variants can be viewed in a way that helps compare personality/readability
* Demo provides more useful feedback than a static still image
* Presentation remains simple and responsive

---

## Task 111 – Add Shared Demo Background & Scale Controls

**Status:** DONE

### Objective

Make visual comparisons more realistic and easier to judge.

### Requirements

* Add a simple reusable demo background:

  * soft neutral tone or gradient
  * non-distracting
  * good contrast for character visibility

* Add scale controls to enlarge/reduce the displayed character

* Optional:

  * toggle outline on/off
  * toggle shadow on/off

### Acceptance Criteria

* Character readability can be assessed against a representative background
* Scale can be adjusted during demo use
* Visual testing is more practical and informative

---

## Task 112 – Add Comparison Overlay Information

**Status:** DONE

### Objective

Make it easier to evaluate which party animal design works best.

### Requirements

* Display on-screen info for current variant:

  * name
  * primary colors
  * shape/style notes
  * optional status such as “shape-based” or “sprite-based”

* Keep overlay minimal and readable

### Acceptance Criteria

* Demo clearly communicates which option is being viewed
* Information supports visual decision-making
* Overlay does not clutter the screen

---

## Task 113 – Support Sprite-Based Variants

**Status:** DONE

### Objective

Allow the demo to preview actual sprite options instead of only shape-based designs.

### Requirements

* Add support for loading small player art assets if available
* Keep fallback support for placeholder or shape-based variants
* Ensure sprite rendering aligns correctly in the demo scene

### Acceptance Criteria

* Demo can show both code-drawn and sprite-based options
* Missing assets do not crash the demo
* Sprite-based previews are easy to compare

---

## Task 114 – Demo Reuse Readiness for Main Game Integration

**Status:** DONE

### Objective

Prepare the chosen player visual option to be moved cleanly into the main game.

### Requirements

* Keep demo code organized so selected variant rendering can be reused

* Separate:

  * variant definitions
  * demo controls
  * render logic

* Avoid demo-specific hacks in reusable rendering code

### Acceptance Criteria

* Chosen player variant can be integrated into the main game with minimal rework
* Demo remains a safe sandbox for future visual iteration
* Render logic is modular and reusable

## Task 115 – Add Player Demo Sprite Asset Support

**Status:** DONE

### Objective

Enable `playerdemo.py` to load external sprite assets for the teddy bear character.

### Requirements

* Load sprite image files for:

  * front
  * side
  * rear

* Store assets in a clear folder structure, for example:

  * `assets/images/player/bear/front.png`
  * `assets/images/player/bear/side.png`
  * `assets/images/player/bear/rear.png`

* Fail gracefully if an asset is missing

### Acceptance Criteria

* `playerdemo.py` loads the teddy bear sprite files successfully
* Missing files do not crash the demo unexpectedly
* Sprite asset paths are easy to update and reuse later

---

## Task 116 – Normalize Sprite Canvas and Display Scaling

**Status:** DONE

### Objective

Ensure all teddy bear directional sprites render at a consistent size and scale.

### Requirements

* Confirm all directional sprites use a consistent canvas size
* Add a shared display scale setting for the demo
* Render front, side, and rear sprites at the same apparent size
* Allow easy tuning of demo display size

### Acceptance Criteria

* Directional sprites render at consistent scale
* Switching directions does not cause visible size jumps
* Display size can be adjusted from one place

---

## Task 117 – Add Direction-to-Sprite Mapping

**Status:** DONE

### Objective

Map movement direction in `playerdemo.py` to the correct teddy bear sprite.

### Requirements

* Use:

  * front sprite for facing down
  * rear sprite for facing up
  * side sprite for facing right
  * horizontally flipped side sprite for facing left

* Keep the mapping logic separate from render code where practical

### Acceptance Criteria

* Demo shows the correct sprite for each facing direction
* Left-facing uses a clean flip of the side sprite
* Direction changes are immediate and stable

---

## Task 118 – Add Center-Bottom Anchor Alignment

**Status:** DONE

### Objective

Keep teddy bear sprites aligned consistently across all facing directions.

### Requirements

* Define a shared anchor point strategy:

  * center-bottom anchor recommended

* Render all sprites using the same anchor alignment rule

* Prevent visible jumping when switching between front, side, and rear sprites

### Acceptance Criteria

* Character remains visually grounded when direction changes
* No noticeable jitter between directional sprites
* Anchor logic is reusable for future player variants

---

## Task 119 – Add Hitbox Definition for Teddy Bear

**Status:** DONE

### Objective

Define a forgiving gameplay hitbox for the teddy bear character in the demo.

### Requirements

* Add a hitbox separate from sprite dimensions

* Recommended:

  * circle or rounded-body collision area
  * smaller than full sprite size

* Position hitbox based on body center, not ears or hat

* Keep hitbox values configurable

### Acceptance Criteria

* Hitbox is clearly defined and independent from sprite bounds
* Hitbox placement feels centered on the bear’s body
* Hitbox size is easy to tune

---

## Task 120 – Add Debug Overlay for Anchor and Hitbox

**Status:** DONE

### Objective

Make sprite alignment and collision setup easy to inspect inside the demo.

### Requirements

* Add a toggleable debug overlay

* Show:

  * anchor point
  * hitbox outline
  * optional sprite bounds

* Add a key to enable/disable debug view

### Acceptance Criteria

* Debug overlay can be toggled on and off
* Anchor and hitbox are clearly visible for inspection
* Overlay helps validate sprite alignment quickly

---

## Task 121 – Add Direction Preview Controls

**Status:** DONE

### Objective

Allow quick testing of teddy bear directional sprites in `playerdemo.py`.

### Requirements

* Add controls to preview facing directions:

  * up
  * down
  * left
  * right

* Optional:

  * idle mode
  * movement preview mode

* Keep controls simple and responsive

### Acceptance Criteria

* User can quickly switch between directional views
* All three source images can be tested in one session
* Direction preview is useful for alignment validation

---

## Task 122 – Add Scale and Offset Tuning Controls

**Status:** DONE

### Objective

Make it easy to fine-tune teddy bear sprite presentation in the demo.

### Requirements

* Add simple controls or constants for adjusting:

  * sprite scale
  * render offset
  * hitbox radius
  * hitbox vertical offset

* Keep these values easy to inspect and update

### Acceptance Criteria

* Sprite scale and offsets can be tuned without major code edits
* Demo supports quick iteration on alignment
* Changes are immediately visible during testing

---

## Task 123 – Add Variant Config Object for Reuse

**Status:** DONE

### Objective

Represent the teddy bear setup as a reusable player visual configuration.

### Requirements

* Create a config or data structure that contains:

  * sprite paths
  * display scale
  * anchor settings
  * hitbox settings

* Keep config separate from demo-specific input code

* Prepare structure for future reuse by bunny, fox, cat, etc.

### Acceptance Criteria

* Teddy bear visual settings are defined in one place
* Future party animal variants can reuse the same structure
* Demo logic stays clean and modular

---

## Task 124 – Validate Demo Reuse for Main Player Integration

**Status:** DONE

### Objective

Prepare the teddy bear visual setup to move cleanly from `playerdemo.py` into the main game.

### Requirements

* Separate reusable rendering/alignment logic from demo-only controls
* Avoid hardcoding demo assumptions into shared player visual code
* Confirm the teddy bear configuration can be imported into the main player system later

### Acceptance Criteria

* Reusable visual logic is clearly separated from demo code
* Teddy bear setup is ready for later integration into the main game
* No major refactor should be needed to reuse the chosen character


# TASKS.md

## Project Phase: Teddy Bear Visual Exploration

Goal: Create 4–5 shape-based teddy bear options inside `playerdemo.py` so the best player silhouette and personality can be selected.

---

## Task 125 – Add Shape-Based Teddy Option Framework

**Status:** DONE

### Objective
Enable multiple code-drawn teddy bear variants in the demo.

### Requirements
- Support multiple teddy render variants (no sprites)
- Keep variants modular and reusable
- Share existing systems:
  - facing
  - bounce
  - scale
  - debug overlay

### Acceptance Criteria
- Demo supports multiple teddy options
- Variants are defined cleanly in one place
- No regression to existing demo features

---

## Task 126 – Teddy Option A: Classic Round Plush

**Status:** DONE

### Objective
Create a soft, friendly baseline teddy.

### Requirements
- Large round head
- Small round ears
- Small oval body
- Minimal face (dot eyes)
- Optional small party hat

### Acceptance Criteria
- Clearly reads as a teddy bear
- Strong, simple silhouette
- Works at small scale

---

## Task 127 – Teddy Option B: Big-Head Chibi

**Status:** DONE

### Objective
Increase personality with exaggerated proportions.

### Requirements
- Larger head-to-body ratio than Option A
- Very small body
- Slightly oversized ears or cheeks
- Simplified face

### Acceptance Criteria
- Feels more playful and stylized
- Head remains visual anchor
- Still readable during motion

---

## Task 128 – Teddy Option C: Gameplay-First Compact

**Status:** DONE

### Objective
Optimize for maximum gameplay readability.

### Requirements
- Compact shape
- Strong ear/head separation
- Minimal width and noise
- Clean face placement

### Acceptance Criteria
- Easy to track during movement
- Silhouette holds under scaling
- Prioritizes clarity over charm

---

## Task 129 – Teddy Option D: Party Hat Hero

**Status:** DONE

### Objective
Lean into the party theme.

### Requirements
- Clear teddy base shape
- Larger or more visible party hat
- Bright accent color
- Hat does not obscure face

### Acceptance Criteria
- Strong party identity
- Still reads as player first
- No visual clutter

---

## Task 130 – Teddy Option E: Taller Plush Variant

**Status:** DONE

### Objective
Test subtle body proportion variation.

### Requirements
- Big head
- Slightly taller/narrower body
- Same visual language as other teddies
- Minimal face + ear detail

### Acceptance Criteria
- Distinct from other options
- Still clearly a teddy
- Useful comparison in demo

---

## Task 131 – Add Teddy Variant Cycling

**Status:** DONE

### Objective
Allow quick comparison of teddy options.

### Requirements
- Add all teddy options to demo cycle
- Display current option name
- Keep switching instant and stable

### Acceptance Criteria
- All options can be cycled in one session
- Name is always visible
- No visual glitches

---

## Task 132 – Add Comparison Notes Overlay

**Status:** DONE

### Objective
Help evaluate each option.

### Requirements
- Display short notes per variant:
  - silhouette type
  - proportion style
  - readability focus
- Keep overlay minimal

### Acceptance Criteria
- Notes improve decision-making
- Overlay remains clean and readable

---

## Task 133 – Readability Validation Pass

**Status:** DONE

### Objective
Ensure all options perform well visually.

### Requirements
- Test against:
  - background
  - scaling
  - facing
  - movement preview
- Make small adjustments as needed

### Acceptance Criteria
- All options are viable
- Differences are intentional
- No major readability issues

---

## Task 134 – Prepare for Main Game Integration

**Status:** DONE

### Objective
Make final teddy easy to integrate.

### Requirements
- Keep rendering logic reusable
- Avoid demo-only hacks
- Document integration path

### Acceptance Criteria
- Selected teddy can move to main game easily
- Minimal refactor required
- Demo remains reusable sandbox

---

# Execution Rules for Agents

For each task:

1. Read `GAME_VISION.md` and `AGENTS.md`
2. Propose a plan BEFORE coding
3. List files to modify
4. Implement only the current task
5. Verify:
   - run the demo
   - check for errors
6. Summarize changes clearly

---

## Notes

- Do NOT skip tasks
- Do NOT expand scope
- Keep implementations simple
- Prioritize readability over detail
- Use shape-based rendering only

# TASKS.md

## Project Phase: Teddy Bear Stylization Pass

Goal: Explore several more stylized teddy bear variants based on Option A so the team can keep the strong readability baseline while adding more charm and personality.

---

## Task 135 – Create Stylized Teddy Exploration Set

**Status:** DONE

### Objective
Add a new set of teddy bear variants derived from Option A.

### Requirements
- Use Option A as the structural baseline
- Create 4–5 new stylized teddy variants
- Keep all variants shape-based
- Preserve shared demo systems:
  - facing
  - bounce
  - scale
  - debug overlay

### Acceptance Criteria
- Demo supports a new family of Option A-derived teddy variants
- New variants are clearly grouped as stylizations of the same core design
- No regression to existing demo behavior

---

## Task 136 – Teddy Variant F: Softer Plush Deluxe

**Status:** DONE

### Objective
Create a softer, more plush-looking version of Option A.

### Requirements
- Keep the same readable round silhouette
- Add slightly fuller cheeks or softer head/body transitions
- Use subtle shape adjustments only
- Avoid extra detail that hurts clarity

### Acceptance Criteria
- Variant feels softer and more plush than Option A
- Silhouette remains immediately readable
- Character still performs well at gameplay scale

---

## Task 137 – Teddy Variant G: Hero Plush

**Status:** DONE

### Objective
Create a slightly bolder protagonist-looking version of Option A.

### Requirements
- Keep Option A proportions mostly intact
- Introduce a more confident silhouette through:
  - slightly stronger chest/body shape
  - clearer stance
  - more intentional hat placement
- Maintain simplicity and softness

### Acceptance Criteria
- Variant feels more like a main character
- Readability remains as strong as Option A
- Changes are visible without becoming noisy

---

## Task 138 – Teddy Variant H: Extra Cute Chibi Plush

**Status:** DONE

### Objective
Push Option A slightly further toward cute/chibi styling.

### Requirements
- Increase head dominance slightly
- Keep body small but stable
- Optionally enlarge ears or adjust eye spacing
- Preserve the same overall teddy identity

### Acceptance Criteria
- Variant feels cuter than Option A
- Character still reads clearly in motion
- Chibi changes do not make the design fragile or awkward

---

## Task 139 – Teddy Variant I: Party Plush Star

**Status:** DONE

### Objective
Create a more theme-forward version of Option A.

### Requirements
- Keep the Option A teddy silhouette intact
- Add stronger party flair using one simple element such as:
  - a more visible party hat
  - a pom-pom
  - a tiny bow tie
  - a confetti-color accent
- Keep accessory placement clean and readable

### Acceptance Criteria
- Variant feels more connected to Confetti Chaos
- Teddy remains readable as the player first
- Extra party styling does not clutter the design

---

## Task 140 – Teddy Variant J: Clean Premium Plush

**Status:** DONE

### Objective
Create a polished, minimal, premium-looking version of Option A.

### Requirements
- Refine spacing and proportions rather than adding detail
- Use very intentional shape placement
- Keep face and accessory treatment minimal
- Focus on “simple but polished” visual feel

### Acceptance Criteria
- Variant feels cleaner and more refined than Option A
- Design remains lightweight and easy to implement
- Silhouette stays strong under scaling and movement preview

---

## Task 141 – Add Stylized Teddy Labels and Notes

**Status:** DONE

### Objective
Make it easy to compare the new Option A-derived variants.

### Requirements
- Add each new stylized teddy to the demo cycle
- Display the active variant name
- Add short style notes such as:
  - softer
  - heroic
  - extra cute
  - party-forward
  - premium clean

### Acceptance Criteria
- User can quickly compare all stylized teddy options
- Labels and notes are always readable
- Variant differences are easy to understand in the demo

---

## Task 142 – Run Stylization Readability Pass

**Status:** DONE

### Objective
Ensure the stylized variants keep the strengths of Option A.

### Requirements
- Test all new variants against:
  - neutral background
  - scale changes
  - facing preview
  - movement preview
- Tune shapes and accessory sizes as needed
- Remove or reduce any detail that hurts clarity

### Acceptance Criteria
- All stylized variants remain viable for gameplay
- Option A readability strengths are preserved
- Variants differ mainly in feel, not in clarity loss

---

## Task 143 – Select Finalists for Main Game Candidate List

**Status:** DONE

### Objective
Narrow the stylized set down to the strongest options.

### Requirements
- Compare Option A and all new stylized variants
- Identify the top 2–3 candidates
- Document why each finalist works in terms of:
  - silhouette
  - readability
  - theme fit
  - charm/personality

### Acceptance Criteria
- A small finalist list is identified
- Selection reasoning is visible in the demo or notes
- Finalists are ready for main game consideration

---

# Execution Rules for Agents

For each task:

1. Read `GAME_VISION.md` and `AGENTS.md`
2. Propose a plan BEFORE coding
3. List files to modify
4. Implement only the current task
5. Verify:
   - run the demo
   - check for errors
6. Summarize changes clearly

---

## Notes

- Do NOT skip tasks
- Do NOT expand scope
- Keep implementations simple
- Preserve Option A readability as the baseline
- Use shape-based rendering only

# TASKS.md

## Project Phase: Softer Plush Deluxe Animal Expansion

Goal: Create 3 additional party animal variants using the “Softer Plush Deluxe” teddy style as the visual guide so the roster begins to feel cohesive, plush, and readable.

---

## Task 144 – Define Softer Plush Deluxe Style Guide for Shared Use

**Status:** DONE

### Objective
Turn the selected teddy direction into a reusable visual style guide for new animals.

### Requirements
- Use the “Softer Plush Deluxe” teddy as the baseline
- Document the shared visual rules for all new animals, including:
  - big head / small body proportions
  - soft rounded shapes
  - minimal facial features
  - plush-like silhouette
  - simple accessory treatment
  - readable outline and contrast rules
- Keep the guide lightweight and practical for implementation

### Acceptance Criteria
- A clear shared style guide exists for future animal variants
- New variants can be built consistently from the same visual rules
- Style guide helps prevent drift in silhouette, tone, or complexity

---

## Task 145 – Create Bunny Variant in Softer Plush Deluxe Style

**Status:** DONE

### Objective
Add a bunny party animal using the softer plush deluxe look.

### Requirements
- Use the shared teddy style guide as the baseline
- Bunny should include:
  - large plush head
  - small soft body
  - long rounded ears
  - simple dot eyes
  - minimal facial detail
- Keep ears readable without becoming thin or noisy
- Maintain strong silhouette separation from the teddy

### Acceptance Criteria
- Bunny clearly reads as a bunny at gameplay scale
- Variant feels like part of the same plush family as the teddy
- Long ears improve distinction without hurting readability

---

## Task 146 – Create Fox Variant in Softer Plush Deluxe Style

**Status:** DONE

### Objective
Add a fox party animal using the softer plush deluxe look.

### Requirements
- Use the shared teddy style guide as the baseline
- Fox should include:
  - large plush head
  - small body
  - soft triangular or rounded-triangular ears
  - simple face placement
  - subtle fox identity cues without sharp complexity
- Keep the fox softer than a typical angular fox design
- Preserve clarity and plush appeal

### Acceptance Criteria
- Fox clearly reads as a fox while staying soft and plush-like
- Variant feels visually cohesive with teddy and bunny
- Ear and face shapes provide distinct identity without visual noise

---

## Task 147 – Create Cat Variant in Softer Plush Deluxe Style

**Status:** DONE

### Objective
Add a cat party animal using the softer plush deluxe look.

### Requirements
- Use the shared teddy style guide as the baseline
- Cat should include:
  - large plush head
  - small body
  - compact soft triangular ears
  - minimal face
  - subtle cat silhouette cues
- Keep the cat distinct from the fox
- Avoid over-detailing whiskers or facial features

### Acceptance Criteria
- Cat clearly reads as a cat at gameplay scale
- Variant feels like part of the same plush character set
- Cat remains readable and distinct from bunny, fox, and teddy

---

## Task 148 – Add Shared Accessory Rules Across Plush Variants

**Status:** DONE

### Objective
Keep the new animals unified through a consistent party-themed accessory system.

### Requirements
- Define how accessories apply across teddy, bunny, fox, and cat
- Use one simple shared accessory approach such as:
  - party hat
  - pom-pom
  - tiny bow tie
- Keep accessory scale and placement consistent
- Ensure accessories support identity without obscuring silhouettes

### Acceptance Criteria
- All plush variants feel like part of one coherent cast
- Accessories reinforce the Confetti Chaos theme
- Accessory treatment remains minimal and readable

---

## Task 149 – Add New Plush Animals to `playerdemo.py`

**Status:** DONE

### Objective
Make the new softer plush deluxe animal variants viewable in the demo.

### Requirements
- Add teddy, bunny, fox, and cat plush variants to the demo cycle
- Ensure each variant uses the shared render structure
- Preserve existing demo systems:
  - facing preview
  - bounce
  - scale controls
  - debug overlay
- Keep switching immediate and stable

### Acceptance Criteria
- Demo can cycle through all softer plush deluxe animals
- Existing demo controls still work correctly
- No crashes or regressions occur when switching variants

---

## Task 150 – Add Variant Labels and Style Notes for New Animals

**Status:** DONE

### Objective
Make the new plush animal set easier to compare and evaluate.

### Requirements
- Display current animal name on screen
- Add short notes for each variant such as:
  - ear type
  - silhouette style
  - readability emphasis
  - plush family role
- Keep notes brief and non-distracting

### Acceptance Criteria
- User can quickly identify which animal is being viewed
- Notes help compare shape language and readability
- Overlay remains clean and useful

---

## Task 151 – Run Cohesion and Readability Pass Across Plush Set

**Status:** DONE

### Objective
Ensure the new animal set feels cohesive and gameplay-ready.

### Requirements
- Review teddy, bunny, fox, and cat together against:
  - neutral background
  - scale changes
  - facing preview
  - movement preview
- Tune shapes, spacing, and accessory sizes as needed
- Ensure each animal is distinct while still feeling part of the same set

### Acceptance Criteria
- All variants feel like members of the same plush family
- Each animal remains visually distinct
- No major readability issues remain

---

## Task 152 – Prepare Plush Animal Set for Main Game Candidate Selection

**Status:** DONE

### Objective
Make the new softer plush deluxe cast ready for next-step selection and integration.

### Requirements
- Keep render logic modular and reusable
- Ensure each animal uses the shared style system cleanly
- Document which variants are strongest candidates for main game use
- Avoid demo-only hacks in reusable visual code

### Acceptance Criteria
- Plush animal set is ready for selection review
- Reusable render logic is organized clearly
- Main game integration path remains straightforward

---

# Execution Rules for Agents

For each task:

1. Read `GAME_VISION.md` and `AGENTS.md`
2. Propose a plan BEFORE coding
3. List files to modify
4. Implement only the current task
5. Verify:
   - run the demo
   - check for errors
6. Summarize changes clearly

---

# TASKS.md

## Project Phase: Main Game Party Animal Integration

Goal: Integrate the “Softer Plush Deluxe” teddy bear into the main game as the new default player visual, using a structure that cleanly supports additional party animals later.

---

## Task 153 – Create Shared Party Animal Render Module

**Status:** DONE

### Objective
Move reusable shape-based player rendering into a shared module for main game use.

### Requirements
- Create a dedicated module for shape-based party animal rendering
- Move reusable drawing logic out of `playerdemo.py` where appropriate
- Keep rendering separate from player movement, combat, and state logic
- Structure the module so multiple animal types can be added later

### Acceptance Criteria
- Main game can import shared party animal render code
- Rendering is decoupled from gameplay logic
- Module structure is ready for future bunny, fox, cat, and other variants

---

## Task 154 – Define Party Animal Visual Config Structure

**Status:** DONE

### Objective
Create a reusable configuration system for party animal visuals.

### Requirements
- Define a config/data structure for party animal visuals that can include:
  - animal name
  - shape/profile type
  - color palette
  - ears / accessory traits
  - outline settings
  - body proportions
  - optional offsets or tuning values
- Keep config simple and code-friendly
- Ensure the structure supports future variants without major refactor

### Acceptance Criteria
- Teddy bear visual settings are defined in one clear config
- System is extensible for additional party animals
- Main game render path can use config-driven visuals cleanly

---

## Task 155 – Add Softer Plush Deluxe Teddy Render Implementation

**Status:** DONE

### Objective
Implement the selected softer plush deluxe teddy bear in the shared main game render system.

### Requirements
- Port the chosen teddy bear design from the demo into the shared module
- Preserve key traits of the selected style:
  - big plush head
  - small soft body
  - rounded shapes
  - minimal face
  - clean accessory treatment
- Keep the implementation lightweight and performant
- Ensure the teddy remains readable at gameplay scale

### Acceptance Criteria
- Softer plush deluxe teddy renders correctly in the shared system
- Visual appearance matches the chosen demo direction closely
- No gameplay behavior depends on teddy-specific render code

---

## Task 156 – Wire Party Animal Renderer Into Main Player Entity

**Status:** DONE

### Objective
Use the shared party animal render system for the actual player in the main game.

### Requirements
- Connect the player entity to the new party animal render module
- Replace placeholder or older player visuals with the softer plush deluxe teddy
- Keep gameplay logic unchanged
- Preserve existing player-facing features such as:
  - movement direction feedback
  - bounce / squash if applicable
  - hitbox separation
  - debug support

### Acceptance Criteria
- Main game player uses the new teddy visual
- No regression in movement, combat, collision, or progression systems
- Render integration remains clean and modular

---

## Task 157 – Add Default Party Animal Registration System

**Status:** DONE

### Objective
Prepare the game to support multiple party animal player options later.

### Requirements
- Add a simple registration or lookup system for party animal variants
- Register the softer plush deluxe teddy as the default active animal
- Keep variant selection separate from rendering internals
- Design the system so new animals can be added with minimal code duplication

### Acceptance Criteria
- Teddy is selectable through a named variant system
- New party animals can be registered later without redesigning the render path
- Default player animal is easy to identify and change

---

## Task 158 – Add Shared Accessory and Style Rules Support

**Status:** DONE

### Objective
Create a reusable way to apply shared party-themed style elements across future animals.

### Requirements
- Support shared accessory logic for party animals, such as:
  - party hat
  - pom-pom
  - small optional accent
- Keep accessory rendering modular and configurable
- Ensure accessories do not obscure the face or hurt readability
- Reuse the same system for future animal variants

### Acceptance Criteria
- Teddy uses shared accessory logic rather than one-off hardcoding
- Future animals can inherit the same party styling system
- Accessory rendering remains readable and lightweight

---

## Task 159 – Validate Gameplay Readability in Main Game Scenes

**Status:** DONE

### Objective
Ensure the new teddy remains easy to track during actual gameplay.

### Requirements
- Test the teddy player visual against:
  - arena background
  - enemy waves
  - confetti particles
  - effects-heavy moments
  - level progression pacing
- Tune outline, contrast, scale, or facial spacing if needed
- Keep adjustments small and targeted

### Acceptance Criteria
- Teddy remains easy to identify during chaotic gameplay
- No confusion with enemies or effects
- Visual clarity is preserved in real game conditions

---

## Task 160 – Preserve Hitbox and Visual Alignment Rules

**Status:** DONE

### Objective
Ensure the new visual presentation aligns cleanly with gameplay collision and positioning.

### Requirements
- Confirm player hitbox remains independent from visual silhouette
- Align render anchor consistently with the main player position
- Ensure body-centered collision still feels fair
- Reuse anchor/hitbox lessons learned from the demo

### Acceptance Criteria
- Player feels visually grounded in the arena
- Hitbox remains fair and configurable
- No visible jumping, drift, or mismatch between visual and collision center

---

## Task 161 – Add Debug Support for Main Game Party Animal Rendering

**Status:** DONE

### Objective
Make main game integration easier to inspect and tune.

### Requirements
- Add or reuse a debug overlay for:
  - anchor point
  - hitbox
  - optional render bounds
  - active party animal name
- Keep debug view toggleable
- Avoid clutter in normal gameplay

### Acceptance Criteria
- Debug tools help inspect teddy alignment and readability
- Overlay can be toggled on and off safely
- Debug support is reusable for future party animals

---

## Task 162 – Separate Reusable Party Animal Code From Demo-Only Code

**Status:** DONE

### Objective
Keep the demo sandbox useful while making the main game integration clean.

### Requirements
- Move reusable animal definitions/render helpers into shared code
- Keep demo-only controls, overlays, and cycling logic inside `playerdemo.py`
- Avoid duplicate implementations of the teddy render logic
- Ensure both the main game and demo can use the same animal definitions where practical

### Acceptance Criteria
- Shared animal logic exists in one place
- Demo remains a sandbox without becoming the source of gameplay hacks
- Main game and demo stay consistent with less maintenance

---

## Task 163 – Add Placeholder Support Path for Future Party Animals

**Status:** DONE

### Objective
Make future expansion straightforward even before new animals are fully integrated.

### Requirements
- Add clear extension points for future animals such as:
  - bunny
  - fox
  - cat
- Support adding new visual configs without changing core player logic
- Document the minimal steps needed to add another party animal later

### Acceptance Criteria
- Future animals can be added through the shared variant system
- Core player code does not need redesign for each new animal
- Expansion path is obvious and low-friction

---

## Task 164 – Final Integration Verification Pass

**Status:** DONE

### Objective
Confirm the softer plush deluxe teddy is ready as the main player visual baseline.

### Requirements
- Run the main game and verify:
  - player visual renders correctly
  - direction feedback works
  - movement feedback still feels good
  - hitbox/debug tools remain correct
  - no performance issues are introduced
- Review code organization for future party animal growth
- Make small cleanup adjustments as needed

### Acceptance Criteria
- Softer plush deluxe teddy is stable in the main game
- Integration is clean and future-ready
- No major refactor is needed to add more party animals later

---

# TASKS.md

## Project Phase: Party Animal Expansion & Player Select

Goal: Add additional playable party animals (bunny, fox, cat) to the main game and implement a simple player selection screen at the beginning of the game using the shared party animal visual system.

---

## Task 165 – Add Bunny Visual Config and Render Support

**Status:** DONE

### Objective
Add the bunny as a playable party animal using the shared shape-based render system.

### Requirements
- Create a bunny party animal definition using the shared config structure
- Follow the established plush style rules:
  - big head
  - small body
  - soft rounded forms
  - minimal face
  - clear silhouette
- Use long rounded ears that remain readable at gameplay scale
- Reuse shared accessory support where appropriate

### Acceptance Criteria
- Bunny is available as a registered party animal
- Bunny renders correctly in the main game
- Bunny feels cohesive with the teddy baseline while remaining distinct

---

## Task 166 – Add Fox Visual Config and Render Support

**Status:** DONE

### Objective
Add the fox as a playable party animal using the shared shape-based render system.

### Requirements
- Create a fox party animal definition using the shared config structure
- Keep the fox soft and plush-like rather than sharp or aggressive
- Use subtle fox cues such as:
  - soft triangular ears
  - slightly different face/body proportions
  - gentle color contrast
- Reuse shared accessory support where appropriate

### Acceptance Criteria
- Fox is available as a registered party animal
- Fox renders correctly in the main game
- Fox is distinct from teddy and bunny without introducing visual noise

---

## Task 167 – Add Cat Visual Config and Render Support

**Status:** DONE

### Objective
Add the cat as a playable party animal using the shared shape-based render system.

### Requirements
- Create a cat party animal definition using the shared config structure
- Follow the same plush family rules as the other animals
- Use compact soft triangular ears and minimal facial features
- Keep the cat distinct from the fox through silhouette and proportion choices
- Reuse shared accessory support where appropriate

### Acceptance Criteria
- Cat is available as a registered party animal
- Cat renders correctly in the main game
- Cat feels cohesive with the other party animals and remains visually distinct

---

## Task 168 – Expand Party Animal Registry for Multiple Playable Characters

**Status:** DONE

### Objective
Make the shared party animal registry ready for multiple selectable player animals.

### Requirements
- Register teddy, bunny, fox, and cat in one clear place
- Ensure each registered animal includes:
  - display name
  - render config
  - palette
  - style/accessory traits
- Keep registration data separate from gameplay logic
- Design the registry so more animals can be added later with minimal duplication

### Acceptance Criteria
- All current playable animals are registered consistently
- Registry is easy to extend for future animals
- Main game can look up animals by key or name cleanly

---

## Task 169 – Add Active Player Animal Selection State

**Status:** DONE

### Objective
Allow the game to track which party animal is currently selected by the player.

### Requirements
- Add a simple game state or config value for the active player animal
- Ensure the selected animal can be passed into player creation/render logic
- Keep this state separate from low-level render implementation
- Use teddy as the fallback default if no selection is set

### Acceptance Criteria
- Game can track the currently selected player animal
- Player entity uses the selected animal cleanly
- Default fallback behavior works without errors

---

## Task 170 – Create Player Selection Screen Scene

**Status:** DONE

### Objective
Add a lightweight player selection screen at the beginning of the game.

### Requirements
- Create a simple pre-game screen or scene shown before gameplay begins
- Display available party animal choices:
  - teddy
  - bunny
  - fox
  - cat
- Keep presentation simple, clear, and fast
- Reuse main game visual assets/rendering where practical

### Acceptance Criteria
- Game opens to a working player selection screen
- Available party animals are clearly presented
- Screen is lightweight and fits the overall game style

---

## Task 171 – Add Navigation and Confirm Controls for Player Select

**Status:** DONE

### Objective
Make the selection screen usable and responsive.

### Requirements
- Add controls to move between animal choices, such as:
  - left/right arrows
  - A/D
- Add confirm input, such as:
  - Enter
  - Space
- Highlight the current selection clearly
- Keep input handling simple and stable

### Acceptance Criteria
- Player can navigate between all animal options
- Current selection is always obvious
- Confirming a selection advances cleanly into the game

---

## Task 172 – Add Character Preview Presentation to Selection Screen

**Status:** DONE

### Objective
Help the player evaluate each party animal before starting a run.

### Requirements
- Show a clear visual preview of the currently selected animal
- Reuse the same shape-based render logic as gameplay where possible
- Support a simple preview state such as:
  - idle
  - bounce
  - slight facing presentation
- Keep the preview readable and non-busy

### Acceptance Criteria
- Each animal can be previewed clearly on the selection screen
- Preview helps compare personality and silhouette
- Presentation remains simple and performant

---

## Task 173 – Add Selection Labels and Short Flavor Notes

**Status:** DONE

### Objective
Make the player select screen feel more polished and informative.

### Requirements
- Display each animal’s name clearly
- Add short flavor notes or style tags, such as:
  - classic plush
  - soft hopper
  - clever plush
  - cozy cat
- Keep text minimal and readable
- Avoid implying gameplay stat differences unless they actually exist

### Acceptance Criteria
- Player can easily identify each option
- Screen feels more intentional and polished
- Notes support charm without clutter

---

## Task 174 – Transition from Player Select Into Gameplay

**Status:** DONE

### Objective
Start the run using the chosen party animal.

### Requirements
- On confirm, transition cleanly from selection screen into the main game
- Spawn the player using the selected animal config
- Ensure the selected animal is used for:
  - rendering
  - accessory styling
  - debug naming if applicable
- Preserve existing gameplay startup flow wherever possible

### Acceptance Criteria
- Confirmed selection carries into gameplay correctly
- Main game starts normally after selection
- Chosen party animal is visible and active during the run

---

## Task 175 – Add Fallback and Safe Defaults for Selection Flow

**Status:** DONE

### Objective
Keep the game stable if selection state is missing or invalid.

### Requirements
- Fall back to teddy if selection data is absent or invalid
- Prevent selection screen issues from crashing gameplay start
- Keep selection handling defensive and simple
- Ensure registered animal lookup failures are handled gracefully

### Acceptance Criteria
- Game still starts safely if selection state is broken
- Teddy fallback works reliably
- No hard crashes occur from invalid selection data

---

## Task 176 – Add Reuse Path Between Selection Screen and Demo Assets

**Status:** DONE

### Objective
Avoid duplicate visual implementations across sandbox and gameplay entry flow.

### Requirements
- Reuse shared party animal definitions/render helpers in both:
  - player selection screen
  - main gameplay
  - demo where practical
- Avoid copying animal-specific render code into the selection scene
- Keep demo-only controls separate from shared logic

### Acceptance Criteria
- Shared visual code remains centralized
- Selection screen and gameplay stay visually consistent
- Future animal updates require minimal duplicated changes

---

## Task 177 – Run Readability and UX Pass on Player Select Screen

**Status:** DONE

### Objective
Ensure the player select flow is clear, appealing, and usable.

### Requirements
- Review the player select screen for:
  - character readability
  - selection clarity
  - clean layout
  - input responsiveness
  - smooth transition into gameplay
- Adjust spacing, scale, labels, or highlight treatment as needed
- Keep the screen simple and lightweight

### Acceptance Criteria
- Selection screen is easy to understand immediately
- Animals are visually distinct and appealing
- Flow from startup to gameplay feels smooth and stable

---

## Task 178 – Final Integration Verification for Party Animal Selection

**Status:** DONE

### Objective
Confirm the expanded party animal system and player select flow are ready for ongoing development.

### Requirements
- Verify:
  - teddy, bunny, fox, and cat all render correctly
  - selection screen appears at game start
  - selection persists into gameplay
  - fallback behavior works
  - no major regressions were introduced
- Review code organization for future animal additions
- Make minor cleanup adjustments as needed

### Acceptance Criteria
- Multi-animal player system is stable
- Player selection flow works end to end
- Future party animal additions remain straightforward

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

## Task 189 – Decouple Level System from Time & Kill Count

**Status:** TODO

### Objective

Remove time-based and kill-count-based level progression.

### Requirements

* Identify and remove:

  * time-driven level increases
  * kill-count thresholds triggering level changes

* Ensure:

  * no remaining logic increments level outside XP system
  * existing systems do not depend on old triggers

### Acceptance Criteria

* Level no longer increases based on time or kill count
* No orphaned logic referencing old level triggers
* Game runs without progression errors

---

## Task 190 – Promote XP to Primary Progression Driver

**Status:** TODO

### Objective

Make player XP the only mechanism for leveling up.

### Requirements

* Ensure XP gain is already wired (Task 81)
* Tie level-up trigger directly to XP thresholds
* Remove any alternate level-up pathways

### Acceptance Criteria

* Player level increases only when XP threshold is reached
* XP is the single source of truth for progression
* Level-up flow is consistent and predictable

---

## Task 191 – Update Spawn System to Use Player Level

**Status:** TODO

### Objective

Drive enemy spawning and difficulty scaling from player level instead of time.

### Requirements

* Replace time-based scaling inputs with:

  * player run level

* Spawn system should use:

  * current player level
  * level-based difficulty curves

* Maintain support for:

  * enemy tiers
  * flavor modifiers

### Acceptance Criteria

* Enemy difficulty scales with player level
* No dependency on elapsed time for scaling
* Gameplay pacing feels responsive to player performance

---

## Task 192 – Redefine Level Progression Curve (XP Scaling)

**Status:** TODO

### Objective

Define how much XP is required per level.

### Requirements

* Implement XP curve, e.g.:

  * linear (simple start)
  * or slightly exponential

* Example:

  * Level 1 → 2: 10 XP
  * Level 2 → 3: 15 XP
  * Level 3 → 4: 22 XP

* Keep values configurable

### Acceptance Criteria

* XP thresholds increase predictably
* Level-ups feel frequent early and slower later
* Curve is easy to tune

---

## Task 193 – Adjust XP Rewards for Enemies

**Status:** TODO

### Objective

Balance XP gain to support new progression model.

### Requirements

* Assign XP values per enemy type:

  * balloons (low)
  * piñatas (medium/high)
  * sprayers (medium)
  * snakes (medium/high)
  * bosses (large bonus)

* Ensure XP flow supports intended pacing

### Acceptance Criteria

* XP gain feels consistent with difficulty
* Player levels up at a satisfying rate
* No extreme spikes or droughts in progression

---

## Task 194 – Align Upgrade Frequency with XP Progression

**Status:** TODO

### Objective

Ensure upgrade pacing matches the new XP-driven level system.

### Requirements

* Validate:

  * how often level-ups occur
  * how often upgrade choices appear

* Adjust XP curve or rewards if needed

### Acceptance Criteria

* Player receives upgrades at a steady, satisfying cadence
* No long gaps without progression
* No overwhelming rapid upgrades

---

## Task 195 – Update UI to Reflect XP-Driven Progression

**Status:** TODO

### Objective

Ensure UI reflects XP-based leveling instead of time or kills.

### Requirements

* Display:

  * current level
  * XP bar progress

* Remove:

  * time-based level indicators
  * kill-based progression indicators (if any)

### Acceptance Criteria

* UI clearly communicates XP progression
* No confusing or outdated indicators remain
* Player understands how leveling works

---

## Task 196 – Remove Legacy Level Logic & Cleanup

**Status:** TODO

### Objective

Clean up any remaining legacy systems tied to old level mechanics.

### Requirements

* Remove:

  * unused variables
  * deprecated functions
  * outdated configs

* Refactor any systems that referenced:

  * time-based scaling
  * kill thresholds

### Acceptance Criteria

* Codebase no longer contains legacy level logic
* Systems are clean and consistent
* No dead code related to old progression remains

---

## Task 197 – Validate Gameplay Pacing After Refactor

**Status:** TODO

### Objective

Ensure the new XP-driven progression feels good in real gameplay.

### Requirements

* Playtest early, mid, and late runs

* Validate:

  * difficulty ramp
  * upgrade cadence
  * enemy pressure scaling

* Adjust:

  * XP curve
  * spawn scaling
  * enemy XP rewards

### Acceptance Criteria

* Game pacing feels natural and engaging
* Difficulty responds to player performance
* Progression loop feels tight and rewarding

---

## Task 198 – Optional: Hybrid Scaling Safeguard (Failsafe)

**Status:** TODO

### Objective

Prevent slow or passive play from stalling progression.

### Requirements

* Add optional fallback scaling:

  * minimal time-based pressure increase
    OR
  * minimum spawn escalation over time

* Keep this subtle and secondary to XP

### Acceptance Criteria

* Game cannot stall if player avoids enemies
* XP remains primary progression driver
* System does not feel artificial or forced


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
