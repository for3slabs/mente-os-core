# ADR-029 · Full v1 → v2 migration: move everything, in risk order, one file at a time

date: 2026-07-30
status: accepted
decided-by: brian
supersedes: ADR-008 (migration on demand)
superseded-by: —

## Context

> **Brian, 2026-07-30:** *"sigo viendo que estamos ocupando v1"* — and the measurement agreed:
> **186 of 258 documents (72%) still lived in v1 folders.**

ADR-008 chose migration ON DEMAND: a file jumps to v2 when someone touches it. That was correct
while v2 was unproven — moving 186 files before the structure was validated would have been a bet.
v2 is now built and verified (F0-F7, `bin/test-f0-f6` at 103/103), so the reason for waiting is gone.

What remained was the cost, measured rather than guessed: **1,586 citations to v1 documents, spread
across 209 documents.** Moving a file is not moving a file — it is rewriting its citations. And
twice on 2026-07-30 a bulk path rewrite broke real citations (4 corrupted filenames inside
`Maestro/`, 28 valid relative paths "completed" into non-existent absolutes).

## Decision

Migrate **everything** from v1 to v2, in four parts Brian confirmed:

1. **`Maestro/` → `registry/`** — yes, despite being a separate git repo with its own remote and
   three consumers (`maestro`, `maestro_lib.sh`, `indexador.py`). Done last, as its own phase.
2. **`Cerebro/` stays** — it is the architectural source of truth of **For3s OS** (the product),
   not of Mente OS (the method). Mixing them is worse than a naming inconsistency.
   Exception evaluated separately: `Cerebro/Registro_Conversaciones.md` belongs to Mente OS.
3. **The 157 uncited documents are ARCHIVED, not deleted** — they are the project's history.
   They keep their names: a renamed fossil loses its traceability.
4. **Filenames are NOT translated to English in this migration.** The 208-file rename stays a
   separate block: moving and renaming at once doubles the risk on the same files.

**Order is by risk, not by folder:** what nobody cites first, what is cited 80 times last, and
`memory/RETOMAR.md` at the very end — it is the first thing read after a `/clear`.

**Every file is moved by `bin/migrate-doc`**, one at a time: `git mv` + header + update its N
citations + verify, and **revert if anything breaks**.

## Rationale

The pending cost of ADR-008 was invisible but real: a system that looks half-migrated is a system
whose own map cannot be trusted, and `CLAUDE.md` was still injecting a rule from a v1 folder.

Rejected alternative: a single bulk `git mv` per folder. It was tried in miniature twice the same
day and broke citations both times. **A bulk rewrite is not safe because the mapping is right — it
is safe when something verifies the result afterwards.**

## Evidence

| Measured 2026-07-30 | |
|---|---|
| documents in v1 folders | **186** (72% of the system) |
| without a contract header | **184** |
| citations to rewrite | **1,586** across **209** documents |
| documents nobody cites (fossils) | **157** |
| most cited single file | `Cerebro/For3s_OS_Grafo_Maestro.md` — 80 citations |

Two bulk rewrites broke citations the same day, which is why the plan mandates per-file moves with
verification between each one.

## Reverting

`git mv` back per file; the plan keeps history so each move is a single revertible commit. What
cannot be reverted cheaply is a half-finished migration — hence the risk order, so an interruption
always leaves the system in a coherent state.
