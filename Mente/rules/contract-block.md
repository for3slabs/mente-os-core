# CONTRACT · BLOCK.md
**Status:** current · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
**Applies to:** every file at `blocks/active/<name>/BLOCK.md`
**Verified by:** `bin/check-blocks` · **Source design:** architecture §3.2-TER
---

## 0 · THE SHAPE

**One block = ONE file.** Sections A-K in this order. Max **200 lines** total.
*(Raised from 150 on 2026-08-05, by Brian. A closed block carries §K — the verdict, what was
learned, what debt it did not close — on top of everything the open block already held; the first
real close landed at 169. The ceiling was sized for open blocks only.)*

> Tiers are the **order of sections inside this file**, not separate files (ADR-009).
> Splitting 70 lines across files saves nothing and adds places that desynchronize.

**Completeness regime — progressive with a hard minimum** (ADR-010):

| Moment | Required |
|---|---|
| **OPEN** | A · B · C · D — **four fields, ~2 minutes** |
| **While working** | E through J, filled as they become known |
| **CLOSE** | everything + the sufficiency check |

> **Cheap to open, expensive to close.** If opening costs ten fields, work happens *without* a block
> and everything is lost.

---

## 1 · THE SECTIONS

| § | Section | Required | Limit | Tier |
|---|---|---|---|---|
| **A** | `Identity` | 🔴 OPEN | 5 lines | 1 |
| **B** | `Scope` — IN / OUT | 🔴 OPEN | 15 lines | 1 |
| **C** | `Connections` | 🔴 OPEN | 10 lines | 1 |
| **D** | `Required standards` | 🔴 OPEN | 8 lines | 1 |
| **E** | `State` | 🟡 working | **10 lines** | 1 |
| **F** | `Sub-blocks` | 🟡 working | 20 rows | 2 |
| **G** | `Decisions` | 🟡 working | — | 2 |
| **H** | `Friction log` | 🟡 working | — | 2 |
| **I** | `Checkpoints` | 🟡 working | — | 3 |
| **J** | `Context` | 🟡 working | **80 (target 50)** | 3 |
| **K** | `Closing` | 🔴 CLOSE | — | — |

---

## 2 · FIELD BY FIELD

### A · Identity — 🔴 required to open

```markdown
id: blk-<name>-<YYYY-MM>
type: code | docs | infra | data
intent: one sentence — what this block is for
status: active | blocked | closed
lane: direct | task | full-block
owner: <person>
created: YYYY-MM-DD · updated: YYYY-MM-DD
```

| Field | Rule |
|---|---|
| `id` | **globally unique.** Resolution is exact — no match means **stop and ask** (ADR-011) |
| `type` | ⭐ decides **which metrics are measured** — see below. Required (ADR-028) |
| `intent` | one sentence. If you cannot write it, you do not know what you are doing yet |
| `status` | exactly one of the three |
| `lane` | set by **propagation**, not by judgment (`rule-lanes.md`) |
| `updated` | ISO date. Stale after 7 days → `bin/flag-stale` |

#### ⭐ `type` — because a validator that measures the wrong thing teaches you to ignore it

> **Brian, 2026-07-30:** *"solo está para demo o para todo el sistema, porque lo vamos a ocupar en
> todo el sistema."*

`bin/grade-block` measures code: tests, importers, duplication. Run it on a **documentation** block
and it reports 0 tests and 0 importers — **🔴 MVP forever, for measuring what does not apply.**

Measured 2026-07-30 against Brian's own pending list: `renombrar los 208 archivos` and
`decidir el hosting` would both score 🔴 permanently. **A validator that cannot ever go green is a
validator you learn to ignore** — and then the doctrine is back to being a document.

| `type` | Metrics that apply | Metrics NOT measured (and reported as `n/a`) |
|---|---|---|
| `code` | dead files · dead exports · duplication · tests · import cycles · stale §F counts | — |
| `docs` | broken links · orphan docs (nothing points at them) · size limits · stale `Updated` | tests · imports · duplication |
| `infra` | runbook exists · rollback documented · secrets referenced not pasted | everything code-shaped |
| `data` | migration is reversible · schema documented · FKs declared | tests · duplication |

**Two hard rules:**

1. ⛔ **`n/a` is never a 🟢.** A metric that does not apply prints `n/a` **with the reason**. Silence
   would let a `docs` block look like it passed a test check it never ran.
2. ⛔ **The type does not lower the bar, it changes the ruler.** A `docs` block still has to reach a
   verdict — it just reaches it with link and orphan checks instead of tests.

> **Mixed blocks:** a block that is genuinely half code and half docs is **two blocks**
> (`block-lifecycle.md` §2 — they would not close on the same day for the same reason).

### B · Scope — 🔴 required to open · ⭐ the critical one

```markdown
## ✅ IN
- <paths, systems, tables this block may touch>

## ⛔ OUT
- DO NOT <what is explicitly out of bounds, and why>
```

**Both lists must be non-empty.** An empty `OUT` is a block with no boundary.

#### ⭐ TWO LEVELS — the block does NOT own system-wide rules

> **Brian's question, 2026-07-29:** *"¿el bloque tiene esas 4 reglas, o el sistema general que
> gobierna por encima de los bloques las tiene?"* — **the system has them.** The block was
> repeating them, which made it look like their source.

| Level | Where it lives | Applies |
|---|---|---|
| 🌐 **System-wide** | `CLAUDE.md` · `base-rules.md` · `settings.local.json` deny | **always** — with or without a block |
| 📦 **Block-specific** | §B `OUT` of the block | **only while this block is open** |

**Full model:** `rules/rule-inheritance.md` — three levels (universal → project → block) with
inheritance that **only restricts, never relaxes**.

**The test:** *would this limit still hold if this block did not exist?*
**Yes → system-wide.** Do not repeat it in `OUT`; inherit it.
**No → block-specific.** It belongs in `OUT`.

Measured on the first real block: of 4 limits written in `OUT`, **2 were system-wide**
(`marca-personal/Mente` from `CLAUDE.md:24`, server-first from `base-rules.md` #7) and only
**2 were actually this block's** (the agent's repo, `api_channel.py`).

> ⚠️ **Why repeating them is harmful, not just redundant:** if a system rule changes in `CLAUDE.md`,
> every block that copied it now carries a stale version — and nothing detects the divergence.
> **It is the same failure as the decisions table that lived in two documents and diverged.**
>
> A block MAY list inherited rules under a clearly separate heading (`🌐 System-wide rules that
> also apply`) **as a reading aid** — never as its own `OUT`.

#### Every OUT line states WHERE it comes from — and how strongly

| Marker | Meaning | Example |
|---|---|---|
| a file path + line | **written rule** — quote its source | `CLAUDE.md:24` · `base-rules.md #7` |
| `deny in settings…` | **technical lock** — enforced by the harness | the strongest kind |
| **`DERIVED:`** | ⭐ **the AI's reasoning from a rule** — say so explicitly | *"it lives in another repo, so by the §2 test…"* |
| nothing | 🔴 **not allowed** — an unsourced limit is an opinion | — |

> ⭐ **`DERIVED:` exists because of a real slip (2026-07-29):** an OUT line cited
> `block-lifecycle.md §2` as if that section said it. §2 gives the *test*; the conclusion was the
> AI's. **Presenting your own reasoning as a written rule is exactly what `owner-0-voice.md` §2.7
> bans.** Reasoning is fine — it just has to be labeled as reasoning.

> ⭐ **Why this is the most important field in the contract:** it is the half that does not exist
> anywhere today, and the direct cause of *"no, así no iba"*. Without a declared boundary the AI
> **rebuilds the scope by inference when context dies — and sounds equally confident.**

### C · Connections — 🔴 required to open

```markdown
## Connections
- DEPENDS ON: blk-<id> (why)
- DEPENDED ON BY: blk-<id>
- ISOLATED FROM: blk-<id>
- 🔴 CRITICAL PIECE: <path> → propagates to N files
```

Every `blk-<id>` cited **must exist**. `CRITICAL PIECE` is what forces the lane up to `full-block`.

### D · Required standards — 🔴 required to open

```markdown
## Required standards
- principles/expertise/<discipline>.md
- rules/rule-<name>.md
- rules/case-<name>.md
```

Every path must exist. **This is layer B of the reading guarantee** (architecture §12-QUATER): the
standard travels *with the work* instead of sitting in a general index nobody opens.

> **This field is why the Método F failed.** It existed, it was findable, and it went unread in 2 of
> 5 sessions. Declared here, the hook injects it before editing.

### E · State — 🟡 · **10 lines max**

```markdown
## State
phase: <where the work is>
next: <the immediate next step>
blockers: <what stops it, or "none">
progress: N/M sub-blocks closed
updated: YYYY-MM-DD
```

The operational heartbeat. Together with A-D it forms **Tier 1** — the sufficiency test.

### F · Sub-blocks — 🟡

```markdown
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | <what> | <path> | N | open/closed/blocked |
```

**`dependents` is not decorative** — it is the propagation graph, and it decides the lane.
The parent block **cannot close** while any sub-block is open.

#### ⭐ The graph is MEASURED, never written from memory

> **Brian, 2026-07-29:** *"debe de ser dinámico y acoplarse a la situación — ya en la práctica no
> importa si son 5 o 14."*

| Rule | Why |
|---|---|
| **Measure with `bin/new-block --piece <path>`** | the count changes as the code changes |
| **The field records WHEN it was measured** | `→ 16 dependents (measured 2026-07-29)` |
| **Re-measure before deciding a lane** | a stale graph picks the wrong lane |
| ⛔ **Never copy a number from a previous block or document** | that is how the design said 5 when reality was 16 |

**Measured proof of why this matters** — the same piece, three answers on the same day:

| Source | `userStore.ts` dependents |
|---|---|
| The architecture example, written from memory | **5** |
| First automated run, counting `.next/` build artifacts | **38** |
| Real measurement, excluding build output | **16** |

> **Build artifacts and vendored code are not dependents: they are copies.** `new-block` excludes
> `.next/` `node_modules/` `dist/` `build/` `__pycache__` `.venv` `coverage`.
> **A number nobody can reproduce is not evidence.**

### G · Decisions — 🟡 · **each one with its rationale**

```markdown
- YYYY-MM-DD · <what was decided>.
  Rationale: <why this and not the alternative>
```

**A decision without a rationale does not count.** This is the *why* that dies with `/clear` today.

> If the decision affects the system (not just this block), it also needs an ADR
> (`rules/contract-adr.md`).

### H · Friction log — 🟡

```markdown
- YYYY-MM-DD · rule: <name> · block: <id> · reason: <why it got in the way>
```

Four fixed fields. Three frictions with the same rule **in distinct blocks** → escalates to Brian
(`rule-friction.md`, ADR-022).

### I · Checkpoints — 🟡

```markdown
- YYYY-MM-DD · <commit> · <what it saved>
```

### J · Context — 🟡 · **80 lines (target 50) · CURATED, not a log**

Durable context only. **Long chronology goes to `docs/`**, never here.
Consolidate **before** closing the session, not after.

### K · Closing — 🔴 required to close

```markdown
## Closing
closed: YYYY-MM-DD
summary: <what was done, what was learned>
connections affected: <blocks that inherit something>
quality verdict: <the measured table — see rules/qa-dimensions.md>
sufficiency: pass | fail
```

---

## 3 · WHAT NEVER GOES IN THIS FILE

| Not here | Goes in | Why |
|---|---|---|
| Chronologies, session logs | `docs/` of the block | they grow without bound |
| The **content** of a standard | `principles/` · `rules/` | **point at it, never copy it** |
| Code, diffs | the repo | the block describes, it does not duplicate |
| Another block's state | that block | isolation (`rule-isolation.md`) |

---

## 4 · WHAT `bin/check-blocks` VERIFIES

```
🔴 STRUCTURE
   · missing section A, B, C or D
   · Scope with an empty IN or OUT list
   · id missing, or duplicated across blocks
   · a cited blk-<id> that does not exist
   · a Required standards path that does not exist

🔴 CLOSING
   · status: closed without section K
   · sufficiency: fail  → the block does not close
   · an open sub-block in a block being closed

🟡 LIMITS
   · BLOCK.md over 200 lines
   · State over 10 lines
   · Context over 80 lines
   · nesting deeper than 3 levels (ADR-015)

🟡 FRESHNESS
   · updated older than 7 days while status: active
```

---

## 5 · THE SUFFICIENCY TEST — the one that decides

> ## Do sections A-E suffice to restart the work safely?

**~60 lines.** They must answer: what is being built · what must NOT be touched · what it depends on ·
under which criterion · what phase it is in · what blocks it.

| Result | Consequence |
|---|---|
| ✅ yes | the block is well written |
| 🔴 no | **the block does not close, even if the code works** |

> Without this test, writing to disk is **accumulating**, not owning the context. It is what turns
> *"being owner of the context"* into something measurable instead of declarative.

---

Related: `contract-document.md` · `rule-lanes.md` · `rule-fix-not-patch.md` · `rule-friction.md` ·
`rule-isolation.md` · `qa-dimensions.md` · `NAMING_CONVENTION.md` ·
ADR-009 (single file) · ADR-010 (progressive) · ADR-011 (reading guarantee) · ADR-015 (nesting).

ADR: `decisions/ADR-028-block-type-decides-metrics.md` (the `type` field) · Implements ADR-006 (blocks live in git — versioned, revertible) · ADR-007 (a closed block is ARCHIVED, never deleted).
