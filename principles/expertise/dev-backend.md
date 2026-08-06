# EXPERTISE · BACKEND
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Ticket:** F1-bis-1 · ✅ **FILLED 2026-08-05 by Brian**
⚠️ **§2-§4 are Brian's criterion.** The imported material moved to
`principles/imported-patterns.md` on 2026-08-05 — it applies, but it is not his judgement.
👉 **The shipping flow (branch → PR) is transversal and lives in `rules/rule-shipping-flow.md`.**
**Language:** US English · **Read by:** owner-2 (development) before writing code, and owner-3
(validation) at block close.
**Injected by:** the block's §D `Required standards` + the hook (architecture §12-QUATER).
---

## 0 · WHAT THIS FILE IS

The **expert criterion** for this discipline, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (architecture §9.1). It asks, structures, and applies —
> it never fills this in on its own. That is exactly the error that produced the current state:
> *"todo está hecho como la IA quiso."*

**Status:** filled 2026-08-05. F1 closed with `dev-database.md`; this one and `dev-frontend`
complete owner-2.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian

| Quote | Date |
|---|---|
| *"no dejes cosas como hardcodeadas"* | 2026-07-24 |
| *"si va a pasar, tenemos que estandarizar"* | 2026-07-25 |
| *"cero hardcodeo: hosts/puertos/credenciales SIEMPRE de ENV"* | Método F §2.3 |

**Precedents to formalize:** the single guard in `session.ts` (12 copies → 0) ·
`instancias.ts` as a 100%-DB bridge with no env · brute-force protection in `verificacion.ts`.

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

The frame lives in `rules/qa-dimensions.md`. What each dimension **demands here** is Brian's
criterion — ✅ filled below.

### 2.1 · Architecture
**Question (frame):** does each piece have a single responsibility and sit in the right layer?
**Required evidence:** the dependency tree + which piece would break how many others.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## FOUR STRUCTURAL DEMANDS — all four
>
> | # | Demand | Why | Precedent |
> |---|---|---|---|
> | 1 | ⭐ **ONE guard per rule, never copied** | authorization, session validation, limits: a single implementation everyone calls. A copied guard drifts, and then one copy is weaker than the rest | `session.ts` — **12 copies → 0** |
> | 2 | **The endpoint does not decide, it orchestrates** | the HTTP route validates input and delegates; the logic lives in a layer testable without HTTP. Separates the cable from the brain | — |
> | 3 | **Configuration enters through ONE point** | nobody reads config on their own | `instancias.ts` — a 100%-DB bridge, zero env vars |
> | 4 | **Each piece can be switched off without breaking the rest** | a subsystem falling must not take the others with it | `container.ts` (model C) |
>
> **Why demand 1 is the strongest here:** a duplicated guard does not fail loudly — it fails
> *partially*. Eleven copies check correctly and the twelfth does not, so the system looks right
> until someone finds the one door that was never locked.
>
> **How to apply it:** count implementations per rule (must be 1), name the layer where the logic
> lives, name the single config entry point, and say what happens to the rest when this piece stops.

### 2.2 · Data design
**Question (frame):** does the schema represent the domain? Are impossible states impossible?
**Required evidence:** the real schema + one case the model cannot represent incorrectly.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — where the logic lives
>
> ## GUARANTEES in the database. DECISIONS in the code.
>
> | Belongs in the DB | Belongs in the code |
> |---|---|
> | what must **never** be able to happen — `FK`, `NOT NULL`, `UNIQUE` | what to **do** about it |
> | the **values**: thresholds, lists, config (`dev-database.md` §2.2) | the **rules** for using those values |
>
> **⛔ No business logic in the database** — no triggers, no stored procedures deciding. The schema
> stores and guarantees *shape*; it does not decide. That keeps the behaviour readable and
> versionable in one place instead of split across two systems that deploy differently.
>
> **Why this is not a contradiction with `dev-database.md` §2.1:** there, the four impossible states
> must be proven **by a constraint, not by an `if`** — that is the *guarantee* half, and it lives in
> the DB. The `if` that then decides what the user sees is the *decision* half, and it lives here.
> **Same law, two halves.**
>
> ⚠️ **Brian also selected *"it depends on the case, the block declares it"*, which does NOT dissolve
> the rule** — it would make the dimension unverifiable, and an unverifiable criterion is an
> intention (`docs/PENDING-BRIAN.md` §4). Read as intended: the split above is the default, and a
> block that departs from it **says so in its §G with the reason**. A departure that is written is
> engineering; one that is silent is drift.

### 2.3 · Abstraction
**Question (frame):** right level — neither copied three times nor generalized for one use?
**Required evidence:** where it repeats, or the real usages.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 IF IT TOUCHES SECURITY OR MONEY, IT IS UNIFIED — ALWAYS.
>
> Auth, permissions, charges: **duplication there is not debt, it is a hole.** It gets unified even
> at **two** copies, without waiting for a third and without arguing about whether they must change
> together.
>
> **Why this overrides the general rule:** `rules/qa-dimensions.md` §2.3 says there is no fixed
> number of repetitions — what decides is whether the copies must change together. That still holds
> everywhere else. **Here the exception is the stake:** a duplicated guard does not fail loudly, it
> fails *partially*. Eleven copies check correctly and the twelfth does not — and nothing tells you
> which one. `session.ts` reached **12 copies** before it was collapsed to one.
>
> **How to apply it:** count the implementations of every security- or money-touching rule. More
> than one → 🔴, regardless of how similar they look today.

### 2.4 · Naming
**Question (frame):** does the name say what it does without reading the body?
**Required evidence:** explain three names without opening the file.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> | # | Rule | ⛔ What it rejects |
> |---|---|---|
> | 1 | **An endpoint says what it does from its route** | if you must read the handler to know the action, the name failed |
> | 2 | 🔴 **No generic endpoint** — `/api/action`, `/api/do` | a route doing N things depending on a parameter hides **N endpoints with no contract**. It is `kind` raised to the API level: one name covering several meanings, and the reader cannot tell which |
> | 3 | **The error name says WHAT failed, not that something did** | ⛔ *"request failed"* → ✅ *"instance not found"*. Same criterion Brian set for checks in `val-functional.md` §2.4, applied to error responses |
>
> **How to apply it:** read three routes and say what each does without opening its file — then read
> three error responses and say what to fix from the message alone.

### 2.5 · Contracts
**Question (frame):** are interfaces declared? Are errors part of the contract?
**Required evidence:** the real signature + what happens when it fails.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## An expected failure is part of the CONTRACT. An unexpected one is logged before it is answered.
>
> | # | Rule | ⛔ What it forbids |
> |---|---|---|
> | 1 | **Every foreseeable failure is declared and answered** — not found, forbidden, invalid input, limit exceeded: each with its code and its shape | the endpoint that only knows how to succeed. This is what the **44 DB accesses with 0 try/catch** were missing |
> | 2 | **The error NEVER leaks internal detail to the client** | no stack, no path, no table name, no reason the auth failed. Detail goes to the log; the client gets only what it needs to act |
> | 3 | **An unexpected failure is RECORDED before responding** | a bug with no trace does not exist for whoever must fix it — the operational face of *"never close something whose failure you would not notice"* (`val-functional.md` §3) |
> | 4 | **A crash IS acceptable when the state is left corrupt** | better to fall than to continue on inconsistent data |
>
> ### ⭐ Rule 4 is the same law as the database's: **the DATA decides.**
>
> `val-integration.md` §2.5 settles stop-vs-degrade by asking whether user data is at risk. Here it
> reappears as *when is a crash correct*: **availability is recoverable, a corrupted record is not.**
> Same criterion, two seams — that is coherence, not repetition.
>
> **How to apply it:** list the endpoint's declared failures with their responses, show that the
> client message carries no internals, and name where the unexpected failure gets recorded.

### 2.6 · Necessity
**Question (frame):** does every file that exists have to exist?
**Required evidence:** who consumes it, and why it could not live elsewhere.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## An endpoint no real client calls is deleted, not documented.
>
> **Measured, never assumed:** if nothing in production invokes it, it is free attack surface and
> free maintenance. `accountStore.ts` had **0 consumers** after the migration and stayed in the tree
> — the same shape, one layer up.
>
> **The evidence is a measurement, not a memory:** who calls it, from where, and when it was last
> called. ⛔ *"it might be used by the mobile app"* is not evidence — either the call exists or the
> endpoint goes.
>
> ⚠️ **An unused endpoint is worse than unused code:** dead code sits still, but a live route
> **answers**. It is reachable, it can be probed, and nobody is watching it.

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — never, no exceptions
>
> | # | ⛔ Never | The case behind it |
> |---|---|---|
> | 1 | **Expose a control endpoint to the internet** | `container.ts`, model C (2026-07-26): the DB is the mailbox, `/ctl` is never exposed. *Exposing a control endpoint to flip a boolean is not worth it* |
> | 2 | 🔴 **Trust an id the client sends** | authorization reads the **verified session**. The hole closed in `verificacion.ts`; and why **only the OWNER** may switch the agent off — a guest holding a key could otherwise turn off someone else's |
> | 3 | **Deploy without being able to revert** | if you cannot go back, it is not a deployment, it is a bet. Same law as migration condition 1 (`dev-database.md` §3) |
> | 4 | **Hardcode a host, a port or a credential** | Método F §2.3 — verifiable by grep |
> | 5 | **Leave the same pattern solved N ways** | *"si va a pasar, tenemos que estandarizar"* |
>
> Rules 1 and 2 are **security findings**: 🔴 on sight, with no discussion of scope.

---

## 4 · WHAT MAKES BRIAN REJECT WORK IN THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## FOUR SIGNALS OF "THIS IS NOT A PRODUCT" — any ONE is enough
>
> | # | Signal | The anchor it comes from |
> |---|---|---|
> | 1 | **Hosts, ports or credentials written into the code** | Método F §2.3, literal: *"cero hardcodeo: hosts/puertos/credenciales SIEMPRE de ENV"* · *"no dejes cosas como hardcodeadas"*. **Verifiable by grep** |
> | 2 | **The same pattern solved N different ways** | *"si va a pasar, tenemos que estandarizar"* (2026-07-25). Three endpoints validating a session three ways is a half-built product |
> | 3 | **No way to know what happened when something fails** | every incident starts from zero. This is what For3s TRACE exists for |
> | 4 | 🔴 **A permission checked on the client and not on the server** | authorization lives in the backend or it does not live. *Identity is verified, never assumed* — the hole closed in `verificacion.ts`, and why only the OWNER may switch the agent off |
>
> ⚠️ **Signal 1 has an exception that is NOT a loophole:** `dev-database.md` §2.2 puts five
> categories in the DB, not in env vars either. **Env is for wiring** (connection strings, deploy
> identity); **the DB is for content**. Hardcoding is the worst of the three, but moving content
> into an env var is not the fix.
>
> **Signal 4 is the only one that is a security finding**, so it is 🔴 on sight, with no discussion
> of scope or table size.

---

## 4-BIS · IMPORTED PATTERNS → `principles/imported-patterns.md` §2 · BACKEND

The failure patterns imported from an external skill live there now, gathered with the other two
disciplines' — **same source, same status, and none of them Brian's criterion.**

> ⭐ **Moved 2026-08-05** because `dev-database.md` broke its 350-line ceiling and
> `principles/expertise/doc-structure.md` §2.1 says a document over its ceiling **must be split,
> with the halves pointing at each other**. ⛔ **Nothing was deleted** — only the numbering changed.

⚠️ **They still apply.** A block that declares this file in its §D is judged by §2-§4 here
(**Brian's criterion**) **and** by those patterns — and where both speak, the stricter one wins
(`rules/rule-inheritance.md`).

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> Never the reverse — a draft written first comes out as *"use best practices."*

**Suggested questions for the interview:**

1. What do you demand of an endpoint before it is done?
2. What makes you reject a backend change?
3. When does an error belong to the contract, and when is it a crash?
4. What must never be hardcoded, beyond credentials?
5. How do you decide whether logic belongs in the API or in the DB?
6. What has to be true before something goes to production?
7. Which backend error do you see most often?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context (layer D, §12-QUATER) |
| Block closes | owner-3 evaluates the 6 dimensions using it (`rules/qa-dimensions.md`) |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are FILLED**, so both the wiring and the criterion are live. Layer 1 of QA
> (`bin/grade-block`) does not depend on this file — that is why F4 can run first.

---

Related: `rules/qa-dimensions.md` (the frame) · `principles/owner-2-dev.md` (who reads it) ·
`principles/owner-3-validation.md` (who applies it) · `docs/Arquitectura_Mente_OS_v2_Bloques.md` §9.
