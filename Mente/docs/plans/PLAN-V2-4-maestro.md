# 🗺️ PLAN · V2-4 — reestructurar el Mente OS Maestro
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-4
**Orden:** 5 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`) — el más arriesgado, va tras estabilizar
---

## Purpose

Reestructurar el controlador que apunta a los Mente OS de todos los proyectos. ⚠️ **Es el único
pendiente del bloque que toca algo EN PRODUCCIÓN**: Foresito (el agente maestro) lo lee **en vivo**.

---

## 1 · EL ESTADO REAL — medido 2026-08-08

| Qué | Medido |
|---|---|
| Naturaleza | **sub-repo con su propio `.git`** — no viaja en el repo de Mente OS |
| Quién lo consume | 👑 **Foresito lo lee EN VIVO** como agente maestro |
| Lo que funciona | permisos fail-closed · el controlador **apunta**, no replica |
| 🔴 **Archivos sin commitear** | **7** (`Maestro/REGLAS_MAESTRO.md` · `Maestro/indexador.py` · `Maestro/punteros.tsv` · `Maestro/registro.md` · `Maestro/relaciones.md` · `Maestro/ALTERNATIVAS_QUE_CONECTAR.md` · `piezas.tsv` sin trackear) |

🔴 **El hallazgo que destapó escribir este plan:** hay **7 archivos modificados sin commitear** en un
repo que un agente en producción lee. ⭐ **Los archivos sobreviven; la RAZÓN del cambio no.** Si algo
se rompe, no hay diff que explique qué cambió ni por qué.

---

## 2 · EL ORDEN CORRECTO — y por qué no es el obvio

⛔ **Lo primero NO es reestructurar: es COMMITEAR lo que ya cambió.** Reestructurar encima de 7
archivos sin versionar mezcla lo nuevo con lo viejo y **hace irreversible el rollback**.

| # | Paso | Por qué antes que el siguiente |
|---|---|---|
| **1** | Commitear los 7 (o descartarlos, con razón escrita) | sin línea base, no hay a dónde volver |
| **2** | Medir qué lee Foresito exactamente | tocar lo que un agente vivo consume sin saber qué consume es adivinar |
| **3** | 🙋 **Brian decide el alcance** de la reestructuración | es criterio, no derivación |
| **4** | Ejecutar, con el agente **apagado o avisado** | el riesgo se acepta con los ojos abiertos, o no se acepta |

---

## 3 · CÓMO SE VERÍA FALLAR

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Romper `Maestro/punteros.tsv` (la fuente de ramas) | el indexador debe **fallar ruidosamente**, nunca devolver una lista vacía en silencio |
| 2 | Apuntar a un repo que no existe | debe decir *cuál* falta, no *"error"* |
| 3 | Dejar los 7 sin commitear y reestructurar | ⚠️ **hoy nada lo impide** — es el hueco que este plan nombra |

⭐ **El #1 es el que mata:** una lista vacía se lee como *"no hay nada que indexar"*, y Foresito
seguiría trabajando **creyendo que no hay fuentes**. `principles/owner-3-validation.md`: *ausencia de
evidencia NO es evidencia*.

---

## 4 · QUÉ CHECK LO VIGILA DESPUÉS

**`check-structure` ya avisa** de los archivos sin commitear del Maestro (medido: sale en 🟡). Lo que
falta es que **ese aviso escale a 🔴 cuando lleve días** — un amarillo permanente se vuelve
invisible, que es justo lo que pasó aquí.

⚠️ Y su matiz, ya escrito en el propio validador: *las rutas dentro del Maestro son relativas a SU
raíz, no a la de Mente* — una reescritura masiva desde Mente **rompió 8 enlaces el 2026-07-30**.

---

## 5 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No toca el Maestro sin apagar o avisar a Foresito.** Es producción.
- ⛔ **No mueve el sub-repo dentro del repo de Mente.** Anidar un `.git` dentro de otro es el
  defecto que `piezas.tsv` documenta en su cabecera.
- ⛔ **No decide el alcance de la reestructuración.** Eso es criterio de Brian (paso 3).

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` · `bridges/Puentes_Mente_OS.md` (el gate) ·
`Maestro/punteros.tsv` (la fuente de ramas) · `bin/check-structure` (quien ya avisa).
