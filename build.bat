@echo off
title GMail-Bomber Builder
pip install pyinstaller
pyinstaller --icon=res/icon.ico --onefile --noconsole gmail_bomber.py
rmdir /s /q "./build/"
ren dist build
del "*.spec"
pause
