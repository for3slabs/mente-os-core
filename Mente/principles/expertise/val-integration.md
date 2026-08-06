# EXPERTISE · VAL-INTEGRATION — the bugs live BETWEEN the pieces
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
✅ **FILLED 2026-08-05 by Brian** — owner-3 now has half its own body of criterion.
**Ticket:** F1-quater-2 · **Branch of:** `principles/owner-3-validation.md` (functional-flow validation)
**Language:** US English · **Read by:** owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for the seams** — what happens where two pieces meet, which is where the
expensive bugs live.

> ⛔ **The AI does not invent criterion** (ADR-003).

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration ⬅ THIS FILE
```

**Why it is separate from `val-functional`:** that one asks *"does this piece work?"* This one asks
*"does the chain still work when every piece works?"* Every piece can pass its own test and the
flow still be broken — that is the failure this discipline exists for.

---

## 1 · CONTEXT ALREADY CAPTURED

### The rule that created this discipline

> **Brian, 2026-07-20:** *"los bugs trágicos viven ENTRE las piezas — auditoría punta a punta con
> datos reales."*
> (memory `feedback_probar_flujo_completo_encadenado`)

### Measured cases — every one of these lived at a seam

| Case | What broke between pieces |
|---|---|
| `kind` (a cookie value) used as the real instance | **the same bug in 6 files** |
| "resolve the instance" copied in 6 places | the fix needed a *"barrido completo del patrón"* |
| `DEMO_ENC_KEY` diverging local vs Vercel since June | the fallback hid it — **production down** |
| `tailscale serve` silently turning off the Funnel | verified from my environment, not Vercel's — **production down again** |
| The 21-jul incident | recovered from a raw `.jsonl` six days later |
| `check-clear-ready` pointing at a path a migration had deleted | guarded by `os.path.exists`, it failed **silently** — the check protecting the cold-start brief had never run |

> ⭐ **The pattern in all six:** each piece was fine on its own. What failed was the assumption one
> piece made about another.

### The reconnection test — already LOCKED

`owner-3-validation.md` §4-D: *restart a sibling, run the flow again, confirm it reconnects from
ENV and not from a hardcoded host.*

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

### 2.1 · Architecture — the map of the seams
**Question (frame):** does each piece have one responsibility, at the right level?
**Here:** are all the consumers of a piece known before it is changed?

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 FOUR CONDITIONS BEFORE TOUCHING A PIECE OTHERS CONSUME — all four
>
> | # | Condition | Why | Precedent |
> |---|---|---|---|
> | 1 | **Every consumer known, MEASURED** — not remembered | a list from memory is a guess | `instancias.ts`: 26 mentions, **9 real imports**. A dependent is a file that IMPORTS the piece, never one that mentions it (`blk-demo` §G) |
> | 2 | **Deployment order: senders first, receiver strict second** | the reverse breaks everything not yet sending the field | `blk-demo` §G, 2026-07-26 — the fix landed with no agent rebuild needed |
> | 3 | **Exercise the WHOLE flow, not the piece** | a unit test on the piece does not answer this dimension | *"los bugs trágicos viven ENTRE las piezas"* (2026-07-20) |
> | 4 | **Revertible without touching the consumers** | if undoing it needs a coordinated change in every dependent, it is not one change — it is N | `userStore.ts`: 12 dependents, **21 edits** |
>
> **How to apply it:** show the measured consumer list (the command and its output), the order the
> two sides went out in, the end-to-end run, and how the change would be undone. Four data points —
> ⛔ *"I checked the consumers"* is not one of them.
>
> ⚠️ **Condition 4 is the one usually skipped**, and it is the one that turns a bad change into an
> expensive one: a piece you cannot revert alone is a piece whose blast radius you accepted blind.

### 2.2 · Data design — what crosses the seam
**Question (frame):** are impossible states impossible?
**Here:** what a piece is entitled to assume about the data another one hands it.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 NOTHING. A PIECE ASSUMES NOTHING AND VALIDATES EVERYTHING IT RECEIVES.
>
> Not even from a piece of our own. Trust does not travel across a seam: the receiver checks shape
> **and** content, every time.
>
> **The case this comes from:** `kind` — a cookie value used as if it were the real instance.
> Six files assumed the previous piece had handed them something meaningful. **Same bug, six
> times.** No validation anywhere, because everything came "from inside".
>
> ## ⭐ AND IDENTITY IS NEVER ASSUMED — IT IS VERIFIED
>
> An id arriving in a request proves nothing about who is asking. **Authorization reads the
> verified session, never an argument.** This is the same hole closed in `verificacion.ts`, and
> the reason `container.ts` lets **only the OWNER** switch the agent off — a guest holding a key
> could otherwise turn off someone else's agent.
>
> ⚠️ **The distinction that keeps this from becoming paranoia:** validating is not re-deriving.
> What the SCHEMA already guarantees by constraint (an FK, a `NOT NULL`) does not get re-checked in
> code — the guarantee lives in the database (`dev-database.md` §2.1). What crosses a seam **without
> a constraint behind it** gets validated, always.
>
> **How to apply it:** for each seam, name what the receiver validates and what it delegates to a
> constraint. ⛔ *"it comes from our own code"* is not an answer — that is precisely what the six
> `kind` files believed.

### 2.3 · Abstraction — the shared pattern
**Question (frame):** copied three times, or over-generalized?
**Here:** when the same logic in two places is duplication and when it is coincidence.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 THE TEST IS THE OWNER OF THE RULE — not how alike the code looks.
>
> **If both places implement a business rule belonging to the SAME owner → it is duplication, and
> it gets unified.** If each side answers to a **different** owner, the resemblance is legitimate
> coincidence and they stay apart, however similar the code reads.
>
> **Why the owner and not the shape:** two pieces can look identical today and diverge tomorrow
> because nothing said they had to move together. Unifying by resemblance couples two rules that
> were never the same rule — and then one owner's change silently alters the other's behaviour.
> Conversely, leaving a single owner's rule in two places is how *"resolve the instance"* ended up
> copied in **6 files** and the fix needed a *"barrido completo del patrón"* four commits later.
>
> **How to apply it:** for each repeated logic, name **whose rule it is**. Same owner → unify, and
> `rules/rule-fix-not-patch.md` applies (evaluate every copy before writing, never patch one).
> Different owners → leave it, and say so in §G so the next reader does not "fix" it.
>
> ⚠️ **This is the same axis as §2.2, §2.4 and §2.6** — ownership decides at every seam. Not who
> wrote the code: **who owns the rule the code enforces.**

### 2.4 · Naming — across the boundary
**Question (frame):** does the name say what it does?
**Here:** the same concept must not have two names on two sides of a seam.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 ONE CONCEPT, ONE NAME ACROSS THE WHOLE FLOW
>
> | # | Rule | Why |
> |---|---|---|
> | 1 | **One concept keeps one name end to end** | if `instancia` on one side is `kind` on the other, someone will conflate them — and that is **exactly** the 6-file bug |
> | 2 | **The OWNER of the datum sets the name** | the piece that rules that datum names it; consumers adopt it. Settles which of the two names wins without debate |
> | 3 | **If two names are unavoidable, DECLARE the mapping** | an external API or a legacy schema cannot be renamed. Then the contract states the translation **in one single place**, never in each consumer |
> | 4 | ⛔ **No generic name at a boundary** | `data`, `info`, `value`, `kind` — at a seam they force the reader to open the other side to learn what arrives |
>
> **Rule 4 is what `kind` actually violated.** It was not rejected for being short
> (`dev-database.md` §2.4: short is fine when the structure justifies it) — it was rejected because
> **at a boundary it says nothing about what it distinguishes.**
>
> **How to apply it:** trace one datum across the seam and name it at both ends. Two names with no
> declared mapping → 🔴. A generic name at the boundary → 🔴, whatever it is called inside.

### 2.5 · Contracts — ⭐ the core of this discipline
**Question (frame):** are interfaces declared? Are errors part of the contract?
**Here:** what each side promises, and what happens when the other side fails. Measured precedent:
**44 DB accesses with 0 try/catch.**

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — 🔴 the core of this discipline
>
> ## ⛔ FAIL LOUDLY. NEVER SILENTLY.
>
> **The measured case:** `DEMO_ENC_KEY` had diverged local vs Vercel **since June**, and a fallback
> hid it until production went down. The fallback did not prevent the failure — it **postponed and
> disguised** it. A silent fallback is not resilience; it is a bug with a delay fuse.
>
> **Four requirements, all of them:**
>
> | # | Requirement |
> |---|---|
> | 1 | **Fail loudly, never silently** — no `catch` that swallows, no fallback that hides a divergence |
> | 2 | **Declare the failure mode in the contract** — without it every consumer invents its own reaction. The 44 accesses with 0 try/catch were exactly this hole |
> | 3 | **Degrade with an EXPLICIT notice** — keep working in reduced mode, but say so. Never pretend everything is fine |
> | 4 | **Stop the whole flow** — when the condition below applies |
>
> ### ⭐ WHAT DECIDES BETWEEN 3 AND 4: **is DATA involved?**
>
> > **If the failure can corrupt or lose user data → STOP.**
> > **If it only degrades a function (a read, an ornament) → continue, with the notice.**
>
> **The reason is the one already written in `dev-database.md` §2.5** (Brian, 2026-08-05):
> *"si la información de los usuarios corre peligro porque no está bien hecha, PERDEMOS
> CREDIBILIDAD, PERDEMOS CONFIANZA."* Availability is recoverable; a corrupted record is not.
> The two options never contradict each other, because **the data decides**, not the mood.
>
> **How to apply it:** for each seam, state its declared failure mode and which side of the line it
> falls on — data or function — **with the reason**. A seam whose §G does not say which it is has
> not answered this dimension.

### 2.6 · Necessity — does this connection have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** which dependency could be removed entirely instead of tested.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A seam is DELETED, not tested, when any of these four holds
>
> | # | The connection… | Why it goes |
> |---|---|---|
> | 1 | exists **only "just in case"** | *"ah, lo dejo aquí por si lo necesitamos"* (`rules/qa-dimensions.md` §2.6). A seam with no real consumer is free failure surface |
> | 2 | is **not backed by the implementation plan** | the root Brian set for `dev-database.md` §2.6: if the plan does not justify it, it is wrong — **even if it works** |
> | 3 | **duplicates a path that already exists** | two routes for the same datum diverge sooner or later. Impossible state #2, seen at the seam |
> | 4 | **crosses an owner/instance boundary without needing to** | every crossing is a dependency to keep alive. Convenience is not a reason to couple two owners |
>
> **The order matters:** ask this dimension **before** writing a test. Testing a connection that
> should not exist is paying maintenance forever for something whose correct fix is deletion.
>
> **How to apply it:** for each seam, name its real consumer and the plan that justifies it. No
> consumer, or no plan → 🔴, and the finding is *delete*, not *cover with a test*.

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — never, no exceptions
>
> | # | ⛔ Never | The case that cost it |
> |---|---|---|
> | 1 | **A fallback that HIDES a divergence** | `DEMO_ENC_KEY` differed local vs Vercel **since June**; the fallback hid it until production went down. A fallback that disguises is a bug with a delay fuse |
> | 2 | **Change the receiver before the senders** | a strict receiver first breaks everything not yet sending the field (`blk-demo` §G, 2026-07-26) |
> | 3 | **Call a seam good without REAL data** | no mocks, no local-only: the full chained flow with real data (2026-07-20) |
> | 4 | **Delete a piece without measuring who imports it** | importers, never mentions — `instancias.ts` had 26 mentions and 9 real imports |
> | 5 | **A default that points at something with an owner** | `general` was the owner's private thread and was used as a default → `rules/case-dangerous-default.md` |
> | 6 | **Treat testing from my environment as testing production** | measured **twice**, both times an outage: `tailscale serve` killed the Funnel; `DEMO_ENC_KEY` diverged |
>
> Rules 5 and 6 were already in force before this file was filled; 1-4 were added on 2026-08-05.
> All six are verifiable — each names a thing you can look for, not an intention.

---

## 4 · WHAT MAKES BRIAN REJECT AN INTEGRATION

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 FOUR SIGNALS THAT IT WAS TESTED IN ISOLATION ONLY — any ONE of them is enough
>
> | # | Signal | Why it is disqualifying |
> |---|---|---|
> | 1 | ⭐ **It was verified from MY environment, not the real one** | **measured twice, both times production went down**: `tailscale serve` silently killed the Funnel, and `DEMO_ENC_KEY` had diverged local vs Vercel since June. Testing from where you build is not testing where it runs |
> | 2 | **Only mocks, no real data** | a mock returns what you expect; real data returns what is there. *"Auditoría punta a punta con datos reales"* (2026-07-20) |
> | 3 | **Nobody restarted anything** | the reconnection test (`principles/owner-3-validation.md` §4-D): restart a neighbouring piece, run the flow again, confirm it reconnects **from ENV** and not from a hardcoded host |
> | 4 | **The evidence says *"seems to work"*** | affirmative verification or nothing: *"recovered X"*, *"vector = 1024 dims"*, *"cron_corridas with today's timestamp"*. ⛔ never *"parece bien"*, *"debería funcionar"*, *"más o menos"* |
>
> **These are not a checklist to score.** Any single one present means the integration was not
> verified — the verdict is 🔴 regardless of how green the unit tests are.
>
> ⚠️ **Signal 1 is the most expensive and the least obvious**, because everything looks correct
> while you are looking at it. It is the only one that has already cost this project two outages.

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**

**Suggested questions for the interview:**

1. What do you demand before believing two pieces really talk to each other?
2. How do you know a change will not break something downstream?
3. What must be tested with real data and never with a mock?
4. Which integration failure has cost you the most, and what would have caught it?
5. When a piece fails, what should the piece next to it do?
6. What has to be verified in the real environment, not a local one?
7. Which assumption between pieces do you see broken most often?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 applies it alongside `val-functional.md` |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are FILLED — wiring and criterion are both live.**

---

Related: `principles/owner-3-validation.md` (the owner this branches from) ·
`principles/expertise/val-functional.md` (its sibling) · `rules/case-dangerous-default.md` ·
`memory feedback_probar_flujo_completo_encadenado` · `docs/PENDING-BRIAN.md`.
