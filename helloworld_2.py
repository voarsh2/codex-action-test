#!/usr/bin/env python3
"""A tiny terminal mission from a friendly Python universe."""

from __future__ import annotations

import itertools
import math
import random
import shutil
import sys
import time


MESSAGE = "Hello, world!"
SUBTITLE = "Greetings delivered from a very small Python universe."
STARS = " .:*oO@"
PLANETS = ("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Neptune")
TRANSMISSION = (
    "Booting pocket observatory",
    "Tuning cosmic antenna",
    "Polishing the greeting",
    "Launching hello beacon",
)
MASCOT = (
    "        /\\",
    "       /  \\",
    "      /_[]_\\",
    "      |    |",
    "     /|_||_|\\",
    "    /_      _\\",
    "      '--`--'",
)
SOUVENIRS = (
    "a pocket-sized sunrise",
    "three polite moonbeams",
    "one certified fresh exclamation point",
    "a tiny orchestra warming up in the margins",
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


def make_sky(width: int, height: int = 7) -> list[str]:
    """Build a compact star field with a wave running through it."""
    rows: list[str] = []
    for y in range(height):
        row = []
        for x in range(width):
            wave = math.sin((x / 5) + y) + math.cos((x / 9) - y)
            if x % 29 == y * 3 % 29:
                row.append("@")
            elif wave > 1.55:
                row.append("*")
            elif wave > 1.25:
                row.append(".")
            else:
                row.append(" ")
        rows.append("".join(row).rstrip())

    rows[height // 2] = f"  {MESSAGE}  ".center(width, "-")
    return rows


def frame(lines: list[str], width: int) -> list[str]:
    """Wrap lines in a simple box that adapts to terminal width."""
    inner = width - 4
    top = "." + "-" * (width - 2) + "."
    bottom = "'" + "-" * (width - 2) + "'"
    return [top, *(f"| {line[:inner]:<{inner}} |" for line in lines), bottom]


def print_countdown() -> None:
    """Show a small launch sequence before the greeting appears."""
    for step, label in enumerate(TRANSMISSION, start=1):
        type_line(f"[{step:02}] {label}...")

    for number in range(3, 0, -1):
        type_line(f"    T-{number}")
    type_line("    Liftoff.")


def print_mascot(width: int) -> None:
    """Send a little ASCII rocket through the output."""
    for line in frame(list(MASCOT), width):
        type_line(line)


def build_manifest() -> list[tuple[str, str]]:
    """Create deterministic mission details so the surprise is replayable."""
    rng = random.Random(MESSAGE)
    destination = rng.choice(PLANETS)
    signal_strength = rng.randint(88, 99)
    souvenir = rng.choice(SOUVENIRS)
    orbit_count = rng.randint(4, 9)
    return [
        ("Destination", destination),
        ("Signal", f"{signal_strength}% bright"),
        ("Payload", MESSAGE),
        ("Orbits", f"{orbit_count} cheerful loops"),
        ("Souvenir", souvenir),
        ("Status", "Received with a grin"),
    ]


def print_postcard(width: int) -> None:
    """Print a small table of invented dispatch details."""
    border = "+" + "-" * (width - 2) + "+"

    print(border)
    for label, value in build_manifest():
        text = f" {label:<12} | {value}"
        print(f"|{text:<{width - 2}}|")
    print(border)


def print_echoes() -> None:
    """Echo each word with a rotating sparkle marker."""
    for word, sparkle in zip(MESSAGE.split(), itertools.cycle(["*", "+", "."])):
        type_line(f"{sparkle} {word}")


def print_decoder_ring(width: int) -> None:
    """Reveal the greeting as a playful Caesar-shift decode."""
    shift = 7
    encoded = []
    for character in MESSAGE:
        if character.isalpha():
            base = ord("A") if character.isupper() else ord("a")
            encoded.append(chr(base + (ord(character) - base + shift) % 26))
        else:
            encoded.append(character)

    type_line("Decoder ring:")
    print("  encoded :", "".join(encoded))
    print("  decoded :", MESSAGE)
    print("  checksum:", sum(ord(character) for character in MESSAGE) % width)


def main() -> None:
    width = terminal_width()
    sky = make_sky(width)

    print()
    print_countdown()
    print()

    for line in sky:
        type_line(line.rstrip())

    print()
    print_mascot(width)
    print()
    print_postcard(width)
    print()
    print_decoder_ring(width)
    print()
    print_echoes()
    type_line(f"\n{SUBTITLE}")


if __name__ == "__main__":
    main()
