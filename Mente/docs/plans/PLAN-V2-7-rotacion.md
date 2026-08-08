# 🗺️ PLAN · V2-7 — terminar la rotación de pendientes
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-7
**Orden:** 3 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`)
---

## Purpose

Cerrar la migración del archivo de pendientes al formato nuevo. **Va tercero porque los pendientes
son la brújula:** mientras estén a medias, todo lo demás se planifica sobre datos incompletos.

---

## 1 · EL ESTADO REAL — medido 2026-08-08

| Qué | Medido |
|---|---|
| Contrato + regla + validador | ✅ escritos (`rules/contract-pending.md` · `rules/rule-pending-rotation.md` · `bin/check-pendings`) |
| Archivo del mes vivo | ✅ **27 pendientes** en 5 bloques, 0 errores de contrato |
| Histórico `memory/PENDIENTES.md` | 🟡 **4,808 líneas · 76 secciones**, declarado CONGELADO |
| Check que vigila el congelado | ✅ en la batería |

**Lo que queda:** los 27 pendientes del archivo vivo son **agrupaciones**, no los ítems sueltos. El
bloque `PRODUCTO-FOR3S-OS` guarda 8 pendientes que **contienen 87 casillas** del histórico
(P-1 sola son 18 capacidades de Hermes).

---

## 2 · LA PREGUNTA QUE DECIDE EL ALCANCE 🙋 BRIAN

**¿Se migran los 87 ítems uno por uno, o se quedan agrupados?**

| Opción | Qué significa |
|---|---|
| **Agrupados (hoy)** | 8 pendientes que apuntan al histórico para el detalle. ⚠️ El histórico está congelado: consultarlo es legítimo, pero **el detalle vive fuera del archivo vivo** |
| **Uno por uno** | ~90 pendientes con sus 3 fechas, prioridad y archivos. El archivo vivo crece a ~2,000 líneas y **vuelve a ser ilegible** — el problema que la rotación resolvió |

⭐ **Recomendación medida:** dejarlos agrupados. **34 de los 87 están congelados por decisión de
Brian**; migrar uno por uno algo que nadie va a tocar reconstruye el cementerio que acabamos de
cerrar. Se migran **cuando se descongelen**, no antes.

---

## 3 · EL TRABAJO — 3 pasos

1. **Decidir el alcance** (§2) — sin esto, el resto es adivinar.
2. **Verificar que ningún ítem abierto se perdió**: contar casillas `[ ]` del histórico contra lo que
   el archivo vivo declara. 🔬 Medido el 2026-08-08: **87 abiertas** — ese es el número a cuadrar.
3. **Cerrar V2-7 con evidencia**: el conteo cuadra y `check-pendings` sale en 0 errores.

---

## 4 · CÓMO SE VERÍA FALLAR

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Escribir un pendiente nuevo en `memory/PENDIENTES.md` | la batería debe **fallar**: el histórico está congelado |
| 2 | Borrar el archivo del mes vivo | la batería debe fallar: *"el mes no rotó"* |
| 3 | Marcar un pendiente `cerrado` sin fecha de cierre | `check-pendings` debe salir 🔴 |

🔬 Los tres **ya se probaron** el 2026-08-08 al construir el validador. Este plan los repite al
cerrar, porque un check que pasó una vez no prueba que siga vivo.

---

## 5 · QUÉ CHECK LO VIGILA DESPUÉS

Los 4 que ya existen en la batería (validador presente · mes vivo existe · contrato cumplido ·
histórico congelado). ⭐ **No hace falta uno nuevo:** este pendiente no añade mecanismo, **termina de
usar el que ya está construido**.

⚠️ **Lo que sí falta y no lo cubre ningún check: la rotación de septiembre.** Nadie la dispara —
hoy depende de que alguien se acuerde el día 1. Registrarlo como pendiente propio al cerrar V2-7.

---

## 6 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No borra `memory/PENDIENTES.md`.** Guarda el POR QUÉ de decisiones vigentes; `rules/contract-document.md`
  §5: *un fósil no se borra, se marca.*
- ⛔ **No descongela nada.** Los 34 ítems pausados siguen pausados: eso es decisión de Brian.

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` · `rules/rule-pending-rotation.md` ·
`rules/contract-pending.md` · `memory/PENDIENTES.md` (el histórico congelado).
