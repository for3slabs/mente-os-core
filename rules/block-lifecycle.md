# BLOCK LIFECYCLE · how a block is opened, worked and closed
**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** grave #3 of the F0-F2 audit · **Complements:** `contract-block.md`
---

## Purpose

`contract-block.md` says **WHAT fields a block has.** This file says **WHO fills them, WHEN, and with
what command.** Found missing in the F0-F2 audit — without it, the first block gets created by
improvisation, which is exactly what v2 exists to prevent.

---

## 1 · OPENING A BLOCK — 6 steps

```
1 · DECIDE: new block or existing one?        → §2
2 · CHOOSE the id                             → blk-<name>-<YYYY-MM>
3 · CREATE the scaffold                       → bin/new-block <name>   (or by hand, §4)
4 · FILL the hard minimum: §A §B §C §D        → ~2 minutes
5 · COMPUTE the lane from §C                  → rule-lanes.md
6 · VALIDATE                                  → bin/check-blocks <id>
```

**Who does what:**

| Step | Who |
|---|---|
| 1 · decide new vs existing | **the AI proposes, Brian confirms** if it is a new block |
| 2 · id | the AI |
| 3 · scaffold | the AI (or `bin/new-block`) |
| 4 · §A §C | the AI, from real data |
| 4 · **§B `Scope` OUT** | ⭐ **Brian confirms** — the boundary is his call |
| 4 · §D `Required standards` | the AI proposes, Brian may add |
| 5 · lane | 🤖 **the propagation graph decides**, not judgment |
| 6 · validate | 🤖 script |

> ⭐ **Step 4 §B is the only one that MAY need Brian at open time** — but only when the boundary
> **cannot be derived**. If every limit already follows from an existing rule (a `deny`, a
> non-negotiable, another block's scope), the AI fills it **and cites the source on each line**.
>
> ⛔ **Never leave a `⬜ BRIAN` hole out of habit.** A hole the AI could have filled from the repo is
> not a request for criterion — it is unfinished work handed over as if it were a decision.
>
> **And if criterion IS genuinely needed: ask it directly, with the options.** Writing `⬜ BRIAN`
> inside a file and mentioning it at the end of a long message is leaving a note, not asking a
> question.
>
> *(Learned on the first real block, 2026-07-29: all four OUT limits were derivable — every one of
> them followed from a `deny`, from `block-lifecycle.md` §2, or from `base-rules.md` #7.)*

---

## 2 · NEW BLOCK OR EXISTING ONE?

```
Does the work share the SAME RELATION as an open block?
        │
   YES ─┴─▶ SUB-BLOCK of that block          (§F row)
        │
    NO ─┴─▶ Does it touch pieces the open block declares in its Scope IN?
              YES ─▶ 🔴 CONFLICT → resolve before opening (§5)
               NO ─▶ NEW BLOCK
```

**The test:** *would both pieces of work close on the same day, for the same reason?*
If yes → same block. If no → separate blocks.

**Examples:**

| Work | Decision |
|---|---|
| "tests for the demo's critical paths" | **sub-block** of `blk-demo` — same relation |
| "connect a payment provider" | **new block** — different relation, even if it touches the demo |
| "rename the 208 files" | **new block** — touches everything, belongs to nothing |

---

## 3 · WORKING THE BLOCK

| Moment | What happens |
|---|---|
| **Every session start** | load Tier 1 (§A-E). If §A-E do not suffice → **say so out loud, do not infer** |
| **Before editing a piece** | the hook injects the §D standards (or read them manually) |
| **On every decision** | write it in §G **with its rationale** — *if it is not written, it is not made* |
| **On every rule that chafes** | log it in §H, comply, continue (`rule-friction.md`) |
| **On every iteration** | leave a checkpoint in §I |
| **Only ONE block executes at a time** | others stay `active` but idle |

---

## 4 · CREATING THE SCAFFOLD

**With the script** (built 2026-07-29):

```bash
bin/new-block <name>                                  # scaffold only
bin/new-block <name> --piece lib/demo/userStore.ts \
              --root /path/to/repo                    # + MEASURE the graph
```

It pre-fills what can be **derived** (id, lane from the measured graph, standards) and leaves
**§B Scope OUT** as a marked hole — the boundary is Brian's decision, not a derivation.

**By hand**, if the script is unavailable:

```
blocks/active/<name>/
├── BLOCK.md      ← from the template in contract-block.md §2
├── docs/         ← empty
└── cache/        ← empty
```

**`BLOCK.md` is copied from `contract-block.md` §2** — never written from memory.

---

## 5 · THE `blocked` STATE

| Question | Answer |
|---|---|
| **Who blocks it?** | whoever finds the blocker — AI or Brian |
| **What is required?** | §E `blockers:` states **what** blocks it and **who** can unblock it |
| **Who unblocks?** | whoever the field names. If it is Brian, it waits |
| **Does it expire?** | `bin/flag-stale` flags it after **14 days** blocked |
| **Can a blocked block hold up its parent?** | ✅ yes — the parent does not close with open sub-blocks |

```markdown
## State
status: blocked
blockers: sub-block 5 depends on deciding the hosting → BRIAN
```

> ⭐ **A blocker with no owner is not a blocker: it is an abandoned block.** The field must name who
> can lift it.

---

## 6 · CLOSING

The 8 steps live in `principles/owner-3-validation.md` §4. Summary:

```
consolidate → curate decisions → resolve frictions → VERIFY SUFFICIENCY
→ summary → declare connections → archive → regenerate indexes
```

**A block does not close if:** sufficiency fails · a sub-block is open · §K is missing.
**A block DOES close with a 🔴 quality verdict** — but marked **MVP with its debt listed.**

---

## 7 · CONFLICT BETWEEN BLOCKS

**Two blocks declaring the same piece in `Scope IN` is a conflict**, not a coincidence.

| Resolution | When |
|---|---|
| **Merge into one block** | the relation is actually the same |
| **Declare a dependency** in §C | one needs the other's output |
| **Split the piece** | each block owns a different part |

⛔ **What is never done:** let both touch it. That is how `userStore.ts` reached 21 edits.

`bin/check-blocks` flags overlapping `Scope IN` declarations.

---

Related: `contract-block.md` (the fields) · `rule-lanes.md` (the lane) · `rule-friction.md` ·
`principles/owner-3-validation.md` §4 (closing) · `bin/new-block` · `bin/check-blocks`.
