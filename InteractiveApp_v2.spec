# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['InteractiveApp_v2.py'],
    pathex=[],
    binaries=[],
    datas=[('Asset 3.png', '.'), ('Asset 11.png', '.'), ('Asset 13.png', '.'), ('Asset 12.png', '.'), ('Asset 7.png', '.'), ('Asset 8.png', '.'), ('Asset 14.png', '.'), ('Asset 9.png', '.'), ('Asset 10.png', '.'), ('Asset 4.png', '.'), ('Asset 5.png', '.')],
    hiddenimports=[],
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
    name='InteractiveApp_v2',
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
    icon=['Asset 1.ico'],
)
