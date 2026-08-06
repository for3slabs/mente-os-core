# ADR-001 · Work unit is the block

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

A BLOCK is a unit of work grouping tasks that share one relation; a SUB-BLOCK is one task attacking one code piece.

## Rationale

One level cannot answer both questions. The block answers *what work depends on what work*; the sub-block answers *what code do I touch*. Rejected alternative: a single level — it loses the propagation graph.

## Evidence

The fix-over-fix comes from the missing second level: 'change where the key is stored' looked like one file and was six.

## Reverting

Collapse to a single level; the propagation graph is lost.
