# RULE · CONFIG HYGIENE — the permissions that govern everything
**Status:** current · **Type:** rule · **Updated:** 2026-07-31 · **Owner:** brian
**Ticket:** finding of the 2026-07-31 `.claude/` audit
**Enforced by:** `bin/check-health` · **Governs:** `.claude/settings.json` · `.claude/settings.local.json`
---

## 0 · WHY THIS FILE EXISTS UNDER THIS NAME

> **Brian, 2026-07-31:** *"si tuviste que leer primero antes de probarlo, corrígelo."*

A file called `rule-config-hygiene.md` existed and **was about moving and renaming files**. The
real config rules lived buried inside an 800-line architecture document. So on 2026-07-31 the AI
audited `.claude/`, pruned 31 permissions, and **re-derived from scratch the exact criteria that
were already written** — because the file whose name promised them did not contain them.

> ## ⭐ A name that lies is a file that does not get read.

The misnamed file is now `rules/rule-moving-files.md`, which is what it always was. **This file
holds the six config rules**, at the level a rule belongs: enforceable, findable, and named after
what it governs.

**Why permissions deserve their own rule:** `.claude/settings.json` registers the four hooks that
govern the whole system — the three gates that block plus the standards injection. It is the
highest-leverage file in the project and, until 2026-07-31, it had **no version history at all**.

---

## 1 · THE SIX RULES

### 1.1 · Secrets are REFERENCED, never pasted

```
⛔  sshpass -p '<THE-REAL-PASSWORD>' ssh brianweb3@for3s
✅  sshpass -p "$FOR3S_SSH_PASS" ssh brianweb3@for3s
```

**Why this is a rule and not advice:** approving a command files it **verbatim** as a permanent
permission. A secret pasted into an approved command is **recorded forever**.

**Measured:** **331 entries** carrying the server password, in a file with no `.gitignore`.

| Where a secret lives | Verdict |
|---|---|
| `secrets/` | ✅ gitignored |
| An environment variable | ✅ never on disk |
| **An approved command** | 🔴 **forbidden** |
| **A settings file** | 🔴 **forbidden** |

> ⚠️ **Purging does not invalidate.** The secret purged on 2026-07-27 **still lives in that
> session's `.jsonl`** — transcripts are not edited. **Any leaked secret gets ROTATED, not just
> deleted.**

---

### 1.2 · Every path declares its WHY

> **Brian:** *"cuando cargue una nueva ruta debe tener un por qué en especial, no solo por cargar."*

```jsonc
"additionalDirectories": [
  // 2026-07-27 · the whole project · daily work
  "$CLAUDE_PROJECT_DIR"
]
```

**Measured when the rule was written:** 9 entries, **none justified**. Three pointed at paths that
did not exist; one contradicted the NavigoX gate.

---

### 1.3 · ⭐ ONE MECHANISM, ONE ENTRY

> ## Does this entry authorize something NO other entry already authorizes?
> If not → **it does not go in.**

| # | Criterion | Measured example |
|---|---|---|
| 1 | **No overlap** — if A contains B, B does not enter | `/tmp` already contained `/tmp/h2` |
| 2 | **No dead paths** — the path exists or it goes | **3 of 9** did not exist |
| 3 | **One entry per MECHANISM, not per invocation** | **234** `Bash(sshpass...)` entries for one mechanism |

**The evidence:** 1,010 permissions grouped by mechanism were 234 `sshpass` + 139 `curl` + 101
`python3` + 161 others. **234 entries for "use sshpass" is not a permission list — it is a log of
every time someone said yes.**

---

### 1.4 · Portable paths

**Measured:** 689 `/home/brianweb3/` paths in `settings.local.json`. **Nobody else can use this.**

| ⛔ Not portable | ✅ Portable |
|---|---|
| `/home/brianweb3/for3s/Mente` | `$CLAUDE_PROJECT_DIR/Mente` |

> ⚠️ **Honest exception:** the 9 GSD hooks are external and carry their own absolute paths. They
> are **documented as non-portable** instead of pretending they are fixed. A declared limit is
> engineering; a hidden one is debt.

---

### 1.5 · 🆕 The protected surface is declared COMPLETE, not per tool

> **Found 2026-07-31, and it had never been written anywhere.**

`deny` covered `Read`, `Edit` and `Write`. **No Bash rule.** So `cat` read what `Read` forbade.

**Proven live, before the fix:** `ls Mente/secrets/` listed the files with zero friction, including
`Secretos_Demo_Sitio.md` — a directory under an explicit `deny Read`.

> ## 🚫 A protection declared by TOOL is a protection with a back door.
> The question is not *"did I deny Read?"* — it is **"can anything still reach it?"**

**For every protected target, deny the real reach channels:**

| Channel | Commands to cover |
|---|---|
| read | `cat` · `head` · `tail` · `less` · `more` |
| binary read | `strings` · `xxd` · `od` · `base64` |
| copy out | `cp` · `mv` · `tar` |

⚠️ **Syntax:** `Bash(cmd *)` — a space and a trailing asterisk. The schema **rejects** `:*` in the
middle of a pattern, so a malformed rule fails at write time, not in production.

**Also worth denying outright:** `Bash(rm -rf *)` with no path. It was authorized, unrestricted.

> ⭐ **Why this rule was invisible:** the other five all check the SHAPE of the permissions — are
> they justified, portable, deduplicated, secret-free. **None asks whether the surface has a hole.**
> A system can be perfectly tidy and still wide open.

---

### 1.6 · 🆕 `deny` lives in BOTH files, `allow` does not

| File | Travels with the repo | What belongs there |
|---|---|---|
| `settings.json` | ✅ yes | the hooks · the `deny` · the shared minimum |
| `settings.local.json` | ⛔ **gitignored** | machine-specific approvals only |

**Measured 2026-07-31:** 16 allow shared vs **199 local**. Anyone opening the project on another
machine starts with 8% of the permissions — and the **25 broad wildcards**, the ones that actually
deserve review, lived in the file nobody audits.

> 🔴 **A `deny` that lives only in the local file protects nobody else.** Mirror every `deny` into
> `settings.json`; keep `allow` asymmetric on purpose.

**And the two entries that make the whole list decorative:** `Bash(bash*)` and `Bash(sh*)`. With
either one approved, any command runs by wrapping it in `bash -c`. Removed 2026-07-31.

---

## 2 · WHAT `bin/check-health` ENFORCES

| Rule | In code | Signal |
|---|---|---|
| 1.1 secrets referenced | ✅ | 🔴 `SECRET · <what> is embedded in an approved command` |
| 1.2 path declares why | 🟡 partial | 🟡 dead path in `additionalDirectories` |
| 1.3 one mechanism | ✅ | 🟡 dead paths · overlapping paths · allow-count threshold |
| 1.4 portable paths | 🟡 partial | — |
| **1.5 complete surface** | ✅ `bin/test-f0-f6` | 🔴 `Bash deny covers the protected targets` |
| **1.6 deny in both** | ✅ `bin/test-f0-f6` | 🔴 per-file deny checks |

> 🔴 **The threshold that failed:** the allow-count check fires at `> 200`. On 2026-07-31 there
> were **199** — one under the line, so it never spoke. **A limit that is missed by one unit is a
> limit set by accident.** Lowered to 120 the same day.

---

## 3 · THE PATTERN BEHIND EVERY MEASURED FAILURE

| Failure | The convention existed | What was missing |
|---|---|---|
| Password **331 times** in settings | `secrets/` was the right place | **nothing forced referencing it** |
| **689 absolute paths** | — | **nothing demanded portability** |
| `additionalDirectories` reaching NavigoX | the gate forbade it | **nothing asked the path to justify itself** |
| **Bash reading past `deny Read`** | — | **nothing asked if the surface was complete** |
| **These rules re-derived from zero** | they were written | **the file named for them held something else** |

> **In all five, the rule existed or was obvious. What was missing was the mechanism** — and in the
> last one, the mechanism was as simple as a filename that told the truth.

---

Related: `rules/rule-moving-files.md` (what this file used to be) ·
`docs/architecture/validators-and-hygiene.md` §12-S (the origin of rules 1.1-1.4) ·
`bin/check-health` · `bin/test-f0-f6` (§F0 security) · `principles/owner-0-voice.md` §2.7.
