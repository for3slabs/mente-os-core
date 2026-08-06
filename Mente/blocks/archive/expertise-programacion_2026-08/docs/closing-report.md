# CLOSING REPORT · block `expertise-programacion`
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian

---

## Purpose

Long-form closing evidence for `blk-expertise-programacion-2026-08`. `BLOCK.md` §K carries the
verdict; this file carries the detail that would blow its 200-line ceiling
(`principles/owner-3-validation.md` §5 step 1: consolidate, long detail → `docs/`).

---

## The close · 2026-08-05 — 🟢 PRODUCT

| Criterion (`principles/owner-3-validation.md` §2) | Result |
|---|---|
| 1 · Functional | 🟢 `test-f0-f6` **160 passed / 0 failed** · `check-blocks` 0 errors · `check-links` 284/284 |
| 2 · Sufficiency | 🟢 §A-E answer the 7 restart questions · both of Brian's rulings recorded in §E |
| 3 · Quality | 🟢 layer 1 **3/3 applicable** + 🟢 layer 2 **6/6 dimensions** |

**Layer 1** · `bin/grade-block expertise-programacion` — secrets 0 · broken links 0 · orphan docs 0
→ 🟢 PRODUCT. (Three metrics are `n/a` for type `docs`; that is ADR-028, not a pass.)

**Layer 2 · criterion review** — second one ever run, evidence shown:

```
BLOCK expertise-programacion — criterion review · 2026-08-05
  1 architecture ... 🟢  the flow lives where it gets INJECTED, not where it thematically fits
                         evidence: hooks/pre-edit-standards.py injects only the block's §D →
                         a transversal rule reaches all 3 disciplines; inside dev-backend.md it
                         would have reached one. This was Brian's correction, §G-5
  2 data .......... 🟢  no value with an owner in any of the 4 files
                         evidence: grade-block "secret values written down: 0"
  3 abstraction ... 🟢  the flow is stated ONCE, pointed at 3 times — not copied
                         evidence: `do not merge` appears 2× in rule-shipping-flow.md and 1× in
                         dev-backend.md, and that one is the pointer line, not a duplicate
  4 naming ........ 🟢  `rules/rule-shipping-flow.md` says what it governs without opening it;
                         `4-BIS` marks imported material against §2-§4 which are Brian's
  5 contracts ..... 🟢  nothing dangles: all 4 files have named consumers, and what was REFUSED
                         is written down with its reason (--dangerously-skip-permissions, §G-3)
                         rather than silently dropped — the what·why·how of dev-database §2.5
  6 necessity ..... 🟢  every piece has a consumer
                         evidence: rule-shipping-flow.md ← the 3 expertise files + INDEX;
                         each 4-BIS section ← its own discipline's blocks
  ─────────────────────────────────────────────────────────────
  CRITERION VERDICT: 🟢 pass — six dimensions green
```

**What was done:** both skills read in full (12 files, 3,157 lines) and absorbed —
`rules/rule-shipping-flow.md` (NEW, transversal: execution loop · 8 git anti-patterns · PR
checklist · branch reference · orchestration · executable specs · 6 setup layers) plus a `4-BIS`
section in each of the three `dev-*` expertise files carrying what is specific to that discipline.

**What was learned:**
> ⭐ **The axis for placing a rule is not what it is ABOUT — it is who needs it INJECTED.**
> A rule reaching one discipline is not a home; it is a blind spot for the others. Brian caught it.

> 🔴 **A validator nobody validates reports verdicts it never measured.** Three defects in
> `grade-block` (§G-6), all producing false or stale output, found only because a block was
> mis-written in a way that exposed them.

**Connections:** `blk-demo` unaffected (different repo, no shared Scope IN) · `bin/grade-block`
fixed ×3 · the 3 `dev-*` expertise files gained a §4-BIS · **criterion holes untouched at 51** —
this block imported external material and never wrote in Brian's §2-§4.

**Debt NOT closed** → `memory/PENDIENTES.md`: ① `grade-block` has no self-test (§H) · ② an archived
block cannot be re-graded, the underscore in `<name>_YYYY-MM` is refused by the name validator (§H)
· ③ Mente OS has no **workspace cheat sheet** — layer 2 of §7 in the new rule — that information is
scattered across the server memory, `Mente/secrets/` and `mente.config.yml`.


---

Related: `blocks/archive/expertise-programacion_2026-08/BLOCK.md` §K (the verdict) ·
`rules/rule-shipping-flow.md` (what this block created) · `rules/qa-dimensions.md` (layer 2) ·
`principles/owner-3-validation.md` §4-5 (the closing procedure) · `bin/grade-block` (layer 1).
