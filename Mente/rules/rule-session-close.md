# RULE · SESSION CLOSE
**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** grave #2 of the F0-F2 audit · **Source:** `CLAUDE.md` (rule since 2026-07-14)
---

## Purpose

What must be written **before** a `/clear`. This rule already existed in v1 and **v2 had not
inherited it** — found in the F0-F2 audit.

---

## 1 · THE RULE

> ## No `/clear` without registering the session first.

`/clear` is a **cut, not a save.** It writes nothing. Whatever is not on disk is lost, with no warning.

---

## 2 · MEASURED COMPLIANCE — why this rule needs enforcement

The rule has existed since 2026-07-14. Measured 2026-07-27:

| | |
|---|---|
| Sessions in the project | 11 |
| **Registered** | **6** |
| 🔴 **Never registered** | **5** |

**The worst offender:** session `4c187f33` — 23.4 MB, 1,033M cache_read tokens, 999K peak context,
**4 days open**. The second-largest session in the project's history, **invisible in the telemetry.**

> From that unregistered session came the 21-jul incident (*"no eres el mismo de siempre, no me
> sirves así"*) — which was **documented nowhere** until it was recovered from the raw `.jsonl` on
> 2026-07-27, six days later.

---

## 3 · WHAT GETS WRITTEN — in this order

| # | Where | What |
|---|---|---|
| 1 | `Cerebro/Registro_Conversaciones.md` | 🔴 **mandatory** — the session autopsy (§4) |
| 2 | `memory/RETOMAR.md` | where we left off + next step. Fresh and small (≤250 lines) |
| 3 | `memory/Bitacora_Progreso.md` | the period's milestones |
| 4 | memories + `MEMORY.md` | one memory per fact, with its index line |
| 5 | `memory/PENDIENTES.md` | non-urgent findings |
| 6 | The active block | §E State · §G Decisions · §J Context consolidated |

---

## 4 · THE SESSION AUTOPSY — required fields

```markdown
| # | ID (short) | Start | End | Size | Msgs | Peak context | Verdict |
```

Plus a section with: **topics · consumption · when consumption started growing abnormally ·
anything strange · reason for closing.**

**Thresholds** (calibrated with real data, `Cerebro/Registro_Conversaciones.md`):

| Signal | 🟢 healthy | 🟡 watch | 🔴 act now |
|---|---|---|---|
| `.jsonl` size | <15 MB | 15-50 | >50 |
| Live context per request | <200K | 200-500K | **>500K** |
| Session age | days | 1-2 weeks | weeks without `/clear` |
| Repeated `Connection closed mid-response` | — | occasional | **repeated = saturated context** |

---

## 5 · ⭐ WHY IT KEEPS FAILING — and what changes in v2

**The cause:** registration is an **event at the end.** It depends on someone remembering after a
30-hour session. And when the session dies suddenly — quota exhausted, crash, auto-compaction —
**there is no close at all.**

**Measured:** 8 auto-compactions (*"ran out of context"*) on 7-jun, 30-jun, 1-jul, 3-jul, 23-jul…
Each one was written by a model and **nobody reviewed any of them.**

### What v2 changes

| v1 | v2 |
|---|---|
| Everything written at close | ⭐ **written DURING** — *if a decision is not written, it is not made* |
| Depends on remembering | `bin/check-health` flags an open session over the threshold |
| A sudden death loses everything | the block already holds scope, decisions and graph on disk |

> **The block is the mitigation.** Even with no clean close, §A-E survive — and that is what the
> sufficiency test guarantees.

---

## 6 · WHAT `bin/check-health` FLAGS

```
🔴 SESSION
   · live context over 200K / 500K
   · session open longer than 48h
   · repeated "Connection closed mid-response"
   · previous session with no entry in Registro_Conversaciones.md
```

---

Related: `Cerebro/Registro_Conversaciones.md` · `CLAUDE.md` (original rule) ·
`contract-block.md` §E/§G/§J · `principles/owner-3-validation.md` §4 (closing procedure).
