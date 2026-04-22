#!/bin/bash

set -e

PROJECT_NAME="FlappyNyanCat"
DESKTOP="$HOME/Desktop"

mkdir -p "$DESKTOP/$PROJECT_NAME"
cd "$DESKTOP/$PROJECT_NAME" || exit

mkdir -p assets/images
mkdir -p assets/sounds
mkdir -p src

touch main.py
touch config.py
touch requirements.txt
touch README.md

touch src/game.py
touch src/player.py
touch src/pipes.py
touch src/ui.py
touch src/utils.py

echo "pygame>=2.5.0" > requirements.txt

cat <<EOL > README.md
# Flappy Nyan Cat PRO

Juego desarrollado en Python con Pygame.

## Instalacion

pip install -r requirements.txt

## Ejecutar

python main.py
EOL

cat <<EOL > .gitignore
__pycache__/
*.py[cod]
.env
venv/
.DS_Store
EOL

if [ ! -d .git ]; then
  git init
fi

git add .
if ! git diff --cached --quiet; then
  git commit -m "Initial commit - base structure Flappy Nyan Cat PRO"
fi

echo "Proyecto creado en el escritorio: $PROJECT_NAME"
