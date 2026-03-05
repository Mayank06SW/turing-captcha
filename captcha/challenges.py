"""
challenges.py — Four CAPTCHA challenge types.

All inherit from BaseChallenge which enforces the interface:
    generate()  →  builds the puzzle, stores the answer internally
    render()    →  prints the challenge to the terminal
    verify(ans) →  returns True/False
"""

import random
import string
import time
from abc import ABC, abstractmethod
from core import display as D


# ── Base ──────────────────────────────────────────────────────────────────────

class BaseChallenge(ABC):
    name = "Challenge"
    _answer = None

    @abstractmethod
    def generate(self) -> None:
        """Build the puzzle and store the correct answer."""

    @abstractmethod
    def render(self) -> None:
        """Print the challenge to stdout."""

    def verify(self, user_answer: str) -> bool:
        """Case-insensitive / whitespace-stripped comparison."""
        return str(self._answer).strip().lower() == user_answer.strip().lower()


# ── 1. Text Recognition ───────────────────────────────────────────────────────

_NOISE_CHARS = list("!@#$%^&*-+=~|<>?/")

class TextChallenge(BaseChallenge):
    """
    Display a short word surrounded by noise characters.
    The user must identify the hidden word.
    """
    name = "Text Recognition"

    _WORDS = [
        "cloud", "table", "flame", "storm", "piano", "brush", "grape",
        "clock", "stone", "laser", "ocean", "prism", "radar", "tiger",
        "vinyl", "frost", "logic", "pixel", "solar", "lunar",
    ]

    def generate(self) -> None:
        self._answer = random.choice(self._WORDS)

    def _noisify(self, word: str) -> str:
        """Surround each letter with noise to simulate distortion."""
        parts = []
        for ch in word:
            n1 = random.choice(_NOISE_CHARS)
            n2 = random.choice(_NOISE_CHARS)
            # randomly alter letter case to add visual noise
            ch_display = ch.upper() if random.random() < 0.4 else ch
            parts.append(f"{n1}{ch_display}{n2}")
        return "  ".join(parts)

    def render(self) -> None:
        D.rule("·")
        print(D._c(D.C.BOLD + D.C.CYAN,
                   f"  CHALLENGE: {self.name}"))
        D.rule("·")
        print()
        D.info("Decode the hidden word from the noisy text below:")
        print()
        noisy = self._noisify(self._answer)
        padding = " " * 4
        print(D._c(D.C.BOLD + D.C.YELLOW, f"{padding}[ {noisy} ]"))
        print()
        D.info("Ignore all symbols — type only the letters you see.")
        print()


# ── 2. Math Challenge ─────────────────────────────────────────────────────────

class MathChallenge(BaseChallenge):
    """
    A two-step arithmetic challenge rendered in a stylised block.
    """
    name = "Math Challenge"

    _OPS = [
        ("+",  lambda a, b: a + b),
        ("-",  lambda a, b: a - b),
        ("×",  lambda a, b: a * b),
    ]

    def generate(self) -> None:
        op_sym, op_fn = random.choice(self._OPS)
        if op_sym == "×":
            a, b = random.randint(2, 9), random.randint(2, 9)
        else:
            a, b = random.randint(10, 50), random.randint(1, 30)
        self._a, self._b, self._op_sym = a, b, op_sym
        self._answer = op_fn(a, b)

    def render(self) -> None:
        D.rule("·")
        print(D._c(D.C.BOLD + D.C.CYAN,
                   f"  CHALLENGE: {self.name}"))
        D.rule("·")
        print()
        D.info("Solve the arithmetic expression:")
        print()
        expr = f"  {self._a}  {self._op_sym}  {self._b}  =  ?"
        print(D._c(D.C.BOLD + D.C.YELLOW,
                   f"    ┌{'─'*30}┐"))
        print(D._c(D.C.BOLD + D.C.YELLOW,
                   f"    │  {expr:<28}│"))
        print(D._c(D.C.BOLD + D.C.YELLOW,
                   f"    └{'─'*30}┘"))
        print()


# ── 3. Word Unscramble ────────────────────────────────────────────────────────

class WordChallenge(BaseChallenge):
    """
    Present a scrambled word; user must unscramble it.
    """
    name = "Word Unscramble"

    _WORDS = [
        "python", "matrix", "binary", "cipher", "neural", "quantum",
        "vector", "signal", "filter", "socket", "thread", "module",
        "syntax", "kernel", "buffer", "daemon", "cursor", "lambda",
    ]

    def _scramble(self, word: str) -> str:
        letters = list(word)
        # ensure the scramble is actually different
        scrambled = letters[:]
        attempts = 0
        while "".join(scrambled) == word and attempts < 20:
            random.shuffle(scrambled)
            attempts += 1
        return "".join(scrambled)

    def generate(self) -> None:
        self._answer = random.choice(self._WORDS)
        self._scrambled = self._scramble(self._answer)

    def render(self) -> None:
        D.rule("·")
        print(D._c(D.C.BOLD + D.C.CYAN,
                   f"  CHALLENGE: {self.name}"))
        D.rule("·")
        print()
        D.info("Unscramble the letters to form a valid English word:")
        print()
        spaced = "  ".join(self._scrambled.upper())
        print(D._c(D.C.BOLD + D.C.YELLOW,
                   f"    →  {spaced}"))
        print()
        D.info(f"Hint: it has {len(self._answer)} letters.")
        print()


# ── 4. Pattern Sequence ───────────────────────────────────────────────────────

class SequenceChallenge(BaseChallenge):
    """
    Show a numeric or symbol sequence with the last element missing.
    The user must identify the next value.
    """
    name = "Pattern Sequence"

    def _arithmetic(self):
        start = random.randint(1, 20)
        step  = random.randint(2, 10)
        seq   = [start + step * i for i in range(5)]
        self._answer = str(seq[-1])
        return seq[:-1]

    def _geometric(self):
        start = random.randint(1, 5)
        ratio = random.randint(2, 4)
        seq   = [start * (ratio ** i) for i in range(5)]
        self._answer = str(seq[-1])
        return seq[:-1]

    def _fibonacci_like(self):
        a, b = random.randint(1, 5), random.randint(1, 5)
        seq  = [a, b]
        for _ in range(3):
            seq.append(seq[-1] + seq[-2])
        self._answer = str(seq[-1])
        return seq[:-1]

    def generate(self) -> None:
        gen = random.choice([self._arithmetic, self._geometric, self._fibonacci_like])
        self._sequence = gen()

    def render(self) -> None:
        D.rule("·")
        print(D._c(D.C.BOLD + D.C.CYAN,
                   f"  CHALLENGE: {self.name}"))
        D.rule("·")
        print()
        D.info("Find the next number in the sequence:")
        print()
        seq_str = "  →  ".join(str(n) for n in self._sequence)
        print(D._c(D.C.BOLD + D.C.YELLOW,
                   f"    {seq_str}  →  ?"))
        print()


# ── registry ──────────────────────────────────────────────────────────────────

CHALLENGES = [TextChallenge, MathChallenge, WordChallenge, SequenceChallenge]
