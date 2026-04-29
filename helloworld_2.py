#!/usr/bin/env python3
"""A tiny terminal mission from a friendly Python universe."""

from __future__ import annotations

import itertools
import math
import argparse
import random
import shutil
import sys
import time


MESSAGE = "Hello, world!"
SUBTITLE = "Greetings delivered from a very small Python universe."
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
THEMES = {
    "space": {
        "accent": "\033[96m",
        "muted": "\033[90m",
        "success": "\033[92m",
        "warning": "\033[93m",
    },
    "ocean": {
        "accent": "\033[94m",
        "muted": "\033[36m",
        "success": "\033[92m",
        "warning": "\033[96m",
    },
    "retro": {
        "accent": "\033[95m",
        "muted": "\033[33m",
        "success": "\033[92m",
        "warning": "\033[91m",
    },
}
RESET = "\033[0m"
SCENES = {
    "launch": (
        "Fueling the teacup thrusters",
        "Teaching the stars to wave back",
        "Requesting runway clearance from the Moon",
    ),
    "orbit": (
        "Parking beside a careful satellite",
        "Taking attendance in the asteroid belt",
        "Broadcasting the greeting in slow circles",
    ),
    "landing": (
        "Unfolding the welcome ramp",
        "Planting a tiny flag labeled hello",
        "Opening the souvenir compartment",
    ),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line controls for the mini mission."""
    parser = argparse.ArgumentParser(description="Launch a tiny hello-world mission.")
    parser.add_argument("--fast", action="store_true", help="skip typewriter pauses")
    parser.add_argument("--quiet", action="store_true", help="skip the countdown")
    parser.add_argument("--message", default=MESSAGE, help="custom greeting payload")
    parser.add_argument("--theme", choices=tuple(THEMES), default="space")
    parser.add_argument("--scene", choices=tuple(SCENES), default="launch")
    parser.add_argument("--name", help="mission commander name")
    parser.add_argument("--destination", choices=PLANETS, help="destination planet")
    return parser.parse_args(argv)


def colorize(text: str, color: str, enabled: bool) -> str:
    """Wrap text in ANSI color when terminal output supports it."""
    if not enabled:
        return text
    return f"{color}{text}{RESET}"


def type_line(text: str, delay: float = 0.03, fast: bool = False) -> None:
    """Print a line one character at a time when stdout is interactive."""
    for character in text:
        print(character, end="", flush=True)
        if sys.stdout.isatty() and not fast:
            time.sleep(delay)
    print()


def terminal_width() -> int:
    """Return a friendly content width for the current terminal."""
    columns = shutil.get_terminal_size(fallback=(70, 20)).columns
    return max(42, min(columns, 78))


def make_sky(width: int, height: int = 7, message: str = MESSAGE) -> list[str]:
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

    rows[height // 2] = f"  {message}  ".center(width, "-")
    return rows


def frame(lines: list[str], width: int) -> list[str]:
    """Wrap lines in a simple box that adapts to terminal width."""
    inner = width - 4
    top = "." + "-" * (width - 2) + "."
    bottom = "'" + "-" * (width - 2) + "'"
    return [top, *(f"| {line[:inner]:<{inner}} |" for line in lines), bottom]


def print_countdown(fast: bool = False, colors: dict[str, str] | None = None) -> None:
    """Show a small launch sequence before the greeting appears."""
    for step, label in enumerate(TRANSMISSION, start=1):
        marker = f"[{step:02}]"
        if colors:
            marker = colorize(marker, colors["muted"], sys.stdout.isatty())
        type_line(f"{marker} {label}...", fast=fast)

    for number in range(3, 0, -1):
        type_line(f"    T-{number}", fast=fast)
    type_line("    Liftoff.", fast=fast)


def print_mascot(width: int, fast: bool = False) -> None:
    """Send a little ASCII rocket through the output."""
    for line in frame(list(MASCOT), width):
        type_line(line, fast=fast)


def build_manifest(
    message: str = MESSAGE,
    name: str = "friend",
    destination: str | None = None,
    scene: str = "launch",
) -> list[tuple[str, str]]:
    """Create deterministic mission details so the surprise is replayable."""
    rng = random.Random(f"{message}:{name}:{scene}")
    destination = destination or rng.choice(PLANETS)
    signal_strength = rng.randint(88, 99)
    souvenir = rng.choice(SOUVENIRS)
    orbit_count = rng.randint(4, 9)
    return [
        ("Commander", name),
        ("Destination", destination),
        ("Scene", scene),
        ("Signal", f"{signal_strength}% bright"),
        ("Payload", message),
        ("Orbits", f"{orbit_count} cheerful loops"),
        ("Souvenir", souvenir),
        ("Status", "Received with a grin"),
    ]


def print_postcard(
    width: int,
    message: str,
    name: str,
    destination: str,
    scene: str,
    colors: dict[str, str],
) -> None:
    """Print a small table of invented dispatch details."""
    border = "+" + "-" * (width - 2) + "+"

    print(border)
    for label, value in build_manifest(message, name, destination, scene):
        text = f" {label:<12} | {value}"
        if label in {"Destination", "Scene"}:
            text = colorize(text, colors["accent"], sys.stdout.isatty())
        print(f"|{text:<{width - 2}}|")
    print(border)


def print_echoes(message: str, fast: bool = False, colors: dict[str, str] | None = None) -> None:
    """Echo each word with a rotating sparkle marker."""
    for word, sparkle in zip(message.split(), itertools.cycle(["*", "+", "."])):
        marker = colorize(sparkle, colors["warning"], sys.stdout.isatty()) if colors else sparkle
        type_line(f"{marker} {word}", fast=fast)


def decode_payload(message: str, shift: int = 7) -> tuple[str, str, int]:
    """Encode and decode a greeting with a tiny Caesar-shift ring."""
    encoded = []
    for character in message:
        if character.isalpha():
            base = ord("A") if character.isupper() else ord("a")
            encoded.append(chr(base + (ord(character) - base + shift) % 26))
        else:
            encoded.append(character)
    return "".join(encoded), message, sum(ord(character) for character in message)


def print_decoder_ring(width: int, message: str, fast: bool = False) -> None:
    """Reveal the greeting as a playful Caesar-shift decode."""
    encoded, decoded, checksum = decode_payload(message)
    type_line("Decoder ring:", fast=fast)
    print("  encoded :", encoded)
    print("  decoded :", decoded)
    print("  checksum:", checksum % width)


def prompt_name(provided: str | None) -> str:
    """Return the chosen commander name, prompting only in interactive use."""
    if provided:
        return provided.strip() or "friend"
    if sys.stdin.isatty():
        answer = input("Mission commander name: ").strip()
        return answer or "friend"
    return "friend"


def choose_destination(provided: str | None, fast: bool = False) -> str:
    """Pick a planet interactively when possible, otherwise use a default."""
    if provided:
        return provided
    if not sys.stdin.isatty():
        return "Mars"

    print("Choose a destination:")
    for index, planet in enumerate(PLANETS, start=1):
        print(f"  {index}. {planet}")
    answer = input("Planet number or name [Mars]: ").strip()
    if not answer:
        return "Mars"
    if answer.isdigit() and 1 <= int(answer) <= len(PLANETS):
        return PLANETS[int(answer) - 1]
    for planet in PLANETS:
        if answer.lower() == planet.lower():
            return planet
    type_line("Unknown coordinates. Setting course for Mars.", fast=fast)
    return "Mars"


def print_scene(scene: str, fast: bool, colors: dict[str, str]) -> None:
    """Print the selected mini-scene."""
    heading = colorize(f"Mini-scene: {scene}", colors["success"], sys.stdout.isatty())
    type_line(heading, fast=fast)
    for line in SCENES[scene]:
        type_line(f"  - {line}", fast=fast)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    width = terminal_width()
    colors = THEMES[args.theme]
    name = prompt_name(args.name)
    destination = choose_destination(args.destination, args.fast)
    sky = make_sky(width, message=args.message)

    print()
    if not args.quiet:
        print_countdown(args.fast, colors)
        print()

    for line in sky:
        type_line(colorize(line.rstrip(), colors["accent"], sys.stdout.isatty()), fast=args.fast)

    print()
    print_scene(args.scene, args.fast, colors)
    print()
    print_mascot(width, args.fast)
    print()
    print_postcard(width, args.message, name, destination, args.scene, colors)
    print()
    print_decoder_ring(width, args.message, args.fast)
    print()
    print_echoes(args.message, args.fast, colors)
    type_line(f"\nCommander {name}, {SUBTITLE}", fast=args.fast)


if __name__ == "__main__":
    main()
