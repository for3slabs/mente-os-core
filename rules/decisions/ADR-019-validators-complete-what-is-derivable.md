# ADR-019 · Validators complete what is derivable

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

Validators do not only verify: they COMPLETE what is derivable (graph, index, drafts marked `auto:`). They never complete criterion, scope or verdict.

## Rationale

A validator that only warns would have warned 5 times and we would still have 5 unregistered sessions. Rejected alternative: verify-only.

## Evidence

The rule *'sin registro no hay /clear'* has existed since 14-jul and was broken 5 of 11 times.

## Reverting

Restrict validators to reporting; the omissions persist.
