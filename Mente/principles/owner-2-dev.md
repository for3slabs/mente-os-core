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
| Database | `expertise/dev-database.md` | ✅ **FILLED 2026-08-05** — phase F1 closed |
| Backend | `expertise/dev-backend.md` | ✅ **FILLED 2026-08-05** (§4-BIS is imported material, separate from his criterion) |
| Frontend | `expertise/dev-frontend.md` | ✅ **FILLED 2026-08-05** |

> ⭐ **`principles/expertise/dev-database.md` is live since 2026-08-05.** What owner-2 can now demand before code is
> written: **five categories that never live in code** (anything with an owner · anything that
> changes without deploying · fixed lists · thresholds · sensitive user data — env vars are for
> wiring, never content) · **four impossible states** the schema must forbid *by constraint, not by
> an `if`* · **a foreign key on every real relation, no exceptions** · **four conditions before a
> migration touches production**.
>
> ⚠️ **And its root reverses the review order:** a table is judged **against its implementation
> plan**, not against best practices. No plan backing it → 🔴 even if every mechanical check passes.

> ## ⭐ 2026-08-05 — OWNER-2 IS FULLY COVERED. All three disciplines carry Brian's criterion.
>
> ⛔ It still never invents criterion (ADR-003) — it now **loads** it instead of falling back to §4
> alone. What each discipline adds on top of the hard rules below: **database** — five categories
> out of code, four impossible states enforced by constraint, FK always · **backend** — one guard
> per rule, expected failures ARE the contract, security/money unified always · **frontend** — the
> server owns the state and React reflects it, a control must never lie, nothing unreconstructable
> lives only in memory.

### ⭐ These three are BRANCHES of owner-2, not owners themselves

> **Brian, 2026-07-31, correcting the AI:** *"los expertise eran formato de documentación,
> desarrollador, validación de flujo funcional. Los 3 que pusiste van DENTRO de desarrollador —
> es una división como si fuera un árbol."*

```
SEED (the three owners)              ROOTS (their disciplines)

owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration
```

**The error being corrected:** the AI presented database/backend/frontend at the *same level* as
the owners. They are not. They are owner-2's disciplines — architecture §9.2 says it plainly:
*"El **Encargado 2** necesita estándares por disciplina."*

**Why the distinction matters:** owners are the **sequence** (who acts, in what order, with what
veto). Disciplines are the **subject matter** (what each field demands). Flattening them makes it
look like "database" could return a plan to owner-1, which it cannot — only owner-2 can.

**The `<owner>-<discipline>` filename prefix exists so the tree is visible in `ls`.** A flat list
of seven files hides which owner each one answers to — which is exactly how the confusion started.

---

## 3 · ACCEPTANCE CRITERIA — what owner-2 sends back

| 🔴 Returned to owner-1 | Why |
|---|---|
| The plan does not say what must NOT be touched | no boundary → the AI expands on its own |
| It does not declare which pieces it touches | the lane cannot be computed (`rules/rule-lanes.md`) |
| A fix with no construction assessment | `rules/rule-fix-not-patch.md` §2 |
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
| 6 | **`fix ≠ patch`** | `rules/rule-fix-not-patch.md` |
| 7 | **Reuse the existing pattern** — do not invent a new one | Método F §2.1 |

---

## 5 · WHAT IT DOES NOT DO

- It does not decide the lane → **propagation**
- It does not issue the quality verdict → **owner-3**
- It does not change a rule that gets in the way → **logs the friction** (`rules/rule-friction.md`)

---

Related: `owner-1-docs.md` · `owner-3-validation.md` · `expertise/*` ·
`rules/rule-fix-not-patch.md` · `rules/rule-lanes.md` · ADR-003.
