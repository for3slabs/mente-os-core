# 🗺️ PLAN · V2-6 — lo que quedó abierto de F0
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-6
**Orden:** 4 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`)
---

## Purpose

F0 cerró 4/4 tickets pero dejó **4 cosas sin hacer** que nunca se convirtieron en pendientes
propios: deuda **invisible**, que es la peor clase.

---

## 1 · EL ESTADO REAL — los 4, verificados contra el disco 2026-08-08

⭐ **Dos de los cuatro YA ESTÁN HECHOS.** El pendiente decía *"4 cosas"* y llevaba así desde el
27-jul; medirlos es lo que lo destapó.

| # | Qué faltaba | Estado hoy |
|---|---|---|
| **1** | **§6 de `principles/owner-0-voice.md` — "Brian's additions"**, en blanco a propósito | 🔴 **ABIERTO** — 🙋 solo lo puede llenar Brian (ADR-003) |
| **2** | **Verificar la voz en una sesión nueva** (los output styles cargan al arrancar) | 🟡 **ABIERTO** — trivial, pero nadie lo firmó |
| **3** | **26 decisiones DUPLICADAS** en Arquitectura §17.1 y Visión §6 | ✅ **RESUELTO** — `docs/DECISIONS.md` es fuente única declarada (29 filas) y §17.1 dice explícitamente *"esta tabla es un RESUMEN de lectura, no la fuente"* |
| **4** | **No existe estándar para decisiones nuevas** | ✅ **RESUELTO** — **30 ADRs** en `rules/decisions/` + `rules/contract-adr.md` |

📊 **Alcance real: 2 abiertos, no 4.** Y uno de los dos es criterio de Brian, no trabajo.

---

## 2 · EL TRABAJO — 2 pasos

### Paso 1 · 🙋 §6 de la voz — SOLO BRIAN

Las 8 reglas actuales salen de **observación con evidencia**. §6 es para criterio que **no se
observó**: cuánto detalle técnico prefiere · cuándo quiere que se le cuestione vs. ejecución
directa · términos que le molestan · cuánto contexto asumir.

⛔ **La IA no puede escribirlo sin inventarlo** (ADR-003). Se pregunta, o se queda vacío **declarado
como vacío** — nunca relleno con lo que parezca razonable.

### Paso 2 · Verificar la voz en frío

Los output styles cargan **al arrancar la sesión**, no en caliente. Comprobar tras un `/clear` que la
voz aplica: modo correcto (🟢🟡🔵), bloque 📦 ENTREGA presente, ninguna frase prohibida.

⚠️ **No se puede autoverificar dentro de la misma sesión** — de ahí que lleve abierto desde julio.

---

## 3 · CÓMO SE VERÍA FALLAR

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Vaciar `docs/DECISIONS.md` | los ADRs siguen siendo la fuente: `check-blocks --adrs` debe seguir en 0 errores |
| 2 | Añadir una decisión SOLO a la tabla de Arquitectura §17.1 | ⚠️ hoy **nada lo detecta** — la sincronía murió pero el candado no existe |
| 3 | Borrar un ADR citado por otro | `check-blocks` debe cazar la simetría rota |

🔴 **El #2 es un hueco vivo:** el problema se declaró resuelto porque §17.1 dice *"soy un resumen"*,
pero **ningún check impide** que alguien escriba ahí una decisión que no esté en `docs/DECISIONS.md`.

---

## 4 · QUÉ CHECK LO VIGILA DESPUÉS

**Toda fila de una tabla-resumen de decisiones existe en `docs/DECISIONS.md`.** Es lo que convierte
*"esta tabla es solo un resumen"* de promesa a hecho.

📊 La evidencia de que hace falta: la duplicación anterior llegó a **75 filas contra 37** antes de
que alguien lo notara.

---

## 5 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No inventa el §6 de la voz.** Vacío declarado > relleno inventado.
- ⛔ **No borra §17.1 de la arquitectura.** Ese borrado estaba planeado *"para F7"* y F7 cerró sin
  hacerlo: es **otro pendiente**, y tocar la arquitectura cruza con V2-1.

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` · `principles/owner-0-voice.md` §6 (el hueco de Brian) ·
`docs/DECISIONS.md` · `rules/contract-adr.md`.
