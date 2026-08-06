# EXPERTISE · DOC-PLANNING — a plan someone can execute
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Ticket:** F1-ter-1 · ✅ **FILLED 2026-08-05 by Brian** · **Branch of:** `principles/owner-1-docs.md` (documentation format)
**Language:** US English · **Read by:** owner-1 before writing a plan, owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for planning**, written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (ADR-003). It asks, structures and applies — it never
> fills this in on its own. That error is what produced *"todo está hecho como la IA quiso."*

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning ⬅ THIS FILE · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration
```

**Why planning is its own discipline:** a plan is judged by whether someone else can execute it
without asking what was meant. That is a different skill from formatting a document correctly —
a perfectly formatted plan can still be unexecutable.

---

## 1 · CONTEXT ALREADY CAPTURED

### Anchors already stated by Brian — to expand, not to replace

| Quote | Date |
|---|---|
| *"que sepa por qué se hizo esto primero antes que otro punto"* | 2026-07-27 |
| *"explicar antes de construir · aprobar antes de ejecutar"* | LOCKED rule |
| *"nunca plan global; por pieza → alinear visión → aprobar → construir"* | 2026-07-20 |

**Precedents this criterion should formalize:**
- the default plan sections (`principles/owner-1-docs.md` §2) — purpose · **why this order** · phases and
  tickets · what can go wrong · what it does NOT do
- *"the contract is a floor, not a ceiling"* — a plan that discovered something new says so
- the Método F: `rules/ESTANDAR_Metodo_Fases_F.md`

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

The frame lives in `rules/qa-dimensions.md`. What each demands **here** is Brian's criterion.

### 2.1 · Architecture — the shape of the plan
**Question (frame):** does each piece have one responsibility, at the right level?
**Here:** is each phase one thing, or is it three things sharing a number?

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A phase delivers ONE verifiable thing. And it declares what it depends on.
>
> | # | Rule | Why |
> |---|---|---|
> | 1 | **One phase, one verifiable delivery** | if it delivers two, you do not know which one failed when something breaks. The same test already applied to checks (`val-functional.md` §2.1) and components (`dev-frontend.md` §2.1) |
> | 2 | **Every phase declares which other it depends on** | the dependency graph is **written, not inferred**. What depends on nothing can run in parallel — and that is only visible if it was declared |
>
> ⚠️ **Rule 1 does not contradict §2.3's "one block spans several disciplines".** A block groups
> what must ship together; **inside it, each phase still delivers one verifiable thing.** Touching
> DB + backend + frontend is one block with several phases, never one phase doing three things.

### 2.2 · Data design — what the plan states as fact
**Question (frame):** does it represent reality? Are impossible states impossible?
**Here:** what must be MEASURED before the plan claims it.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## FOUR THINGS A PLAN MEASURES BEFORE IT CLAIMS THEM
>
> | # | Measured | Why | The case |
> |---|---|---|---|
> | 1 | ⭐ **every limit or blocker the plan declares** | *"un límite que no has verificado no es un límite: es una suposición disfrazada"* | 2026-08-03: a sub-block was declared BLOCKED without consulting the source. The docs answered it — the three sub-blocks took **one hour** |
> | 2 | **the current state the plan starts from** | how many there are, what fails today, what already exists. **Without a measured BEFORE there is no way to know the plan improved anything** (`val-functional.md` §2.2 condition 2) |
> | 3 | **who consumes what will be touched** | importers measured, never remembered — `instancias.ts` had 26 mentions and **9 real imports** |
> | 4 | **that the piece it claims to reuse exists and does that** | planning on a function believed to exist is planning on smoke |
>
> ⚠️ **Number 1 is the one that fails silently**, because a false blocker never announces itself:
> the work simply does not get done, and nobody measures what did not happen. **A plan reporting
> blocked without measuring is the same defect as a check reporting green without measuring**
> (`rules/rule-checks-must-measure.md`), one level up.

### 2.3 · Abstraction — the level of detail
**Question (frame):** the right level, neither repeated nor over-generalized?
**Here:** when a ticket is too big to execute and when it is so small it is noise.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## ⭐ FIRST, WHAT A BLOCK IS — Brian, 2026-08-05
>
> > *"Tiene una comunicación con 2 o más archivos: si editar una función de la demo obliga a tocar
> > BD + frontend + backend, aquí hay un caso donde tocas 3 funciones diferentes — **se contempla
> > como un BLOQUE**."*
>
> **This is not a fifth size signal: it decides what a phase IS.** A change that spans several
> disciplines is **one block**, not three phases that happen to be related. Splitting it by
> discipline is how one half ships and the other does not — and the seam between them is where
> `val-integration.md` says the expensive bugs live.
>
> ⚠️ **And it settles the ordering inside that block:** the pieces are worked in the order
> `dev-backend.md`/`blk-demo` §G already set — **senders first, the strict receiver second** — never
> "whatever is quickest first".
>
> ## THEN, THE FOUR SIGNALS THAT A PHASE IS TOO BIG
>
> | # | Signal | Why |
> |---|---|---|
> | 1 | **It does not fit in one session without losing context** | ⭐ the 21-jul incident: 5 days, 821K of context, measured degradation — *"no eres el mismo de siempre"*. If it does not fit, it is split |
> | 2 | **It touches pieces that cannot be reverted together** | undoing it needs N coordinated changes → it was never one phase, it was N (`val-integration.md` §2.1 condition 4) |
> | 3 | **Its success criterion needs an *"and"*** | the same test used for components and for checks: one sentence, or it is two phases |
> | 4 | **Nobody can execute it without asking Brian** | a decision surfacing mid-execution that the plan did not anticipate means the cut was wrong |
>
> **How to apply it:** before approving, name the disciplines the change touches (one block, per the
> rule above), then walk the four signals. Any one present → split, and say in §G where you cut.

### 2.4 · Naming — phases and tickets
**Question (frame):** does the name say what it does without reading the body?
**Here:** does `F4-2` say what it delivers, or does it need the paragraph under it?

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## The name says what it DELIVERS, not what it consists of.
>
> ✅ *"F4-2 · the battery tests its own checks"* — ⛔ *"F4-2 · system improvements"*
> **It must be understandable without the paragraph below it.**
>
> ## ⛔ No phase called "polish", "improvements" or "cleanup"
>
> A name that does not say what it delivers **hides undefined scope** — it is `kind` at the plan
> level: one label covering whatever ends up inside. And undefined scope cannot be approved,
> because there is nothing concrete to approve.
>
> **How to apply it:** read the phase names alone, with no bodies. If you cannot say what the plan
> will produce, this dimension is 🔴.

### 2.5 · Contracts — what the plan promises
**Question (frame):** are the interfaces declared? Are errors part of the contract?
**Here:** the success criterion of each ticket. *"It works"* is not a criterion.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A success criterion carries FOUR things. Fewer, and the ticket is not planned.
>
> | # | It states… | Example | ⛔ Not enough |
> |---|---|---|---|
> | 1 | **a concrete datum, measurable afterwards** | *"the battery goes from 160 to 165"* · *"broken citations = 0"* | *"it works"* |
> | 2 | **the exact command that verifies it** | `bin/test-f0-f6` · `bin/grade-block demo --root ../marca-personal` | *"run the tests"* — whoever executes would invent their own proof |
> | 3 | **what would be SEEN if it failed** | *"the check turns red naming the piece"* | silence — a failure nobody would notice |
> | 4 | **who signs it off** | a script, or Brian by name | left blank, which lets the AI approve its own work |
>
> **Requirement 3 is `val-functional.md` §3 moved forward in time:** *never close something whose
> failure you would not notice* — asked **before building**, not at the close. If the plan cannot
> say what failure looks like, the ticket has no way to be wrong, and something that cannot be
> wrong cannot be verified either.
>
> **Requirement 4 is what stops self-approval** (ADR-003): when the criterion needs judgement, the
> plan names who judges. A criterion with no judge is a criterion the executor grades itself on.

### 2.6 · Necessity — does this phase have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** which phase could be deleted with nothing lost.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A phase is deleted when nothing is lost by not doing it.
>
> **The test:** remove it and describe the final result. If it is the same, it was filler.
>
> ⚠️ **Filler in a plan is not harmless.** It consumes the session that §2.3 signal 1 is trying to
> protect — every phase that delivers nothing is context spent on nothing, and context is the
> resource whose exhaustion caused the 21-jul degradation.
>
> **How to apply it:** for each phase, name what would be missing at the end if it were skipped.
> If the answer is *"nothing concrete"*, delete it — do not shrink it.

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — never, no exceptions
>
> | # | ⛔ Never | Source |
> |---|---|---|
> | 1 | **Build without explaining and without approval** | LOCKED rule: *explain before building · approve before executing*. The phase is explained, approved, and only then executed |
> | 2 | **A global plan instead of one per piece** | *"nunca plan global; por pieza → alinear visión → aprobar → construir"* (2026-07-20) |
> | 3 | **Leave a `PENDING · BRIAN` hole that could be derived** | a hole the AI could have filled by reading the repo is not a decision — it is unfinished work handed over as if it were one (`rules/block-lifecycle.md` §1) |
>
> ### ⭐ AND WHEN THE HOLE IS REAL — Brian, 2026-08-05
>
> > *"Si existe un hueco y se necesita tomar una decisión, **márcalo como un pendiente y asígnamelo**
> > para que podamos avanzar."*
>
> **A genuine hole does not stop the plan — it becomes an assigned pending.** Three requirements,
> and the third is the one usually missing:
>
> | Requirement | ⛔ Not enough |
> |---|---|
> | **filed** in `memory/PENDIENTES.md`, not only mentioned in passing | a note inside a file nobody opens |
> | **assigned to Brian by name**, with the decision stated in one line | *"pending"* with no owner — that is an abandoned block (`rules/block-lifecycle.md` §5) |
> | ⭐ **everything that does NOT depend on it keeps moving** | stopping the whole plan over one decision |
>
> **This is the counterweight to rule 3.** Rule 3 forbids inventing a hole out of laziness; this
> says a real hole is **routed, never used as a reason to stop.** Both together: *derive what you
> can, ask what you cannot, and keep going with the rest.*

---

## 4 · WHAT MAKES BRIAN REJECT A PLAN

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## SIX SIGNALS — any ONE and the plan goes back
>
> | # | Signal | Why |
> |---|---|---|
> | 1 | **It does not say what will NOT be touched** | with no written boundary the AI expands on its own. Already an owner-2 acceptance criterion |
> | 2 | **It does not explain WHY that order** | *"que sepa por qué se hizo esto primero antes que otro punto"* (2026-07-27). An order with no reason cannot be argued with, so it cannot be corrected |
> | 3 | **It decides something that was Brian's to decide** | the plan settles a criterion only he can set instead of asking. ADR-003 seen from the planning side |
> | 4 | **It omits something believing it is "already covered"** | judging what is redundant **is itself criterion**, and getting it wrong deletes something useful in silence. Measured today: the AI proposed importing only ~40% of an external skill; Brian overruled it |
> | 5 | ⭐ **It omits something believing BRIAN already knows it** | *"no omitas algo porque crees que ya lo sé"* — Brian, 2026-08-05 |
> | 6 | ⛔ **It excuses itself with *"I thought it was like this"* or *"I did not know"*** | *"y mucho menos decir: ah, pensé que era de esta forma, o no sabía"* — Brian, 2026-08-05 |
>
> ### ⭐ Signals 5 and 6 are one rule, and it is about how the AI behaves
>
> > **The plan does not rely on what the reader already knows, and never explains itself
> > afterwards with not having known.**
>
> Assuming Brian already knows something is the same failure as omitting it for being covered
> (signal 4) — **the AI deciding what does not need saying.** And *"I did not know"* is not an
> excuse but a **confession that it did not ask**: the plan was written over an unverified
> assumption, when asking cost one question. It is `rules/rule-checks-must-measure.md` applied to
> planning: **an unverified limit is a guess wearing a limit's clothes.**

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**
> Never the reverse — a draft written first comes out as *"use best practices."*

**Suggested questions for the interview:**

1. What do you demand of a plan before approving it?
2. What makes you reject one outright?
3. How do you know a phase is too big before it is executed?
4. What has to be written down for you to trust the order of the phases?
5. Which planning mistake do you see most often and bothers you most?
6. When is a plan finished — as opposed to just long?
7. What must a plan say about what it will NOT do?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 evaluates the 6 dimensions using it |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are FILLED — wiring and criterion are both live.** Layer 1 of QA
> (`bin/grade-block`) does not depend on this file.

---

Related: `principles/owner-1-docs.md` (the owner this branches from) · `principles/expertise/doc-structure.md`
(its sibling) · `rules/qa-dimensions.md` (the frame) · `rules/ESTANDAR_Metodo_Fases_F.md` ·
`docs/PENDING-BRIAN.md` (the index of every hole).
