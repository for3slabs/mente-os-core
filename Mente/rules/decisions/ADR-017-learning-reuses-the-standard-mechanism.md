# ADR-017 · Learning reuses the standard mechanism

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

Learning cases are consulted through the SAME mechanism as standards: the block declares them, the hook injects them. No new mechanism.

## Rationale

Steps 1-5 of learning already work (the case gets written well). Step 6 fails: nothing guarantees it gets read. Rejected alternative: a separate retrieval system — more machinery for the same gap.

## Evidence

`case-dangerous-default.md` exists and is well written; nothing guarantees it is consulted before the next default is chosen.

## Reverting

Build a separate consultation path; two mechanisms to keep in sync.
