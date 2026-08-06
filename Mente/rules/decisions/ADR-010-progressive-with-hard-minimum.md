# ADR-010 · Progressive with hard minimum

date: 2026-07-27
status: accepted
decided-by: brian
supersedes: —
superseded-by: —

## Context

Taken during the v2 design session (2026-07-27). Full reasoning lives in
`docs/Arquitectura_Mente_OS_v2_Bloques.md`; this record exists so the decision has its own
traceable, revertible file (see `rules/contract-adr.md`).

## Decision

Opening a block requires only 4 fields (identity, scope, connections, required standards). Closing requires everything plus the sufficiency check.

## Rationale

If opening costs 10 fields, work happens WITHOUT a block and everything is lost. Rejected alternative: strict from the start — the Método F is strict and went unread in 2 of 5 sessions.

## Evidence

The 4 required fields are exactly the ones that do not exist today, and whose absence caused every measured problem.

## Reverting

Make it strict at open; expect the block to be skipped.
