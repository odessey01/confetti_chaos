# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_root = Path(SPECPATH)  # provided by PyInstaller runtime
src_root = project_root / "src"
assets_root = project_root / "assets"
demo_mode_flag = project_root / "build_flags" / "demo_mode.flag"

block_cipher = None
datas = [(str(assets_root), "assets")]
if demo_mode_flag.exists():
    datas.append((str(demo_mode_flag), "build_flags"))

a = Analysis(
    [str(src_root / "main.py")],
    pathex=[str(src_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="confetti-chaos",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
