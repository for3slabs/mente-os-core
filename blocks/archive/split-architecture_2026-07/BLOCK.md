# BLOCK · split-architecture

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-split-architecture-2026-07
type: docs
intent: split the 2496-line architecture into readable pieces without losing a single pointer
status: closed · lane: full-block
owner: brian
created: 2026-07-30 · updated: 2026-07-30

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- docs/Arquitectura_Mente_OS_v2_Bloques.md — the file being split
- Cuerpo/architecture/ — where the pieces will live
- Maestro/piezas.tsv — one line per piece that becomes canonical

## ⛔ OUT
- DO NOT change WHAT the architecture says. This block moves text, it does not rewrite design:
  a split that also edits content makes it impossible to tell a move from a change in review.
- DO NOT rewrite the 44 documents that cite it — citations keep resolving because the original
  filename stays as the entry point. Rewriting them is the 208-file rename, a separate block.
- DO NOT split `rules/contract-block.md` or `rules/NAMING_CONVENTION.md` here — same size
  warning, different file; they would not close the same day for the same reason
  (`rules/block-lifecycle.md` §2)

## 🌐 System-wide rules that also apply (inherited, not owned here)
- `CLAUDE.md`: never touch marca-personal/Mente · the gate to other Mente OS
- `base-rules.md` #3: report the measurement, never state

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: nothing — the split is self-contained
- DEPENDED ON BY: blk-demo-2026-07 (its §D standards point at rules born in this document)
- ISOLATED FROM: every other work in Mente OS
- 🔴 CRITICAL PIECE: measured 2026-07-30 — **44 documents cite this file**, and
  `bin/check-structure` reads `Maestro/piezas.tsv`, which will declare each piece.
  That propagation forces the lane to `full-block`, not the size of the edit.

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
## Required standards
- rules/contract-document.md
- rules/rule-fix-not-patch.md
- rules/NAMING_CONVENTION.md

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: CLOSED — 2496 → 632 lines, 5 pieces, verdict 🟢 PRODUCT
next: (none — archived)
blockers: none
progress: 6/6 sub-blocks closed
updated: 2026-07-30

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | imports | status |
|---|---|---|---|---|
| 1 | extract §3 THE BLOCK (435 lines) | architecture/block-anatomy.md | 0 | closed |
| 2 | extract §12-TER..SEPTIES (758 lines) | architecture/validators-and-hygiene.md | 0 | closed |
| 3 | extract §6 + §7 + §10 (415 lines) | architecture/lifecycle-and-learning.md | 0 | closed |
| 4 | leave the entry point: index + pointers | (the original file) | 0 | closed |
| 5 | declare every piece in piezas.tsv | Maestro/piezas.tsv | 0 | closed |
| 6 | verify 0 broken pointers + battery green | (verification) | 0 | closed |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- 2026-07-30 · lane is `full-block`, NOT the `direct` the scaffold guessed.
  Rationale: `rules/rule-lanes.md` — the lane comes from measured propagation. 44 documents cite
  this file and a validator reads a table that will name its pieces. Measured, not judged.
- 2026-07-30 · **the original filename stays as the entry point**, holding the index and the
  pointers. Rationale: 44 citations keep resolving with zero edits elsewhere. Renaming the entry
  turns a 3-file split into a 44-document rewrite — that is the 208-file rename, another block.
- 2026-07-30 · cut by MEASURED weight, not intuition: §3 alone is 435 lines, §12-TER..SEPTIES is
  758. Rationale: ADR-027 — the limit is the SIGNAL, and the grown sections mark exactly where
  content that did not fit was glued on.

- 2026-07-30 · sub-block 1 · §3 moved verbatim, replaced in place by a POINTER, not deleted.
  Rationale: `rules/rule-fix-not-patch.md` — the 46 documents citing the entry point keep
  resolving, and a reader landing on §3 is told where it went and why. Verified: **0 content
  lines lost** (every line >25 chars exists in the new file or the piece).

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- (none recorded)

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-07-30 · opened · measured 2496 lines / 800 limit · 12 grown sections
- 2026-07-30 · sub-block 1 closed · 2496 → 2078 · block-anatomy.md 454/800
- 2026-07-30 · sub-block 2 closed · 2078 → 1340 · validators-and-hygiene.md 781/800
- 2026-07-30 · sub-block 3+5 closed · 1340 → 945 · lifecycle-and-learning.md · 3 pieces in piezas.tsv

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context
The file is the HOW of Mente OS v2; `principles/vision-mente-os-v2.md` holds the why.
It grew from 995 to 2347 lines in ONE session (2026-07-27) and is now 2496 — **3× its declared
limit** — with 12 grown sections (`0-BIS` … `12-SEPTIES`) that are themselves the split signal
(ADR-027: a file is split when it holds TWO DISTINCT THINGS).

⚠️ Lines 499-567 are an **embedded BLOCK.md template**, not real sections. A naive parser reads
them as document structure; any tooling that cuts by heading must skip that range.

This is the second pilot (F8). The demo was migrated WITH its history, so it never exercised
opening a block at minute zero. This one did — scaffold in 0.18s, and **the scaffold's guessed
lane was wrong**, which is exactly what a second pilot is for.

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
Closed 2026-07-30 · verdict 🟢 PRODUCT · see blocks/archive/split-architecture_2026-07/
