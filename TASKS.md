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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

**Status:** TODO

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

