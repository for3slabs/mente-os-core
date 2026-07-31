# EXPERTISE · DOC-STRUCTURE — a document that can be found and trusted
**Status:** draft · **Type:** contract · **Updated:** 2026-07-31 · **Owner:** brian
**Ticket:** F1-ter-2 · **Branch of:** `principles/owner-1-docs.md` (documentation format)
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
| Files far over any readable size | `PENDIENTES.md` at **240 KB** |
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

> ⬜ **PENDING · BRIAN**

### 2.2 · Data design — the metadata
**Question (frame):** does it represent the domain? Are impossible states impossible?
**Here:** which header fields are mandatory, and what an impossible `Type` would be.

> ⬜ **PENDING · BRIAN**

### 2.3 · Abstraction — pointer vs copy
**Question (frame):** the right level, neither copied nor over-generalized?
**Here:** when to point at a document and when to restate it. The 75-vs-37 divergence is the case.

> ⬜ **PENDING · BRIAN**

### 2.4 · Naming — files and sections
**Question (frame):** does the name say what it does without opening it?
**Here:** what makes a filename findable six months later.

> ⬜ **PENDING · BRIAN**

### 2.5 · Contracts — the header and the limits
**Question (frame):** are the interfaces declared? Are errors part of the contract?
**Here:** what a reader is entitled to assume from `Status: current`.

> ⬜ **PENDING · BRIAN**

### 2.6 · Necessity — does this document have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** when a document should be a section of another one, or a memory instead.

> ⬜ **PENDING · BRIAN**

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ⬜ **PENDING · BRIAN** — what is **never** done, no exceptions.
> Shape that works (an existing one): *"a duplicated table is a pointer waiting to diverge."*

---

## 4 · WHAT MAKES BRIAN REJECT A DOCUMENT

> ⬜ **PENDING · BRIAN** — the signals that make him say *"this is not usable."*

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

> ⚠️ **While §2-§4 stay empty, the wiring works but the criterion is void.**

---

Related: `principles/owner-1-docs.md` (the owner this branches from) · `principles/expertise/doc-planning.md`
(its sibling) · `rules/contract-document.md` · `rules/NAMING_CONVENTION.md` ·
`docs/PENDING-BRIAN.md` (the index of every hole).
