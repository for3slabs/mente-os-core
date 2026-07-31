# EXPERTISE · DATABASE
**Status:** draft · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F1-2 · closes phase F1
**Language:** US English · **Read by:** owner-2 (development) before writing code, and owner-3
(validation) at block close.
**Injected by:** the block's §D `Required standards` + the hook (architecture §12-QUATER).
---

## 0 · WHAT THIS FILE IS

The **expert criterion** for this discipline, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (architecture §9.1). It asks, structures, and applies —
> it never fills this in on its own. That is exactly the error that produced the current state:
> *"todo está hecho como la IA quiso."*

**Why this discipline goes first:** it is where Brian has already expressed the most criterion,
and it is **what propagates the most** — touching the DB reaches everything that reads the table.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian — to expand, not to replace

| Quote | Date |
|---|---|
| *"vamos a desarrollar una base de datos, no un MVP pedorro, vamos por un producto"* | 2026-07-24 |
| *"la base de datos es la base de información, si no tenemos un control estamos mal"* | 2026-07-24 |
| *"esos valores no deberían estar puestos en el código... debería estar en la base de datos y poder solo modificar la base de datos"* | 2026-07-25 |
| *"tenemos que estandarizar cómo es que creamos los hilos para que no pase esta situación"* | 2026-07-25 |

**Precedents already built that this criterion should formalize:**
- `demo_instancias` as the single source of truth · 7 FKs · `demo_config` editable without a push
- the `hoteles` → `sin-tema` default (`rules/case-dangerous-default.md`)

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

The frame lives in `rules/qa-dimensions.md`. What each dimension **demands here** is Brian's
criterion — pending below.

### 2.1 · Architecture
**Question (frame):** does each piece have a single responsibility and sit in the right layer?
**Required evidence:** the dependency tree + which piece would break how many others.

> ⬜ **PENDING · BRIAN**

### 2.2 · Data design
**Question (frame):** does the schema represent the domain? Are impossible states impossible?
**Required evidence:** the real schema + one case the model cannot represent incorrectly.

> ⬜ **PENDING · BRIAN**

### 2.3 · Abstraction
**Question (frame):** right level — neither copied three times nor generalized for one use?
**Required evidence:** where it repeats, or the real usages.

> ⬜ **PENDING · BRIAN**

### 2.4 · Naming
**Question (frame):** does the name say what it does without reading the body?
**Required evidence:** explain three names without opening the file.

> ⬜ **PENDING · BRIAN**

### 2.5 · Contracts
**Question (frame):** are interfaces declared? Are errors part of the contract?
**Required evidence:** the real signature + what happens when it fails.

> ⬜ **PENDING · BRIAN**

### 2.6 · Necessity
**Question (frame):** does every file that exists have to exist?
**Required evidence:** who consumes it, and why it could not live elsewhere.

> ⬜ **PENDING · BRIAN**

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ⬜ **PENDING · BRIAN** — the things that are **never** done here, no exceptions.
> Format: one line per rule, imperative, verifiable.
> Example of the right shape (from an existing case): *"a default never points at something that
> has an owner."*

---

## 4 · WHAT MAKES BRIAN REJECT WORK IN THIS DISCIPLINE

> ⬜ **PENDING · BRIAN** — the signals that make him say *"this is not a product."*

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> Never the reverse — a draft written first comes out as *"use best practices."*

**Suggested questions for the interview:**

1. What do you demand of a schema before approving it?
2. What makes you reject a DB change outright?
3. Which values must **never** live in code, and why?
4. How do you know a table is badly designed, without running anything?
5. What must be **impossible to represent** in a correct model?
6. When is a FK mandatory, and when is it overkill?
7. What has to be true before a migration touches production?
8. Which DB error do you see most often and bothers you most?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context (layer D, §12-QUATER) |
| Block closes | owner-3 evaluates the 6 dimensions using it (`rules/qa-dimensions.md`) |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ⚠️ **While §2-§4 stay empty, the wiring works but the criterion is void.** Layer 1 of QA
> (`bin/grade-block`) does not depend on this file — that is why F4 can run first.

---

Related: `rules/qa-dimensions.md` (the frame) · `principles/owner-2-dev.md` (who reads it) ·
`principles/owner-3-validation.md` (who applies it) · `docs/Arquitectura_Mente_OS_v2_Bloques.md` §9.
