# ADR-009 · Single file per block

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

One block = ONE file (`BLOCK.md`, sections A-K, <=150 lines). Tiers are the order of sections inside it, not separate files.

## Rationale

Splitting 70 lines across files saves nothing and adds places that desynchronize. Rejected alternative: 7 files per unit (internOS style) — its premise is a chat-first agent, not ours.

## Evidence

`memory/RETOMAR.md` (203 lines, one file) is what works best in Mente OS; the demo scattered across 5 `DEMO_*.md` is what works worst — nobody knows which to open.

## Reverting

Split into multiple files; reintroduce the sync problem.
