"""Weapon evolution definition and condition-check helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeaponEvolutionDefinition:
    evolution_id: str
    weapon_id: str
    required_tags: tuple[str, ...]
    result_form_id: str
    description: str
    # TODO: Wire runtime weapon-level checks into evolution eligibility when weapon levels exist.
    required_weapon_level: int | None = None


WEAPON_EVOLUTION_DEFINITIONS: tuple[WeaponEvolutionDefinition, ...] = (
    WeaponEvolutionDefinition(
        evolution_id="burst_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_explosion", "rocket_split"),
        result_form_id="burst_rocket",
        description="Bottle Rocket splits into burst fragments.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="big_pop_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_explosion", "rocket_power"),
        result_form_id="big_pop_rocket",
        description="Bottle Rocket gains larger explosion impact.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="delayed_blast_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_explosion", "rocket_sticky"),
        result_form_id="delayed_blast_rocket",
        description="Bottle Rocket sticks and detonates after a short delay.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="pinball_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_bounce", "rocket_speed"),
        result_form_id="pinball_rocket",
        description="Bottle Rocket ricochets toward another target on impact.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="chain_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_speed", "rocket_power"),
        result_form_id="chain_rocket",
        description="Bottle Rocket retargets forward through nearby enemies in a chain.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="piercing_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_speed", "rocket_split"),
        result_form_id="piercing_rocket",
        description="Bottle Rocket pierces through targets for line-clear pressure.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="wide_arc_sparkler",
        weapon_id="sparkler",
        required_tags=("sparkler_range", "sparkler_speed"),
        result_form_id="wide_arc_sparkler",
        description="Sparkler swings in a wider arc.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="orbiting_sparklers",
        weapon_id="sparkler",
        required_tags=("sparkler_orbit", "sparkler_speed"),
        result_form_id="orbiting_sparklers",
        description="Sparkler spawns orbiting sparks around the player.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="spark_aura",
        weapon_id="sparkler",
        required_tags=("sparkler_range", "sparkler_persistence"),
        result_form_id="spark_aura",
        description="Sparkler transforms into a periodic spark aura.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="flare_whip",
        weapon_id="sparkler",
        required_tags=("sparkler_orbit", "sparkler_range"),
        result_form_id="flare_whip",
        description="Sparkler lashes in wide sweeping control arcs.",
        required_weapon_level=3,
    ),
    WeaponEvolutionDefinition(
        evolution_id="ember_ring",
        weapon_id="sparkler",
        required_tags=("sparkler_persistence", "sparkler_speed"),
        result_form_id="ember_ring",
        description="Sparkler emits a pulsing ember ring around the player.",
        required_weapon_level=3,
    ),
)

_EVOLUTION_BY_ID = {definition.evolution_id: definition for definition in WEAPON_EVOLUTION_DEFINITIONS}
COMPATIBLE_MULTI_EVOLUTION_WEAPONS: frozenset[str] = frozenset({"bottle_rocket"})


def list_weapon_evolutions() -> tuple[WeaponEvolutionDefinition, ...]:
    return WEAPON_EVOLUTION_DEFINITIONS


def get_weapon_evolution(evolution_id: str) -> WeaponEvolutionDefinition | None:
    return _EVOLUTION_BY_ID.get(str(evolution_id))


def eligible_weapon_evolutions(
    *,
    weapon_id: str,
    acquired_tags: tuple[str, ...] | list[str] | set[str],
    exclude_evolution_ids: tuple[str, ...] | list[str] | set[str] = (),
) -> list[WeaponEvolutionDefinition]:
    tags = {str(tag) for tag in acquired_tags}
    excluded = {str(item) for item in exclude_evolution_ids}
    eligible: list[WeaponEvolutionDefinition] = []
    for definition in WEAPON_EVOLUTION_DEFINITIONS:
        if definition.weapon_id != str(weapon_id):
            continue
        if definition.evolution_id in excluded:
            continue
        if set(definition.required_tags).issubset(tags):
            eligible.append(definition)
    return eligible


def preview_weapon_evolutions_with_added_tags(
    *,
    weapon_id: str,
    acquired_tags: tuple[str, ...] | list[str] | set[str],
    added_tags: tuple[str, ...] | list[str] | set[str],
    exclude_evolution_ids: tuple[str, ...] | list[str] | set[str] = (),
) -> list[WeaponEvolutionDefinition]:
    preview_tags = {str(tag) for tag in acquired_tags}
    preview_tags.update(str(tag) for tag in added_tags)
    return eligible_weapon_evolutions(
        weapon_id=weapon_id,
        acquired_tags=tuple(sorted(preview_tags)),
        exclude_evolution_ids=exclude_evolution_ids,
    )


class WeaponEvolutionTracker:
    """Tracks which evolutions have already triggered this run."""

    def __init__(self) -> None:
        self._triggered: set[str] = set()
        self._triggered_weapons: set[str] = set()
        self._pending: list[WeaponEvolutionDefinition] = []

    def reset(self) -> None:
        self._triggered.clear()
        self._triggered_weapons.clear()
        self._pending.clear()

    def check_for_new(
        self,
        *,
        weapon_id: str,
        acquired_tags: tuple[str, ...] | list[str] | set[str],
    ) -> list[WeaponEvolutionDefinition]:
        resolved_weapon_id = str(weapon_id)
        if (
            resolved_weapon_id in self._triggered_weapons
            and resolved_weapon_id not in COMPATIBLE_MULTI_EVOLUTION_WEAPONS
        ):
            return []
        newly_eligible = eligible_weapon_evolutions(
            weapon_id=resolved_weapon_id,
            acquired_tags=acquired_tags,
            exclude_evolution_ids=tuple(self._triggered),
        )
        if newly_eligible:
            newly_eligible = [newly_eligible[0]]
        for definition in newly_eligible:
            self._triggered.add(definition.evolution_id)
            self._triggered_weapons.add(definition.weapon_id)
            self._pending.append(definition)
        return list(newly_eligible)

    def consume_pending(self) -> list[WeaponEvolutionDefinition]:
        pending = list(self._pending)
        self._pending.clear()
        return pending

    def has_triggered(self, evolution_id: str) -> bool:
        return str(evolution_id) in self._triggered

    def has_triggered_weapon(self, weapon_id: str) -> bool:
        return str(weapon_id) in self._triggered_weapons

    def triggered_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._triggered))
