# ADR-008 · Migration on demand

date: 2026-07-27
status: superseded
decided-by: brian
supersedes: —
superseded-by: ADR-029-full-v1-to-v2-migration.md

## Context

Taken during the v2 design session (2026-07-27). Full reasoning lives in
`docs/Arquitectura_Mente_OS_v2_Bloques.md`; this record exists so the decision has its own
traceable, revertible file (see `rules/contract-adr.md`).

## Decision

Legacy work migrates to blocks ON DEMAND — when it is touched. What is never touched is never migrated. The demo is the deliberate pilot.

## Rationale

Migrating what will not be touched is work with no return, and it destroys the alive/fossil signal. Rejected alternative: bulk migration — the exact error that brought us here.

## Evidence

Of 194 .md files, only 97 are alive (touched since July). Half the tree is fossil.

## Reverting

Bulk-migrate; lose the modification-date signal that separates alive from fossil.

## Superseded 2026-07-30

On-demand migration was correct **while v2 was unproven** — moving 186 files before the structure
was validated would have been a bet. v2 is now built and verified (F0-F7, `bin/test-f0-f6` at
103/103), and the measurement showed the cost of waiting: **72% of the system still in v1 folders**.

→ `rules/decisions/ADR-029-full-v1-to-v2-migration.md` · plan: `docs/plan-v1-to-v2-migration.md`
