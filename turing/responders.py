"""
responders.py — HumanResponder and AIResponder.

Each responder receives the conversation history and the judge's latest
question, then returns a (response_text, delay_seconds) tuple.
The relay uses the delay to simulate realistic typing time.
"""

import random
import time
from typing import List, Tuple


# ── Base class ────────────────────────────────────────────────────────────────

class BaseResponder:
    name = "Entity"

    def respond(self, question: str, history: List[Tuple[str, str]]) -> Tuple[str, float]:
        """Return (response_text, simulated_typing_delay_in_seconds)."""
        raise NotImplementedError


# ── Human-like responder ──────────────────────────────────────────────────────

_HUMAN_INTROS = [
    "hmm, ", "well, ", "i mean, ", "okay so ", "tbh ", "honestly ", "",
    "lol ", "idk, ", "like, ",
]

_HUMAN_FILLERS = [
    " you know?", " i guess.", " lol.", ".", " idk.", " haha.", "!",
    " kinda?", " ig.", " ngl.",
]

_HUMAN_REPLIES = {
    # keyed by keyword → list of possible snippets
    "favourite": [
        "probably pizza or ramen, hard to choose lol",
        "coffee honestly, i can't function without it",
        "sleep. not even joking.",
    ],
    "hobby": [
        "i play guitar but i'm still kinda bad at it",
        "i read a lot, mostly fantasy stuff",
        "gaming, drawing, and watching too much youtube",
    ],
    "feel": [
        "tired today tbh, didn't sleep well",
        "pretty good! had a solid breakfast for once",
        "okay i guess, just vibing",
    ],
    "think": [
        "i mean, it depends on the day right?",
        "hard question, not sure i have a clear answer",
        "probably a mix of both honestly",
    ],
    "name": [
        "just call me alex",
        "i usually go by sam",
        "people call me morgan",
    ],
    "age": [
        "22, why do you ask lol",
        "old enough i suppose haha",
        "somewhere between student and broke adult",
    ],
    "default": [
        "that's a really interesting question actually",
        "hmm yeah i've thought about that before",
        "not sure i have a great answer for that one",
        "could be! i'm open to it",
        "honestly depends on the context i think",
        "i feel like everyone has a different take on this",
        "lol yeah that's kinda how it is",
        "i get what you mean",
    ],
}


def _human_lookup(question: str) -> str:
    q = question.lower()
    for key, replies in _HUMAN_REPLIES.items():
        if key in q:
            return random.choice(replies)
    return random.choice(_HUMAN_REPLIES["default"])


class HumanResponder(BaseResponder):
    name = "Human"

    # occasional deliberate typos
    _TYPOS = {
        "the": "teh", "that": "taht", "and": "adn", "have": "ahve",
        "think": "htink", "your": "yoru",
    }

    def _add_typo(self, text: str) -> str:
        if random.random() < 0.25:          # 25% chance of one typo
            words = text.split()
            for i, w in enumerate(words):
                clean = w.strip(".,!?")
                if clean in self._TYPOS:
                    words[i] = w.replace(clean, self._TYPOS[clean])
                    return " ".join(words)
        return text

    def respond(self, question: str, history: List[Tuple[str, str]]) -> Tuple[str, float]:
        core = _human_lookup(question)
        intro = random.choice(_HUMAN_INTROS)
        filler = random.choice(_HUMAN_FILLERS)
        raw = f"{intro}{core}{filler}"
        text = self._add_typo(raw)
        # humans take longer to type longer messages
        delay = random.uniform(1.5, 3.5) + len(text) * 0.01
        return text, delay


# ── AI-like responder ─────────────────────────────────────────────────────────

_AI_REPLIES = [
    "That's an interesting question. I would say it depends on context and one's"
    " individual perspective.",
    "I find this topic quite nuanced. There are multiple valid viewpoints worth"
    " considering.",
    "My understanding is that this is an area where empirical evidence and"
    " personal experience often diverge.",
    "I appreciate the question. Reasoning carefully, I think the most defensible"
    " position involves weighing several factors.",
    "This is a question that has fascinated thinkers for centuries. I lean toward"
    " a pragmatic interpretation.",
    "There is genuine uncertainty here. I try to hold my views tentatively and"
    " remain open to revision.",
    "Logically speaking, the answer hinges on how we define the key terms"
    " involved.",
    "I would characterise my view as cautiously optimistic, though I acknowledge"
    " the counterarguments.",
    "The evidence suggests a moderate position. Extremes on either side tend to"
    " oversimplify.",
    "That is a fair challenge. Let me think through it systematically.",
]

_AI_SUFFIX = [
    " Would you like to explore this further?",
    " Does that align with your own thinking?",
    " I am happy to elaborate if helpful.",
    " What is your perspective?",
    "",
    "",
]


class AIResponder(BaseResponder):
    name = "AI"

    def respond(self, question: str, history: List[Tuple[str, str]]) -> Tuple[str, float]:
        base = random.choice(_AI_REPLIES)
        suffix = random.choice(_AI_SUFFIX)
        text = base + suffix
        # AI responses arrive more consistently — less variable timing
        delay = random.uniform(0.8, 2.0)
        return text, delay
