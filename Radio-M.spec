# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Radio-M.py'],
    pathex=[],
    binaries=[],
    datas=[('WL.jpg', '.'), ('guitar_emoji.png', '.'), ('rock_on_emoji.png', '.'), ('R.ico', '.'), ('custom_font.ttf', '.')],
    hiddenimports=['vlc'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Radio-M',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['R.ico'],
)
