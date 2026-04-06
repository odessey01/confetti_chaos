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
pyinstaller --name confetti-chaos --onefile --add-data "assets;assets" src/main.py
```

The runtime path helpers in `src/systems/paths.py` support both normal and
frozen execution and ensure:
- no hardcoded absolute paths
- assets resolved from runtime root
- writable save directory at `<project-root>/saves` for local runs

## Validation commands

```powershell
python -m unittest discover -s tests -v
python src/main.py
```
