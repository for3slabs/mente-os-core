# ADR-025 · Config hygiene four rules

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

Four config hygiene rules: secrets are referenced never pasted; every path declares its reason; ONE MECHANISM ONE ENTRY; paths are portable.

## Rationale

In all three failures the rule existed or was obvious — what was missing was the MECHANISM. Rejected alternative: rely on discipline.

## Evidence

331 entries carrying the server password · 689 absolute paths · 3 of 9 paths dead · 234 entries for a single mechanism.

## Reverting

Drop the rules; config degrades again by accumulation.
