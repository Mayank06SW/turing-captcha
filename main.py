"""
main.py — Entry point.

TURING TEST & CAPTCHA — Terminal Implementation
Artificial Intelligence — Individual Assignment

Usage:
    python main.py
"""

import sys
import time
from engine import terminal as T
from engine.records import SessionLog
from interrogation.detective import run_interrogation
from lockdown.gate import run_lockdown


def _banner() -> None:
    T.clr()
    T.line("═", col=T.A.B + T.A.MAG)
    print(T.c(T.A.B + T.A.MAG,  "  TURING TEST & CAPTCHA"))
    print(T.c(T.A.GRY,           "  Terminal Implementation"))
    print(T.c(T.A.GRY,           "  Artificial Intelligence — Individual Assignment"))
    T.line("═", col=T.A.B + T.A.MAG)
    print()


def _show_summary(log: SessionLog) -> None:
    T.clr()
    s = log.summary()
    T.line("═", col=T.A.B + T.A.CYN)
    print(T.c(T.A.B + T.A.CYN, "  SESSION SUMMARY"))
    T.line("═", col=T.A.B + T.A.CYN)
    print()

    # ── Interrogation ─────────────────────────────────────────────────────────
    print(T.c(T.A.B + T.A.RED, "  ── INTERROGATION ROOM (Turing Test) ──"))
    print(f"  Rounds played       :  {s['interrogations']}")
    print(f"  Detective accuracy  :  {s['detective_accuracy']:.0%}")
    print(f"  Machine escape rate :  {s['machine_escape_rate']:.0%}  "
          + T.c(T.A.GRY, "(rounds where machine fooled you)"))

    if log.interrogations:
        print()
        print(T.c(T.A.GRY, "  Round breakdown:"))
        for i, r in enumerate(log.interrogations, 1):
            res = T.c(T.A.GRN, "✔ correct") if r.correct else T.c(T.A.RED, "✘ wrong")
            broke = T.c(T.A.YLW, "  [contradiction caught]") if r.broke else ""
            print(f"    {i}.  Suspect: {r.suspect_was:<8}  "
                  f"Verdict: {r.verdict:<12}  {res}  "
                  f"({r.questions}Q){broke}")

    print()

    # ── Lockdown ──────────────────────────────────────────────────────────────
    print(T.c(T.A.B + T.A.BLU, "  ── LOCKDOWN (CAPTCHA) ──"))
    print(f"  Puzzles attempted   :  {s['lockdown_attempts']}")
    print(f"  Pass rate           :  {s['lockdown_pass_rate']:.0%}")

    if log.lockdowns:
        print()
        print(T.c(T.A.GRY, "  Puzzle breakdown:"))
        for i, r in enumerate(log.lockdowns, 1):
            res = T.c(T.A.GRN, "PASS") if r.passed else T.c(T.A.RED, "FAIL")
            bot = T.c(T.A.RED, "  [bot flag]") if r.flagged_bot else ""
            print(f"    {i}.  {r.puzzle_name:<22}  {res}  "
                  f"attempts: {r.attempts_used}{bot}")

    print()
    T.line("═", col=T.A.B + T.A.CYN)
    T.pause()


def main() -> None:
    log = SessionLog()

    while True:
        _banner()
        s = log.summary()

        # live stats if session has data
        if s["interrogations"] or s["lockdown_attempts"]:
            print(T.c(T.A.GRY,
                f"  Session ▸  "
                f"Interrogations: {s['interrogations']} "
                f"(accuracy {s['detective_accuracy']:.0%})  │  "
                f"Lockdown: {s['lockdown_attempts']} puzzles "
                f"({s['lockdown_pass_rate']:.0%} pass rate)"))
            print()

        print(T.c(T.A.B, "  MAIN MENU"))
        print()
        entries = [
            ("1", "Interrogation Room",   "Turing Test — you are the detective"),
            ("2", "Lockdown Puzzles",     "CAPTCHA — prove you are human"),
            ("3", "Session Summary",      ""),
            ("Q", "Quit",                 ""),
        ]
        for key, label, hint in entries:
            hint_str = T.c(T.A.GRY, f"  — {hint}") if hint else ""
            print(f"    {T.c(T.A.B + T.A.YLW, f'[{key}]')}  {label}{hint_str}")

        print()
        T.line(col=T.A.GRY)
        print()

        choice = T.ask("Select", col=T.A.B + T.A.WHT).upper()

        if choice == "1":
            run_interrogation(log)
        elif choice == "2":
            run_lockdown(log)
        elif choice == "3":
            _show_summary(log)
        elif choice in ("Q", "QUIT", "EXIT"):
            T.clr()
            _banner()
            T.status("info", "Session ended. Goodbye.")
            print()
            sys.exit(0)
        else:
            T.status("warn", "Invalid selection.")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
