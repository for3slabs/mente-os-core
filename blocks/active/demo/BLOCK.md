# BLOCK · demo

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-demo-2026-07
type: code
intent: turn the web demo from an MVP into something that can be handed to a client
status: active · lane: full-block
owner: brian
created: 2026-07-24 · updated: 2026-07-29

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- marca-personal/lib/demo/*.ts · components/demo/* · components/for3s-admin/*
- marca-personal/app/api/demo/**
- Neon DB `for3s_demo` (demo_* tables)

## ⛔ OUT
<!-- Only limits SPECIFIC to this block. System-wide rules are not repeated here —
     they apply with or without a block and live in CLAUDE.md / base-rules.md.
     Repeating them made this block look like their source, which it is not. -->
- DO NOT touch the For3s-OS agent (`for3slabs/for3s`) — separate repo. This block only
  CONSUMES 5 endpoints: /v1/chat · /v1/conector · /v1/miskeys · /v1/oauth · /v1/token
- DO NOT change `api_channel.py` — DERIVED: it lives in the agent's repo, so by the
  block-lifecycle.md §2 test it is separate work, not a sub-block of this one
- DO NOT touch the admin panel's non-demo sections — outside this block's intent

## 🌐 System-wide rules that also apply (inherited, not owned here)
- `CLAUDE.md`: never touch marca-personal/Mente/ · never read ~/5M-incubathon/ without the gate
- `base-rules.md` #7: server-first — push to GitHub only on explicit order
  ⚠️ Vercel deploys from `main`, so **any push to main is a production deploy**

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: the For3s-OS agent via the API channel (`/v1/chat`) — not yet a block
- DEPENDED ON BY: none declared
- ISOLATED FROM: everything else in Mente OS
- 🔴 CRITICAL PIECES (imports measured 2026-07-29 with `bin/new-block --piece`):
  - lib/demo/session.ts → 12 · lib/demo/userStore.ts → 12
  - lib/demo/instancias.ts → 9 · for3sChat.ts → 6 · eventos.ts → 6

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
## Required standards
- rules/rule-fix-not-patch.md
- rules/rule-lanes.md
- rules/case-dangerous-default.md
- principles/expertise/dev-database.md
<!-- expertise/dev-frontend.md removed 2026-07-30 (bin/check-applied): 6 closed sub-blocks, zero
     frontend decisions. Re-add when sub-block 10 touches a component. -->

<!-- ══ E · STATE ══ ≤10 lines ══ -->
## State
phase: 6 files raised to product; 3 blockers remain before it can be handed over
next: sub-block 7 — jazz/mashe owners into the DB, delete allowedEmails.ts DEV_FALLBACK
blockers: sub-block 9 waits on the hosting decision → BRIAN
progress: 6/9 sub-blocks closed
updated: 2026-08-02
note: untouched through 2026-08-03 (S7 built the v2, S8 hardened it, S9 made it installable).
      A stale date here is not forgotten work: the blockers are where 2026-07-26 left them.

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | imports | status |
|---|---|---|---|---|
| 1 | DB-only bridge, no env (I1-I5) | lib/demo/instancias.ts | 9 | closed |
| 2 | single guard, 12 copies to 0 (S1-S3) | lib/demo/session.ts | 12 | closed |
| 3 | brute-force protection (V1-V4) | lib/demo/verificacion.ts | 2 | closed |
| 4 | safety net + identity without `kind` (U1-U6) | lib/demo/userStore.ts | 12 | closed |
| 5 | per-instance telemetry | lib/demo/eventos.ts | 6 | closed |
| 6 | real agent on/off, owner only (model C) | lib/demo/container.ts | 1 | closed |
| 7 | jazz/mashe owners to DB, drop DEV_FALLBACK | lib/demo/allowedEmails.ts | 1 | active |
| 8 | tests for the 5 critical paths | (no file — **0 test files exist**) | 0 | open |
| 9 | decide the hosting | (infrastructure) | 0 | blocked |
| 10 | delete the orphan (0 importers since 2026-06-16) | components/demo/ConnectClaude.tsx | 0 | open |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
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

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- (none recorded)

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-07-26 · 1c54a49 · explicit topic sent by the site
- 2026-07-26 · 5f86bed · `kind` column and demo_accounts dropped
- 2026-07-26 · 793e858 · heartbeat + TTL — current HEAD of main

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context
Site repo `ElBrAyAn1967/For3s` — **not** the agent's. Branch `main` at `793e858`, clean.
Neon DB `for3s_demo`: `demo_instancias` is the single source of truth, 7 FKs, `demo_config`
editable without a push.
`DEMO_ENC_KEY` rotated and unified local=Vercel on 2026-07-26 — they had diverged since June
and a fallback was hiding it. Key lives in `Mente/secrets/`.
Reachable through the Tailscale Funnel — which means **it depends on Brian's laptop being on**.
Full chronology of the 2026-07-24/26 session: `memory/PENDIENTES.md` and the demo memories.

**Recovered docs** (moved here 2026-07-30 from `marca-personal/Mente/Doc/`, where the AI had
written them during the 2026-07-21 scope violations — see docs/):
- `blocks/active/demo/docs/demo-progress.md` — demo progress, June
- `blocks/active/demo/docs/guide-github-oauth-app.md` — ⭐ **operational step Brian still has to execute**
- `blocks/active/demo/docs/plan-piece-e-admin.md` — the Piece E admin plan

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — the block is still active)
