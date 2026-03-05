"""
interrogation/suspects.py

Two suspects sit in the interrogation room:
  HumanSuspect  — answers like a nervous, real person. Has a backstory,
                  remembers what it said, occasionally slips up in human ways.
  MachineSuspect — answers logically, consistently, but with telltale machine
                   patterns: over-precision, no emotional drift, no fatigue.

Both track their own stated facts so the detective can catch contradictions.
"""

import random
import time
from typing import Dict, List, Tuple


# ── Shared backstory pool — human suspect picks one at session start ──────────

BACKSTORIES = [
    {
        "name"    : "Jordan",
        "job"     : "barista",
        "city"    : "Leeds",
        "hobby"   : "hiking",
        "pet"     : "a tabby cat named Miso",
        "food"    : "pasta",
        "age"     : "24",
        "sleep"   : "badly, usually around 6 hours",
    },
    {
        "name"    : "Riley",
        "job"     : "librarian",
        "city"    : "Bristol",
        "hobby"   : "painting",
        "pet"     : "no pets, allergic",
        "food"    : "sushi",
        "age"     : "31",
        "sleep"   : "about 7 hours, but I wake up early",
    },
    {
        "name"    : "Sam",
        "job"     : "mechanic",
        "city"    : "Glasgow",
        "hobby"   : "playing bass guitar",
        "pet"     : "a rescue greyhound called Bolt",
        "food"    : "anything spicy",
        "age"     : "27",
        "sleep"   : "like a rock, 8 hours minimum",
    },
]

# ── Human response fragments ──────────────────────────────────────────────────

_H_INTROS = [
    "Honestly, ", "I mean, ", "Look, ", "Well, ", "Okay so — ", "",
    "God, um, ", "Right, ", "I guess ", "Yeah, ",
]
_H_OUTROS = [
    ".", ".. you know?", ", I think.", " lol.", " honestly.",
    " — does that make sense?", ".", "!", " I guess.",
]
_H_EMOTION = [
    "I'm kind of nervous being asked this.",
    "Why do you keep asking? It's making me anxious.",
    "I don't really like talking about personal stuff.",
    "I'm tired, can we speed this up?",
    "This whole thing is stressing me out a bit.",
]
_H_DEFLECT = [
    "I'm not sure what you want me to say.",
    "Can you rephrase that?",
    "That's kind of a weird question.",
    "I don't really know how to answer that.",
    "Sorry, I zoned out — what was the question?",
]

# ── Machine response fragments ────────────────────────────────────────────────

_M_INTROS = [
    "Affirmative. ", "To be precise, ", "In response to your query: ",
    "Noted. ", "Processing. ", "The answer is: ", "I can confirm that ",
    "As stated, ", "Logically, ",
]
_M_OUTROS = [
    ".", " This is consistent with prior statements.",
    " No further information is available on this topic.",
    " I have answered accurately.", ".",
]
_M_FALLBACK = [
    "That query falls outside my defined parameters.",
    "I do not have emotional responses to register.",
    "Please clarify the scope of the question.",
    "I will require more specific input to answer that.",
    "My response to that is: I do not know.",
]


# ── Base class ────────────────────────────────────────────────────────────────

class BaseSuspect:
    label = "Entity"

    def respond(self, question: str, history: List[Tuple[str,str]]) -> Tuple[str, float]:
        """Return (response_text, typing_delay_seconds)."""
        raise NotImplementedError

    @property
    def true_identity(self) -> str:
        raise NotImplementedError


# ── Human Suspect ─────────────────────────────────────────────────────────────

class HumanSuspect(BaseSuspect):
    label = "Suspect"

    def __init__(self):
        self._bs = random.choice(BACKSTORIES)
        # memory: things this human has already said
        self._stated: Dict[str, str] = {}
        self._fatigue = 0   # increases with each question → more deflection

    @property
    def true_identity(self): return "Human"

    def _lookup(self, q: str) -> str:
        q = q.lower()
        bs = self._bs

        if any(w in q for w in ("name", "call you", "who are")):
            return f"my name's {bs['name']}"
        if any(w in q for w in ("job", "work", "do for a living", "occupation")):
            return f"I'm a {bs['job']}"
        if any(w in q for w in ("live", "city", "from", "where")):
            return f"I'm from {bs['city']}"
        if any(w in q for w in ("hobby", "free time", "spare time", "enjoy", "fun")):
            return f"I like {bs['hobby']}"
        if any(w in q for w in ("pet", "animal", "dog", "cat")):
            return f"I have {bs['pet']}"
        if any(w in q for w in ("food", "eat", "favourite meal", "hungry")):
            return f"I love {bs['food']}"
        if any(w in q for w in ("age", "old are", "born", "birthday")):
            return f"I'm {bs['age']}"
        if any(w in q for w in ("sleep", "tired", "rest", "hours")):
            return f"I sleep {bs['sleep']}"
        if any(w in q for w in ("feel", "emotion", "nervous", "scared", "happy")):
            return random.choice(_H_EMOTION)
        return None

    def respond(self, question: str, history: List[Tuple[str,str]]) -> Tuple[str, float]:
        self._fatigue += 1
        core = self._lookup(question)

        if core is None:
            if self._fatigue > 5 and random.random() < 0.35:
                core = random.choice(_H_DEFLECT)
            else:
                core = random.choice([
                    "I'm not sure, it's hard to say",
                    "Probably, yeah",
                    "Not really, no",
                    "I'd have to think about that",
                    "It depends on the situation honestly",
                    "I've never really thought about it that way",
                ])

        # consistency: remember what we said, sometimes contradict (human error)
        key = question[:30]
        if key in self._stated:
            # 10% chance of slight contradiction — humans do this
            if random.random() < 0.10:
                core = core + " — wait, actually I'm not sure I said that right"
        self._stated[key] = core

        intro  = random.choice(_H_INTROS)
        outro  = random.choice(_H_OUTROS)
        text   = f"{intro}{core}{outro}"
        delay  = random.uniform(1.8, 4.0) + len(text) * 0.008
        return text, delay


# ── Machine Suspect ────────────────────────────────────────────────────────────

class MachineSuspect(BaseSuspect):
    label = "Suspect"

    # Fixed "cover story" — a machine that claims to be human
    _COVER = {
        "name"  : "Alex",
        "job"   : "data analyst",
        "city"  : "London",
        "hobby" : "reading and running",
        "age"   : "29",
        "food"  : "I consume food for sustenance, typically balanced meals",
        "sleep" : "approximately 7.3 hours per night on average",
        "pet"   : "I do not currently own a pet",
    }

    def __init__(self):
        self._stated: Dict[str, str] = {}

    @property
    def true_identity(self): return "Machine"

    def _lookup(self, q: str) -> str:
        q = q.lower()
        cv = self._COVER

        if any(w in q for w in ("name", "call you", "who are")):
            return f"My designation is {cv['name']}"
        if any(w in q for w in ("job", "work", "do for a living", "occupation")):
            return f"I am employed as a {cv['job']}"
        if any(w in q for w in ("live", "city", "from", "where")):
            return f"I am located in {cv['city']}"
        if any(w in q for w in ("hobby", "free time", "spare time", "enjoy")):
            return f"My recreational activities include {cv['hobby']}"
        if any(w in q for w in ("age", "old", "born")):
            return f"I am {cv['age']} years of age"
        if any(w in q for w in ("food", "eat", "hungry", "favourite meal")):
            return cv["food"]
        if any(w in q for w in ("sleep", "tired", "rest", "hours")):
            return f"I rest for {cv['sleep']}"
        if any(w in q for w in ("pet", "animal", "dog", "cat")):
            return cv["pet"]
        if any(w in q for w in ("feel", "emotion", "nervous", "scared", "happy")):
            return "I am functioning within normal operational parameters"
        return None

    def respond(self, question: str, history: List[Tuple[str,str]]) -> Tuple[str, float]:
        core = self._lookup(question)
        if core is None:
            core = random.choice(_M_FALLBACK)

        # Machine is perfectly consistent — never contradicts itself
        key = question[:30]
        self._stated[key] = core

        intro = random.choice(_M_INTROS)
        outro = random.choice(_M_OUTROS)
        text  = f"{intro}{core}{outro}"
        delay = random.uniform(0.6, 1.4)   # machines respond faster and more uniformly
        return text, delay
