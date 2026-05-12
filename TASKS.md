## Steam Leaderboard Integration

Status: DONE (2026-05-12)

### Objective
Add Steam leaderboard support for run scores while preserving offline/local fallback behavior.

### Requirements
- Create a `LeaderboardService` abstraction.
- Add a local JSON-backed leaderboard fallback.
- Add a Steam-backed leaderboard implementation.
- Submit scores only after game-over.
- Use Steam `KeepBest` behavior so lower repeat scores do not overwrite the player's best score.
- Display top global scores and friend scores if available.
- Fail gracefully if Steam is unavailable.

### Acceptance Criteria
- Game runs normally without Steam.
- Game submits score to Steam when launched through Steam.
- Game shows local scores when Steam is unavailable.
- Steam leaderboard uses `global_high_score`.
- Score is submitted once per completed run.
