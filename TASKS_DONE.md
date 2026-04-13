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


## Task 199 – Character Passive System Foundation

**Status:** DONE

### Objective

Create a system for character-specific passive modifiers applied at run start.

### Requirements

* Add a character definition structure that supports:

  * character id
  * display name
  * passive bonus
  * passive drawback

* Apply passives when a run begins

* Keep passives data-driven and separate from core player logic

### Acceptance Criteria

* Character passives are defined in one clear place
* Passive effects are applied at the start of a run
* System is easy to extend for new characters

---

## Task 200 – Implement Initial Character Passives

**Status:** DONE

### Objective

Add the first set of character-specific passive strengths and weaknesses.

### Requirements

* Implement at minimum:

  * **Bear**: +1 max health, reduced movement speed
  * **Bunny**: increased movement speed, -1 max health
  * **Cat**: increased damage, increased damage taken
  * **Raccoon**: increased pickup radius or XP gain, reduced damage

* Ensure passive values are easy to tune

* Keep effects noticeable but not dominant

### Acceptance Criteria

* Each starting character has a distinct passive identity
* Tradeoffs are clearly reflected in gameplay
* No passive breaks game balance or core systems

---

## Task 201 – Character Passive UI Presentation

**Status:** DONE

### Objective

Show character passive strengths and weaknesses clearly to the player.

### Requirements

* Display for each character:

  * passive name or summary
  * positive effect
  * negative effect

* Integrate into character selection or demo UI

* Keep presentation short and readable

### Acceptance Criteria

* Player can understand each character's tradeoff quickly
* UI clearly communicates strengths and weaknesses
* Passive descriptions remain consistent with actual gameplay behavior

---

## Task 202 – Dodge System Foundation

**Status:** DONE

### Objective

Add a player dodge action as a short repositioning tool.

### Requirements

* Add a dodge input action

* Dodge should:

  * move the player quickly in the current movement direction
  * have a fixed short duration
  * have a fixed short travel distance

* Keep dodge separate from normal movement update logic where practical

### Acceptance Criteria

* Player can trigger dodge reliably
* Dodge movement feels distinct from normal movement
* System is modular and tunable

---

## Task 203 – Dodge Cooldown & State Handling

**Status:** DONE

### Objective

Prevent dodge spam and ensure dodge behaves consistently.

### Requirements

* Add dodge cooldown

* Prevent dodge from activating:

  * during cooldown
  * while dead
  * in invalid game states

* Add internal dodge state tracking such as:

  * dodging
  * cooldown remaining

### Acceptance Criteria

* Dodge cannot be spammed
* Dodge state transitions are stable and predictable
* Invalid activations are handled cleanly

---

## Task 204 – Dodge Invulnerability Window

**Status:** DONE

### Objective

Give dodge a short invulnerability window without making it overpowered.

### Requirements

* Add partial invulnerability during dodge

* Invulnerability should:

  * be shorter than full dodge duration
  * not persist after dodge ends

* Ensure enemy collisions respect dodge invulnerability

### Acceptance Criteria

* Dodge can be used to avoid damage when timed correctly
* Invulnerability window is noticeable but limited
* Dodge does not trivialize enemy pressure

---

## Task 205 – Dodge Visual & Audio Feedback

**Status:** DONE

### Objective

Make dodge feel responsive, readable, and thematic.

### Requirements

* Add effects such as:

  * brief afterimage
  * confetti burst or trail
  * squash/stretch or motion emphasis
  * optional dodge sound

* Ensure visuals do not interfere with readability

### Acceptance Criteria

* Dodge has clear feedback when activated
* Player can easily tell when dodge occurred
* Feedback improves feel without clutter

---

## Task 206 – Dodge Balance & Character Interaction

**Status:** DONE

### Objective

Tune dodge so it works fairly across all characters and playstyles.

### Requirements

* Validate dodge behavior for:

  * Bear
  * Bunny
  * Cat
  * Raccoon

* Tune:

  * cooldown
  * distance
  * invulnerability timing

* Decide whether passives affect dodge at all in this phase

### Acceptance Criteria

* Dodge is useful across all characters
* No character gains a clearly broken dodge advantage
* Dodge remains a skill tool, not a dominant strategy

---

## Task 207 – Super Ability System Foundation

**Status:** DONE

### Objective

Create a framework for character-specific super abilities.

### Requirements

* Add a super ability structure supporting:

  * character id
  * super name
  * charge amount
  * max charge
  * activation behavior

* Add a dedicated activation input

* Keep supers modular and character-specific

### Acceptance Criteria

* Super abilities are represented in a reusable system
* Activation input is recognized correctly
* Framework supports multiple distinct supers

---

## Task 208 – Super Charge System

**Status:** DONE

### Objective

Require supers to be earned through gameplay rather than simple time cooldown.

### Requirements

* Add super meter charge from gameplay events such as:

  * enemy kills
  * boss damage or boss defeat
  * optional XP pickup collection

* Prevent super from charging infinitely past max

* Reset or reinitialize charge correctly on run start

### Acceptance Criteria

* Super meter fills during normal gameplay
* Charge gain is visible and consistent
* Supers must be earned before activation

---

## Task 209 – Implement Bear Super: Roar

**Status:** DONE

### Objective

Give the Bear a crowd-control super that creates breathing room.

### Requirements

* On activation:

  * emit radial roar/shockwave
  * push enemies away
  * optionally apply brief stun or slow

* Keep effect readable and short-lived

### Acceptance Criteria

* Bear super reliably creates space
* Effect is noticeable and satisfying
* Super does not break encounter flow

---

## Task 210 – Implement Bunny Super: Mega Hop

**Status:** DONE

### Objective

Give the Bunny a mobility-focused super with an impactful landing.

### Requirements

* On activation:

  * perform a longer dodge-style leap
  * grant invulnerability during travel
  * create AoE impact on landing

* Keep travel path and landing readable

### Acceptance Criteria

* Bunny super provides a strong repositioning tool
* Landing effect is clear and useful
* Super feels distinct from normal dodge

---

## Task 211 – Implement Cat Super: Frenzy

**Status:** DONE

### Objective

Give the Cat a short offensive burst super.

### Requirements

* On activation:

  * temporarily increase damage and/or attack rate
  * optionally add projectile or melee enhancement

* Add a short active duration

* Keep effect clearly visible to player

### Acceptance Criteria

* Cat super noticeably increases offensive output
* Duration and effect are easy to understand
* Super feels aggressive and character-appropriate

---

## Task 212 – Implement Raccoon Super: Chaos Drop

**Status:** DONE

### Objective

Give the Raccoon a cunning, value-oriented super.

### Requirements

* On activation, create a reward/control effect such as:

  * burst of pickups
  * temporary bonus to pickup drops
  * small crowd-control pulse plus reward generation

* Keep effect on-theme and immediately understandable

### Acceptance Criteria

* Raccoon super feels distinct from other supers
* Effect creates a meaningful momentum swing
* Super reinforces scavenger/cunning identity

---

## Task 213 – Super Meter UI

**Status:** DONE

### Objective

Display super charge clearly during gameplay.

### Requirements

* Add a super meter UI element

* Show:

  * current charge progress
  * ready state when full

* Keep UI readable alongside score, XP, and health indicators

### Acceptance Criteria

* Player can easily tell when super is ready
* Meter updates correctly during gameplay
* UI remains readable during chaotic moments

---

## Task 214 – Super Activation Feedback

**Status:** DONE

### Objective

Make super use feel impactful and unmistakable.

### Requirements

* Add strong feedback for super activation, such as:

  * audio cue
  * flash or burst effect
  * character-specific visual treatment
  * brief banner or icon emphasis

* Ensure each character super has distinct feedback language

### Acceptance Criteria

* Super activation feels powerful
* Character supers are visually distinguishable
* Feedback enhances the moment without obscuring play

---

## Task 215 – Super Balance & Cooldown Tuning

**Status:** DONE

### Objective

Tune supers so they are impactful, earned, and not spammable.

### Requirements

* Tune:

  * charge rate
  * effect strength
  * duration
  * interaction with bosses and dense enemy waves

* Validate that supers feel:

  * worth earning
  * not mandatory every few seconds
  * strong without trivializing the run

### Acceptance Criteria

* Supers feel like clutch or power moments
* Charge pacing supports meaningful decisions
* No super dominates all other gameplay systems

## Task 216 – Aim Assist System Foundation

**Status:** DONE

### Objective

Introduce a modular aim assist system to improve targeting, especially for controller input.

### Requirements

* Create an aim assist module or component

* System should:

  * evaluate nearby enemies
  * influence projectile direction
  * remain optional and configurable

* Keep logic separate from weapon firing code where possible

### Acceptance Criteria

* Aim assist system exists as a reusable component
* Can be enabled/disabled without breaking gameplay
* Does not interfere with non-assisted aiming paths

---

## Task 217 – Detect Input Type (Controller vs Keyboard/Mouse)

**Status:** DONE

### Objective

Apply aim assist primarily when using a controller.

### Requirements

* Detect active input method:

  * controller
  * keyboard/mouse

* Enable aim assist by default for controller

* Keep assist weaker or disabled for mouse input

### Acceptance Criteria

* System correctly detects input type
* Aim assist behavior changes based on input method
* No unintended interference with mouse precision

---

## Task 218 – Define Aim Cone Parameters

**Status:** DONE

### Objective

Define the geometry and constraints of the aim assist cone.

### Requirements

* Define:

  * cone angle (e.g., 15–25 degrees)
  * max assist distance
  * forward direction based on player aim

* Ensure cone:

  * only includes targets in front of player
  * excludes enemies behind player

* Keep values configurable

### Acceptance Criteria

* Cone correctly represents forward aiming space
* Targets outside cone are ignored
* Parameters are easy to tune

---

## Task 219 – Target Selection Within Aim Cone

**Status:** DONE

### Objective

Select the most appropriate enemy target within the aim cone.

### Requirements

* Evaluate enemies inside cone

* Prioritize based on:

  * closest distance (primary)
  * optionally smallest angle offset

* Handle cases:

  * no targets in cone
  * multiple valid targets

### Acceptance Criteria

* System consistently selects a reasonable target
* No erratic or unintuitive target switching
* Graceful fallback when no targets are available

---

## Task 220 – Apply Directional Aim Adjustment

**Status:** DONE

### Objective

Slightly adjust projectile direction toward selected target.

### Requirements

* Blend original aim direction with target direction

* Use configurable assist strength (e.g., 10–30%)

* Ensure:

  * adjustment is subtle
  * player intent is preserved

* Do not snap instantly to target

### Acceptance Criteria

* Projectiles are gently nudged toward targets
* Player can still miss if aim is poor
* Adjustment feels natural and not forced

---

## Task 221 – Distance & Falloff Handling

**Status:** DONE

### Objective

Reduce aim assist influence for distant or edge-case targets.

### Requirements

* Apply falloff based on:

  * distance to target
  * angle offset within cone

* Stronger assist:

  * closer targets
  * more centered targets

* Weaker assist:

  * far or edge-of-cone targets

### Acceptance Criteria

* Nearby enemies receive stronger assist
* Distant targets do not cause unnatural snapping
* Assist feels consistent across scenarios

---

## Task 222 – Integrate Aim Assist with Projectile Weapons

**Status:** DONE

### Objective

Apply aim assist to existing projectile systems (e.g., bottle rocket).

### Requirements

* Hook aim assist into firing logic

* Ensure:

  * only applied at moment of firing
  * does not affect projectile after launch (for now)

* Maintain compatibility with:

  * auto-fire systems
  * future weapon variations

### Acceptance Criteria

* Projectile weapons benefit from aim assist
* No regression in firing behavior
* System works across different weapon types

---

## Task 223 – Debug Visualization for Aim Cone (Optional but Recommended)

**Status:** DONE

### Objective

Provide a visual overlay to validate aim assist behavior.

### Requirements

* Add toggleable debug mode

* Show:

  * aim cone
  * selected target
  * adjusted aim direction

* Keep debug visuals lightweight

### Acceptance Criteria

* Developer can visually inspect aim assist behavior
* Cone and target selection are clearly visible
* Debug mode can be toggled on/off easily

---

## Task 224 – Aim Assist Tuning & Balancing

**Status:** DONE

### Objective

Tune aim assist to feel helpful but not overpowered.

### Requirements

* Adjust:

  * cone angle
  * assist strength
  * distance falloff

* Test with:

  * controller input
  * dense enemy scenarios
  * fast-moving targets

### Acceptance Criteria

* Aim assist improves hit consistency without removing skill
* Players still need to aim intentionally
* No “auto-targeting” feel

---

## Task 225 – Optional Settings Toggle (Future-Friendly)

**Status:** DONE

### Objective

Allow players to control aim assist behavior.

### Requirements

* Add settings option:

  * enable/disable aim assist
  * optional strength slider (future)

* Default:

  * enabled for controller
  * reduced or off for mouse

### Acceptance Criteria

* Player can toggle aim assist
* Settings persist during session
* Feature integrates cleanly with existing options menu

## Task 226 – Bottle Rocket Weapon Identity Refactor

**Status:** DONE

### Objective

Replace the current generic projectile with a themed bottle rocket weapon.

### Requirements

* Reframe the primary ranged projectile as a **bottle rocket**

* Update naming in code and UI where appropriate:

  * projectile references
  * weapon references
  * asset references

* Keep gameplay behavior compatible with the existing firing system

### Acceptance Criteria

* Primary projectile is consistently represented as a bottle rocket
* Naming is clear and thematic across code and presentation
* No regression in current weapon firing behavior

---

## Task 227 – Bottle Rocket Visual Representation

**Status:** DONE

### Objective

Give the projectile a distinct bottle rocket look.

### Requirements

* Create or integrate a bottle rocket visual:

  * simple sprite OR
  * lightweight shape-based representation

* Visual should suggest:

  * rocket body
  * directional orientation
  * readable silhouette at gameplay scale

* Ensure projectile rotates or aligns with travel direction if appropriate

### Acceptance Criteria

* Projectile is visually identifiable as a bottle rocket
* Direction of travel is easy to read
* Visual remains clear during active gameplay

---

## Task 228 – Bottle Rocket Flight Behavior

**Status:** DONE

### Objective

Make bottle rocket motion feel distinct from a generic bullet.

### Requirements

* Update projectile movement to feel like a bottle rocket, such as:

  * fast forward travel
  * slight wobble or instability
  * optional subtle acceleration

* Keep movement readable and predictable enough for gameplay

### Acceptance Criteria

* Bottle rocket feels distinct from the prior projectile
* Motion is thematic without becoming erratic
* Projectile remains reliable as a player weapon

---

## Task 229 – Bottle Rocket Launch Feedback

**Status:** DONE

### Objective

Make firing the bottle rocket feel punchy and satisfying.

### Requirements

* Add launch feedback such as:

  * muzzle flash or spark burst
  * small recoil effect
  * launch sound hook if audio exists
  * brief smoke/confetti trail at launch

* Keep effects lightweight and readable

### Acceptance Criteria

* Firing the weapon has clear launch feedback
* Weapon feels more responsive and satisfying
* Effects do not clutter the screen

---

## Task 230 – Bottle Rocket Trail Effect

**Status:** DONE

### Objective

Add a short flight trail to reinforce motion and identity.

### Requirements

* Add a trailing effect behind the bottle rocket, such as:

  * smoke puffs
  * spark particles
  * confetti streaks

* Keep trail short-lived and performance-friendly

* Ensure trail does not obscure enemies or player

### Acceptance Criteria

* Bottle rocket leaves a readable thematic trail
* Trail improves visual feel without reducing clarity
* Performance remains stable with multiple projectiles

---

## Task 231 – Bottle Rocket Impact Effect

**Status:** DONE

### Objective

Make bottle rocket hits feel explosive and celebratory.

### Requirements

* On impact with enemy or end-of-life condition:

  * trigger pop/explosion effect
  * spawn confetti or spark burst
  * play impact sound hook if available

* Keep explosion visual small and readable in Phase 1

* Ensure hit feedback differs from simple projectile disappearance

### Acceptance Criteria

* Bottle rocket impact is visually satisfying
* Enemy hits feel more impactful than before
* Effects are thematic and easy to read

---

## Task 232 – Bottle Rocket Collision & Damage Validation

**Status:** DONE

### Objective

Ensure the bottle rocket still behaves correctly as a combat projectile.

### Requirements

* Validate:

  * collision with enemies
  * damage application
  * projectile cleanup after impact
  * range/lifetime expiration

* Ensure new visuals/effects do not break damage logic

### Acceptance Criteria

* Bottle rocket damages enemies reliably
* Projectile is removed cleanly after impact or expiration
* No gameplay regressions are introduced

---

## Task 233 – Aim Assist Compatibility for Bottle Rocket

**Status:** DONE

### Objective

Ensure bottle rocket firing works cleanly with the controller aim assist cone system.

### Requirements

* Confirm aim assist adjusts launch direction correctly
* Ensure bottle rocket orientation matches adjusted trajectory
* Validate assist behavior with:

  * close targets
  * moving targets
  * multiple enemies in cone

### Acceptance Criteria

* Aim assist improves bottle rocket targeting without overcorrecting
* Projectile visuals align with final launch direction
* No mismatch exists between aim logic and projectile motion

---

## Task 234 – Bottle Rocket Weapon Tuning

**Status:** DONE

### Objective

Tune bottle rocket stats so it feels fun, readable, and balanced.

### Requirements

* Tune:

  * speed
  * fire rate
  * lifetime/range
  * wobble amount
  * trail density
  * impact effect intensity

* Ensure bottle rocket remains satisfying in both early and mid-run gameplay

### Acceptance Criteria

* Bottle rocket feels distinct and fun to use
* Tuning supports both controller and keyboard play
* Weapon remains effective without overpowering the run

---

## Task 235 – Future Hook Prep for Bottle Rocket Upgrades

**Status:** DONE

### Objective

Prepare the bottle rocket system for later upgrade paths.

### Requirements

* Structure bottle rocket logic so it can support future upgrades such as:

  * multi-shot
  * larger explosions
  * faster rockets
  * homing assist
  * split rockets
  * confetti burst modifiers

* Avoid hardcoding one-off behavior that blocks extension

### Acceptance Criteria

* Bottle rocket system is easy to extend with upgrades later
* Current implementation remains clean and modular
* No major refactor should be needed for future weapon progression


## Task 236 – Add Bear Walking Sprite Sheet Asset to `playerdemo.py`

**Status:** DONE

### Objective

Load the bear walking sprite sheet into the player demo as an animation source.

### Requirements

* Add the bear walking sheet to the expected asset location
* Load the sprite sheet with alpha transparency
* Fail gracefully if the file is missing or cannot be read
* Keep sprite sheet loading separate from demo input/render logic

### Acceptance Criteria

* `playerdemo.py` loads the bear walking sprite sheet successfully
* Missing asset does not crash unexpectedly
* Asset loading is isolated and reusable

---

## Task 237 – Define Sprite Sheet Grid & Frame Extraction

**Status:** DONE

### Objective

Slice the walking sheet into a grid of animation frames.

### Requirements

* Assume and configure:

  * number of columns
  * number of rows

* Extract each cell as a frame using fixed grid dimensions

* Preserve full cell size rather than cropping tightly around the bear

* Store frames in a structure like `frames[row][column]`

### Acceptance Criteria

* Frames are extracted consistently from the sprite sheet
* Each frame has the same dimensions
* Frame extraction can be adjusted from one place if grid values change

---

## Task 238 – Add Row Preview Mode

**Status:** DONE

### Objective

Allow `playerdemo.py` to preview one animation row at a time.

### Requirements

* Add controls to change the active animation row
* Display current row index on screen
* Render the selected row using its extracted frames
* Keep row selection independent from full direction logic for now

### Acceptance Criteria

* User can cycle through sprite sheet rows in the demo
* Current row is clearly identified
* Any row can be previewed without restarting the demo

---

## Task 239 – Add Timed Walk Animation Playback

**Status:** DONE

### Objective

Animate the selected row as a looping walk cycle.

### Requirements

* Add animation playback using time-based frame advancement
* Support configurable playback speed (FPS)
* Loop across the frames in the selected row
* Support pause/play toggle for inspection

### Acceptance Criteria

* Selected row animates smoothly in a loop
* Playback speed is stable and tunable
* Animation can be paused for debugging

---

## Task 240 – Add Direction Mapping for Animated Preview

**Status:** DONE

### Objective

Map directional preview controls to the appropriate sprite sheet rows.

### Requirements

* Add a direction mapping system for:

  * up
  * down
  * left
  * right

* Use left/right row mapping or horizontal flip where appropriate

* Keep mapping configurable in case row meanings change

* Show current direction label on screen

### Acceptance Criteria

* Direction controls switch to the correct animation row
* Left/right handling is stable and visually correct
* Current facing direction is visible in the demo

---

## Task 241 – Add Animated Anchor Alignment

**Status:** DONE

### Objective

Keep the animated bear visually grounded across all frames.

### Requirements

* Render all animation frames using the same anchor strategy
* Use center-bottom anchor by default
* Prevent visible jumping between frames and rows
* Keep anchor logic reusable for future animated characters

### Acceptance Criteria

* Bear remains visually grounded during animation
* No noticeable frame-to-frame jitter from alignment issues
* Anchor logic works consistently across rows

---

## Task 242 – Add Fixed Hitbox Overlay for Animated Frames

**Status:** DONE

### Objective

Validate a stable gameplay hitbox against the walking animation.

### Requirements

* Add a fixed player hitbox independent of frame pixels
* Base hitbox on torso/body area, not ears or hat
* Render hitbox overlay in the demo
* Keep hitbox size and offset configurable

### Acceptance Criteria

* Hitbox stays stable while animation plays
* Hitbox feels centered on the animated bear body
* Overlay helps validate fairness and consistency

---

## Task 243 – Add Debug Overlay for Frame Bounds and Anchor

**Status:** DONE

### Objective

Make sprite alignment issues easy to inspect during animation playback.

### Requirements

* Add toggleable overlays for:

  * frame bounds
  * anchor point
  * hitbox
  * current row/frame index

* Keep overlays lightweight and readable

* Add a key to enable/disable debug mode

### Acceptance Criteria

* Debug overlays can be toggled on and off
* Frame bounds, anchor, and hitbox are clearly visible
* Debug mode is useful for tuning alignment and scale

---

## Task 244 – Add Scale and Offset Tuning Controls for Animated Preview

**Status:** DONE

### Objective

Make it easy to tune how the animated bear is presented in the demo.

### Requirements

* Add controls or editable constants for:

  * display scale
  * render X/Y offset
  * hitbox radius
  * hitbox vertical offset

* Ensure adjustments are reflected immediately

### Acceptance Criteria

* Scale and offset can be tuned quickly in the demo
* Animated bear remains centered and readable
* Tuning controls improve iteration speed

---

## Task 245 – Add Idle vs Walk Preview State

**Status:** DONE

### Objective

Support a simple idle presentation alongside the walk animation.

### Requirements

* Add a mode to show:

  * walking loop
  * idle frame or paused default frame

* Allow toggling between idle and walk preview

* Keep behavior simple and useful for visual review

### Acceptance Criteria

* Demo can switch between idle and walk preview modes
* Idle mode provides a stable frame for inspection
* Walk mode remains smooth and readable

---

## Task 246 – Prepare Animated Bear Config for Reuse

**Status:** DONE

### Objective

Package the bear animation settings into a reusable character config.

### Requirements

* Create a config or data structure containing:

  * sprite sheet path
  * row/column counts
  * direction-to-row mapping
  * scale
  * anchor settings
  * hitbox settings
  * animation FPS

* Keep demo-only controls separate from reusable config

### Acceptance Criteria

* Bear animation setup is defined in one reusable place
* Future party animal sprite sheets can use the same structure
* Demo code remains clean and modular

---

## Task 247 – Validate Bear Animation Readiness for Main Game Integration

**Status:** DONE

### Objective

Confirm the animated bear setup can be integrated into the main player system later.

### Requirements

* Separate reusable animation/render logic from demo-specific UI and controls
* Confirm direction mapping, anchor, and hitbox logic are portable
* Avoid one-off demo hacks that would complicate game integration

### Acceptance Criteria

* Animated bear system is ready for reuse in the main game
* Minimal refactor should be needed later
* Demo remains a safe visual sandbox

## Task 248 – Create Main-Game Player Animation System Foundation

**Status:** DONE

### Objective

Add a reusable player animation system to the main game.

### Requirements

* Create a player animation component or module responsible for:

  * loading animation assets
  * tracking animation state
  * advancing animation frames
  * returning the correct current frame for rendering

* Keep animation logic separate from player movement/combat logic

* Design for reuse across future party animal characters

### Acceptance Criteria

* Main game has a dedicated player animation system
* Animation state is not hardcoded inside movement logic
* System is reusable for future characters

---

## Task 249 – Integrate Bear Idle and Walk Animation Assets

**Status:** DONE

### Objective

Use the existing `bear_idle` and `bear_walking` sheets as the player’s visual source in the main game.

### Requirements

* Load both animation sheets into the main game asset pipeline

* Slice each sheet into frames using configurable metadata

* Support at minimum:

  * idle loop
  * walking loop

* Fail gracefully if assets are missing or invalid

### Acceptance Criteria

* Main game loads both bear animation sheets successfully
* Idle and walk frames are available to the player renderer
* Asset loading is modular and robust

---

## Task 250 – Add Player Animation State Switching

**Status:** DONE

### Objective

Switch between idle and walking animations based on player movement.

### Requirements

* Use idle animation when player is not moving
* Use walking animation when player movement input is active
* Ensure animation transitions are immediate and stable
* Prevent flickering or rapid state oscillation near zero movement

### Acceptance Criteria

* Player shows idle animation while standing still
* Player shows walk animation while moving
* State switching feels smooth and predictable

---

## Task 251 – Preserve Anchor Alignment Across Animations

**Status:** DONE

### Objective

Ensure the player remains visually grounded when switching between idle and walk loops.

### Requirements

* Apply the same anchor alignment strategy used in `playerdemo`

* Keep the player visually stable across:

  * idle frames
  * walking frames
  * direction changes if supported

* Reuse center-bottom anchor logic where practical

### Acceptance Criteria

* Player does not visibly jump when changing animation states
* Animation remains grounded during movement
* Alignment logic is consistent with demo behavior

---

## Task 252 – Integrate Fixed Gameplay Hitbox with Animated Player

**Status:** DONE

### Objective

Keep gameplay collision stable while using animated visuals.

### Requirements

* Continue using a fixed gameplay hitbox independent of animation frame bounds
* Ensure hitbox remains tied to the player’s body center
* Validate that animation changes do not affect collision fairness

### Acceptance Criteria

* Animated player uses a stable hitbox
* Collisions feel fair and predictable
* No animation frame causes collision inconsistency

---

## Task 253 – Add Directional Facing Support for Animated Bear

**Status:** DONE

### Objective

Support directional presentation for the animated bear in the main game.

### Requirements

* Define how direction is represented in the current animation setup

* If only one walk/idle loop exists:

  * support horizontal flipping where appropriate
  * preserve readability

* Keep direction logic configurable so future assets can use directional sheets later

### Acceptance Criteria

* Animated bear faces appropriately during gameplay
* Direction logic is stable and readable
* Current implementation does not block future directional upgrades

---

## Task 254 – Update Player Renderer to Use Animation Frames

**Status:** DONE

### Objective

Replace static player rendering with animated frame rendering in the main game.

### Requirements

* Update the player render path to use the current frame from the animation system

* Preserve:

  * scaling
  * layering
  * camera/world positioning
  * player clarity against background and effects

* Keep rendering modular

### Acceptance Criteria

* Player is rendered using animated frames during gameplay
* No regressions in player visibility or layering
* Rendering path remains clean and reusable

---

## Task 255 – Add Animation Timing Tuning

**Status:** DONE

### Objective

Tune idle and walk animation playback speed for game feel.

### Requirements

* Add configurable FPS or playback speed for:

  * idle loop
  * walk loop

* Ensure:

  * idle feels alive but not distracting
  * walk feels responsive and readable

* Allow tuning without deep code changes

### Acceptance Criteria

* Idle and walk loops play at appropriate speeds
* Animation speed supports gameplay feel
* Timing values are easy to adjust

---

## Task 256 – Validate Interaction with Core Gameplay Systems

**Status:** DONE

### Objective

Ensure animated player integration does not break existing gameplay systems.

### Requirements

* Validate compatibility with:

  * movement
  * dodge
  * health system
  * weapon firing
  * damage feedback
  * aim assist
  * pause/state changes

* Ensure animation continues or pauses appropriately by game state

### Acceptance Criteria

* Animated player works correctly with all core systems
* No gameplay regressions are introduced
* State changes behave correctly with animation playback

---

## Task 257 – Add Debug Overlay for In-Game Animation Validation

**Status:** DONE

### Objective

Make it easy to validate animated player alignment inside the real game.

### Requirements

* Add optional debug overlays for:

  * player hitbox
  * anchor point
  * current animation state
  * current frame index

* Keep overlay lightweight and toggleable

### Acceptance Criteria

* Debug overlay can be enabled during gameplay
* Alignment and collision can be inspected easily
* Overlay assists tuning without cluttering normal play

---

## Task 258 – Prepare Character Animation Config for Future Party Animals

**Status:** DONE

### Objective

Generalize the bear animation setup so other party animals can reuse the same system.

### Requirements

* Define a reusable animation config structure containing:

  * asset paths
  * frame counts
  * playback speed
  * scale
  * anchor settings
  * flip rules

* Ensure bunny, cat, raccoon, and future characters can plug into the same system later

### Acceptance Criteria

* Bear animation setup is no longer a one-off implementation
* Animation system is ready for future party animals
* Main game can support multiple animated character sets with minimal refactor


## Task 259 – Bottle Rocket Lifetime Explosion

**Status:** DONE

### Objective

Make bottle rockets detonate automatically after traveling a limited distance.

### Requirements

* Add a maximum travel distance or lifetime for bottle rockets

* When the rocket reaches that limit:

  * trigger an explosion/pop effect
  * remove the projectile cleanly

* Preserve normal explosion behavior on enemy impact

* Keep the distance configurable

### Acceptance Criteria

* Bottle rockets explode reliably after traveling their maximum range
* Expiration explosion feels intentional, not like a disappearance
* No orphaned projectiles remain after detonation

---

## Task 260 – Bottle Rocket Trajectory Decay

**Status:** DONE

### Objective

Make bottle rocket flight lose stability or effectiveness over time.

### Requirements

* Add trajectory decay behavior such as:

  * slight downward arc
  * increasing wobble over distance
  * gradual speed reduction
  * mild drift from original path

* Keep behavior readable and thematic

* Avoid making the projectile feel random or uncontrollable

### Acceptance Criteria

* Bottle rocket flight feels less like a perfect bullet
* Decay is noticeable but still playable
* Projectile remains understandable to the player

---

## Task 261 – Distance-Based Flight Tuning

**Status:** DONE

### Objective

Tune bottle rocket motion so its travel arc and detonation feel satisfying.

### Requirements

* Tune:

  * initial speed
  * decay rate
  * wobble amount
  * travel distance before explosion

* Ensure bottle rockets feel:

  * energetic at launch
  * unstable later in flight
  * consistent enough for player skill

### Acceptance Criteria

* Bottle rocket has a readable travel profile
* Range feels intentional and useful
* Tuning supports both keyboard and controller play

---

## Task 262 – End-of-Range Explosion Effect

**Status:** DONE

### Objective

Give expired bottle rockets a thematic firework-style payoff.

### Requirements

* When bottle rocket reaches max distance:

  * trigger a small explosion burst
  * add sparks/confetti/firework pop visuals
  * optionally add sound hook if audio exists

* Differentiate this visually from direct-hit explosion if practical

* Keep the effect lightweight and readable

### Acceptance Criteria

* End-of-range detonation feels satisfying
* Explosion reinforces bottle rocket identity
* Effect does not clutter gameplay

---

## Task 263 – Explosion Radius & Enemy Interaction

**Status:** DONE

### Objective

Decide whether bottle rocket explosions affect nearby enemies on detonation.

### Requirements

* Define explosion interaction:

  * direct-hit only
  * or small AoE on detonation

* If AoE is added:

  * keep radius modest
  * prevent it from overpowering base weapon balance

* Ensure both impact and end-of-range explosions follow the same damage rules where intended

### Acceptance Criteria

* Explosion damage behavior is clear and consistent
* AoE, if present, is readable and balanced
* Bottle rocket remains thematic without becoming overpowered

---

## Task 264 – Visual Trail Update for Decaying Flight

**Status:** DONE

### Objective

Make the bottle rocket trail reflect its decaying trajectory.

### Requirements

* Update trail visuals so they support the new motion style, such as:

  * more erratic sparks later in flight
  * smoke tapering
  * slight visual instability near expiration

* Keep trail effects subtle and performant

### Acceptance Criteria

* Trail visually supports the bottle rocket’s changing flight
* Decay is easier to read through effects
* Visuals remain clean in busy gameplay

---

## Task 265 – Aim Assist Compatibility with Decaying Rockets

**Status:** DONE

### Objective

Ensure controller aim assist still feels useful with bottle rockets that decay in flight.

### Requirements

* Validate aim assist with:

  * limited range
  * decaying trajectory
  * expiration explosions

* Ensure assist influences launch direction only

* Avoid making mid-flight decay feel like aim assist failure

### Acceptance Criteria

* Aim assist remains helpful for bottle rockets
* Projectile decay feels intentional, not inaccurate
* Controller targeting remains satisfying

---

## Task 266 – Bottle Rocket Readability & Balance Pass

**Status:** DONE

### Objective

Tune the more thematic bottle rocket so it remains fun, readable, and effective.

### Requirements

* Validate:

  * launch feel
  * travel arc
  * explosion timing
  * enemy hit consistency
  * visual clarity in crowded fights

* Tune to ensure rockets feel like:

  * celebratory
  * slightly chaotic
  * still skill-based

### Acceptance Criteria

* Bottle rockets feel more thematic than the previous projectile
* They remain reliable enough for normal play
* The weapon is fun without becoming messy or frustrating

## Task 267 – Weapon Choice System Foundation

**Status:** DONE

### Objective

Create a system that supports multiple player weapon options instead of a single hardcoded primary weapon.

### Requirements

* Refactor player weapon handling so the active weapon is selected from a weapon definition/config

* Support at minimum:

  * Bottle Rocket
  * Sparkler

* Keep weapon logic modular and reusable

* Avoid hardcoding attack behavior directly into player update logic

### Acceptance Criteria

* Player can use a weapon selected from a configurable system
* Bottle Rocket and Sparkler can coexist in the codebase cleanly
* Weapon switching/selection architecture is ready for expansion

---

## Task 268 – Sparkler Weapon Definition

**Status:** DONE

### Objective

Add Sparkler as a valid weapon option in the weapon system.

### Requirements

* Define Sparkler weapon metadata including:

  * id
  * display name
  * type (melee)
  * damage
  * range
  * attack cadence/cooldown

* Keep values tunable from one place

* Distinguish Sparkler clearly from projectile weapons

### Acceptance Criteria

* Sparkler exists as a selectable weapon definition
* Weapon properties are centralized and editable
* Sparkler is recognized by the weapon system as a melee weapon

---

## Task 269 – Sparkler Baton Attack Shape

**Status:** DONE

### Objective

Implement the Sparkler as a short-range baton-style melee attack.

### Requirements

* Attack should be directional and close-range

* Use a simple hit shape such as:

  * short arc
  * cone
  * short forward sweep

* Base direction on player facing or aim direction

* Keep attack readable and tightly scoped

### Acceptance Criteria

* Sparkler attacks in front of the player
* Attack shape is visually and mechanically distinct from Bottle Rocket
* Melee strike feels deliberate and directional

---

## Task 270 – Sparkler Attack Timing & Cooldown

**Status:** DONE

### Objective

Make Sparkler attacks feel responsive but not spammy.

### Requirements

* Add attack cadence/cooldown for Sparkler swings
* Support repeated use while attack input is held or triggered, depending on current weapon input model
* Ensure cooldown timing is clear and stable

### Acceptance Criteria

* Sparkler attack fires at a predictable cadence
* Attack timing feels responsive
* Weapon cannot be spammed beyond intended rate

---

## Task 271 – Sparkler Enemy Hit Detection

**Status:** DONE

### Objective

Apply damage correctly to enemies struck by the Sparkler.

### Requirements

* Detect enemies inside the sparkler hit area
* Apply damage once per valid strike
* Prevent duplicate hit registration during the same attack window
* Support multiple enemy hits if intended by design

### Acceptance Criteria

* Enemies in the sparkler attack zone take damage reliably
* No duplicate damage bugs occur during a single swing
* Hit detection is fair and consistent

---

## Task 272 – Sparkler Visual Representation

**Status:** DONE

### Objective

Make the Sparkler attack visually clear and on-theme.

### Requirements

* Add visual feedback for the sparkler swing, such as:

  * short glowing baton arc
  * spark burst
  * bright tip/trail
  * brief flare at attack start

* Keep effects lightweight and readable in crowded gameplay

### Acceptance Criteria

* Sparkler attack is easy to see and understand
* Visual style feels thematic and distinct from projectile attacks
* Effects do not clutter the screen

---

## Task 273 – Sparkler Audio Hook & Attack Feel

**Status:** DONE

### Objective

Give the Sparkler attack satisfying moment-to-moment feel.

### Requirements

* Add hooks for:

  * swing sound
  * spark crackle
  * hit sound on enemy contact

* Optional:

  * subtle player pose emphasis
  * minor recoil or swing follow-through

### Acceptance Criteria

* Sparkler attack feels more tactile and satisfying
* Audio hooks are ready even if final assets are not yet added
* Attack feedback improves melee readability

---

## Task 274 – Add Sparkler as a Player Weapon Choice

**Status:** DONE

### Objective

Allow the player to select Sparkler as a weapon option.

### Requirements

* Add a selection path for Sparkler, such as:

  * character/start selection
  * debug/dev toggle
  * temporary menu option

* Ensure selection flow is simple and does not disrupt existing systems

* Keep the system extensible for future weapons

### Acceptance Criteria

* Player can start or test a run with Sparkler selected
* Sparkler selection is clearly reflected in gameplay
* Bottle Rocket remains available as an alternative weapon choice

---

## Task 275 – Sparkler Integration with Aim/Facing Logic

**Status:** DONE

### Objective

Ensure Sparkler direction uses the correct player orientation or aim source.

### Requirements

* Define how Sparkler chooses attack direction:

  * movement direction
  * facing direction
  * controller aim direction
  * last non-zero input direction

* Keep behavior consistent and readable

* Ensure controller support feels good

### Acceptance Criteria

* Sparkler attack direction is predictable
* Direction logic works on both keyboard and controller
* Attack does not fire in confusing or unintended directions

---

## Task 276 – Sparkler Balance Pass (Baseline Melee Choice)

**Status:** DONE

### Objective

Tune Sparkler so it is a viable but distinct alternative to Bottle Rocket.

### Requirements

* Tune:

  * damage
  * range
  * cooldown
  * enemy hit count
  * visual clarity

* Validate relative strengths:

  * Sparkler should reward proximity and positioning
  * Bottle Rocket should remain safer at range

### Acceptance Criteria

* Sparkler feels strong enough to choose
* It does not invalidate Bottle Rocket
* Melee gameplay feels riskier but rewarding

---

## Task 277 – Future Evolution Hooks for Sparkler

**Status:** DONE

### Objective

Prepare Sparkler for later upgrade/evolution into wider melee and aura forms.

### Requirements

* Structure Sparkler logic so it can later support:

  * wider arc
  * longer range
  * faster swings
  * spark projectiles
  * aura evolution

* Avoid hardcoding a one-off melee implementation that blocks future growth

### Acceptance Criteria

* Sparkler implementation is ready for future progression upgrades
* Current baton-style version remains clean and simple
* No major refactor should be needed for later evolution

## Task 278 – XP Drop Entity System Foundation

**Status:** DONE

### Objective

Create a world pickup entity for XP that drops from defeated enemies.

### Requirements

* Add a new pickup/entity type for XP drops

* XP drops should:

  * exist in the world after enemy death
  * be collectible by the player
  * store an XP value

* Keep XP drops separate from direct XP award logic

* Design the system so future pickups can reuse the same foundation

### Acceptance Criteria

* XP drops can be spawned as world entities
* Each drop carries a configurable XP value
* System is modular and reusable for future pickups

---

## Task 279 – Enemy Death Refactor to Spawn XP Drops

**Status:** DONE

### Objective

Change enemy deaths so they spawn XP drops instead of awarding XP instantly.

### Requirements

* Remove direct XP gain on enemy death

* On enemy death:

  * spawn one or more XP drops
  * assign XP amount based on enemy type

* Support at minimum:

  * balloons
  * piñatas
  * sprayers
  * snakes
  * bosses

### Acceptance Criteria

* Enemies no longer grant XP instantly
* Enemy deaths reliably create XP drops
* XP values vary appropriately by enemy type

---

## Task 280 – XP Drop Visual Identity

**Status:** DONE

### Objective

Make XP drops readable, attractive, and on-theme.

### Requirements

* Add a clear visual for XP drops, such as:

  * glowing confetti cluster
  * candy-like orb
  * celebratory sparkle pickup

* Ensure drops:

  * are visible against the background
  * are distinguishable from enemies/projectiles
  * remain readable during chaotic gameplay

### Acceptance Criteria

* XP drops are easy to identify in the world
* Visual style fits the game theme
* Pickup visibility is maintained in active combat

---

## Task 281 – Player XP Pickup Collision

**Status:** DONE

### Objective

Allow the player to collect XP drops by moving over them.

### Requirements

* Add collision/overlap handling between player and XP drops

* On collection:

  * add XP to player progression
  * remove drop cleanly
  * trigger optional feedback hook

* Prevent duplicate collection events

### Acceptance Criteria

* Player can collect XP drops reliably
* XP is awarded only when pickup is collected
* Drops are removed cleanly after collection

---

## Task 282 – XP Pickup Feedback

**Status:** DONE

### Objective

Make collecting XP feel rewarding and noticeable.

### Requirements

* Add feedback for XP pickup, such as:

  * small sparkle burst
  * subtle sound hook
  * floating XP text or pulse
  * XP bar response

* Keep effects lightweight and readable

### Acceptance Criteria

* XP collection feels satisfying
* Feedback clearly communicates pickup success
* Effects do not clutter gameplay

---

## Task 283 – XP Value Distribution by Enemy Type

**Status:** DONE

### Objective

Define how much XP each enemy should drop.

### Requirements

* Configure XP drop values for each enemy type

* Suggested pattern:

  * balloons = low
  * piñatas = medium/high
  * sprayers = medium
  * snakes = medium/high
  * bosses = large reward

* Keep values centralized and tunable

### Acceptance Criteria

* XP values are configurable from one place
* Different enemy types feel appropriately rewarding
* XP flow supports intended progression pacing

---

## Task 284 – XP Drop Lifetime & Cleanup Rules

**Status:** DONE

### Objective

Prevent XP drops from accumulating indefinitely and hurting performance.

### Requirements

* Define lifetime/cleanup rules for XP drops, such as:

  * persist for a long but finite duration
  * optional fade before expiration

* Ensure cleanup does not feel unfair or too aggressive

* Remove expired drops safely

### Acceptance Criteria

* XP drops do not accumulate forever
* Cleanup behavior is stable and unobtrusive
* Performance remains consistent during long runs

---

## Task 285 – XP Pickup Radius / Magnetism Foundation

**Status:** DONE

### Objective

Improve pickup feel by allowing nearby XP drops to move toward the player.

### Requirements

* Add a small collection radius or magnet effect

* XP drops near the player should:

  * be attracted slightly
  * remain collectible without pixel-perfect overlap

* Keep magnetism modest in the baseline version

### Acceptance Criteria

* XP pickup feels smooth and forgiving
* Magnet effect does not trivialize map movement
* Collection remains readable and satisfying

---

## Task 286 – XP Pickup Integration with Character Passives

**Status:** DONE

### Objective

Ensure the XP pickup system supports character-specific passives and future upgrade hooks.

### Requirements

* Integrate XP drop collection with character modifiers such as:

  * Raccoon increased pickup radius or XP gain

* Keep the system extensible for future upgrades like:

  * stronger magnetism
  * bonus XP
  * pickup chaining

### Acceptance Criteria

* Character passives can influence XP pickup behavior cleanly
* XP pickup system is extensible for future progression upgrades
* No hardcoded assumptions block future tuning

---

## Task 287 – XP-Driven Level-Up Flow Validation

**Status:** DONE

### Objective

Ensure level progression still feels correct after switching to collectible XP drops.

### Requirements

* Validate:

  * XP gain pacing
  * level-up frequency
  * enemy pressure vs reward collection
  * readability of progression loop

* Adjust XP values, drop counts, or collection feel as needed

### Acceptance Criteria

* XP pickup system supports a satisfying level-up cadence
* Collecting XP adds meaningful movement decisions
* Progression remains fun and understandable

---

## Task 288 – XP Pickup Balance & Playtest Pass

**Status:** DONE

### Objective

Tune XP pickups so they improve gameplay without becoming frustrating or trivial.

### Requirements

* Tune:

  * drop size/visibility
  * XP value
  * pickup radius
  * drop persistence time
  * boss reward volume

* Validate behavior in:

  * early runs
  * crowded mid-game
  * boss encounters

### Acceptance Criteria

* XP pickups feel rewarding and manageable
* Players are encouraged to move and collect without undue frustration
* System improves the survivor gameplay loop overall

## Task 289 – Upgrade Tagging System Foundation

**Status:** DONE

### Objective

Introduce a tagging system for upgrades to support weapon evolution conditions.

### Requirements

* Each upgrade can include one or more tags, such as:

  * `rocket_explosion`
  * `rocket_split`
  * `sparkler_range`
  * `sparkler_speed`

* Store tags in upgrade definitions

* Ensure tags are easily queryable at runtime

### Acceptance Criteria

* Upgrades can be tagged with meaningful identifiers
* Player state can track acquired tags
* System is extensible for future upgrades

---

## Task 290 – Player Upgrade State Tracking

**Status:** DONE

### Objective

Track all upgrades and tags acquired during a run.

### Requirements

* Maintain a structure for:

  * acquired upgrades
  * accumulated tags

* Ensure:

  * tags persist across the run
  * tags can be queried efficiently

### Acceptance Criteria

* Player upgrade state reflects all chosen upgrades
* Tag queries return correct results
* System supports evolution checks

---

## Task 291 – Evolution Definition System

**Status:** DONE

### Objective

Define weapon evolutions using tag combinations.

### Requirements

* Create a structure for evolutions including:

  * weapon id
  * required tags
  * resulting evolved form

* Example:

  * Bottle Rocket + (`rocket_explosion` + `rocket_split`) → Burst Rocket

* Keep definitions centralized and data-driven

### Acceptance Criteria

* Evolutions are defined without hardcoding logic into weapons
* New evolutions can be added easily
* System supports multiple weapons

---

## Task 292 – Evolution Condition Checker

**Status:** DONE

### Objective

Detect when a player meets the requirements for a weapon evolution.

### Requirements

* On upgrade acquisition:

  * check if required tag combinations are satisfied

* Ensure:

  * evolutions trigger only once
  * no duplicate evolutions occur

### Acceptance Criteria

* Evolution conditions are evaluated correctly
* Evolutions trigger when requirements are met
* System prevents repeated triggers

---

## Task 293 – Weapon Evolution Application

**Status:** DONE

### Objective

Transform a weapon into its evolved form.

### Requirements

* Replace or modify weapon behavior when evolved:

  * update projectile logic
  * update visuals/effects
  * update damage behavior

* Preserve compatibility with:

  * aim assist
  * existing upgrades

### Acceptance Criteria

* Weapon behavior changes correctly after evolution
* No regressions in firing or damage systems
* Evolution feels distinct from base weapon

---

## Task 294 – Bottle Rocket Evolution: Burst Rocket

**Status:** DONE

### Objective

Create the first bottle rocket evolution that splits into multiple projectiles.

### Requirements

* Trigger condition:

  * `rocket_explosion` + `rocket_split`

* On explosion:

  * spawn multiple smaller rockets or fragments
  * maintain readability and performance

* Keep spread controlled and predictable

### Acceptance Criteria

* Burst Rocket triggers correctly
* Explosion produces multiple projectiles
* Behavior is fun and readable

---

## Task 295 – Bottle Rocket Evolution: Big Pop Rocket

**Status:** DONE

### Objective

Create a bottle rocket evolution with larger explosion impact.

### Requirements

* Trigger condition:

  * `rocket_explosion` + `rocket_power`

* Increase:

  * explosion radius
  * visual intensity

* Keep balance so it doesn’t trivialize gameplay

### Acceptance Criteria

* Explosion is noticeably larger and more impactful
* Evolution triggers correctly
* Gameplay remains balanced

---

## Task 296 – Sparkler Evolution: Wide Arc

**Status:** DONE

### Objective

Enhance sparkler melee reach and coverage.

### Requirements

* Trigger condition:

  * `sparkler_range` + `sparkler_speed`

* Increase:

  * attack arc width
  * slightly increase range

* Maintain directional feel

### Acceptance Criteria

* Sparkler covers a larger area
* Attack remains readable and controlled
* Evolution feels like a clear upgrade

---

## Task 297 – Sparkler Evolution: Spark Aura

**Status:** DONE

### Objective

Transform sparkler into a continuous damage aura.

### Requirements

* Trigger condition:

  * `sparkler_range` + `sparkler_persistence`

* Replace baton behavior with:

  * circular damage aura
  * periodic damage ticks

* Add clear visual identity for aura

### Acceptance Criteria

* Sparkler transitions into aura behavior
* Damage is applied consistently over time
* Aura is visually clear and distinct

---

## Task 298 – Evolution Feedback System

**Status:** DONE

### Objective

Make weapon evolutions feel like impactful moments.

### Requirements

* On evolution trigger:

  * brief pause or slowdown
  * visual burst (confetti/firework)
  * optional sound cue
  * optional on-screen text (e.g., “EVOLVED”)

* Ensure feedback is noticeable but not disruptive

### Acceptance Criteria

* Evolution events feel rewarding and memorable
* Player clearly understands an evolution occurred
* Feedback integrates smoothly with gameplay

---

## Task 299 – Evolution UI Indicator

**Status:** DONE

### Objective

Show players their weapon evolution state.

### Requirements

* Indicate:

  * current weapon form
  * whether evolution has occurred

* Optional:

  * show partial progress (future enhancement)

* Keep UI minimal and readable

### Acceptance Criteria

* Player can identify evolved weapons visually or via UI
* UI remains clean and non-intrusive
* Evolution state is clear during gameplay

---

## Task 300 – Evolution Balance & Playtest Pass

**Status:** DONE

### Objective

Ensure evolutions feel powerful but not game-breaking.

### Requirements

* Validate:

  * evolution frequency
  * power spike impact
  * synergy with enemies and bosses
  * performance under heavy effects

* Adjust:

  * tag requirements
  * effect strength
  * spawn counts

### Acceptance Criteria

* Evolutions feel exciting but fair
* Builds feel distinct across runs
* System supports replayability without overpowering gameplay

---

## Task 301 – Meta Progression Data Structure Foundation

**Status:** DONE

### Objective

Create a data structure to track persistent character unlocks across game sessions.

### Requirements

* Define a meta progression structure that includes:

  * unlocked characters list
  * unlock conditions met

* Keep data simple and extensible for future meta features

* Store in a separate file from settings (e.g., `meta_progression.json`)

### Acceptance Criteria

* Meta progression data can be loaded and saved
* Structure supports character unlock tracking
* Data is isolated from runtime settings

---

## Task 302 – Character Unlock Conditions Definition

**Status:** DONE

### Objective

Define the requirements for unlocking each character.

### Requirements

* Create unlock conditions such as:

  * Bear: unlocked by default
  * Bunny: complete 5 runs
  * Cat: reach high score of 10,000
  * Raccoon: defeat 10 bosses

* Keep conditions data-driven and tunable

* Ensure conditions are achievable but require progression

### Acceptance Criteria

* Each character has clear unlock requirements
* Conditions are balanced for replayability
* System can check conditions against player progress

---

## Task 303 – Meta Progression Persistence

**Status:** DONE

### Objective

Implement saving and loading of meta progression data.

### Requirements

* Load meta progression on game start
* Save after unlock achievements
* Handle missing/corrupt files gracefully
* Integrate with existing save system patterns

### Acceptance Criteria

* Unlocks persist across game sessions
* Data loads correctly on startup
* No crashes from missing meta files

---

## Task 304 – Character Unlock State Tracking

**Status:** DONE

### Objective

Track which characters are unlocked based on meta progression.

### Requirements

* Check unlock conditions against current meta state
* Provide a way to query if a character is available
* Update unlock state when conditions are met

### Acceptance Criteria

* Character availability is determined correctly
* Unlocks trigger when conditions are satisfied
* System integrates with character selection logic

---

## Task 305 – Locked Character UI Presentation

**Status:** DONE

### Objective

Show locked characters clearly in the character selection UI.

### Requirements

* For locked characters, display:

  * locked icon or overlay
  * unlock requirement hint
  * prevent selection

* Keep presentation consistent with existing UI style

### Acceptance Criteria

* Locked characters are visually distinct
* Players understand how to unlock them
* UI remains clean and readable

---

## Task 306 – Unlock Achievement Feedback

**Status:** DONE

### Objective

Provide satisfying feedback when a character is unlocked.

### Requirements

* On unlock:

  * show notification or popup
  * optional sound/visual effect
  * update UI immediately

* Keep feedback lightweight and thematic

### Acceptance Criteria

* Unlocking a character feels rewarding
* Feedback is clear and non-disruptive
* Player understands the unlock occurred

---

## Task 307 – Integration with Start Menu

**Status:** DONE

### Objective

Ensure character selection respects unlock state.

### Requirements

* Update start menu to show only unlocked characters
* Allow selection of unlocked characters
* Maintain compatibility with existing menu flow

### Acceptance Criteria

* Only unlocked characters can be selected
* Start menu updates correctly after unlocks
* No regressions in menu navigation

---

## Task 308 – Unlock Balance and Validation

**Status:** DONE

### Objective

Tune unlock conditions and validate the system works end-to-end.

### Requirements

* Test unlock paths for each character
* Adjust conditions for fair progression
* Ensure unlocks encourage replay without frustration

### Acceptance Criteria

* Unlock conditions are achievable and motivating
* System works reliably in gameplay
* Meta progression enhances replayability

## Task 312 – Add Evolution Tags for New Weapon Behaviors

**Status:** DONE

### Objective

Extend the upgrade tagging system to support new evolution paths.

### Requirements

* Add new tags:

  * `rocket_sticky`
  * `rocket_bounce`
  * `sparkler_orbit`
  * `sparkler_persistence`

* Ensure tags:

  * are integrated into upgrade definitions
  * can be queried by the evolution system

### Acceptance Criteria

* New tags are recognized by the system
* Tags can be combined with existing ones
* No regression in existing evolution checks

---

## Task 313 – Define New Evolution Conditions

**Status:** DONE

### Objective

Add evolution definitions for the new weapon variants.

### Requirements

* Define:

### Bottle Rocket Evolutions

* **Delayed Blast Rocket**

  * requires: `rocket_explosion` + `rocket_sticky`

* **Pinball Rocket**

  * requires: `rocket_bounce` + `rocket_speed`

### Sparkler Evolutions

* **Orbiting Sparklers**

  * requires: `sparkler_orbit` + `sparkler_speed`

* **Spark Aura**

  * requires: `sparkler_range` + `sparkler_persistence`

* Store all definitions in centralized evolution config

### Acceptance Criteria

* All four evolutions are defined in the system
* Conditions are clear and data-driven
* Evolutions are discoverable through upgrades

---

## Task 314 – Bottle Rocket Evolution: Delayed Blast (Sticky Rocket)

**Status:** DONE

### Objective

Implement rockets that stick to enemies and explode after a delay.

### Requirements

* On hit:

  * rocket attaches to enemy
  * start short countdown timer

* After delay:

  * trigger explosion at enemy position
  * apply damage

* Ensure:

  * visual indicator for “armed” rocket
  * no duplicate attachment stacking bugs

### Acceptance Criteria

* Rockets visibly stick to enemies
* Explosion occurs after delay
* Behavior is readable and satisfying

---

## Task 315 – Delayed Blast Visual & Feedback

**Status:** DONE

### Objective

Make sticky rockets clearly communicate delayed detonation.

### Requirements

* Add:

  * blinking or glowing indicator while attached
  * small buildup effect before explosion
  * distinct sound cue (if available)

* Ensure clarity in crowded combat

### Acceptance Criteria

* Player can clearly identify armed rockets
* Explosion timing is readable
* Feedback enhances anticipation

---

## Task 316 – Bottle Rocket Evolution: Pinball Rockets

**Status:** DONE

### Objective

Implement rockets that bounce between enemies.

### Requirements

* On impact:

  * redirect rocket toward another nearby enemy
  * limit number of bounces

* Define:

  * max bounce count
  * targeting rules (nearest enemy)

* Ensure:

  * no infinite loops
  * predictable behavior

### Acceptance Criteria

* Rockets chain between enemies
* Bounce count is respected
* Behavior is fun and readable

---

## Task 317 – Pinball Rocket Targeting Logic

**Status:** DONE

### Objective

Ensure bounce targeting feels intentional and fair.

### Requirements

* Select next target based on:

  * proximity
  * not previously hit (if possible)

* Fallback behavior:

  * expire if no valid target exists

### Acceptance Criteria

* Bounce targeting feels consistent
* Rockets do not behave randomly
* Edge cases handled cleanly

---

## Task 318 – Sparkler Evolution: Orbiting Sparklers

**Status:** DONE

### Objective

Create orbiting spark projectiles around the player.

### Requirements

* Spawn orbiting elements:

  * rotate around player
  * maintain fixed radius

* Apply:

  * contact damage to enemies
  * consistent rotation speed

* Ensure:

  * visual clarity
  * stable orbit behavior

### Acceptance Criteria

* Sparks orbit smoothly around the player
* Enemies take damage on contact
* System performs well under load

---

## Task 319 – Orbiting Spark Visual Identity

**Status:** DONE

### Objective

Make orbiting sparks visually distinct and readable.

### Requirements

* Add:

  * glowing spark particles
  * subtle motion trails
  * rotation clarity

* Avoid visual clutter in dense combat

### Acceptance Criteria

* Orbiting sparks are easy to track
* Visuals match the sparkler theme
* Effects remain performant

---

## Task 320 – Sparkler Evolution: Spark Aura Refinement

**Status:** DONE

### Objective

Enhance the existing spark aura evolution to be more distinct and polished.

### Requirements

* Ensure aura:

  * has clear radius
  * applies periodic damage ticks
  * scales visually with upgrades

* Improve:

  * visual feedback
  * tick timing consistency

### Acceptance Criteria

* Aura is visually clear and satisfying
* Damage is applied consistently
* Evolution feels like a major upgrade

---

## Task 321 – Evolution Conflict Handling

**Status:** DONE

### Objective

Prevent conflicting evolutions from triggering simultaneously.

### Requirements

* Define rules:

  * one evolution per weapon at a time
  * prioritize based on condition or order

* Prevent:

  * multiple evolution states active simultaneously
  * unintended stacking behaviors

### Acceptance Criteria

* Only one evolution applies per weapon
* Conflicts are resolved predictably
* System remains stable

---

## Task 322 – Evolution Balance Pass for New Variants

**Status:** DONE

### Objective

Tune the new evolutions for gameplay balance and feel.

### Requirements

* Validate:

  * damage output
  * usability
  * synergy with enemies and bosses
  * performance impact

* Adjust:

  * bounce counts
  * delay timing
  * orbit radius
  * aura strength

### Acceptance Criteria

* Each evolution feels distinct and viable
* No evolution dominates all others
* Gameplay remains readable and fun

---

## Task 323 – Playtest: Build Diversity Validation

**Status:** DONE

### Objective

Ensure new evolutions create meaningful run-to-run variety.

### Requirements

* Playtest multiple builds:

  * rocket-focused
  * sparkler-focused
  * mixed upgrades

* Validate:

  * different strategies emerge
  * evolutions feel discoverable
  * player choices matter

### Acceptance Criteria

* Builds feel different across runs
* Evolutions encourage experimentation
* System increases replayability

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

---

# Appended From TASKS.md

# TASKS.md

## Project Phase: Weapon Evolutions V2

Goal: Rebalance the weapon evolution system so evolutions require more intentional upgrade investment, increase build diversity, and preserve distinct identities for Bottle Rocket and Sparkler.

---

## 1. Split overloaded evolution tags into separate upgrades

### Objective
Remove cases where one upgrade contributes too much evolution progress by granting multiple key tags.

### Tasks
- [ ] Update `projectile_speed_up` so it no longer grants `rocket_bounce`
- [ ] Keep `projectile_speed_up` focused on `rocket_speed`
- [ ] Update `sparkler_arc_up` so it no longer grants `sparkler_persistence`
- [ ] Keep `sparkler_arc_up` focused on `sparkler_orbit`
- [ ] Add a new upgrade definition: `ricochet_rounds`
- [ ] Set `ricochet_rounds` tags to `("rocket_bounce",)`
- [ ] Add a new upgrade definition: `sparkler_duration_up`
- [ ] Set `sparkler_duration_up` tags to `("sparkler_persistence",)`
- [ ] Give both new upgrades names, descriptions, weights, categories, and stack rules that match the current upgrade style
- [ ] Ensure both new upgrades are included in `UPGRADE_DEFINITIONS`

### Acceptance Criteria
- `projectile_speed_up` only contributes `rocket_speed`
- `sparkler_arc_up` only contributes `sparkler_orbit`
- `ricochet_rounds` exists and contributes `rocket_bounce`
- `sparkler_duration_up` exists and contributes `sparkler_persistence`

---

## 2. Rebalance existing evolution requirements

### Objective
Ensure core evolutions require two distinct upgrade investments and remove accidental one-upgrade unlocks.

### Tasks
- [ ] Keep `burst_rocket` as `rocket_explosion + rocket_split`
- [ ] Keep `big_pop_rocket` as `rocket_explosion + rocket_power`
- [ ] Keep `delayed_blast_rocket` as `rocket_explosion + rocket_sticky`
- [ ] Keep `pinball_rocket` as `rocket_bounce + rocket_speed`
- [ ] Verify `pinball_rocket` can no longer be unlocked by `projectile_speed_up` alone
- [ ] Keep `wide_arc_sparkler` as `sparkler_range + sparkler_speed`
- [ ] Keep `orbiting_sparklers` as `sparkler_orbit + sparkler_speed`
- [ ] Keep `spark_aura` as `sparkler_range + sparkler_persistence`
- [ ] Review evolution descriptions so they still match the updated requirements

### Acceptance Criteria
- No current evolution is unlocked by a single upgrade alone
- Evolution descriptions accurately match the new requirements

---

## 3. Add new Bottle Rocket evolution paths

### Objective
Reduce dependence on `rocket_explosion` and create more varied Bottle Rocket builds.

### Tasks
- [ ] Add a new evolution definition: `chain_rocket`
- [ ] Set `chain_rocket` required tags to `("rocket_speed", "rocket_power")`
- [ ] Set `chain_rocket` result form id to `chain_rocket`
- [ ] Write description for retargeting / chaining behavior
- [ ] Add a new evolution definition: `piercing_rocket`
- [ ] Set `piercing_rocket` required tags to `("rocket_speed", "rocket_split")`
- [ ] Set `piercing_rocket` result form id to `piercing_rocket`
- [ ] Write description for piercing / line-clear behavior
- [ ] Ensure both appear in `list_weapon_evolutions()`
- [ ] Confirm both participate in eligibility checks

### Acceptance Criteria
- Bottle Rocket has at least 6 total evolution definitions
- At least 2 Bottle Rocket evolutions do not require `rocket_explosion`

---

## 4. Add new Sparkler evolution paths

### Objective
Create clearer stance-style Sparkler build options with more intentional specialization.

### Tasks
- [ ] Add a new evolution definition: `flare_whip`
- [ ] Set `flare_whip` required tags to `("sparkler_orbit", "sparkler_range")`
- [ ] Set `flare_whip` result form id to `flare_whip`
- [ ] Write description for sweeping control behavior
- [ ] Add a new evolution definition: `ember_ring`
- [ ] Set `ember_ring` required tags to `("sparkler_persistence", "sparkler_speed")`
- [ ] Set `ember_ring` result form id to `ember_ring`
- [ ] Write description for pulsing ring behavior
- [ ] Ensure both appear in `list_weapon_evolutions()`
- [ ] Confirm both participate in eligibility checks

### Acceptance Criteria
- Sparkler has at least 5 total evolution definitions
- Sparkler evolutions each represent a distinct stance / role

---

## 5. Add evolution tier metadata for future gating

### Objective
Prepare the system for later weapon-level gating without forcing a full implementation rewrite now.

### Tasks
- [ ] Extend `WeaponEvolutionDefinition` with optional tier metadata
- [ ] Add optional `required_weapon_level` field to `WeaponEvolutionDefinition`
- [ ] Set current standard evolutions to recommended minimum weapon level `3`
- [ ] Leave tracker behavior unchanged if weapon level is not yet wired in
- [ ] Add TODO comments where runtime weapon level checks will be integrated later
- [ ] Keep backward compatibility where possible

### Acceptance Criteria
- Evolution definitions can express weapon-level requirements
- Existing code still runs even if weapon level is not yet enforced

---

## 6. Improve evolution weighting so completions are favored more strongly

### Objective
Make upgrade offerings feel smarter by more strongly favoring upgrades that complete evolutions.

### Tasks
- [ ] Review current `EVOLUTION_TAG_WEIGHT_MULTIPLIER`
- [ ] Replace single multiplier logic with separate handling for:
  - [ ] upgrades that complete an evolution
  - [ ] upgrades that partially progress an evolution
- [ ] Add helper logic to distinguish:
  - [ ] no contribution
  - [ ] contributes one missing tag
  - [ ] fully completes one or more eligible evolutions
- [ ] Target approximate weighting:
  - [ ] completion â‰ˆ `2.5x`
  - [ ] progress â‰ˆ `1.5x`
  - [ ] neutral = `1.0x`
- [ ] Keep logic generic so new evolutions automatically benefit
- [ ] Add unit-testable helper methods if needed

### Acceptance Criteria
- Upgrades that complete an evolution are offered more often than neutral choices
- Partial-progress upgrades are still favored, but less than completion upgrades

---

## 7. Formalize Bottle Rocket merge compatibility rules

### Objective
Prevent incompatible merged behaviors and make future evolution stacking predictable.

### Tasks
- [ ] Decide where merge compatibility data should live:
  - [ ] in `weapon_evolutions.py`
  - [ ] or in a dedicated config/helper
- [ ] Add compatibility rules for Bottle Rocket evolutions
- [ ] Allow merges for:
  - [ ] `burst_rocket` + `big_pop_rocket`
  - [ ] `burst_rocket` + `delayed_blast_rocket`
  - [ ] `big_pop_rocket` + `chain_rocket`
  - [ ] `pinball_rocket` + `chain_rocket`
  - [ ] `piercing_rocket` + `big_pop_rocket`
- [ ] Block merges for:
  - [ ] `pinball_rocket` + `delayed_blast_rocket`
  - [ ] `burst_rocket` + `piercing_rocket`
- [ ] Expose helper(s) for checking whether a newly eligible Bottle Rocket evolution can merge into the current form
- [ ] Keep Sparkler excluded from merge behavior

### Acceptance Criteria
- Bottle Rocket merge behavior is data-driven
- Incompatible combinations are blocked consistently

---

## 8. Preserve Sparkler single-form behavior explicitly

### Objective
Keep Sparklerâ€™s identity clear and avoid accidental multi-form merging later.

### Tasks
- [ ] Review current runtime handling for Sparkler evolution activation
- [ ] Add explicit comments or guard logic that Sparkler supports one active form only
- [ ] Ensure new Sparkler evolutions replace or become the active form according to current design
- [ ] Prevent Bottle Rocket merge logic from being applied to Sparkler
- [ ] Document this in code and in the markdown reference

### Acceptance Criteria
- Sparkler still uses one active evolution form at a time
- Behavior is enforced explicitly, not just by convention

---

## 9. Add evolution progress helpers for future UI work

### Objective
Prepare the system for player-facing evolution hints and upgrade previews.

### Tasks
- [ ] Add helper to report missing tags for each evolution per weapon
- [ ] Add helper to report which evolutions are 1 tag away
- [ ] Add helper to report whether a candidate upgrade:
  - [ ] progresses an evolution
  - [ ] completes an evolution
- [ ] Reuse existing preview-style functionality where possible
- [ ] Keep output simple and UI-friendly

### Acceptance Criteria
- Code can answer â€œwhat am I close to unlocking?â€
- Code can answer â€œdoes this upgrade progress or complete an evolution?â€

---

## 10. Update documentation to match V2 behavior

### Objective
Make the markdown docs the clear source of truth for design and implementation.

### Tasks
- [ ] Update `WEAPON_EVOLUTION.md` or replace it with `WEAPON_EVOLUTION_V2.md`
- [ ] Reflect the new tag map
- [ ] Reflect the new evolution definitions
- [ ] Document that `pinball_rocket` now requires `ricochet_rounds`
- [ ] Document that `spark_aura` now requires `sparkler_duration_up`
- [ ] Document Bottle Rocket merge compatibility
- [ ] Document Sparkler single-form behavior
- [ ] Document optional weapon-level gating metadata
- [ ] Add a short â€œdesign goalsâ€ section explaining why the rebalance exists

### Acceptance Criteria
- Documentation matches the implemented code
- A developer can understand the full evolution system from the markdown file

---

## 11. Add test coverage for evolution eligibility and upgrade progression

### Objective
Prevent regressions as more evolutions and upgrades are added.

### Tasks
- [ ] Add tests for `eligible_weapon_evolutions()`
- [ ] Add tests for `preview_weapon_evolutions_with_added_tags()`
- [ ] Add tests that `pinball_rocket` is not unlocked by `projectile_speed_up` alone
- [ ] Add tests that `pinball_rocket` is unlocked by `ricochet_rounds + fire_rate_up`
- [ ] Add tests that `spark_aura` is not unlocked by `sparkler_arc_up + sparkler_range_up`
- [ ] Add tests that `spark_aura` is unlocked by `sparkler_duration_up + sparkler_range_up`
- [ ] Add tests for new evolutions:
  - [ ] `chain_rocket`
  - [ ] `piercing_rocket`
  - [ ] `flare_whip`
  - [ ] `ember_ring`
- [ ] Add tests for weighting helper behavior if new logic is split into helper functions
- [ ] Add tests for Bottle Rocket merge compatibility helpers

### Acceptance Criteria
- Core evolution rules are covered by automated tests
- The main rebalance changes are protected from regression

---

## 12. Final gameplay validation pass

### Objective
Verify the new system feels better in actual runs, not just in code.

### Tasks
- [ ] Start runs using Bottle Rocket and confirm multiple distinct build paths appear
- [ ] Start runs using Sparkler and confirm builds feel more specialized
- [ ] Verify no evolution unlocks too early from a single overloaded upgrade
- [ ] Verify offered upgrades more often support current build direction
- [ ] Verify Bottle Rocket merge behavior feels readable and intentional
- [ ] Verify Sparkler remains simple and stance-like
- [ ] Capture notes on any evolution that still feels too easy or too weak
- [ ] Adjust weights and tag distribution based on playtest results

### Acceptance Criteria
- Evolutions feel intentional rather than accidental
- Both weapons support multiple viable build paths
- No single upgrade dominates progression too strongly

---

## Suggested Implementation Order

1. Split overloaded tags into separate upgrades
2. Rebalance existing evolution requirements
3. Add new Bottle Rocket evolutions
4. Add new Sparkler evolutions
5. Improve evolution weighting
6. Add merge compatibility rules
7. Preserve Sparkler single-form behavior explicitly
8. Add progress helpers
9. Update docs
10. Add tests
11. Playtest and tune

---

## Definition of Done

- [ ] All V2 upgrades and evolutions are implemented
- [ ] Overloaded tag sources are split
- [ ] `pinball_rocket` no longer unlocks accidentally
- [ ] New non-explosion Bottle Rocket paths are live
- [ ] New Sparkler stance paths are live
- [ ] Weighting better supports evolution completion
- [ ] Merge rules are explicit and data-driven
- [ ] Docs and tests are updated
- [ ] Playtest confirms improved build diversity and clarity
