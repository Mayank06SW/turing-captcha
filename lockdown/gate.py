"""
lockdown/gate.py

CAPTCHA Lockdown — Logic Puzzle Gate.

The system is the judge. The player must solve logic puzzles to prove
they are human. A timing gate flags suspiciously fast answers as bots.
Three wrong answers trigger lockout.
"""

import time
import random
from engine import terminal as T
from engine.records import SessionLog
from lockdown.puzzles import PUZZLES, BasePuzzle

BOT_SPEED_THRESHOLD = 2.0   # seconds — faster than this is bot-suspicious
MAX_ATTEMPTS        = 3


def _run_puzzle(puzzle: BasePuzzle, log: SessionLog) -> bool:
    """
    Run one puzzle through the timing gate with retry logic.
    Returns True if the player passed.
    """
    puzzle.build()

    T.clr()
    puzzle.display()

    hint_shown = False

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            T.status("warn", f"Attempt {attempt} of {MAX_ATTEMPTS}")
            if not hint_shown:
                show = T.ask("Show hint? (Y/N)", col=T.A.GRY).upper()
                if show == "Y":
                    T.status("info", f"Hint: {puzzle.hint}")
                    hint_shown = True
            print()

        t_start = time.perf_counter()
        raw = T.ask("Your answer", col=T.A.B + T.A.GRN)
        elapsed = time.perf_counter() - t_start

        if raw.lower() == "q":
            log.log_lockdown(puzzle.name, False, attempt, False)
            T.status("warn", "Puzzle abandoned.")
            return False

        # ── timing gate ───────────────────────────────────────────────────────
        if elapsed < BOT_SPEED_THRESHOLD:
            T.status("fail",
                f"Answer received in {elapsed:.2f}s — below the "
                f"{BOT_SPEED_THRESHOLD}s human threshold. Bot suspected.")
            print()
            T.verdict_screen(False,
                "ACCESS DENIED — Response too fast.",
                f"Minimum human response time: {BOT_SPEED_THRESHOLD}s")
            log.log_lockdown(puzzle.name, False, attempt, flagged_bot=True)
            T.pause()
            return False

        # ── correctness ───────────────────────────────────────────────────────
        if puzzle.check(raw):
            T.status("ok", f"Correct!  ({elapsed:.1f}s)")
            T.verdict_screen(True,
                "ACCESS GRANTED — Human verified.",
                f"Puzzle: {puzzle.name}  |  Attempts: {attempt}")
            log.log_lockdown(puzzle.name, True, attempt, flagged_bot=False)
            T.pause()
            return True
        else:
            T.status("fail", f"Wrong answer.  ({elapsed:.1f}s)")
            remaining = MAX_ATTEMPTS - attempt
            if remaining:
                T.status("info", f"{remaining} attempt(s) remaining.")

    # ── lockout ───────────────────────────────────────────────────────────────
    T.verdict_screen(False,
        "LOCKOUT — Too many wrong answers.",
        f"Correct answer was: {puzzle._answer}")
    log.log_lockdown(puzzle.name, False, MAX_ATTEMPTS, flagged_bot=False)
    T.pause()
    return False


def _menu(log: SessionLog) -> None:
    while True:
        T.clr()
        T.line("═", col=T.A.B + T.A.BLU)
        print(T.c(T.A.B + T.A.BLU, "  LOCKDOWN — Logic Puzzle CAPTCHA"))
        print(T.c(T.A.GRY,         "  Prove you are human. Solve the puzzle."))
        T.line("═", col=T.A.B + T.A.BLU)
        print()
        T.status("info",
            f"Timing gate: answers under {BOT_SPEED_THRESHOLD}s are flagged as bot.")
        T.status("info", "Max 3 attempts per puzzle before lockout.")
        print()

        for i, cls in enumerate(PUZZLES, 1):
            print(f"    {T.c(T.A.B + T.A.YLW, str(i))}.  {cls.name}")
        print(f"    {T.c(T.A.B + T.A.YLW, 'A')}.  All puzzles in sequence")
        print(f"    {T.c(T.A.B + T.A.YLW, 'R')}.  Random puzzle")
        print(f"    {T.c(T.A.B + T.A.YLW, 'Q')}.  Return to main menu")
        print()
        T.line(col=T.A.GRY)
        print()

        choice = T.ask("Select", col=T.A.B + T.A.YLW).upper()

        if choice == "Q":
            return

        if choice == "A":
            for cls in PUZZLES:
                _run_puzzle(cls(), log)
            return

        if choice == "R":
            _run_puzzle(random.choice(PUZZLES)(), log)
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(PUZZLES):
            _run_puzzle(PUZZLES[int(choice) - 1](), log)
            continue

        T.status("warn", "Invalid selection.")
        time.sleep(0.8)


def run_lockdown(log: SessionLog) -> None:
    """Entry point called from main.py."""
    _menu(log)
