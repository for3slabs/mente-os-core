# EXPERTISE · DATABASE
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Ticket:** F1-2 · ✅ **FILLED 2026-08-05 by Brian — phase F1 closed.** First discipline with criterion.
**Language:** US English · **Read by:** owner-2 (development) before writing code, and owner-3
(validation) at block close.
**Injected by:** the block's §D `Required standards` + the hook (architecture §12-QUATER).
---

## 0 · WHAT THIS FILE IS

The **expert criterion** for this discipline, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (architecture §9.1). It asks, structures, and applies —
> it never fills this in on its own. That is exactly the error that produced the current state:
> *"todo está hecho como la IA quiso."*

**Why this discipline goes first:** it is where Brian has already expressed the most criterion,
and it is **what propagates the most** — touching the DB reaches everything that reads the table.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian — to expand, not to replace

| Quote | Date |
|---|---|
| *"vamos a desarrollar una base de datos, no un MVP pedorro, vamos por un producto"* | 2026-07-24 |
| *"la base de datos es la base de información, si no tenemos un control estamos mal"* | 2026-07-24 |
| *"esos valores no deberían estar puestos en el código... debería estar en la base de datos y poder solo modificar la base de datos"* | 2026-07-25 |
| *"tenemos que estandarizar cómo es que creamos los hilos para que no pase esta situación"* | 2026-07-25 |

**Precedents already built that this criterion should formalize:**
- `demo_instancias` as the single source of truth · 7 FKs · `demo_config` editable without a push
- the `hoteles` → `sin-tema` default (`rules/case-dangerous-default.md`)

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

The frame lives in `rules/qa-dimensions.md`. What each dimension **demands here** is Brian's
criterion — ✅ filled below.

### 2.1 · Architecture
**Question (frame):** does each piece have a single responsibility and sit in the right layer?
**Required evidence:** the dependency tree + which piece would break how many others.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 THE FOUR STATES A CORRECT MODEL CANNOT REPRESENT
>
> A schema is judged by what it makes **impossible**, not by what it allows. All four are
> mandatory — Brian selected every one of them, none is optional:
>
> | # | Impossible state | Enforced by | The case that proves it |
> |---|---|---|---|
> | 1 | **An orphan record** — a row without the owner it belongs to | `FK NOT NULL` | the most measured bug family in the demo |
> | 2 | **Two sources of truth for one datum** | one table owns it; nothing mirrors it | ⭐ `kind` — lived in a cookie AND in the DB, the code picked wrong → same bug in 6 files |
> | 3 | **A dead-end intermediate state** — rows stuck in `pending`/`processing` forever | every transient state needs a timeout or a forced transition | — |
> | 4 | **A default pointing at something with an owner** | the default is a neutral drawer, never a reserved name | `general` was the owner's private thread and was used as default → `rules/case-dangerous-default.md` |
>
> **How to apply it:** for each of the four, show the schema constraint that makes it impossible —
> **not the code that avoids it.** Code that "always checks" is not a guarantee; a constraint is.
> If the only thing preventing an orphan row is an `if` in the application, state 1 is 🔴.
>
> **Why architecture and not data design:** these four are about how the pieces of the model relate
> to each other. §2.2 governs *where a value lives*; this governs *which combinations may exist*.

### 2.2 · Data design
**Question (frame):** does the schema represent the domain? Are impossible states impossible?
**Required evidence:** the real schema + one case the model cannot represent incorrectly.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 WHAT NEVER LIVES IN CODE — five categories, not one
>
> `rules/qa-dimensions.md` §2.2 states the general rule (*a value with an owner never lives in
> code*). **For a database that rule is the floor, not the ceiling.** Five categories, all of them
> in the DB:
>
> | # | Category | Why | The case |
> |---|---|---|---|
> | 1 | **Anything with an owner** | it identifies a person, instance or tenant | `allowedEmails.ts` `DEV_FALLBACK` — still open |
> | 2 | **Anything that changes without deploying** | if changing it needs a push, it is in the wrong place | `demo_config` — editable, no push |
> | 3 | **Any fixed list** (catalogs, topics, roles) | ⚠️ *not mechanical* — see the exception below | S4a "cero listas fijas": 4 lists moved |
> | 4 | **Any threshold or numeric limit** (TTLs, retries, quotas, max sizes) | tuning must not require a deploy | — |
> | 5 | **⭐ Any sensitive user information** | Brian, 2026-08-05 | see §2.5 — this is about trust, not storage |
>
> > ## ⛔ *"Tenemos que evitar ocupar variables que vayan a Vercel y que se pongan en la base de datos."*
> >
> > *"La idea no es solo mantenerla nosotros: es que sea ESCALABLE y que no tengamos que
> > preocuparnos por esas pequeñeces."* — Brian, 2026-08-05
>
> **This makes environment variables a measurable smell, not a style choice.** An env var holding a
> value from any of the five categories is a finding: it does not scale (every instance needs it set
> by hand), it cannot be audited, and changing it is a deploy. The precedent is already recorded —
> 3 bridge env vars were retired from Vercel on 2026-07-26 and the demo stayed alive (HTTP 200).
>
> **How to apply it:** for every env var and every constant in the block, ask which of the five it
> falls into. If it falls into any → 🔴 until it lives in the DB. Env vars are for **wiring**
> (connection strings, deploy identity), never for **content**.
>
> ### ⚠️ How this sits with Método F §2.3 — *"cero hardcodeo (todo de ENV)"*
>
> **They do not contradict each other; this one is stricter.** Método F answers *"where does a
> value NOT go?"* → not into the code. This answers the next question it never asked:
> *"and where does it go instead?"* → **wiring to ENV, content to the DB.**
> Moving a fixed list from code into an env var satisfies Método F and still fails here: it does
> not scale (every instance set by hand), it cannot be audited, and changing it is a deploy.
> Per `rules/rule-inheritance.md`, **the stricter wins** — a discipline may tighten, never relax.
>
> ⚠️ **Category 3 is NOT mechanical** — measured in S4a: OAuth and foresito keep fixed lists
> *on purpose*, because moving them to the DB would let a DB write change an authorization path.
> A fixed list that PROTECTS something stays in code, and the block says why.

### 2.3 · Abstraction
**Question (frame):** right level — neither copied three times nor generalized for one use?
**Required evidence:** where it repeats, or the real usages.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — FOREIGN KEYS
>
> ## 🔴 A REAL RELATION ALWAYS CARRIES A FOREIGN KEY. NO EXCEPTIONS.
>
> If a column points at another table, it has an FK. Not "when it matters", not "unless it is a log
> table", not "when an orphan would break something" — **always**. Brian rejected all three softer
> variants on purpose.
>
> **Why the hard version and not the case-by-case one:** *"la base de datos es la base de
> información, si no tenemos un control estamos mal."* A per-case rule cannot be verified by a
> script, and an unverifiable criterion is an intention, not a criterion
> (`docs/PENDING-BRIAN.md` §4). This one is checkable: list the columns that reference another
> table and confirm each has a constraint.
>
> **The precedent:** `demo_instancias` — single source of truth, **7 FKs**, recorded in this file's
> §1 as a good precedent since 2026-07-24.
>
> **Consequence:** the cost of an FK on a high-volume append-only table (telemetry, audit) is
> accepted. If a specific table ever cannot carry one, that is a **§H friction entry with its
> measurement** — not a silent exemption.

### 2.4 · Naming
**Question (frame):** does the name say what it does without reading the body?
**Required evidence:** explain three names without opening the file.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## ⭐ THE ROOT COMES FIRST: **there must be an IMPLEMENTATION PLAN that justifies why the table exists.**
>
> > *"Debe existir un plan de implementación ANTES, que valide el por qué la tabla existe. Y de ese
> > punto partimos en determinar si está mal o no — porque el plan no lo va a respaldar."*
> > — Brian, 2026-08-05
>
> **This reverses the order of the whole dimension.** A table is not judged against a checklist of
> good practices; it is judged **against its plan**. The four signals below are how a badly designed
> table LOOKS — but the verdict comes from whether the plan backs it. A table the plan does not
> justify is wrong even if it passes all four.
>
> **The four signals, visible without running anything** (all selected by Brian):
>
> | # | Signal | Why it is visible | The case |
> |---|---|---|---|
> | 1 | **Columns that do not say what they distinguish** | you must read the code to know | ⭐ `kind` — the ambiguity produced the 6-file bug |
> | 2 | **Columns nullable that should not be** | all-nullable = the schema decides nothing and pushes validation into code | visible in the DDL |
> | 3 | **One table holding two different things** | columns that only apply to half the rows | §2.1 *"does more than one thing"*, applied to the schema |
> | 4 | **No created_at / updated_at** | nothing to audit with, nothing to debug when it breaks | verifiable by script |
>
> **How to apply it:** name the plan that justifies the table, then walk the four signals. The
> evidence for this dimension is **two things**: the plan reference AND the four checks — the plan
> alone is not enough, and the four checks without a plan judge a table nobody justified.

### 2.5 · Contracts
**Question (frame):** are interfaces declared? Are errors part of the contract?
**Required evidence:** the real signature + what happens when it fails.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — 🔴 this is about CREDIBILITY, not storage
>
> > ## ⛔ TODO CONECTADO. Y LO QUE NO ESTÉ CONECTADO LLEVA SU ALERTA: **qué no está conectado, POR QUÉ, y CÓMO va a conectarse.**
> >
> > *"No solo estamos manejando base de datos, es INFORMACIÓN. Y si la información de los usuarios
> > corre peligro porque no está bien hecha, PERDEMOS CREDIBILIDAD, PERDEMOS CONFIANZA."*
> > — Brian, 2026-08-05
>
> This is `rules/qa-dimensions.md` §2.5 (*no orphaned, dead or unconnected code*) with a database's
> stake attached: what dangles here is not a function, it is **user data**. That is why category 5
> of §2.2 — sensitive user information — belongs to this dimension too.
>
> **⭐ The reporting rule that comes with it — and it is a rule about ME, not about the schema:**
>
> > *"Es mejor decir: lo que está hecho, está probado, funcional, TODO lo construido — y aquí están
> > los siguientes pasos como continuación."*
>
> **The failure it exists to kill** (Brian's own words, 2026-08-05):
>
> > *"Hoy manejo base de datos, mañana frontend, y cuando regreso a base de datos me da información
> > que ni enterado, o me dice que YA FUNCIONA mientras yo sabía que no era así — hasta que le meto
> > una palabra en específico y entonces 'recuerda', pero vagamente. Eso lo queremos evitar."*
>
> **So an unconnected piece is not a bug to hide until asked. It is a declaration owed up front**,
> carrying three fields, never one:
>
> | Field | Not enough |
> |---|---|
> | **what** is not connected | ⛔ "there are some pending things" |
> | **why** it is not | ⛔ "it did not get done" |
> | **how** it will connect, when it happens | ⛔ silence — this is the field that gets skipped |
>
> **How to apply it at block close:** the report states what is built, tested and functional — and
> then, separately and explicitly, every seam left open with its three fields. A close that says
> only *"it works"* fails this dimension even if every test is green, because the next session
> starts blind and Brian has to extract it with the right keyword.
>
> ⚠️ **This is the DB-side twin of the S10 defect** — *"no entiendo qué leer ni cómo leerlo, ni sé
> qué sigue"*. Same root: state was reported without its continuation.

### 2.6 · Necessity
**Question (frame):** does every file that exists have to exist?
**Required evidence:** who consumes it, and why it could not live elsewhere.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## ⭐ ALL FOUR ERRORS HAVE ONE ROOT: **there was no implementation plan, or it did not justify it.**
>
> > *"Ojo aquí: hay tablas que SÍ necesitan esos dos datos. Pero todo parte del plan de
> > implementación — y el por qué salen todos estos errores."* — Brian, 2026-08-05
>
> **The four errors Brian sees most often** (all four selected):
>
> | # | Error | The case |
> |---|---|---|
> | 1 | **Columns/tables nobody uses, still there** | `accountStore` — 0 consumers after the migration, stayed in the tree. *"Ah, lo dejo aquí por si lo necesitamos"* |
> | 2 | **Data that belongs in the DB living in env vars** | §2.2 — does not scale, cannot be audited, changing it is a deploy |
> | 3 | **Migrations nobody knows whether they ran** | no record of what was applied where turns it into guesswork |
> | 4 | **The same datum copied into two tables** | ⚠️ **NOT automatically wrong** — see below |
>
> ### 🔴 Error 4 is the one that needs judgement, not a rule
>
> **Duplication is legitimate when the plan justifies it.** Some tables genuinely need the same two
> data points, and a validator that flags every repeat would be inventing criterion. What makes it
> an error is not the copy — it is a copy **the plan does not back**.
>
> **So the question for this dimension is never *"is this duplicated?"*. It is:**
>
> > **Does the implementation plan justify this table, this column, this copy existing?**
> > If the plan does not back it → 🔴, whatever it looks like.
> > If the plan backs it → 🟢, even if it duplicates.
>
> **How to apply it:** for each table and column, point at the plan that justifies it. Where there
> is no plan, that is the finding — before anything about the shape of the schema.
>
> ⚠️ **Consequence for layer 1:** `bin/grade-block` measures *dead code* mechanically. For a DB
> block that number is a **signal, not a verdict** — the verdict needs the plan, which no script
> can read.

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 BEFORE A MIGRATION TOUCHES PRODUCTION — four conditions, ALL of them
>
> `hooks/gate-critical.py` already **BLOCKS** a migration with no structurally declared rollback
> (a down marker or a reverse statement — never the word "rollback" in a comment; a comment saying
> `-- no rollback needed` used to disable the gate). Brian's criterion **extends that gate**:
>
> | # | Condition | Why it is not optional |
> |---|---|---|
> | 1 | **Rollback declared + backup VERIFIED** | the rollback only saves you if the backup actually exists. Verified, not assumed |
> | 2 | **Run first against REAL data** | `feedback_probar_flujo_completo_encadenado` — a migration that only ran on an empty DB is not tested |
> | 3 | **No consumer left broken — senders first** | `blk-demo` §G: senders send the field first, the receiver goes strict second. The reverse breaks everything not yet sending it |
> | 4 | **Runs twice without breaking** (idempotent) | if it fails halfway and is retried, it must not duplicate or corrupt. This is what separates a migration from a script |
>
> **How to apply it:** the block shows the four, each with its datum — the rollback statement, the
> backup that was verified, the consumer list that was checked, and the second run. Affirmative
> verification: *"ran twice, row count identical"*, never *"should be idempotent"*.
>
> ### Other hard rules of this discipline
>
> - **A real relation always carries a foreign key** (§2.3) — no exceptions.
> - **A default never points at something that has an owner** (`rules/case-dangerous-default.md`).
> - **A value in any of the five categories of §2.2 never lives in code or in an env var.**
> - **Nothing dangles silently** (§2.5) — an unconnected piece is declared with what · why · how.

---

## 4 · WHAT MAKES BRIAN REJECT WORK IN THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — partially answered, see the hole below
>
> **The one already stated, and it is the strongest:** work is rejected when **something is not
> connected and its state is not declared** (§2.5). Not because the seam exists — seams are normal
> — but because reporting *"it works"* over an open seam is what costs credibility and trust.
>
> > *"Es mejor decir: lo que está hecho, está probado, funcional — y aquí están los siguientes
> > pasos."* The rejection is not of the gap. **It is of the silence about the gap.**
>
> **The second, and it is the root of §2.4 and §2.6:** work is rejected when **there is no
> implementation plan that justifies what was built**, or the plan does not back it.
>
> > *"Debe existir un plan de implementación antes, que valide el por qué la tabla existe. De ese
> > punto partimos en determinar si está mal o no."*
>
> That reverses the usual review order: the schema is not measured against best practices, it is
> measured **against its plan**. A table the plan does not justify is rejected even when it passes
> every mechanical check — and a duplicate the plan DOES justify is accepted.
>
> **Summary — the two rejection signals for this discipline:**
>
> | # | Rejected when | Where it is applied |
> |---|---|---|
> | 1 | something is not connected **and its state is not declared** (what · why · how) | §2.5 |
> | 2 | there is **no implementation plan** backing what exists | §2.4 · §2.6 |

---

## 4-BIS · IMPORTED PATTERNS → `principles/imported-patterns.md` §1 · DATABASE

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

1. What do you demand of a schema before approving it?
2. What makes you reject a DB change outright?
3. Which values must **never** live in code, and why?
4. How do you know a table is badly designed, without running anything?
5. What must be **impossible to represent** in a correct model?
6. When is a FK mandatory, and when is it overkill?
7. What has to be true before a migration touches production?
8. Which DB error do you see most often and bothers you most?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context (layer D, §12-QUATER) |
| Block closes | owner-3 evaluates the 6 dimensions using it (`rules/qa-dimensions.md`) |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are filled since 2026-08-05**, so both the wiring and the criterion are live. Layer 1 of QA
> (`bin/grade-block`) does not depend on this file — that is why F4 can run first.

---

Related: `rules/qa-dimensions.md` (the frame) · `principles/owner-2-dev.md` (who reads it) ·
`principles/owner-3-validation.md` (who applies it) · `docs/Arquitectura_Mente_OS_v2_Bloques.md` §9.
