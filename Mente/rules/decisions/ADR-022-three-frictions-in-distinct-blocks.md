# ADR-022 · Three frictions in distinct blocks

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

A rule is flagged for review at 3 frictions in DISTINCT blocks. It never expires, and the rule is never changed automatically — it escalates to Brian.

## Rationale

Arithmetic, not interpretation: a mechanism that needs judgment to fire does not fire. Rejected alternative: count repetitions within one block — any long task would raise false alarms.

## Evidence

none — mechanism design.

## Reverting

Count raw repetitions; expect false alarms and then the mechanism gets ignored.
