# ADR-003 · Brian owns the criterion

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

Brian designs the expert criterion. The AI only gives it form — it never invents criterion.

## Rationale

The current state came from the opposite: *"todo está hecho como la IA quiso, nunca ocupaste nada como base."* Rejected alternative: extract criterion from existing code (Agent OS style) — applied to the demo it would extract the vibecoding.

## Evidence

`userStore.ts` edited 21 times would become the standard if criterion were extracted from code.

## Reverting

Let the AI draft criterion; expect generic output like *"use best practices"*.
