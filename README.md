# Turing Test & CAPTCHA — Terminal Implementation

Artificial Intelligence course demonstration. - Individual Assignment
Two sides of the same question: can you tell human from machine?

---

## Members

| Name | Roll Number |
|---|---|
| Mayank Rao ponnala | SE24UCSE026 |

---

## Concept

### The Turing Test (1950)

Alan Turing proposed the **Imitation Game** — a test of machine intelligence. A human judge converses with two entities (one human, one machine) without knowing which is which. If the judge cannot reliably distinguish the machine from the human, the machine is said to have **passed**.

This implementation frames the Turing Test as an **Interrogation Room** — the player is a detective who must determine whether the suspect across the table is a human or a machine.

### CAPTCHA (2003)

von Ahn et al. proposed the **reverse Turing Test**. The system is the judge. The user is tested. This implementation replaces distorted-text challenges with **pure logic puzzles** — tasks that are intuitive for humans but expose the mechanical nature of bots through timing and reasoning patterns.

### Key Difference

```
Turing Test   →  AI tries to pass as human       →  Human is the judge
CAPTCHA       →  Human tries to prove humanity   →  Machine is the judge
```

---

## Architecture

```
+------------------------------------------------------------------+
|                    INTERROGATION ROOM (Turing Test)              |
|                                                                  |
|   DETECTIVE (you)                                                |
|       |                                                          |
|       |  questions                                               |
|       v                                                          |
|   INTERROGATION ROOM CONTROLLER                                  |
|       — randomly seats one suspect, hides identity              |
|       — simulates thinking delay (animated)                      |
|       — watches for contradictions if detective applies pressure |
|       |                                                          |
|       |  routes to:                                              |
|       |                                                          |
|   HumanSuspect                    MachineSuspect                 |
|   — personal backstory            — fixed cover story            |
|   — emotional drift, typos        — over-precise, no fatigue    |
|   — can be caught contradicting   — perfectly consistent         |
|       |                                                          |
|       v                                                          |
|   DETECTIVE submits verdict: Human / Machine / Inconclusive      |
|       |                                                          |
|       v                                                          |
|   SESSION LOG — tracks detective accuracy + machine escape rate  |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|                    LOCKDOWN (CAPTCHA)                            |
|                                                                  |
|   PLAYER (you)                                                   |
|       |                                                          |
|       v                                                          |
|   PUZZLE SELECTOR                                                |
|       one of six logic puzzle types:                             |
|       Syllogism / Truth&Liar / OddOneOut / Weight&Logic /        |
|       CipherDecode / GridReasoning                               |
|       |                                                          |
|       |  puzzle rendered to terminal                             |
|       v                                                          |
|   PLAYER submits answer                                          |
|       |                                                          |
|       v                                                          |
|   TIMING GATE                                                    |
|       — answer < 2.0s → bot flagged, immediate lockout           |
|       — hint available on second attempt                         |
|       — max 3 attempts before lockout                            |
|       |                                                          |
|       v                                                          |
|   GATE: PASS (human verified) or FAIL (bot suspected / lockout)  |
+------------------------------------------------------------------+
```

---

## Project Structure

```
turing-captcha/
|
+-- main.py                      Entry point, main menu, session summary
|
+-- engine/
|   +-- terminal.py              All terminal output: ANSI, typewriter, boxes
|   +-- records.py               Session log for both modules
|
+-- interrogation/
|   +-- suspects.py              HumanSuspect and MachineSuspect classes
|   +-- room.py                  Interrogation Room controller + contradiction detection
|   +-- detective.py             Turing Test game loop
|
+-- lockdown/
|   +-- puzzles.py               Six logic puzzle types (all inherit BasePuzzle)
|   +-- gate.py                  Timing gate, retry logic, CAPTCHA game loop
```

---

## CAPTCHA — Logic Puzzle Types

| Puzzle | Human Advantage | Why Bots Fail |
|---|---|---|
| Syllogism | Deductive reasoning is intuitive | Requires formal logic parsing |
| Truth & Liar | Contradiction detection is natural | Nested negation is computationally costly |
| Odd One Out | Categorical perception is instant | Requires semantic knowledge graph |
| Weight & Logic | Arithmetic + reasoning combined | Multi-step inference pipeline |
| Cipher Decode | Pattern recognition, not computation | Slower lookup / brute-force |
| Grid Reasoning | Spatial counting is instant | Grid parsing + query processing takes time |

All puzzles enforce a **2.0 second timing gate** — answers arriving faster than this are flagged as bot behaviour and trigger immediate lockout.

---

## Interrogation Room — How the Suspects Work

```python
room = InterrogationRoom()  # randomly seats Human or Machine
```

The room randomly seats either a `HumanSuspect` or a `MachineSuspect`. The detective never knows which is which until the reveal.

**HumanSuspect:**
- Has a randomly assigned backstory (name, job, city, hobby, pet, food, age)
- Emotional drift increases with each question — becomes defensive and tired
- Occasional self-contradiction (10% chance per revisited topic)
- Response timing is slow and variable (1.8–4.0s)

**MachineSuspect:**
- Has a fixed cover story it maintains perfectly
- Responds with over-precise, logically structured answers
- Never contradicts itself — pressure questions always fail
- Response timing is fast and uniform (0.6–1.4s)

**Contradiction Detection:**
If the detective includes phrases like *"but earlier you said"* or *"you just contradicted yourself"*, the room checks for genuine inconsistency. A human has a ~45% chance of being caught. A machine is never caught.

---

## Setup

No external libraries required. Pure Python standard library.

```bash
python main.py
```

### Step 1 — Clone the repository

```bash
git clone https://github.com/Mayank06SW/turing-captcha.git
cd turing-captcha
```

### Step 2 — Usage

```
MAIN MENU
  [1]  Interrogation Room    -- Turing Test: you are the detective
  [2]  Lockdown Puzzles      -- CAPTCHA: prove you are human
  [3]  Session Summary
  [Q]  Quit
```

**Inside the Interrogation Room:**
Ask the suspect questions freely. Use pressure phrases like *"but earlier you said..."* to catch contradictions. After 4+ questions, enter:
- `H` → verdict: Human
- `M` → verdict: Machine
- `I` → verdict: Inconclusive
- `Q` → abandon round

**Inside Lockdown:**
Choose a puzzle type or run all six in sequence. Read carefully and take your time — the timing gate requires at least 2 seconds or you will be flagged as a bot.

---

## Upgrading as the Course Progresses

The architecture is designed to grow:

**Add a new logic puzzle:**
```
1. Create a class in lockdown/puzzles.py
2. Inherit from BasePuzzle
3. Implement: build() / display() / hint / check()
4. Add to the PUZZLES list at the bottom of the file
Nothing else changes.
```

**Add a new suspect type:**
```
1. Create a class in interrogation/suspects.py
2. Inherit from BaseSuspect
3. Implement: respond() and true_identity
4. Add it to the random.choice() in InterrogationRoom.__init__()
Nothing else changes.
```

**Connect to a real LLM (GPT, Claude):**
```
1. Replace MachineSuspect.respond() with an API call
2. The Room, timing, scoring — all unchanged.
```

---

## References

- Turing, A. M. (1950). Computing Machinery and Intelligence. *Mind*, 59(236), 433–460.
- von Ahn, L., Blum, M., Hopper, N., & Langford, J. (2003). CAPTCHA: Using Hard AI Problems for Security.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*. Chapter 2: Intelligent Agents.
