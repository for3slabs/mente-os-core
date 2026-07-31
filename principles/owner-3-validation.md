# OWNER-3 · VALIDATION
**Status:** current · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-4 · **Source:** architecture §4 · Encargado 3
---

## Purpose

Verifies the **whole behavior of the block: that nothing is left dangling.** Last in the cycle, and
the only one that can refuse to close a block.

---

## 1 · ⭐ THE MASTER RULE

> ## 🚫 It does not declare "this is fine." It REPORTS THE MEASUREMENT.

**The precedent that forces this** — same code, opposite verdicts, 9 minutes apart:

| When | What was said |
|---|---|
| 26-jul 06:24 | *"tiene el estado completo para retomar sin perder nada"* |
| **26-jul 06:33** (after a `/clear`) | *"lo que está mal es que este archivo lo implementa a medias"* |

**A verdict that changes with context is not a verdict. It is a mood.**

---

## 1-bis · ⭐ ITS DISCIPLINES — the roots of this owner

**Owner-3 does not carry its own criterion — it loads Brian's**, exactly as owner-2 does:

| Discipline | File | Status |
|---|---|---|
| Functional — does this piece actually work? | `expertise/val-functional.md` | ⬜ **pending · Brian** |
| Integration — does the chain still work? | `expertise/val-integration.md` | ⬜ **pending · Brian** |

```
SEED (the three owners)              ROOTS (their disciplines)

owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration   ⬅ THIS OWNER
```

> **Brian, 2026-07-31:** *"es una división como si fuera un árbol — la semilla son formato de
> documentación, desarrollador, validación de flujo funcional, y a partir de ellos salen raíces."*

**Why these two and not one:** `val-functional` asks *"does this piece work?"*; `val-integration`
asks *"does the chain still work when every piece works?"* Every piece can pass its own test and
the flow still be broken — Brian, 2026-07-20: *"los bugs trágicos viven ENTRE las piezas."*

⛔ **It never invents criterion** (ADR-003). While those files are empty, owner-3 applies the
§5-BIS battery (§4) and layer 1 of the verdict (§3) — neither depends on Brian's input.

---

## 2 · THE THREE CLOSING CRITERIA — none optional

| # | Criterion | Question |
|---|---|---|
| 1 | **Functional** | does what exists **work and stay connected**? nothing dangling? |
| 2 | **Sufficiency** | do sections **A-E** suffice to restart safely? |
| 3 | **Quality verdict** | layer 1 measured + layer 2 criterion |

### What each failure means

| Fails | Consequence |
|---|---|
| 1 · functional | 🔴 **does not close.** Something is broken |
| 2 · sufficiency | 🔴 **does not close, even if the code works** — the next session would start blind |
| 3 · quality | 🟡 **may close, but marked MVP with its debt listed** |

> ⭐ **Criterion 2 is the one nobody had.** A block that closes without it means the next session
> rebuilds the scope by inference — and that is *"no, así no iba"*.

---

## 3 · THE QUALITY VERDICT — two layers

**Layer 1 · measurable** (`bin/grade-block`) — does not depend on Brian's pending criterion:
dead code · exports never imported · duplicated blocks · files touched with no test · undeclared
dependents · import cycles · critical-path coverage.

**Layer 2 · criterion** (`rules/qa-dimensions.md`) — 6 dimensions, each with **required evidence**:
architecture · data design · abstraction · naming · contracts · **necessity**.

> ⛔ **A dimension is not answered by asserting it.** It is answered by showing the evidence.
> An answer without evidence does not count — that is what stops the AI from self-approving.

**Combined:** 🟢 product (both green) · 🟡 close · 🔴 MVP.

---

## 4 · ⭐ THE §5-BIS BATTERY — inherited from the Método F, not reinvented

> **Brian's hard rule (Método F §2.4):** *"no basta probar el carril; hay que verificar que TODO sigue
> conectado."*

**This battery already existed in v1 and v2 must not lose it.** It is criterion 1 (functional) made
concrete. **Seven checks — no phase closes without all of them.**

| # | Check | What it means |
|---|---|---|
| **A** | **Base suite** | `pytest -q` + `ruff check` + `ruff format --check` + `ty` (gate) + Hypothesis |
| **B** | **Real startup** | rebuild + `docker compose up` + read the logs ("cerebro conectado", "MCP conectado", "Application started", guardián OK). **The import passing is not enough — the real startup is** |
| **C** | **`/salud` complete** | every subsystem E2E → **0 FAIL** or the phase does not close |
| **D** | **Memory in depth** | write→embed→retrieve by meaning→graph→cascade + **RECONNECTION test** (restart a sibling, run the flow again, confirm it reconnects from ENV and not from a hardcoded host) |
| **E** | **Every H** | walk the milestones (H4-H12 + AC + execute_code + P1) with a **real action/datum**, not just the subsystem that was touched. A change in the center can disconnect anything |
| **F** | **Tools** | every tool invoked with a real test (MCP with a real handshake, not a bare GET) |
| **G** | **What the phase itself added** | the new functionality end-to-end, **with a real LLM** when it applies — unit tests do not exercise the actual prompt or behavior |

### ⭐ AFFIRMATIVE VERIFICATION — the rule that makes the battery worth anything

> Every check confirms with **a datum**: *"recovered X"* · *"vector = 1024 dims"* ·
> *"cron_corridas with today's timestamp"* · *"21 tools"*.
> **Never** *"seems fine"* · *"it should work"* · *"more or less".*

**"More or less connected" is the declared enemy** (Método F §2.2). When something *almost* works →
**stop and investigate.**

### How it relates to the three closing criteria

| Criterion | Covered by |
|---|---|
| 1 · **Functional** | ⭐ **this battery, §4 A-G** |
| 2 · Sufficiency | §2 |
| 3 · Quality verdict | §3 |

> ⚠️ **Scope note:** checks B-F assume the For3s OS agent (containers, `/salud`, memory, MCP).
> For a block that only touches documents or the web demo, the applicable subset is declared in the
> block's §D. **What is never optional is affirmative verification.**

---

## 5 · THE CLOSING PROCEDURE — 8 fixed steps

```
1 · CONSOLIDATE §J Context      → curated to ≤80 lines (long detail → docs/)
2 · CURATE §G Decisions         → each with its rationale
3 · RESOLVE §H Friction         → escalate to Brian as proposals
4 · VERIFY SUFFICIENCY          → ⭐ do A-E suffice?  NO ─▶ does not close
5 · WRITE the summary           → what was done · what was learned
6 · DECLARE connections         → which blocks are affected
7 · ARCHIVE                     → blocks/archive/<name>-<YYYY-MM>/
8 · REGENERATE index and states → 🤖 automatic, never by hand
```

> **Hard rule: consolidate BEFORE closing, not after.** A close that depends on someone remembering
> at the end is the close that already failed 5 of 11 times.

---

## 6 · WHAT IT DOES NOT DO

- It does not judge the plan → **owner-1**
- It does not write code → **owner-2**
- It does not invent the QA dimensions → **Brian** (ADR-014)
- It does not delete forensic evidence → the `.jsonl` files are never touched

---

Related: `owner-1-docs.md` · `owner-2-dev.md` · `rules/qa-dimensions.md` ·
`rules/contract-block.md` §K · `bin/grade-block` · ADR-013 · ADR-014.
