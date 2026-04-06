# Packaging Notes

## Local setup

Create a virtual environment and install the project in editable mode:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Run the game:

```powershell
python -m confetti_chaos
```

Or use the generated console script:

```powershell
confetti-chaos
```

## Distribution options

For Python package distribution:

```powershell
python -m pip install build
python -m build
```

This creates wheel and source distribution artifacts in `dist/`.

For a standalone desktop executable, PyInstaller is a common next step:

```powershell
pip install pyinstaller
pyinstaller --name confetti-chaos --onefile -m confetti_chaos
```

If the game later depends on sprites, sounds, or fonts, switch away from
`--onefile` or add explicit asset collection rules so packaged builds can
find those files at runtime.
