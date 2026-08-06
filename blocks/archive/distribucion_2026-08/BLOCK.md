# BLOCK · distribucion

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-distribucion-2026-08
type: code
intent: make Mente OS v2 installable by someone who is not Brian — config-driven, not hand-filled
status: closed · lane: full-block · owner: brian
created: 2026-08-02 · updated: 2026-08-05

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- `Mente/mente.config.yml` + `Mente/bin/mente_config.py` (the separation that already exists)
- `Mente/bin/init` (NEW — the piece that does not exist today)
- templates for `CLAUDE.md` · `PROJECT-RULES.md` · `.claude/settings.json`
- the 4 hook `command` paths in `.claude/settings.json`
- `CAPABILITIES.md` (NEW — what the agent can do, and the engine/instance line)

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
- 🔴 CRITICAL PIECES: `bin/mente_config.py` → 6 importers · `.claude/settings.json` → 4 hooks
  (the 34 absolute paths that set the lane are recorded in §J)

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
## Required standards
- rules/rule-fix-not-patch.md
- rules/rule-config-hygiene.md
- rules/rule-checks-must-measure.md
- principles/expertise/val-integration.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: CLOSED 2026-08-05 · 🟢 PRODUCT (layer 1 7/7 + layer 2 six dimensions, §K)
next: nothing — debt handed to PENDIENTES.md (field proof by a third party · 60 criterion holes)
blockers: none
progress: 6/6 sub-blocks closed
updated: 2026-08-05
note: first block ever judged by layer 2 — the six QA dimensions were filled the same day.

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | do the 4 hooks survive a portable path? | `.claude/settings.json` | 4 hooks | ✅ closed |
| 2 | `bin/init` — ask, then generate | `bin/init` | 0 | ✅ closed |
| 3 | templates for the 3 startup files | `templates/*.template` | 0 | ✅ closed |
| 4 | check: no engine file carries an owner name or absolute path | `bin/test-f0-f6` | — | ✅ closed |
| 5 | ⭐ the agent's CAPABILITY MAP — what it can do, and the engine/instance line | `CAPABILITIES.md` | — | ✅ closed |
| 6 | make the engine/instance boundary a LOCK, portable | `.claude/settings.json` | 4 hooks | ✅ closed |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- **⭐ The blocker was asserted, not measured — and it did not exist.** Sub-block 1 was declared
  "needs a clean clone" because a naive probe resolved to empty (the variable is undefined in the
  session shell). **The source was never consulted.** The official docs state the placeholder is
  exported into the hook process and the command runs through `sh -c`. Setting it as the harness
  does and running each hook from `/tmp`: all four ran, gate-critical still exited 2.
  **A limit you have not verified is not a limit — it is a guess wearing one's clothes.**
  Kept as the block's most useful lesson: the same failure as every check that reported green
  without measuring (`rules/rule-checks-must-measure.md`), one level up — a *plan* reporting
  blocked without measuring.
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
  **② where the line is** — it edits the INSTANCE and never the ENGINE. Was 3 `ask` rules with
  an absolute path (so they did not travel); now 24 portable ones. → §F-6.
- **The boundary must be a LOCK, not a paragraph.** This project's own measured law: a rule in
  code is obeyed 100%, one in a document 40-60% — and `PROJECT-RULES.md` §1 now labels which is
  which. Telling the agent "do not touch the engine" in prose is the 40-60% case. Sub-block 6
  makes it the 100% case, portably.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- **`generate-metrics` corre la batería entera (~2 min) y toma su lock.** Lanzarlo mientras otra
  corrida está viva publica números de la corrida VIEJA sin avisar: pasó en el wrap de S9
  (`battery.checks` salió 142 con la batería en 160). No es defecto —el lock hace su trabajo—
  pero conviene esperar a que libere antes de creerse un número recién publicado.

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-02 · opened with the diagnosis measured, zero code written
- 2026-08-03 · sub-block 5 ✅ `CAPABILITIES.md` + 2 checks: it may only name validators
  that exist, and `CLAUDE.md` must route to it (an unreferenced map is a map nobody reads)
- 2026-08-03 · sub-block 6 ✅ engine write-gated PORTABLY (24 rules, `$CLAUDE_PROJECT_DIR`)
  🔴 found doing it: Edit/Write do NOT cover Bash — a python one-liner rewrote a file
  under bin/ untouched by the Edit rule. Same back door as rule-config-hygiene §1.5
- 2026-08-03 · sub-blocks 1·2·3 ✅ PROVEN ON A REAL CLONE: engine copied to /tmp,
  owner set to another name, `bin/init` generated CLAUDE.md + PROJECT-RULES.md with
  6 mentions of the new owner and ZERO of Brian, wired 4 portable hooks, and a hook
  of the clone RAN against the clone's own path
- 2026-08-03 · sub-block 4 ✅ the engine carries no one's name. Found and fixed REAL
  contamination: `bin/test-f0-f6` had `-home-brianweb3-for3s` hardcoded — the engine
  shipping with one user's identity. Now asks mente_config. Comments exempt on purpose:
  4 validators document that same incident, and deleting history to satisfy a grep
  would erase why the rule exists

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context
**Why this block exists** (Brian, 2026-08-02): *"esto está local para mí y aun así tenemos
errores. AÚN NO VEO QUE SEA ALGO QUE PODAMOS CONFIAR A QUE LA GENTE PUEDA OCUPAR."*

**The measured problem (2026-08-02, now solved).** `mente.config.yml` was built so a new user
edits one file and nothing else. The validators honoured that; the three startup files did not —
`.claude/settings.json` carried **43** occurrences of one username and **34** absolute paths,
`PROJECT-RULES.md` 11 mentions of the owner, `CLAUDE.md` 4.

🔴 **What made it urgent (solved by §F-1):** the 4 hooks pointed at one user's home, so a clone
started with **no gate running** — silently. That is the worst failure mode for a system whose
thesis is *"what is in code is obeyed 100%"*.

**⭐ WHO INSTALLS THIS IS AN AGENT, NOT A PERSON** (Brian, 2026-08-02): *"VA A HABER UN AGENTE DE
IA O UN LLM QUE ES EL QUE EJECUTE TODAS ESAS INSTRUCCIONES. DEBE DE SABER QUÉ CAPACIDADES TIENE
DENTRO DE MENTE OS V2 Y CÓMO EJECUTARLAS SIN TOCAR EL CÓDIGO DE MENTE OS V2."*

That reframed the deliverable: a form assumes a human reads labels and types values, so the
deliverable became a **capability map** instead — `CAPABILITIES.md`, §G and §F-5.

**Related, already registered:** `memory/PENDIENTES.md` §🚪 (`CLAUDE.md` §ESTADO carries instance
state) is the same problem seen from the document side — this block is the mechanism that closes it.
**Full closing evidence:** `blocks/archive/distribucion_2026-08/docs/closing-report.md`
(sub-block 1's lesson is kept verbatim in §G).

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing · 2026-08-05 — 🟢 PRODUCT

> ⭐ **First block in Mente OS ever judged by LAYER 2.** The six QA dimensions were empty
> (`⬜ PENDING · BRIAN`) until Brian filled them the same day. Full evidence, dimension by
> dimension: **`blocks/archive/distribucion_2026-08/docs/closing-report.md`**.

| Criterion (`principles/owner-3-validation.md` §2) | Result |
|---|---|
| 1 · Functional | 🟢 `test-f0-f6` **160 passed / 0 failed** · `check-blocks` 0 errors · 281/281 citations |
| 2 · Sufficiency | 🟢 §A-E answer the 7 restart questions · §J within its ceiling |
| 3 · Quality | 🟢 layer 1 **7/7** + 🟢 layer 2 **6/6 dimensions**, evidence attached |

**Done:** Mente OS v2 is installable by someone who is not Brian — 4 portable hooks (a clone used to
start with **no gate running, silently**), `bin/init` (generates, never hand-fills), 3 templates, a
check that no engine file carries anyone's name, `CAPABILITIES.md`, and the engine/instance line as
a portable LOCK: 24 `$CLAUDE_PROJECT_DIR` rules where 3 absolute paths did not travel.
**Learned:** ⭐ *a limit you have not verified is not a limit — it is a guess wearing one's clothes*
(§G) · 🔴 `Edit`/`Write` deny rules do **not** cover `Bash`.

**Connections:** `blk-demo` unaffected (different repo, no shared Scope IN) · `docs/PENDING-BRIAN.md`
row 2 closed, holes **66 → 60** · `rules/qa-dimensions.md` `draft` → `current` · closes the
document-side view of `memory/PENDIENTES.md` §🚪.

**Debt NOT closed** → `memory/PENDIENTES.md`: ① field proof by a real third party (the clone test ran
on this machine — proves the mechanism, not another owner's experience) · ② 60 criterion holes in the
8 discipline files · ③ Brian's 2 decisions: GPG · `~/.claude.json`.
**Friction (§H):** `generate-metrics` published a stale `1 failed` during this close. Proposal:
refuse to publish when it did not own the lock for the whole run.
