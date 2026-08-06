# QA DIMENSIONS · the senior review
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Language:** US English · **Used by:** owner-3 (validation) at block close
**Layer 1 (measurable) lives in:** `bin/grade-block` — this file is **layer 2**.
---

## 0 · WHY THIS FILE EXISTS

> **Brian, 2026-07-27:** *"que la arquitectura es correcta, si el diseño de datos es bueno, si la
> abstracción es la adecuada, si el nombre es claro. **Porque así v2 se diferencia**: no cumplimos
> con solo lo que nos dijo la IA, cumplimos porque sabemos qué requerimientos necesitas. Tenemos QA
> como uno de los elementos internos de Mente OS y eso vale oro. Que no sea 'me lo dio la IA y no
> sé', sino que **se sienta hecho por un senior de 50 años de experiencia**."*

**Any linter has layer 1.** What no linter has is **a senior's criterion** — and that criterion is
Brian's, not the AI's.

### The rule that governs this whole file

> ## 🚫 The AI does not declare "this is fine." The AI reports the measurement.

A dimension is **not answered by asserting it**. It is answered by **showing the required evidence.**
An answer without evidence does not count.

---

## 1 · HOW A DIMENSION WORKS

Each of the six has **three parts**:

| Part | Purpose |
|---|---|
| **Question** | what is being judged, in one concrete sentence |
| **Required evidence** | 🔴 **what must be SHOWN** to answer — asserting is not answering |
| **Typical failure** | what it looks like when it is wrong (comes from real cases) |

**Verdict per dimension:** 🟢 pass · 🟡 concern (documented, does not block) · 🔴 fail.

**A loose criterion is useless.** *"The architecture must be correct"* is as empty as *"it is fine"*.
That is why every dimension demands evidence.

---

## 2 · THE SIX DIMENSIONS

### 2.1 · ARCHITECTURE

**Question:** does each piece have a single responsibility and sit in the right layer?

**Required evidence:** the dependency tree + name which piece would break how many others.

**Typical failure (measured):** `lib/demo/userStore.ts` concentrated 5 responsibilities and had
5 dependents → 21 edits and 42% of commits were fixes.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> **How a dependent is counted:** the **total** of what points at the piece — **weighted by how
> relevant that file is**, and read in order of importance. Not a flat count: ten dependents on
> throwaway files are not ten dependents on the pieces that carry the flow.
>
> **What makes a piece badly cut — BOTH at once, not either:**
> 1. **the number** of dependents (weighted, as above), **and**
> 2. **it does more than one thing.**
>
> One without the other is not a fail. A piece with many dependents that does exactly one thing is
> correctly cut and deserves them. A piece that does three things and nobody imports is a 🟡, not
> a 🔴 — it will become one the moment it gets dependents.
>
> **⛔ SCOPE — this dimension judges existing code, never a proposal.** Brian, asked what makes him
> reject a structure before it has dependents: *the graph is not there yet, so there is nothing to
> measure.* The three measured failures of this file (`userStore.ts`, `kind`, `accountStore.ts`)
> were **all** caught after the fact, with the graph in hand. Judging a design with no graph would
> be criterion invented on the spot — the thing this file exists to prevent.
>
> **Consequence:** a block whose code is not written yet **cannot fail 2.1**. It is not a 🟢 either —
> it is **`not measurable yet`**, the same way `grade-block` marks a metric that does not apply
> (ADR-028: *not measured is NOT a pass*).
>
> <!-- The "not measurable yet" marker is written in words, never with the white-square glyph:
>      generate-metrics counts that glyph as a criterion hole, so using it as an example here
>      would inflate criterion.holes by one. Measured 2026-08-05 (it did: 61 instead of 60). -->



---

### 2.2 · DATA DESIGN

**Question:** does the schema represent the domain? Is it normalized? Are impossible states
impossible?

**Required evidence:** the real schema + one case the model **cannot** represent incorrectly.

**Typical failure (measured):** `kind` (a cookie value) was used as if it were the real instance →
the same bug appeared in 6 files.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 A VALUE THAT HAS AN OWNER NEVER LIVES IN CODE.
>
> If the datum identifies **a person or an instance**, it belongs in the database. No exceptions for
> convenience, none for "it is only for dev".
>
> **The case that fixed it — still open today.** `lib/demo/allowedEmails.ts` carries a
> `DEV_FALLBACK` that authorizes a **fake email address**: an identity, with an owner, written into
> code. It is sub-block 7 of `blk-demo` and it is the reason that block cannot be handed to a
> client. The same shape was already resolved once — jazz's and mashe's owners were moved to the DB
> in S4a — which is what makes this a criterion and not an incident.
>
> **Why the owner is the test, and not "does it change often":** `demo_config` is editable without a
> push, and that is good, but frequency is a symptom. Ownership is the cause. A value with an owner
> that never changes is still wrong in code, because the code is not where its owner can be checked.
>
> **How to apply it:** for each constant in the block, ask *who does this belong to?* If the answer
> names a person, an instance, or a tenant → 🔴 until it lives in the DB.
>
> **Anchors this expands:** *"vamos a desarrollar una base de datos, no un MVP pedorro"* ·
> *"si no tenemos control estamos mal"* · `rules/case-dangerous-default.md`
> (*"a default never points at something that has an owner"* — same root, seen from the default side).
>
> ⚠️ **What this criterion does NOT cover:** the single-source-of-truth failure (`kind`, a cookie
> value used as if it were the real instance, same bug in 6 files). That is a different criterion in
> this same dimension, **not yet written** — Brian chose the ownership rule first, deliberately.

---

### 2.3 · ABSTRACTION

**Question:** is it at the right level — neither copied three times nor generalized for a single use?

**Required evidence:** the places where it repeats, **or** the real usages of the abstraction.

**Typical failure (measured):** "resolve the instance" copied in 6 places; the fix required a
*"barrido completo del patrón"* four commits later.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> **BOTH sides get evaluated, not one.** Copied too many times *and* generalized too early are the
> same failure seen from opposite ends. A review that only hunts duplication passes an abstraction
> built for a single caller — and that one is harder to remove later, because it looks deliberate.
>
> **There is no fixed number of repetitions that forces an abstraction — it depends on the case.**
> Three copies of two trivial lines may be fine; two copies of the instance-resolution logic were
> not. What decides is not the count, it is whether the copies **have to change together**.
>
> **How to apply it — one question per side:**
> - *copied:* if this rule changes, how many places must change with it? If they must all change and
>   they are separate, that is the failure of the 6 copies.
> - *generalized:* how many real callers does this abstraction have **today**? One caller is a 🟡
>   with its rationale, zero is 🔴 — and zero is also a 2.6 finding.
>
> **Consequence when it fails:** `rules/rule-fix-not-patch.md` applies — all the copies get evaluated
> **before** anything is written, never one patched and the rest left.

---

### 2.4 · NAMING

**Question:** does the name say what it does, without reading the body?

**Required evidence:** explain three names from the block **without opening the file**.

**Typical failure (measured):** `kind` does not say what it distinguishes — reading the body was
required, and that ambiguity produced the 6-file bug of §2.2.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> **Short names are allowed when they are necessary. There is no length ceiling and no length floor
> — what governs is the structure and the decision already taken** in that block.
>
> So the test is **not** *"is this name long enough?"*. It is **coherence**: does the name match the
> structure it lives in and the decision this block recorded in §G? A short name inside a structure
> where that short form is the established convention is correct. The same short name dropped into a
> structure that spells things out is a 🟡, because now the reader has to hold two conventions.
>
> **Why `kind` still fails this test:** it was not rejected for being four letters. It was rejected
> because **it does not say what it distinguishes** — no structure and no recorded decision made
> `kind` mean "instance", so the body had to be read. That ambiguity is what produced the 6-file bug
> of §2.2. Length was never the defect; the missing decision was.
>
> **How to apply it:** when a name is short, name the structure or the §G decision that makes it
> readable. If neither exists, the name is not short — it is undecided.

---

### 2.5 · CONTRACTS

**Question:** are the interfaces between pieces declared? Are errors part of the contract?

**Required evidence:** the real signature + what happens when it fails.

**Typical failure (measured):** 4 functions in `userStore.ts` with no declared failure mode — and
44 DB accesses with **0 try/catch** (fixed in U1).

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — 🔴 the hardest rule in this file
>
> **It is an error whenever it is not connected and has not been identified** — between the piece
> and whatever it sets off downstream. Both halves count: unconnected **or** unidentified.
>
> > ## ⛔ NO PUEDE DEJAR CÓDIGO HUÉRFANO, MUERTO, SIN CONECTAR
> >
> > *"Y ESO LO LOGRAMOS ANALIZANDO TODO Y PROBANDO EL FLUJO A PROFUNDIDAD CON DATOS REALES."*
> > — Brian, 2026-08-05
>
> **This is stated without exceptions on purpose.** It does not soften for pieces that look
> peripheral, and there is no "critical path only" carve-out: the failure is orphaned code, and
> orphaned code is never on the path you were watching.
>
> **The evidence this demands is the strictest in the file**, and it is not a signature review:
> - **analyze everything** — the piece *and* what it triggers downstream, not the function alone
> - **exercise the flow in depth with REAL data** — a unit test on the piece does not answer this
>   dimension, because *"los bugs trágicos viven ENTRE las piezas"*
>   (`feedback_probar_flujo_completo_encadenado`, Brian 2026-07-20)
>
> **How it connects to the rest of the system:**
> - the §5-BIS battery (`owner-3-validation.md` §4) is how this gets exercised — checks B-G
> - **affirmative verification** is mandatory: *"recovered X"*, never *"seems connected"*
> - deployment order, already recorded in `blk-demo` §G: **senders send the field first, the
>   receiver goes strict second.** The reverse breaks everything not yet sending it.
>
> **The overlap with 2.6 is deliberate, not redundant.** 2.6 asks *does this file have to exist?*
> 2.5 asks *is what exists wired and accounted for?* A file can be necessary and still dangle.

---

### 2.6 · 🔴 NECESSITY

**Question:** does **every file that exists HAVE to exist?**

**Required evidence:** for each new file — who consumes it, and why it could not live somewhere else.

**Typical failure (measured):** `accountStore.ts` had **0 consumers** after the migration and stayed
in the tree.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — already stated, kept verbatim
>
> > *"Que lo que está es necesario, y no se lo inventó, o lo quiso mover, o dijo 'ah, lo dejo aquí
> > por si lo necesitamos'."* — Brian
>
> **Confirmed as-is on 2026-08-05.** Asked whether the three sins it names — *inventing it* ·
> *wanting to move it* · *leaving it just in case* — carry different weight, Brian's answer was to
> **leave it exactly as written**. So they are not ranked: all three are the same failure, which is
> a file in the tree that no one can justify.
>
> **How to apply it:** for every file in the block, name **who consumes it** and **why it could not
> live somewhere else**. No consumer → 🔴. A consumer that is only a build artifact or a mention in
> a comment does not count (`blk-demo` §G, 2026-07-29: *a dependent is a file that IMPORTS the
> piece, not one that mentions it*).
>
> **Layer 1 already measures the blunt half of this** (`grade-block`: *files nobody imports*), which
> is why the criterion here is the other half: **a file with importers can still fail 2.6** if the
> reason it exists is one of the three sins.

---

## 3 · OUTPUT FORMAT

```
BLOCK demo — criterion review · 2026-07-27
  1 architecture ... 🟡  userStore concentrates 5 responsibilities
                         evidence: tree attached · 5 modules depend on it
  2 data .......... 🟢  normalized schema, 7 FKs, no impossible states
                         evidence: schema.sql + "guest without owner" is unrepresentable
  3 abstraction ... 🔴  "resolve instance" copied in 6 places
                         evidence: paths of the 6 copies
  4 naming ........ 🟡  `kind` does not say what it distinguishes
                         evidence: 3 names explained; `kind` required reading the body
  5 contracts ..... 🔴  4 functions with no declared failure mode
                         evidence: signatures without an error type
  6 necessity ..... 🔴  accountStore.ts: 0 consumers after the migration
                         evidence: grep returned nothing
  ─────────────────────────────────────────────────────────────
  CRITERION VERDICT: 🔴 fail — 3 dimensions red
```

**Combined with layer 1** (`bin/grade-block`): 🟢 product · 🟡 close · 🔴 MVP.
A 🔴 does not forbid closing the block — it forbids **closing it as a product**. It closes marked
**MVP with its debt listed.**

---

## 4 · PER-DISCIPLINE CRITERION

The six dimensions are **the frame**. What each one demands **changes by discipline**:

| Discipline | File | Status |
|---|---|---|
| Database | `principles/expertise/dev-database.md` | ✅ **FILLED 2026-08-05** — F1 closed |
| Backend | `principles/expertise/dev-backend.md` | ✅ **FILLED 2026-08-05** |
| Frontend | `principles/expertise/dev-frontend.md` | ✅ **FILLED 2026-08-05** |

> ✅ **Layer 2 is no longer an empty form** (2026-08-05): the six dimensions of §2 all carry Brian's
> criterion, so a criterion review can now be run on any block. What is still pending is the
> **per-discipline** refinement in the table above — the frame is filled, the specializations are not.
>
> ⚠️ **A dimension answered from §2 alone is valid.** When the block's discipline file is filled it
> **adds** demands, never relaxes them (`rule-inheritance.md`: rules add up, the stricter one wins).

---

## 5 · METHOD FOR FILLING THIS

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> **Never** *"the AI drafts and Brian corrects"* — that produces *"use best practices"*.

Recorded as risk #1 of phase F1 in the implementation plan.

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` §12-QUINQUIES (the design) ·
`principles/owner-3-validation.md` (who applies this) · `bin/grade-block` (layer 1) ·
`rules/case-dangerous-default.md` (source of several typical failures).
