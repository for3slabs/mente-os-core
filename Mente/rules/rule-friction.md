# RULE · FRICTION
**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-3 · **Source:** architecture §8 · ADR-005 · ADR-022
---

## Purpose

What to do when a rule gets in the way mid-work — and how the system detects a rule that is simply
wrong.

---

## 1 · THE PROTOCOL

```
1 · COMPLY               — even if it seems wrong
2 · LOG THE FRICTION     — in the block, §H
3 · CONTINUE             — the work never stops
4 · AT CLOSE             — frictions surface together as improvement proposals
5 · BRIAN DECIDES        — if approved, the rule changes with date, reason and author
```

### ⚠️ The one exception — stop immediately

If complying causes **real damage**: breaking production · exposing a secret · losing data.
**Then stop and ask.**

---

## 2 · WHY THIS SHAPE

| Alternative | Why it was rejected |
|---|---|
| Ask every time something chafes | Brian becomes a **bottleneck**; the system gets slow |
| Let the AI skip the rule it judges wrong | in a month **the rules are the AI's again** — that is vibecoding |

**Logging and accumulating makes the system learn without constant supervision.**

---

## 3 · THE LOG FORMAT — four fixed fields

```markdown
YYYY-MM-DD · rule: <name> · block: <id> · reason: <why it got in the way>
```

Lives in `BLOCK.md` §H. `bin/check-blocks` counts them.

---

## 4 · ⭐ DETECTION — arithmetic, not interpretation

```
rule "server-first": 3 frictions · blk-demo · blk-panel · blk-trace
🔔 RULE REVIEW — 3 distinct blocks
```

### The two details that make it work

**① DISTINCT BLOCKS, not repetitions.**
3 frictions in the **same** block = one task chafing.
3 frictions in **distinct** blocks = **the rule is wrong.**
> Without this distinction any long task would raise false alarms — and then the mechanism gets ignored.

**② IT NEVER EXPIRES.**
If the 3 frictions accumulate over six months, it is still a signal.
> **The problem is not the speed of the friction: it is its recurrence.**

---

## 5 · WHAT HAPPENS WHEN IT FIRES

⛔ **The rule is NOT changed automatically.** It escalates to Brian with the 3 frictions and their
reasons. He decides: **adjust** · **keep with a documented exception** · **remove**.

> Consistent with the master principle: *"no existen reglas inmutables, existen apuntadores a reglas —
> estándares mejorando con criterios del usuario."* **The system detects; Brian decides.**

---

## 6 · EXAMPLES

**Normal friction — logged, work continues:**
```markdown
2026-07-27 · rule: server-first · block: blk-demo
  reason: wanted to push an already-verified urgent fix; the rule requires an explicit order
  action: COMPLIED, left the commit unpushed, continued
```

**The exception — stopped immediately:**
```markdown
2026-07-26 · rule: zero-hardcoding · block: blk-demo
  reason: wanted to read DEMO_ENC_KEY from a constant to test quickly
  ⚠️ STOPPED AND ASKED — the fallback was hiding local ≠ Vercel.
     Continuing would have left the demo broken in production, silently.
```

---

Related: `contract-block.md` §H · `bin/check-blocks` · ADR-005 · ADR-022 · architecture §8.
