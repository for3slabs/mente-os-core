# CONNECTIONS · blk-expertise-programacion-2026-08
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian

## Purpose

Qué queda afectado por este bloque, y qué no lo está a propósito.

---

## Afectado

| Qué | Cómo |
|---|---|
| 🆕 `rules/rule-shipping-flow.md` | **nació aquí**, y es **transversal**: la declara en su §D un bloque de cualquier disciplina |
| `principles/expertise/dev-backend.md` · `dev-database.md` · `dev-frontend.md` | cada uno ganó una sección `§4-BIS` de material importado, **separada del criterio de Brian** |
| `bin/grade-block` | 3 defectos corregidos (§G-6) |
| `blk-demo` §D | declara el flujo de PR desde entonces — **verificado ejecutando el hook** |

## NO afectado, y es deliberado

- **Los huecos de criterio** — este bloque importó material externo y **nunca escribió dentro del
  §2-§4 de un archivo de expertise**. Confundir ambos blanquearía opinión de terceros como
  criterio del dueño (ADR-003).
- **`blk-demo`** — otro repo, ninguna pieza compartida en los §B.

## Lo que queda abierto para otros

1. `grade-block` **no tiene self-test** — sus 3 defectos se hallaron por accidente. *(Cerrado
   después, en la misma sesión: 5 casos en `bin/test-f0-f6` §SELF-TEST.)*
2. **No existe la hoja de referencia del workspace** — la capa 2 de las 6 del setup. *(Cerrado
   después: `docs/WORKSPACE.md`.)*
3. Un bloque **archivado** no podía recalificarse. *(Cerrado después: `grade-block` acepta el
   sufijo `_YYYY-MM`.)*

---

Related: `blocks/archive/expertise-programacion_2026-08/SUMMARY.md` · `rules/rule-shipping-flow.md` ·
`principles/expertise/dev-backend.md` §4-BIS · `memory/PENDIENTES.md`.
