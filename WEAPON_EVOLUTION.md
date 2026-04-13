# Weapon Evolution V2

This document defines the rebalanced weapon evolution system for Confetti Chaos.

It introduces:
- Improved tag distribution
- More intentional build paths
- Reduced accidental evolutions
- Expanded evolution diversity
- Clearer weapon identities

---

# Core Design Principles

## Tag-Driven System
- Evolutions are triggered by **tags**, not upgrade IDs.
- Upgrades grant **1 primary evolution tag** (with rare exceptions).

## Build Intent > Accidental Unlocks
- Most evolutions require **2 distinct upgrade investments**.
- No single upgrade should satisfy an evolution alone.

## Weapon Identity

### Bottle Rocket
- **Modular / combinatorial**
- Can **merge compatible evolution behaviors**
- Supports branching and stacking builds

### Sparkler
- **Stance-based / specialized**
- Only **one active evolution at a time**
- Evolutions are more transformative

---

# Runtime Rules

- Evolutions trigger when required tags are met.
- Evolutions may optionally require minimum weapon level (recommended).
- Bottle Rocket:
  - First evolution becomes base form
  - Additional compatible evolutions may merge
- Sparkler:
  - Only one evolution active at a time (latest replaces previous)

---

# Upgrade Tag Map (V2)

## Bottle Rocket Tags

| Tag | Upgrade ID | Upgrade Name |
| --- | --- | --- |
| `rocket_explosion` | `confetti_burst_up` | Party Burst |
| `rocket_split` | `projectile_cap_up` | Extra Chamber |
| `rocket_power` | `projectile_damage_up` | Heavy Confetti |
| `rocket_sticky` | `enemy_slow` | Sticky Floor |
| `rocket_speed` | `fire_rate_up` | Rapid Pop |
| `rocket_speed` | `projectile_speed_up` | Crisp Shots |
| `rocket_bounce` | `ricochet_rounds` | Ricochet Rounds |

## Sparkler Tags

| Tag | Upgrade ID | Upgrade Name |
| --- | --- | --- |
| `sparkler_range` | `sparkler_range_up` | Long Spark |
| `sparkler_speed` | `fire_rate_up` | Rapid Pop |
| `sparkler_orbit` | `sparkler_arc_up` | Wide Swing |
| `sparkler_persistence` | `sparkler_duration_up` | Glowing Embers |

---

# Bottle Rocket Evolutions (V2)

## Core Evolutions

### burst_rocket
- Tags: `rocket_explosion` + `rocket_split`
- Effect: Splits into explosive fragments
- Role: AoE / crowd clear

---

### big_pop_rocket
- Tags: `rocket_explosion` + `rocket_power`
- Effect: Larger explosion impact
- Role: Burst damage / bossing

---

### delayed_blast_rocket
- Tags: `rocket_explosion` + `rocket_sticky`
- Effect: Sticks to enemies and detonates
- Role: Trap / control

---

### pinball_rocket
- Tags: `rocket_bounce` + `rocket_speed`
- Effect: Ricochets between targets
- Role: Multi-hit / mobility damage

NOTE:
- No longer unlocks from a single upgrade.
- Requires `ricochet_rounds`.

---

## New Non-Explosion Paths

### chain_rocket
- Tags: `rocket_speed` + `rocket_power`
- Effect: Retargets to nearby enemies after impact
- Role: Single-target pressure / chaining

---

### piercing_rocket
- Tags: `rocket_speed` + `rocket_split`
- Effect: Pierces through enemies in a line
- Role: Lane clear / positioning

---

# Bottle Rocket Merge Rules

## Compatible Merges

| Primary | Can Merge With |
|--------|---------------|
| burst_rocket | big_pop_rocket |
| burst_rocket | delayed_blast_rocket |
| big_pop_rocket | chain_rocket |
| pinball_rocket | chain_rocket |
| piercing_rocket | big_pop_rocket |

## Restricted Merges

| Blocked Combination | Reason |
|--------------------|--------|
| pinball + delayed_blast | Conflicting physics |
| burst + piercing | Competing projectile behaviors |

---

# Sparkler Evolutions (V2)

## Core Evolutions

### wide_arc_sparkler
- Tags: `sparkler_range` + `sparkler_speed`
- Effect: Wider melee arc
- Role: General-purpose coverage

---

### orbiting_sparklers
- Tags: `sparkler_orbit` + `sparkler_speed`
- Effect: Orbiting sparks around player
- Role: Defensive / passive damage

---

### spark_aura
- Tags: `sparkler_range` + `sparkler_persistence`
- Effect: Periodic AoE aura
- Role: Area denial / sustained damage

---

## New Evolutions

### flare_whip
- Tags: `sparkler_orbit` + `sparkler_range`
- Effect: Extended sweeping arcs
- Role: Spacing / crowd control

---

### ember_ring
- Tags: `sparkler_persistence` + `sparkler_speed`
- Effect: Pulsing ring of sparks
- Role: Aggressive AoE pressure

---

# Evolution Tiers (Optional)

## Tier 1 (Standard)
- Requirement:
  - 2 tags
  - Weapon level ≥ 3

## Tier 2 (Advanced)
- Requirement:
  - 3 tags
  - Weapon level ≥ 5

### Example Tier 2 Evolutions

#### super_burst_rocket
- Tags: `rocket_explosion` + `rocket_split` + `rocket_power`
- Effect: Enhanced fragmentation + damage

---

#### sticky_pinball_rocket
- Tags: `rocket_bounce` + `rocket_speed` + `rocket_sticky`
- Effect: Ricocheting delayed detonations

---

#### solar_sparkler
- Tags: `sparkler_range` + `sparkler_speed` + `sparkler_persistence`
- Effect: Expanding periodic burn pulses

---

# Evolution Weighting Guidance

Upgrade selection should prioritize:

- Completing an evolution: **high priority (≈2.5x weight)**
- Progressing toward evolution: **medium priority (≈1.5x weight)**
- Neutral upgrades: base weight

---

# Future Extensions

- Keystone evolutions (4+ tags)
- Opposing tag systems (e.g., precision vs chaos)
- Passive modifier evolutions (non-replacement effects)
- Player-visible evolution progress UI

---

# Summary

This V2 system improves:

- Build diversity
- Player agency
- Balance consistency
- Evolution clarity

While maintaining:

- Tag-driven flexibility
- Simple runtime checks
- Expandable design