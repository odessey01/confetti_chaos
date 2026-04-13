# AGENTS.md

## Project Context
This is a Python-based 2D game intended for Steam release.

Agents MUST read:
- GAME_VISION.md
- TECH_SPEC.md
- TASKS.md

before making any changes in a new session.
During the same session, do not fully reread these docs every task unless:
- the user asks for a full reread
- those files changed
- scope changed enough that a refresh is needed

---

## Operating Rules

1. Always propose a plan before coding
2. Limit changes to the smallest possible scope
3. Do not introduce new libraries without approval
4. Keep code modular and organized under /src
5. Do not break existing functionality

---

## Execution Workflow

For every task:
1. Read relevant files
2. Output plan:
   - files to change
   - approach
3. Wait for approval (unless explicitly told to proceed)
4. Implement
5. Run lightweight, task-appropriate verification
6. Summarize changes

Throughput defaults:
- Prefer batching related TODOs (for example 2-3 at a time) when risk is low, instead of one TODO per turn
- Keep progress updates concise; avoid repetitive narration when no decision changed
- Prefer focused file reads/snippets over full file dumps when only a small section is needed

Verification defaults:
- Prefer targeted tests for the files or systems touched by the task
- Use lightweight checks such as `pytest` on a specific test file, small focused test selections, or `python -m compileall` when appropriate
- Run the full test suite only for broad changes, refactors, cross-cutting risk, or before major checkpoints
- If no automated test exists for the task, do the smallest reasonable verification step and state what was or was not verified

Rate/Cost guardrails:
- Do not repeat large context summaries unless the user asks
- Reuse known project context from earlier in the session
- Keep final summaries high-signal and short by default
- If multiple valid approaches exist, choose the one with fewer turns/tool calls unless quality would clearly suffer
- If model routing is available, prefer a smaller/faster model for routine edits and targeted test loops; reserve larger models for architecture-heavy changes

---

## Game-Specific Constraints

- Maintain 60 FPS target
- Keep gameplay loop simple and fast
- Avoid overengineering
- Prefer clarity over abstraction

---

## Commands

Common commands:
- Run game: `python src/main.py`
- Run tests: `pytest`
- Run focused tests: `pytest tests/test_some_area.py` or `pytest -q tests/test_some_area.py`
- Build (future): `pyinstaller ...`

---

## Definition of Done

- Feature works in-game
- No errors in console
- Does not degrade performance
- Includes lightweight verification steps appropriate to the scope of the task
