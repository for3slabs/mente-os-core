# RULE · PENDING ROTATION — rotación mensual de pendientes
**Status:** current · **Type:** rule · **Updated:** 2026-08-08 · **Owner:** brian
**Applies to:** `memory/pendiente-<mes>-<año>.md` · **Shape:** `rules/contract-pending.md`
**Verified by:** `bin/check-pendings` · `bin/test-f0-f6`
**Replaces:** la rotación *"por cierre, no por fecha"* (`memory/PENDIENTES.md`, 2026-07-29) — ver §4
---

## Purpose

**Rota el ARCHIVO, no el pendiente.** Brian, 2026-08-08:

> *"El pendiente de enero puede seguir hasta diciembre. Lo que rotamos es el archivo que contiene
> al pendiente. El archivo es el que cambia por mes; el pendiente se arrastra hasta que se cierre."*

---

## 1 · LA MECÁNICA — cada inicio de mes

```
memory/pendiente-agosto-2026.md   ──rota──▶   memory/pendiente-septiembre-2026.md
        │                                              │
        │ los CERRADOS se quedan aquí                  │ los ABIERTOS y PAUSADOS
        │ (con su fecha de cierre)                     │ se REESCRIBEN íntegros
```

| Qué pasa con… | Destino |
|---|---|
| **Abierto** o **pausado** | ✅ se **reescribe completo** en el mes nuevo |
| **Cerrado** / **terminado** | ⛔ se queda en el mes donde murió, con su fecha |
| **Eliminado** | ⛔ se queda, con la razón escrita |

📊 **Ejemplo de Brian:** *"si este mes solucionamos 10, entonces el siguiente mes tendríamos 24 del
v1"*. El archivo mensual **es** la métrica: si el número no baja, la deuda no baja.

---

## 2 · ⭐ SE REESCRIBEN, NO SE APUNTAN

> **Brian, 2026-08-08:** *"aquí se vuelven a apuntar, es decir se vuelven a escribir tal cual.
> ¿Por qué? Porque no queremos que por un bug o error no encuentres los pendientes."*

⛔ **Prohibido rotar con punteros** (*"ver el archivo de agosto §3"*). Cada archivo mensual es
**autosuficiente**: se lee solo, sin abrir los anteriores.

**Por qué, y no es redundancia por gusto:** un puntero roto convierte un pendiente en invisible, y
un pendiente invisible no se planifica ni se cierra — desaparece. La duplicación cuesta bytes; la
pérdida cuesta trabajo que nadie sabe que falta.

⚠️ El precio aceptado a conciencia: si un pendiente se edita, se edita en **el mes vivo**. Los meses
anteriores son historia congelada y **no se corrigen** — el rastro debe mostrar lo que se sabía
entonces.

---

## 3 · 🆕 DE DÓNDE VIENE — el campo `Arrastrado desde`

Todo pendiente que rota lleva **el archivo del que llegó**:

```markdown
- **Arrastrado desde:** `memory/pendiente-agosto-2026.md`
```

Se propaga hacia atrás en cadena, así que el rastro completo se recorre archivo por archivo.

⭐ **Por qué es una función y no un adorno:** sin ella, un pendiente que lleva seis meses vivo se lee
igual que uno de ayer. **La antigüedad ES información** — un pendiente que ha rotado cinco veces sin
cerrarse está diciendo algo, normalmente que nunca fue prioridad real o que le falta un plan.

---

## 4 · POR QUÉ REEMPLAZA A LA REGLA ANTERIOR

La regla del 2026-07-29 decía *"rotación por CIERRE, no por fecha — un pendiente de enero puede
seguir abierto en diciembre"*. **Ese objetivo se conserva íntegro:** el pendiente de enero sigue
vivo en diciembre. Lo que cambia es el **mecanismo**, y el nuevo añade dos cosas que el viejo no
tenía:

| | Anterior (29-jul) | ⭐ Ahora |
|---|---|---|
| Qué rota | lo cerrado sale a un archivo anual | **el archivo entero, cada mes** |
| Rastro de antigüedad | ninguno | **`Arrastrado desde`** |
| El archivo como métrica | no — mezcla abierto y cerrado | **sí: lo que queda es lo que se debe** |

⛔ **No coexisten.** Dos reglas de rotación vivas es cómo nace el próximo bug: la del 29-jul queda
derogada y este archivo es el único que gobierna.

---

## 5 · LA PRIMERA ROTACIÓN — de `memory/PENDIENTES.md` al formato nuevo

El archivo histórico (**4,794 líneas · 76 secciones**) se convierte una sola vez:

1. Separar cerrado de abierto — hay marcas `✅ CERRADO` / `RESUELTO`, y **casillas `[ ]` que no
   coinciden con el título de su sección** (medido: una sección `✅ CERRADO` con 7 casillas abiertas).
2. **Verificar cada pendiente contra el disco antes de arrastrarlo.** Medido el 2026-08-08: 2 de los
   9 pendientes v2 ya estaban HECHOS. ⭐ **Arrastrar sin verificar propaga deuda falsa.**
3. Agrupar lo abierto en bloques (`rules/contract-pending.md` §2); lo que no encaje → `PENDIENTE-EXTRA`.
4. `memory/PENDIENTES.md` queda como archivo histórico y **deja de recibir escrituras**.

---

Related: `rules/contract-pending.md` (la forma de un pendiente y de un bloque) ·
`rules/contract-archive.md` · `rules/rule-session-close.md` · `bin/check-pendings`.
