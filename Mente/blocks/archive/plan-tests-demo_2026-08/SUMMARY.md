# SUMMARY · plan-tests-demo
**Status:** current · **Type:** block · **Updated:** 2026-08-05 · **Owner:** brian
**Closed:** 2026-08-05 · **Layer 1:** 🟢 PRODUCT (`bin/grade-block plan-tests-demo`)

## Purpose

What this block delivered, what it deliberately left open, and the two lessons worth carrying —
so nobody has to reopen `BLOCK.md` to know whether it can be trusted.

---

## 1 · What it delivered

**Two artefacts, both verified:**

1. **`blocks/archive/plan-tests-demo_2026-08/docs/plan-critical-paths.md`** — the four critical paths of the demo, each carrying the four
   fields `principles/expertise/doc-planning.md` §2.5 demands: **datum · command · what failure
   looks like · who signs it.** Order chosen by Brian, rationale written per path.
2. **`marca-personal/tests/autorizar.test.ts`** — ONE test of path ②, as proof the plan executes
   rather than describes. **Measured: 5 pass · 1 fails on purpose.**

📊 **BEFORE → AFTER → BRIDGE**

| | before | after | what actually changed |
|---|---|---|---|
| test files in the demo | 🔴 **0** | 🟢 **1** | one of `blk-demo`'s two layer-1 reds closed |
| test runner | 🔴 **none** | Vitest 4.1.10 | the repo had `dev · build · start · lint` and zero test deps |
| sub-block 7 of `demo` | a paragraph | 🔴 a red test | it has a **definition of done**, not a description |

---

## 2 · The one thing to understand before touching it

🔴 **`tests/autorizar.test.ts` fails today, and that is the deliverable.**

`lib/demo/allowedEmails.ts` carries a `DEV_FALLBACK` that authorizes `jazz@example.com` when the
env var is missing — an address nobody controls. The test asserts it should be refused; it is not.
Output, measured: `expected false, received true`.

⚠️ **Do not "fix" it by weakening the assertion.** `val-functional.md` §2.2: *a check must be seen
failing before its green means anything.* Its green **is** the definition of `blocks/active/demo`
§F-7 closing, and closing that needs a datum only Brian holds — **who owns jazz and mashe.**

---

## 3 · ⛔ What it did NOT do, on purpose

- **Did not fix `DEV_FALLBACK`** — that is `blocks/active/demo` §F-7, blocked on Brian.
- **Did not write the other three tests** — ① ENTER · ③ TALK · ④ POWER stay in `demo` §F-8, in the
  order the plan justifies.
- **Did not commit and did not push.** `PROJECT-RULES.md`: Vercel deploys `marca-personal` from
  `main`, so a push there **is a production deploy.** Files are on disk, tree otherwise clean.

---

## What was learned

🔴 **A validator reads the cell, not the intent.** Decorating a §F state cell with
`active · 🔴 red test holds it` silently disabled the unclosed-sub-block warning in
`hooks/pre-edit-standards.py` — its row pattern expects a bare `\w+` there. The battery caught it;
**nothing else would have.** The §F state column is a machine-read interface: one bare word, nuance
goes in the description column. Escalated in §H.

⚠️ **`grep -rl` counts files; `grade-block` counts references.** My count said `allowedEmails` had
1 importer, the validator said 2 — one file importing two symbols. **The validator's number is the
one that governs**, because it is the one the check compares against.

---

Related: `blocks/archive/plan-tests-demo_2026-08/BLOCK.md` (the full record) ·
`blocks/archive/plan-tests-demo_2026-08/docs/plan-critical-paths.md` (the plan itself) ·
`blocks/active/demo/BLOCK.md` §F-7 and §F-8 (where the open work lives) ·
`principles/expertise/val-functional.md` §2.2 (why a red test is proof).
