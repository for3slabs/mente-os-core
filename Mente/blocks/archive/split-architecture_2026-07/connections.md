# CONNECTIONS · split-architecture (closed 2026-07-30)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Contract:** `rules/contract-archive.md` §2

## Purpose

What this block leaves affected for whoever opens the next one.

## Pieces this block owned — now free
- `docs/Arquitectura_Mente_OS_v2_Bloques.md` — now the entry point (632 lines)
- `Cuerpo/architecture/` — 5 new pieces, all declared in `Maestro/piezas.tsv`
- `Maestro/piezas.tsv` — 5 lines added

## Blocks that depended on it
- `blk-demo-2026-07` — its §D standards point at rules described in this document.
  **Dependency satisfied:** the entry point keeps its filename, so every citation still resolves.

## Rules this block created
- None new. It APPLIED `rules/contract-document.md` (size limits), `rules/rule-fix-not-patch.md`
  (pointer in place, not deletion) and ADR-027 (the limit is the signal).

## What is still open
- Nothing from this block. All 6 sub-blocks closed.
- ⚠️ Two size warnings survive OUTSIDE this scope, registered in `memory/PENDIENTES.md`:
  `rules/contract-block.md` 336/250 · `rules/NAMING_CONVENTION.md` 266/250.

---

Related: `blocks/archive/split-architecture_2026-07/SUMMARY.md` · `rules/contract-archive.md`.
