# RULE · LANES
**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-3 · **Source:** architecture §5 · ADR-004
---

## Purpose

Decide how much process a piece of work goes through. Three lanes, and **the lane is chosen by
PROPAGATION — never by the AI's judgment.**

---

## 1 · THE THREE LANES

| Lane | When | Path |
|---|---|---|
| `direct` | trivial change: a string, a color, a typo | **validation only** |
| `task` | one loose sub-block, no new design | **owner-2 → owner-3** |
| `full-block` | something new, or it touches several pieces | **owner-1 → owner-2 → owner-3**, with backtracking |

---

## 2 · ⭐ HOW THE LANE IS CHOSEN — not by judgment

```
Does the target have DECLARED DEPENDENTS in the graph?
        │
   YES ─┴─▶ full-block                    (no discussion)
        │
    NO ─┴─▶ new design needed?
              YES ─▶ task
               NO ─▶ direct
```

**The decision comes from the graph, not from an estimate.**

> ⭐ **This is the whole point of the rule.** It prevents the AI from declaring something trivial and
> being wrong — which is exactly how `userStore.ts` got edited 21 times.

---

## 3 · THE CASE THAT PROVES IT

| Request | Looks like | Actually is |
|---|---|---|
| *"guarda la API key en la instancia real, no en el kind de la cookie"* | a task | 🔴 **full-block** |

`lib/demo/userStore.ts` had **5 declared dependents**. Treated as a task, one file was fixed — and
four commits later came *"barrido completo del patrón cookie kind ≠ instancia real"*.

**Measured:** 25 of 60 commits were fixes (42%) · `userStore.ts` edited 21 times.

---

## 4 · EXAMPLES

| Request | Lane | Why |
|---|---|---|
| *"change the button text"* | `direct` | no declared dependents |
| *"the quota error message is unclear"* | `direct` | string, no logic |
| *"add try/catch to this isolated function"* | `task` | no dependents |
| *"add a `name` column to demo_users"* | 🔴 `full-block` | touches the DB → propagates to every reader |
| *"connect a payment provider"* | 🔴 `full-block` | new piece + external integration |

---

## 5 · WHY THREE AND NOT ONE

If every task went through all three owners, **the system becomes unbearable and gets abandoned** —
and an abandoned standard protects nothing. That is the Método F failure mode: strict, and unread in
2 of 5 sessions.

---

Related: `contract-block.md` §A (`lane` field) · `rule-fix-not-patch.md` · `principles/owner-2-dev.md` ·
ADR-004.
