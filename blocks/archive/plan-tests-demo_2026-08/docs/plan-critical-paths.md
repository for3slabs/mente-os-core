# PLAN · the demo's critical-path tests
**Status:** current · **Type:** plan · **Updated:** 2026-08-05 · **Owner:** brian
**Block:** `blocks/active/plan-tests-demo` §F-1 · **Judged by:** `principles/expertise/doc-planning.md`
**Estado:** ⬜ **NO EJECUTADO** — explicar antes de construir, aprobar antes de ejecutar

## Purpose

`blk-demo-2026-07` has **0 test files** and its sub-block 8 has been open since 2026-07-26 with
nothing written. This plan makes it executable: **which paths, in which order, and how each one
proves it works.**

> ⛔ **This plan does not write the tests.** It delivers the order and the criteria; the block that
> owns it writes ONE, as proof it executes (§B). The rest is `blk-demo` §F-8.

---

## 1 · THE MEASURED STATE — the BEFORE, without which nothing can be said to improve

| Measurement | Value | How |
|---|---|---|
| Test files in the demo | 🔴 **0** | `bin/grade-block demo --root ../marca-personal` |
| **Test runner** | 🔴 **none** | `package.json` declares `dev · build · start · lint` and zero test deps |
| Modules under `lib/demo` | 25 | `ls` |
| API routes | 20 | `find app/api/demo -name route.ts` |
| Layer-1 verdict of the block | 🔴 **MVP** | two reds: 0 tests · 1 dead file |

**Dependents, measured — they inform the order, they do not decide it:**
`session` 12 · `userStore` 10 · `instancias` 6 · `verificacion` 3 · `apiKey` 3 · `crypto` 2 ·
`container` 1 · `allowedEmails` 0.

⚠️ **`allowedEmails` has 0 importers and is still path ②.** The count measures blast radius, not
stake: that file authorizes a **fake email address** and is the reason the block cannot be handed
to a client. **A number is evidence, never a verdict** — Brian chose the four.

---

## 2 · THE FOUR PATHS — chosen by Brian, 2026-08-05

### ① ENTER — verify email → session → my instance

**Why:** it is the front door, and **it broke twice**: an owner got in with no code, and re-sending
the code reset the brute-force counter (`verificacion.ts` V1-V4).

| Field | Value |
|---|---|
| **Datum** | a wrong code is rejected · **the counter does NOT reset on re-send** · a valid code lands on the owner's OWN instance |
| **Command** | the runner chosen in §4, over `lib/demo/verificacion.ts` + `session.ts` |
| **What failure looks like** | the counter goes back to zero after re-sending → brute force is open again |
| **Who signs it** | 🤖 the test — it is a boolean, no judgement needed |

### ② AUTHORIZE — a guest must NOT reach what is not theirs

**Why:** ⭐ **the hole open TODAY.** `allowedEmails.ts` carries a `DEV_FALLBACK` that authorizes a
fake address. It is `blk-demo` sub-block 7 and the reason the block cannot ship.

| Field | Value |
|---|---|
| **Datum** | an address NOT in the DB is refused · **the fake `DEV_FALLBACK` address is refused too** |
| **Command** | the runner, over `lib/demo/allowedEmails.ts` + `acceso.ts` |
| **What failure looks like** | the fake address gets in — which is what happens today |
| **Who signs it** | 🤖 the test · ⚠️ **but the FIX is sub-block 7 and needs Brian**: the jazz/mashe owners must reach the DB first |

⚠️ **This test will FAIL when written, and that is correct.** It documents the open hole instead of
waiting for the fix. `val-functional.md` §2.2: *a check must be seen failing before its green means
anything* — here it starts red, on purpose, and its passing IS the definition of sub-block 7 closing.

### ③ TALK — message → agent → answer in MY thread

**Why:** the path the user sees, and where the `kind` bug lived — a cookie value used as the real
instance, **the same bug in 6 files**.

| Field | Value |
|---|---|
| **Datum** | the message reaches the instance the session declares — **never the one a parameter claims** |
| **Command** | the runner, over `lib/demo/for3sChat.ts` + `instancias.ts` |
| **What failure looks like** | a message answered by another owner's instance — silent, and the worst of the four |
| **Who signs it** | 🤖 the test |

### ④ POWER — only the OWNER switches the agent off

**Why:** a guest holding a key could switch off someone else's agent. Fixed in `container.ts`
(model C, `df6e93c`) — **with no test holding it.**

| Field | Value |
|---|---|
| **Datum** | the owner switches it off ✅ · **a guest with a valid key is refused** |
| **Command** | the runner, over `lib/demo/container.ts` |
| **What failure looks like** | a guest turns off an agent that is not theirs |
| **Who signs it** | 🤖 the test |

---

## 3 · THE ORDER, AND WHY THIS ONE

1. **② AUTHORIZE first**, even though it will fail. It is the only one guarding an **open** hole,
   and a red test is how sub-block 7 gets a definition of done instead of a description.
2. **① ENTER second** — it is the front door and it already broke twice; the two other paths
   assume a valid session, so this one holds them up.
3. **③ TALK third** — the highest blast radius (`session` 12 · `instancias` 6) and the failure the
   user would never notice on their own.
4. **④ POWER last** — one dependent, the fix is already in, and only the regression is missing.

⚠️ **Sub-block 2 writes ONE of these.** Which one is Brian's call: ② documents the open hole, ①
protects the door everything else needs.

---

## 4 · 🙋 THE DECISION THE PLAN CANNOT MAKE — the test runner

**Measured: there is none.** Choosing it is not derivable from the repo, so it is asked, not
guessed (ADR-003).

| Option | What it means |
|---|---|
| **Vitest** | the usual pick for Next.js today; fast, TS out of the box |
| **Jest** | more widespread, heavier setup on TS |
| **`node --test`** | zero dependencies; the poorest ergonomics |

⭐ **Recommendation: Vitest.** Reason: these four paths are logic over `lib/demo/*.ts` — no browser
needed — and Vitest runs TypeScript with no extra build. The trade-off: one more dev dependency in
a repo that today has none.

---

## 5 · ⛔ WHAT THIS PLAN DOES NOT DO

- **It does not fix the `DEV_FALLBACK`** — that is `blk-demo` sub-block 7, and it needs a datum only
  Brian has (who owns jazz and mashe).
- **It does not touch the hosting** — sub-block 9, blocked on Brian.
- **It does not write four tests.** One, as proof (§B).
- **It does not use mocks for what crosses a process.** `val-functional.md` §2.3: where it crosses
  a process or touches user data, **only the real system counts**.

---

Related: `blocks/archive/plan-tests-demo_2026-08/BLOCK.md` (the block that owns this) ·
`principles/expertise/doc-planning.md` §2.5 (the four fields every criterion carries) ·
`principles/expertise/val-functional.md` §2.2 (what counts as proof) ·
`blocks/active/demo/BLOCK.md` §F-8 (where the other three land).
