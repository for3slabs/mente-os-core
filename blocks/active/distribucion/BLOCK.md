# BLOCK · distribucion

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-distribucion-2026-08
type: code
intent: make Mente OS v2 installable by someone who is not Brian — config-driven, not hand-filled
status: active · lane: full-block · owner: brian
created: 2026-08-02 · updated: 2026-08-03

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- `Mente/mente.config.yml` + `Mente/bin/mente_config.py` (the separation that already exists)
- `Mente/bin/init` (NEW — the piece that does not exist today)
- templates for `CLAUDE.md` · `PROJECT-RULES.md` · `.claude/settings.json`
- the 4 hook `command` paths in `.claude/settings.json`
- `Mente/CAPABILITIES.md` (NEW — what the agent can do, and the engine/instance line)

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
phase: sub-block 5 closed — the agent has a capability map, verified by the battery
next: sub-block 6 — the engine/instance line as a portable LOCK (does not need a clone)
blockers: sub-block 1 needs a CLEAN CLONE to test; it cannot be proven from this session
progress: 1/6 sub-blocks closed
updated: 2026-08-03

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | do the 4 hooks survive a portable path? | `.claude/settings.json` | 4 hooks | open |
| 2 | `bin/init` — ask, then generate | `bin/init` (new) | 0 | open |
| 3 | templates for the 3 startup files | `*.template` | 0 | open |
| 4 | check: no engine file carries an owner name or absolute path | `bin/test-f0-f6` | — | open |
| 5 | ⭐ the agent's CAPABILITY MAP — what it can do, and the engine/instance line | `CAPABILITIES.md` | — | ✅ closed |
| 6 | make the engine/instance boundary a LOCK, portable | `.claude/settings.json` | 4 hooks | open |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- **Sub-block 1 goes FIRST and may sink the plan.** If `$CLAUDE_PROJECT_DIR` does not expand in
  `hooks[].command`, the hooks cannot be portable and `bin/init` must write absolute paths for
  that machine instead. Building the templates before knowing this would be building on a guess.
- **`bin/init` GENERATES, never hand-edits.** Same reason `docs/METRICS.md` exists: a value copied
  by hand is correct exactly once.
- **Templates live in the engine; the generated files do not.** `CLAUDE.md` already declares
  `Scope: documento de INSTANCIA` — this block makes that declaration true instead of a caveat.
- **⭐ The installer is not a person — it is an AGENT** (Brian, 2026-08-02). Whoever fills the
  instance in is an LLM, so the deliverable is not a form: it is a **capability map** the agent
  reads. Two halves, and the second is the one nothing covers today:
  **① what it CAN do** — which validator answers which question, which gate blocks and why,
  what `grade-block` measures. Measured: **no document states this.** `CLAUDE.md` routes *where
  to read*; `README.md` lists one command. An agent that does not know `bin/grade-block` exists
  will hand-write a verdict — inventing criterion, which ADR-003 forbids.
  **② where the line is** — it edits the INSTANCE (its `mente.config.yml`, its blocks, its
  documents) and never the ENGINE (`bin/` `hooks/` `rules/`). Today `ask` covers
  `Edit(bin/**)`, `Edit(hooks/**)`, `Write(hooks/**)` — but **`Write(bin/**)` is missing**, and
  all three carry Brian's absolute path, so they do not travel with a clone.
- **The boundary must be a LOCK, not a paragraph.** This project's own measured law: a rule in
  code is obeyed 100%, one in a document 40-60% — and `PROJECT-RULES.md` §1 now labels which is
  which. Telling the agent "do not touch the engine" in prose is the 40-60% case. Sub-block 6
  makes it the 100% case, portably.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- (none recorded)

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-02 · opened with the diagnosis measured, zero code written
- 2026-08-03 · sub-block 5 ✅ `CAPABILITIES.md` + 2 checks: it may only name validators
  that exist, and `CLAUDE.md` must route to it (an unreferenced map is a map nobody reads)

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

**⭐ WHO INSTALLS THIS IS AN AGENT, NOT A PERSON** (Brian, 2026-08-02): *"VA A HABER UN AGENTE DE
IA O UN LLM QUE ES EL QUE EJECUTE TODAS ESAS INSTRUCCIONES. DEBE DE SABER QUÉ CAPACIDADES TIENE
DENTRO DE MENTE OS V2 Y CÓMO EJECUTARLAS SIN TOCAR EL CÓDIGO DE MENTE OS V2."*

That reframes the deliverable. A form assumes a human reads labels and types values. An agent
needs two things a form does not give:

| | Today | Measured |
|---|---|---|
| **What it CAN do** | nothing states it | `CLAUDE.md` routes *where to read*; `README.md` lists **1** command |
| **Where the line is** | 3 `ask` rules | `Write(bin/**)` missing · all 3 carry an absolute path |

**Why ① is correctness, not documentation:** an agent that does not know `bin/grade-block`
exists hand-writes a verdict — inventing criterion (ADR-003). Same for `check-sufficiency`
before closing, or `generate-metrics` instead of typing a number.

**Why ② must be a lock:** *"do not touch the engine"* in prose is this project's own 40-60% case
(`PROJECT-RULES.md` §1 now labels which rules are locks and which are discipline). The instance
half must stay writable — the agent fills in blocks, documents and `mente.config.yml` as work
advances — while `bin/` `hooks/` `rules/` stay closed to it. That asymmetry is the product.

**Related, already registered:** `memory/PENDIENTES.md` §🚪 (`CLAUDE.md` §ESTADO carries instance
state) is the same problem seen from the document side — this block is the mechanism that closes it.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — the block is still active)
