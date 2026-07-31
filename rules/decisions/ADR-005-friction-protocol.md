# ADR-005 · Friction protocol

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

When a rule gets in the way: comply, log the friction, continue, and propose the change at block close. Exception: stop immediately on real damage.

## Rationale

Asking every time makes Brian a bottleneck; changing rules unilaterally means the rules become the AI's again within a month. Rejected alternative: allow the AI to skip a rule it judges wrong.

## Evidence

none — process design.

## Reverting

Remove the log; rule evolution stops being evidence-based.
