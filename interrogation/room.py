"""
interrogation/room.py

The Interrogation Room.

The detective (player) sits across from an unknown suspect.
The room controller:
  • routes each question to the hidden suspect
  • simulates typing delay with an animated indicator
  • watches for contradictions and flags them to the detective
  • enforces the round structure (min questions, verdict)
"""

import random
import time
from typing import List, Tuple

from interrogation.suspects import BaseSuspect, HumanSuspect, MachineSuspect
from engine import terminal as T


MIN_QUESTIONS = 4
MAX_QUESTIONS = 12

# Phrases the detective can call out to try to catch a contradiction
PRESSURE_PHRASES = [
    "but earlier you said",
    "you just contradicted yourself",
    "that doesn't match what you told me",
    "you said something different before",
    "wait, earlier you mentioned",
]


class InterrogationRoom:
    """
    Manages one interrogation session.
    Randomly seats either a HumanSuspect or MachineSuspect.
    The detective never knows which — only sees the responses.
    """

    def __init__(self):
        self._suspect: BaseSuspect = random.choice([HumanSuspect(), MachineSuspect()])
        self._history: List[Tuple[str, str]] = []   # (question, answer)
        self._contradictions_caught = 0

    @property
    def true_identity(self) -> str:
        return self._suspect.true_identity

    @property
    def question_count(self) -> int:
        return len(self._history)

    @property
    def broke(self) -> bool:
        """Did the detective catch at least one contradiction?"""
        return self._contradictions_caught > 0

    def _animate_thinking(self, delay: float) -> None:
        steps = max(4, int(delay * 3))
        step_dur = delay / steps
        T_chars = ["   ", ".  ", ".. ", "..."]
        print(f"\n  {T.c(T.A.GRY, 'Suspect thinking')}", end="", flush=True)
        for i in range(steps):
            print(f"\r  {T.c(T.A.GRY, 'Suspect thinking' + T_chars[i % 4])}",
                  end="", flush=True)
            time.sleep(step_dur)
        print(f"\r  {T.c(T.A.GRY, '                   ')}\r", end="")

    def _check_contradiction(self, question: str) -> bool:
        """
        If the detective's question contains a pressure phrase,
        check whether the suspect actually gave a conflicting answer
        earlier.  Returns True if a genuine contradiction was found.
        """
        q_lower = question.lower()
        if not any(p in q_lower for p in PRESSURE_PHRASES):
            return False
        # For simulation: a Machine is never caught (consistent),
        # a Human has a small chance of being caught in a contradiction.
        if self._suspect.true_identity == "Human":
            caught = random.random() < 0.45
        else:
            caught = False   # Machine never contradicts — pressure fails
        if caught:
            self._contradictions_caught += 1
        return caught

    def question(self, q: str) -> str:
        """Send a question; return the response text."""
        contradiction = self._check_contradiction(q)

        response, delay = self._suspect.respond(q, self._history)
        self._animate_thinking(delay)
        self._history.append((q, response))

        if contradiction:
            print(T.c(T.A.B + T.A.YLW,
                "\n  ⚡  CONTRADICTION DETECTED — the suspect stumbled!"))

        return response
