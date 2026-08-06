# 🔬 ANÁLISIS COMPARATIVO — 3 frameworks vs Mente OS v2
**Status:** current · **Type:** analysis · **Updated:** 2026-07-29 · **Owner:** brian
**Fecha:** 2026-07-27 · **Petición de Brian:** *"compara Mente OS con opentag, agent-os y open-swe"*

## Purpose

Contrastar Mente OS v2 contra 3 frameworks externos para saber qué le falta y qué ya hace mejor.
El hallazgo que decidió el rumbo: **ninguno responde "¿esto es producto o MVP?"** — ese veredicto
medido es el diferenciador del sistema.

> ⚠️ **Notación INTERNA.** Aquí se nombran las fuentes para el análisis; **lo que se construya NO
> cita el origen** (regla LOCKED, Método F §1).
> **Complementa:** `docs/analysis-internos-v1.md` (el 4º framework analizado).
---

## 1 · QUÉ ES CADA UNO

| Proyecto | Problema que resuelve | Naturaleza |
|---|---|---|
| **Agent OS** (buildermethods) | extraer estándares del código e inyectarlos según lo que construyes | comandos + perfiles · md |
| **Open SWE** (LangChain, MIT) | framework para agentes de código internos: sandbox, ~15 tools, orquestación | Deep Agents + LangGraph |
| **OpenTag** (amplifthq) | ejecutar agentes locales desde Slack/GitHub con recibos y ledger auditable | 16 paquetes npm · TS |
| **Mente OS v2** | gobernar cómo se construye **+ verificar si el resultado es producto o MVP** | doctrina + validadores |

---

## 2 · 🔴 AGENT OS — el más cercano al v2

**Sus 4 funciones son casi el v2 punto por punto:**

| Agent OS | Mente OS v2 | ¿Coinciden? |
|---|---|---|
| **Discover Standards** — extraer patrones del código existente | 🔴 **al revés**: el criterio lo escribe Brian | ⚠️ **diferencia crítica** |
| **Deploy Standards** — *"inyectar los relevantes según lo que construyes"* | ✅ §12-QUATER capas A + B + D | ✅ misma idea |
| **Shape Spec** — mejores planes → mejores builds | ✅ el `BLOQUE.md` (§3.2-TER) | ✅ |
| **Index Standards** — mantenerlos organizados y descubribles | ✅ `generar-indice` (§12-TER) | ✅ |

### ⭐ 2.1 · Confirma la decisión más importante del v2

Su mecanismo de aplicación, textual:

> *"Agent OS aplica los estándares inyectando las guías relevantes según el contexto,
> **asegurando consistencia sin enforcement pesado**."*

**Eso es exactamente el camino que el v2 RECHAZÓ.** Y no por gusto — por evidencia medida:

| Forma de la regla | Cumplimiento en Mente OS |
|---|---|
| **código** (gate, permisos fail-closed) | ✅ **100%** |
| **documento / inyección + confianza** | 🔴 **falla 40-60%** |

El Método F es precisamente un estándar bien escrito, inyectado por referencia en `CLAUDE.md`, y
**en 2 de 5 sesiones nunca se leyó**. Agent OS eligió inyectar y confiar. El v2 eligió **3 puertas
cerradas** (§12-QUATER) porque los datos dicen que confiar no basta.

> **Conclusión:** que un proyecto maduro haya optado por "sin enforcement pesado" **valida que la
> decisión del v2 es una postura consciente**, no un exceso.

### ⚠️ 2.2 · "Discover Standards" sería PELIGROSO en nuestro caso

Ellos extraen los estándares **del código que ya existe**. En Mente OS eso sería contraproducente:

| Si extrajéramos patrones de… | Extraeríamos… |
|---|---|
| la demo | `userStore.ts` con 21 toques y 5 responsabilidades |
| `for3sChat.ts` | lógica duplicada en 6 sitios |
| los 60 commits | **42% de fixes como si fueran el método** |

> **Extraer estándares de código vibecodeado produce estándares vibecodeados.**
> Por eso la decisión 3 del v2 —*"el criterio lo diseña Brian, la IA solo le da forma"*— es correcta
> y **no debe cambiarse** aunque exista un mecanismo automático que parezca más cómodo.

### 2.3 · Lo que NO tienen
- ❌ Ningún veredicto de calidad: nada responde *"¿esto es producto o MVP?"*
- ❌ Ninguna doctrina de fix ≠ parche
- ❌ Ningún grafo de propagación
- ❌ Ninguna gestión de contexto que sobreviva al `/clear`

---

## 3 · 🟡 OPEN SWE — dos piezas incorporadas

### ✅ 3.1 · INCORPORADO · Middleware que COMPLETA, no solo verifica

> *"El middleware compromete y abre el PR automáticamente **si el agente no lo hizo**."*

**Por qué se incorpora, medido:** la regla *"sin registro no hay `/clear`"* existe desde el 14-jul y
**se incumplió 5 de 11 veces**. Un validador que solo avisa **habría avisado 5 veces y seguiríamos
con 5 sesiones sin registrar.**

→ **Integrado en §12-T.1**, con la regla dura que le faltaba a la referencia:
**completar es para lo DERIVABLE, nunca para el criterio.** Todo lo autocompletado se marca `auto:`.

### ✅ 3.2 · Confirma el límite de 3 encargados

> *"En lugar de acumular cientos de tools, Open SWE provee ~15 cuidadosamente seleccionadas."*

Es la misma lógica que Brian fijó: *"nunca más de 3, porque si no el sistema no entiende"*.
**Dos proyectos independientes llegaron al mismo principio: menos piezas, elegidas.**

### 3.3 · Lo que NO aplica

| Suyo | Por qué no |
|---|---|
| Sandboxes cloud (Modal, Daytona, Runloop) | el server `for3s` ya aísla por `docker compose -p` |
| `AGENTS.md` único para todo el repo | ⭐ el v2 lo tiene **mejor**: estándares **por bloque** (§D), no globales |
| Deep Agents + LangGraph | Mente OS es doctrina + validadores, no un runtime de agentes |
| Invocación desde Slack/Linear | la superficie de Brian es Claude Code |

> ⭐ **Nota:** su `AGENTS.md` global es exactamente el problema que el v2 evita. Un archivo único
> para todo el repo no puede decir *"para ESTA tarea aplica el criterio de BD"*. El campo §D del
> bloque sí.

---

## 4 · 🟢 OPENTAG — una pieza incorporada

### ✅ 4.1 · INCORPORADO · Recibo de aprobación

> *"Action receipts: superficies de aprobación compactas que muestran los cambios propuestos
> **antes** de ejecutar."*

**El hueco que cerró:** el v2 tenía 3 puertas que bloquean, pero **ninguna forma de presentar el
cambio para aprobar de un vistazo**. Bloquear sin dar salida es fricción pura.

→ **Integrado en §12-T.2** con 3 reglas propias: cabe en una pantalla · muestra la **propagación**
(lo que Brian no podía ver) · incluye la evaluación de la construcción (§7).

### 4.2 · Su work ledger — más estricto que el nuestro

Registra: **evento origen · decisión de admisión · snapshot de contexto · resultado.**
Nuestro `guardados.md` solo lleva commits.

🟡 **Anotado como mejora futura**, no incorporado aún: habría que decidir si el bloque necesita ese
nivel de trazabilidad o si es burocracia para un equipo de una persona.

### 4.3 · Lo que NO aplica
Su arquitectura entera (Slack → listener → dispatcher → runner → ACP) resuelve *"invocar agentes
desde el chat del equipo"*. **No es el problema de Brian.**

---

## 5 · TABLA MAESTRA

| Capacidad | Agent OS | Open SWE | OpenTag | internOS | **Mente OS v2** |
|---|---|---|---|---|---|
| Estándares según contexto | ✅ | 🟡 global | ❌ | ❌ | ✅ por bloque |
| **Enforcement duro** | 🔴 *"sin enforcement pesado"* | 🟡 middleware | ✅ recibos | 🟡 scripts | ✅ **3 puertas** |
| Validadores que completan | ❌ | ✅ | 🟡 | ❌ | ✅ **§12-T.1** |
| Recibo de aprobación | ❌ | ❌ | ✅ | ❌ | ✅ **§12-T.2** |
| Unidad de trabajo con estado | ❌ | 🟡 todos | ✅ ledger | ✅ workstream | ✅ bloque |
| Contexto que sobrevive al reset | ❌ | 🟡 | ✅ | ✅ | ✅ |
| Límites de tamaño validados | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Grafo de propagación** | ❌ | ❌ | ❌ | ❌ | ⭐ **§3.1-bis** |
| **Fix ≠ parche** | ❌ | ❌ | ❌ | ❌ | ⭐ **§7** |
| **¿Producto o MVP?** | ❌ | ❌ | ❌ | ❌ | ⭐⭐⭐ **§12-QUINQUIES** |
| **QA de criterio de senior** | ❌ | ❌ | ❌ | ❌ | ⭐⭐ **6 dimensiones** |
| **LA VOZ** | ❌ | ❌ | ❌ | ❌ | ⭐⭐ **Encargado 0** |
| **En producción** | ✅ | ✅ | ✅ | ✅ | 🔴 **nada construido** |

---

## 6 · LAS 4 CONCLUSIONES

### ① El veredicto de calidad es un hueco REAL del mercado
**Cuatro frameworks maduros, en producción, y ninguno responde *"¿esto es producto o MVP?"***
Todos resuelven **coordinación** (qué hacer, en qué orden, con qué contexto). **Ninguno resuelve
verificación de calidad interna.**

> No es una obsesión de Brian: es el hueco que nadie ha llenado. **Es el diferenciador del v2.**

### ② La decisión de enforcement duro queda validada por contraste
Agent OS eligió *"sin enforcement pesado"*. El v2 eligió 3 puertas cerradas **con datos**:
código = 100%, documento = 40-60%. **Saber que otro proyecto tomó el camino contrario convierte la
decisión del v2 en postura consciente.**

### ③ El criterio debe venir de Brian, nunca del código existente
Su "Discover Standards" extrae patrones del código. **Aplicado a la demo extraería el vibecoding.**
La decisión 3 del v2 no se toca.

### ④ 🔴 La lección incómoda que se repite en los 4
**Los cuatro están construidos y funcionando. El v2 tiene el mejor diseño y cero líneas escritas.**

- internOS: v1.0.0 tras **15 versiones** iterando
- Open SWE: patrones que **Stripe, Ramp y Coinbase** validaron por separado
- Agent OS y OpenTag: en uso

> **Es exactamente el patrón que nos trajo aquí: diseñar mucho antes de validar poco.**
> El plan lo previene (F3 el piloto antes de la maquinaria, valor temprano en F1/F3/F4) —
> **pero solo si se respeta.**

---

## 7 · INCORPORACIONES DE ESTE ANÁLISIS

| # | Qué | De dónde | Dónde quedó |
|---|---|---|---|
| 1 | **Validadores que COMPLETAN lo derivable** (marcado `auto:`) | Open SWE | ✅ **§12-T.1** · decisión 19 |
| 2 | **Recibo de aprobación** al bloquear una puerta | OpenTag | ✅ **§12-T.2** · decisión 20 |
| 3 | Work ledger de 4 campos por evento | OpenTag | 🟡 anotado, sin decidir |

---

Relacionado: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (el plano) ·
`principles/vision-mente-os-v2.md` (el porqué) ·
`docs/analysis-internos-v1.md` (el 4º framework) ·
[[project_mente_os_v2_bloques]].

---

Related: `principles/vision-mente-os-v2.md` (la visión que este análisis contrastó) · `docs/analysis-internos-v1.md` (el otro análisis comparativo).
