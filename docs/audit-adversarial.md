# Adversarial audit · attacking F0-F6 to break it

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Reproducible with:** `bin/test-f0-f6` (section ADVERSARIAL)
---

## Purpose

Brian asked to test everything from F0 to F6 **in order to break it**, not to confirm it. That is a
different exercise: a battery that only passes proves nothing.

**Result: 9 real bugs, 3 of them in the guards themselves.** Every one is now a permanent check.

---

## The 9 bugs

### 1 🔴 `check-sufficiency` returned SUCCESS for a block that does not exist
`check-sufficiency does-not-exist` printed "no blocks found" and **exited 0**. Any caller — a hook,
a gate, CI — reads 0 as *"this block is sufficient"*. **The most dangerous shape of bug: silent
approval.**

### 2 🔴 A glob silently graded a DIFFERENT block
`check-sufficiency '*'` printed **"✅ SUFFICIENT"** about `demo`. `check-applied '*'` printed a
report titled `*` while measuring `demo`. **A validator that answers a question you did not ask is
worse than one that errors.** Fixed in all three name-taking validators: a block name is a folder
name, and globs and paths are refused.

### 3 🔴 The word "rollback" in prose DISABLED the database gate
`DROP TABLE x; -- no rollback needed` **passed**, because the pattern matched `\brollback\b`
anywhere. **A comment stating the opposite switched off the protection** — the escape hatch was a
typo away. Rollback detection is now structural and anchored to line starts.

### 4 🔴 Destructive SQL from application code was completely unguarded
The gate only inspected files whose NAME looked like a migration. Measured: the demo runs SQL from
`duenos.ts`, `eventos.ts`, `userStore.ts`. **`await sql\`DROP TABLE users\`` inside a .ts did the same
damage with no filename to flag it.** Now blocked — and it also protects the immutable-audit rule
(`DELETE FROM audit_log` in Python is refused).

### 5 🔴 `status: CLOSED` in caps evaded the close gate entirely
Markdown is written by humans. **A case-sensitive guard is a guard with a typo-sized hole.**

### 6 🔴 The pre-commit failed OPEN when the validator lost its execute bit
`chmod -x bin/check-blocks` made the validator read as "not found", so the hook took the fail-OPEN
path and **let every commit through**. Same fail-open failure as the first F5 bug, reached by a
different route. EXISTS and EXECUTABLE are now different answers. A 120s timeout was added: a
validator that hangs is a commit that hangs.

### 7 🔴 Three crashes in the PreToolUse hooks
`null`, `[]` and `{"file_path": 123}` raised `AttributeError` / `TypeError`. **A hook that only warns
must never fail** — an unexpected exit code can interfere with the edit it was meant to comment on.
The payload comes from outside; its shape is never assumed. 12 malformed payloads now pass silently.

### 8 ⭐🔴 NOTHING PROTECTED THE GUARDS
A hook could be deleted, emptied, or stripped of its execute bit and **nothing in the startup path
noticed.** Only the full battery caught it — and the battery runs by hand.

> **A disarmed guard is worse than no guard: the system keeps reporting healthy while unprotected.**

`check-health` now verifies every guard exists, is executable, and is not gutted — and it runs at
every SessionStart, the only moment guaranteed to happen. It also checks that each registered hook
still points at a file that exists.

### 9 🟡 A malformed `id` broke the graph silently
`id: NOT-AN-ID` was accepted. But §C connections resolve with `blk-[\w-]+`, so **that block could
never be referenced by another** — the graph broke with no error. The id shape is load-bearing.

---

## What could NOT be broken

| Attack | Result |
|---|---|
| hand-write `🟢 PRODUCT` into the block | ⭐ **contradicted** — the verdict is measured, never read from the file |
| declare 0 dependents where there are 12 | detected as a stale count |
| `hooks/session-start.sh` with its validators deleted | exits 0 — **a startup hook that breaks is a session that will not start** |
| 15 hostile arguments across 3 validators | all rejected cleanly |
| empty / title-only / §B-less blocks | all refused |
| `type: codex`, duplicate id, `blk-DEMO-...` | all refused |

---

## And 3 false failures that were MY testing, not the code

- `DROP\tTABLE` "evaded" the gate — the shell passed a literal `\t`, not a tab
- a `.ts` case "passed" — my bash helper was eating the backtick
- 3 adversarial checks reported silent — `cmd | grep -q` under `set -o pipefail` takes the exit of
  the **first failing stage**, and `check-health` legitimately exits 2

⭐ **Lesson kept in the battery: capture the output first, evaluate it after. Never mix running with
judging.** Reporting a bug that is not there costs the same trust as missing one.

---

## Verification

```
bin/test-f0-f6 → passed: 87 · failed: 0   (60 → 77 → 87 as the phases and attacks landed)
bin/check-blocks → 0 errors · 0 warnings
```

---

Related: `docs/audit-f0-f5.md` · `docs/f5-execution-log.md` · `docs/f6-execution-log.md` ·
`bin/test-f0-f6` · `bin/check-health` · `hooks/gate-critical.py`.
