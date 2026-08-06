# Audit · F0-F5 end to end

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Reproducible with:** `bin/test-f0-f6`
---

## Purpose

Brian asked to test every flow from F0 to F5 and analyse the behaviour. This is what the
measurement found — **including 5 bugs the phases themselves had not caught.**

The battery is a **script, not a session**: 59 affirmative checks, each stating the expected value
and comparing. A battery that cannot be re-run proves nothing about tomorrow.

---

## Result

```
passed: 60 · failed: 0
notes:  34 criterion holes still waiting on Brian
```

| Phase | Checks | What it proves |
|---|---|---|
| **F0** security | 11 | the gates are harness locks, not doctrine · no secret VALUES in approved commands · `secrets/` 700/600/gitignored |
| **F1** structure | 14 | 11 directories · document + ADR contracts hold · ADR numbering has no gaps |
| **F2** owners | 4 + 1 note | 4 owners + 3 expertise · owner-0 master rule present · §5-BIS in owner-3 |
| **F3** the block | 7 | contract clean · sufficiency BOTH directions · no stale · OUT separated from inherited |
| **F4** measure | 6 | ⭐ **deterministic across runs** · no-type refused · `n/a` is not a pass · empty scope is not PRODUCT |
| **F5** verify | 14 | 3 hooks executable · **9 GSD hooks untouched** · pre-commit blocks AND fails open · `/clear` lock refuses |
| **cross-phase** | 3 | every §D standard exists · every cited ADR exists · §F graph still matches reality |

---

## ⭐ 5 bugs found — 3 of them in the validators themselves

### 1 · The battery reported 1 criterion hole when 34 exist
It counted `⬜` in `PENDING-BRIAN.md`, which is the **index**. The holes live in the source files.
**A test that measures where the data is not is a false green** — the exact thing it exists to catch.
Fix: count the source files, and cross-check against a **declared** `holes-total:` field.

### 2 · The index total was invented from a year
The cross-check grepped "the first number in the file" and read `2026` as a count. Fix: the total
must be a declared field (`holes-total: 34`) or nothing at all. **A made-up number is worse than no
number.**

### 3 · Scope-overlap detector produced a FALSE POSITIVE
A fresh scaffold whose `IN` was still `⬜ PENDING` "overlapped" with every block — on the empty
string and on `## Checkpoints`. It compared raw lines, not paths.
**A false positive teaches you to ignore the validator, which is worse than the overlap it hunts.**

### 4 · `re.S` made §B swallow §D (caused by fixing #3)
With `re.S`, `.` matched newlines and the comment group ran from §B IN down into a later §D,
pulling standards paths into the scope set. Removing `re.S` then broke **multi-line** comments and
reported the demo block's OUT as empty — a red on the only real block. Fixed with a comment pattern
that may span lines but cannot cross a `## ` heading, verified against **both** blocks.

### 5 · An empty block scored 🟢 PRODUCT
An empty `docs` scope has zero broken links and zero orphans, so it graded green. **Absence of
evidence read as evidence.** Fix: a verdict with **zero files measured** is `⬜ NOTHING MEASURED`,
never a pass.

---

## Mutation testing — does it fail when something IS broken?

A battery that only ever passes proves nothing. Five deliberate breakages, five catches:

| Mutation | Caught |
|---|---|
| NavigoX `deny` rules deleted | ✅ |
| `sshpass -p '<REDACTADO>'` pasted into an approved command | ✅ |
| §D pointing at a file that does not exist | ✅ |
| `ADR-099` cited without existing | ✅ |
| hooks unregistered from `settings.json` | ✅ |

All five restored afterwards; verified with zero residue (secrets, deny counts, hooks, block files,
probe directories).

---

## E2E lifecycle flow

`new-block` without `--type` → **refuses and explains** · with `--type docs` → scaffold with
`BLOCK.md` + `docs/` + `cache/` · unfilled block → **fails sufficiency** and **the `/clear` lock
refuses** · real scope overlap → **pre-commit blocks** · all probe blocks removed, `check-blocks`
returns to `0 errors · 0 warnings`.

---

## 🔴 A bug I INTRODUCED while fixing the warnings — and how it was caught

Fixing the 32 bare-path warnings, I ran a bulk replacement that substituted filenames **as
substrings**. `Plan_Maestro_Entrenamiento.md` became `work/Ronda_Entrenamiento_Plan_Maestro.md` — a
pointer to a file that never existed — in **4 historical documents**. It also touched **24 files
outside the scope of v2**.

**How it was caught:** not by reading the diff. By adding a check that every Mente-internal cited
path must resolve, then running it. It reported 36.

**What was done:**
1. 22 historical files reverted with `git checkout` (all were tracked, so nothing was lost)
2. The 2 with genuine v2 work (`memory/PENDIENTES.md`, the architecture) repaired by hand
3. The 4 corrupted names restored to the real filename, measured on disk

⭐ **The lesson, now enforced by `bin/test-f0-f6`:** a bulk rewrite is not safe because the mapping
is right — it is safe when something verifies the result afterwards. **The check that catches this
class of bug is now permanent.**

### And a second-order lesson: the check itself was too blunt

Its first version flagged 36, of which **28 were not bugs**: `docs/INDEX.md` and `docs/STATES.md`
are files **F7 generates** · `Doc/X.md` is a prose example · `memory/PENDIENTES.md` names files the
pending work will CREATE. **A check that cannot tell "does not exist yet" from "points nowhere"
produces noise, and noise is how a validator gets ignored.** It now distinguishes four classes.

### Real findings among the 8 that remained

| Finding | Fix |
|---|---|
| The architecture claimed `Maestro/punteros.tsv` **"✅ exists"** — it lives at `Maestro/punteros.tsv` | path corrected. **A false claim inside a design document is the worst kind** |
| `docs/INDEX.md` / `docs/STATES.md` — Spanish names predating ADR-023 | → `docs/INDEX.md` / `docs/STATES.md` |
| `blocks/active/demo/docs/plan-piece-e-admin.md` | moved into the demo block in F3; path updated |
| `Doc/Entrenamiento_Manifiesto.md` — a planned deliverable **never produced** | ⭐ **marked as never produced** rather than repointed. Rewriting it would have been a lie |

---

## What is still open (registered, not hidden)

| | |
|---|---|
| 🟡 34 criterion holes | Brian's, in the source files — F4 does not depend on them |
| 🟡 32 bare-path warnings in 18 files | preexisting, go with the 208-file rename |
| 🟡 `plan-v2-rollout.md` at 413/400 | splits per phase when F5 closes, not by trimming lines |
| 🟡 `for3s/.git` is an empty shell | Brian's call whether to delete or init properly |
| 🔴 the demo has 0 test files | sub-block 8 of the demo block |

---

Related: `docs/f4-execution-log.md` · `docs/f5-execution-log.md` · `bin/test-f0-f6` ·
`memory/PENDIENTES.md`.
