from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import EXE, PYZ
from os import path
from shutil import copytree

analysis = Analysis(
    scripts=['main.py'],
    pathex=[path.abspath('.')],
    datas=[('.env', '.')],
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

copytree(path.abspath("storage"), path.abspath(path.join("dist", "storage")), dirs_exist_ok=True)
