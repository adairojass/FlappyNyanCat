"""Utility helpers for persistence, stars and audio synthesis."""

from __future__ import annotations

import math
import random
from array import array
from pathlib import Path
from typing import Any

import pygame


Star = dict[str, Any]


def load_high_score(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        value = int(path.read_text(encoding="utf-8").strip() or "0")
        return max(0, value)
    except (ValueError, OSError):
        return 0


def save_high_score(path: Path, score: int) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(max(0, int(score))), encoding="utf-8")
    except OSError:
        # The game remains playable even if persistence fails.
        pass


def build_starfield(count: int, width: int, height: int) -> list[Star]:
    stars: list[Star] = []
    for _ in range(count):
        stars.append(
            {
                "x": random.uniform(0, width),
                "y": random.uniform(0, height),
                "speed": random.uniform(12, 120),
                "radius": random.randint(1, 3),
                "twinkle": random.uniform(0.7, 1.0),
                "phase": random.uniform(0, math.tau),
            }
        )
    return stars


def update_starfield(stars: list[Star], dt: float, width: int, height: int) -> None:
    for star in stars:
        star["x"] -= star["speed"] * dt
        star["phase"] += dt * random.uniform(0.8, 1.6)
        if star["x"] < -4:
            star["x"] = width + random.uniform(2, 30)
            star["y"] = random.uniform(0, height)
            star["speed"] = random.uniform(12, 120)


def make_tone(
    frequency: float,
    duration: float,
    volume: float = 0.35,
    sample_rate: int = 44100,
) -> pygame.mixer.Sound:
    n_samples = max(1, int(sample_rate * duration))
    buf = array("h")
    amp = int(max(0.0, min(1.0, volume)) * 32767)
    for i in range(n_samples):
        t = i / sample_rate
        sample = int(amp * math.sin(2 * math.pi * frequency * t))
        buf.append(sample)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_chime(
    notes: list[float],
    note_duration: float = 0.14,
    volume: float = 0.2,
    sample_rate: int = 44100,
) -> pygame.mixer.Sound:
    buf = array("h")
    amp = int(max(0.0, min(1.0, volume)) * 32767)
    for freq in notes:
        note_samples = max(1, int(sample_rate * note_duration))
        for i in range(note_samples):
            t = i / sample_rate
            env = max(0.0, 1.0 - i / note_samples)
            sample = int(amp * env * math.sin(2 * math.pi * freq * t))
            buf.append(sample)
    return pygame.mixer.Sound(buffer=buf.tobytes())
