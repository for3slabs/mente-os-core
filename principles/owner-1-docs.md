# OWNER-1 · DOCUMENTATION
**Status:** current · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-4 · **Source:** architecture §4 · Encargado 1
---

## Purpose

Owns the **form** of every plan and document. First of the three owners — but with **no hierarchy**
over the other two (Brian: *"los 3 tienen el mismo nivel"*).

---

## 1 · WHAT IT OWNS

| Responsibility | Contract |
|---|---|
| The shape of every document | `rules/contract-document.md` |
| The shape of every block | `rules/contract-block.md` |
| The shape of every decision | `rules/contract-adr.md` |
| Naming of files and folders | `rules/NAMING_CONVENTION.md` |
| Size limits per type | architecture §3.2-QUATER · ADR-027 |

---

## 2 · THE IMPLEMENTATION PLAN

**Every plan is born with default sections.** At completion, **the system may add more** if the
picture turned out different from the one foreseen.

> ⭐ **The contract is a floor, not a ceiling.** A plan that discovered something new should say so —
> forcing it back into the original shape hides the finding.

### Default sections of a plan

| # | Section | Why |
|---|---|---|
| 1 | Purpose | if it needs three paragraphs, the plan does two things |
| 2 | Why this order | ⭐ Brian: *"que sepa por qué se hizo esto primero antes que otro punto"* |
| 3 | Phases and tickets | each with who carries the weight |
| 4 | What can go wrong | early signal + response |
| 5 | What this plan does NOT do | the boundary |

---

## 3 · ACCEPTANCE CRITERIA — what owner-1 rejects

| 🔴 Rejected | Why |
|---|---|
| A document with no header (`Status` · `Type` · `Updated` · `Owner`) | nothing can audit it · measured: 15 of 188 had a date |
| A `Type` that does not exist in the table | nobody knows which limit applies |
| A file over the limit for its type | ADR-027 |
| A duplicated table instead of a pointer | measured: the decisions table diverged (75 vs 37 rows) |
| Section numbering with `-bis` / `-TER` | the smell that says *split me* |
| A claim with no evidence | `owner-0-voice.md` §2.7 |

---

## 4 · WHAT IT DOES NOT DO

- It does not judge whether the code is good → **owner-2**
- It does not verify the system still works → **owner-3**
- It does not invent criterion → **Brian** (ADR-003)
- It does not decide the lane → **propagation** (`rule-lanes.md`)

---

Related: `owner-0-voice.md` (transversal) · `owner-2-dev.md` · `owner-3-validation.md` ·
`rules/contract-document.md` · `rules/contract-block.md` · `rules/contract-adr.md`.
