# 🗺️ PLAN GLOBAL · BLOQUE MOTOR
**Status:** current · **Type:** plan · **Updated:** 2026-08-08 · **Owner:** brian
**Gobierna:** `memory/pendiente-agosto-2026.md` → `## BLOQUE · MOTOR`
**Contrato:** `rules/contract-pending.md` §2 (todo bloque necesita su plan global) · §3 (los dos tipos)
**Criterio de orden:** Brian, 2026-08-08 — *"lo que desbloquea a otro primero"*
---

## Purpose

En qué **orden** se atacan los 7 pendientes del bloque MOTOR, **por qué en ese orden**, y **qué se
mide** para decir que cada uno cerró. Sin esto hay que releer los 7 cada vez para recordar cuál
estorba a cuál.

> ⭐ **Qué NO es este documento:** no explica *cómo* se arregla cada pendiente — eso vive en el
> `PLAN-<pendiente>.md` de cada uno (Brian, 2026-08-08: *"cada pendiente debe tener su propio plan
> de implementación"*). Aquí solo va el orden y su razón.

---

## 0 · QUÉ ES EL BLOQUE MOTOR

**Mente OS mismo: la herramienta que construimos para que For3s OS funcione** (Brian, 2026-08-08).
No es el producto ni el agente — es `bin/`, `hooks/`, `rules/`, `principles/` y la forma del árbol.

⚠️ **Renombrado de `MENTE-OS-V2` a `MOTOR` el 2026-08-08.** El nombre anterior chocaba con el nombre
del sistema y **confundió a Brian en una lectura real**: leyó *"trabajar en MENTE-OS-V2"* como *"la
versión v2"* y no como *"ese cajón de pendientes"*. Un nombre que hay que explicar ya falló.

---

## 1 · EL GRAFO DE DEPENDENCIAS — medido, no supuesto

```
V2-1 ──bloquea──▶ V2-3
(arquitectura)    (encarpetado: la arquitectura declara el árbol objetivo)

V2-7  V2-4  V2-6  V2-5  V2-2      ← sin dependencias entre sí
```

**Una sola dependencia real en todo el bloque.** Todo lo demás puede hacerse en cualquier orden, así
que el criterio *"lo que desbloquea a otro primero"* solo fuerza una cosa: **V2-1 antes que V2-3.**

---

## 2 · EL ORDEN, Y POR QUÉ

| # | Pendiente | Va aquí porque… | Cierra cuando |
|---|---|---|---|
| **1** | **V2-1** arquitectura | 🔴 es lo único que **bloquea a otro**. Decisión de Brian ya tomada: **NO se parte** | su cabecera declara la excepción de fuente de verdad y el check de techo la respeta |
| **2** | **V2-3** encarpetado | queda desbloqueado en cuanto V2-1 cierre | la frontera motor/instancia se **ve** en el árbol, no hay que leerla |
| **3** | **V2-7** rotación | 🔴 los pendientes son la brújula: mientras esté a medias, el resto se planifica sobre datos incompletos | los 87 ítems v1 migrados y `memory/PENDIENTES.md` congelado sin escrituras |
| **4** | **V2-6** F0 abierto | 🟠 4 cosas sueltas que nunca se convirtieron en pendientes propios — son deuda **invisible** | las 4 tienen pendiente propio o están cerradas con evidencia |
| **5** | **V2-4** Maestro | 🟠 toca un sub-repo que **Foresito lee EN VIVO**: el más arriesgado, va después de estabilizar lo demás | el Maestro reestructurado sin romper al agente maestro |
| **6** | **V2-5** config | 🟢 lo urgente ya se hizo el 27-jul; queda barrido de fondo | `check-blocks` y `rule-config-hygiene` sin avisos de config |
| **7** | **V2-2** renombrado | 🟢 el daño real (citas rotas) ya lo cubren `check-links` y el candado de la batería | los 28 archivos renombrados y 0 citas rotas |

### ⚠️ Por qué V2-1 va primero aunque su decisión sea "no hacer nada"

**Cerrarlo cuesta minutos y libera a V2-3.** Brian decidió el 2026-08-08 declararlo **fuente de
verdad**: `principles/expertise/doc-structure.md` §2.1 lo permite para un documento que otros citan
**para RESOLVER una discusión**, no para consultar — y 46 documentos apuntan a este.

🔬 **La evidencia que sostiene la decisión, medida:** ya se partió una vez (julio,
`blk-split-architecture`) y hoy hay **74% duplicado** entre las mitades, con 330 líneas viviendo solo
en el original. **La partición creó la divergencia que debía evitar.**

⛔ **La excepción se ESCRIBE en la cabecera del archivo, nunca se asume** (`principles/expertise/doc-structure.md` §2.1:
*"and the exception is written in its header, never assumed"*). Un archivo grande sin su razón
escrita es indistinguible de un archivo descuidado.

---

## 3 · CADA PENDIENTE LLEVA SU PROPIO PLAN

> **Brian, 2026-08-08:** *"cada pendiente debe de tener su propio plan de implementación."*

| Pendiente | Su plan |
|---|---|
| V2-1 | `docs/plans/PLAN-V2-1-arquitectura.md` |
| V2-3 | `docs/plans/PLAN-V2-3-encarpetado.md` |
| V2-7 | `docs/plans/PLAN-V2-7-rotacion.md` |
| V2-6 | `docs/plans/PLAN-V2-6-f0-abierto.md` |
| V2-4 | `docs/plans/PLAN-V2-4-maestro.md` |
| V2-5 | `docs/plans/PLAN-V2-5-config.md` |
| V2-2 | `docs/plans/PLAN-V2-2-renombrado.md` |

Cada uno declara: **qué archivos toca** (referencia, no ley) · **cómo se vería fallar** · **qué check
lo vigila al cerrar**. El último punto es el que impide que el arreglo se deshaga solo.

---

## 4 · CÓMO SE SABE QUE EL BLOQUE ENTERO CERRÓ

**Los 7 en estado `cerrado` con su fecha**, y estas tres medidas en verde a la vez:

| Medida | Hoy | Al cerrar |
|---|---|---|
| `bin/test-f0-f6` | 210 · 0 fallos | 0 fallos, con los checks que cada pendiente añada |
| Clon de otro dueño | 197 · 1 fallo (el correcto) | igual o mejor |
| `bin/check-blocks` | 0 errores · 2 avisos | 0 errores |

⛔ **Un pendiente NO cierra porque su prosa lo diga: cierra con fecha y con evidencia medida**
(`rules/contract-pending.md` §1). Medido el 2026-08-08 en el archivo viejo: una sección marcada
`✅ CERRADO` tenía 7 casillas sin marcar.

---

## 5 · LO QUE ESTE PLAN NO ORDENA

- **El bloque `PRODUCTO-FOR3S-OS`** — 34 de sus ítems están **congelados por decisión de Brian**
  (*"registrados, NO desarrollar aún"*). Planificar el orden de algo que no se va a tocar produce un
  documento que caduca antes de leerse, y eso es lo que llenó `memory/PENDIENTES.md` de 4,794 líneas.
- **El bloque `ESTRATEGICO`** — espera decisiones de Brian (dominio, GPG, prueba de campo). Un plan
  de implementación sobre una decisión ajena sería inventar criterio (ADR-003).
- **El bloque `DEMO`** — su avance se gobierna en `blocks/active/demo/BLOCK.md`, no aquí.

---

Related: `memory/pendiente-agosto-2026.md` (los pendientes que este plan ordena) ·
`rules/contract-pending.md` (por qué un bloque necesita plan) ·
`principles/expertise/doc-planning.md` (qué hace ejecutable a un plan) ·
`principles/expertise/doc-structure.md` §2.1 (la excepción de fuente de verdad que cierra V2-1).
