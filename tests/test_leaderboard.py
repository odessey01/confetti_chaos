"""Focused tests for leaderboard service behavior."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.leaderboard import (  # noqa: E402
    LocalJsonLeaderboardService,
    SteamLeaderboardService,
)


class _FakeSteamClient:
    def __init__(self, *, available: bool = True, submit_ok: bool = True) -> None:
        self._available = bool(available)
        self._submit_ok = bool(submit_ok)
        self.submissions: list[tuple[str, int, bool]] = []
        self.global_rows: list[tuple[str, int]] = [("alice", 120), ("bob", 95)]
        self.friend_rows: list[tuple[str, int]] = [("friend_1", 88)]

    def is_available(self) -> bool:
        return self._available

    def submit_score(self, leaderboard_id: str, score: int, *, keep_best: bool = False) -> bool:
        self.submissions.append((str(leaderboard_id), int(score), bool(keep_best)))
        return self._submit_ok

    def get_top_scores(self, leaderboard_id: str, limit: int, *, friends_only: bool = False) -> list[tuple[str, int]]:
        _ = leaderboard_id
        rows = self.friend_rows if friends_only else self.global_rows
        return rows[: max(1, int(limit))]


class LeaderboardTests(unittest.TestCase):
    def test_local_service_uses_keep_best_for_same_player(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = pathlib.Path(tmp_dir) / "leaderboard.json"
            service = LocalJsonLeaderboardService(file_path=path, player_id="me")
            service.submit_score(40)
            service.submit_score(25)
            service.submit_score(51)
            snapshot = service.snapshot(limit=5)
            self.assertEqual(snapshot.source, "local")
            self.assertFalse(snapshot.steam_available)
            self.assertEqual(len(snapshot.global_top), 1)
            self.assertEqual(snapshot.global_top[0].player_name, "me")
            self.assertEqual(snapshot.global_top[0].score, 51)

    def test_steam_submit_uses_keep_best_flag(self) -> None:
        fake = _FakeSteamClient(available=True, submit_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            fallback = LocalJsonLeaderboardService(file_path=pathlib.Path(tmp_dir) / "leaderboard.json", player_id="local")
            service = SteamLeaderboardService(steam_client=fake, fallback=fallback)
            self.assertTrue(service.submit_score(77))
            self.assertEqual(fake.submissions, [("global_high_score", 77, True)])

    def test_steam_failure_falls_back_to_local(self) -> None:
        fake = _FakeSteamClient(available=True, submit_ok=False)
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = pathlib.Path(tmp_dir) / "leaderboard.json"
            fallback = LocalJsonLeaderboardService(file_path=path, player_id="local")
            service = SteamLeaderboardService(steam_client=fake, fallback=fallback)
            self.assertTrue(service.submit_score(64))
            local_snapshot = fallback.snapshot(limit=3)
            self.assertEqual(local_snapshot.source, "local")
            self.assertEqual(local_snapshot.global_top[0].score, 64)

    def test_steam_snapshot_includes_global_and_friend_rows(self) -> None:
        fake = _FakeSteamClient(available=True, submit_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            fallback = LocalJsonLeaderboardService(file_path=pathlib.Path(tmp_dir) / "leaderboard.json", player_id="local")
            service = SteamLeaderboardService(steam_client=fake, fallback=fallback)
            snapshot = service.snapshot(limit=2)
            self.assertTrue(snapshot.steam_available)
            self.assertEqual(snapshot.source, "steam")
            self.assertEqual([row.player_name for row in snapshot.global_top], ["alice", "bob"])
            self.assertEqual([row.player_name for row in snapshot.friend_top], ["friend_1"])


if __name__ == "__main__":
    unittest.main()
