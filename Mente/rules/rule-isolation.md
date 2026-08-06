# RULE · ISOLATION
**Status:** current · **Type:** rule · **Updated:** 2026-07-29 · **Owner:** brian
**Ticket:** F2-3 · **Source:** architecture §11.6
---

## Purpose

Blocks do not read each other by default. This is the Puentes gate, applied **inside** the system.

---

## 1 · THE RULE

| ⛔ Forbidden by default | ✅ Allowed |
|---|---|
| Reading another block's files | a connection **declared** in §C |
| Broad scanning of `blocks/active/` | an **explicit request** from Brian |
| Inferring from similar names | resolution by **exact id** |
| Cross-block synthesis | explicit request only |

---

## 2 · WHY IT EXISTS

The Puentes gate has **100% measured compliance** — it protects one thing and therefore gets
honored. Without this rule, *"reading the other blocks for context"* reproduces **inside** the system
the consumption problem the gate already solved **outside** it.

> The precedent that justifies it: session S1 ran 47 days, reached ~985K of live context, and one
> `"hola"` cost 970K tokens and burned the day's quota.

---

## 3 · RESOLUTION IS EXACT

```
1 · Look up the block by EXACT id
2 · Match? ── YES ─▶ load Tier 1 (§A-E)
        │
        └── NO ──▶ ⛔ STOP AND ASK
```

**Forbidden:** fuzzy match · inferring from similar names · picking the most recent block *"because
it is probably that one"*.

> ⭐ **Why this is the most important part:** an AI that infers **sounds exactly as confident** as one
> that knows. That is the mechanism behind *"no, así no iba"*. Stopping turns a silent loss into a
> visible question.

---

## 4 · HOW A LEGITIMATE CROSS HAPPENS

**Via §C of the block** — the connection is declared, so reading it is not a violation:

```markdown
## Connections
- DEPENDS ON: blk-canal-api (consumes /v1/chat)
```

**Or Brian asks for it explicitly.** Nothing else.

---

## 5 · WHAT `bin/check-health` FLAGS

```
🟡 ISOLATION
   · a block reading files from another block with no declared connection
   · a §C connection pointing at a block that does not exist
```

---

Related: `contract-block.md` §C · `bridges/Puentes_Mente_OS.md` (the outer gate) ·
architecture §11.5 · §11.6.
