# EXPERTISE · VAL-FUNCTIONAL — does what exists actually work?
**Status:** draft · **Type:** contract · **Updated:** 2026-07-31 · **Owner:** brian
**Ticket:** F1-quater-1 · **Branch of:** `principles/owner-3-validation.md` (functional-flow validation)
**Language:** US English · **Read by:** owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for proving something works** — as opposed to believing it does.

> ⛔ **The AI does not invent criterion** (ADR-003).

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional ⬅ THIS FILE · val-integration
```

**Why this discipline exists — the failure that created it:**

| When | What was said |
|---|---|
| 26-jul 06:24 | *"tiene el estado completo para retomar sin perder nada"* |
| **26-jul 06:33**, after a `/clear` | *"lo que está mal es que este archivo lo implementa a medias"* |

Same code, opposite verdicts, nine minutes apart. **A verdict that changes with context is not a
verdict — it is a mood.** This file is what makes the verdict reproducible.

---

## 1 · CONTEXT ALREADY CAPTURED

### The rule that governs everything here

> **Brian (Método F §2.4):** *"no basta probar el carril; hay que verificar que TODO sigue conectado."*

### ⭐ Affirmative verification — already LOCKED, not pending

Every check confirms with **a datum**: *"recovered X"* · *"vector = 1024 dims"* · *"21 tools"*.
**Never** *"seems fine"* · *"it should work"* · *"more or less."*

> **"More or less connected" is the declared enemy** (Método F §2.2). When something *almost*
> works → stop and investigate.

### The §5-BIS battery — inherited from v1, seven checks

Already written in `owner-3-validation.md` §4 (A base suite · B real startup · C `/salud` · D memory
in depth · E every milestone · F tools · G what the phase added). **This file does not restate it —
it captures the criterion for judging its results.**

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

### 2.1 · Architecture — the shape of the proof
**Question (frame):** does each piece have one responsibility?
**Here:** does each check prove one thing, or does a green mask two untested paths?

> ⬜ **PENDING · BRIAN**

### 2.2 · Data design — the evidence itself
**Question (frame):** does it represent reality?
**Here:** which datum counts as proof, and which datum only looks like proof.

> ⬜ **PENDING · BRIAN**

### 2.3 · Abstraction — depth of testing
**Question (frame):** the right level?
**Here:** when a unit test is enough and when only the real system counts. Measured precedent:
*"unit tests do not exercise the actual prompt or behavior."*

> ⬜ **PENDING · BRIAN**

### 2.4 · Naming — what a check is called
**Question (frame):** does the name say what it does?
**Here:** does a failing check name what broke, or only that something did?

> ⬜ **PENDING · BRIAN**

### 2.5 · Contracts — what green means
**Question (frame):** are errors part of the contract?
**Here:** what a reader is entitled to assume from a passing check. Measured precedent: an EMPTY
scope scored 🟢 PRODUCT because there was nothing to measure — **absence of evidence read as
evidence.**

> ⬜ **PENDING · BRIAN**

### 2.6 · Necessity — does this check have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** which check has never failed and never will — and is therefore theater.

> ⬜ **PENDING · BRIAN**

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ⬜ **PENDING · BRIAN** — what is **never** accepted as proof.
> Shape that works (an existing one): *"affirmative verification: confirm with a datum, never
> with 'seems fine'."*

---

## 4 · WHAT MAKES BRIAN REJECT A VERIFICATION

> ⬜ **PENDING · BRIAN** — the signals that make him say *"you did not actually test this."*

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**

**Suggested questions for the interview:**

1. What do you demand before believing something works?
2. What makes you distrust a green result?
3. Which datum counts as proof, and which one only looks like it?
4. When is a unit test enough, and when does only the real system count?
5. What has to be true before something touches production?
6. Which verification mistake have you caught most often — in me?
7. What would you rather see fail loudly than pass quietly?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 applies criterion 1 (functional) with it |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ⚠️ **While §2-§4 stay empty, the wiring works but the criterion is void.** The §5-BIS battery
> and affirmative verification already operate — they do not depend on these holes.

---

Related: `principles/owner-3-validation.md` (the owner this branches from) ·
`principles/expertise/val-integration.md` (its sibling) · `rules/ESTANDAR_Metodo_Fases_F.md` §5-BIS ·
`bin/grade-block` (layer 1) · `docs/PENDING-BRIAN.md`.
