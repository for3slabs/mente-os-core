# F6 · execution log — from rules-in-a-file to a routed hierarchy

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Phase:** F6 (guarantee reading) · **Plan:** `docs/plan-v2-rollout.md`
---

## Purpose

F5 made the system verify itself. **F6 makes sure the right rules are READ** — and only the right
ones. It is the most intrusive phase, which is why the plan put it near the end: *you earn the right
to block after proving the criterion works.*

---

## What was built

| # | Piece | Status |
|---|---|---|
| **F6-1** | `PROJECT-RULES.md` (new) + `CLAUDE.md` turned into a ROUTER | ✅ |
| **F6-2** | hook that injects §D standards before editing | ✅ **already built in F5** |
| **F6-3** | the three critical gates: `hooks/gate-critical.py` | ✅ |
| **F6-4** | `bin/check-applied` — were the standards APPLIED or just listed? | ✅ |

---

## F6-1 · the three levels now exist

Before: every rule lived in `CLAUDE.md`, so **every block and every future project inherited them.**

> **Brian, 2026-07-29:** *"el sistema NO SOLO LO VOY A OCUPAR PARA DEMO, y entonces el resto de lo
> que haga va a estar contagiado con esas reglas."*

```
🌐 Mente/base-rules.md    119 lines   universal conduct
🏢 PROJECT-RULES.md       141 lines   the gate · server-first · scope · identity · security
📦 BLOCK.md §B                        only while that block is open
```

`CLAUDE.md` is now a **router**: it points at where rules live and does not repeat them. **A rule
written in `CLAUDE.md` has no declared level — that was the bug.**

⭐ **Verified: 0 of 24 rules lost.** Each concept from the old `CLAUDE.md` was traced to its new
home before the old file was replaced (backup first, then a 24-point cross-check). `base-rules.md`
keeps the 2 project rules **as pointers only** — a reader must know they exist, but it is no longer
their source.

**Order mattered:** `PROJECT-RULES.md` was created **before** anything was removed from `CLAUDE.md`
(`rules/rule-inheritance.md` §6) — otherwise a session in between loses the rule entirely.

---

## F6-3 · ⭐ each gate at the level it EARNED

**Rule of this phase:** *if a gate obstructs more than it protects, it degrades to a warning.*
Levels chosen from measurement, not preference:

| Gate | Measured | Level | Why |
|---|---|---|---|
| edit a piece with declared dependents | 5 files, edited constantly | ⚠️ **WARN** | blocking the daily path is pure friction; the propagation lane already forces the decision |
| touch the database | 4 SQL files, rarely touched | 🔴 **BLOCK** | an irreversible migration is the one mistake with no undo |
| close a block without sufficiency | `check-sufficiency` existed, **nothing called it** | 🔴 **BLOCK** | restarting from disk alone is the only reason blocks exist |

⭐ **Gate 1 stays a warning on purpose.** That is not weakness — it is the measurement saying a
second stop adds nothing where `rules/rule-lanes.md` already raised the lane.

Escape hatch documented inside every block message (`rules/rule-friction.md`).

---

## 🔴 Three bugs, all found by TESTING

### 1 · The DB gate could never fire
Its `DOWN` pattern included `DROP\s+(TABLE|COLUMN)` — so **a `DROP TABLE` counted as its own
rollback.** A rollback is a *declared way back*, never the destructive statement itself.

### 2 · The close gate never checked open sub-blocks
It read the block text from `owning_block()`, which returns `None` for a `BLOCK.md` — **a block does
not declare its own file in its §B IN.** The check silently never ran. Fix: read the file being
closed, directly.

### 3 · The battery and the gate disagreed
`printf` emitted `status: closed\n` with a **literal** backslash-n inside the JSON value, so the
hook's `^status:\s*closed` never matched. The gate blocked correctly by hand and passed in the
battery — **the worst kind of disagreement**, because the battery is what you trust when you are
tired.

---

## F6-4 · the validator caught 4 decorative standards

`bin/check-applied demo` → **4 of 5 declared standards showed no evidence of use.**

Investigated one by one instead of deleting them:

| Standard | Verdict |
|---|---|
| `rules/rule-fix-not-patch.md` | **applied** — the `kind` fix evaluated all 6 files. Citation was missing, now added |
| `expertise/database.md` | **applied** — a column dropped, not shadowed. Citation added |
| `rules/rule-lanes.md` | **applied** — the lane came from the measured graph. Decision written |
| `expertise/frontend.md` | 🔴 **never applied** — 6 closed sub-blocks, **zero** frontend decisions. **Removed from §D** |

⭐ **A standard declared and never applied is decoration** — and an inflated §D makes the injection
hook noisy, which is how a hook gets ignored. Removing it was the honest fix, not inventing evidence.

---

## Verification

```
bin/test-f0-f6 → passed: 77 · failed: 0
bin/check-blocks → 0 errors · 0 warnings
```

The battery grew from 60 to 77 checks: the 3 levels exist · `CLAUDE.md` stores no project rules ·
the 5 migrated rules are still findable · both DB gate directions · both close gate directions ·
gate 1 warns and never blocks · every §D standard shows evidence of use.

**The 9 global GSD hooks: still 9, untouched.** The 3 project hooks live in
`.claude/settings.json` of the project.

---

Related: `docs/plan-v2-rollout.md` · `rules/rule-inheritance.md` (the model) ·
`PROJECT-RULES.md` · `bin/check-applied` · `hooks/gate-critical.py` · `docs/f5-execution-log.md`.
