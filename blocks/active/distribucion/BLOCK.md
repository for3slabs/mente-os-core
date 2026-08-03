# BLOCK · distribucion

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-distribucion-2026-08
type: code
intent: make Mente OS v2 installable by someone who is not Brian — config-driven, not hand-filled
status: active · lane: full-block · owner: brian
created: 2026-08-02 · updated: 2026-08-02

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- `Mente/mente.config.yml` + `Mente/bin/mente_config.py` (the separation that already exists)
- `Mente/bin/init` (NEW — the piece that does not exist today)
- templates for `CLAUDE.md` · `PROJECT-RULES.md` · `.claude/settings.json`
- the 4 hook `command` paths in `.claude/settings.json`

## ⛔ OUT
- DO NOT touch `Mente/Cerebro/` — DERIVED: it is the For3s product graph, not the engine
  (`CLAUDE.md` §DÓNDE VIVE CADA COSA marks it "NO se migra")
- DO NOT touch `blocks/active/demo/**` — DERIVED: another block's Scope IN (`rule-isolation.md`)
- DO NOT rewrite `memory/` `work/` `vision/` — DERIVED: the public engine already excludes them
- DO NOT weaken any `deny` to make a path portable — DERIVED: `PROJECT-RULES.md` §3
  *"never propose lifting a deny for convenience"*

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: nothing — the config layer it extends is already built
- DEPENDED ON BY: none declared
- ISOLATED FROM: `demo` (that block lives in `marca-personal/`, this one in the engine)
- 🔴 CRITICAL PIECES (measured 2026-08-02):
  - `bin/mente_config.py` → 6 importers · `.claude/settings.json` → 4 registered hooks
  - 34 unique absolute paths under `/home/brianweb3/` · 43 occurrences

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
## Required standards
- rules/rule-fix-not-patch.md
- rules/rule-config-hygiene.md
- rules/rule-checks-must-measure.md
- principles/expertise/val-integration.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: opened — diagnosis measured, nothing built
next: sub-block 1 — verify whether $CLAUDE_PROJECT_DIR expands inside hooks[].command
blockers: sub-block 1 needs a CLEAN CLONE to test; it cannot be proven from this session
progress: 0/4 sub-blocks closed
updated: 2026-08-02

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | do the 4 hooks survive a portable path? | `.claude/settings.json` | 4 hooks | open |
| 2 | `bin/init` — ask, then generate | `bin/init` (new) | 0 | open |
| 3 | templates for the 3 startup files | `*.template` | 0 | open |
| 4 | check: no engine file carries an owner name or absolute path | `bin/test-f0-f6` | — | open |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- **Sub-block 1 goes FIRST and may sink the plan.** If `$CLAUDE_PROJECT_DIR` does not expand in
  `hooks[].command`, the hooks cannot be portable and `bin/init` must write absolute paths for
  that machine instead. Building the templates before knowing this would be building on a guess.
- **`bin/init` GENERATES, never hand-edits.** Same reason `docs/METRICS.md` exists: a value copied
  by hand is correct exactly once.
- **Templates live in the engine; the generated files do not.** `CLAUDE.md` already declares
  `Scope: documento de INSTANCIA` — this block makes that declaration true instead of a caveat.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- (none recorded)

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-02 · opened with the diagnosis measured, zero code written

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context
**Why this block exists** (Brian, 2026-08-02): *"esto está local para mí y aun así tenemos
errores. AÚN NO VEO QUE SEA ALGO QUE PODAMOS CONFIAR A QUE LA GENTE PUEDA OCUPAR."*

**The measured problem.** `mente.config.yml` was built so a new user edits one file and nothing
else — its own header says *"if they ever have to touch `bin/` to make the system work, this
separation failed"*. The validators honour it. **The three startup files do not:**

| File | Brian's data baked in |
|---|---|
| `.claude/settings.json` | **43 occurrences** of `brianweb3`, **34 unique absolute paths** |
| `PROJECT-RULES.md` | 11 mentions of "Brian" |
| `CLAUDE.md` | 4 mentions of "Brian" |

🔴 **The hard blocker:** the 4 hooks — the system's three gates plus standards injection — point
at `/home/brianweb3/for3s/Mente/hooks/`. A new user clones and **no gate starts**. It does not
fail loudly; it silently stops governing, which is the worst failure mode for a system whose
thesis is *"what is in code is obeyed 100%"*.

**What was tried and reverted (2026-08-02).** The hooks were rewritten with
`$CLAUDE_PROJECT_DIR` — which demonstrably works in permission rules. But it could **not be
verified for hooks from this session**: the variable is undefined in the session shell, so the
probe resolved to an empty path and proved nothing. Leaving all four gates changed on an
unverified assumption is the exact defect this project spent 2026-08-02 correcting eight times.
Reverted; `check-health` confirms the gates are intact.

**Related, already registered:** `memory/PENDIENTES.md` §🚪 (`CLAUDE.md` §ESTADO carries instance
state) is the same problem seen from the document side — this block is the mechanism that closes it.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — the block is still active)
