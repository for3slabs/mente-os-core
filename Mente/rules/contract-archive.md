# CONTRACT · an archived block

**Status:** current · **Type:** contract · **Updated:** 2026-07-30 · **Owner:** brian
**Applies to:** every directory under `blocks/archive/<name>_<YYYY-MM>/`
**Verified by:** `bin/check-structure` · **Source design:** architecture §12.0 + closing steps 5-7
**Ticket:** F8-3 — found missing 2026-07-30: the validator demanded these files, no contract said
what goes in them
---

## Purpose

`contract-block.md` says what an ACTIVE block carries. This says what survives when it closes.

**The gap this fills, measured 2026-07-30:** `bin/check-structure` already refuses an archived block
without `SUMMARY.md` and `blocks/archive/split-architecture_2026-07/connections.md`, and the design names both — but **nothing said what goes
inside them.** A validator that demands a file whose content is undefined produces empty files that
satisfy the check and teach nothing.

> ⭐ **Why an archive exists at all:** *"cerrados = experiencia consultable"* (architecture §12.0).
> A closed block that cannot be consulted was not closed. It was abandoned with paperwork.

---

## 0 · THE SHAPE

```
blocks/archive/<name>_<YYYY-MM>/
├── SUMMARY.md        🔴 required — what was done and what was LEARNED
├── connections.md    🔴 required — what other work this leaves affected
└── BLOCK.md          🔴 required — the block as it closed, moved verbatim
```

⚠️ **`SUMMARY.md` and `blocks/archive/split-architecture_2026-07/connections.md` are DOCUMENTS**: they carry the standard header
(`**Status:** · **Type:** · **Updated:** · **Owner:**`), a `## Purpose` and a `Related:` line, like
everything else under `rules/contract-document.md`. Found on the first real close, 2026-07-30 —
`bin/check-blocks` refused them and the contract had not said so.

**The directory name carries the closing month**, not the opening one: `demo_2026-08` if it closed
in August. Two blocks with the same name in different months are two entries, not a conflict.

⛔ **`docs/` and `cache/` do NOT move.** `cache/` is disposable by definition; `docs/` moves only
if the block owns those documents exclusively — a document consulted by other work stays where it
is, and `SUMMARY.md` points at it.

---

## 1 · `SUMMARY.md` — what was done and what was learned

| Field | Required | Rule |
|---|---|---|
| **What it was for** | 🔴 | the §A `intent`, verbatim. Not rewritten from memory |
| **What was built** | 🔴 | the closed sub-blocks, with the commit that landed each one |
| **The quality verdict** | 🔴 | the `bin/grade-block` output at closing time, **with the numbers** |
| ⭐ **What was LEARNED** | 🔴 | the part that makes this consultable — see below |
| **What was left out** | 🔴 | what did NOT get done and why. An empty section is a lie |
| **Debt handed over** | 🟡 | what another block inherits, naming that block |

### ⭐ "What was learned" — the only section that is not a copy

Everything else in `SUMMARY.md` is consolidation. This one is the reason to keep the file.

> **The test:** *would a person opening this block a year from now avoid a mistake because of this
> line?* If not, it is a description, not a lesson.

| ✅ A lesson | ⛔ Not a lesson |
|---|---|
| *"a DEFAULT never points at something with an owner — `general` was the owner's private thread"* | *"we fixed the topic bug"* |
| *"a dependent is a file that IMPORTS the piece; `instancias.ts` had 26 mentions and 9 imports"* | *"we measured the dependents"* |
| *"the same bug surfaced in 6 files because a cookie value was used as the real instance"* | *"we refactored `kind`"* |

**A lesson that repeats generalises to a rule** (`rules/rule-*.md`) or a case
(`rules/case-*.md`) — that is how an error becomes a form instead of staying an anecdote.

---

## 2 · `blocks/archive/split-architecture_2026-07/connections.md` — what this leaves affected

Closing step 6. Its job is to answer, for whoever opens the NEXT block:
**"what does this block's closing change for me?"**

| Field | Required | Rule |
|---|---|---|
| **Pieces this block owned** | 🔴 | its §B `IN` — now free for another block to claim |
| **Blocks that depended on it** | 🔴 | each `blk-<id>` that named it in §C, and whether that dependency is now satisfied or orphaned |
| **Rules this block created** | 🟡 | rules or ADRs born here that now apply system-wide |
| **What is still open** | 🔴 | sub-blocks that did NOT close and where they went |

> ⭐ **A block does not close over open sub-blocks** (`rules/block-lifecycle.md` §5). If one is
> still open it MOVES to another block first, and this file names where it went. **An orphaned
> sub-block is work that disappears silently.**

---

## 3 · WHAT NEVER GOES IN AN ARCHIVE

⛔ **Secrets** — not even expired ones. `secrets/` is the only place.
⛔ **The full conversation** — the autopsy lives in `Cerebro/Registro_Conversaciones.md`.
⛔ **Code or diffs** — the repo already has them. The archive describes; it does not duplicate.
⛔ **A rewritten history** — the block is moved as it closed. Correcting it afterwards turns a
record into a story.

---

## 4 · WHAT `bin/check-structure` VERIFIES

```
🔴 ARCHIVE INCOMPLETE
   · an archived directory with no SUMMARY.md
   · an archived directory with no connections.md
   · an archived directory with no BLOCK.md

🟡 ARCHIVE
   · SUMMARY.md with an empty "what was learned" — the only section that is not a copy
   · connections.md naming a blk-<id> that does not exist
```

---

## 5 · THE CLOSING TEST

> **Would someone who never saw this block understand, from these three files alone, what it was
> for, what it left behind, and what mistake not to repeat?**

If not, the block does not close. **Same criterion as the sufficiency test** — there it is about
restarting work, here about consulting finished work.

---

Related: `rules/contract-block.md` (the active block) · `rules/block-lifecycle.md` §6 (the 8 closing
steps) · `principles/owner-3-validation.md` §4 (the §5-BIS battery) · `bin/check-structure` ·
`bin/grade-block` (the verdict that goes into SUMMARY).
