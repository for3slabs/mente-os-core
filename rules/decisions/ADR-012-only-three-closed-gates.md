# ADR-012 · Only three closed gates

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

Only three actions block: editing a piece with declared dependents, touching the database, closing a block without passing sufficiency. Everything else warns.

## Rationale

The gate logic: protect FEW things and it gets honored 100% of the time. Rejected alternative: block twenty things — the system becomes friction and gets disabled.

## Evidence

The Puentes gate protects one thing and has 100% measured compliance.

## Reverting

Add more gates and watch adoption fall; or remove them and lose the only real enforcement.
