# ADR-021 · When an error becomes a case

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

An error becomes a reusable case only if it passes three questions: would it recur elsewhere, was the cause a wrong CRITERION, can it be written as an actionable rule. Plus: automatic threshold at 2 repetitions, and a cap of 12 active cases.

## Rationale

If every error becomes a case, there are 80 in three months and none gets consulted. Rejected alternative: no filter.

## Evidence

Calibrated against real errors: the `general` default passes; the heredoc bug does not (it is a fix). Precedent: files without a declared limit all overflowed.

## Reverting

Remove the filter or the cap; the case folder becomes the new 240 KB file nobody reads.
