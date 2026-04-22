#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt -r requirements-build.txt
python3 scripts/build.py

echo "Build completed: dist/FlappyNyanCat.app"
echo "You can double-click the app in Finder to open the game."
