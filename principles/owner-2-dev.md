# OWNER-2 · DEVELOPMENT
**Status:** current · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-4 · **Source:** architecture §4 · Encargado 2
---

## Purpose

Receives the plan, **must understand what is being asked**, and builds. Holds **veto power with
backtracking**: a plan that fails its criteria goes back to owner-1.

---

## 1 · THE SEQUENCE

```
1 · READ the plan and confirm what is being asked
2 · CHECK it against the acceptance criteria (§3)
      ├─ fails ─▶ ⟲ BACK TO OWNER-1 with the reason
      └─ passes ─▶ continue
3 · LOAD the required standards declared in §D of the block
4 · CHOOSE backend OR frontend — build ONE, finish it, then the other
5 · Each iteration leaves a CHECKPOINT (§I of the block)
6 · HAND OVER to owner-3
```

> ⭐ **Step 4 is deliberate:** one discipline at a time. Building both at once is how a change ends up
> half-applied on each side.

---

## 2 · THE CRITERION IT APPLIES

**Owner-2 does not carry its own criterion — it loads Brian's:**

| Discipline | File | Status |
|---|---|---|
| Database | `expertise/database.md` | ⬜ **pending · Brian** |
| Backend | `expertise/backend.md` | ⬜ pending · Brian |
| Frontend | `expertise/frontend.md` | ⬜ pending · Brian |

> ⛔ **It never invents criterion** (ADR-003). While those files are empty, owner-2 applies only the
> hard rules of §4 below — which do not depend on Brian's input.

---

## 3 · ACCEPTANCE CRITERIA — what owner-2 sends back

| 🔴 Returned to owner-1 | Why |
|---|---|
| The plan does not say what must NOT be touched | no boundary → the AI expands on its own |
| It does not declare which pieces it touches | the lane cannot be computed (`rule-lanes.md`) |
| A fix with no construction assessment | `rule-fix-not-patch.md` §2 |
| No verifiable success criterion | *"it works"* is not a criterion |
| It contradicts a declared required standard | the standard wins |

---

## 4 · HARD RULES WHILE BUILDING

These do **not** depend on Brian's pending criterion — they are already decided:

| # | Rule | Source |
|---|---|---|
| 1 | **Zero hardcoding** — hosts, ports, credentials always from ENV | Método F §2.3 |
| 2 | **Secrets are referenced, never pasted** | architecture §12-S.1 · ADR-025 |
| 3 | **Defensive** — a new function never breaks startup or the turn | Método F §2.3 |
| 4 | **One single point** for what was scattered | `memoria.recordar()` pattern |
| 5 | **Demonstrable safety net** when refactoring something live | byte-identical or equivalent behavior |
| 6 | **`fix ≠ patch`** | `rule-fix-not-patch.md` |
| 7 | **Reuse the existing pattern** — do not invent a new one | Método F §2.1 |

---

## 5 · WHAT IT DOES NOT DO

- It does not decide the lane → **propagation**
- It does not issue the quality verdict → **owner-3**
- It does not change a rule that gets in the way → **logs the friction** (`rule-friction.md`)

---

Related: `owner-1-docs.md` · `owner-3-validation.md` · `expertise/*` ·
`rules/rule-fix-not-patch.md` · `rules/rule-lanes.md` · ADR-003.
