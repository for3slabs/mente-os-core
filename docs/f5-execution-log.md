# F5 · execution log — from doctrine to lock

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Phase:** F5 (verify) · **Plan:** `docs/plan-v2-rollout.md`
---

## Purpose

F4 measured the code. **F5 makes the system enforce itself.** The measured law: rules enforced by
code comply 100%; rules that live only in a document comply 40-60%.

---

## What was built

| # | Piece | Blocks? | What it does |
|---|---|---|---|
| **F5-1** | `hooks/session-start.sh` | ⛔ never | runs `check-health` + `flag-stale`; **speaks only on 🔴** |
| **F5-2** | `hooks/pre-edit-standards.py` | ⛔ never | touch a file in a block's Scope IN → its §D standards are named, plus a warning if an unclosed sub-block covers it |
| **F5-3** | `hooks/pre-commit.sh` | ⭐ **YES** | an invalid block never reaches a commit |
| **F5-4** | `bin/check-clear-ready` | ⛔ never | ⭐ **the /clear lock** — refuses when the verdict lives only in context |

**Registered in `.claude/settings.json` of the PROJECT**, not `~/.claude/settings.json`.
The 9 GSD hooks are global and were left untouched — verified: still 9.

---

## 🔴 Two bugs found by TESTING, not by reading

Both in `hooks/pre-commit.sh`, the only hook that blocks. Both were found by attempting a real commit —
neither was visible in the source.

### Bug 1 · the guard failed OPEN while looking installed

The first version resolved its own directory from `BASH_SOURCE`. **Git runs the hook from
`.git/hooks/`**, so `dirname/..` resolved to `.git` — `check-blocks` was not there, exit was
**127**, and the `-eq 2` test never matched.

Measured with a probe hook:

```
cwd=/home/brianweb3/for3s/Mente
MENTE resuelto=/home/brianweb3/for3s/Mente/.git     ← wrong
existe check-blocks: NO
check-blocks exit=127
```

**Every commit passed while the hook looked installed.** ⭐ A guard that fails open is worse than no
guard: it is a false sense of safety. Fix: resolve from `git rev-parse --show-toplevel`.

### Bug 2 · the fix for bug 1 would have blocked EVERY commit in marca-personal

Failing closed on a missing validator is right — but `marca-personal` is its **own repo**, with
Mente as a *sibling*, so it found nothing and would have blocked all work in the repo where the demo
lives.

**The rule that came out of it:**

> **fail-OPEN when Mente is genuinely absent** (that repo is not governed by blocks) ·
> **fail-CLOSED when Mente exists but is broken** (a validator that cannot run is not a pass).

---

## Verification — 4 tests, all passing

| Test | Result |
|---|---|
| Mente + broken block (`type` removed) | 🔴 **blocked** — commit never created, HEAD unchanged |
| marca-personal (finds Mente as a sibling) | exit 1 — validates, does not break |
| block repaired | exit 0 in **both** repos |
| unrelated repo with no Mente nearby | exit 0 — **does not block other people's repos** |

Hooks installed as **real files, not symlinks**, in `Mente/.git/hooks/` and
`marca-personal/.git/hooks/`.

**Escape hatch on purpose:** `git commit --no-verify`, documented in the hook itself
(`rules/rule-friction.md` — a guard with no escape hatch gets deleted, and a deleted guard protects
nothing).

---

## ⭐ F5-4 · what the /clear lock says about the session that built it

```
🔴 DO NOT /clear YET — 1 thing would be lost
   this session (4fc1996c, 7 MB) has NO entry in Cerebro/Registro_Conversaciones.md
```

This is the answer to the worst failure of the project: *"antes del clear me dijo todo está
perfecto; después del clear, sigue roto."* Nothing lied — `/clear` is a **cut, not a save**, and the
verdict lived only in the conversation. **The fix is not a better memory: it is refusing to cut while
something that matters exists only in context.**

---

## F0 holes found while doing F5 (and closed)

`.claude/settings.json` — the **shared** file, which travels with the repo — had never been audited.
`check-health` only read `settings.local.json`.

| Hole | Fix |
|---|---|
| `Read(//home/brianweb3/**)` with **zero** deny rules → open door to `~/.ssh` | 10 deny rules added to **both** files |
| the 2 gates (NavigoX, marca-personal/Mente) existed only in `.local`, which is gitignored | duplicated into the shared file so they travel |
| dead path `/home/brianweb3/Godinez/marca-personal` | removed |
| `check-health` audited only the local file | now audits both, and flags a broad `Read` grant with no deny covering credentials |

Verified with a negative test: emptying `deny` makes `check-health` report the hole; restoring it
goes silent.

---

Related: `docs/plan-v2-rollout.md` · `rules/rule-session-close.md` (the /clear rule) ·
`rules/rule-friction.md` (why the escape hatch exists) · `bin/check-clear-ready`.
