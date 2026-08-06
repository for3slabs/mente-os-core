# SUMMARY · split-architecture

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Closed:** 2026-07-30 · **Block:** `blk-split-architecture-2026-07` · **Block type:** docs
**Contract:** `rules/contract-archive.md`

## Purpose

What this block did, what it left behind, and the mistake not to repeat.

## What it was for

Split the 2496-line architecture into readable pieces without losing a single pointer.

## What was built

| # | Sub-block | Result |
|---|---|---|
| 1 | extract §3 THE BLOCK | `docs/architecture/block-anatomy.md` — 454 lines |
| 2 | extract §12-TER…SEPTIES | `docs/architecture/validators-and-hygiene.md` — 780 lines |
| 3 | extract §6+§7+§10 | `docs/architecture/lifecycle-and-learning.md` — 434 lines |
| 4 | entry point + 2 extra cuts | `docs/architecture/folder-structure.md` 292 · `docs/architecture/language-policy.md` 86 |
| 5 | declare every piece | 5 lines added to `Maestro/piezas.tsv` |
| 6 | verify | battery green · 0 broken pointers |

**2496 → 632 lines** in the entry point. Six files, each under its 800-line limit.

## The quality verdict

```
bin/grade-block split-architecture --root /home/brianweb3/for3s/Mente
secret values written down ... 0  🟢
broken links ................. 0  🟢
orphan docs .................. 0  🟢
LAYER 1 VERDICT: 🟢 PRODUCT
```

## ⭐ What was learned

**A split surfaces what nobody was measuring.** Moving §12-SEPTIES made `grade-block` read that
text for the first time — and it found **Brian's real SSH password**, written since 2026-07-27
inside an example of *"what NOT to do"*. It had survived every audit because no validator had ever
measured that file. **A password inside a bad-practice example is still a password**; the example
teaches just as well with an obviously fake value.

**The `-BIS`/`-TER` suffix was never a naming quirk — it was the file saying it held two distinct
things.** Every one of the 12 grown sections mapped exactly onto a cut. Once each group became its
own file the suffixes stopped meaning anything and were renumbered: keeping them would preserve the
scar of a problem already solved.

**A pointer in place beats a deletion.** Each extracted section left a stub saying where it went and
why, so the 46 documents citing the entry point kept resolving with zero edits elsewhere. Deleting
instead would have turned a 5-file split into a 46-document rewrite.

**Verified after every single cut: 0 content lines lost** — every line over 25 characters exists in
the new file or in the extracted piece. Measured five times, not assumed once.

## What was left out

- `rules/contract-block.md` (336/250) and `rules/NAMING_CONVENTION.md` (266/250) still exceed their
  limits. Deliberately out of scope (§B OUT): different files, and they would not close the same day
  for the same reason.
- The 46 documents citing the architecture still cite the entry point. That is correct — rewriting
  them belongs to the 208-file rename.

## Debt handed over

- `blk-208-rename` (not yet opened): the 11 documents declaring paths by hand →
  `Maestro/piezas.tsv`.

---

Related: `blocks/archive/split-architecture_2026-07/connections.md` · `rules/contract-archive.md` · `Maestro/piezas.tsv`.
