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
- P: pausar/reanudar durante partida
- M: volver al menu principal
- R: reiniciar desde Game Over
- ESC: salir

## Crear Ejecutable (Sin VS Code)

### macOS (.app)

```bash
chmod +x build_mac.sh
./build_mac.sh
```

Resultado: `dist/FlappyNyanCat.app`

Haz doble click sobre la app para abrir el juego.

### macOS (.dmg instalable)

```bash
chmod +x build_mac_release.sh
./build_mac_release.sh
```

Resultados:

- `dist/FlappyNyanCat.app`
- `dist/FlappyNyanCat-macOS.dmg`

### Windows (.exe)

En PowerShell o CMD:

```bat
build_windows.bat
```

Resultado: `dist\\FlappyNyanCat\\FlappyNyanCat.exe`

Haz doble click sobre el `.exe` para abrir el juego.

### Windows (instalador)

1. Instala Inno Setup 6 (una sola vez):
    - https://jrsoftware.org/isdl.php
2. Ejecuta:

```bat
build_windows_installer.bat
```

Resultado: `dist\\FlappyNyanCat-Setup-Windows.exe`

Este instalador crea acceso directo en escritorio y menu inicio.

### Icono Personalizado

- En macOS: agrega `assets/images/icon.icns` antes de compilar.
- En Windows: agrega `assets/images/icon.ico` antes de compilar.

Si esos archivos no existen, el ejecutable se genera con icono por defecto.

### Build Automatico Para macOS y Windows (GitHub Actions)

Tambien puedes generar ambos ejecutables desde GitHub sin abrir VS Code:

1. Ve a la pestana Actions del repositorio.
2. Ejecuta el workflow `Build Distributables`.
3. Descarga los artifacts:
    - `FlappyNyanCat-macOS-app`
    - `FlappyNyanCat-macOS-dmg`
    - `FlappyNyanCat-Windows-portable`
    - `FlappyNyanCat-Windows-Setup`

## Notas

- Si no hay assets externos, el juego usa graficos y sonidos generados en runtime.
- Puedes reemplazar o agregar recursos en assets/images y assets/sounds.
