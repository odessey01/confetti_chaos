"""Run upgrade definitions and selection/application helpers."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class UpgradeDefinition:
    id: str
    name: str
    description: str
    category: str
    effect_values: dict[str, float]
    max_stacks: int | None = None
    repeatable: bool = True
    weight: float = 1.0
    allowed_weapon_ids: tuple[str, ...] | None = None


UPGRADE_DEFINITIONS: tuple[UpgradeDefinition, ...] = (
    UpgradeDefinition(
        id="move_speed_up",
        name="Quick Feet",
        description="+Move speed.",
        category="player",
        effect_values={"move_speed_mult": 0.09},
        max_stacks=5,
        weight=1.0,
    ),
    UpgradeDefinition(
        id="fire_rate_up",
        name="Rapid Pop",
        description="+Fire rate.",
        category="weapon",
        effect_values={"fire_rate_mult": 0.11},
        max_stacks=5,
        weight=1.0,
    ),
    UpgradeDefinition(
        id="projectile_speed_up",
        name="Crisp Shots",
        description="+Rocket speed.",
        category="weapon",
        effect_values={"projectile_speed_mult": 0.12},
        max_stacks=5,
        weight=0.9,
        allowed_weapon_ids=("bottle_rocket",),
    ),
    UpgradeDefinition(
        id="projectile_cap_up",
        name="Extra Chamber",
        description="+1 active rocket (max 5).",
        category="weapon",
        effect_values={"projectile_cap_bonus": 1.0},
        max_stacks=2,
        weight=0.65,
        allowed_weapon_ids=("bottle_rocket",),
    ),
    UpgradeDefinition(
        id="confetti_burst_up",
        name="Party Burst",
        description="+Confetti burst size.",
        category="effects",
        effect_values={"confetti_bonus": 2.0},
        max_stacks=4,
        weight=0.8,
    ),
    UpgradeDefinition(
        id="score_bonus",
        name="Spotlight Bonus",
        description="+Score from defeats.",
        category="economy",
        effect_values={"score_mult": 0.10},
        max_stacks=5,
        weight=0.9,
    ),
    UpgradeDefinition(
        id="enemy_slow",
        name="Sticky Floor",
        description="-Enemy move speed.",
        category="control",
        effect_values={"enemy_speed_reduction": 0.06},
        max_stacks=4,
        weight=0.7,
    ),
    UpgradeDefinition(
        id="projectile_damage_up",
        name="Heavy Confetti",
        description="+Rocket damage.",
        category="weapon",
        effect_values={"projectile_damage": 1.0},
        max_stacks=3,
        weight=0.75,
        allowed_weapon_ids=("bottle_rocket",),
    ),
    UpgradeDefinition(
        id="sparkler_range_up",
        name="Long Spark",
        description="+Sparkler range.",
        category="weapon",
        effect_values={"sparkler_range_bonus": 16.0},
        max_stacks=4,
        weight=0.8,
        allowed_weapon_ids=("sparkler",),
    ),
    UpgradeDefinition(
        id="sparkler_damage_up",
        name="Hotter Sparks",
        description="+Sparkler damage.",
        category="weapon",
        effect_values={"sparkler_damage_bonus": 1.0},
        max_stacks=3,
        weight=0.8,
        allowed_weapon_ids=("sparkler",),
    ),
    UpgradeDefinition(
        id="sparkler_arc_up",
        name="Wide Swing",
        description="+Sparkler swing arc.",
        category="weapon",
        effect_values={"sparkler_cone_bonus_degrees": 10.0},
        max_stacks=3,
        weight=0.75,
        allowed_weapon_ids=("sparkler",),
    ),
)


class RunUpgradeSystem:
    def __init__(self, *, rng: random.Random | None = None) -> None:
        self._rng = rng if rng is not None else random.Random()
        self._defs = {definition.id: definition for definition in UPGRADE_DEFINITIONS}
        self.stacks: dict[str, int] = {}
        self.current_choices: list[UpgradeDefinition] = []

    def reset(self) -> None:
        self.stacks.clear()
        self.current_choices = []

    def generate_choices(self, *, count: int = 3, active_weapon_id: str | None = None) -> list[UpgradeDefinition]:
        valid = [
            definition
            for definition in self._defs.values()
            if self.is_valid_choice(definition.id, active_weapon_id=active_weapon_id)
        ]
        if not valid:
            self.current_choices = []
            return []
        picked: list[UpgradeDefinition] = []
        pool = list(valid)
        target = max(1, count)
        while pool and len(picked) < target:
            picked_definition = self._weighted_pick(pool)
            picked.append(picked_definition)
            pool = [candidate for candidate in pool if candidate.id != picked_definition.id]
        self.current_choices = picked
        return list(self.current_choices)

    def apply_choice(self, upgrade_id: str, *, active_weapon_id: str | None = None) -> bool:
        definition = self._defs.get(upgrade_id)
        if definition is None or not self.is_valid_choice(upgrade_id, active_weapon_id=active_weapon_id):
            return False
        self.stacks[upgrade_id] = self.stacks.get(upgrade_id, 0) + 1
        self.current_choices = []
        return True

    def is_valid_choice(self, upgrade_id: str, *, active_weapon_id: str | None = None) -> bool:
        definition = self._defs.get(upgrade_id)
        if definition is None:
            return False
        if not self._is_weapon_allowed(definition, active_weapon_id):
            return False
        current = self.stacks.get(upgrade_id, 0)
        if definition.max_stacks is not None and current >= definition.max_stacks:
            return False
        if not definition.repeatable and current > 0:
            return False
        return True

    def stack_count(self, upgrade_id: str) -> int:
        return self.stacks.get(upgrade_id, 0)

    def effects_snapshot(self) -> dict[str, float]:
        effects: dict[str, float] = {}
        for upgrade_id, count in self.stacks.items():
            definition = self._defs.get(upgrade_id)
            if definition is None or count <= 0:
                continue
            for key, value in definition.effect_values.items():
                effects[key] = effects.get(key, 0.0) + (float(value) * count)
        return effects

    def _weighted_pick(self, pool: list[UpgradeDefinition]) -> UpgradeDefinition:
        total = sum(max(0.0, definition.weight) for definition in pool)
        if total <= 0.0:
            return pool[0]
        roll = self._rng.random() * total
        cumulative = 0.0
        for definition in pool:
            cumulative += max(0.0, definition.weight)
            if roll <= cumulative:
                return definition
        return pool[-1]

    def _is_weapon_allowed(self, definition: UpgradeDefinition, active_weapon_id: str | None) -> bool:
        if not definition.allowed_weapon_ids:
            return True
        if active_weapon_id is None:
            return True
        return str(active_weapon_id) in definition.allowed_weapon_ids
