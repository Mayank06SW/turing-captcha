"""
verifier.py — Timing-aware CAPTCHA verifier.

Rules:
  • Response time < BOT_THRESHOLD  → flagged as bot (even if correct)
  • Wrong answer                   → attempt consumed
  • MAX_ATTEMPTS wrong answers     → lockout
"""

import time
from dataclasses import dataclass
from captcha.challenges import BaseChallenge
from core import display as D

BOT_THRESHOLD   = 1.5   # seconds — faster than this is suspicious
MAX_ATTEMPTS    = 3


@dataclass
class VerifyResult:
    passed:       bool
    timed_out:    bool   # True if answer arrived suspiciously fast
    attempts_used: int
    message:      str


def run_verification(challenge: BaseChallenge) -> VerifyResult:
    """
    Present the challenge, collect answers with retry logic,
    enforce timing check, and return a VerifyResult.
    """
    challenge.generate()
    challenge.render()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            D.warn(f"Attempt {attempt} of {MAX_ATTEMPTS}")

        start = time.perf_counter()
        raw = D.prompt("Your answer", colour=D.C.BOLD + D.C.GREEN)
        elapsed = time.perf_counter() - start

        if raw.lower() == "q":
            return VerifyResult(False, False, attempt, "Challenge abandoned.")

        # ── timing check ──────────────────────────────────────────────────
        if elapsed < BOT_THRESHOLD:
            D.error(
                f"Response in {elapsed:.2f}s — below the {BOT_THRESHOLD}s"
                f" human threshold.  Bot behaviour detected."
            )
            return VerifyResult(
                passed=False,
                timed_out=True,
                attempts_used=attempt,
                message=f"Too fast ({elapsed:.2f}s). Bot suspected.",
            )

        # ── correctness check ─────────────────────────────────────────────
        if challenge.verify(raw):
            D.success(f"Correct!  ({elapsed:.1f}s)")
            return VerifyResult(
                passed=True,
                timed_out=False,
                attempts_used=attempt,
                message="Human verified.",
            )
        else:
            D.error(f"Incorrect. ({elapsed:.1f}s)")
            if attempt < MAX_ATTEMPTS:
                D.info(f"{MAX_ATTEMPTS - attempt} attempt(s) remaining.")

    # ── lockout ───────────────────────────────────────────────────────────
    D.error("Maximum attempts reached.  Access denied.")
    return VerifyResult(
        passed=False,
        timed_out=False,
        attempts_used=MAX_ATTEMPTS,
        message="Lockout after too many wrong answers.",
    )
