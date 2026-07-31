# ADR-007 · Closed blocks are archived

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

A closed block is archived as completed, detailed as consultable experience. It does not die.

## Rationale

Brian: *"se archiva como completado y está detallado todo como experiencia de memoria."* Rejected alternative: delete on close — loses the learning.

## Evidence

none — judgment call.

## Reverting

Delete closed blocks; the archive stops being a source of precedent.
