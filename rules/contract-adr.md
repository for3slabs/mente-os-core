# CONTRACT · ADR (Architecture Decision Record)
**Status:** current · **Type:** contract · **Updated:** 2026-07-29 · **Owner:** brian
validator from 2026-07-27 onward.
**Where ADRs live:** `rules/decisions/ADR-NNN-short-name.md`
**Generated index:** `docs/DECISIONS.md` — produced by `bin/generate-index`, never written by hand.
---

## 0 · WHY THIS EXISTS

> **Brian, 2026-07-27:** *"para generar una nueva decisión o una nueva regla o ruta, ¿existe un
> estándar que podamos crear para que no se salga de control?"*

**There was none.** 26 decisions were taken in a single session with no standard. Measured state
before this contract:

| Symptom | Data |
|---|---|
| Decisions taken | **26** |
| With an individual date | ❌ only the table header said `2026-07-27` |
| With their own reversible file | ❌ none |
| **Duplicated across two documents** | 🔴 **yes — 75 rows vs 37, already diverged** |
| Can you tell which decision superseded another? | ❌ no |

**The precedent that makes this urgent:** `CLAUDE.md` governs the whole system and has **one single
commit** in its history. The rules changed many times and **not one change left a trace.**

> This contract exists so v2 does not repeat that.

---

## 1 · THE THREE RULES

| # | Rule | What it prevents |
|---|---|---|
| **1** | **One decision = one file.** Never a row in a shared table | the duplication that already happened |
| **2** | **`docs/DECISIONS.md` is GENERATED** from the ADR files — nobody writes it | an index that lies (measured: 35/188 in the old README) |
| **3** | **A decision is never edited — it is SUPERSEDED** by a new one that points at it | losing the history of *why* it changed |

> ⚠️ **Rule 3 is the one people break.** Editing an accepted ADR erases the reason the old decision
> existed. If the decision changes, write `ADR-NNN+1` with `supersedes: ADR-NNN`.

---

## 2 · THE TEMPLATE

```markdown
# ADR-NNN · Short imperative name

date: 2026-07-27
status: accepted
decided-by: brian
supersedes: —
superseded-by: —

## Context
The problem that forced the decision — **with data, not adjectives.**

## Decision
What was decided, in one sentence.

## Rationale
Why this and not the alternative. Name the alternative that was rejected.

## Evidence
The measurement that backs it. If there is none, say `none — judgment call`.

## Reverting
How to undo it if it turns out wrong.
```

### Field rules

| Field | Required | Notes |
|---|---|---|
| `date` | ✅ | ISO `YYYY-MM-DD` |
| `status` | ✅ | `proposed` · `accepted` · `superseded` · `reverted` |
| `decided-by` | ✅ | `brian` for criterion · `ai` only for pure form |
| `supersedes` / `superseded-by` | ✅ | `—` when none. **Both sides must point at each other** |
| `Context` | ✅ | with data |
| `Decision` | ✅ | one sentence |
| `Rationale` | ✅ | must name the rejected alternative |
| `Evidence` | ✅ | a number, a file, a command — or `none — judgment call` |
| `Reverting` | ✅ | **if it cannot be undone, say so explicitly** |

> ⭐ **`Evidence` and `Reverting` are what make this more than a changelog.** A decision with no
> evidence is an opinion; a decision with no exit is a trap.

---

## 3 · WHAT ELSE NEEDS AN ADR (not just decisions)

| New object | Minimum requirement |
|---|---|
| **Decision** | an ADR with all fields |
| **Rule** (`rules/rule-*.md`) | born from an ADR · the rule links back to its ADR |
| **Path** (`additionalDirectories`, a pointer) | inline comment with **date + reason** (§12-S.2) · passes the non-redundancy test (§12-S.3) |
| **Validator** (`bin/*`) | an ADR stating what it checks and why |
| **Expertise criterion** | lives in `principles/expertise/*` · the ADR records *that it was defined*, not its content |

> **A path does not need a full ADR** — that would be bureaucracy. It needs a reason in a comment.
> The heavier the object, the heavier the record.

---

## 4 · NUMBERING

- Sequential, zero-padded to three: `ADR-001`, `ADR-027`.
- **Numbers are never reused**, not even for reverted decisions.
- A reverted ADR keeps its number and its file, with `status: reverted`.

---

## 5 · WHAT `bin/check-blocks` VERIFIES

```
🔴 ADR
   · required field missing
   · status not in the allowed set
   · supersedes pointing at an ADR that does not exist
   · one-sided supersede link (A says it supersedes B, B does not say so)
   · duplicate ADR number
   · Evidence empty and not explicitly "none — judgment call"
```

---

## 6 · MIGRATION — the 26 decisions of 2026-07-27

> ⬜ **PENDING** — see `memory/PENDIENTES.md` §"ESTÁNDAR PARA TOMAR DECISIONES".

They currently live as rows in two duplicated tables (`Arquitectura §17.1` and `Visión §6`).
Once migrated, both tables are replaced by a pointer to the generated `docs/DECISIONS.md`.

**Order:** write the ADRs → generate the index → delete the duplicated tables.
**Never the reverse** — deleting the tables first loses the only copy.

---

Related: `NAMING_CONVENTION.md` §4.2 (`ADR-NNN-` prefix) ·
`docs/Arquitectura_Mente_OS_v2_Bloques.md` §12-SEPTIES (config hygiene) ·
`docs/DECISIONS.md` (generated index).
