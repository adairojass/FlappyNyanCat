@echo off
setlocal

call build_windows.bat
if errorlevel 1 exit /b %errorlevel%

set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist %ISCC% (
  %ISCC% installer\windows\FlappyNyanCat.iss
  if errorlevel 1 exit /b %errorlevel%
  echo Installer created: dist\FlappyNyanCat-Setup-Windows.exe
) else (
  echo Inno Setup 6 not found.
  echo Install from: https://jrsoftware.org/isdl.php
  echo Portable executable remains available at: dist\FlappyNyanCat\FlappyNyanCat.exe
)
