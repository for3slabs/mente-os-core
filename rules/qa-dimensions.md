# QA DIMENSIONS · the senior review
**Status:** draft · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
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

> ⬜ **PENDING · BRIAN — your criterion**
>
> What goes here: what *you* demand before accepting an architecture. What makes you reject a
> structure. The failure you see most often.
>
> Why the AI does not write it: this is criterion, not observation (architecture §9.1).

---

### 2.2 · DATA DESIGN

**Question:** does the schema represent the domain? Is it normalized? Are impossible states
impossible?

**Required evidence:** the real schema + one case the model **cannot** represent incorrectly.

**Typical failure (measured):** `kind` (a cookie value) was used as if it were the real instance →
the same bug appeared in 6 files.

> ⬜ **PENDING · BRIAN — your criterion**
>
> Anchors already stated by Brian, to expand here:
> - *"vamos a desarrollar una base de datos, no un MVP pedorro"*
> - *"si no tenemos control estamos mal"*
> - the values that must live in the DB and never in code (`demo_config` precedent)

---

### 2.3 · ABSTRACTION

**Question:** is it at the right level — neither copied three times nor generalized for a single use?

**Required evidence:** the places where it repeats, **or** the real usages of the abstraction.

**Typical failure (measured):** "resolve the instance" copied in 6 places; the fix required a
*"barrido completo del patrón"* four commits later.

> ⬜ **PENDING · BRIAN — your criterion**

---

### 2.4 · NAMING

**Question:** does the name say what it does, without reading the body?

**Required evidence:** explain three names from the block **without opening the file**.

**Typical failure (measured):** `kind` does not say what it distinguishes — reading the body was
required, and that ambiguity produced the 6-file bug of §2.2.

> ⬜ **PENDING · BRIAN — your criterion**

---

### 2.5 · CONTRACTS

**Question:** are the interfaces between pieces declared? Are errors part of the contract?

**Required evidence:** the real signature + what happens when it fails.

**Typical failure (measured):** 4 functions in `userStore.ts` with no declared failure mode — and
44 DB accesses with **0 try/catch** (fixed in U1).

> ⬜ **PENDING · BRIAN — your criterion**

---

### 2.6 · 🔴 NECESSITY

**Question:** does **every file that exists HAVE to exist?**

**Required evidence:** for each new file — who consumes it, and why it could not live somewhere else.

**Typical failure (measured):** `accountStore.ts` had **0 consumers** after the migration and stayed
in the tree.

> **This dimension is the direct answer to Brian:** *"que lo que está es necesario, y no se lo
> inventó, o lo quiso mover, o dijo 'ah, lo dejo aquí por si lo necesitamos'."*

> ⬜ **PENDING · BRIAN — your criterion**

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
| Database | `principles/expertise/dev-database.md` | ⬜ **pending · Brian** — F1-2 |
| Backend | `principles/expertise/dev-backend.md` | ⬜ pending · Brian — F1-bis |
| Frontend | `principles/expertise/dev-frontend.md` | ⬜ pending · Brian — F1-bis |

> ⚠️ **Until at least one is filled, layer 2 is an empty form.** Layer 1 (`grade-block`) works
> without it — that is why F4 can run before F1-bis closes.

---

## 5 · METHOD FOR FILLING THIS

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> **Never** *"the AI drafts and Brian corrects"* — that produces *"use best practices"*.

Recorded as risk #1 of phase F1 in the implementation plan.

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` §12-QUINQUIES (the design) ·
`principles/owner-3-validation.md` (who applies this) · `bin/grade-block` (layer 1) ·
`rules/case-dangerous-default.md` (source of several typical failures).
