# EXPERTISE · DOC-PLANNING — a plan someone can execute
**Status:** draft · **Type:** contract · **Updated:** 2026-07-31 · **Owner:** brian
**Ticket:** F1-ter-1 · **Branch of:** `principles/owner-1-docs.md` (documentation format)
**Language:** US English · **Read by:** owner-1 before writing a plan, owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for planning**, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (ADR-003). It asks, structures and applies — it never
> fills this in on its own. That error is what produced *"todo está hecho como la IA quiso."*

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning ⬅ THIS FILE · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration
```

**Why planning is its own discipline:** a plan is judged by whether someone else can execute it
without asking what was meant. That is a different skill from formatting a document correctly —
a perfectly formatted plan can still be unexecutable.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian — to expand, not to replace

| Quote | Date |
|---|---|
| *"que sepa por qué se hizo esto primero antes que otro punto"* | 2026-07-27 |
| *"explicar antes de construir · aprobar antes de ejecutar"* | LOCKED rule |
| *"nunca plan global; por pieza → alinear visión → aprobar → construir"* | 2026-07-20 |

**Precedents this criterion should formalize:**
- the default plan sections (`owner-1-docs.md` §2) — purpose · **why this order** · phases and
  tickets · what can go wrong · what it does NOT do
- *"the contract is a floor, not a ceiling"* — a plan that discovered something new says so
- the Método F: `rules/ESTANDAR_Metodo_Fases_F.md`

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

The frame lives in `rules/qa-dimensions.md`. What each demands **here** is Brian's criterion.

### 2.1 · Architecture — the shape of the plan
**Question (frame):** does each piece have one responsibility, at the right level?
**Here:** is each phase one thing, or is it three things sharing a number?

> ⬜ **PENDING · BRIAN**

### 2.2 · Data design — what the plan states as fact
**Question (frame):** does it represent reality? Are impossible states impossible?
**Here:** what must be MEASURED before the plan claims it.

> ⬜ **PENDING · BRIAN**

### 2.3 · Abstraction — the level of detail
**Question (frame):** the right level, neither repeated nor over-generalized?
**Here:** when a ticket is too big to execute and when it is so small it is noise.

> ⬜ **PENDING · BRIAN**

### 2.4 · Naming — phases and tickets
**Question (frame):** does the name say what it does without reading the body?
**Here:** does `F4-2` say what it delivers, or does it need the paragraph under it?

> ⬜ **PENDING · BRIAN**

### 2.5 · Contracts — what the plan promises
**Question (frame):** are the interfaces declared? Are errors part of the contract?
**Here:** the success criterion of each ticket. *"It works"* is not a criterion.

> ⬜ **PENDING · BRIAN**

### 2.6 · Necessity — does this phase have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** which phase could be deleted with nothing lost.

> ⬜ **PENDING · BRIAN**

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ⬜ **PENDING · BRIAN** — what is **never** done when planning, no exceptions.
> Format: one line, imperative, verifiable.
> Shape that works (an existing one): *"explain and get approval before building."*

---

## 4 · WHAT MAKES BRIAN REJECT A PLAN

> ⬜ **PENDING · BRIAN** — the signals that make him say *"this plan is not ready."*

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> Never the reverse — a draft written first comes out as *"use best practices."*

**Suggested questions for the interview:**

1. What do you demand of a plan before approving it?
2. What makes you reject one outright?
3. How do you know a phase is too big before it is executed?
4. What has to be written down for you to trust the order of the phases?
5. Which planning mistake do you see most often and bothers you most?
6. When is a plan finished — as opposed to just long?
7. What must a plan say about what it will NOT do?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 evaluates the 6 dimensions using it |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ⚠️ **While §2-§4 stay empty, the wiring works but the criterion is void.** Layer 1 of QA
> (`bin/grade-block`) does not depend on this file.

---

Related: `principles/owner-1-docs.md` (the owner this branches from) · `principles/expertise/doc-structure.md`
(its sibling) · `rules/qa-dimensions.md` (the frame) · `rules/ESTANDAR_Metodo_Fases_F.md` ·
`docs/PENDING-BRIAN.md` (the index of every hole).
