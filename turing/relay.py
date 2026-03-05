"""
relay.py — Anonymizer that hides which responder is active.

The relay randomly picks one responder at the start of a round and routes
all questions through it.  The judge never sees the identity — only the
response text and a simulated typing delay.
"""

import random
import time
from typing import List, Tuple

from turing.responders import BaseResponder, HumanResponder, AIResponder
from core.display import C, slow_print, _c


class Relay:
    """
    Routes judge questions to one hidden responder.

    Parameters
    ----------
    human : HumanResponder
    ai    : AIResponder
    """

    def __init__(self, human: HumanResponder, ai: AIResponder):
        self._human = human
        self._ai = ai
        self._active: BaseResponder = None
        self._history: List[Tuple[str, str]] = []

    def new_round(self) -> None:
        """Randomly assign a responder for this round; reset history."""
        self._active = random.choice([self._human, self._ai])
        self._history = []

    @property
    def active_name(self) -> str:
        """The true identity — revealed only after the verdict."""
        return self._active.name

    def ask(self, question: str) -> str:
        """
        Send a question through the relay.
        Simulates typing delay before displaying the response.
        Returns the response text.
        """
        response, delay = self._active.respond(question, self._history)
        self._history.append((question, response))

        # show typing indicator
        print(f"\n  {_c(C.DIM, 'Entity is typing')} ", end="", flush=True)
        steps = max(3, int(delay * 4))
        step_dur = delay / steps
        for _ in range(steps):
            print(_c(C.DIM, "."), end="", flush=True)
            time.sleep(step_dur)
        print()

        return response

    @property
    def exchange_count(self) -> int:
        return len(self._history)
