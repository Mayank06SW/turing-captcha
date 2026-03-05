"""
engine/terminal.py
All terminal output: ANSI colours, printing helpers, UI frames.
Pure Python standard library only.
"""

import os, sys, time, textwrap

# ── ANSI ──────────────────────────────────────────────────────────────────────
class A:
    R  = "\033[0m"
    B  = "\033[1m"
    DM = "\033[2m"
    IT = "\033[3m"

    RED  = "\033[31m"; GRN = "\033[32m"; YLW = "\033[33m"
    BLU  = "\033[34m"; MAG = "\033[35m"; CYN = "\033[36m"
    WHT  = "\033[37m"; GRY = "\033[90m"

    BG_RED   = "\033[41m"
    BG_GRN   = "\033[42m"
    BG_YLW   = "\033[43m"
    BG_BLU   = "\033[44m"


def c(colour, text):
    return f"{colour}{text}{A.R}"


def clr():
    os.system("cls" if os.name == "nt" else "clear")


def line(char="─", n=68, col=A.GRY):
    print(c(col, char * n))


def pause(msg="  Press ENTER to continue…"):
    input(c(A.GRY, msg))


def ask(prompt_text, col=A.B + A.WHT):
    try:
        return input(f"\n  {c(col, '▶')}  {prompt_text}  ").strip()
    except (KeyboardInterrupt, EOFError):
        print(); return "q"


def typewrite(text, delay=0.025, col=A.WHT, indent=2):
    """Print text character by character — typewriter effect."""
    prefix = " " * indent
    sys.stdout.write(prefix)
    for ch in text:
        sys.stdout.write(c(col, ch))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def boxed(lines, width=64, border_col=A.GRY, text_col=A.WHT):
    """Print lines inside a box."""
    print(c(border_col, "  ┌" + "─" * width + "┐"))
    for ln in lines:
        wrapped = textwrap.wrap(ln, width - 2) or [""]
        for wl in wrapped:
            pad = " " * (width - 2 - len(wl))
            print(c(border_col, "  │ ") + c(text_col, wl + pad) + c(border_col, " │"))
    print(c(border_col, "  └" + "─" * width + "┘"))


def status(kind, msg):
    icons = {"ok": (A.GRN, "✔"), "fail": (A.RED, "✘"),
             "info": (A.CYN, "ℹ"), "warn": (A.YLW, "⚠")}
    col, icon = icons.get(kind, (A.WHT, "·"))
    print(c(col, f"  {icon}  {msg}"))


def verdict_screen(passed, headline, detail=""):
    print()
    if passed:
        line("▓", col=A.B + A.GRN)
        print(c(A.B + A.GRN, f"  ✔  {headline}"))
        if detail: print(c(A.GRN, f"     {detail}"))
        line("▓", col=A.B + A.GRN)
    else:
        line("▓", col=A.B + A.RED)
        print(c(A.B + A.RED, f"  ✘  {headline}"))
        if detail: print(c(A.RED, f"     {detail}"))
        line("▓", col=A.B + A.RED)
    print()
