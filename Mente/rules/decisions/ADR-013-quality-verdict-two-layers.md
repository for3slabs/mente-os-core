# ADR-013 · Quality verdict two layers

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

The quality verdict has two layers: measurable by script, and criterion across 6 dimensions each with REQUIRED EVIDENCE. Master rule: the AI does not declare, it reports the measurement.

## Rationale

A verdict that changes with the AI's context is not a verdict, it is a mood. Rejected alternative: trust the AI's assessment — it demonstrably flips.

## Evidence

24-jul 21:15 *'el sistema está completo'* -> 26-jul 06:33 (9 minutes after a /clear) *'lo implementa a medias'*. Same code, opposite verdicts.

## Reverting

Return to AI-asserted quality; the contradiction returns with it.
