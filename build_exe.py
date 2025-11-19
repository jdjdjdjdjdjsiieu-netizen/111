"""
Build Executable for Windows
Создание исполняемого .exe файла с помощью PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

print("""
╔════════════════════════════════════════════════════════════╗
║   ALFA CAMPAIGN MANAGER - Build Executable                 ║
║   Создание исполняемого файла для Windows                  ║
╚════════════════════════════════════════════════════════════╝
""")

# Проверка PyInstaller
print("[1/4] Проверка PyInstaller...")
try:
    import PyInstaller
    print("✓ PyInstaller установлен")
except ImportError:
    print("⚠ PyInstaller не установлен. Устанавливаю...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller установлен")

print()

# Создание spec файла
print("[2/4] Создание конфигурации...")

spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
        ('.env', '.'),
        ('*.py', '.'),
        ('*.tsx', '.'),
        ('*.ts', '.'),
        ('*.md', '.'),
    ],
    hiddenimports=[
        'telethon',
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'aiohttp',
        'google.generativeai',
        'groq',
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
    name='AlfaCampaignManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""

spec_file = Path("AlfaCampaignManager.spec")
spec_file.write_text(spec_content)
print(f"✓ Создан файл: {spec_file}")
print()

# Сборка
print("[3/4] Сборка исполняемого файла...")
print("Это может занять несколько минут...")
print()

try:
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file)
    ])
    print()
    print("✓ Сборка завершена")
except subprocess.CalledProcessError as e:
    print(f"\n✗ Ошибка сборки: {e}")
    sys.exit(1)

print()

# Проверка результата
print("[4/4] Проверка результата...")
exe_file = Path("dist/AlfaCampaignManager.exe")
if exe_file.exists():
    size_mb = exe_file.stat().st_size / (1024 * 1024)
    print(f"✓ Исполняемый файл создан: {exe_file}")
    print(f"  Размер: {size_mb:.1f} MB")
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   ГОТОВО!                                                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"Исполняемый файл: dist/AlfaCampaignManager.exe")
    print()
    print("Для запуска:")
    print("  1. Скопируйте AlfaCampaignManager.exe в папку проекта")
    print("  2. Дважды кликните на AlfaCampaignManager.exe")
    print("  3. Следуйте инструкциям на экране")
    print()
else:
    print("✗ Исполняемый файл не найден!")
    print("  Проверьте логи выше для деталей")
    sys.exit(1)
"""

if __name__ == "__main__":
    pass
