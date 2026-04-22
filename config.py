"""Global configuration for Flappy Nyan Cat PRO."""

import sys
from pathlib import Path

# Window
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
TITLE = "Flappy Nyan Cat PRO"

# Physics
GRAVITY = 1400.0
JUMP_VELOCITY = -420.0
MAX_FALL_SPEED = 620.0
PLAYER_START_X = 220
PLAYER_START_Y = SCREEN_HEIGHT // 2

# Pipes
PIPE_WIDTH = 110
PIPE_GAP = 180
PIPE_SPAWN_SECONDS = 1.45
PIPE_SPAWN_MIN = 0.95
PIPE_SPEED_BASE = 230.0
PIPE_SPEED_MAX = 420.0
PIPE_SPEED_SCORE_MULTIPLIER = 7.5

# Gameplay
POINTS_PER_PIPE = 1

# Colors
SPACE_TOP = (11, 22, 61)
SPACE_BOTTOM = (33, 7, 52)
STAR_COLOR = (255, 255, 214)
TEXT_MAIN = (245, 247, 255)
TEXT_ACCENT = (132, 235, 255)
TEXT_WARNING = (255, 170, 175)
PIPE_BODY = (93, 224, 126)
PIPE_EDGE = (37, 122, 65)
PIPE_CAP = (133, 242, 157)

# Paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"


def _resolve_user_data_dir() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "FlappyNyanCat"
    if sys.platform.startswith("win"):
        appdata = Path.home() / "AppData" / "Roaming"
        return appdata / "FlappyNyanCat"
    return Path.home() / ".flappynyancat"


USER_DATA_DIR = _resolve_user_data_dir()
HIGH_SCORE_FILE = USER_DATA_DIR / "highscore.txt"
