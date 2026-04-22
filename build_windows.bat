@echo off
setlocal

py -m pip install -r requirements.txt -r requirements-build.txt
py scripts\build.py

echo Build completed: dist\FlappyNyanCat\FlappyNyanCat.exe
echo Double-click the .exe to open the game.
