# ADR-023 · Us english for instructions

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

Everything the AI reads as an INSTRUCTION is in US English — including `BLOCK.md`. Brian's thinking stays in Spanish.

## Rationale

The AI resolves English paths and fields precisely, and English is the language of every convention this builds on. Rejected alternative: everything in Spanish — loses precision in fields and names.

## Evidence

Verified: writing in Spanish does not degrade comprehension. The fix-over-fix problem did not come from language.

## Reverting

Translate instructions back to Spanish; precision in field and path resolution degrades.
