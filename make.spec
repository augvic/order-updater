from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import EXE, PYZ
import os

analysis = Analysis(
    scripts=['main.py'],
    pathex=[os.path.abspath('.')],
    optimize=0
)

pyz = PYZ(analysis.pure)

exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    name='OrderUpdater',
    upx=True,
    icon="icon.ico"
)
