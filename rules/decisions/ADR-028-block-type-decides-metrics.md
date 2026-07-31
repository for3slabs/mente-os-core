# ADR-028 · A block declares its TYPE, and the type decides which metrics are measured

date: 2026-07-30
status: accepted
decided-by: brian
supersedes: —
superseded-by: —

## Context

`bin/grade-block` (phase F4) was built and run against the first real block, `demo`, which is a code
block. Brian then asked the question that exposed the gap: *"solo está para demo o para todo el
sistema, porque lo vamos a ocupar en todo el sistema."*

The script itself is generic — measured 2026-07-30, it contains **zero** references to `demo`,
`marca-personal` or `for3s`; it takes the block name as an argument and reads the scope from the
block's own §B IN. But every metric it computes is code-shaped: importers, tests, duplication,
import cycles.

## Decision

`§A` of `BLOCK.md` gains a **required** `type` field: `code | docs | infra | data`.
`bin/grade-block` measures only the metrics that apply to that type, and prints every
non-applicable metric as `n/a` **with the reason it was skipped**.

Two hard rules:
1. `n/a` is never counted as green.
2. The type does not lower the bar, it changes the ruler — every type still reaches a verdict.

## Rationale

A validator that can never go green is a validator you learn to ignore, and then the doctrine is
back to being a document — which is the exact failure v2 exists to fix (document-only rules comply
40-60%, code-enforced rules comply 100%).

Rejected alternative: refuse to grade non-code blocks. That leaves docs and infra blocks closing on
the AI's word, which is the original pain — *"me dijo todo está perfecto, le di /clear y me dijo
sigue roto."*

## Evidence

Measured against Brian's own pending list in `memory/PENDIENTES.md`:

| Pending block | Would score | Why it is wrong |
|---|---|---|
| rename the 208 files | 🔴 MVP, permanently | 0 tests and 0 importers — it has no code |
| decide the hosting | 🔴 MVP, permanently | no files to import at all |
| split the architecture | 🔴 MVP, permanently | a `.md` cannot have a test file |

Three of the seven registered pendings would have been graded 🔴 forever by a validator that was
working correctly.

## Reverting

Drop the `type` field and the per-type metric table; `grade-block` returns to code-only metrics and
must then be forbidden on non-code blocks, or it will report false reds.
