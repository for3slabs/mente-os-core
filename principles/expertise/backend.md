# EXPERTISE · BACKEND
**Status:** draft · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F1-bis-1 · runs in parallel with F2-F3
**Language:** US English · **Read by:** owner-2 (development) before writing code, and owner-3
(validation) at block close.
**Injected by:** the block's §D `Required standards` + the hook (architecture §12-QUATER).
---

## 0 · WHAT THIS FILE IS

The **expert criterion** for this discipline, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (architecture §9.1). It asks, structures, and applies —
> it never fills this in on its own. That is exactly the error that produced the current state:
> *"todo está hecho como la IA quiso."*

**Why it is not blocking:** F1 closes with `database.md` alone. Backend and frontend run in
parallel with F2-F3 so the criterion is not a bottleneck.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian

| Quote | Date |
|---|---|
| *"no dejes cosas como hardcodeadas"* | 2026-07-24 |
| *"si va a pasar, tenemos que estandarizar"* | 2026-07-25 |
| *"cero hardcodeo: hosts/puertos/credenciales SIEMPRE de ENV"* | Método F §2.3 |

**Precedents to formalize:** the single guard in `session.ts` (12 copies → 0) ·
`instancias.ts` as a 100%-DB bridge with no env · brute-force protection in `verificacion.ts`.

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

1. What do you demand of an endpoint before it is done?
2. What makes you reject a backend change?
3. When does an error belong to the contract, and when is it a crash?
4. What must never be hardcoded, beyond credentials?
5. How do you decide whether logic belongs in the API or in the DB?
6. What has to be true before something goes to production?
7. Which backend error do you see most often?

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
