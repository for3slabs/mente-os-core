# 📋 CONTRACT · HANDOFF MANIFEST — bounded delegation
**Status:** current · **Type:** contract · **Updated:** 2026-07-31 · **Owner:** brian
**Language:** US English · **Validated by:** `bin/verify-handoff`
**Schema:** `rules/schema-handoff-v1.yml` · **Template:** `rules/template-handoff.yml`
---

## 0 · WHY THIS EXISTS

> **The measured failure:** on 2026-07-20 a single session ran **421 Bash commands with zero
> subagents**. Everything happened in one context, which grew to 999K tokens and produced the
> 21-jul incident (*"no eres el mismo de siempre, no me sirves así"*).

Delegating is not the problem. **Delegating without bounds is.** A specialist spawned with no
declared scope reads whatever it wants, writes wherever it lands, and returns prose nobody can
verify. The cost lands back in the coordinator's context — exactly what delegation was meant
to avoid.

**A handoff manifest is a written contract between the coordinator and the specialist:**
what it may read · what it must do · where it may write · when it must stop.

> ## 🚫 No manifest, no delegation.
> A specialist without a declared write scope is an unbounded agent inside a bounded system.

---

## 1 · WHAT THE MANIFEST DECLARES

| Block | Required | What it settles |
|---|---|---|
| `mente_handoff` | 🔴 | schema version — a specialist **rejects** an unknown version instead of guessing |
| `handoff_id` | 🔴 | unique within the block · `YYYY-MM-DD-HHMM-<slug>` |
| `block` | 🔴 | which block this belongs to — must exist on disk |
| `block_path` | 🔴 | path to the block directory |
| `role` | 🟢 | descriptive only, for logs and readability |
| `load` | 🔴 | **the read scope.** `required` (always) + `optional` (specialist's call) |
| `task` | 🔴 | `objective` · `success_condition` · `stop_condition` |
| `binding_checks` | 🔴 | machine-testable predicates, run in order — first failure aborts |
| `write_back` | 🔴 | **the write scope.** Where the return artifact goes + which sections it must contain |
| `isolation` | 🟢 | inline reminders carried into the specialist's prompt |

**The two scopes are the point.** `load` bounds reading, `write_back` bounds writing. Everything
else exists to make those two verifiable.

---

## 2 · ⭐ WHAT IS DIFFERENT HERE (and why)

The reference implementation binds a handoff to a **chat thread** (`thread_id: discord:149115…`).
Mente OS binds it to a **BLOCK**.

| Reference | Mente OS v2 | Why |
|---|---|---|
| bound to a chat thread | **bound to a block `id`** | our unit of work is the block, not a conversation. A block survives the chat that created it |
| 7 state files per unit | **one `BLOCK.md`, sections A-K** | measured: `RETOMAR.md` (1 file) is what works here; the demo scattered across 5 files is what does not |
| `also_append` → `MEMORY.md` | **`also_append` → `§J Context`** | same idea, our container |
| specialist may not touch BRIEF/STATUS/DECISIONS | **may not touch §A-E or §G** | identity, scope, state and decisions belong to the coordinator |

**Inherited without change**, because it was right: the return artifact lives under
`handoffs/`, the write scope is an allowlist, and an unknown schema version is refused.

---

## 3 · THE WRITE SCOPE — the rule that matters most

A specialist writes to **exactly two places**, both declared:

1. **its return artifact** — `handoffs/<handoff_id>.md` inside the block. Always allowed.
2. **`also_append`** — bounded appends to coordinator-owned files. **v1 permits only `BLOCK.md`
   §J (Context)**, and every entry declares `max_lines`.

Everything else is denied by default. There is no "the task needed it" exception: if the scope
was wrong, the manifest was wrong — fix the manifest, re-run the handoff.

> 🔴 **§A-E and §G are never writable by a specialist.** Identity, scope, connections, standards,
> state and decisions are the coordinator's. A specialist that rewrites the state it was given is
> not delegated work — it is a second coordinator.

---

## 4 · THE RETURN ARTIFACT

`write_back.artifact_schema` lists the sections the return must contain, in order. v1 default:

| Section | What goes in it |
|---|---|
| `objective` | restated from the manifest — proves it read the right one |
| `work` | what it actually did |
| `findings` | what it found, with evidence |
| `open-questions` | what it could not resolve |
| `status` | `done` · `blocked` · `aborted-binding-mismatch` |

**`status` is the machine-readable outcome.** `aborted-binding-mismatch` means the specialist
found the disk did not match its manifest and stopped **before acting** — the good failure.

---

## 5 · BINDING CHECKS — manifest vs reality

Run **in order**; the first failure aborts and nothing is written.

| # | Check | Fails when |
|---|---|---|
| 1 | `block_path_exists` | the path does not resolve to a directory |
| 2 | `block_md_exists` | `BLOCK.md` is missing or unreadable |
| 3 | `block_id_matches` | `BLOCK.md`'s `id:` differs from the manifest's `block` |
| 4 | `load_required_paths_exist` | any `load.required` path does not resolve |

> ⚠️ **Why order matters:** checking the id before the file exists produces a confusing error
> instead of the real one. Each check assumes the previous passed.

**v1 dispatch:** `bin/verify-handoff` runs these four unconditionally, in this fixed order.
The `binding_checks` array in the manifest is **documentary in v1** — it reserves the wire format
for a v2 verifier that parses and dispatches. A manifest listing a check v1 does not know is not
an error; v1 simply does not run it.

---

## 6 · EXIT CODES — `bin/verify-handoff`

| Code | Meaning |
|---|---|
| **0** | well-formed **and** all binding checks passed → safe to spawn the specialist |
| **1** | usage error or the manifest file is missing |
| **2** | 🔴 **malformed** — the manifest itself is wrong (missing block, bad write scope) |
| **3** | 🔴 **binding failed** — the manifest is fine but reality does not match |

**2 and 3 are different on purpose.** A 2 means *fix the manifest*. A 3 means *the manifest
describes a world that does not exist* — usually a block that moved or was renamed.

---

## 7 · ⭐ THE GATE — this is enforced, not suggested

`hooks/gate-handoff.py` runs on `PreToolUse(Agent|Task)`. **The level was measured, not chosen**
(2026-07-31, across every `.jsonl` in the project):

| Tool | Calls |
|---|---|
| Bash | **9,786** |
| Edit | 3,289 |
| Read | 1,851 |
| **Agent** | **32** — 15 of them read-only |

**That measurement inverted the diagnosis.** The 20-jul failure was not *delegating badly* — it
was **not delegating at all**. There is no history of specialists writing where they should not;
there is a history of everything happening in one context until it hit 999K.

So the gate follows the law of `hooks/gate-critical.py`: *a gate that obstructs more than it protects
degrades to a warning.*

| The specialist can… | Level | Why |
|---|---|---|
| **WRITE** (`general-purpose`, custom agents, **unknown types**) | 🔴 **BLOCK** | an unbounded writer inside a bounded system is the real risk |
| **only READ** (`Explore`, `Plan`) | ⚠️ **WARN** | it cannot corrupt anything — and this is the cheap delegation that was *missing* |

> 🔴 **Unknown agent types fail CLOSED.** An agent whose tools are not known could be anything,
> so it is treated as a writer. Failing open here would make the gate decorative.

### Presence is not compliance

A manifest sitting on disk opens nothing. The gate runs `bin/verify-handoff` on it and requires
**exit 0**. A malformed or unfilled manifest leaves the gate shut — otherwise the scope would be
paperwork rather than a boundary.

### The escape hatch

```bash
MENTE_HANDOFF_BYPASS=1
```

Documented on purpose (`rules/rule-friction.md`: *a gate with no escape hatch gets deleted*).
It is deliberate and **loud** — it prints that nothing records what the specialist may read,
where it may write, or when it must stop.

---

## 8 · WHEN A HANDOFF IS WORTH IT

> ⛔ **Not every task deserves a manifest.** Writing one costs more than a small task saves.

| Delegate | Do it inline |
|---|---|
| broad search across many files where only the conclusion matters | anything you can answer with two reads |
| a bounded sub-task whose intermediate output would flood the context | work that needs the coordinator's full context to judge |
| repeated mechanical work over a known file set | one-off edits |

**The measured signal:** if the work would produce dozens of tool calls whose *output* you do not
need — only the conclusion — that is a handoff. The 20-jul session is the counter-example: 421
Bash commands whose full output stayed in context forever.

---

Related: `rules/schema-handoff-v1.yml` (the schema) · `rules/template-handoff.yml` (fill this) ·
`bin/verify-handoff` (the validator) · `rules/contract-block.md` (§J is the only appendable target) ·
`docs/analysis-internos-v1.md` §4.10 (where this gap was first recorded).
