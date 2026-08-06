# EXPERTISE · VAL-FUNCTIONAL — does what exists actually work?
**Status:** current · **Type:** contract · **Updated:** 2026-08-05 · **Owner:** brian
✅ **FILLED 2026-08-05 by Brian** — with `val-integration.md`, **owner-3 is fully covered**: the
only owner that can refuse to close a block now judges with its own body of criterion.
**Ticket:** F1-quater-1 · **Branch of:** `principles/owner-3-validation.md` (functional-flow validation)
**Language:** US English · **Read by:** owner-3 at block close.
**Injected by:** the block's §D `Required standards` + `hooks/pre-edit-standards.py`.
---

## 0 · WHAT THIS FILE IS

The **expert criterion for proving something works** — as opposed to believing it does.

> ⛔ **The AI does not invent criterion** (ADR-003).

**Where this sits in the tree** (Brian, 2026-07-31):

```
owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-database · dev-backend · dev-frontend
owner-3 · functional-flow       ──▶  val-functional ⬅ THIS FILE · val-integration
```

**Why this discipline exists — the failure that created it:**

| When | What was said |
|---|---|
| 26-jul 06:24 | *"tiene el estado completo para retomar sin perder nada"* |
| **26-jul 06:33**, after a `/clear` | *"lo que está mal es que este archivo lo implementa a medias"* |

Same code, opposite verdicts, nine minutes apart. **A verdict that changes with context is not a
verdict — it is a mood.** This file is what makes the verdict reproducible.

---

## 1 · CONTEXT ALREADY CAPTURED

### The rule that governs everything here

> **Brian (Método F §2.4):** *"no basta probar el carril; hay que verificar que TODO sigue conectado."*

### ⭐ Affirmative verification — already LOCKED, not pending

Every check confirms with **a datum**: *"recovered X"* · *"vector = 1024 dims"* · *"21 tools"*.
**Never** *"seems fine"* · *"it should work"* · *"more or less."*

> **"More or less connected" is the declared enemy** (Método F §2.2). When something *almost*
> works → stop and investigate.

### The §5-BIS battery — inherited from v1, seven checks

Already written in `principles/owner-3-validation.md` §4 (A base suite · B real startup · C `/salud` · D memory
in depth · E every milestone · F tools · G what the phase added). **This file does not restate it —
it captures the criterion for judging its results.**

---

## 2 · THE SIX DIMENSIONS FOR THIS DISCIPLINE

### 2.1 · Architecture — the shape of the proof
**Question (frame):** does each piece have one responsibility?
**Here:** does each check prove one thing, or does a green mask two untested paths?

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 ONE CHECK PROVES ONE THING.
>
> If it proves two, a green can be **hiding an unexercised path** — and when it goes red you do not
> know which of the two broke. Both failures are the same defect: the check stopped being a
> measurement and became a summary.
>
> **The measured case:** check `5c` (2026-08-05) grepped the whole `BLOCK.md` for a rule name. It
> conflated two different things — *declared in §D* and *mentioned anywhere* — so it passed while
> the §D declaration was gone. **One check, two meanings, and the wrong one won.**
>
> **How to apply it:** state in one sentence what the check proves. If the sentence needs an *and*,
> it is two checks.

### 2.2 · Data design — the evidence itself
**Question (frame):** does it represent reality?
**Here:** which datum counts as proof, and which datum only looks like proof.

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — 🔴 the core of this discipline
>
> ## FOUR CONDITIONS FOR A DATUM TO COUNT AS PROOF — all four, not a menu
>
> | # | Condition | Why it cannot be faked | The case |
> |---|---|---|---|
> | 1 | **A CONCRETE datum the system returned** | you cannot produce it without running the thing | *"recovered X"* · *"vector = 1024 dims"* · *"21 tools"* — affirmative verification, already LOCKED |
> | 2 | **A measured BEFORE and AFTER** | a final number alone does not say anything changed | *"144 broken citations → 0"*. Without the *before*, "0 broken" might always have been 0 |
> | 3 | **The check has been SEEN TO FAIL on purpose** | a check you have only seen green is untested | 2026-08-05: check `5c` reported green while the rule was merely *mentioned* in §G — it measured nothing |
> | 4 | **Reproducible after a `/clear`** | if the result changes when context is lost, it was an impression | ⭐ **this is the case that created this whole file**: same code, opposite verdicts, nine minutes apart |
>
> ## ⛔ AND THE INVERSE: ABSENCE OF EVIDENCE IS NOT EVIDENCE
>
> **Measured 2026-08-05:** an empty scope scored 🟢 PRODUCT — zero dead files, zero broken links,
> zero duplication — because there was **nothing to measure**. Every metric was green and none had
> run. A green with no measured subject is not a pass; it is a missing measurement wearing a pass.
>
> **How to apply it:** the report shows the datum, the before→after, and how the check was seen to
> fail. ⛔ *"the tests pass"* answers none of the four.

### 2.3 · Abstraction — depth of testing
**Question (frame):** the right level?
**Here:** when a unit test is enough and when only the real system counts. Measured precedent:
*"unit tests do not exercise the actual prompt or behavior."*

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## The unit test is enough for ONE case, and only one
>
> ✅ **Pure, deterministic logic** — computation with no state, no network, no I/O. There the unit
> test is the right tool and demanding the real system is waste.
>
> ## 🔴 ONLY THE REAL SYSTEM COUNTS when either holds
>
> | # | Condition | Why the unit test cannot answer it |
> |---|---|---|
> | 1 | **It crosses a process or a network** — containers, DB, external API | the unit test proves your function, **not the cable**. This is the seam `val-integration.md` governs |
> | 2 | **It touches USER DATA** | `dev-database.md` §2.5: *"si la información de los usuarios corre peligro... perdemos credibilidad"*. Where user data is at stake, the proof is made with real data |
>
> **The decision rule:** ask what the test would still prove if the mock were wrong. If the answer
> is *"nothing"*, the mock IS the thing under test and the proof is circular.
>
> ⚠️ **Related but NOT claimed here:** the §5-BIS battery (`principles/owner-3-validation.md` §4-G)
> separately requires exercising new functionality **with a real LLM** where it applies, because
> *"unit tests do not exercise the actual prompt or behavior"*. That requirement already existed —
> it is inherited, not part of this criterion, and it was not asked in these terms.

### 2.4 · Naming — what a check is called
**Question (frame):** does the name say what it does?
**Here:** does a failing check name what broke, or only that something did?

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A failing check must be actionable WITHOUT opening the code. Three requirements:
>
> | # | Requirement | ⛔ Not enough |
> |---|---|---|
> | 1 | **Name WHAT broke, not that something broke** | *"validation failed"* → ✅ *"`bin/init` exists but the capability map never names it"* |
> | 2 | **Expected vs obtained, always** | the `expected: 0 / got: 4` format `bin/test-f0-f6` already uses. Without it you must read the source to understand the failure |
> | 3 | **Point at the rule that justifies it** | the message cites the document or ADR it comes from, so the reader knows **why** the demand exists — not just that it exists |
>
> **Why requirement 3 and not just the first two:** a check whose reason nobody can find gets
> deleted or weakened the first time it becomes inconvenient. Citing its source is what stops a
> failing check from being read as an obstacle instead of a finding.
>
> **How to apply it:** read the failure message alone, with no access to the repo. If you cannot
> say what to fix, the check fails this dimension however correct its logic is.

### 2.5 · Contracts — what green means
**Question (frame):** are errors part of the contract?
**Here:** what a reader is entitled to assume from a passing check. Measured precedent: an EMPTY
scope scored 🟢 PRODUCT because there was nothing to measure — **absence of evidence read as
evidence.**

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## A green promises TWO things, and nothing more
>
> | # | What the reader may assume | What they may NOT |
> |---|---|---|
> | 1 | **That specific path executed correctly** | ⛔ that the system is fine. A green says nothing about the paths the check does not touch |
> | 2 | **That the check measured something REAL** — not an empty set | ⛔ that `n/a` equals `passed`. A green over 0 cases is not a green: the check must state how many cases it measured (ADR-028 already says this for `grade-block`) |
>
> **The case that forces requirement 2:** an empty scope returned zero dead files, zero broken
> links, zero duplication — every metric green, **none of them run**. The reader concluded the
> block was sound. Absence of evidence had been rendered as evidence.
>
> **How to apply it:** a check reports its subject count alongside its result. A verdict built on
> greens whose measured count is zero is 🔴, not 🟢 — and **"not measured" is never a pass**.
>
> <!-- "not measured" is written in words, never with the white-square glyph: generate-metrics
>      counts that glyph as a criterion hole, so illustrating it here would inflate the metric.
>      Fourth time this defect appeared on 2026-08-05 — a document that shows a marker corrupts
>      the metric that counts it. -->


### 2.6 · Necessity — does this check have to exist?
**Question (frame):** does everything that exists have to exist?
**Here:** which check has never failed and never will — and is therefore theater.

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## 🔴 A CHECK THAT MEETS ANY OF THESE THREE IS DELETED. Not kept "just in case".
>
> | # | The check… | Why it goes |
> |---|---|---|
> | 1 | **cannot fail — ever** | if no state of the world turns it red, it does not measure: it decorates. Verifiable: try to break it; if you cannot, it goes |
> | 2 | **is fully covered by another** | two checks that always go red together — one of them is noise |
> | 3 | **measures the FORM, not the effect** | it confirms a file exists or a line is written, not that the rule holds. That is the difference between citing and verifying |
>
> **Brian was asked whether a redundant check is harmless and answered no: it is deleted.**
> The reason is not tidiness — it is that **a check that cannot fail manufactures false confidence,
> and false confidence is worse than a known gap.** A gap you can see; a green that means nothing
> you cannot.
>
> ⚠️ **The honest consequence, stated because it cuts both ways:** deleting is irreversible and
> `bin/test-f0-f6` publishes `battery.checks` as a live number, so a deletion lowers a figure that
> reads like progress. **The count is not the metric — `failed: 0` is.** A battery of 200 checks
> where 40 cannot fail is weaker than one of 160 that all can.
>
> **How to apply it:** before defending a check, try to make it red. If you cannot construct the
> failure it claims to catch, that is the finding — and the finding is **delete**, not document.

---

## 3 · HARD RULES OF THIS DISCIPLINE

> ### ✅ BRIAN'S CRITERION · 2026-08-05 — never accepted as proof, no exceptions
>
> | # | ⛔ Never | The case |
> |---|---|---|
> | 1 | **A green from a check nobody has seen fail** | `rules/rule-checks-must-measure.md` raised to a hard rule. It cost a false check on 2026-08-05 |
> | 2 | **A number from memory or copied by hand** | measure it and cite the source (`docs/METRICS.md`). **A copied number is correct exactly once** |
> | 3 | **"It compiled" / "no errors" as proof that it works** | starting is not working. §5-BIS B: *the import passing is not enough — the real startup is* |
> | 4 | ⭐ **Closing something whose failure you would not notice** | if you cannot say **how you would find out it broke**, you have not verified it — you have assumed it |
> | 5 | **Affirmative verification** — already in force | confirm with a datum, never with *"seems fine"* |
>
> ⭐ **Rule 4 is the one that generalises the other four.** It converts every close into one
> question: *what would tell me this broke, and does it exist?* A system with no answer to that is
> not verified — it is unmonitored.

---

## 4 · WHAT MAKES BRIAN REJECT A VERIFICATION

> ### ✅ BRIAN'S CRITERION · 2026-08-05
>
> ## FOUR SIGNALS THAT IT WAS NOT REALLY TESTED — any ONE is enough
>
> | # | Signal | Why it disqualifies |
> |---|---|---|
> | 1 | ⭐ **It tells me it works without showing the datum** | it asserts a result instead of reporting a measurement. This is owner-3's master rule: *"it does not declare 'this is fine'. It REPORTS THE MEASUREMENT."* |
> | 2 | **It tested the piece, not the whole flow** | every piece passes its own test and the chain is still broken — *"los bugs trágicos viven ENTRE las piezas"* (2026-07-20), seen from the proof side |
> | 3 | **It says *"should work"* or *"more or less"*** | Método F §2.2: *"más o menos conectado" is the declared enemy*. When something ALMOST works → stop and investigate, never continue |
> | 4 | **The green came from a path nobody executed** | the check ran but never touched what it claims to measure: 0 cases, empty scope, a condition never entered. **Green by vacancy** |
>
> **These are not scored.** Any single one present means the verification did not happen — 🔴
> regardless of how many other checks are green.
>
> ⚠️ **Signal 4 is the hardest to see**, because it looks identical to a real pass from the outside.
> It is the reason condition 3 of §2.2 exists: **a check must be seen failing before its green is
> worth anything.**

---

## 5 · METHOD FOR FILLING THIS FILE

> 🔴 **The AI asks. Brian answers with real cases. The AI structures.**

**Suggested questions for the interview:**

1. What do you demand before believing something works?
2. What makes you distrust a green result?
3. Which datum counts as proof, and which one only looks like it?
4. When is a unit test enough, and when does only the real system count?
5. What has to be true before something touches production?
6. Which verification mistake have you caught most often — in me?
7. What would you rather see fail loudly than pass quietly?

---

## 6 · HOW THIS FILE GETS USED (already wired)

| Moment | What happens |
|---|---|
| Block opens | the block declares this file in §D `Required standards` |
| Before editing | the hook **injects it** into context |
| Block closes | owner-3 applies criterion 1 (functional) with it |
| Validation | `bin/check-blocks` verifies the block declared it when it applies |

> ✅ **§2-§4 are FILLED.** The §5-BIS battery and affirmative verification still operate on top —
> both apply, and the stricter wins (`rules/rule-inheritance.md`).

---

Related: `principles/owner-3-validation.md` (the owner this branches from) ·
`principles/expertise/val-integration.md` (its sibling) · `rules/ESTANDAR_Metodo_Fases_F.md` §5-BIS ·
`bin/grade-block` (layer 1) · `docs/PENDING-BRIAN.md`.
