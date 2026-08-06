# ADR-030 · The block message IS the receipt

date: 2026-08-02
status: accepted
decided-by: brian
supersedes: ADR-020 (approval receipt on block)
superseded-by: —

## Context

ADR-020 decided that a blocking gate would emit an **approval receipt**: "one screen with the
piece, its propagation, the construction assessment, and approve/inspect/deny". It was the only
ADR whose own `Evidence` field read `none — adopted from an external reference (action receipts)`.

Measured 2026-08-02, auditing all 29 ADRs for traceability:

| | |
|---|---|
| Files mentioning `receipt` in `hooks/` or `bin/` | **0** |
| ADRs with no measured evidence | **1** — this one |
| ADRs never implemented | **1** — the same one |

That correlation is the finding, not the gap: **a decision adopted from an outside reference,
with no pain of our own behind it, is the one nobody builds.**

But the audit also showed the gap was not what it looked like. Of the four things ADR-020 asked
for, `hooks/gate-critical.py` already emits three, on every block:

```
🔴 BLOCKED · <the PIECE> destroys data with no rollback.
   A migration that cannot go back is the one mistake with no undo.   ← why
   Add a down/rollback section, or state in §G why it is one-way.     ← what to assess
   Bypass: edit it outside this session, and log the reason in §H.    ← the way out
```

What ADR-020 set out to prevent — *"blocking with a bare error message"* — never happened. The
gates were built with the exit built in, which is also what `rules/rule-friction.md` demands.

## Decision

The gate's block message **is** the receipt: piece, reason, what to assess, and the documented way
out — printed as text, not as a screen. There is no separate receipt artifact, and no
approve/inspect/deny flow.

## Rationale

Rejected alternative: build the receipt as specified. It would add a fourth element (propagation)
to a message that already works, at the cost of editing `gate-critical.py` — one of the only three
closed gates (ADR-012) — for a mostly cosmetic gain. A `PreToolUse` hook has no interface for an
interactive approve/inspect/deny, and faking one would be worse than not having it.

The receipt's real content is delivered by the piece that owns each part: the **lane** carries the
propagation (`rules/rule-lanes.md` — chosen from the graph, never from judgment), and the
**construction assessment** is `rules/rule-fix-not-patch.md` §2, which the gate's message points at.

## Evidence

`grep -rl receipt hooks/ bin/` → 0 files, 2026-08-02. Three of ADR-020's four elements verified
present in `gate-critical.py` (GATE 2 and GATE 3 messages). GATE 1 already computes propagation
for its warning, so the information exists — it is simply reported by the lane instead of by a
receipt.

## Reverting

Set this back to `proposed` and reinstate ADR-020. The work it would require is bounded and known:
reuse GATE 1's dependent-count in the GATE 2 and GATE 3 messages, ~20 lines plus tests that the
gates still block what they must.

---

Related: `ADR-020-approval-receipt-on-block.md` (superseded) · `ADR-012-only-three-closed-gates.md`
(the gates this touches) · `rules/rule-friction.md` (every block prints its way out) ·
`rules/rule-lanes.md` (where propagation is actually reported) · `rules/rule-fix-not-patch.md`
(the construction assessment).
