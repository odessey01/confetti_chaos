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
python -m unittest discover -s tests -v
python src/main.py
```

## Packaged smoke test

After building:

1. Launch `dist/confetti-chaos.exe`.
2. Verify menu loads and start/restart work.
3. Verify hazards, collision, pause, and audio cues still function.
4. Verify high score persists across relaunch.
5. Close app cleanly with no crash.

## Local release checklist

- [ ] Unit tests pass (`python -m unittest discover -s tests -v`)
- [ ] Build succeeds (`.\build.ps1`)
- [ ] Packaged exe launches from `dist/confetti-chaos.exe`
- [ ] Assets (audio) are present in packaged run
- [ ] Save/high score persists between launches
- [ ] Menu/play/pause/game-over loop is stable
- [ ] Keyboard + controller input still work
- [ ] App exits cleanly without traceback
