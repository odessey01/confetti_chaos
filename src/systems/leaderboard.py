"""Leaderboard services with local fallback and optional Steam integration."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Protocol

from .paths import saves_dir


LEADERBOARD_FILE_NAME = "leaderboard.json"
DEFAULT_LEADERBOARD_ID = "global_high_score"
DEFAULT_LOCAL_PLAYER_ID = "local_player"


@dataclass(frozen=True, slots=True)
class LeaderboardEntry:
    player_name: str
    score: int


@dataclass(frozen=True, slots=True)
class LeaderboardSnapshot:
    source: str
    global_top: tuple[LeaderboardEntry, ...]
    friend_top: tuple[LeaderboardEntry, ...]
    steam_available: bool


class LeaderboardService(Protocol):
    def submit_score(self, score: int) -> bool:
        """Submit a score using KeepBest behavior."""

    def snapshot(self, *, limit: int = 10) -> LeaderboardSnapshot:
        """Return global and friend leaderboard rows."""


def _leaderboard_path(path: Path | None = None) -> Path:
    return path if path is not None else saves_dir() / LEADERBOARD_FILE_NAME


class LocalJsonLeaderboardService:
    """JSON leaderboard fallback used when Steam is unavailable."""

    def __init__(self, *, file_path: Path | None = None, player_id: str = DEFAULT_LOCAL_PLAYER_ID) -> None:
        self._file_path = _leaderboard_path(file_path)
        self._player_id = str(player_id).strip() or DEFAULT_LOCAL_PLAYER_ID

    def _load_payload(self) -> dict[str, Any]:
        if not self._file_path.exists():
            return {"entries": []}
        try:
            payload = json.loads(self._file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"entries": []}
        if not isinstance(payload, dict):
            return {"entries": []}
        entries = payload.get("entries", [])
        if not isinstance(entries, list):
            entries = []
        return {"entries": entries}

    def _save_payload(self, payload: dict[str, Any]) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def submit_score(self, score: int) -> bool:
        resolved_score = max(0, int(score))
        payload = self._load_payload()
        entries: list[dict[str, Any]] = []
        best_by_player: dict[str, int] = {}
        for item in payload.get("entries", []):
            if not isinstance(item, dict):
                continue
            player_name = str(item.get("player_name", "")).strip()
            value = item.get("score", 0)
            if not player_name or not isinstance(value, int):
                continue
            best_by_player[player_name] = max(best_by_player.get(player_name, 0), max(0, int(value)))
        best_by_player[self._player_id] = max(best_by_player.get(self._player_id, 0), resolved_score)
        for player_name, best_score in best_by_player.items():
            entries.append({"player_name": player_name, "score": int(best_score)})
        entries.sort(key=lambda row: int(row["score"]), reverse=True)
        self._save_payload({"entries": entries})
        return True

    def snapshot(self, *, limit: int = 10) -> LeaderboardSnapshot:
        payload = self._load_payload()
        rows: list[LeaderboardEntry] = []
        for item in payload.get("entries", []):
            if not isinstance(item, dict):
                continue
            player_name = str(item.get("player_name", "")).strip()
            score = item.get("score", 0)
            if not player_name or not isinstance(score, int):
                continue
            rows.append(LeaderboardEntry(player_name=player_name, score=max(0, int(score))))
        rows.sort(key=lambda row: row.score, reverse=True)
        top = tuple(rows[: max(1, int(limit))])
        return LeaderboardSnapshot(
            source="local",
            global_top=top,
            friend_top=(),
            steam_available=False,
        )


class SteamLeaderboardService:
    """Steam-backed leaderboard service with graceful local fallback."""

    def __init__(
        self,
        *,
        leaderboard_id: str = DEFAULT_LEADERBOARD_ID,
        steam_client: Any | None = None,
        fallback: LeaderboardService | None = None,
    ) -> None:
        self._leaderboard_id = str(leaderboard_id).strip() or DEFAULT_LEADERBOARD_ID
        self._fallback = fallback or LocalJsonLeaderboardService()
        self._steam_client = steam_client if steam_client is not None else self._create_default_steam_client()

    @staticmethod
    def _create_default_steam_client() -> Any | None:
        try:
            import steamworks  # type: ignore
        except Exception:
            return None
        try:
            if hasattr(steamworks, "STEAMWORKS"):
                client = steamworks.STEAMWORKS()
                if hasattr(client, "initialize"):
                    client.initialize()
                return client
        except Exception:
            return None
        return None

    def _steam_available(self) -> bool:
        client = self._steam_client
        if client is None:
            return False
        checker = getattr(client, "is_available", None)
        if callable(checker):
            try:
                return bool(checker())
            except Exception:
                return False
        return True

    def _submit_steam_keep_best(self, score: int) -> bool:
        client = self._steam_client
        if client is None:
            return False
        resolved_score = max(0, int(score))
        submit = getattr(client, "submit_score", None)
        if callable(submit):
            try:
                return bool(submit(self._leaderboard_id, resolved_score, keep_best=True))
            except Exception:
                return False
        submit_keep_best = getattr(client, "submit_score_keep_best", None)
        if callable(submit_keep_best):
            try:
                return bool(submit_keep_best(self._leaderboard_id, resolved_score))
            except Exception:
                return False
        return False

    def _steam_rows(self, *, limit: int, friends_only: bool) -> tuple[LeaderboardEntry, ...]:
        client = self._steam_client
        if client is None:
            return ()
        getter = getattr(client, "get_top_scores", None)
        if not callable(getter):
            return ()
        try:
            rows = getter(self._leaderboard_id, max(1, int(limit)), friends_only=friends_only)
        except Exception:
            return ()
        output: list[LeaderboardEntry] = []
        if not isinstance(rows, list):
            return ()
        for row in rows:
            if isinstance(row, dict):
                name = str(row.get("player_name", "")).strip()
                score = row.get("score", 0)
            elif isinstance(row, (tuple, list)) and len(row) >= 2:
                name = str(row[0]).strip()
                score = row[1]
            else:
                continue
            if not name or not isinstance(score, int):
                continue
            output.append(LeaderboardEntry(player_name=name, score=max(0, int(score))))
        output.sort(key=lambda entry: entry.score, reverse=True)
        return tuple(output[: max(1, int(limit))])

    def submit_score(self, score: int) -> bool:
        if self._steam_available() and self._submit_steam_keep_best(score):
            return True
        return self._fallback.submit_score(score)

    def snapshot(self, *, limit: int = 10) -> LeaderboardSnapshot:
        if self._steam_available():
            global_rows = self._steam_rows(limit=limit, friends_only=False)
            friend_rows = self._steam_rows(limit=limit, friends_only=True)
            if global_rows or friend_rows:
                return LeaderboardSnapshot(
                    source="steam",
                    global_top=global_rows,
                    friend_top=friend_rows,
                    steam_available=True,
                )
        fallback_snapshot = self._fallback.snapshot(limit=limit)
        return LeaderboardSnapshot(
            source=fallback_snapshot.source,
            global_top=fallback_snapshot.global_top,
            friend_top=fallback_snapshot.friend_top,
            steam_available=False,
        )


def create_leaderboard_service() -> LeaderboardService:
    """Create a Steam-first service that always has local fallback behavior."""

    return SteamLeaderboardService()
