# CONNECTIONS · plan-tests-demo
**Status:** current · **Type:** block · **Updated:** 2026-08-05 · **Owner:** brian

## Purpose

Which blocks and pieces this one touched, so a later change knows what it moves. Step 6 of the
closing procedure (`principles/owner-3-validation.md` §5).

---

## 1 · Blocks affected

| Block | How | State it leaves it in |
|---|---|---|
| `blocks/active/demo` | ⭐ **directly.** §F-7 now says *held by a red test*; §F-8 went from *0 test files* to *② done, ① ③ ④ pending* | 🟡 still 🔴 MVP — **one** of its two reds closed (`test files 0 → 1`); the other is the dead file `components/demo/ConnectClaude.tsx` (§F-10) |
| `blocks/archive/expertise-programacion_2026-08` | consumes it — `val-functional.md` and `doc-planning.md` were **used in anger** here for the first time | unchanged; this is the field evidence it was missing |

⛔ **No other block declares these pieces.** `bin/check-blocks`: 0 errors — no overlapping `Scope IN`.

---

## 2 · Pieces touched outside Mente

| Piece | Change | Consequence |
|---|---|---|
| `marca-personal/tests/autorizar.test.ts` | 🆕 created | first test in the repo's history |
| `marca-personal/vitest.config.ts` | 🆕 created | ⚠️ the `@/*` alias is **required** — `tsconfig.json` declares it and without mirroring it no `lib/demo/*` import resolves |
| `marca-personal/package.json` | `test: vitest run` + Vitest 4.1.10 as devDependency | the repo has a test command for the first time |

⛔ **`lib/demo/allowedEmails.ts` was NOT modified.** It is read by the test, never touched — fixing
it is `demo` §F-7, and it needs Brian's datum.

---

## 3 · What a future change should know

- **The red test is load-bearing.** Anyone making the suite green without fixing `DEV_FALLBACK`
  has removed the only thing measuring the hole. See `SUMMARY.md` §2.
- **Nothing is committed.** A `git status` in `marca-personal` shows 4 entries; that is expected,
  and pushing to `main` deploys to production.
- **The §F state cell is machine-read** by `hooks/pre-edit-standards.py`. One bare word.

---

Related: `SUMMARY.md` (what it delivered) · `BLOCK.md` §H (the friction escalated to Brian) ·
`blocks/active/demo/BLOCK.md` (the block that inherits the open work).
