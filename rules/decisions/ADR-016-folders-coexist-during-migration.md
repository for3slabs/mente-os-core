# ADR-016 · Folders coexist during migration

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

The new folder structure COEXISTS with the old one. Zero broken pointers.

## Rationale

218 unique paths cite the current folders across documents; a rename without coexistence breaks them silently. Rejected alternative: rename and fix afterwards.

## Evidence

A broken markdown link throws no error — it surfaces weeks later.

## Reverting

Force a hard cutover; expect silent breakage.
