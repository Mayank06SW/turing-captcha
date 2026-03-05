"""
engine/records.py
Stores all results for the current session.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class InterrogationRecord:
    suspect_was: str        # "Human" | "Machine"
    verdict:     str        # "Human" | "Machine" | "Inconclusive"
    correct:     bool
    questions:   int
    broke:       bool       # did the suspect contradict themselves?


@dataclass
class LockdownRecord:
    puzzle_name:   str
    passed:        bool
    attempts_used: int
    flagged_bot:   bool     # failed timing gate


class SessionLog:
    def __init__(self):
        self.interrogations: List[InterrogationRecord] = []
        self.lockdowns:      List[LockdownRecord]      = []

    # ── interrogation ─────────────────────────────────────────────────────────

    def log_interrogation(self, suspect_was, verdict, questions, broke):
        correct = (suspect_was == verdict)
        self.interrogations.append(
            InterrogationRecord(suspect_was, verdict, correct, questions, broke)
        )

    @property
    def interrogation_accuracy(self):
        if not self.interrogations: return 0.0
        return sum(r.correct for r in self.interrogations) / len(self.interrogations)

    @property
    def machine_escape_rate(self):
        """Fraction of Machine rounds where the detective was fooled."""
        ml = [r for r in self.interrogations if r.suspect_was == "Machine"]
        if not ml: return 0.0
        fooled = sum(1 for r in ml if r.verdict != "Machine")
        return fooled / len(ml)

    # ── lockdown ──────────────────────────────────────────────────────────────

    def log_lockdown(self, puzzle_name, passed, attempts_used, flagged_bot):
        self.lockdowns.append(
            LockdownRecord(puzzle_name, passed, attempts_used, flagged_bot)
        )

    @property
    def lockdown_pass_rate(self):
        if not self.lockdowns: return 0.0
        return sum(r.passed for r in self.lockdowns) / len(self.lockdowns)

    # ── full summary ──────────────────────────────────────────────────────────

    def summary(self):
        return {
            "interrogations"        : len(self.interrogations),
            "detective_accuracy"    : self.interrogation_accuracy,
            "machine_escape_rate"   : self.machine_escape_rate,
            "lockdown_attempts"     : len(self.lockdowns),
            "lockdown_pass_rate"    : self.lockdown_pass_rate,
        }
