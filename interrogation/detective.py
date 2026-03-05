"""
interrogation/detective.py

Game loop for the Interrogation Room module.
The player is the detective. They question the suspect, look for cracks,
then submit a verdict: Human / Machine / Inconclusive.
"""

import time
from engine import terminal as T
from engine.records import SessionLog
from interrogation.room import InterrogationRoom, MIN_QUESTIONS, MAX_QUESTIONS, PRESSURE_PHRASES


_INTRO_LINES = [
    "The door swings shut behind you.",
    "A single bulb flickers overhead.",
    "Across the steel table, the suspect waits.",
    "You open your notepad.",
    "They could be human. They could be a machine.",
    "Your job: find out which.",
]

_HINT_LINES = [
    "  Ask personal questions — machines over-explain, humans ramble.",
    "  Ask about feelings — machines describe states, humans feel them.",
    "  Try a contradiction — use phrases like 'but earlier you said...'",
    "  Watch the response time — machines answer unnervingly fast.",
    "  Ask something illogical — humans laugh it off, machines process it.",
]


def _intro_scene() -> None:
    T.clr()
    T.line("═", col=T.A.B + T.A.RED)
    print(T.c(T.A.B + T.A.RED,   "  INTERROGATION ROOM"))
    print(T.c(T.A.GRY,           "  Turing Test — Interrogation Mode"))
    T.line("═", col=T.A.B + T.A.RED)
    print()
    for line in _INTRO_LINES:
        T.typewrite(line, delay=0.03, col=T.A.IT + T.A.GRY)
        time.sleep(0.15)
    print()
    T.line(col=T.A.GRY)
    print(T.c(T.A.B, "\n  DETECTIVE TIPS"))
    for h in _HINT_LINES:
        print(T.c(T.A.GRY, h))
    print()
    T.line(col=T.A.GRY)
    print()
    print(T.c(T.A.GRY,
        f"  Ask at least {MIN_QUESTIONS} questions. Commands:\n"
        f"  {T.c(T.A.YLW,'H')} → verdict: Human   "
        f"  {T.c(T.A.YLW,'M')} → verdict: Machine   "
        f"  {T.c(T.A.YLW,'I')} → Inconclusive   "
        f"  {T.c(T.A.YLW,'Q')} → abandon"))
    print()
    T.pause("  Press ENTER to begin the interrogation…")


def _print_exchange_header(room: InterrogationRoom) -> None:
    q = room.question_count
    bar = T.c(T.A.GRY, f"  Q:{q}  ")
    if q >= MIN_QUESTIONS:
        bar += T.c(T.A.GRN, "  [verdict available: H / M / I]")
    else:
        bar += T.c(T.A.GRY, f"  [need {MIN_QUESTIONS - q} more question(s) before verdict]")
    print(bar)


def run_interrogation(log: SessionLog) -> None:
    _intro_scene()

    room = InterrogationRoom()
    verdict = None

    T.clr()
    T.line("─", col=T.A.RED)
    print(T.c(T.A.B + T.A.RED, "  INTERROGATION IN PROGRESS"))
    T.line("─", col=T.A.RED)
    print()

    while True:
        _print_exchange_header(room)
        raw = T.ask("Detective", col=T.A.B + T.A.YLW)

        if not raw:
            continue

        upper = raw.upper()

        # ── abandon ───────────────────────────────────────────────────────────
        if upper == "Q":
            T.status("warn", "Interrogation abandoned — no verdict recorded.")
            T.pause()
            return

        # ── verdict ───────────────────────────────────────────────────────────
        if upper in ("H", "M", "I"):
            if room.question_count < MIN_QUESTIONS:
                T.status("warn",
                    f"Need at least {MIN_QUESTIONS} questions first "
                    f"({room.question_count} asked).")
                continue
            verdict_map = {"H": "Human", "M": "Machine", "I": "Inconclusive"}
            verdict = verdict_map[upper]
            break

        # ── max questions ─────────────────────────────────────────────────────
        if room.question_count >= MAX_QUESTIONS:
            T.status("warn",
                "Maximum questions reached. Submit verdict: H, M, or I.")
            continue

        # ── question ──────────────────────────────────────────────────────────
        response = room.question(raw)
        print()
        T.typewrite(f"Suspect:  {response}", delay=0.018, col=T.A.WHT)
        print()

    # ── reveal ────────────────────────────────────────────────────────────────
    true_id = room.true_identity
    correct = (verdict == true_id)
    log.log_interrogation(true_id, verdict, room.question_count, room.broke)

    print()
    T.line("═", col=T.A.B + T.A.RED)
    print(T.c(T.A.B,           "  CASE CLOSED"))
    T.line("─", col=T.A.GRY)
    T.c(T.A.GRY, "")
    print(f"  Your verdict     :  {T.c(T.A.B, verdict)}")
    print(f"  Suspect was      :  {T.c(T.A.B, true_id)}")
    print(f"  Questions asked  :  {room.question_count}")
    print(f"  Contradictions   :  {'Yes — suspect broke' if room.broke else 'None caught'}")
    T.line("═", col=T.A.B + T.A.RED)

    if correct:
        T.verdict_screen(True,
            "CORRECT — You read them right.",
            "Good detective work.")
    else:
        if true_id == "Machine" and verdict != "Machine":
            T.verdict_screen(False,
                "WRONG — The machine slipped through.",
                "It passed the Turing Test. You were fooled.")
        else:
            T.verdict_screen(False,
                "WRONG — You misread the suspect.",
                "Back to detective school.")

    T.pause()
