"""Data-driven character unlock condition definitions and evaluators."""

from __future__ import annotations

from dataclasses import dataclass

from .meta_progression import MetaProgression

BUNNY_UNLOCK_REQUIRED_RUNS = 5
CAT_UNLOCK_REQUIRED_HIGH_SCORE = 10_000
RACCOON_UNLOCK_REQUIRED_BOSSES = 10


@dataclass(frozen=True)
class UnlockProgressSnapshot:
    total_runs_completed: int = 0
    high_score: int = 0
    bosses_defeated: int = 0


@dataclass(frozen=True)
class CharacterUnlockCondition:
    condition_id: str
    character_id: str
    description: str
    required_runs_completed: int = 0
    required_high_score: int = 0
    required_bosses_defeated: int = 0
    unlocked_by_default: bool = False


CHARACTER_UNLOCK_CONDITIONS: tuple[CharacterUnlockCondition, ...] = (
    CharacterUnlockCondition(
        condition_id="unlock_teddy_default",
        character_id="teddy_f",
        description="Unlocked by default.",
        unlocked_by_default=True,
    ),
    CharacterUnlockCondition(
        condition_id="unlock_bunny_runs",
        character_id="bunny_f",
        description="Complete 5 runs.",
        required_runs_completed=BUNNY_UNLOCK_REQUIRED_RUNS,
    ),
    CharacterUnlockCondition(
        condition_id="unlock_cat_score",
        character_id="cat_f",
        description="Reach a high score of 10,000.",
        required_high_score=CAT_UNLOCK_REQUIRED_HIGH_SCORE,
    ),
    CharacterUnlockCondition(
        condition_id="unlock_raccoon_bosses",
        character_id="fox_f",
        description="Defeat 10 bosses.",
        required_bosses_defeated=RACCOON_UNLOCK_REQUIRED_BOSSES,
    ),
)

_UNLOCK_BY_CHARACTER_ID = {
    definition.character_id: definition for definition in CHARACTER_UNLOCK_CONDITIONS
}
_UNLOCK_BY_CONDITION_ID = {
    definition.condition_id: definition for definition in CHARACTER_UNLOCK_CONDITIONS
}


def list_character_unlock_conditions() -> tuple[CharacterUnlockCondition, ...]:
    return CHARACTER_UNLOCK_CONDITIONS


def get_character_unlock_condition(character_id: str) -> CharacterUnlockCondition | None:
    return _UNLOCK_BY_CHARACTER_ID.get(str(character_id))


def get_unlock_condition_by_id(condition_id: str) -> CharacterUnlockCondition | None:
    return _UNLOCK_BY_CONDITION_ID.get(str(condition_id))


def is_unlock_condition_met(
    definition: CharacterUnlockCondition,
    progress: UnlockProgressSnapshot,
) -> bool:
    if definition.unlocked_by_default:
        return True
    if int(progress.total_runs_completed) < int(definition.required_runs_completed):
        return False
    if int(progress.high_score) < int(definition.required_high_score):
        return False
    if int(progress.bosses_defeated) < int(definition.required_bosses_defeated):
        return False
    return True


def evaluate_unlock_progress(progress: UnlockProgressSnapshot) -> tuple[tuple[str, ...], tuple[str, ...]]:
    unlocked_characters: list[str] = []
    met_condition_ids: list[str] = []
    for definition in CHARACTER_UNLOCK_CONDITIONS:
        if is_unlock_condition_met(definition, progress):
            unlocked_characters.append(definition.character_id)
            met_condition_ids.append(definition.condition_id)
    return tuple(sorted(set(unlocked_characters))), tuple(sorted(set(met_condition_ids)))


def unlock_thresholds_snapshot() -> dict[str, int]:
    return {
        "bunny_required_runs_completed": int(BUNNY_UNLOCK_REQUIRED_RUNS),
        "cat_required_high_score": int(CAT_UNLOCK_REQUIRED_HIGH_SCORE),
        "raccoon_required_bosses_defeated": int(RACCOON_UNLOCK_REQUIRED_BOSSES),
    }


def is_character_unlocked(meta_progression: MetaProgression, character_id: str) -> bool:
    return str(character_id) in {str(item) for item in meta_progression.unlocked_characters}


def refresh_meta_unlock_state(meta_progression: MetaProgression) -> bool:
    progress = UnlockProgressSnapshot(
        total_runs_completed=max(0, int(meta_progression.total_runs_completed)),
        high_score=max(0, int(meta_progression.best_score)),
        bosses_defeated=max(0, int(meta_progression.bosses_defeated)),
    )
    unlocked, met_conditions = evaluate_unlock_progress(progress)
    unlocked_set = {str(item) for item in meta_progression.unlocked_characters}
    condition_set = {str(item) for item in meta_progression.unlock_conditions_met}
    desired_unlocked_set = set(unlocked)
    desired_condition_set = set(met_conditions)
    changed = False
    if desired_unlocked_set != unlocked_set:
        meta_progression.unlocked_characters = sorted(desired_unlocked_set)
        changed = True
    if desired_condition_set != condition_set:
        meta_progression.unlock_conditions_met = sorted(desired_condition_set)
        changed = True
    return changed
