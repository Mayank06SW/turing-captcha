"""
gate.py — CAPTCHA game loop.

Lets the user choose individual challenge types or run all four in sequence.
Results are recorded in the session.
"""

import random
from core import display as D
from core.session import Session
from captcha.challenges import CHALLENGES
from captcha.verifier import run_verification


def _print_menu() -> None:
    D.rule()
    print(D._c(D.C.BOLD + D.C.CYAN,
               "  CAPTCHA CHALLENGES  —  Prove you are human"))
    D.rule()
    print()
    D.info("Select a challenge type, or run all four in sequence.")
    print()
    for i, cls in enumerate(CHALLENGES, 1):
        print(f"    {D._c(D.C.BOLD + D.C.YELLOW, str(i))}.  {cls.name}")
    print(f"    {D._c(D.C.BOLD + D.C.YELLOW, 'A')}.  All challenges (in order)")
    print(f"    {D._c(D.C.BOLD + D.C.YELLOW, 'R')}.  Random challenge")
    print(f"    {D._c(D.C.BOLD + D.C.YELLOW, 'Q')}.  Return to main menu")
    print()
    D.rule(colour=D.C.DIM)
    print()


def _run_one(challenge_cls, session: Session) -> None:
    D.clr()
    challenge = challenge_cls()
    result = run_verification(challenge)

    print()
    D.rule()
    D.label("Challenge  ", challenge.name)
    D.label("Result     ", "PASS" if result.passed else "FAIL")
    D.label("Attempts   ", str(result.attempts_used))
    D.label("Detail     ", result.message)
    D.rule()

    if result.passed:
        D.verdict_banner(True,  "Access granted — human confirmed.")
    elif result.timed_out:
        D.verdict_banner(False, "Bot detected — response too fast.")
    else:
        D.verdict_banner(False, "Access denied.")

    session.record_captcha(
        challenge.name,
        result.passed,
        result.attempts_used,
        result.timed_out,
    )
    input("\n  Press ENTER to continue…")


def run_captcha(session: Session) -> None:
    """Entry point called from main.py."""
    while True:
        D.clr()
        _print_menu()

        choice = D.prompt("Select", colour=D.C.BOLD + D.C.YELLOW).upper()

        if choice == "Q":
            return

        if choice == "A":
            for cls in CHALLENGES:
                _run_one(cls, session)
            return

        if choice == "R":
            _run_one(random.choice(CHALLENGES), session)
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(CHALLENGES):
            _run_one(CHALLENGES[int(choice) - 1], session)
            continue

        D.warn("Invalid selection — please try again.")
        input("  Press ENTER…")
