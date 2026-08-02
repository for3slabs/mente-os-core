# ADR-027 · Size limits per document type

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

Size limits are declared PER DOCUMENT TYPE across the whole system, not only for blocks. Master rule: a file is split when it contains TWO DISTINCT THINGS — the limit is the SIGNAL, not the cause.

## Rationale

v2 had limits only for what it would create, not for what already exists nor for its own documents. Rejected alternative: one global limit — a logbook must be allowed to grow.

## Evidence

This architecture document went from 995 to 2,347 lines in ONE session. `memory/RETOMAR.md`, the only file with a declared limit, is the only one that never overflowed.

## Reverting

Remove the limits; expect the same drift that produced a 253 KB PENDIENTES.md.
