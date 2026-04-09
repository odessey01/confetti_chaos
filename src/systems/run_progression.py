"""Run-level progression system (separate from stage/level progression)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunProgression:
    run_level: int = 1
    xp: int = 0
    xp_to_next_level: int = 10
    pending_level_ups: int = 0
    base_xp_to_next: int = 10
    growth_factor: float = 1.5

    def reset(self) -> None:
        self.run_level = 1
        self.xp = 0
        self.pending_level_ups = 0
        self.xp_to_next_level = self._xp_requirement_for_level(self.run_level)

    def gain_xp(self, amount: int) -> int:
        gained = max(0, int(amount))
        if gained <= 0:
            return 0
        self.xp += gained
        levels_gained = 0
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.run_level += 1
            levels_gained += 1
            self.pending_level_ups += 1
            self.xp_to_next_level = self._xp_requirement_for_level(self.run_level)
        return levels_gained

    def consume_pending_level_up(self) -> bool:
        if self.pending_level_ups <= 0:
            return False
        self.pending_level_ups -= 1
        return True

    def progress_fraction(self) -> float:
        if self.xp_to_next_level <= 0:
            return 0.0
        return max(0.0, min(self.xp / self.xp_to_next_level, 1.0))

    def snapshot(self) -> dict[str, int | float]:
        return {
            "run_level": self.run_level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level,
            "pending_level_ups": self.pending_level_ups,
            "progress_fraction": self.progress_fraction(),
        }

    def _xp_requirement_for_level(self, level: int) -> int:
        clamped = max(1, int(level))
        requirement = int(round(self.base_xp_to_next * (self.growth_factor ** (clamped - 1))))
        return max(self.base_xp_to_next, requirement)
