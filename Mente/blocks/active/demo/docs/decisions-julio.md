# DECISIONES DE JULIO · blk-demo-2026-07
**Status:** current · **Type:** block · **Updated:** 2026-08-05 · **Owner:** brian
**Block:** `blocks/active/demo` §G · **Split:** 2026-08-05, `doc-structure.md`

## Purpose

Las 7 decisiones de julio del bloque `demo`, movidas ÍNTEGRAS desde su §G cuando el BLOCK.md pasó
su techo de 200 líneas. ⛔ **No se resumió ni se borró nada** — `doc-structure.md`: sobre el techo
un documento SE PARTE y las mitades se apuntan; nunca se borra historia para que un check pase.

Cubren los sub-bloques **1-6, todos `closed`**. Las decisiones VIVAS siguen en el §G del bloque.

---

## Las 7 decisiones

- 2026-07-26 · default `hoteles` to `sin-tema`, NOT `general`. (commit 1c54a49)
  Rationale: `general` is a RESERVED name — the owner's private thread. As a default it
  would have routed guests into the owner's own space. See rules/case-dangerous-default.md
- 2026-07-26 · rollout order: senders send the field first, receiver gets strict second.
  Rationale: the reverse breaks everything that does not send it yet. Side effect: the fix
  landed with no agent rebuild needed.
- 2026-07-26 · agent on/off via the DB as mailbox (model C), `/ctl` never exposed. (df6e93c)
  Rationale: exposing a control endpoint to the internet to flip a boolean is not worth it.
- 2026-07-26 · **only the OWNER** can turn the agent off. (df6e93c)
  Rationale: a guest holding a key could switch off the owner's agent.
- 2026-07-26 · drop the `kind` column and the `demo_accounts` table. (5f86bed, closes C6p2)
  Rationale: `kind` (a cookie value) was used as if it were the real instance — the same bug
  surfaced in 6 files. Applied `rules/rule-fix-not-patch.md` (all 6 evaluated before writing,
  not one patched) and `principles/expertise/dev-database.md` (a column dropped, not shadowed).
- 2026-07-29 · lane `full-block` computed from the measured graph, not from judgement.
  Rationale: `rules/rule-lanes.md` — session.ts and userStore.ts propagate to 12 files each.
- 2026-07-29 · **a dependent is a file that IMPORTS the piece, not one that mentions it.**
  Rationale: `instancias.ts` had 26 mentions and 9 real imports. A comment naming a file is
  not a dependency; counting it inflates the lane. Build artifacts are copies, not dependents.

<!-- ══ G-BIS · QUALITY VERDICT ══ measured, never asserted ══ -->
## Quality verdict · 2026-07-30 · `bin/grade-block demo` · type `code`

| Metric | Value | |
|---|---|---|
| secret values written down | 0 | 🟢 |
| files nobody imports (dead code) | **1** | 🔴 |
| exports never imported | 0 | 🟢 |
| duplicated blocks (>=8 lines) | 0 | 🟢 |
| **test files** | **0** | 🔴 |
| import cycles | 0 | 🟢 |
| dependent counts gone stale | 0 | 🟢 |

**LAYER 1 VERDICT: 🔴 MVP** — not a product yet.

**The two reds:**
- `components/demo/ConnectClaude.tsx` — **145 lines, 0 importers, untouched since 2026-06-16.**
  Verified: the only occurrence of its name is its own `export default`.
- **0 test files** in the entire site. Sub-block 8 exists for this.

**Reproducible:** `bin/grade-block demo --root ../marca-personal`. Same numbers before and after a
`/clear` — that is the point (architecture §12-Q.4).

**Layer 2** (senior criterion, 6 dimensions) pending: `rules/qa-dimensions.md` needs Brian's input.

---

Related: `blocks/active/demo/BLOCK.md` §G (las decisiones vivas y el puntero a este archivo).
