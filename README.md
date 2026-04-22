# Flappy Nyan Cat PRO

Juego estilo Flappy Bird hecho en Python + Pygame, con tema espacial y Nyan Cat animado.

## Caracteristicas PRO

- Fisica mejorada con gravedad suave y salto fluido
- Sistema de puntos con HUD visible
- Dificultad progresiva (velocidad y spawn dinamicos)
- Colisiones precisas con mascaras
- Reinicio rapido sin cerrar el juego (R)
- Pantallas de inicio y Game Over
- Fondo espacial animado
- Sonidos sintetizados (salto/colision) + musica de fondo opcional
- Guardado de high score en archivo local

## Estructura

```text
FlappyNyanCat/
|-- main.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- setup_project.sh
|-- highscore.txt
|-- assets/
|   |-- images/
|   |   `-- .gitkeep
|   `-- sounds/
|       `-- .gitkeep
`-- src/
    |-- game.py
    |-- player.py
    |-- pipes.py
    |-- ui.py
    `-- utils.py
```

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
python main.py
```

## Controles

- SPACE: iniciar y saltar
- R: reiniciar desde Game Over
- ESC: salir

## Notas

- Si no hay assets externos, el juego usa graficos y sonidos generados en runtime.
- Puedes reemplazar o agregar recursos en assets/images y assets/sounds.
