# RULE · FIX ≠ PATCH
**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-3 · **Source:** architecture §7
---

## Purpose

How to resolve a bug **without stacking code on top of it.** This is the rule that attacks
fix-over-fix directly.

---

## 1 · BRIAN'S WORDS — the contract

> *"No se crea un código o solución arriba solo para tapar el problema. Se evalúa la construcción; a
> partir de saber todo el contexto del código se establece cómo solucionar el error. Si se tiene que
> pensar o hacerlo por otro medio, está bien. **Lo que no está bien es tener decenas de código sin
> orden**, porque tendremos problemas de redundancia."*

---

## 2 · THE PROCEDURE — mandatory

```
1 · DO NOT write the fix yet
2 · EVALUATE THE CONSTRUCTION      — read the piece and its surroundings
3 · KNOW THE FULL CONTEXT          — grep every consumer before deciding
4 · CHOOSE THE REAL SOLUTION       — even if it means another route
5 · DECLARE the propagation in the block (§C, §F)
6 · That sequence is what gets repeated and iterated with the human
```

**Step 3 is the one that gets skipped.** It is the difference between the two questions below.

---

## 3 · ⭐ THE ONE QUESTION THAT CHANGES EVERYTHING

| Fix-over-fix asks | This rule asks |
|---|---|
| *"where does it fail?"* | *"**why does this failure exist, and where else does it live?**"* |

---

## 4 · THE SAME BUG, BOTH WAYS

**Real case: "the API key is stored in the wrong place."**

```
❌ HOW IT WENT
   1. bug reported
   2. find WHERE it fails → one file
   3. fix it there                        → commit d5dc778
   4. another similar symptom appears      → commit 6310bcf
   5. another one                          → commit 5326bb6
   6. discover the pattern was everywhere
   7. "barrido completo del patrón"        → commit b61e3d0
   ⤷ 4 commits for one problem · userStore.ts ended with 21 edits
```

```
✅ WITH THIS RULE
   1. bug reported
   2. touch nothing yet
   3. EVALUATE: where does `kind` come from? who else treats it as the instance?
      → grep: 6 files
   4. FULL CONTEXT: the cause is not "this file stores it wrong",
      it is "kind (a cookie value) is used as if it were the real instance"
   5. REAL SOLUTION: one single point that resolves the real instance
   6. ONE change, 6 sites correct, cause eliminated
   ⤷ 1 commit · the pattern cannot reappear
```

**The difference is not effort. It is step 3.**

---

## 5 · WHEN THE GATE BLOCKS

Editing a piece with declared dependents is one of the **three closed gates**
(architecture §12-QUATER). The gate does not just refuse — it emits an **approval receipt** showing
the piece, its propagation, and the construction assessment required by §2 above.

**The gate opens when steps 2-4 are demonstrably done.**

---

## 6 · WHAT THIS RULE IS NOT

- It is not *"never fix quickly"*. A typo is a typo.
- It applies when the piece **has declared dependents** — that is what `rule-lanes.md` detects.
- It does not forbid choosing a different route. Brian: *"si se tiene que pensar o hacerlo por otro
  medio, está bien."*

---

Related: `rule-lanes.md` · `contract-block.md` §C/§F · `case-dangerous-default.md` ·
`principles/owner-2-dev.md` · architecture §7 · §12-T.2 (the receipt).
