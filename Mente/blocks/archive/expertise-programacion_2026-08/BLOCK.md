# BLOCK · expertise-programacion

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-expertise-programacion-2026-08
type: docs
intent: absorb the useful part of 2 external skills into Mente OS's own programming expertise
status: closed · lane: direct · owner: brian
created: 2026-08-05 · updated: 2026-08-05

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
<!-- ⭐ The only field the AI does not fill: the boundary is a decision, not a
     derivation (block-lifecycle.md §1). An empty OUT is a block with no boundary. -->
<!-- Paths from the Mente root (check-links' convention); grade-block resolves both since §G-6. -->
## ✅ IN
- `principles/expertise/dev-backend.md` · `principles/expertise/dev-database.md`
- `principles/expertise/dev-frontend.md` · `rules/rule-shipping-flow.md` (NEW, §G-5)
- `bin/grade-block` (added mid-block: grading this one exposed 3 defects in it, §G-6)

## ⛔ OUT
- ⛔ **NEVER a value copied verbatim that names Convex** — DERIVED from Brian, 2026-08-05:
  *"debe ser propio de Mente OS v2"*. The logic may be kept; the vendor may not.
- ⛔ **NEVER `--dangerously-skip-permissions`** — DERIVED: `PROJECT-RULES.md` §3 forbids proposing
  the lifting of a deny for convenience. `cracked-dev` recommends it; it does not travel.
- ⛔ DO NOT touch `blocks/active/demo/**` — DERIVED: another block's Scope IN (`rule-isolation.md`)
- ⛔ DO NOT touch `Mente/Cerebro/` — DERIVED: For3s product graph, not the engine (`CLAUDE.md`)
- ⛔ DO NOT fill criterion holes the skills do not answer — DERIVED: ADR-003, the AI never
  invents criterion. A skill is external material, NOT Brian's criterion.

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: `rules/qa-dimensions.md` — the 6 dimensions are the frame every expertise file fills
- DEPENDED ON BY: any future block declaring `dev-backend.md` in its §D (none today)
- ISOLATED FROM: `demo` (lives in `marca-personal/`, this one in the engine)
- 🔴 CRITICAL PIECES: `dev-backend.md` → read by owner-2 before writing code AND injected by
  `hooks/pre-edit-standards.py`. What lands here enters context on every backend edit.
<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
<!-- These get injected before editing (architecture §12-QUATER). Every path must exist. -->
## Required standards
- rules/rule-fix-not-patch.md
- rules/rule-checks-must-measure.md
- rules/contract-document.md
- principles/expertise/doc-structure.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: CLOSED 2026-08-05 · 🟢 PRODUCT (layer 1 3/3 applicable + layer 2 six dimensions, §K)
next: nothing — debt handed to PENDIENTES.md (grade-block self-test · re-grading an archived block)
blockers: none
progress: 5/5 sub-blocks closed
updated: 2026-08-05
note: Brian's two rulings — ① everything from cracked-dev goes in, omitting is not good;
      ② Convex logic may be kept but must read as Mente OS v2's own, never naming the vendor.

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | piece | status |
|---|---|---|---|
| 1 | ⭐ the WHOLE cracked-dev methodology, transversal to every discipline | `rules/rule-shipping-flow.md` | ✅ closed |
| 1b | what is backend-SPECIFIC stays in the discipline file | `principles/expertise/dev-backend.md` | ✅ closed |
| 2 | the query/access failure patterns, rewritten — no vendor named | `principles/expertise/dev-database.md` | ✅ closed |
| 3 | what reaches the frontend, as Mente OS's own logic | `principles/expertise/dev-frontend.md` | ✅ closed |
| 4 | decide: does the git/PR flow belong to a discipline or to a rule of its own? | §G-5 decision | ✅ closed |
| 5 | fix the 3 defects `grade-block` revealed while grading this block | `bin/grade-block` | ✅ closed |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- **⭐ EVERYTHING from `cracked-dev` goes in** (Brian, 2026-08-05): *"incorpóralo todo dentro del
  experto en programación, hay muchos apartados en donde es necesario y omitir algo no es algo
  bueno."* Rationale: the AI had proposed extracting only the ~40% Mente OS lacks. Brian overruled
  it — the judgement of what is "already covered" is itself criterion, and getting it wrong deletes
  something useful silently. **Where Mente OS already has a harder version, both are stated and the
  stricter one wins** (`rules/rule-inheritance.md`), instead of dropping the weaker.
- **⭐ Convex logic may be kept — the vendor may not** (Brian, 2026-08-05): *"hay que ver si nos
  sirven; si nos sirven hay que estructurar esa lógica, pero debe ser propio de Mente OS v2."*
  Rationale: measured, **Convex appears zero times in For3s** (stack: Python 3.12 + Postgres+AGE+
  pgvector; demo: Next.js + Neon). Copying 2,563 lines of a vendor's syntax into the file the hook
  INJECTS before every backend edit would put a database he does not have into context. The
  underlying failures are real and transferable; the API names are not.
- **⛔ `--dangerously-skip-permissions` does NOT come in.** Rationale: `cracked-dev` recommends it
  for autonomous spawns. It is the exact inverse of this project's 212 `deny` and 3 gates, and
  `PROJECT-RULES.md` §3 forbids proposing that a deny be lifted for convenience. Recorded here
  rather than silently omitted, because §F-1 says nothing is omitted: **it is refused, with reason.**
- **A skill is external material, never Brian's criterion.** Rationale: ADR-003. What comes from a
  skill is written as *"pattern imported from X"*, never inside a `✅ BRIAN'S CRITERION` block.
  Confusing the two would launder third-party opinion as the owner's judgement — the precise
  failure this whole expertise layer exists to prevent. Implemented as a `4-BIS` section in each
  file, with a red banner, leaving §2-§4 untouched and still pending.
- **§F-4 · ⭐ CORRECTED BY BRIAN, same day — the shipping flow is a RULE, not backend's property.**
  The AI first ruled it should stay inside `dev-backend.md` ("one subject, one home"). Brian
  overruled it: *"no solo los PR deben ir en backend, porque va a haber PR de frontend, de base de
  datos... deben estar esparcidas, debe haber reglas por experto."*
  **He was right, and it is measurable:** `hooks/pre-edit-standards.py` injects **only what the
  block declares in its §D**. A frontend block declares `dev-frontend.md` — so a flow living in
  `dev-backend.md` would **never reach it**. The agent shipping a frontend ticket would not know
  how to open the PR. Same for database.
  → Created `rules/rule-shipping-flow.md` (transversal, any discipline declares it in §D).
  `dev-backend.md` keeps only what is backend-specific, and all three expertise files point at it.
  ⭐ **The lesson:** "one subject, one home" was the right principle applied to the wrong axis. The
  axis is not *which topic* — it is **who needs it injected**. A rule that only reaches one
  discipline is not a home: it is a blind spot for the other two.
- **§G-6 · 🔴 THREE DEFECTS IN `bin/grade-block`, found by grading this block — all fixed.**
  Rationale for fixing them here instead of filing them: all three make the validator **report a
  verdict it did not measure** — the exact failure `rules/rule-checks-must-measure.md` forbids.
  Closing a block with a tool known to lie is not closing it.
  ① a comment between `## ✅ IN` and the first `- ` killed the scope **silently** → false ⬜ with
  every real metric green · ② `check-links` resolves from `Mente/`, `grade-block` from the repo
  root, so a §B satisfying one broke the other · ③ the layer-2 line was hardcoded *"still pending
  Brian"* and became a lie the day he filled it. Detail in this block's `docs/` closing report.
  ⭐ **Corrects the record:** the AI told Brian ADR-028 made 🟢 impossible for `docs` blocks *by
  design*. **Wrong.** The design was fine; the §B was mis-written and the parser failed silently.
  A defect assumed to be architectural lived in the thing doing the measuring.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- **`bin/grade-block` is graded by nothing.** Three real defects (§G-6) survived in the tool that
  issues every layer-1 verdict, and all three were found by accident — because a block happened to
  be mis-written in a way that exposed them. The battery covers `check-blocks`, `check-links` and
  `check-health`, but the SELF-TEST section has no case that feeds `grade-block` a deliberately
  malformed §B and asserts it refuses instead of returning a false ⬜.
  👉 **Proposal for Brian:** add that case to `bin/test-f0-f6` §SELF-TEST. Not done here — it is
  outside this block's Scope IN, and widening the scope to fix it would be the exact thing §B is
  for. Filed rather than silently done.
- **The archived-block naming convention breaks `grade-block`.** `distribucion` was archived as
  `distribucion_2026-08`, and the tool refuses any name with an underscore (*"lowercase, digits and
  hyphens only"*). So **a closed block can never be re-graded** — the verdict in its §K cannot be
  reproduced, which contradicts the reproducibility that architecture §12-Q.4 requires. Preexisting,
  not caused here.

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-08-05 · opened after reading **all 12 files of both skills in full** (3,157 lines), with the
  decisive measurement taken first: the vendor of the second skill appears **zero times** in For3s
- 2026-08-05 · §F-1 ✅ `dev-backend.md` §4-BIS.1-.8 — the full methodology: execution loop, the 8
  git anti-patterns, orchestration (max 2 agents), PR checklist, what makes a spec executable,
  the 6 setup layers, 8 backend failure patterns, branch/commit reference
- 2026-08-05 · §F-2 ✅ `dev-database.md` §4-BIS — 6 query/access patterns, vendor-free
- 2026-08-05 · §F-3 ✅ `dev-frontend.md` §4-BIS — only **3** patterns survived translation; the
  rest was vendor API. Recorded honestly rather than padded
- 2026-08-05 · 🔴 caught while measuring: writing the `⬜` glyph as an EXAMPLE in a header inflated
  `criterion.holes` from 8 to 9 in `dev-backend.md`. **Third time today** the same defect appears —
  a document that illustrates a marker corrupts the metric counting it

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context

**Why this block exists** (Brian, 2026-08-05): *"necesito que desmantelen estas skills y estén ya
incorporadas dentro del sistema de Mente OS v2, que formen parte de su código fuente, en especial
EXPERTO EN PROGRAMACIÓN."*

**The two sources, read in full before writing anything** (MIT both): `cracked-dev` (5 files, 594
lines — **methodology**: setup · execution · planning · orchestration + 3 templates) and
`convex-skill` (7 files, 2,563 lines — **framework knowledge**: vendor syntax, schemas, 8 pitfalls).

**Measured before deciding:** `grep -rl convex` over the whole repo → **zero matches**. For3s runs
Python 3.12 + Postgres+AGE+pgvector; the demo is Next.js + Neon. That single measurement is what
separates §F-1 (import the methodology) from §F-2 (translate the logic, drop the API).

**What `cracked-dev` genuinely adds** (measured against the engine): branch-per-ticket → verify →
PR → **do not merge** · the PR checklist · max 2 parallel agents · the scoped spawn template.
Everything else already exists here in a **harder** form (Método F, blocks, §H friction, a
160-check battery) — per §G-1 both are written and the stricter wins.

**The transferable patterns** are vendor-independent; the first — trusting a client-supplied
identity — is the same hole already closed in `verificacion.ts` and `container.ts`, which is
evidence it belongs in criterion, not that it is new.

**Working copies** stayed in the session scratchpad, outside the repo. Nothing was copied verbatim
into `Mente/` — §G-2 and §G-4.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing · 2026-08-05 — 🟢 PRODUCT

> Full evidence, dimension by dimension:
> **`blocks/archive/expertise-programacion_2026-08/docs/closing-report.md`**

| Criterion (`principles/owner-3-validation.md` §2) | Result |
|---|---|
| 1 · Functional | 🟢 `test-f0-f6` **160 passed / 0 failed** · `check-blocks` 0 errors · 284/284 citations |
| 2 · Sufficiency | 🟢 §A-E answer the 7 restart questions · both of Brian's rulings in §E |
| 3 · Quality | 🟢 layer 1 **3/3 applicable** + 🟢 layer 2 **6/6 dimensions**, evidence attached |

**Done:** both skills read in full (12 files, 3,157 lines) and absorbed —
`rules/rule-shipping-flow.md` (NEW, transversal: execution loop · 8 git anti-patterns · PR
checklist · branch reference · orchestration · executable specs · 6 setup layers) plus a `4-BIS`
section in each `dev-*` expertise file with what is specific to that discipline.

**Learned:**
> ⭐ **The axis for placing a rule is not what it is ABOUT — it is who needs it INJECTED.**
> A rule reaching one discipline is not a home; it is a blind spot for the others. Brian caught it.
> 🔴 **A validator nobody validates reports verdicts it never measured** — 3 defects in
> `grade-block` (§G-6), found only because a block was mis-written in a way that exposed them.

**Connections:** `blk-demo` unaffected (different repo, no shared Scope IN) · `bin/grade-block`
fixed ×3 · the 3 `dev-*` files gained a §4-BIS · **criterion holes untouched at 51** — this block
imported external material and never wrote inside Brian's §2-§4.

**Debt NOT closed** → `memory/PENDIENTES.md`: ① `grade-block` has no self-test (§H) · ② an archived
block cannot be re-graded — the underscore in `<name>_YYYY-MM` is refused by the name validator
(§H) · ③ no **workspace cheat sheet** exists (layer 2 of the new rule §7): that information is
scattered across the server memory, `Mente/secrets/` and `mente.config.yml`.
