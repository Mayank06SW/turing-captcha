"""
lockdown/puzzles.py

Six logic-puzzle CAPTCHA types. All inherit BasePuzzle.

Interface:
    build()          — generate the puzzle, store answer internally
    display()        — render to terminal
    check(ans)       — return True/False
    hint (property)  — one-line hint string

Puzzles:
    1. SyllogismPuzzle   — deductive logic (All A are B…)
    2. TruthLiarPuzzle   — knights and knaves
    3. GridPathPuzzle    — navigate a grid with constraints
    4. SetMemberPuzzle   — which item belongs / doesn't belong
    5. ScalePuzzle       — balance-scale weight reasoning
    6. CipherPuzzle      — simple Caesar / reverse cipher
"""

import random
import string
from abc import ABC, abstractmethod


# ── Base ──────────────────────────────────────────────────────────────────────

class BasePuzzle(ABC):
    name  = "Puzzle"
    _answer = None

    @abstractmethod
    def build(self) -> None: ...

    @abstractmethod
    def display(self) -> None: ...

    @property
    @abstractmethod
    def hint(self) -> str: ...

    def check(self, user_answer: str) -> bool:
        return str(self._answer).strip().lower() == user_answer.strip().lower()


# ── 1. Syllogism ──────────────────────────────────────────────────────────────

_SYLLOGISMS = [
    # (premise1, premise2, question, answer, explanation)
    ("All birds have wings.",
     "Penguins are birds.",
     "Do penguins have wings?",
     "yes",
     "Penguins are birds → birds have wings → penguins have wings."),

    ("No reptiles are warm-blooded.",
     "All snakes are reptiles.",
     "Are snakes warm-blooded?",
     "no",
     "Snakes are reptiles → reptiles are not warm-blooded → snakes are not."),

    ("All students passed the exam.",
     "Maria is a student.",
     "Did Maria pass the exam?",
     "yes",
     "Maria is a student → all students passed → Maria passed."),

    ("Some fruits are sweet.",
     "Lemons are fruits.",
     "Are lemons definitely sweet?",
     "no",
     "Only *some* fruits are sweet — lemons might not be one of them."),

    ("All mammals breathe air.",
     "Whales are mammals.",
     "Do whales breathe air?",
     "yes",
     "Whales are mammals → mammals breathe air → whales breathe air."),

    ("No fish can walk.",
     "A trout is a fish.",
     "Can a trout walk?",
     "no",
     "No fish can walk → trout is a fish → trout cannot walk."),
]


class SyllogismPuzzle(BasePuzzle):
    name = "Syllogism"

    def build(self):
        self._s = random.choice(_SYLLOGISMS)
        self._answer = self._s[3]

    def display(self):
        from engine.terminal import c, A, line, boxed
        line("·")
        print(c(A.B + A.CYN, f"  LOCKDOWN PUZZLE — {self.name}"))
        line("·")
        print()
        boxed([
            "PREMISE 1 :  " + self._s[0],
            "PREMISE 2 :  " + self._s[1],
            "",
            "QUESTION  :  " + self._s[2],
            "",
            "Answer YES or NO.",
        ])
        print()

    @property
    def hint(self):
        return f"Logic: {self._s[4]}"


# ── 2. Truth / Liar ───────────────────────────────────────────────────────────

_TL_SCENARIOS = [
    # (setup, question, answer, explanation)
    ("Alex always tells the truth. Jordan always lies.\n"
     "  Alex says: 'Jordan is a liar.'",
     "Is Alex telling the truth?",
     "yes",
     "Alex tells the truth; Jordan is indeed a liar — so yes."),

    ("There are two guards. One always lies, one always tells the truth.\n"
     "  You ask one: 'Are you the truth-teller?' They say: 'Yes.'",
     "Can you determine who you asked?",
     "no",
     "Both would say yes — the truth-teller honestly and the liar falsely."),

    ("Alex always tells the truth.\n"
     "  Alex says: 'It is raining.'",
     "Is it raining?",
     "yes",
     "Alex tells the truth → it is raining."),

    ("Jordan always lies.\n"
     "  Jordan says: 'I am not a liar.'",
     "Is Jordan a liar?",
     "yes",
     "Jordan lies → 'I am not a liar' is false → Jordan is a liar."),

    ("Alex always tells the truth. Jordan always lies.\n"
     "  Jordan says: 'Alex is a liar.'",
     "Is Alex a liar?",
     "no",
     "Jordan lies → 'Alex is a liar' is false → Alex is not a liar."),
]


class TruthLiarPuzzle(BasePuzzle):
    name = "Truth & Liar"

    def build(self):
        self._sc = random.choice(_TL_SCENARIOS)
        self._answer = self._sc[2]

    def display(self):
        from engine.terminal import c, A, line, boxed
        line("·")
        print(c(A.B + A.CYN, f"  LOCKDOWN PUZZLE — {self.name}"))
        line("·")
        print()
        boxed([
            "SCENARIO:",
            "",
            *[f"  {l}" for l in self._sc[0].split("\n")],
            "",
            "QUESTION :  " + self._sc[1],
            "",
            "Answer YES or NO.",
        ])
        print()

    @property
    def hint(self):
        return self._sc[3]


# ── 3. Set Member — odd one out ───────────────────────────────────────────────

_SETS = [
    (["eagle", "sparrow", "penguin", "falcon"], "penguin",
     "All others can fly."),
    (["rose", "tulip", "oak", "daisy"], "oak",
     "All others are flowers; oak is a tree."),
    (["mercury", "venus", "moon", "mars"], "moon",
     "All others are planets; moon is a natural satellite."),
    (["python", "java", "cobra", "ruby"], "cobra",
     "All others are programming languages; cobra is a snake."),
    (["paris", "berlin", "london", "seine"], "seine",
     "All others are capital cities; seine is a river."),
    (["square", "circle", "triangle", "sphere"], "sphere",
     "All others are 2D shapes; sphere is 3D."),
    (["2", "4", "7", "8"], "7",
     "All others are even numbers; 7 is odd."),
    (["km", "litre", "metre", "mile"], "litre",
     "All others measure distance; litre measures volume."),
]


class SetMemberPuzzle(BasePuzzle):
    name = "Odd One Out"

    def build(self):
        self._set_data = random.choice(_SETS)
        self._answer = self._set_data[1]

    def display(self):
        from engine.terminal import c, A, line, boxed
        line("·")
        print(c(A.B + A.CYN, f"  LOCKDOWN PUZZLE — {self.name}"))
        line("·")
        print()
        items = self._set_data[0][:]
        random.shuffle(items)
        boxed([
            "Which item does NOT belong with the others?",
            "",
            "  →  " + "   |   ".join(items),
            "",
            "Type the word exactly.",
        ])
        print()

    @property
    def hint(self):
        return self._set_data[2]


# ── 4. Scale / Weight Puzzle ──────────────────────────────────────────────────

_SCALES = [
    ("A weighs more than B.  B weighs more than C.",
     "Which is heaviest?", "A",
     "A > B > C so A is heaviest."),

    ("X = Y + 2.  Y = 3.",
     "What is X?", "5",
     "Y=3, X=Y+2=5."),

    ("Three boxes: Red, Blue, Green.\n"
     "  Red is heavier than Blue.\n"
     "  Green is lighter than Blue.",
     "Order from heaviest to lightest (e.g. R B G):", "R B G",
     "Red > Blue > Green."),

    ("Bag A has 4 apples. Bag B has twice as many as A.\n"
     "  Bag C has 3 fewer than B.",
     "How many apples in bag C?", "5",
     "A=4, B=8, C=8-3=5."),

    ("A candle burns 1 cm every 2 hours.\n"
     "  It starts at 10 cm tall.",
     "How tall after 6 hours? (in cm)", "7",
     "6 hours = 3 cm burned. 10 - 3 = 7 cm."),
]


class ScalePuzzle(BasePuzzle):
    name = "Weight & Logic"

    def build(self):
        self._sc = random.choice(_SCALES)
        self._answer = self._sc[2].lower().replace(" ", "")

    def check(self, user_answer: str) -> bool:
        return user_answer.strip().lower().replace(" ", "") == self._answer

    def display(self):
        from engine.terminal import c, A, line, boxed
        line("·")
        print(c(A.B + A.CYN, f"  LOCKDOWN PUZZLE — {self.name}"))
        line("·")
        print()
        lines = [l for l in self._sc[0].split("\n")]
        boxed([
            *lines,
            "",
            "QUESTION:  " + self._sc[1],
        ])
        print()

    @property
    def hint(self):
        return self._sc[3]


# ── 5. Cipher ─────────────────────────────────────────────────────────────────

_WORDS = ["signal", "bridge", "tunnel", "mirror", "planet",
          "socket", "filter", "cipher", "window", "vector"]


class CipherPuzzle(BasePuzzle):
    name = "Cipher Decode"

    def _caesar(self, text: str, shift: int) -> str:
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('a') if ch.islower() else ord('A')
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)

    def build(self):
        self._word  = random.choice(_WORDS)
        self._shift = random.randint(1, 5)
        self._encoded = self._caesar(self._word, self._shift)
        self._answer  = self._word

    def display(self):
        from engine.terminal import c, A, line, boxed
        line("·")
        print(c(A.B + A.CYN, f"  LOCKDOWN PUZZLE — {self.name}"))
        line("·")
        print()
        boxed([
            f"Each letter has been shifted forward by {self._shift} position(s)",
            f"in the alphabet (Caesar cipher).",
            "",
            f"  Encoded :  {self._encoded.upper()}",
            "",
            "Decode and type the original word (lowercase).",
        ])
        print()

    @property
    def hint(self):
        return f"Shift each letter back by {self._shift} in the alphabet."


# ── 6. Grid Path ──────────────────────────────────────────────────────────────

class GridPathPuzzle(BasePuzzle):
    """
    A 3×3 grid. Some cells are blocked (#). The player must say
    how many unblocked cells there are, or answer a simple path question.
    """
    name = "Grid Reasoning"

    _GRIDS = [
        # (grid_rows, question, answer, hint)
        (["[ ][ ][#]",
          "[ ][#][ ]",
          "[ ][ ][ ]"],
         "How many unblocked cells ( [ ] ) are in the grid?",
         "7",
         "Count all [ ] cells: top row 2, middle 2, bottom 3 = 7."),

        (["[#][ ][ ]",
          "[ ][#][ ]",
          "[ ][ ][#]"],
         "How many blocked cells ( [#] ) are in the grid?",
         "3",
         "One blocked cell per row, 3 rows = 3."),

        (["[ ][ ][ ]",
          "[#][#][ ]",
          "[ ][ ][ ]"],
         "Which row has the most blocked cells? (top / middle / bottom)",
         "middle",
         "Middle row has 2 blocked cells; others have none."),

        (["[ ][#][ ]",
          "[ ][ ][ ]",
          "[#][ ][ ]"],
         "How many unblocked cells ( [ ] ) are in the grid?",
         "7",
         "Grid has 9 cells, 2 blocked → 7 unblocked."),
    ]

    def build(self):
        self._gd = random.choice(self._GRIDS)
        self._answer = self._gd[2].lower()

    def display(self):
        from engine.terminal import c, A, line, boxed
        line("·")
        print(c(A.B + A.CYN, f"  LOCKDOWN PUZZLE — {self.name}"))
        line("·")
        print()
        grid_lines = ["  " + row for row in self._gd[0]]
        boxed([
            "Legend:  [ ] = open cell    [#] = blocked cell",
            "",
            *grid_lines,
            "",
            "QUESTION:  " + self._gd[1],
        ])
        print()

    @property
    def hint(self):
        return self._gd[3]


# ── Registry ──────────────────────────────────────────────────────────────────

PUZZLES = [
    SyllogismPuzzle,
    TruthLiarPuzzle,
    SetMemberPuzzle,
    ScalePuzzle,
    CipherPuzzle,
    GridPathPuzzle,
]
