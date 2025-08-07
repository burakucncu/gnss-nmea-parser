# -*- mode: python ; coding: utf-8 -*-
"""
NMEA Parser PyInstaller Specification File
==========================================
This file contains the configuration for building NMEA_Parser.exe
using PyInstaller. It includes all necessary dependencies and settings
for creating a standalone executable.

Usage:
    pyinstaller NMEA_Parser.spec

Requirements:
    - Python 3.11+
    - PyQt5 5.15.10
    - PyInstaller 6.3.0
    - All dependencies listed in requirements.txt
"""

block_cipher = None

a = Analysis(
    ['NMEA/gui.py'],  # Main application entry point
    pathex=[],
    binaries=[],
    datas=[
        ('NMEA/nmea.py', '.'),  # Include NMEA parsing module
        # Add any additional data files here if needed
    ],
    hiddenimports=[
        # PyQt5 WebEngine dependencies for map functionality
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore', 
        'PyQt5.QtWebChannel',
        'PyQt5.QtWebEngine',
        
        # Core PyQt5 modules
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        
        # Mapping and web-related dependencies
        'folium',
        'folium.plugins',
        'branca',
        'branca.colormap',
        'jinja2',
        'markupsafe',
        'requests',
        
        # Standard library modules (usually auto-detected but included for safety)
        'json',
        'csv',
        'tempfile',
        'subprocess',
        'shutil',
        'os',
        'sys'
    ],
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
    name='NMEA_Parser',
    debug=False,                    # Set to True for debugging
    bootloader_ignore_signals=False,
    strip=False,                    # Strip symbols to reduce size
    upx=True,                      # Compress executable with UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                 # Hide console window for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None                      # Add path to .ico file if you have an icon
)
