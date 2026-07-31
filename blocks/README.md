# BLOCKS

**Status:** current · **Type:** entry-point · **Updated:** 2026-07-29 · **Owner:** brian

## Purpose

Where work lives. One directory per block; one `BLOCK.md` per directory.

```
blocks/
├── active/     work in progress — several may exist, ONE executes at a time
├── blocked/    waiting on something that §E names an owner for
└── archive/    closed — consultable experience, never deleted
```

**Contracts:** `rules/contract-block.md` (the fields) · `rules/block-lifecycle.md` (the transitions)
**Create one:** `bin/new-block <name>` · **Validate:** `bin/check-blocks --blocks`

---

Related: `rules/contract-block.md` · `rules/block-lifecycle.md` · `base-rules.md`.
