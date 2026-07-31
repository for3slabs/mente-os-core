# ADR-004 · Three friction lanes

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

Three lanes — direct, task, full-block — and the lane is chosen by PROPAGATION, not by the AI's judgment.

## Rationale

If every task went through all three owners the system becomes unbearable and gets abandoned. Rejected alternative: the AI estimates the lane — it would mislabel work as trivial.

## Evidence

'Guarda la API key en la instancia real' looked like a task; `userStore.ts` had 5 dependents. It produced 21 edits and 42% of commits as fixes.

## Reverting

Single lane for everything: either unbearable friction or no protection.
