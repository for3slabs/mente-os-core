# ADR-002 · Who the system is for

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

The system exists so the AI works better with expert rules, and so anyone entering works with the same criterion.

## Rationale

Brian: *"es para que trabajes mejor con reglas de personas que ya saben del tema y que también tengan el mismo criterio."* Rejected alternative: for the AI only — it would not be shareable.

## Evidence

none — framing decision.

## Reverting

Narrow the scope to the AI alone; the system stops being portable to collaborators.
