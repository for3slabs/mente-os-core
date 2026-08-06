# ADR-016 · Folders coexist during migration

date: 2026-07-27
status: superseded
decided-by: brian
supersedes: —
superseded-by: ADR-029-full-v1-to-v2-migration.md

## Context

Taken during the v2 design session (2026-07-27). Full reasoning lives in
`docs/Arquitectura_Mente_OS_v2_Bloques.md`; this record exists so the decision has its own
traceable, revertible file (see `rules/contract-adr.md`).

## Decision

The new folder structure COEXISTS with the old one. Zero broken pointers.

## Rationale

218 unique paths cite the current folders across documents; a rename without coexistence breaks them silently. Rejected alternative: rename and fix afterwards.

## Evidence

A broken markdown link throws no error — it surfaces weeks later.

## Reverting

Force a hard cutover; expect silent breakage.

---

> ⭐ **Cómo terminó esta decisión (2026-08-02).** No se revirtió: **se cumplió.** La coexistencia
> hizo exactamente su trabajo — `bin/check-links` mide hoy **0 citas rotas**, que era su objetivo
> declarado ("zero broken pointers"), sobre las 218 rutas en riesgo.
>
> ADR-029 la supersede por la misma razón que superseda a ADR-008: ambas gobernaban **CÓMO
> migrar**, y ADR-029 cambió esa política a "migrar todo, en orden de riesgo". Al completarse la
> migración (0 carpetas v1 en disco) la coexistencia dejó de tener a qué aplicarse.
>
> ⚠️ **`superseded` es lo más cercano que ofrece el vocabulario** (`contract-adr.md` §76:
> `proposed · accepted · superseded · reverted`). No existe un estado para *"cumplida y agotada"*,
> y no se inventó uno: un vocabulario cerrado es una decisión de Brian, no un descubrimiento de
> la IA (`rule-config-hygiene.md` §1.5). Esta nota cubre el hueco hasta que se decida si hace
> falta `fulfilled`.
