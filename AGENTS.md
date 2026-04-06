# AGENTS.md

## Project Context
This is a Python-based 2D game intended for Steam release.

Agents MUST read:
- GAME_VISION.md
- TECH_SPEC.md
- TASKS.md

before making any changes.

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
5. Run tests or verify execution
6. Summarize changes

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
- Build (future): `pyinstaller ...`

---

## Definition of Done

- Feature works in-game
- No errors in console
- Does not degrade performance
- Includes verification steps