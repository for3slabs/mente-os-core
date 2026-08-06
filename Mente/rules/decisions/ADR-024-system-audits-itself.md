# ADR-024 · System audits itself

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

`bin/check-health` audits the system's own health and runs by itself at SessionStart. Rule: if you have to ASK for it, it is not automated. It never deletes forensic evidence.

## Rationale

Three failures lived for WEEKS and were found by Brian asking. Rejected alternative: manual audit on request — that is exactly what failed.

## Evidence

additionalDirectories granting NavigoX access (weeks) · registro.md claiming 173 docs when there were 195 · 999 stale files.

## Reverting

Unhook it from SessionStart; the system stops watching itself.
