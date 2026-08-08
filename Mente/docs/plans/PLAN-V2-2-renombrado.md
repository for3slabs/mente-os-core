# 🗺️ PLAN · V2-2 — renombrado a la convención inglesa
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Pendiente:** `memory/pendiente-agosto-2026.md` → BLOQUE MOTOR → V2-2
**Orden:** 7 de 7 (`docs/plans/PLAN-GLOBAL-motor.md`) — el último: 🟢 el daño real ya está cubierto
---

## Purpose

Terminar de llevar los nombres de archivo a la convención declarada en
`rules/NAMING_CONVENTION.md` §7.4, que ya trae el plan completo escrito.

---

## 1 · EL ESTADO REAL — medido 2026-08-08

📊 **Quedan ~16 archivos**, no 208. La migración v1→v2 se llevó la mayoría por el camino.

| Grupo | Archivos | Qué hacer |
|---|---|---|
| **Convención universal** | `README` `CHANGELOG` `LICENSE` `CAPABILITIES` `INDEX` `STATES` `DECISIONS` `METRICS` | ⛔ **NO se tocan** — mayúsculas es su forma correcta en cualquier repo |
| **Puertas de entrada** | `RETOMAR.md` · `memory/PENDIENTES.md` | 🙋 **decisión de Brian**: son las que él escribe a mano cada día |
| **Reglas** | `rules/ESTANDAR_Metodo_Fases_F.md` · `rules/NAMING_CONVENTION.md` | 🟡 candidatos reales |
| **Archivo histórico** | 5 en `memory/archive/` | ⛔ **fósiles: no se renombran** (`rules/contract-document.md` §5) |
| **Planes nuevos** | `PLAN-GLOBAL-motor.md` y los 6 `PLAN-V2-*.md` | ⚠️ ver abajo |

🔴 **El hallazgo que destapó escribir este plan:** los planes que acabo de crear **entran en la lista
de renombrado**. `rules/contract-pending.md` §3 dicta el nombre `PLAN-<nombre>.md` en mayúsculas, y
`NAMING_CONVENTION` §7.4 pediría minúsculas. ⭐ **Dos reglas del sistema se contradicen entre sí**, y
la contradicción nació hoy, escribiendo el plan de la regla que la delata.

---

## 2 · LA DECISIÓN QUE HAY QUE TOMAR PRIMERO 🙋 BRIAN

**¿Qué gana cuando un contrato dicta un nombre y la convención dicta otro?**

| Opción | Consecuencia |
|---|---|
| **Manda la convención** | hay que corregir `rules/contract-pending.md` §3 y renombrar los 7 planes |
| **Mandan los contratos** | `NAMING_CONVENTION` declara la excepción: *"un nombre dictado por un contrato no se renombra"* |

⭐ **Sin esta decisión el pendiente no se puede ejecutar**, porque cada archivo tendría dos nombres
correctos. `rules/rule-inheritance.md` dice *"en conflicto gana la más estricta"* — pero aquí **ninguna es
más estricta**: son dos formas distintas, no dos niveles de exigencia.

---

## 3 · EL TRABAJO — 3 pasos

1. **Resolver el conflicto de §2** (decisión de Brian).
2. **Renombrar con `git mv`**, nunca copiando: la historia del archivo debe sobrevivir.
3. **Reescribir las citas** — y verificar con `bin/check-links` que llega a **0 rotas**.

---

## 4 · CÓMO SE VERÍA FALLAR

| # | Sabotaje | Resultado que lo valida |
|---|---|---|
| 1 | Renombrar un archivo sin actualizar quien lo cita | `check-links` debe salir 🔴 |
| 2 | Renombrar una pieza de `piezas.tsv` sin actualizar la tabla | `check-structure` debe decir `PIECE MOVED OR LOST` |
| 3 | Renombrar un fósil de `memory/archive/` | ⚠️ **hoy nada lo impide** — y borrar/mover historia rompe el diagnóstico |

---

## 5 · QUÉ CHECK LO VIGILA DESPUÉS

`check-links` y `check-structure` **ya cubren** el daño real (citas rotas, piezas perdidas). ⭐ Por eso
este pendiente bajó de 🔴 a 🟢: **lo que dolía ya tiene candado**; lo que queda es cosmética.

Lo que **sí falta**: un check que impida renombrar un fósil.

---

## 6 · LO QUE ESTE PENDIENTE NO HACE

- ⛔ **No renombra `README`, `CHANGELOG`, `LICENSE`** ni los generados: mayúsculas es su convención.
- ⛔ **No toca `memory/archive/`** — son fósiles.
- ⛔ **No renombra nada antes de resolver §2.**

---

Related: `docs/plans/PLAN-GLOBAL-motor.md` · `rules/NAMING_CONVENTION.md` §7.4 (el plan detallado) ·
`rules/contract-pending.md` §3 (la regla que contradice) · `rules/contract-document.md` §5 (fósiles).
