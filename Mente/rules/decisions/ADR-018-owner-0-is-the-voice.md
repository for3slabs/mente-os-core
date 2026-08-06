# ADR-018 · Owner 0 is the voice

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

Mente OS also governs HOW it communicates, via OWNER-0 (the voice) — transversal, not a fourth owner. Eight negative, checkable rules.

## Rationale

Brian used the same phrase for the code and the prose: *"se siente hecho por IA."* Same disease: producing correct form without judgment. Rejected alternative: vague guidance like *"be clear"* — that is the kind of instruction that causes the problem.

## Evidence

Measured: `CLAUDE.md` had zero style rules, `output-styles/` did not exist, `.claude/settings.json` had no `outputStyle`. Nobody had written the file.

## Reverting

Remove `outputStyle` from settings.json — one line, fully reversible.
