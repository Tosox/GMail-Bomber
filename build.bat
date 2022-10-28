@echo off
title GMail-Bomber Builder
pyinstaller --icon=res/icon.ico --onefile --noconsole gmail_bomber.py
rmdir /s /q "./build/"
ren dist build
del "*.spec"
pause
