# ADR-011 · Four layers guarantee reading

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

Four layers guarantee a file is actually read: router in CLAUDE.md, the block declares it, a hook injects or blocks, a validator checks at close.

## Rationale

Existing != findable != READ. The Método F satisfied the first two and failed the third. Rejected alternatives: telling CLAUDE.md to read it (already does, failed) and embedding all standards in CLAUDE.md (startup would go from 38K to hundreds of thousands of tokens).

## Evidence

The Método F was never read in 2 of 5 analyzed sessions — including the demo session, 1,276 requests, 0 reads.

## Reverting

Drop the hook layer; reading depends on the AI's judgment again.
