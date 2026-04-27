#!/usr/bin/env python3
"""A more playful hello-world script."""

from __future__ import annotations

import itertools
import shutil
import sys
import time


MESSAGE = "Hello, world!"
STARS = " .:*oO@"


def type_line(text: str, delay: float = 0.03) -> None:
    """Print a line one character at a time when stdout is interactive."""
    for character in text:
        print(character, end="", flush=True)
        if sys.stdout.isatty():
            time.sleep(delay)
    print()


def make_sky(width: int) -> list[str]:
    """Build a compact banner with a tiny orbit around the greeting."""
    width = max(32, min(width, 72))
    center = MESSAGE.center(width)
    border = "".join(STARS[(index * 3 + width) % len(STARS)] for index in range(width))
    orbit = "".join("*" if index % 11 == 0 else " " for index in range(width))
    return [border, orbit, center, orbit[::-1], border[::-1]]


def main() -> None:
    width = shutil.get_terminal_size(fallback=(60, 20)).columns
    sky = make_sky(width)

    print()
    for line in sky:
        type_line(line.rstrip())

    print()
    for word, sparkle in zip(MESSAGE.split(), itertools.cycle(["*", "+"])):
        type_line(f"{sparkle} {word}")

    type_line("\nGreetings delivered from a very small Python universe.")


if __name__ == "__main__":
    main()
