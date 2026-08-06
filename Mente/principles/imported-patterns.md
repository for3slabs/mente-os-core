# IMPORTED · failure patterns absorbed from external skills
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Language:** US English · **Source:** `convex-skill` (MIT) · **Block:** `blocks/archive/expertise-programacion_2026-08`
**Declared by:** the same §D that declares the discipline it belongs to

## Purpose

Failure patterns imported from an external skill and **rewritten as Mente OS v2's own logic** —
the vendor is never named, because measured, it appears **zero times** in For3s.

> ## 🔴 THIS IS NOT BRIAN'S CRITERION
>
> It is external material, usable today, **but not his judgement**. His criterion lives in
> `principles/expertise/*` §2-§4. Mixing the two would launder third-party opinion as the owner's
> judgement — the precise failure ADR-003 exists to prevent, and the reason these sections were
> kept apart from the start.

> ⭐ **Why they were gathered here (2026-08-05).** `dev-database.md` reached **381 lines against a
> ceiling of 350**, and Brian's own rule — `principles/expertise/doc-structure.md` §2.1, written
> that same day — says a document over its ceiling **must be split, with the halves pointing at
> each other**. The three `§4-BIS` sections were the natural cut: **same source, same status, and
> not the owner's criterion.** ⛔ **Not one word was removed** — only the section numbers changed,
> because a number is an address, not content.

---

## 1 · DATABASE — query and access defects

> 🔴 **NOT Brian's criterion.** External material (`convex-skill`, MIT), imported 2026-08-05 by his
> ruling: *"hay que estructurar esa lógica, pero debe ser propio de Mente OS v2."* **Rewritten as
> this system's own logic — the vendor is never named**, because measured, it appears zero times in
> For3s (stack: Python 3.12 + Postgres+AGE+pgvector; demo: Next.js + Neon). The failure transfers;
> the API does not. → `blocks/archive/expertise-programacion_2026-08` §G-2.
>
> 👉 **A database PR follows the same flow as any other: `rules/rule-shipping-flow.md`.** Declare it
> in the block's §D so the hook injects it. §3 of this file adds what a MIGRATION demands on top.

| # | Pattern | Why it is a defect |
|---|---|---|
| 1 | 🔴 **Authorization from a client-supplied id** | the request says who it is and the query believes it. Authorization reads the **verified session**, never an argument. Same shape as the hole closed in `verificacion.ts` and the owner-only rule in `container.ts` |
| 2 | **Filtering on a column with no index** | a full scan: fine at 10 rows, a timeout at 100,000 |
| 3 | **Reading a whole table with no bound** | *"give me everything"* works today and exhausts memory when the table grows |
| 4 | **Writing without awaiting the result** | 🔴 the write **fails silently** — no error, no row, and a clean-looking log |
| 5 | **Many sequential writes where one transaction belongs** | race conditions and inconsistent intermediate state |
| 6 | **Reading the clock inside a cached read** | the value freezes at first evaluation and serves stale data. Time-based transitions belong to a scheduled job that WRITES state, so the query can filter by that state |

**How to apply it:** #1 is always 🔴 — it is a security finding, not a performance one. #2 and #3
are 🔴 on any table expected to grow and 🟡 on a bounded one — and the block **states the measured
row count**, never assumes it. #4 to #6 are 🔴 on sight, because all three fail *silently*: nothing
reports that the write was lost or the data was stale.

⚠️ **Relation to §2.1:** pattern 1 is the code-level face of impossible state 1 (*an orphan
record*). Here the schema cannot help — a constraint cannot tell a legitimate id from a spoofed
one. **That is why it lives in criterion and not in a validator.**

---

## 2 · BACKEND — defects in any backend

> 🔴 **NOT Brian's criterion.** External material (`convex-skill`, MIT), imported 2026-08-05 by his
> ruling: *"hay que estructurar esa lógica, pero debe ser propio de Mente OS v2."* **Rewritten as
> this system's own logic — the vendor is never named**, because measured, it appears zero times in
> For3s. §2-§4 above stay Brian's and stay pending (ADR-003).
>
> ## 👉 THE SHIPPING FLOW IS NOT HERE — it is `rules/rule-shipping-flow.md`
>
> Branch → verify → PR → do not merge · the 8 git anti-patterns · the PR checklist · orchestration ·
> what makes a spec executable · the 6 setup layers. **It moved out on 2026-08-05** (Brian):
> *"va a haber PR de frontend, de base de datos"* — the hook injects only what a block declares in
> its §D, so a flow living here would never reach a frontend or database block. A block of ANY
> discipline declares that rule in its §D. What stays below is what is **specific to backend**.


### 4-BIS.7 · 🔴 FAILURE PATTERNS THAT APPLY TO ANY BACKEND

> Imported 2026-08-05 from a second external skill (`convex-skill`, MIT). **Rewritten as Mente OS
> v2's own logic** by Brian's ruling: *"hay que estructurar esa lógica, pero debe ser propio de
> Mente OS v2."* The vendor's API is not named, because measured, that vendor appears **zero times**
> in For3s — the stack is Python 3.12 + Postgres+AGE+pgvector, and the demo is Next.js + Neon.
> What is kept is the failure; what is dropped is the syntax.

| # | Pattern | Why it is a defect | Already seen here |
|---|---|---|---|
| 1 | 🔴 **Trusting an identity the CLIENT supplies** | anyone can impersonate anyone by passing the right id. Authorization reads the **verified session**, never an argument | the hole closed in `verificacion.ts`; and in `container.ts`, *only the OWNER may switch the agent off* |
| 2 | **Filtering without an index** | a full scan: it works with 10 rows and times out with 100,000 | — |
| 3 | **Fetching without a bound** | *"give me everything"* returns fine today and exhausts memory when the table grows | — |
| 4 | **Not awaiting an async call** | the write **fails silently**: no error, no data, and the log looks clean | — |
| 5 | **Sequential writes where one batch belongs** | race conditions and inconsistent intermediate state | — |
| 6 | **Circular imports through the schema module** | passes the type-checker and explodes at runtime with *"validator is undefined"* | 🤖 already measured: `bin/grade-block` counts `import cycles` |
| 7 | **Reading the clock inside a cached read** | the value freezes at the first evaluation and serves stale data. Time-based transitions belong to a scheduled job that writes state | — |
| 8 | **Refetching by hand after a write** | duplicates the source of truth and races the real update | — |

**How to apply it:** #1 is a security finding, always 🔴. #2 and #3 are 🔴 on any table expected to
grow, 🟡 on a bounded one — and the block states which it is **with the row count measured**, not
assumed. #4 to #8 are 🔴 when found, because all five fail *silently*: nothing in the logs says the
write was lost, the data was stale, or the state was inconsistent.

---

## 3 · FRONTEND — client-side data

> 🔴 **NOT Brian's criterion.** External material (`convex-skill`, MIT), imported 2026-08-05 by his
> ruling that the logic may be kept but must read as Mente OS v2's own — so **the vendor is never
> named**. → `blocks/archive/expertise-programacion_2026-08` §G-2.
>
> 👉 **A frontend PR follows the same flow as any other: `rules/rule-shipping-flow.md`.** Declare it
> in the block's §D so the hook injects it — it is transversal, not backend's property.

| # | Pattern | Why it is a defect |
|---|---|---|
| 1 | **Refetching by hand after a write** | when the data layer already pushes updates, a manual refetch duplicates the source of truth and races the real one. Trust the subscription; if there is none, say so explicitly |
| 2 | **Deriving state the server already owns** | the client recomputes what the backend decided, and the two drift. The server owns the truth; the client renders it |
| 3 | **A client-side guard as the only guard** | hiding a button is presentation, not authorization. Every hidden action still needs its check on the server (§ the backend's pattern 1) |

**How to apply it:** #3 is 🔴 always — it is a security finding. #1 and #2 are 🟡 unless a
divergence is measured, in which case they are 🔴 with the two conflicting values shown.

⚠️ **Scope note, measured:** the source skill is written for a reactive backend-as-a-service the
demo does not use. Only these three survived translation — the rest was vendor API. **Three
patterns imported honestly beat thirty copied blindly.**

---

Related: `principles/expertise/dev-database.md` · `principles/expertise/dev-backend.md` ·
`principles/expertise/dev-frontend.md` (**the three halves this was split from** — each one's
§2-§4 carries Brian's criterion, which these patterns never replace) ·
`principles/expertise/doc-structure.md` §2.1 (the rule that forced the split) ·
`rules/rule-shipping-flow.md` (the other half of what those skills contributed).
