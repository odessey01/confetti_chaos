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


WEAPON_EVOLUTION_DEFINITIONS: tuple[WeaponEvolutionDefinition, ...] = (
    WeaponEvolutionDefinition(
        evolution_id="burst_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_explosion", "rocket_split"),
        result_form_id="burst_rocket",
        description="Bottle Rocket splits into burst fragments.",
    ),
    WeaponEvolutionDefinition(
        evolution_id="big_pop_rocket",
        weapon_id="bottle_rocket",
        required_tags=("rocket_explosion", "rocket_power"),
        result_form_id="big_pop_rocket",
        description="Bottle Rocket gains larger explosion impact.",
    ),
    WeaponEvolutionDefinition(
        evolution_id="wide_arc_sparkler",
        weapon_id="sparkler",
        required_tags=("sparkler_range", "sparkler_speed"),
        result_form_id="wide_arc_sparkler",
        description="Sparkler swings in a wider arc.",
    ),
    WeaponEvolutionDefinition(
        evolution_id="spark_aura",
        weapon_id="sparkler",
        required_tags=("sparkler_range", "sparkler_persistence"),
        result_form_id="spark_aura",
        description="Sparkler transforms into a periodic spark aura.",
    ),
)

_EVOLUTION_BY_ID = {definition.evolution_id: definition for definition in WEAPON_EVOLUTION_DEFINITIONS}


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
        self._pending: list[WeaponEvolutionDefinition] = []

    def reset(self) -> None:
        self._triggered.clear()
        self._pending.clear()

    def check_for_new(
        self,
        *,
        weapon_id: str,
        acquired_tags: tuple[str, ...] | list[str] | set[str],
    ) -> list[WeaponEvolutionDefinition]:
        newly_eligible = eligible_weapon_evolutions(
            weapon_id=weapon_id,
            acquired_tags=acquired_tags,
            exclude_evolution_ids=tuple(self._triggered),
        )
        if newly_eligible:
            newly_eligible = [newly_eligible[0]]
        for definition in newly_eligible:
            self._triggered.add(definition.evolution_id)
            self._pending.append(definition)
        return list(newly_eligible)

    def consume_pending(self) -> list[WeaponEvolutionDefinition]:
        pending = list(self._pending)
        self._pending.clear()
        return pending

    def has_triggered(self, evolution_id: str) -> bool:
        return str(evolution_id) in self._triggered

    def triggered_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._triggered))
