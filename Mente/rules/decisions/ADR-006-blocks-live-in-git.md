# ADR-006 · Blocks live in git

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

Blocks live inside Mente OS, versioned in git.

## Rationale

A work unit whose history is not versioned cannot be audited. Rejected alternative: a separate store outside git.

## Evidence

The ~87 memories live outside git — when something breaks there, there is no history to revert.

## Reverting

Move blocks out of git; lose their history.
