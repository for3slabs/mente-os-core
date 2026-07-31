# ARCHITECTURE · the block — definition and anatomy

**Status:** current · **Type:** architecture · **Updated:** 2026-07-30 · **Owner:** brian
**Part of:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` (§3) · **Block:** `blk-split-architecture-2026-07`

## Purpose

What a BLOCK is, what a SUB-BLOCK is, and every field a `BLOCK.md` carries. Extracted verbatim from
§3 of the architecture on 2026-07-30: at 435 lines it was more than half the 800-line limit of the
whole document, and it is one distinct thing (ADR-027).

⚠️ **Moved, not rewritten.** A split that also edits content makes it impossible to tell a move
from a change in review (block §B OUT).

---

## 3 · EL BLOQUE — definición y anatomía

### 3.1 · Definición (Brian, literal)

> *"BLOQUE es una unidad de trabajo en donde están varias tareas a realizar, todas con la misma
> relación, por eso el nombre del bloque. Por ejemplo → IMPLEMENTACIÓN DE DEMO: dentro deben venir
> todas las tareas de demo. Y por supuesto son sus sub-bloques, para que ahora sí cada tarea ataque
> a una pieza de código."*

**Quedan definidos DOS NIVELES, cada uno con su trabajo:**

| Nivel | Qué es | Qué agrupa | Qué declara |
|---|---|---|---|
| **BLOQUE** | unidad de trabajo | tareas **con la misma relación** | conexiones con otros bloques |
| **SUB-BLOQUE** | una tarea | ataca **una pieza de código** | propagación sobre el código |

**Por qué importa la distinción:** el grafo existe en los dos niveles pero significa cosas
distintas. En el bloque, "conexión" = dependencia de trabajo. En el sub-bloque, "conexión" =
propagación técnica (qué se toca al tocar esto). **El fix-sobre-fix nace de no tener el segundo.**

Ejemplo real: bloque `IMPLEMENTACIÓN DE DEMO` → sub-bloques `userStore.ts`, `session.ts`,
`verificacion.ts`, `instancias.ts`…

### 3.1-bis · DIAGRAMA — los dos niveles y sus dos grafos

```
   NIVEL 1 · BLOQUES (unidades de trabajo)
   ═══════════════════════════════════════════════════════════════

   ┌──────────────┐   depende de   ┌──────────────┐
   │  CANAL API   │◄───────────────│     DEMO     │
   └──────────────┘                └──────┬───────┘
                                          │ depende de él
                                          ▼
                                   ┌──────────────┐      ┌──────────────┐
                                   │ PANEL ADMIN  │      │ ENTRENAMIENTO│
                                   └──────────────┘      └──────────────┘
                                                          ▲ AISLADO
                                                          └── sin conexión

   conexión = DEPENDENCIA DE TRABAJO
   ("no puedo cerrar DEMO si CANAL API no responde")


   NIVEL 2 · SUB-BLOQUES del bloque DEMO (tareas → piezas de código)
   ═══════════════════════════════════════════════════════════════

              ┌─────────────────┐
              │  userStore.ts   │  ← 5 dependientes 🔴
              └────────┬────────┘
          ┌────────────┼────────────┬──────────────┐
          ▼            ▼            ▼              ▼
   ┌───────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐
   │session.ts │ │for3sChat │ │admin.ts  │ │ route.ts    │
   └───────────┘ └──────────┘ └──────────┘ └─────────────┘

   conexión = PROPAGACIÓN TÉCNICA
   ("si toco userStore.ts, se propaga a 5 archivos")
   ⭐ ESTE grafo es el que decide el CARRIL (§5)
```

> **Por qué dos niveles y no uno:** el bloque responde *"¿qué trabajo depende de qué trabajo?"*.
> El sub-bloque responde *"¿qué código toco al tocar esto?"*. **El fix-sobre-fix nace de no tener
> el segundo:** sin el grafo de propagación, "cambiar dónde se guarda la key" parece un cambio de
> un archivo — y son seis.

### 3.1-ter · ✅ ANIDAMIENTO — MÁXIMO 3 NIVELES *(decidido por Brian 2026-07-27)*

**El caso que lo plantea:** una referencia externa madura (v1.0.0, en producción) empezó con dos
niveles y en su versión estable **añadió anidamiento a cualquier profundidad**. Que lo necesitaran
en producción es señal, no prueba.

**El caso real nuestro:** el bloque `DEMO` ya insinúa un tercer nivel —
`DEMO` → *«reestructuración de BD»* → `userStore.ts`. Hoy eso se aplasta en un solo nivel de
sub-bloques y se pierde la agrupación intermedia.

| Opción | Ventaja | Riesgo |
|---|---|---|
| **A · 2 niveles fijos** (hoy) | simple, imposible de enredar | trabajos grandes quedan con 20 sub-bloques planos |
| **B · Anidamiento libre** | refleja la realidad de trabajos grandes | árboles profundos = el desorden que estamos arreglando |
| **C · 3 niveles máximo** ⭐ | permite agrupar sin permitir laberintos | hay que respetar el tope |

> ## ✅ DECISIÓN: **máximo 3 niveles — `BLOQUE › GRUPO › SUB-BLOQUE`**
>
> Por coherencia con la regla que Brian ya fijó para los encargados: *"nunca más de 3, porque si no
> el sistema no entiende"*. **Mismo criterio, aplicado a la profundidad.**

```
DEMO                             ← NIVEL 1 · BLOQUE (unidad de trabajo)
├── reestructuración-BD          ← NIVEL 2 · GRUPO (opcional, agrupa por afinidad)
│   ├── userStore.ts             ← NIVEL 3 · SUB-BLOQUE (una pieza de código)
│   └── session.ts
└── seguridad
    ├── verificacion.ts
    └── container.ts
```

**Reglas del anidamiento:**
- El **GRUPO es opcional**: si el bloque tiene pocas tareas, se va directo a sub-bloques (2 niveles).
- **El nivel 3 es el tope duro.** Un sub-bloque **no puede** contener otro sub-bloque.
- Si un grupo necesitara subdividirse → **es señal de que debe ser su propio BLOQUE**, no un cuarto nivel.
- El validador `revisar-bloques` **rechaza** cualquier estructura de más de 3 niveles.

### 3.2 · Contenido obligatorio de un bloque

| Campo | Para qué |
|---|---|
| **Título** | identidad del bloque |
| **Descripción** | qué se quiere hacer |
| **Intención** | *"cada bloque debe crearse con una misma intención"* |
| **Límites — qué SÍ / qué NO** | ⭐ **el campo crítico**: delimita el alcance |
| **Conexiones** | ¿aislado o conectado? ¿de qué depende? ¿quién depende de él? |
| **Contexto** | el contexto propio del bloque, **en disco** |
| **Estado** | activo · bloqueado · cerrado |
| **Avance** | cuánto se ha avanzado |
| **Calificación** | evaluación de calidad del bloque |
| **Puntos de guardado** | uno por iteración o mejora |
| **Sub-bloques** | las tareas, con su estado |
| **Al cerrar** | resumen detallado + conexión con otros bloques |

> ⭐ **Sobre el campo "qué NO":** es la mitad que hoy no existe en ningún sitio y la causa directa
> de *"no, así no iba"*. Sin límite declarado, la IA reconstruye el alcance por inferencia cuando
> el contexto muere — **y suena igual de segura**. El "qué NO" es lo que lo impide.

### 3.2-bis · ⭐ LÍMITES DE TAMAÑO — declarados y VALIDADOS

**La evidencia que obliga a esta regla:**

| Archivo nuestro | Tamaño | ¿Tenía límite? | Resultado |
|---|---|---|---|
| `memory/PENDIENTES.md` | **240 KB** | ❌ | ilegible · leído 39× en una sesión |
| `memory/Estado_Sesion_Continuidad.md` | 196 KB | ❌ | fósil que sigue vivo |
| `memory/Bitacora_Progreso.md` | 162 KB | ❌ | crece sin recorte |
| `MEMORY.md` (memorias) | 19.5 KB | ❌ | la pieza **más pesada** del arranque |
| **`memory/RETOMAR.md`** | **14.4 KB** | ✅ ~200 líneas | **no se desbordó** |

> **El único archivo con límite declarado es el único que no se desbordó.** La disciplina de tamaño
> no es una buena costumbre: **es una función del sistema**.

**Límites por archivo del bloque:**

| Archivo | Límite | Naturaleza |
|---|---|---|
| `BLOCK.md` §A-D — identity, scope, connections, standards | **≤60 líneas** | se lee SIEMPRE |
| `BLOCK.md` §E `State` | **≤10 líneas** | latido operativo |
| `BLOCK.md` §J `Context` | **≤80 líneas (meta ≤50)** | **resumen CURADO, nunca un log** |
| `BLOCK.md` §G `Decisions` · §H `Friction` · §I `Checkpoints` | sin límite | append-only |
| `BLOCK.md` §F `Sub-blocks` | ≤20 filas | una tarea, una pieza |
| `docs/` del bloque | sin límite | ahí va el detalle largo |
| **`BLOCK.md` completo** | **≤150 líneas** | archivo único (§3.2-TER) |

**Reglas de higiene:**
- La **cronología detallada va en `docs/`**, nunca en `contexto.md`.
- **Se consolida ANTES de cerrar la sesión, no después.**
- El límite lo **verifica un script** (§16-BIS), no la buena voluntad.

### 3.2-QUATER · ⭐⭐⭐ LÍMITES POR TIPO DE DOCUMENTO — todo el sistema, no solo los bloques

> **Brian, 2026-07-29:** *"¿podemos empezar a controlar el tamaño de los archivos, o eso ya está
> diseñado en el v2? El control de todos los archivos, el volumen de todo, para que no se dispare."*

**El hueco que esto cierra:** el v2 tenía límites **solo para lo que va a crear** (el `BLOCK.md`).
**No para lo que ya existe, ni para sus propios documentos.**

#### 🔴 La evidencia — medida el 2026-07-29

| Archivo | Líneas | ¿Tenía límite? |
|---|---|---|
| `memory/Estado_Sesion_Continuidad.md` | **4,779** | ❌ |
| `memory/PENDIENTES.md` | **3,138** | ❌ |
| **`docs/Arquitectura_Mente_OS_v2_Bloques.md`** (este) | **2,347** | ❌ 🔴 |
| `memory/Bitacora_Progreso.md` | 1,506 | ❌ |
| `Cerebro/For3s_OS_Grafo_Maestro.md` | 1,279 | ❌ |
| `MEMORY.md` | 107 líneas / **19 KB** | ❌ — **la pieza más pesada del arranque** |
| `memory/RETOMAR.md` | 224 | ✅ **≤200 → el único que no se desbordó** |

> 🔴 **Este documento pasó de 995 a 2,347 líneas en UNA sesión (+1,352).**
> **El documento que predica límites de tamaño no tenía límite.** Va camino de ser el próximo
> `memory/PENDIENTES.md`, que también empezó siendo útil.

#### La tabla de límites

| Tipo | Límite | Qué se hace al pasarse |
|---|---|---|
| **Puerta de entrada** (`RETOMAR` · `INDEX` · `PENDING-BRIAN`) | **≤200 líneas** | mover contenido a punteros |
| **Contrato / regla** (`rules/*`) | **≤250** | partir por tema |
| **Arquitectura / plano** | **≤800** | 🔴 **partir en documentos por área** |
| **Plan** | **≤400** | mover fases cerradas a la bitácora |
| **`BLOCK.md`** | **≤150** | ver §3.2-bis (ya diseñado) |
| **`MEMORY.md`** (índice de memorias) | **≤80** | archivar memorias viejas |
| **Registro append-only** (bitácora · decisiones · roces) | **sin límite** | pero **rotación anual** |
| **`memory/PENDIENTES.md`** ⭐ | **sin límite** | **rotación por CIERRE**, no por fecha (ver abajo) |
| **Índice generado** (`INDEX` · `STATES` · `DECISIONS`) | sin límite | se **genera**, no se escribe |
| **Fósil** | **congelado** | no crece · se mueve a `docs/archive/` |

#### ⭐ LA REGLA QUE LAS UNE

> ## Un archivo no se parte por tamaño: se parte cuando contiene DOS COSAS DISTINTAS.
> **El límite es la SEÑAL, no la causa.**

Aplicado a este documento: **2,347 líneas significan que ya contiene varios documentos.**
§12-BIS a §12-SEPTIES son un manual de configuración; §10 es el sistema de aprendizaje. **Crecieron
dentro de un sitio que no era el suyo.** El tamaño solo lo hizo visible.

#### ⭐ El caso especial: `memory/PENDIENTES.md` — rotación por CIERRE, no por fecha

**Medido 2026-07-29: 3,213 líneas · 253 KB.** Es el archivo más grande del sistema después de los
fósiles, y **el único tipo que la tabla no cubría** — el archivo donde se registran los pendientes
era, él mismo, un pendiente.

**Por qué no lleva límite:** es append-only, y un pendiente **no se puede borrar porque el archivo
creció**. Recortarlo sería perder trabajo declarado.

**Por qué la rotación NO es anual aquí:** un pendiente de enero puede seguir abierto en diciembre.
La fecha no dice nada sobre su vigencia. **Lo que la dice es si está cerrado.**

| Regla | Cómo funciona |
|---|---|
| **Un pendiente CERRADO sale del archivo** | se mueve a `docs/archive/pendientes-<año>.md` con su fecha de cierre |
| **`memory/PENDIENTES.md` contiene SOLO lo abierto** | su tamaño mide la deuda real, no la historia |
| **La rotación la dispara el cierre**, no el calendario | ✅ un pendiente resuelto = una línea menos |

> ⭐ **El efecto que importa:** el tamaño de `memory/PENDIENTES.md` pasa a ser **una métrica útil**.
> Si crece, la deuda crece. Hoy no dice nada porque mezcla lo abierto con lo ya resuelto.

**Lo que `check-health` comprueba:**
```
🟡 PENDING FILE
   · closed items still living in PENDIENTES.md   ← should be archived
   · items with no status marker at all
```

#### Por qué "rotación anual" y no un límite, para los append-only

Una bitácora **tiene** que crecer: su valor es la historia. Ponerle un límite obligaría a borrar
evidencia — y de la evidencia forense salió el incidente del 21-jul que no estaba documentado.
**Se rota (cierra el año, abre otro), no se recorta.**

#### Lo que `check-health` añade por esta regla

```
🟡 SIZE
   · file over its declared type limit
   · file with no declared type          ← nobody knows what limit applies
   · MEMORY.md over 80 lines
   · append-only file with no yearly rotation
```

> **Este documento habría sonado la alarma al pasar de 800 líneas** — hace unas 1,500 líneas.

### 3.2-TER · ⭐⭐ EL CONTRATO DE `BLOQUE.md` — diseño preciso

> **Decisión (Brian, 2026-07-27):** *"archivo único por bloque, pero ese archivo debe estar muy bien
> diseñado, diseño preciso a detalle, porque ya que no vamos a ocupar muchos, el control debe ser
> más profundo."*

**Por qué archivo único y no siete** *(corrección medida)*:

| Evidencia | Lectura |
|---|---|
| `memory/RETOMAR.md` = 203 líneas, 7 secciones, **un archivo** | ✅ lo que **mejor funciona** de Mente OS · siempre se lee entero |
| La demo hoy = **5 archivos `DEMO_*.md`** + índice en memoria | 🔴 nadie sabe cuál abrir |
| Tier 1 completo ≈ 70 líneas | partir 70 líneas **no ahorra nada** y añade sitios que se desincronizan |

> **Regla de separación:** *un archivo se parte cuando **crece sin control**, no por categoría.*
> Por eso `docs/` existe (las cronologías crecen) y `contexto.md` solo se separa si supera su límite.

#### Régimen de completitud: PROGRESIVO con MÍNIMO DURO

| Momento | Exigencia | Por qué |
|---|---|---|
| **Al ABRIR** | solo **4 campos** (§A) | si abrir cuesta 10 campos, se trabaja **sin bloque** — y se pierde todo |
| **Durante** | se llena lo que se va sabiendo | un campo inventado es **peor** que uno vacío: parece información |
| **Al CERRAR** | **todo**, incluida la suficiencia | cerrar mal le cuesta a la **siguiente sesión**, que arranca ciega |

> **Asimetría deliberada: barato de abrir, caro de cerrar.** Es lo que ya se observa en el sistema:
> `memory/RETOMAR.md` es fácil de actualizar → está fresco. `memory/PENDIENTES.md` exige rigor → 240 KB ilegibles.

#### El archivo, sección por sección

**Orden = frecuencia de lectura.** Lo que se lee siempre va arriba.

> 🇺🇸 **Los nombres de sección van en inglés** (§0-BIS) — la IA lee este archivo en cada arranque.

| § | Section | Obligatorio | Límite | Valida | Por qué existe |
|---|---|---|---|---|---|
| **A** | **`Identity`** | 🔴 **al ABRIR** | 5 líneas | campo + formato + **ID único** | sin ID no hay resolución exacta → vuelve la inferencia |
| **B** | **`Scope` — IN / OUT** | 🔴 **al ABRIR** | 15 líneas | ambas listas no vacías | ⭐ **evita que la IA se expanda sola** — causa de *"no, así no iba"* |
| **C** | **`Connections`** | 🔴 **al ABRIR** | 10 líneas | los bloques citados **existen** | decide el lane (§5) · previene el fix-sobre-fix |
| **D** | **`Required standards`** | 🔴 **al ABRIR** | 8 líneas | las rutas existen | ⭐ **el estándar viaja CON el trabajo** — capa B contra el fallo del Método F |
| **E** | **`State`** | 🟡 al trabajar | **10 líneas** | actualizado ≤ 7 días | latido operativo · mitad del Tier 1 |
| **F** | **`Sub-blocks`** | 🟡 al trabajar | 20 filas | cada uno con pieza y estado | el grafo de propagación |
| **G** | **`Decisions`** | 🟡 al trabajar | — | **cada una con rationale** | el *porqué* que hoy muere con `/clear` |
| **H** | **`Friction log`** | 🟡 al trabajar | — | — | evolución de reglas (§8) |
| **I** | **`Checkpoints`** | 🟡 al trabajar | — | — | puntos de retorno |
| **J** | **`Context`** | 🟡 al trabajar | **≤80 (meta 50)** | tamaño · **no ser un log** | lo durable; el detalle largo → `docs/` |
| **K** | **`Closing`** | 🔴 **al CERRAR** | — | resumen + conexiones + suficiencia | herencia al siguiente bloque |

**Total con todo lleno: ~150 líneas.** Barato de leer entero.

#### Las 4 puertas del mínimo duro

```
   ABRIR UN BLOQUE — lo único que se exige
   ═══════════════════════════════════════════════════
   A · ID + intención (1 línea)     ¿qué es y cómo se llama?
   B · qué SÍ / qué NO        ⭐    ¿hasta dónde llego?
   C · conexiones                   ¿qué toco al tocarlo?
   D · estándares obligatorios ⭐    ¿con qué criterio se hace?
   ═══════════════════════════════════════════════════
   4 campos · ~2 minutos
```

> **Los 4 son exactamente los que HOY no existen en ningún sitio**, y su ausencia causó todos los
> problemas medidos: alcance perdido · expansión no declarada · fix-sobre-fix · estándar no leído.

#### Qué NO lleva el archivo (y dónde va)

| No va aquí | Va en | Por qué |
|---|---|---|
| Cronologías, logs de sesión | `docs/` | crecen sin control |
| El contenido de los estándares | `Alma/` · `Cerebro/` | **se apunta, no se copia** (regla madre) |
| Código, diffs | el repo | el bloque describe, no duplica |
| Estado de otros bloques | su propio bloque | aislamiento (§11.6) |

### 3.3 · EJEMPLO REAL — el bloque `demo` (en inglés, como será)

*(archivo único con hechos verificados de la demo. Secciones A-D = el mínimo duro.
🇺🇸 **En inglés porque la IA lo lee en cada arranque** — §0-BIS.)*

```markdown
# BLOCK · demo

<!-- ══ A · IDENTITY ══ required to OPEN · ≤5 lines ══ -->
id: blk-demo-2026-07
intent: turn the web demo from an MVP into a sellable product
status: active · lane: full-block · owner: brian
created: 2026-07-24 · updated: 2026-07-27

<!-- ══ B · SCOPE ══ required to OPEN · ≤15 lines ══ -->
## ✅ IN
- lib/demo/*.ts · components/demo/* · app/api/demo/*
- Neon DB `for3s_demo` (demo_* tables)
- Admin panel /for3s-admin

## ⛔ OUT
- DO NOT touch the For3s-OS agent (separate block, separate repo)
- DO NOT touch marca-personal/Mente/ (scope forbidden in CLAUDE.md)
- DO NOT change the API channel without opening its own block
- DO NOT deploy to Vercel without an explicit order from Brian

<!-- ══ C · CONNECTIONS ══ required to OPEN · ≤10 lines ══ -->
## Connections
- DEPENDS ON: blk-canal-api (consumes /v1/chat)
- DEPENDED ON BY: blk-panel-admin
- ISOLATED FROM: blk-entrenamiento
- 🔴 CRITICAL PIECE: lib/demo/userStore.ts → propagates to 5 files

<!-- ══ D · REQUIRED STANDARDS ══ required to OPEN · ≤8 lines ══ -->
## Required standards
- rules/rule-fix-not-patch.md          ← fixes in flight
- principles/expertise/dev-database.md     ← the DB is touched
- principles/expertise/dev-frontend.md     ← components are touched
- rules/case-dangerous-default.md      ← defaults are in play

<!-- ══ E · STATE ══ ≤10 lines · half of Tier 1 ══ -->
## State
phase: polishing to product
next: close sub-block 6 (jazz/mashe owners into the DB)
blockers: sub-block 5 depends on deciding the hosting
progress: 4/6 sub-blocks closed
updated: 2026-07-27

<!-- ══ F · SUB-BLOCKS ══ the propagation graph ══ -->
## Sub-blocks
| # | task | code piece | dependents | status |
|---|---|---|---|---|
| 1 | DB-only bridge, no env | lib/demo/instancias.ts | 2 | closed |
| 2 | single guard (12 copies→0) | lib/demo/session.ts | 3 | closed |
| 3 | brute-force protection | lib/demo/verificacion.ts | 1 | closed |
| 4 | round F0 U1-U6 | lib/demo/userStore.ts | 🔴 5 | closed |
| 5 | tests for the 5 critical paths | (no file yet) | 0 | blocked |
| 6 | jazz/mashe owners into the DB | lib/demo/allowedEmails.ts | 2 | active |

<!-- ══ G · DECISIONS ══ each one WITH its rationale ══ -->
## Decisions
- 2026-07-26 · default `hoteles` → `sin-tema`, NOT `general`.
  Rationale: `general` is a RESERVED name (the owner's private thread); as a
  default it would have routed guests into the owner's own space.
- 2026-07-26 · rollout order: senders first, strict receiver second.
  Rationale: the other way around breaks everything that doesn't send the field yet.

<!-- ══ H · FRICTION ══ escalates to Brian on close ══ -->
## Friction log
- (none recorded)

<!-- ══ I · CHECKPOINTS ══ -->
## Checkpoints
- 2026-07-26 · 1c54a49 · explicit topic
- 2026-07-26 · 793e858 · heartbeat + TTL

<!-- ══ J · CONTEXT ══ ≤80 lines · CURATED, not a log ══ -->
## Context
Site repo ElBrAyAn1967/For3s (≠ the agent's) · Neon DB · main at 793e858.
DEMO_ENC_KEY rotated and unified local=Vercel (2026-07-26).
Full timeline of the session → docs/session-2026-07-26.md

<!-- ══ K · CLOSING ══ required to CLOSE ══ -->
## Closing
(pending — the block is still active)
```

**Lo que este archivo hace y hoy no existe en ningún sitio:**

| Sección | Lo que evita |
|---|---|
| **B · OUT** | que la IA se expanda sola o reconstruya el alcance por inferencia |
| **C · critical piece** | el fix-sobre-fix: `userStore.ts` y sus 5 dependientes quedan **declarados** |
| **D · required standards** | que el estándar exista y nadie lo lea (el fallo del Método F) |
| **G · rationale** | que el *porqué* muera con el `/clear` |

> ⭐ **Prueba de suficiencia (§11.4):** con leer **A-E** —unas 60 líneas— se puede reiniciar con
> seguridad: qué se construye, qué NO se toca, de qué depende, con qué criterio, en qué fase va y
> qué lo bloquea. **Eso es ser dueño del contexto.**

### 3.4 · Estados y concurrencia

- **Estados:** `activo` · `bloqueado` · `cerrado`
- **Varios bloques pueden estar en proceso, pero solo se ejecuta UNO a la vez.**
- **Sub-bloques:** el bloque grande **no avanza** hasta cerrar los pequeños.
- **Al cerrarse** (decisión de Brian): *"se archiva como completado y está detallado todo como
  experiencia de memoria"* → el bloque cerrado **no muere: se vuelve fuente consultable**.

---

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (the entry point and index) ·
`rules/contract-block.md` (the enforceable contract this section describes) ·
`rules/block-lifecycle.md` · `blocks/archive/split-architecture_2026-07/BLOCK.md`.
