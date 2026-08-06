# EXPERTISE · DOC-STRUCTURE — a document that can be found and trusted
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
**Ticket:** F1-ter-2 · ✅ **FILLED 2026-08-05 — the LAST discipline. All 7 now carry criterion.** · **Branch of:** `principles/owner-1-docs.md` (documentation format)
**Language:** US English · **Read by:** owner-1 before writing a document, owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for how a document is built** — its shape, its size, its metadata, its
pointers. Written by Brian so the system can apply it.

> ⛔ **The AI does not invent criterion** (ADR-003).

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning · doc-structure ⬅ THIS FILE
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional · val-integration
```

**Why structure is its own discipline, separate from planning:** a plan is judged by whether it
can be executed; a document is judged by whether it can be **found, dated and trusted** months
later. The measured failure was structural, not editorial: **15 of 188 documents had a date.**

---

## 1 · CONTEXT ALREADY CAPTURED

### Measured failures this criterion exists to prevent

| Failure | Measurement |
|---|---|
| Documents with no auditable header | **15 of 188** had a date |
| An index that inventoried a fraction of reality | **35 of 188** |
| A duplicated table instead of a pointer | the decisions table diverged: **75 vs 37 rows** |
| Files far over any readable size | `memory/PENDIENTES.md` at **240 KB** |
| `-bis` / `-TER` numbering | the smell that says *split me* |

> ⭐ **The measured law:** the only file with a declared limit (`RETOMAR.md`, ~200 lines) is the
> only one that never overflowed. A limit that is enforced is a limit that holds.

**Precedents already built that this criterion should formalize:**
- `rules/contract-document.md` · `rules/contract-block.md` · `rules/contract-adr.md`
- `rules/NAMING_CONVENTION.md` — US English for instructions, Spanish for Brian's thinking
- size limits per type (ADR-027), enforced by `bin/check-health`

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

### 2.1 · Architecture — where a document lives
**Question (frame):** does each piece have one responsibility, at the right level?
**Here:** which folder owns it, and when one document should be two.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A document is split when any of these three holds
>
> | # | Split when… | Why |
> |---|---|---|
> | 1 | **it contains TWO DISTINCT THINGS** | ADR-027's master rule. `principles/owner-0-voice.md` mixes the voice and the delivery contract: two subjects, two documents |
> | 2 | **two different people maintain it** | same criterion Brian set for components (`dev-frontend.md` §2.1): two reasons to change = two pieces |
> | 3 | ⭐ **it exceeds its declared size limit** | Brian, 2026-08-05 — see below |
>
> ### ⭐ Signal 3 hardens ADR-027 — Brian, 2026-08-05
>
> > *"También el tamaño: si el tamaño excede el límite **debe partirse en dos y estar relacionados
> > o apuntando**."*
>
> ADR-027 said the limit is **the signal, not the cause** — a file over its ceiling was a hint to
> look for two subjects. **This makes it an obligation:** over the ceiling, it splits. And the two
> halves **point at each other**, because a split that leaves orphans trades one problem for a
> worse one — a reader who finds half the answer and does not know the other half exists.
>
### ⛔ THE ONE EXCEPTION — a SOURCE OF TRUTH is never split by size

> **Brian, 2026-08-05:** *"deja el archivo como está, intacto como en v1. Es fuente de verdad, y
> las fuentes de verdad no importa el tamaño del archivo."*

**A source of truth is the document that DECIDES** — the one every other cites when they disagree.
`docs/Arquitectura_Mente_OS_v2_Bloques.md` (2,454 lines) is one: 46 documents point at it, and the
whole v2 design was settled in it.

**Why size must not govern it, and it is not indulgence:**

| | |
|---|---|
| **Splitting it invents a second authority** | with two files, the next reader must decide which one wins — and *"which of the two is true"* is the exact ambiguity a source of truth exists to remove |
| **Its value IS its completeness** | you read it to settle an argument, not to skim. A ceiling optimises for reading; this file optimises for **deciding** |
| **Measured precedent** | it was split once (July, `blk-split-architecture`). Result today: **74% duplicated** across `docs/architecture/`, 330 lines living only in the original. **The split created the divergence it was meant to prevent** — the same shape as the 75-vs-37 table |

**How to tell one apart:** a source of truth is cited *to resolve*, not *to consult*. If a document
is what other documents point at when they disagree, its ceiling does not apply — **and the
exception is written in its header, never assumed.**

⚠️ **This is a narrow door, not a loophole.** Everything else over its ceiling still splits: being
long is not being authoritative. Today exactly one file claims it.

---

> ⚠️ **Consequence of §2.1, stated plainly:** files over their ceiling are **pending splits**, not
> warnings. Done 2026-08-05: `principles/owner-0-voice.md` (582 → 285, its §7 became
> `principles/contract-delivery.md`) · `dev-database.md` (381 → 364, its imported section became
> `principles/imported-patterns.md`) · `memory/RETOMAR.md`. **Exempt as a source of truth:**
> `docs/Arquitectura_Mente_OS_v2_Bloques.md`.

### 2.2 · Data design — the metadata
**Question (frame):** does it represent the domain? Are impossible states impossible?
**Here:** which header fields are mandatory, and what an impossible `Type` would be.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## Four mandatory fields: `Status` · `Type` · `Updated` · `Owner`
>
> **Missing any one of them, the document does not meet its own contract** (§2.5) — whatever its
> body says. These are not bureaucracy: each one answers a question the reader cannot answer alone.
>
> | Field | The question it answers | Missing it means |
> |---|---|---|
> | `Status` | is this still in force? | you must read it whole and still not know |
> | `Type` | what limits apply? | the ceiling and the mandatory fields cannot be checked (ADR-027) |
> | `Updated` | when was it last true? | **the 15-of-188 failure** |
> | `Owner` | who keeps it true? | nobody updates it and no alarm fires |
>
> ⚠️ **`Type` is the one that fails silently**, because a wrong type does not look wrong: the
> document reads fine and **the wrong ceiling gets enforced against it**. It is the metadata
> equivalent of `kind` — a field whose value silently changes how everything else is judged.

### 2.3 · Abstraction — pointer vs copy
**Question (frame):** the right level, neither copied nor over-generalized?
**Here:** when to point at a document and when to restate it. The 75-vs-37 divergence is the case.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 IF THE DATUM HAS AN OWNER SOMEWHERE ELSE — ALWAYS A POINTER.
>
> **The value is read from where it is measured.** This is the rule Brian already applied when he
> stripped the state out of `CLAUDE.md`: a router that declares state goes stale, because a copied
> number is correct exactly once.
>
> ### ✅ What MAY be copied — two cases, both narrow
>
> | Case | Why it is safe |
> |---|---|
> | **What can no longer change** — a historical quote, a closed decision | it has no future in which to diverge |
> | **The SUMMARY, never the detail** | one orienting sentence lets you read without jumping; the full content stays at its source |
>
> **The measured failure:** a duplicated table diverged to **75 rows against 37**. Nobody noticed,
> because both looked correct on their own — which is exactly the shape of the seam failures
> `val-integration.md` governs: each piece fine, the pair wrong.
>
> ⚠️ **Note what Brian did NOT choose:** *"never duplicate a table, ever"* was on the table and he
> left it out. **The rule is by OWNERSHIP, not by shape** — a table of things that can no longer
> change may be copied; a two-line list of live values may not. Same axis as `val-integration.md`
> §2.3: *who owns the datum decides*, not what it looks like.

### 2.4 · Naming — files and sections
**Question (frame):** does the name say what it does without opening it?
**Here:** what makes a filename findable six months later.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> | # | Rule | ✅ / ⛔ |
> |---|---|---|
> | 1 | **The name says the SUBJECT, never the moment** | ✅ `rule-shipping-flow` — ⛔ `notas-del-lunes`, `v2-final`. Six months later you search by subject; nobody remembers which Monday |
> | 2 | **A prefix that groups the family** | `rule-` · `contract-` · `ADR-` · `dev-` · `val-` · `doc-`. The prefix makes the family visible **in `ls`** — a flat list hides which owner each file answers to, and that is exactly how the owner/discipline confusion started |
> | 3 | ⛔ **No `-bis`, `-v2`, `-final`, `-nuevo`** | already a registered smell: `-bis`/`-TER` numbering is what says **split me** (§2.1). A version in the name means the previous one was never resolved |
>
> **Rule 3 is a symptom, not a style preference.** `-v2` in a filename says two documents exist for
> one subject and nobody decided which is true — which is §2.3's divergence waiting to happen,
> with the added cost that the reader cannot tell which to trust.

### 2.5 · Contracts — the header and the limits
**Question (frame):** are the interfaces declared? Are errors part of the contract?
**Here:** what a reader is entitled to assume from `Status: current`.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## `Status: current` is a CONTRACT with four terms. Any missing, and it promises nothing.
>
> | # | The reader may assume… | The header field | Why |
> |---|---|---|---|
> | 1 | ⭐ **somebody verified it, and it says with what** | `Verified by: bin/check-links` — a script or a person, named | without this, `current` is an opinion wearing a status |
> | 2 | **its date reflects the last real change** | `Updated:` | an old date with `Status: current` is the fossil signal `bin/check-health` flags at 90 days |
> | 3 | **its type declares its limits** | `Type:` | the type decides the line ceiling and which fields are mandatory (ADR-027). A wrong type breaks the verification silently |
> | 4 | **whoever maintains it is named** | `Owner:` | a document with no owner is updated by nobody and ages with no alarm going off |
>
> ⭐ **Term 1 is what separates this from bureaucracy.** The other three are metadata; **this one is
> the measurement**. It is `val-functional.md` §2.2 applied to a document: *a datum counts as proof
> when it names how it was obtained.* A header that claims `current` without saying who checked it
> is asserting, not reporting.
>
> **How to apply it:** read the header alone. If you cannot say **who verified it, when, under what
> type and who owns it**, the document does not meet its own contract — whatever its body says.

### 2.6 · Necessity — does this document have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** when a document should be a section of another one, or a memory instead.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A document should NOT exist when either holds
>
> | # | Do not create it if… | What it should be instead |
> |---|---|---|
> | 1 | **its content fits in one that already exists** | a **section** of that one. A new document means another index entry, another header, another date to keep true — cost paid forever for content that had a home |
> | 2 | **nobody will read it twice** | a **memory** or a session note. What is consulted once and never again is not a system document |
>
> **The tension with §2.1, and how it resolves:** §2.1 splits what is too big; this refuses what is
> too small. Both answer the same question — *does this deserve its own header, owner and date?*
> Under the ceiling and read repeatedly → yes. Otherwise → section, or memory.
>
> **How to apply it:** before creating a file, name the document it could be a section of. If one
> exists and the answer is only *"it would make that file long"*, that is not a reason — that is
> §2.1's problem, and it has its own rule.

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — never, no exceptions
>
> | # | ⛔ Never | The case |
> |---|---|---|
> | 1 | **Write a live number in prose** | cite the metric and its source (`docs/METRICS.md`), never the value. **A copied number is correct exactly once** — why `CLAUDE.md` stopped declaring state |
> | 2 | **Leave a pointer to something that does not exist** | *"a pointer to nothing is worse than no pointer: it is read as a promise."* Caught by the battery on this very session, against the AI |
> | 3 | 🔴 **Delete history so a check turns green** | already decided when four validators kept the comments documenting a past incident: **erasing the trail to satisfy a grep destroys why the rule exists** |
> | 4 | 🔴 **Write a secret, not even as an example** | what is written stays in the transcript, and the `.jsonl` files are not editable. **A leaked secret is ROTATED, not deleted** (`rules/rule-config-hygiene.md` §1.1) |
> | 5 | **Duplicate what has an owner elsewhere** | §2.3 — *a duplicated table is a pointer waiting to diverge* (75 vs 37) |
>
> ⭐ **Rule 3 is the one that protects the other four.** The moment a check can be satisfied by
> deleting evidence instead of fixing the cause, every rule in this file becomes optional — the
> system starts measuring what is convenient rather than what is true.

---

## 4 · WHAT MAKES BRIAN REJECT A DOCUMENT

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## FOUR SIGNALS — any ONE and the document is not usable
>
> | # | Signal | The measurement behind it |
> |---|---|---|
> | 1 | ⭐ **You cannot tell whether it is still current or a fossil** | **15 of 188 documents had a date.** Without a date and a status you must read it whole to find out if it still applies — and you still do not know |
> | 2 | **It asserts numbers that are no longer true** | a number copied by hand is correct **exactly once**. This is why `docs/METRICS.md` exists and why `CLAUDE.md` stopped declaring state |
> | 3 | **It does not say why it exists or who it serves** | with no Purpose, whoever inherits it cannot decide whether to keep it or delete it — so they keep it, forever |
> | 4 | **You must read it whole to find one thing** | with no index and no navigable sections, a long file is a file nobody opens twice. `memory/PENDIENTES.md` reached **240 KB** |
>
> ⚠️ **Signals 1 and 2 are the pair that costs most**, because they fail in opposite directions:
> the undated document makes you distrust something true, and the stale number makes you trust
> something false. **The second is worse** — a wrong answer is more expensive than no answer.

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**

**Suggested questions for the interview:**

1. What do you demand of a document before it counts as finished?
2. What makes a document useless to you six months later?
3. When should something be a pointer instead of a copy?
4. How do you decide a file is too long — by lines, or by something else?
5. What has to be in the header for you to trust what it says?
6. Which documentation mistake do you see most often?
7. When is a document not worth writing at all?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 evaluates the 6 dimensions using it |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are FILLED — wiring and criterion are both live.**

---

Related: `principles/owner-1-docs.md` (the owner this branches from) · `principles/expertise/doc-planning.md`
(its sibling) · `rules/contract-document.md` · `rules/NAMING_CONVENTION.md` ·
`docs/PENDING-BRIAN.md` (the index of every hole).
