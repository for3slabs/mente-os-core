# F4 · execution log

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Phase:** F4 (measure) · **Plan:** `plan-v2-rollout.md`
---

## Purpose

What F4 actually measured and what it caught. The plan says what F4 *is*; this says what *happened*
when it ran. Split out on 2026-07-30 when the plan crossed its 400-line limit — two distinct things
in one file (ADR-027).

---

## 🔍 AUDITORÍA F0-F2 (2026-07-29) — 3 graves cazados y cerrados

Antes de avanzar a F3 se auditó lo construido. **Los 3 graves tenían la misma causa: capacidad que
v1 YA TENÍA y el v2 no heredó.** Se diseñó mirando lo que faltaba, sin usar §15 *"lo que no se toca"*
como checklist.

| # | Hueco | Cierre |
|---|---|---|
| ① | **La batería §5-BIS desapareció** — owner-3 tenía 3 criterios pero no los 7 checks A-G | ✅ `principles/owner-3-validation.md` §3-BIS, **copiada del Método F, no reinventada** + verificación afirmativa |
| ② | **La regla `/clear` no estaba en el v2** — la que se incumplió 5 de 11 veces | ✅ `rules/rule-session-close.md` + no-negociable **#8** de `base-rules.md` |
| ③ | **Nada decía CÓMO se crea un bloque** — el contrato dice qué campos, no quién los llena | ✅ `rules/block-lifecycle.md` — 6 pasos + quién hace qué |
| +⑦ | `rules/case-dangerous-default.md` no existía (4 archivos lo referenciaban) | ✅ migrado a `rules/` |

**⭐ `rules/block-lifecycle.md` cerró además 3 huecos medianos:** nuevo bloque vs existente (§2) ·
el estado `blocked` con dueño del bloqueo (§5) · conflicto entre bloques (§7).

> ⭐ **El hallazgo de método:** *diseñar mirando lo que falta pierde lo que ya funcionaba.*
> La sección §15 de la arquitectura existe para eso y no se usó. **Añadido al procedimiento: toda
> fase revisa §15 antes de cerrar.**

> ✅ **F2 CERRADO 2026-07-29 — 14 archivos, todos en inglés, todos bajo su límite (≤250).**
> Cada uno lleva el header del contrato (`Status`/`Type`/`Updated`/`Owner`) y **referencias a ADRs
> verificadas**. `principles/owner-2-dev.md` aplica solo sus 7 reglas duras mientras el criterio de Brian
> (`expertise/*`) siga vacío — **no inventa criterio** (ADR-003).

> 🇺🇸 **Todos los archivos de F2 nacen en inglés de EE.UU.** (decisión 23) y con la convención de
> nombres (`rules/NAMING_CONVENTION.md`). Son instrucciones: los lee la IA.

**Cierra cuando:** existe la plantilla vacía de un bloque y las reglas que la gobiernan.

---


---

## F4-6 · from one lane to the whole SYSTEM

> *"¿solo está para demo o para todo el sistema? porque lo vamos a ocupar en todo el sistema."*

**El hallazgo:** `grade-block` no tenía hardcodeo (medido: 0 referencias a `demo`/`marca-personal`),
pero **todas sus métricas eran de código.** Contra la lista real de pendientes, 3 de 7 bloques
habrían dado 🔴 MVP para siempre — renombrar 208 archivos, partir la arquitectura, decidir el
hosting. **Un validador que nunca puede pasar a verde es un validador que se aprende a ignorar**, y
ahí la doctrina vuelve a ser un documento.

**La solución (ADR-028):** el bloque declara `type: code | docs | infra | data` en §A, y el tipo
decide la regla de medir. Lo que no aplica imprime `n/a` **con su razón** — y `n/a` nunca es 🟢.

| Tipo | Se mide |
|---|---|
| `code` | archivos muertos · exports muertos · duplicación · tests · ciclos · §F desactualizado |
| `docs` | enlaces roots · docs huérfanos |
| `infra` | runbook documentado · rollback documentado |
| `data` | migraciones sin rollback |
| **todos** | ⭐ **secretos escritos en vez de referenciados** |

**Probado en los 4 tipos + 2 casos negativos (2026-07-30):**

| Prueba | Resultado |
|---|---|
| `code` sobre la demo | 🔴 MVP — **mismos números que antes**, sin regresión |
| `docs` sobre los 28 ADRs | 🟡 CLOSE — cazó 1 huérfano **real** (el propio ADR-028) |
| `infra` sin runbook | 🔴 MVP — con `n/a` explicado en tests/imports |
| `data` con 2 migraciones | 🔴 MVP — detectó **1 sin rollback** |
| bloque sin `type` | 🔴 rechaza y explica, **no adivina** (exit 1) |
| secreto pegado en un `.md` | 🔴 lo encontró y nombró el archivo |

**Cableado en los 3 consumidores:** `rules/contract-block.md` §A · `bin/new-block --type` (deriva del
`--piece`, pide cuando no puede) · `bin/check-blocks` (falta `type` = 🔴).

---

Related: `rules/contract-block.md` §A · `decisions/ADR-028-block-type-decides-metrics.md` ·
`bin/grade-block`.
