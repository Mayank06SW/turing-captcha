"""
display.py — All terminal output, colours, and prompt helpers.
Pure Python standard library only.
"""

import os
import sys
import time


# ── ANSI colour codes ─────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    BG_RED   = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE  = "\033[44m"


def _c(colour: str, text: str) -> str:
    return f"{colour}{text}{C.RESET}"


def clr():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def rule(char: str = "─", width: int = 66, colour: str = C.DIM + C.WHITE) -> None:
    print(_c(colour, char * width))


def header(title: str, subtitle: str = "", colour: str = C.CYAN) -> None:
    rule()
    print(_c(C.BOLD + colour, f"  {title}"))
    if subtitle:
        print(_c(C.DIM, f"  {subtitle}"))
    rule()


def banner() -> None:
    """Print the main application banner."""
    clr()
    rule("═", colour=C.BOLD + C.CYAN)
    lines = [
        "  TURING TEST & CAPTCHA",
        "  Terminal Implementation",
        "  Artificial Intelligence — Individual Assignment",
    ]
    for line in lines:
        print(_c(C.BOLD + C.CYAN, line))
    rule("═", colour=C.BOLD + C.CYAN)
    print()


def info(msg: str) -> None:
    print(_c(C.CYAN, f"  ℹ  {msg}"))


def success(msg: str) -> None:
    print(_c(C.GREEN, f"  ✔  {msg}"))


def warn(msg: str) -> None:
    print(_c(C.YELLOW, f"  ⚠  {msg}"))


def error(msg: str) -> None:
    print(_c(C.RED, f"  ✘  {msg}"))


def label(key: str, value: str, key_colour: str = C.DIM) -> None:
    print(f"  {_c(key_colour, key + ':')}  {value}")


def prompt(msg: str, colour: str = C.BOLD + C.WHITE) -> str:
    """Display a styled prompt and return stripped user input."""
    try:
        return input(f"\n  {_c(colour, '▶')}  {msg}  ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return "q"


def slow_print(msg: str, delay: float = 0.03, colour: str = C.WHITE) -> None:
    """Print a message character-by-character to simulate typing."""
    sys.stdout.write("  ")
    for ch in msg:
        sys.stdout.write(_c(colour, ch))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def verdict_banner(passed: bool, label_text: str = "") -> None:
    if passed:
        rule("▓", colour=C.BOLD + C.GREEN)
        print(_c(C.BOLD + C.GREEN, f"  ✔  PASS  {label_text}"))
        rule("▓", colour=C.BOLD + C.GREEN)
    else:
        rule("▓", colour=C.BOLD + C.RED)
        print(_c(C.BOLD + C.RED, f"  ✘  FAIL  {label_text}"))
        rule("▓", colour=C.BOLD + C.RED)
