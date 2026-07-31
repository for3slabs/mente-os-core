# ADR-020 · Approval receipt on block

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

When a gate blocks, an APPROVAL RECEIPT is emitted: one screen with the piece, its propagation, the construction assessment, and approve/inspect/deny.

## Rationale

Blocking without an exit is pure friction. Rejected alternative: block with a bare error message.

## Evidence

none — adopted from an external reference (action receipts).

## Reverting

Remove the receipt; gates become walls.
