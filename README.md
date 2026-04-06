# confetti_chaos
Pop, burst, and chain-react your way through colorful roguelite chaos. A kid-friendly ARPG where balloons are the enemies and every run is a confetti-filled adventure.

## Foundation

This repository now includes a small Python game scaffold with:

- `src/confetti_chaos/settings.py` for app settings and runtime paths
- `src/confetti_chaos/scenes/` for a simple scene manager plus starter scenes
- `src/confetti_chaos/save_data.py` for JSON save/load support
- `src/main.py` as the active vertical-slice game entry point
- `pyproject.toml` and `requirements.txt` for dependencies and packaging
- `docs/PACKAGING.md` for install/build notes

## Project structure

```text
confetti_chaos/
|-- docs/
|   `-- PACKAGING.md
|-- src/
|   |-- main.py
|   `-- confetti_chaos/
|       |-- scenes/
|       |   |-- base.py
|       |   |-- gameplay.py
|       |   |-- manager.py
|       |   `-- title.py
|       |-- game.py
|       |-- save_data.py
|       `-- settings.py
|-- LICENSE
|-- pyproject.toml
`-- requirements.txt
```

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python src/main.py
```
