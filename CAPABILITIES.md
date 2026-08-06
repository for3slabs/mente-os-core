# CAPABILITIES — what the agent can do inside Mente OS, and where the line is

**Status:** current · **Type:** entry-point · **Updated:** 2026-08-05 · **Owner:** brian
**Level:** 🔧 ENGINE — ships with the engine · describes it · carries no instance data
**Verified by:** `bin/test-f0-f6` (§CAPABILITIES) · **Block:** `blocks/archive/distribucion_2026-08` §F-5

## Purpose

**You are an agent working inside a Mente OS instance.** This file tells you what the engine can
do for you, and which half of the tree you may write to. It is the answer to two questions no
other document answers: *what can I run?* and *what may I change?*

> ⭐ **This is not documentation — it is correctness.** An agent that does not know
> `bin/grade-block` exists will hand-write a product/MVP verdict. That is **inventing criterion**,
> which `rules/decisions/ADR-003-brian-owns-the-criterion.md` forbids. The whole quality layer
> exists to prevent exactly that, and it only works if you know it is there.

---

## 1 · ⛔ THE LINE — instance is yours, engine is not

```
📦 INSTANCE — you fill this in, as the work advances
   mente.config.yml · blocks/ · memory/ · docs/ · work/ · vision/ · Cerebro/
   CLAUDE.md · PROJECT-RULES.md          (generated for THIS user)

🔧 ENGINE — you run it, you do not rewrite it
   bin/ · hooks/ · rules/ · principles/ · CAPABILITIES.md
```

**Why the asymmetry is the product:** the instance half must stay writable — that is where the
user's work lives and grows. The engine half is what makes the guarantees true. An agent that
edits a validator to make its own output pass has removed the only thing that was checking it.

| If you want to… | Do NOT | Instead |
|---|---|---|
| change a threshold | edit `bin/*` | edit `mente.config.yml` |
| silence a check | edit the validator | fix what it reports, or record the exception where the rule says |
| add a project rule | edit `rules/*` | `PROJECT-RULES.md` (project) or `BLOCK.md` §B (this work only) |
| change a decision | edit an accepted ADR | write a new ADR that supersedes it (`rules/contract-adr.md` rule 3) |

> 🔒 Editing `bin/` or `hooks/` is gated — the harness asks before letting it through. **The gate
> is not an obstacle to route around.** If a change to the engine is genuinely needed, say so and
> let the owner decide.

---

## 2 · WHAT YOU CAN RUN — the validators
<!-- No count in this heading on purpose: it read "15 validators" while bin/ held 16 executables
     (2026-08-05). A number copied into prose is correct exactly once — docs/METRICS.md
     (`validators`) is the measured one. Same defect this file warns about three sections below. -->


Every one exits with a code you can act on. **Never re-implement by hand what one of these
measures** — that is how a measured verdict becomes an opinion.

### The question each one answers

| Run this | To answer | Exit |
|---|---|---|
| `bin/check-health` | *is anything wrong right now?* — runs itself at session start | 0 clean · 1 warn · 2 error |
| `bin/check-blocks` | *do documents, blocks and ADRs satisfy their contracts?* | 0 · 1 warn · 2 error |
| `bin/check-links` | *does every citation resolve?* | 0 · 1 something points nowhere |
| `bin/check-structure` | *is the folder tree the one the design declared?* | 0 · 1 warn · 2 missing |
| `bin/check-sufficiency <block>` | *can this block restart from disk alone?* | 0 sufficient · 2 not |
| `bin/check-applied <block>` | *were the declared standards actually applied?* | 0 · 1 not |
| `bin/check-clear-ready` | *is it safe to `/clear` right now?* | 0 safe · 1 something would be lost |
| `bin/flag-stale` | *which blocks stopped moving?* | 0 · 1 warn · 2 error |
| `bin/verify-handoff <file>` | *is this delegation actually bounded?* | 0 bounded · 2 malformed |
| ⭐ `bin/grade-block <block>` | **product or MVP — MEASURED, never an opinion** (this is LAYER 1) | 0 product · 1 close · 2 MVP |

> ## ⭐ THE VERDICT HAS TWO LAYERS — and layer 2 is NOT a script
>
> `grade-block` measures what a machine can (dead code, links, duplication, tests). **Layer 2 is
> `rules/qa-dimensions.md`: six dimensions carrying Brian's criterion, LIVE since 2026-08-05.**
> It is applied by reading, at block close, and **each dimension demands EVIDENCE SHOWN, never
> asserted**. Per discipline it is refined by `principles/expertise/*`.
>
> | Owner | Disciplines | State |
> |---|---|---|
> | owner-2 · development | `dev-database` · `dev-backend` · `dev-frontend` | ✅ **fully covered** |
> | owner-3 · functional-flow | `val-functional` · `val-integration` | ✅ **fully covered** |
> | owner-1 · documentation | `doc-planning` · `doc-structure` | ⬜ still Brian's to write |
>
> ⚠️ **A discipline file adds demands on top of the six dimensions, never relaxes them**
> (`rules/rule-inheritance.md`). Where both speak, **the stricter one wins.**
>
> ⛔ **Do not hand-write a criterion verdict.** Run layer 1, then walk the six dimensions with their
> evidence. A dimension answered without evidence does not count — that is the rule that stops the
> AI from approving its own work (ADR-003).
>
> **Combined:** 🟢 product (both green) · 🟡 close · 🔴 MVP. A 🔴 does not forbid closing the block;
> it forbids closing it **as a product**.

### The ones that WRITE

| Run this | It produces |
|---|---|
| `bin/new-block <name> --type code\|docs\|infra\|data` | a block scaffold from the contract |
| `bin/generate-index` | 🤖 `docs/INDEX.md` + `docs/STATES.md` from what is on disk |
| `bin/generate-metrics` | 🤖 `docs/METRICS.md` — **every live number, measured once** |
| `bin/migrate-doc <src> <dst>` | moves ONE document safely (`--dry-run` first) |
| `bin/init` | a NEW instance: reads `mente.config.yml` → generates `CLAUDE.md`, `PROJECT-RULES.md` and the 4 portable hook paths. **Run once, by whoever clones the engine** |
| `bin/test-f0-f6` | the whole system end to end — **what matters is `failed: 0`** |

> 🔴 **Never type a live number into prose.** Run `generate-metrics` and cite the metric name:
> ⛔ *"the battery is 151/151"* → ✅ *"green — count in `docs/METRICS.md` (`battery.checks`)"*.
> A number copied by hand is correct exactly once.

---

## 3 · WHAT RUNS WITHOUT YOU — 3 gates + 1 injection

You do not call these. They fire on their own, and two of them **refuse**.

| When | What | Blocks? |
|---|---|---|
| session start | `hooks/session-start.sh` — health, structure, drifting blocks | ⛔ never |
| before an edit | `hooks/pre-edit-standards.py` — injects the owning block's §D | ⛔ never |
| before an edit | `hooks/gate-critical.py` — DB with no rollback · closing an insufficient block | 🔴 **exit 2** |
| before an edit | `hooks/gate-handoff.py` — a writing sub-agent with no declared scope | 🔴 **exit 2** |
| before touching `secrets/` | `hooks/gate-secrets.py` — 🔑 reading with a live lease · ⛔ writing ALWAYS asks | **ask/allow** |
| when the context loads | `bin/secrets-lease open` — issues the secrets lease (SessionStart + PostCompact) | grants |
| before a commit | `hooks/pre-commit.sh` — a block violating its contract | 🔴 **BLOCKS** |

**When a gate blocks, its message IS the receipt** (`ADR-030`): the piece, why it is
irreversible, what to assess, and the documented way out. Read it — do not retry blind.

---

## 4 · THE FIVE RULES YOU WILL HIT FIRST

| Rule | In one line |
|---|---|
| `ADR-003` the owner owns the criterion | measure, or ask — **never invent** a verdict or a threshold |
| `rules/rule-fix-not-patch.md` | before fixing: *why does this failure exist, and **where else does it live**?* |
| `rules/rule-lanes.md` | the lane comes from the dependency **graph**, never from your estimate |
| `rules/rule-checks-must-measure.md` | a check you have only seen GREEN has not been tested |
| `rules/rule-session-close.md` | no `/clear` without registering the session first |
| 🚢 `rules/rule-shipping-flow.md` | branch → verify → PR → **⛔ do not merge.** Transversal: backend, frontend, database and docs alike. Declare it in the block's §D so the hook hands it to you |

Full map of which rule applies at which level: `CLAUDE.md` → `PROJECT-RULES.md` → `BLOCK.md` §B.

### Where the machine you are on is described

**`docs/WORKSPACE.md`** — which repo is which · what is gated and why · **where** each credential
lives · which command answers which question · what runs by itself.
⛔ It carries **no values**: it says WHERE a secret lives, never WHAT it is. Read it instead of
re-deriving the layout every session — re-derivation is where a wrong assumption enters.

---

## 5 · THE LOOP — how work actually moves

```
1 · read memory/RETOMAR.md            ← ~90% of the time this is enough
2 · block open?  → load its §A-E      ← if §A-E do not suffice, SAY SO, do not infer
3 · new work?    → bin/new-block <name> --type <t>   then fill §A §B §C §D
4 · work         → the hooks inject and gate as you go
5 · verify       → bin/check-blocks · bin/check-sufficiency · bin/grade-block
6 · closing?     → run bin/check-clear-ready and register the session first
```

> ⚠️ **`§B Scope OUT` is the owner's call** — unless every limit **derives** from an existing rule,
> in which case you write it and cite the source on each line. A `⬜ PENDING` hole you could have
> filled from the repo is unfinished work handed over as if it were a decision
> (`rules/block-lifecycle.md` §1).

---

Related: `CLAUDE.md` (the router that sends you here) · `PROJECT-RULES.md` (this project's rules) ·
`rules/block-lifecycle.md` (opening and closing) · `docs/METRICS.md` (every live
number) · `mente.config.yml` (the one file an instance edits).
