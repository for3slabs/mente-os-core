# SUMMARY · blk-expertise-programacion-2026-08
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian

## Purpose

Qué se hizo y qué se aprendió al absorber dos skills externas dentro de Mente OS v2.
El veredicto medido vive en el §K del bloque; la evidencia por dimensión, en `docs/`.

---

## Qué se hizo

Se leyeron **completas** dos skills externas (12 archivos, 3,157 líneas, ambas MIT) y se absorbió
lo que aplica:

| De dónde | Qué entró | Dónde |
|---|---|---|
| `cracked-dev` (metodología) | bucle de ejecución · 8 anti-patrones de git · checklist de PR · orquestación (máx 2 agentes) · qué hace ejecutable un spec · las 6 capas de setup | 🆕 `rules/rule-shipping-flow.md` |
| `convex-skill` (framework) | 6 patrones de fallo de consulta/acceso · 8 de backend · 3 de frontend | §4-BIS de los 3 `dev-*` |

**Veredicto al cerrar: 🟢 PRODUCTO** — capa 1 3/3 aplicables + capa 2 6/6.

## What was learned

> ⭐ **El eje para ubicar una regla no es DE QUÉ TRATA — es a quién hay que INYECTÁRSELA.**

La IA ubicó el flujo de PR dentro de `dev-backend.md` aplicando *"un tema, una casa"*. **Brian lo
corrigió:** *"va a haber PR de frontend, de base de datos"*. Y era **medible**:
`hooks/pre-edit-standards.py` inyecta **solo lo que el bloque declara en su §D**, así que un flujo
viviendo en backend **nunca habría llegado** a un bloque de frontend. Una regla que alcanza a una
sola disciplina no es una casa: es un punto ciego para las otras dos.

> 🔴 **Un validador que nadie valida reporta veredictos que nunca midió.**

Calificar este bloque destapó **3 defectos en `bin/grade-block`**: un comentario en el §B mataba el
scope **en silencio** (⬜ falso con todas las métricas en verde) · dos validadores resolvían rutas
desde raíces distintas · la línea de la capa 2 estaba escrita a mano como *"pending Brian"* y
empezó a mentir el día que se llenó. Los tres arreglados; los tres hallados **por accidente**.

## Lo que se RECHAZÓ, escrito en vez de omitido

⛔ **`--dangerously-skip-permissions`.** `cracked-dev` lo recomienda para spawns autónomos. Es el
inverso exacto de las 212 reglas `deny` y las 3 puertas de este proyecto, y `PROJECT-RULES.md` §3
prohíbe proponer levantar un `deny` por comodidad. **Registrado para que un lector futuro sepa que
se evaluó y se rechazó, no que se pasó por alto.**

---

Related: `blocks/archive/expertise-programacion_2026-08/BLOCK.md` · `blocks/archive/expertise-programacion_2026-08/connections.md` ·
`blocks/archive/expertise-programacion_2026-08/docs/closing-report.md` · `rules/rule-shipping-flow.md` (lo que nació aquí).
