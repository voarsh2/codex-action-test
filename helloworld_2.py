#!/usr/bin/env python3
"""A tiny terminal postcard from a friendly Python universe."""

from __future__ import annotations

import itertools
import random
import shutil
import sys
import time


MESSAGE = "Hello, world!"
SUBTITLE = "Greetings delivered from a very small Python universe."
STARS = " .:*oO@"
PLANETS = ("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn")
TRANSMISSION = (
    "Booting pocket observatory",
    "Tuning cosmic antenna",
    "Polishing the greeting",
    "Launching hello beacon",
)


def type_line(text: str, delay: float = 0.03) -> None:
    """Print a line one character at a time when stdout is interactive."""
    for character in text:
        print(character, end="", flush=True)
        if sys.stdout.isatty():
            time.sleep(delay)
    print()


def terminal_width() -> int:
    """Return a friendly content width for the current terminal."""
    columns = shutil.get_terminal_size(fallback=(70, 20)).columns
    return max(42, min(columns, 78))


def make_sky(width: int) -> list[str]:
    """Build a compact banner with orbit lines around the greeting."""
    center = f"  {MESSAGE}  ".center(width, "-")
    border = "".join(STARS[(index * 3 + width) % len(STARS)] for index in range(width))
    orbit = "".join("*" if index % 13 == 0 else "." if index % 7 == 0 else " " for index in range(width))
    return [border, orbit, center, orbit[::-1], border[::-1]]


def print_countdown() -> None:
    """Show a small launch sequence before the greeting appears."""
    for step, label in enumerate(TRANSMISSION, start=1):
        type_line(f"[{step:02}] {label}...")


def print_postcard(width: int) -> None:
    """Print a small table of invented dispatch details."""
    rng = random.Random(MESSAGE)
    destination = rng.choice(PLANETS)
    signal_strength = rng.randint(88, 99)
    border = "+" + "-" * (width - 2) + "+"
    rows = [
        ("Destination", destination),
        ("Signal", f"{signal_strength}% bright"),
        ("Payload", MESSAGE),
        ("Status", "Received with a grin"),
    ]

    print(border)
    for label, value in rows:
        text = f" {label:<12} | {value}"
        print(f"|{text:<{width - 2}}|")
    print(border)


def print_echoes() -> None:
    """Echo each word with a rotating sparkle marker."""
    for word, sparkle in zip(MESSAGE.split(), itertools.cycle(["*", "+", "."])):
        type_line(f"{sparkle} {word}")


def main() -> None:
    width = terminal_width()
    sky = make_sky(width)

    print()
    print_countdown()
    print()

    for line in sky:
        type_line(line.rstrip())

    print()
    print_postcard(width)
    print()
    print_echoes()
    type_line(f"\n{SUBTITLE}")


if __name__ == "__main__":
    main()
