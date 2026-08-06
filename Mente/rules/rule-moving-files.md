# RULE · MOVING AND RENAMING FILES

**Status:** current · **Type:** rule · **Updated:** 2026-07-30 · **Owner:** brian
**Ticket:** finding #2 of the 2026-07-30 doc recovery

---

## Purpose

How to move or rename a file without losing its history or breaking what points at it.
Written because `git mv` was presented as optional when it was not.

---

## 1 · THE SEQUENCE — in this order, always

```
1 · IS IT TRACKED?        git ls-files <path>
        │
        ├─ tracked ──▶  git mv <old> <new>     ← NOT optional
        └─ untracked ─▶  mv <old> <new>
2 · WHO POINTS AT IT?      grep -rl "<basename>" --include="*.md"
3 · REPOINT every hit      including memories and CLAUDE.md
4 · VERIFY                 0 orphaned pointers
5 · COMMIT                 with the reason, not just the what
```

**Step 1 is the one that gets skipped.** `mv` on a tracked file makes git see a delete plus an
untracked file — the history of that file stops at the move.

---

## 2 · WHAT WENT WRONG (2026-07-30)

Three docs were moved out of `marca-personal/Mente/Doc/`. All six files in that directory were
**tracked in git**, and `git mv` was mentioned as *"if they are tracked, use git mv"* — a hint, not
a step. Plain `mv` was used.

**Consequence:** git reported 2 deletions pending, and the moved files arrived as untracked.
Nothing was lost, but the history did not follow them, and it took an extra commit to close.

> ⭐ **The lesson:** *"check if it is tracked"* is not advice — it is **step 1**. A conditional
> mentioned in passing is a step that will be skipped.

---

## 3 · WHEN THE TARGET IS PROTECTED BY A `deny`

If the source or destination is inside a path with a `deny` rule, **the AI cannot do it.**

| Who | Does what |
|---|---|
| **Brian** | runs the `mv` / `git mv` — the `deny` exists to stop the AI |
| **The AI** | prepares the exact commands, then **verifies byte sizes** afterwards |

⛔ **Never propose lifting a `deny` to make the move easier.** The day a lock can be lifted because
it is inconvenient, it stops being a lock.

---

## 4 · VERIFICATION AFTER THE MOVE — affirmative, with numbers

| Check | How |
|---|---|
| Content survived | **byte count before == byte count after** |
| Git is clean | `git status --short <dir>` returns nothing |
| No orphan pointers | `grep -rl "<old-basename>"` returns nothing |
| Readable at destination | actually open the first lines |

> *"It moved fine"* is not verification. **10,592 bytes before and after** is.

---

Related: `rules/NAMING_CONVENTION.md` §7 (migration on demand) ·
`docs/Arquitectura_Mente_OS_v2_Bloques.md` §12-SEPTIES (config hygiene) ·
`principles/owner-0-voice.md` §2.7 (a claim is verified, not assumed).
