# ADR-026 · Permission granularity is the mechanism

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

A permission's granularity is the MECHANISM, not the invocation. `Bash(sshpass *)`, not 234 literal variants.

## Rationale

1,341 entries cannot be audited by anyone; that is how the NavigoX contradiction slipped in. Test: does this entry authorize something no other entry already authorizes? Rejected alternative: literal per-command entries — the current state.

## Evidence

1,341 -> 127 entries after applying it (-91%), with `rm` deliberately kept literal.

## Reverting

Re-approve command by command; the list grows back.
