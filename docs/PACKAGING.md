# Packaging Notes

## Local setup

Create a virtual environment and install the project in editable mode:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Run the active vertical-slice game from repository root:

```powershell
python src/main.py
```

## Test commands

Primary test command used in active development:

```powershell
python -m pytest -q
```

Build script compatibility note:
- `build.ps1` currently runs `python -m unittest discover -s tests -v` unless `-SkipTests` is passed.
- If you prefer one test path, run `pytest` manually before build and use `.\build.ps1 -SkipTests`.

## Standalone build (recommended)

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

Run the repeatable build script from repo root:

```powershell
.\build.ps1
```

Equivalent direct command:

```powershell
python -m PyInstaller --noconfirm --clean confetti-chaos.spec
```

Output executable location:

```text
dist/confetti-chaos.exe
```

## Asset and save behavior

- Assets are bundled via `confetti-chaos.spec` (`assets/` -> `assets`).
- Runtime path helpers resolve assets in frozen mode.
- Save/high-score files are written to:
  - local dev run: `<repo>/saves`
  - packaged run: `%USERPROFILE%/confetti-chaos/saves`

## Validation commands

```powershell
python -m pytest -q
python src/main.py
```

## Packaged smoke test

After building:

1. Launch `dist/confetti-chaos.exe`.
2. Verify menu loads and start/restart work.
3. Verify hazards, collision, pause, and audio cues still function.
4. Verify run XP, level-up overlay, and 1-of-3 upgrade selection flow work.
5. Verify projectile cap starts at 3 and upgrades can raise it to 5.
6. Verify themed/animated background renders correctly and gameplay remains readable.
7. Verify high score persists across relaunch.
8. Close app cleanly with no crash.

## Local release checklist

- [ ] Tests pass (`python -m pytest -q`)
- [ ] Build succeeds (`.\build.ps1`)
- [ ] Packaged exe launches from `dist/confetti-chaos.exe`
- [ ] Assets (audio: `sfx/`, `music/`, `ambient/`) are present in packaged run
- [ ] Save/high score persists between launches
- [ ] Run progression + level-up upgrade flow is stable
- [ ] Projectile cap behavior is correct (start 3, upgrade max 5)
- [ ] Background theme/ambient layers render correctly during gameplay
- [ ] Menu/play/pause/game-over loop is stable
- [ ] Keyboard + controller input still work
- [ ] App exits cleanly without traceback
