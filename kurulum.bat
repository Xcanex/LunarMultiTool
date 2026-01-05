@echo off
title Lunar Tool
color 0a

python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python yüklü değil veya PATH eklenmemiş
    pause
    exit /b
)

echo [+] Gerekli kütüphaneler yükleniyor...
pip install --upgrade --force-reinstall -r requirements.txt

echo.
echo [+] Lunar Tool baslatiliyor...
python LunarTool.py

pause
