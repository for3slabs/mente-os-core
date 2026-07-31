# ADR-014 · Brian owns qa criterion

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

Brian supplies the 6 QA dimensions per discipline. The AI applies them and brings the evidence — it never issues its own opinion.

## Rationale

This is what differentiates v2: four mature frameworks were analyzed and none answers *is this a product or an MVP?*. Rejected alternative: AI-generated dimensions — that is a linter, not a senior.

## Evidence

internOS, Agent OS, Open SWE and OpenTag: zero quality verdicts among them.

## Reverting

Let the AI write the dimensions; layer 2 degrades into layer 1.
