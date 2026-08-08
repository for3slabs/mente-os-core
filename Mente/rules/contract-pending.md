# CONTRACT · un PENDIENTE y su BLOQUE
**Status:** current · **Type:** contract · **Updated:** 2026-08-08 · **Owner:** brian
**Applies to:** every entry in `memory/pendiente-<mes>-<año>.md`
**Verified by:** `bin/check-pendings` · **Rotation:** `rules/rule-pending-rotation.md`
**Source:** criterio de Brian, 2026-08-08 (sesión de rediseño de pendientes)
---

## 0 · POR QUÉ EXISTE

`memory/PENDIENTES.md` llegó a **4,794 líneas · 348 KB** mezclando 30 secciones cerradas con 46
abiertas. Medido el 2026-08-08: **2 pendientes v2 estaban HECHOS** (los 30 ADRs existen, las 3
jerarquías existen) y seguían contando como deuda, y una sección marcada `✅ CERRADO` tenía 7
casillas sin marcar.

> ⭐ **Un pendiente que miente sobre su estado es peor que no tenerlo**, porque se planifica sobre él.

**El tamaño debe ser una métrica: si crece, la deuda crece.** Hoy no dice nada porque mezcla lo
resuelto con lo vivo.

---

## 0-bis · DÓNDE ENCAJA ESTO — los 3 sistemas de For3s (Brian, 2026-08-08)

**For3s (la empresa) vive de tres sistemas, no de uno:**

| Sistema | Qué es |
|---|---|
| 🤖 **Agentes** | los For3s desplegados — Telegram, canal API, multi-instancia |
| 🧠 **Mente OS** | ⭐ **la HERRAMIENTA que construimos para que lo demás funcione.** v1 → v2, y **todo v1 se migra a v2** |
| 🏢 **For3s OS** | el producto |

⭐ **Mente OS no es un proyecto aparte: es parte de la construcción de For3s OS.** Por eso un
pendiente de Mente OS y uno del producto **conviven en el mismo archivo** — separarlos por
"sistema" fue lo que hizo que dos pendientes v2 cumplidos siguieran contando como deuda.

---

## 1 · LA FORMA DE UN PENDIENTE

```markdown
### <ID> · <título en una línea>

- **Prioridad:** 🔴 urgente | 🟠 medio | 🟢 sin prisa
- **Estado:** activo | pausado | cerrado | eliminado
- **Creado:** YYYY-MM-DD · **Modificado:** YYYY-MM-DD · **Cerrado:** YYYY-MM-DD | —
- **Arrastrado desde:** `pendiente-<mes>-<año>.md` | — (nació aquí)
- **Archivos de referencia:** rutas — ⚠️ punto de partida, NO la lista completa
- **Plan:** `docs/plans/PLAN-<nombre>.md` | — (pendiente pequeño, no lo necesita)
- **Depende de:** `<bloque>` § — o `—`

**Descripción.** Todo lo que hay que saber para retomarlo sin preguntar: qué falla, qué se midió,
qué se decidió y qué NO. Si el lector tiene que reconstruir contexto, la descripción está incompleta.
```

### Campo por campo

| Campo | Regla |
|---|---|
| **Prioridad** | 🔴🟠🟢 — **la propone la IA** con el criterio de los ADRs y Brian corrige. ⛔ **Nunca justifica omitir un pendiente:** un bloque se atiende ENTERO, el color solo ayuda a leer |
| **Estado** | `pausado` ≠ `cerrado`. **Pausado sigue rotando**; cerrado se queda en el mes que murió |
| **Las 3 fechas** | creación · modificación · cierre. Sin fecha de cierre, un pendiente no está cerrado por mucho que lo diga la prosa |
| **Arrastrado desde** | 🆕 **desde qué archivo llegó.** Sin esto no se sabe cuánto lleva vivo, y un pendiente de 6 meses se lee igual que uno de ayer |
| **Archivos de referencia** | ⚠️ **NO son ley.** Brian, 2026-08-08: *"como es un pendiente no sabemos qué tan grande sea el error, es solo para tomar como referencia por dónde iniciar"* |
| **Plan** | los grandes o anidados lo llevan; los pequeños **no pueden** apuntar a uno inventado |
| **Depende de** | si depende de otro bloque, **se leen LOS DOS antes de construir** — el panorama parcial es cómo se rompe lo de al lado |

---

## 2 · TODO PENDIENTE VIVE EN UN BLOQUE

Un pendiente suelto no existe: **pertenece a un bloque de pendientes** (`## BLOQUE · <nombre>`).

### Para abrir un BLOQUE hacen falta 3 cosas

| # | Requisito | Por qué |
|---|---|---|
| 1 | **Análisis** de lo que se va a realizar | un bloque sin análisis es una carpeta con nombre |
| 2 | **≥2 pendientes** | uno solo no es un tema, es un pendiente. ⭐ **Excepción: tema NUEVO** — si la memoria no conoce dónde clasificarlo, 1 basta |
| 3 | **Plan de implementación GLOBAL** | `PLAN-GLOBAL-<bloque>.md` — qué se hace con el bloque entero |

### ⭐ `BLOQUE · PENDIENTE-EXTRA` — el cajón declarado

Lo que **no encaja en ningún bloque** va ahí. No es un vertedero: es la declaración honesta de
*"esto existe y todavía no sé de qué es"*.

⚠️ **Si un pendiente no cumple este contrato, primero se investiga: algo va mal.** Solo cuando se
comprueba que no hay defecto, se manda a `PENDIENTE-EXTRA` — nunca al revés.

---

## 3 · LOS DOS TIPOS DE PLAN

| Plan | Alcance | Cuándo |
|---|---|---|
| **`PLAN-GLOBAL-<bloque>.md`** | el bloque entero: qué se hace con cada pendiente y en qué orden | 🔴 obligatorio para abrir un bloque |
| **`PLAN-<pendiente>.md`** | UN pendiente a profundidad: comportamiento, aristas, verificación | cuando es grande o tiene pendientes anidados |

⭐ **Un plan aprovecha v2 entero**, no es una lista de tareas: declara qué bloque de trabajo lo
ejecutará, qué estándares `§D` aplican, qué se mide para saber que cerró y **cómo se vería fallar**
(`principles/expertise/val-functional.md` §2.2). Un plan que no dice cómo se verifica no es un plan.

---

## 4 · LOS 4 VERBOS DE UN PENDIENTE

| Verbo | Qué hace | ¿Rota al mes siguiente? |
|---|---|---|
| **Pausar** | sigue vivo, no se trabaja ahora | ✅ sí |
| **Cerrar** | resuelto, con su fecha y su evidencia | ⛔ no — se queda en el mes donde murió |
| **Terminar** | sinónimo de cerrar | ⛔ no |
| **Eliminar** | dejó de tener sentido — **se escribe POR QUÉ** | ⛔ no |

⛔ **Eliminar sin razón escrita está prohibido:** un pendiente que desaparece sin explicación vuelve
a nacer dentro de tres meses como hallazgo nuevo.

---

## 5 · CÓMO SE MUESTRAN CUANDO BRIAN LOS PIDE

Con la forma del bloque 📦 ENTREGA (`principles/contract-delivery.md`), aplicada a pendientes:

```
📋 PENDIENTES · <mes> <año>            🔴 N urgentes · 🟠 N medios · 🟢 N sin prisa

## BLOQUE · <nombre>                    N abiertos · N cerrados este mes
  🔴 <ID> · <título>            arrastrado desde <mes>  ·  plan: sí/no
  🟠 <ID> · <título>            nació aquí

### ✅ CERRADOS ESTE MES
### 🙋 NECESITA TU DECISIÓN            — o la palabra "nada"
### 👉 QUE SIGUE                       — el ÚNICO siguiente
```

⭐ **Nunca una lista plana:** el bloque es la unidad de lectura, y un pendiente sin su bloque no
dice de qué trata.

---

Related: `rules/rule-pending-rotation.md` (la rotación mensual) · `rules/contract-block.md` (la
forma que este contrato imita: barato de abrir, caro de cerrar) · `rules/contract-document.md` ·
`principles/contract-delivery.md` (la forma de la entrega) · `bin/check-pendings`.
