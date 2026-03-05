"""
judge.py — Turing Test game loop.

The judge (user) asks questions to an anonymous entity.
After at least MIN_EXCHANGES, the judge submits a verdict.
Results are recorded in the session.
"""

import time
from core import display as D
from core.session import Session
from turing.relay import Relay
from turing.responders import HumanResponder, AIResponder

MIN_EXCHANGES = 3
MAX_EXCHANGES = 10


def _print_instructions() -> None:
    D.rule()
    print(D._c(D.C.BOLD + D.C.CYAN,
               "  TURING TEST SIMULATOR  —  You are the Judge"))
    D.rule()
    print()
    D.info("You will converse with an anonymous entity.")
    D.info("It is either a HUMAN or an AI — you cannot tell which.")
    D.info(f"Ask at least {MIN_EXCHANGES} questions, then submit your verdict.")
    print()
    D.label("Commands", "type your question freely")
    D.label("Verdict  ", "after 3+ exchanges, enter  H (Human)  A (AI)  U (Unsure)")
    D.label("Exit     ", "enter  Q  to return to the main menu")
    print()
    D.rule(colour=D.C.DIM)
    print()


def _verdict_map(v: str) -> str:
    return {"H": "Human", "A": "AI", "U": "Unsure"}.get(v.upper(), "Unknown")


def run_turing(session: Session) -> None:
    """Entry point called from main.py."""
    D.clr()
    _print_instructions()

    relay = Relay(HumanResponder(), AIResponder())
    relay.new_round()

    verdict = None

    while True:
        raw = D.prompt("You → ", colour=D.C.BOLD + D.C.YELLOW)
        if not raw:
            continue

        upper = raw.upper()

        # ── exit ──────────────────────────────────────────────────────────────
        if upper == "Q":
            D.warn("Round abandoned — no verdict recorded.")
            input("\n  Press ENTER to continue…")
            return

        # ── verdict submission ────────────────────────────────────────────────
        if upper in ("H", "A", "U"):
            if relay.exchange_count < MIN_EXCHANGES:
                D.warn(
                    f"You need at least {MIN_EXCHANGES} exchanges before submitting"
                    f" a verdict. ({relay.exchange_count} so far)"
                )
                continue
            verdict = upper
            break

        # ── max exchanges guard ───────────────────────────────────────────────
        if relay.exchange_count >= MAX_EXCHANGES:
            D.warn("Maximum exchanges reached. Enter H, A, or U to submit your verdict.")
            continue

        # ── normal question ───────────────────────────────────────────────────
        response = relay.ask(raw)
        print()
        D.slow_print(f"Entity → {response}", colour=D.C.WHITE, delay=0.02)
        print()
        D.info(
            f"Exchanges: {relay.exchange_count}  |  "
            f"Verdict available after {MIN_EXCHANGES}"
        )

    # ── reveal and score ──────────────────────────────────────────────────────
    true_entity = relay.active_name
    correct = (
        (verdict == "H" and true_entity == "Human") or
        (verdict == "A" and true_entity == "AI")
    )

    session.record_turing(true_entity, verdict, relay.exchange_count)

    print()
    D.rule()
    D.label("Your verdict  ", _verdict_map(verdict), D.C.BOLD)
    D.label("True identity ", true_entity,            D.C.BOLD)
    D.label("Exchanges     ", str(relay.exchange_count))
    D.rule()

    if correct:
        D.verdict_banner(True,  "You identified correctly!")
    else:
        if true_entity == "AI" and verdict in ("H", "U"):
            D.verdict_banner(False, "The AI fooled you — it passed the Turing Test.")
        else:
            D.verdict_banner(False, "Incorrect identification.")

    # AI pass/fail note
    if true_entity == "AI":
        if verdict in ("H", "U"):
            print(D._c(D.C.MAGENTA,
                       "\n  ★  The AI passed the Turing Test for this round."))
        else:
            print(D._c(D.C.CYAN,
                       "\n  ◆  The AI did not fool you — it failed the Turing Test."))

    input("\n  Press ENTER to continue…")
