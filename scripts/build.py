"""Build standalone app with PyInstaller for the current OS."""

from __future__ import annotations

import platform
from pathlib import Path

import PyInstaller.__main__


PROJECT_NAME = "FlappyNyanCat"
ROOT_DIR = Path(__file__).resolve().parent.parent


def _data_separator() -> str:
    return ";" if platform.system() == "Windows" else ":"


def _icon_arg() -> list[str]:
    images_dir = ROOT_DIR / "assets" / "images"
    if platform.system() == "Darwin":
        icon = images_dir / "icon.icns"
    elif platform.system() == "Windows":
        icon = images_dir / "icon.ico"
    else:
        return []

    if icon.exists():
        return ["--icon", str(icon)]
    return []


def main() -> None:
    sep = _data_separator()
    main_path = ROOT_DIR / "main.py"
    assets_path = ROOT_DIR / "assets"
    args = [
        "--noconfirm",
        "--clean",
        "--specpath",
        "build",
        "--windowed",
        "--name",
        PROJECT_NAME,
        "--add-data",
        f"{assets_path}{sep}assets",
        str(main_path),
    ]

    args.extend(_icon_arg())

    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    main()
