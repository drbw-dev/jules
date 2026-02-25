@echo off
echo Building executable...
set PYTHONPATH=%~dp0libs;%PYTHONPATH%
pyinstaller --onefile --paths=libs --hidden-import=ursina --hidden-import=src.assets --hidden-import=src.level_gen --hidden-import=src.player --hidden-import=src.enemy --name="HorrorGame" src/main.py
echo Build complete. executable is in dist/
pause
