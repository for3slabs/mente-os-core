# EXPERTISE · VAL-INTEGRATION — the bugs live BETWEEN the pieces
**Status:** draft · **Type:** contract · **Updated:** 2026-07-31 · **Owner:** brian
**Ticket:** F1-quater-2 · **Branch of:** `principles/owner-3-validation.md` (functional-flow validation)
**Language:** US English · **Read by:** owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for the seams** — what happens where two pieces meet, which is where the
expensive bugs live.

> ⛔ **The AI does not invent criterion** (ADR-003).

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration ⬅ THIS FILE
```

**Why it is separate from `val-functional`:** that one asks *"does this piece work?"* This one asks
*"does the chain still work when every piece works?"* Every piece can pass its own test and the
flow still be broken — that is the failure this discipline exists for.

---

## 1 · CONTEXT ALREADY CAPTURED

### The rule that created this discipline

> **Brian, 2026-07-20:** *"los bugs trágicos viven ENTRE las piezas — auditoría punta a punta con
> datos reales."*
> (memory `feedback_probar_flujo_completo_encadenado`)

### Measured cases — every one of these lived at a seam

| Case | What broke between pieces |
|---|---|
| `kind` (a cookie value) used as the real instance | **the same bug in 6 files** |
| "resolve the instance" copied in 6 places | the fix needed a *"barrido completo del patrón"* |
| `DEMO_ENC_KEY` diverging local vs Vercel since June | the fallback hid it — **production down** |
| `tailscale serve` silently turning off the Funnel | verified from my environment, not Vercel's — **production down again** |
| The 21-jul incident | recovered from a raw `.jsonl` six days later |
| `check-clear-ready` pointing at a path a migration had deleted | guarded by `os.path.exists`, it failed **silently** — the check protecting the cold-start brief had never run |

> ⭐ **The pattern in all six:** each piece was fine on its own. What failed was the assumption one
> piece made about another.

### The reconnection test — already LOCKED

`owner-3-validation.md` §4-D: *restart a sibling, run the flow again, confirm it reconnects from
ENV and not from a hardcoded host.*

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

### 2.1 · Architecture — the map of the seams
**Question (frame):** does each piece have one responsibility, at the right level?
**Here:** are all the consumers of a piece known before it is changed?

> ⬜ **PENDING · BRIAN**

### 2.2 · Data design — what crosses the seam
**Question (frame):** are impossible states impossible?
**Here:** what a piece is entitled to assume about the data another one hands it.

> ⬜ **PENDING · BRIAN**

### 2.3 · Abstraction — the shared pattern
**Question (frame):** copied three times, or over-generalized?
**Here:** when the same logic in two places is duplication and when it is coincidence.

> ⬜ **PENDING · BRIAN**

### 2.4 · Naming — across the boundary
**Question (frame):** does the name say what it does?
**Here:** the same concept must not have two names on two sides of a seam.

> ⬜ **PENDING · BRIAN**

### 2.5 · Contracts — ⭐ the core of this discipline
**Question (frame):** are interfaces declared? Are errors part of the contract?
**Here:** what each side promises, and what happens when the other side fails. Measured precedent:
**44 DB accesses with 0 try/catch.**

> ⬜ **PENDING · BRIAN**

### 2.6 · Necessity — does this connection have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** which dependency could be removed entirely instead of tested.

> ⬜ **PENDING · BRIAN**

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ⬜ **PENDING · BRIAN** — what is **never** done across a seam.
> Shapes that already work (existing ones):
> - *"a default never points at something that has an owner"*
> - *"testing from my environment is not testing production"*

---

## 4 · WHAT MAKES BRIAN REJECT AN INTEGRATION

> ⬜ **PENDING · BRIAN** — the signals that say *"this was tested in isolation only."*

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**

**Suggested questions for the interview:**

1. What do you demand before believing two pieces really talk to each other?
2. How do you know a change will not break something downstream?
3. What must be tested with real data and never with a mock?
4. Which integration failure has cost you the most, and what would have caught it?
5. When a piece fails, what should the piece next to it do?
6. What has to be verified in the real environment, not a local one?
7. Which assumption between pieces do you see broken most often?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 applies it alongside `val-functional.md` |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ⚠️ **While §2-§4 stay empty, the wiring works but the criterion is void.**

---

Related: `principles/owner-3-validation.md` (the owner this branches from) ·
`principles/expertise/val-functional.md` (its sibling) · `rules/case-dangerous-default.md` ·
`memory feedback_probar_flujo_completo_encadenado` · `docs/PENDING-BRIAN.md`.
