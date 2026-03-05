"""
session.py — Tracks results across Turing Test and CAPTCHA sessions.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class TuringRound:
    entity: str          # "Human" or "AI"
    verdict: str         # "H", "A", "U"
    exchanges: int
    correct: bool        # Judge was right


@dataclass
class CaptchaAttempt:
    challenge_type: str
    passed: bool
    attempts_used: int
    timed_out: bool


class Session:
    """Holds the complete state for one program run."""

    def __init__(self):
        self.turing_rounds: List[TuringRound] = []
        self.captcha_attempts: List[CaptchaAttempt] = []

    # ── Turing helpers ────────────────────────────────────────────────────────

    def record_turing(self, entity: str, verdict: str, exchanges: int) -> None:
        correct = (
            (verdict == "H" and entity == "Human") or
            (verdict == "A" and entity == "AI")
        )
        self.turing_rounds.append(
            TuringRound(entity, verdict, exchanges, correct)
        )

    @property
    def turing_accuracy(self) -> float:
        if not self.turing_rounds:
            return 0.0
        return sum(r.correct for r in self.turing_rounds) / len(self.turing_rounds)

    @property
    def ai_pass_rate(self) -> float:
        """Fraction of AI rounds where the judge was fooled (H or U verdict)."""
        ai_rounds = [r for r in self.turing_rounds if r.entity == "AI"]
        if not ai_rounds:
            return 0.0
        fooled = sum(1 for r in ai_rounds if r.verdict in ("H", "U"))
        return fooled / len(ai_rounds)

    # ── CAPTCHA helpers ───────────────────────────────────────────────────────

    def record_captcha(self, challenge_type: str, passed: bool,
                       attempts_used: int, timed_out: bool) -> None:
        self.captcha_attempts.append(
            CaptchaAttempt(challenge_type, passed, attempts_used, timed_out)
        )

    @property
    def captcha_pass_rate(self) -> float:
        if not self.captcha_attempts:
            return 0.0
        return sum(a.passed for a in self.captcha_attempts) / len(self.captcha_attempts)

    # ── Summary ───────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        return {
            "turing_rounds"     : len(self.turing_rounds),
            "turing_accuracy"   : self.turing_accuracy,
            "ai_pass_rate"      : self.ai_pass_rate,
            "captcha_attempts"  : len(self.captcha_attempts),
            "captcha_pass_rate" : self.captcha_pass_rate,
        }
