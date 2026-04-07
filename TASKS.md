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
