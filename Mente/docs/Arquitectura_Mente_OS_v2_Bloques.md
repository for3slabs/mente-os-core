# 🏗️ ARQUITECTURA — Mente OS v2: el sistema de BLOQUES

**Status:** current · **Type:** architecture · **Updated:** 2026-08-06 · **Owner:** brian
**Exempt:** size, split-signal · FUENTE DE VERDAD — decisión de Brian 2026-08-05: *"las fuentes de verdad no importa el tamaño"*. 46 documentos la citan para RESOLVER; partirla inventaría una segunda autoridad.

## Purpose

La FUENTE DE VERDAD estructural de Mente OS v2: qué es un bloque, qué secciones lleva, cómo se
abre y se cierra, y cómo se relacionan las piezas. **46 documentos la citan para RESOLVER**, no
para consultar — cuando dos documentos se contradicen, manda este.

⛔ **FUENTE DE VERDAD — EXENTA DEL TECHO DE TAMAÑO, POR DECISIÓN DE BRIAN (2026-08-05).**
*"Déjalo intacto como en v1. Es fuente de verdad, y las fuentes de verdad no importa el tamaño."*
**No se parte, no se resume, no se poda.** 46 documentos la citan para RESOLVER, no para consultar;
partirla inventaría una segunda autoridad y *"¿cuál de las dos manda?"* es justo la ambigüedad que
una fuente de verdad existe para eliminar. Criterio y prueba: `principles/expertise/doc-structure.md`
§2.1 (⛔ la única excepción). ⚠️ `bin/check-health` seguirá marcándola 🟡: **es esperado.**

> **Diseño de:** Brian López · **Redacción:** sesión 2026-07-27 · **Capa:** Cuerpo (el CÓMO)
> **Estatus:** 📐 **ESPECIFICACIÓN CERRADA EN DISEÑO — NO CONSTRUIDA.**
> Pendiente de Ronda F0 (evaluación) y aprobación explícita para construir.
> **El por qué:** `principles/vision-mente-os-v2.md`
>
> **Regla de lectura:** las citas en bloque son palabras literales de Brian. **Son el contrato**
> (Método F §1: "captura la visión en palabras del propio Brian — son el contrato").

---

## ÍNDICE

| § | Sección | Incluye ejemplo |
|---|---|---|
| 0-BIS | ⭐⭐ **POLÍTICA DE IDIOMA** — instrucciones en 🇺🇸 · pensamiento en 🇪🇸 | 📋 vocabulario canónico |
| 1 | Principio rector | |
| 2 | El flujo de arranque | |
| 3 | **El BLOQUE — definición y anatomía** | 📊 §3.1-bis los 2 grafos · ✅ §3.1-ter **anidamiento (máx 3)** · ⭐ §3.2-bis límites · ⭐⭐ **§3.2-TER el CONTRATO** · ✅ §3.3 plantilla `DEMO` |
| 4 | Los 3 ENCARGADOS | |
| 5 | **Los 3 CARRILES de fricción** | ✅ §5.1 asignación de carril |
| 6 | **El ciclo de vida — EL PROCESO COMPLETO** | 📊 §6.1 flujo entero · ⭐ §6.1-bis **cierre en 8 pasos** · 📊 §6.2 dónde vive el contexto |
| 7 | **BLOQUE MEJORADO — anti fix-sobre-fix** | ✅ §7.1 mal vs bien resuelto |
| 8 | **Evolución de reglas — el roce** | ✅ §8.1 roce, excepción y 3-roces |
| 9 | El sistema de EXPERTISE | |
| 10 | **El sistema de APRENDIZAJE de errores** | ✅ §10.3 de error a forma aprendida · ✅ §10.4 **cómo se consulta** |
| 11 | **Contexto y caché por bloque** | ⭐ §11.3 **tiers** · §11.4 **suficiencia** · §11.5 **resolución determinista** · §11.6 aislamiento |
| 12 | **Estructura de carpetas** | 📊 §12.0 árbol completo · ✅ §12.1 **la nueva CONVIVE** |
| 12-BIS | **INVENTARIO DE ARCHIVOS** — qué se crea, qué se reusa | 📋 tablas A-G |
| 12-TER | ⭐ **LOS VALIDADORES** — comprueban · completan · **se auto-auditan** | 🔧 6 scripts · §12-T.1 completar · §12-T.2 recibo · **§12-T.3 check-health** |
| 12-QUATER | ⭐⭐ **CÓMO SE GARANTIZA QUE UN ARCHIVO SE LEA** — 4 capas + 3 puertas cerradas | 📊 diagrama + ejemplo |
| 12-QUINQ | ⭐⭐⭐ **EL VEREDICTO DE CALIDAD — QA dentro de Mente OS** | 📊 capa medible + 6 dimensiones de criterio |
| 12-SEPT | ⭐⭐⭐ **HIGIENE DE CONFIGURACIÓN** — secretos · por qué · **un mecanismo una entrada** · portabilidad | 📋 4 reglas medidas |
| 12-SEXIES | ⭐⭐ **LA VOZ — cómo se comunica Mente OS** | 📋 8 reglas negativas · Encargado 0 |
| 13 | Sistemas transversales | |
| 14 | Migración por demanda | |
| 15 | **Lo que NO se toca** | |
| 16 | Principios de diseño no negociables | |
| 16-BIS | **Incorporaciones de referencia externa** (ya integradas arriba) | 📋 9 incorporaciones |
| 17 | Pendientes para la Ronda F0 | |

---

## 0-BIS · ⭐⭐ POLÍTICA DE IDIOMA *(decidido 2026-07-27)*

> **Brian:** *"cuando tengamos que poner instrucciones de texto, todo será en inglés — inglés de
> Estados Unidos."*

**La regla de reparto:**

| Qué | Idioma | Por qué |
|---|---|---|
| **Todo lo que la IA lee como INSTRUCCIÓN** | 🇺🇸 **inglés (US)** | la IA lo resuelve con precisión; es el idioma de todas las convenciones sobre las que se apoya |
| **El pensamiento de Brian** | 🇪🇸 **español** | es su criterio; forzarlo a otro idioma le quita matiz |

### 0-BIS.1 · Qué va en INGLÉS (US)

| Archivo | Tipo |
|---|---|
| `CLAUDE.md` + el enrutador (capa A) | instrucción · se inyecta |
| `~/.claude/output-styles/for3s.md` | instrucción · **el mayor peso del sistema** |
| `base-rules.md` | instrucción |
| `principles/owner-0-voice.md` · `owner-1-docs` · `owner-2-dev` · `owner-3-validation` | instrucción |
| `principles/expertise/{database,backend,frontend}.md` | instrucción |
| `rules/contract-*.md` · `rules/rule-*.md` · `rules/qa-dimensions.md` | instrucción |
| `rules/case-*.md` | instrucción (se inyecta antes de trabajar) |
| **`blocks/active/*/BLOCK.md`** ⭐ | **instrucción — la IA lo lee en cada arranque** |
| Nombres de archivos y carpetas | `rules/NAMING_CONVENTION.md` |
| Salida de los validadores (`bin/*`) | instrucción · mensajes de error |
| Commits, changelog público | ya era la práctica |

### 0-BIS.2 · Qué se queda en ESPAÑOL

`Vision_Mente_OS_v2` · `Plan_Implementacion` · los análisis comparativos · `memory/RETOMAR.md` ·
`Bitacora_Progreso` · `Registro_Conversaciones` · las memorias · **y las conversaciones con Brian**.

> **El criterio de corte:** *¿esto lo lee la IA para SABER QUÉ HACER, o lo lee un humano para
> ENTENDER QUÉ PASÓ?* Lo primero va en inglés. Lo segundo en español.

### 0-BIS.3 · ⭐ El vocabulario canónico — traducido

| Español (v1) | 🇺🇸 **Inglés (v2)** |
|---|---|
| bloque · sub-bloque | **block · sub-block** |
| encargado 0/1/2/3 | **owner-0 (voice) · owner-1 · owner-2 · owner-3** |
| carril: directo · tarea · bloque-completo | **lane: direct · task · full-block** |
| límites: qué SÍ / qué NO | **scope: IN / OUT** |
| roce (con una regla) | **friction** |
| veredicto de calidad | **quality verdict** |
| prueba de suficiencia | **sufficiency check** |
| fix ≠ parche | **fix ≠ patch** |
| propagación · dependientes | **propagation · dependents** |
| punto de guardado | **checkpoint** |
| estándar obligatorio | **required standard** |
| validador | **validator** |
| puerta cerrada | **closed gate** |
| recibo de aprobación | **approval receipt** |

> ⚠️ **Un solo término por concepto.** Prohibido mezclar (`lane` en un sitio y `carril` en otro):
> es exactamente la anarquía que el v2 existe para eliminar.

### 0-BIS.4 · Inglés de EE.UU., no británico

`behavior` (no *behaviour*) · `organize` (no *organise*) · `analyze` (no *analyse*) ·
`center` (no *centre*) · `license` (sustantivo y verbo).
**Fechas:** ISO `2026-07-27` siempre — evita la ambigüedad MM/DD vs DD/MM.

---

## 1 · PRINCIPIO RECTOR

> **"ESTANDARIZAR, TRAZABILIZAR, SABER DÓNDE ESTÁ LA DATA. CONTROLAR LOS PROCESOS DE LA IA.
> EJECUTA INSTRUCCIONES CLARAS, NO LO DEJAMOS QUE LO HAGA ÉL SOLO."**

Mente OS **documenta bien** — eso se conserva íntegro. Lo que le falta es **gobernar la ejecución**.

**Propósito declarado (Brian, 2026-07-27):**
> *"Es para que trabajes mejor con reglas de personas que ya saben del tema y son expertas, y que
> también tengan el mismo criterio."*

Dos consecuencias de diseño:
- Las reglas **no son opinión de la IA**: son criterio experto codificado.
- El sistema es **compartible**: cualquiera que entre trabaja con el mismo criterio.

---

## 2 · EL FLUJO DE ARRANQUE

Toda sesión, **con cualquier IA**, sigue este orden. La portabilidad es requisito, no aspiración:
el protocolo no puede depender de Claude Code.

```
┌─ 1 · REGLAS INDISPENSABLES ──────────── lo mínimo, antes que nada
├─ 2 · CONTEXTO de lo que se estaba haciendo
├─ 3 · ÚLTIMO REALIZADO ───────────────── RETOMAR.md
├─ 4 · DETERMINA EL ARQUITECTO ────────── ¿qué perfil pide esta tarea?
├─ 5 · ELIGE LAS HERRAMIENTAS
└─ 6 · ABRE / CREA EL BLOQUE DE TRABAJO
```

**Regla transversal:**
> *"Las funciones o acciones SIEMPRE son en bloques."*

Nada se ejecuta fuera de un bloque.

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
| **`Arquitectura_Mente_OS_v2_Bloques.md`** (este) | **2,347** | ❌ 🔴 |
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

## 4 · LOS 3 ENCARGADOS

> **Regla dura:** *"Van a existir más estándares pero **nunca puede ser mayor a 3**, porque si no
> el sistema no entiende."*
> *"No tienen nivel de importancia: **los 3 encargados tienen el mismo nivel** entre ellos."*

Los tres se aplican **simultáneamente** sobre el bloque. Cada uno es un estándar con sus propias
reglas, subdivisiones y manejos específicos.

### Encargado 1 · Estilo / formato de documentación
- Define la forma de todo documento y de todo plan.
- **Todo plan nace con apartados base por defecto.**
- Al completarse el plan, **el sistema puede agregar apartados** si el panorama resultó distinto
  al previsto. → *El contrato es un piso, no un techo.*

### Encargado 2 · Desarrollo
- Recibe el plan y **debe entender qué se le pide**.
- Elige **backend o frontend**; implementa uno y, al terminar, el otro.
- Tiene **estándares propios para backend y para frontend** (§9, el sistema de expertise).
- **Poder de veto con retroceso:** si el plan no cumple sus criterios, **lo devuelve al paso
  anterior a mejorarse**.

### Encargado 3 · Validación del flujo funcional
- Verifica **todo el comportamiento del bloque: que nada quede suelto**.
- Que lo que existe en código **funcione y esté conectado**.
- Es el último en actuar dentro del ciclo.

**⭐ Sus TRES criterios de cierre (ninguno es opcional):**

| # | Criterio | Pregunta que responde |
|---|---|---|
| 1 | **Funcional** | ¿lo que existe **funciona y está conectado**? ¿nada quedó suelto? |
| 2 | **De suficiencia** | ¿las secciones A-E bastan para **reiniciar con seguridad**? (§11.4) |
| 3 | ⭐⭐ **Veredicto de calidad** | **capa 1 medible** + **capa 2 de criterio** (§12-QUINQUIES) |

> **Regla madre del Encargado 3:** 🚫 **no declara "está bien" — REPORTA LA MEDICIÓN.**
> Si el criterio 2 falla, el bloque no se cierra aunque el código funcione.
> Si el 3 sale 🔴, el bloque **puede** cerrarse pero **marcado como MVP con su deuda listada** —
> lo que no se puede es cerrarlo diciendo "está bien".

---

## 5 · LOS 3 CARRILES DE FRICCIÓN ✅ *(decidido 2026-07-27)*

**Problema que resuelve:** si toda tarea pasa por los 3 encargados, el sistema se vuelve
insoportable y se abandona. **Un estándar que estorba se deja de usar** — y volveríamos al inicio.

| Carril | Cuándo | Recorrido |
|---|---|---|
| **Directo** | cambio trivial: un texto, un color, un typo | solo **Validación** (¿no rompió nada?) |
| **Tarea** | un sub-bloque suelto, sin diseño nuevo | **Desarrollo → Validación** |
| **Bloque completo** | algo nuevo, o que toca varias piezas | **Documentación → Desarrollo → Validación**, con retroceso |

### ⭐ La regla que elige el carril — NO la elige la IA

> **El carril lo decide la PROPAGACIÓN, no el juicio de la IA.**
> Si el cambio toca algo con dependencias declaradas, **sube automáticamente a bloque completo**.

**Por qué:** esto evita que la IA declare "esto es trivial" y se equivoque — que es exactamente
cómo nació el `userStore.ts × 21`. La decisión sale del grafo, no de una estimación.

### 5.1 · EJEMPLOS de asignación de carril *(casos reales de la demo)*

| Petición | Carril | Por qué |
|---|---|---|
| *"cambia el texto del botón a 'Entrar'"* | **Directo** | sin dependencias declaradas |
| *"el copy del error de cupo no se entiende"* | **Directo** | cadena de texto, no toca lógica |
| *"añade un console.log para depurar"* | **Directo** | no altera comportamiento |
| *"guarda la API key en la instancia real, no en el kind de la cookie"* | 🔴 **Bloque completo** ← *aunque parezca tarea* | `userStore.ts` tiene 5 dependientes declarados. **Este es el caso exacto que produjo el fix-sobre-fix:** se trató como tarea, se arregló un sitio, y 4 commits después hubo que hacer *"barrido completo del patrón"* |
| *"añade un campo `nombre` a demo_users"* | **Bloque completo** | toca BD → propaga a todo lo que lee la tabla |
| *"pon try/catch en esta función suelta"* | **Tarea** | pieza aislada, sin dependientes |
| *"conecta la demo con un proveedor de pagos"* | **Bloque completo** | pieza nueva + integración externa |

> ⭐ **La fila roja es la lección entera del sistema.** Bajo el criterio de hoy, "guardar la key en
> la instancia real" suena a tarea pequeña. El grafo dice otra cosa: `userStore.ts` es un nodo con
> 5 dependientes. **El carril lo decide el grafo, no la apariencia de la petición.**

---

## 6 · CICLO DE VIDA DE UN BLOQUE

### 6.1 · EL PROCESO COMPLETO — de "hola" a bloque cerrado

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  A · ARRANQUE (cualquier IA · ~38-40K tokens)                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
   ┌───────────────────────┐
   │ 1 REGLAS BASE         │  automático · lo mínimo indispensable
   ├───────────────────────┤
   │ 2 CONTEXTO            │  qué se estaba haciendo
   ├───────────────────────┤
   │ 3 RETOMAR.md          │  lo último realizado
   ├───────────────────────┤
   │ 4 ¿QUÉ ARQUITECTO?    │  ¿qué perfil pide esta tarea?
   ├───────────────────────┤
   │ 5 HERRAMIENTAS        │
   └──────────┬────────────┘
              ▼
       ┌─────────────────────────────┐
       │ ¿Hay BLOQUE ACTIVO?         │
       └──────┬───────────────┬──────┘
         SÍ   │               │   NO
              ▼               ▼
     ┌─────────────────┐  ┌──────────────────┐
     │ CARGAR bloque   │  │ CREAR bloque     │
     │ ⚠ si falta algo │  │ · intención      │
     │   DECIRLO en    │  │ · límites SÍ/NO  │
     │   voz alta      │  │ · conexiones     │
     │   (no inferir)  │  │ · sub-bloques    │
     └────────┬────────┘  └────────┬─────────┘
              └────────┬───────────┘
                       ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  B · ELECCIÓN DE CARRIL — la decide la PROPAGACIÓN, no la IA                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
              ┌──────────────────────────────────────┐
              │ ¿Lo que se toca tiene DEPENDIENTES   │
              │  declarados en el grafo?             │
              └───────┬──────────────────────┬───────┘
                  SÍ  │                      │  NO
                      ▼                      ▼
            ┌──────────────────┐   ┌──────────────────────┐
            │ BLOQUE COMPLETO  │   │ ¿diseño nuevo?       │
            │ (los 3 encargados)│   └───┬──────────────┬───┘
            └────────┬─────────┘    NO  │              │ SÍ
                     │                  ▼              ▼
                     │           ┌────────────┐  ┌──────────────┐
                     │           │  DIRECTO   │  │    TAREA     │
                     │           │ solo valida│  │ Des.→Valida  │
                     │           └──────┬─────┘  └──────┬───────┘
                     ▼                  │               │
╔═══════════════════════════════════════════════════════════════════════════════╗
║  C · EL CICLO DE LOS 3 ENCARGADOS (mismo nivel · aplican a la vez)             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                     │
        ┌────────────▼─────────────┐
        │  ¿QUÉ SE QUIERE HACER?   │
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐
        │  SE ANALIZA              │
        └────────────┬─────────────┘
                     ▼
        ┌──────────────────────────┐      ¿existe conexión con otro bloque?
        │  SE COMPARA con bloques  │◄──── evita duplicar
        └────────────┬─────────────┘      detecta propagación
                     ▼
   ╭─────────────────────────────────────╮
   │ ① PLAN DE IMPLEMENTACIÓN            │  ENCARGADO 1 · documentación
   │    apartados base por defecto       │  (al final puede añadir más
   │                                     │   si el panorama cambió)
   ╰──────────────────┬──────────────────╯
                      ▼
   ╭─────────────────────────────────────╮
   │ ② ANÁLISIS DEL PLAN                 │  ENCARGADO 2 · desarrollo
   │    ¿cumple mis criterios?           │
   ╰──────┬───────────────────────┬──────╯
     cumple│                      │NO cumple
          │                       │
          │        ⟲ RETROCESO ───┘
          │        regresa a ① a mejorarse
          ▼
   ╭─────────────────────────────────────╮
   │ ③ DESARROLLO EJECUTA                │  backend O frontend
   │    uno primero, luego el otro       │  ← estándares por disciplina
   │    ▸ cada iteración = PUNTO DE      │    (sistema de expertise)
   │      GUARDADO del bloque            │
   ╰──────────────────┬──────────────────╯
                      ▼
   ╭─────────────────────────────────────╮
   │ ④ VALIDACIÓN DEL FLUJO              │  ENCARGADO 3
   │    que NADA quede suelto            │
   │    que lo que existe funcione       │
   │    y esté CONECTADO                 │
   ╰──────┬───────────────────────┬──────╯
     pasa │                       │ no pasa
          │                       └──⟲ vuelve a ③
          ▼
        ┌──────────────────────────────┐
        │ ¿QUEDAN SUB-BLOQUES ABIERTOS?│
        └────┬────────────────────┬────┘
         SÍ  │                    │ NO
             │                    ▼
             │       ╔═══════════════════════════════════════════════════════════╗
             │       ║  D · CIERRE                                               ║
             │       ╚═══════════════════════════════════════════════════════════╝
             │         ┌────────────────────────────────┐
             │         │ BLOQUE CERRADO → ARCHIVADO     │
             │         │  · resumen detallado           │
             │         │  · conexiones con otros bloques│
             │         │  · experiencia de memoria      │
             │         │  · roces → propuestas a Brian  │
             │         └───────────────┬────────────────┘
             │                         ▼
             │              ┌─────────────────────┐
             │              │ CONSULTABLE por los │
             │              │ próximos bloques    │
             │              └─────────────────────┘
             │
             └──⟲ el bloque grande NO AVANZA
                  hasta cerrar los pequeños
```

### 6.1-bis · ⭐ EL CIERRE ES UN PROCEDIMIENTO, no una intención

**El fallo que corrige, medido:** 5 de 11 sesiones **nunca se registraron** · 8 auto-compactaciones
sin revisar. La regla *"sin registro no hay /clear"* existe desde el 14-jul y **se incumplió el 45%
de las veces** — porque dependía de acordarse.

```
   CERRAR UN BLOQUE — pasos fijos, en orden
   ═══════════════════════════════════════════════════════════
   1. CONSOLIDAR contexto.md      → curado a ≤80 líneas
                                    (el detalle largo se muda a docs/)
   2. CURAR decisiones            → cada una con su rationale
   3. RESOLVER roces              → suben a Brian como propuestas
   4. VERIFICAR SUFICIENCIA       → ⭐ ¿el Tier 1 basta para reiniciar?
                                       NO ─▶ el bloque NO se cierra
   5. ESCRIBIR RESUMEN            → qué se hizo · qué se aprendió
   6. DECLARAR CONEXIONES         → qué bloques quedan afectados
   7. ARCHIVAR                    → _archivados/<BLOQUE>_<fecha>/
   8. REGENERAR índice y estados  → 🤖 automático, nunca a mano
```

> **Regla dura:** *consolidar ANTES del cierre, no después.* Un cierre que depende de que alguien
> se acuerde al final es el cierre que ya falló 5 de 11 veces.

### 6.2 · DÓNDE VIVE EL CONTEXTO (y por qué `/clear` deja de doler)

```
        HOY                                    v2
   ────────────────                    ────────────────────

   ┌──────────────┐                    ┌──────────────┐
   │ CONVERSACIÓN │ ← fuente           │ CONVERSACIÓN │ ← caché
   │              │   de verdad        │              │   desechable
   │ · alcance    │                    └──────┬───────┘
   │ · criterio   │                           │ lee/escribe
   │ · grafo      │                           ▼
   └──────┬───────┘                    ┌──────────────────┐
          │                            │  BLOQUE (disco)  │ ← fuente
        /clear                         │  · límites SÍ/NO │   de verdad
          │                            │  · decisiones    │
          ▼                            │  · conexiones    │
      ✗ TODO MUERE                     │  · guardados     │
                                       └────────┬─────────┘
   RETOMAR sobrevive pero                       │
   solo dice "dónde                           /clear
   quedamos", no "qué                           │
   estábamos construyendo"                      ▼
                                          ✓ NADA SE PIERDE
   → la IA RECONSTRUYE                      se recarga del bloque
     por inferencia
     y suena segura                       ⚠ si el bloque está
   → "no, así no iba"                       incompleto: SE DICE,
                                             no se infiere
```

---

## 7 · BLOQUE MEJORADO — la regla anti fix-sobre-fix

> *"¿Qué pasa si a un bloque se le implementa un fix o mejora? **No se crea un código o solución
> arriba solo para tapar el problema.** Se evalúa la construcción; a partir de saber todo el
> contexto del código se establece cómo solucionar el error. Si se tiene que pensar o hacerlo por
> otro medio, está bien. **Lo que no está bien es tener decenas de código sin orden**, porque
> tendremos problemas de redundancia."*

### Procedimiento obligatorio ante un fix

1. **NO** escribir la solución encima.
2. **Evaluar la construcción** existente.
3. **Conocer TODO el contexto del código** antes de decidir.
4. **Elegir la solución real** — aunque implique otro camino.
5. El bloque debe contener **la información necesaria para conectarse con otros bloques**.
6. Esa es **la secuencia a repetir e iterar con el humano**.

### Justificación medida (la demo)

| Evidencia | Dato |
|---|---|
| Commits que son fixes | **25 de 60 (42%)** |
| `userStore.ts` tocado | **21 veces** |
| `for3sChat.ts` tocado | 14 veces |
| Prueba textual | *"barrido completo del patrón cookie kind ≠ instancia real"* llegó **4 commits después** de *"guardar la API key en la instancia REAL"* → se arregló el síntoma, no la causa, y hubo que volver |

### 7.1 · EJEMPLO — el mismo bug, mal y bien resuelto

**Caso real: "la API key se guarda en el sitio equivocado".**

```
❌ COMO SE HIZO (fix-sobre-fix)
   1. Bug reportado: la key del dueño se guarda mal
   2. Se busca DÓNDE falla → un archivo
   3. Se corrige AHÍ                          → commit d5dc778
   4. Aparece otro síntoma parecido           → commit 6310bcf
   5. Aparece otro más                        → commit 5326bb6
   6. Se descubre que el patrón estaba en TODOS lados
   7. "barrido completo del patrón"           → commit b61e3d0
   ⤷ 4 commits para un solo problema · userStore.ts terminó con 21 toques
```

```
✅ COMO LO HARÍA EL BLOQUE MEJORADO
   1. Bug reportado: la key del dueño se guarda mal
   2. NO tocar nada todavía
   3. EVALUAR LA CONSTRUCCIÓN:
      ¿de dónde sale "kind"? ¿quién más lo usa para identificar la instancia?
      → grep: aparece en 6 archivos
   4. ENTENDER EL CONTEXTO COMPLETO:
      la causa NO es "este archivo guarda mal"
      la causa es "kind (cookie) se usa como si fuera la instancia real"
   5. DECIDIR LA SOLUCIÓN REAL:
      un punto único que resuelva la instancia real → los 6 sitios lo usan
   6. UN cambio, 6 sitios corregidos, causa eliminada
   ⤷ 1 commit · el patrón no puede reaparecer
```

**La diferencia no es esfuerzo: es el paso 3.** El fix-sobre-fix pregunta *"¿dónde falla?"*.
El bloque mejorado pregunta *"¿por qué existe este fallo y dónde más vive?"*.

> Este mismo criterio ya está probado en Mente OS: `memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` §2
> — *"el código suele decir de dónde viene. Antes de teorizar: grep + leer el comentario +
> contrastar con Mente OS. En 3 comandos se supo el origen exacto."*

---

## 8 · EVOLUCIÓN DE REGLAS — el protocolo del roce ✅ *(decidido 2026-07-27)*

> **Principio:** *"NO EXISTEN REGLAS INMUTABLES, EXISTEN APUNTADORES A REGLAS. ESTÁNDARES
> MEJORANDO CON CRITERIOS DEL USUARIO."*

**Qué hace la IA cuando una regla le estorba a mitad del trabajo:**

```
1. LA CUMPLE                  ← aunque le parezca mal
2. REGISTRA EL ROCE           ← en el bloque: qué regla · qué quería hacer · por qué chocó
3. SIGUE TRABAJANDO           ← nunca se detiene el trabajo
4. AL CERRAR EL BLOQUE        ← los roces llegan JUNTOS como propuestas de mejora
5. BRIAN DECIDE               ← si aprueba: la regla cambia con fecha, motivo y autor
```

**⚠️ Única excepción — se interrumpe de inmediato:** si cumplir la regla causa **daño real**
(romper producción · exponer un secreto · perder datos), se para y se pregunta.

**Por qué así:**
- Si la IA pregunta cada vez que algo estorba → Brian se vuelve **cuello de botella**.
- Si la IA cambia reglas por su cuenta → en un mes **las reglas son suyas otra vez** = vibecoding.
- Registrar y acumular hace que el sistema **aprenda sin vigilancia constante**.

**⭐ Conexión con el aprendizaje (§10):** el roce con una regla **es información**. Si una regla
estorba tres veces, **la regla está mal** — y el sistema debería detectarlo solo.

### 8.1 · EJEMPLOS de roce *(cómo se ve en la práctica)*

**Roce normal — se registra y se sigue:**
```markdown
## Roces con reglas
- 2026-07-27 · regla: "server-primero, push solo con orden explícita"
  quería: pushear el fix del heartbeat de una vez (ya verificado, urgente)
  choqué con: la regla exige orden explícita de Brian
  qué hice: CUMPLÍ la regla, dejé el commit sin push, seguí trabajando
  propuesta: ¿un carril rápido para fixes ya verificados? (decide Brian al cerrar)
```

**Excepción — se interrumpe de inmediato:**
```markdown
- 2026-07-26 · regla: "cero hardcodeo, todo de ENV"
  quería: leer DEMO_ENC_KEY de una constante para probar rápido
  choqué con: cumplir la regla implicaba usar el fallback...
  ⚠️ PARÉ Y PREGUNTÉ — el fallback tapaba que local ≠ Vercel.
     Seguir habría dejado la demo rota en producción sin que se notara.
```

**Detección automática de regla mala (3 roces):**
```
regla "X" registró roce en: bloque DEMO · bloque PANEL · bloque TRACE
→ 🔔 3 roces en bloques distintos = la regla estorba de forma sistemática
→ se eleva a Brian como REVISIÓN DE REGLA, no como propuesta suelta
```

---

## 9 · EL SISTEMA DE EXPERTISE

### 9.1 · Origen del criterio ✅ *(definido por Brian 2026-07-27)*

> *"Del criterio del experto: él ya ha manejado el tema con las personas, pero **va a diseñar esos
> criterios y estándares** para que se puedan ocupar en Mente OS."*

**Reparto de responsabilidades, sin ambigüedad:**

| Quién | Qué aporta |
|---|---|
| **Brian** | **el criterio** — diseñado desde su experiencia real con expertos |
| **La IA** | **la forma** — extraer, estructurar y dejarlo aplicable por el sistema |

> **La IA NO inventa el criterio.** Ese es el error que produjo el estado actual
> (*"todo está hecho como la IA quiso"*).

### 9.2 · Qué debe cubrir

El Encargado 2 necesita estándares por disciplina. Lo que el Método F **no cubre** hoy y aquí debe
existir:

- Diseño de datos previo (esquema, normalización, contratos)
- Estructura de carpetas y archivos
- Protocolos e interfaces entre piezas
- Detección de duplicación
- Convenciones de nombres
- Cuándo un archivo debe existir y cuándo no

**Como mínimo:** un cuerpo de criterio para **backend**, otro para **frontend**, otro para
**base de datos**.

---

## 10 · EL SISTEMA DE APRENDIZAJE DE ERRORES

> **Brian, 2026-07-27:** *"Tenemos que evaluar cómo hacer que esos errores no solo sean errores,
> sean forma que ya aprendió, o ver la forma de mejorar este apartado."*

### 10.1 · El precedente que ya funcionó

`memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` convirtió un error real en **método reutilizable con
checklist**: síntoma → origen → el error que casi se comete → la lección como regla → checklist
para la próxima vez.

**Salió bien, pero fue un accidente feliz.** Lo que falta es que sea **sistemático**.

### 10.2 · Las tres fuentes de aprendizaje

| Fuente | Qué produce |
|---|---|
| **Errores cazados** | un caso reutilizable con checklist |
| **Roces con reglas** (§8) | propuesta de mejora de la regla |
| **Bloques archivados** | experiencia consultable (*"detallado todo como experiencia de memoria"*) |

### 10.3 · EJEMPLO — de error suelto a forma aprendida

**El recorrido completo con un caso real (el default `hoteles`):**

```
① ERROR DETECTADO
   Brian: "no sé de dónde viene este hoteleria, no entiendo"

② SE RASTREA (no se teoriza)
   grep → api_channel.py: TEMA_DEFAULT = "hoteles"  # fase Incubathon
   El comentario dice el origen. 3 comandos, causa exacta.

③ SE INTENTA UN FIX... Y BRIAN LO CAZA
   Propuesta: cambiar default a "general" (parecía neutro)
   Brian: "general únicamente es para los dueños... eso está mal"
   → habría mandado invitados al hilo PRIVADO del dueño

④ SE EXTRAE LA REGLA (aquí nace el aprendizaje)
   ⭐ "Un default NUNCA debe apuntar a algo que tenga dueño o
      significado reservado. El default es un cajón neutro."

⑤ SE VUELVE CONSULTABLE
   → Cuerpo/CASO_Default_Peligroso_Tema_Hilo.md + checklist de 7 pasos
   → memoria feedback_default_nunca_apunta_a_algo_con_dueno

⑥ SE APLICA LA PRÓXIMA VEZ
   Antes de elegir CUALQUIER default: "¿este nombre significa algo
   para alguien?" Si sí → otro.
```

**Lo que hoy falla es el paso ⑥.** Los pasos ① a ⑤ ya ocurrieron y quedaron bien escritos.
Pero **nada garantiza que se consulte** antes del próximo default. Un aprendizaje que no se
consulta **no es aprendizaje: es un archivo**.

> **Por eso el sistema de aprendizaje no es "escribir más casos" — es asegurar que el caso
> LLEGUE al bloque que lo necesita.** El Encargado 2 debería recibir los casos aplicables a su
> disciplina antes de empezar, no después de romper algo.

### 10.4 · ✅ CÓMO SE CONSULTA EL APRENDIZAJE *(decidido 2026-07-27)*

> **El problema (§10.3):** los pasos ① a ⑤ ya funcionan — el caso se escribe bien. **Falla el ⑥:
> que se consulte la próxima vez.** Un aprendizaje que no se consulta no es aprendizaje: es un archivo.

**Decisión: EL MISMO MECANISMO QUE LOS ESTÁNDARES.** No se inventa uno nuevo.

```
   1 · EL BLOQUE LOS DECLARA        sección §D de BLOQUE.md
       ## Estándares obligatorios
       - Alma/expertise/base_datos.md          ← estándar
       - rules/case-dangerous-default.md  ← ⭐ CASO
                    ↓
   2 · EL HOOK LOS INYECTA          antes de editar (capa D, §12-QUATER)
       "vas a elegir un default → aquí está el caso que ya te mordió"
                    ↓
   3 · EL VALIDADOR LO COMPRUEBA    al cerrar
       ¿se aplicó lo declarado?
```

**Por qué reusar el mecanismo y no crear otro:**
- Los casos **son estándares**, solo que nacidos de un error propio en vez de del criterio previo.
- Un segundo mecanismo sería **otro sitio donde algo se puede omitir** — justo lo que hay que evitar.
- Reusa las 4 capas ya decididas: **el caso viaja CON el trabajo**, no vive en un índice general.

**Sigue pendiente de definir en la Ronda F0:**
- ¿Cuándo un error **merece** convertirse en caso? (no todos lo merecen)
- ¿Cómo se detecta que una regla estorbó **3 veces** y debe revisarse? (§8.1)

---

### 10.5 · ✅ CUÁNDO UN ERROR MERECE SER CASO — *F0-1, decidido 2026-07-27*

**El problema que resuelve:** si todo error se vuelve caso, en tres meses hay 80 y **ninguno se
consulta** — sería el nuevo `memory/PENDIENTES.md`. Si ninguno lo hace, los errores se repiten.

#### La prueba de las 3 preguntas — debe cumplir LAS TRES

| # | Pregunta | Qué filtra |
|---|---|---|
| 1 | **¿Volvería a pasar en otro sitio?** | si es único de ese archivo es un **fix**; si es patrón, es **caso** |
| 2 | **¿La causa fue un CRITERIO equivocado**, no un descuido? | un typo no enseña nada; *"el default apuntaba a algo con dueño"* sí |
| 3 | **¿Se puede escribir como regla accionable** que evite el error **antes** de cometerlo? | si no se puede, es una **anécdota** |

#### Calibración con errores reales — para que el criterio no sea abstracto

| Error real | ¿Caso? | Por qué |
|---|---|---|
| Default `general` rompía el aislamiento | ✅ **sí** | patrón + criterio equivocado + regla clara |
| "Reenviar código" burlaba el anti-fuerza-bruta | ✅ **sí** | *"resetear un contador es resetear la defensa"* |
| `tailscale serve` apagó el Funnel | ✅ **sí** | *"probar desde local ≠ probar producción"* |
| `chown -R` en bind mount rompió el HOST | ✅ **sí** | regla ya escrita y LOCKED |
| Heredoc que se comió las variables | ❌ **no** | fix técnico; ya vive en el Método F |
| `DEMO_ENC_KEY` divergente | 🟡 **el patrón sí** | *"un fallback que tapa una divergencia"*; el incidente no |

#### Dos reglas duras que acompañan

**① Umbral automático por repetición.** Si el mismo **tipo** de error aparece **2 veces**, se vuelve
caso **aunque no pase las 3 preguntas**. *La repetición es evidencia por sí sola.*

**② Límite de 12 casos activos.** Al llegar a 13 → **fusionar o archivar**.
> Sin límite, la carpeta de casos se convierte en el archivo de 240 KB que nadie lee.
> **Misma lección: el único archivo con límite es el único que no se desbordó.**

---

### 10.6 · ✅ CÓMO SE DETECTA UNA REGLA QUE ESTORBA — *F0-2, decidido 2026-07-27*

**Principio: que sea ARITMÉTICA, no interpretación.** Un mecanismo que exige juicio para dispararse,
no se dispara.

#### El registro del roce — línea estructurada de 4 campos

```
2026-07-27 · regla: server-primero · bloque: blq-demo · motivo: fix urgente ya verificado
```

**fecha · regla · bloque · motivo.** `revisar-bloques` los cuenta (§12-TER).

#### El disparo

```
regla "server-primero": 3 roces · blq-demo · blq-panel · blq-trace
🔔 REVISIÓN DE REGLA — 3 bloques distintos
```

#### Los dos detalles que hacen que funcione

**① BLOQUES DISTINTOS, no repeticiones.**
3 roces en el **mismo** bloque = fricción puntual de esa tarea.
3 roces en **bloques distintos** = **la regla está mal**.
> Sin esta distinción, cualquier tarea larga dispararía falsas alarmas y el mecanismo se ignoraría.

**② NO CADUCA.**
Si los 3 roces se acumulan en seis meses, sigue siendo señal.
> **El problema no es la velocidad de la fricción: es su recurrencia.**

#### Qué pasa al dispararse

⛔ **La regla NO se cambia automáticamente.** Se **eleva a Brian** con los 3 roces y sus motivos.
Él decide: **ajustar** · **mantener con excepción documentada** · **eliminar**.

> Coherente con el principio madre — *"no existen reglas inmutables, existen apuntadores a reglas:
> estándares mejorando con criterios del usuario"*. **El sistema detecta; Brian decide.**

---

## 11 · CONTEXTO Y CACHÉ POR BLOQUE

> *"Necesitamos guardar caché por bloque y contexto por bloque... tener contexto unitario y global...
> ser el dueño del contexto por bloque, apuntar al contexto del bloque cuando se ocupe."*

### 11.1 · El cambio de fondo

| | Hoy | v2 |
|---|---|---|
| Fuente de verdad | **la conversación** | **el disco** |
| La conversación es | todo | **caché desechable** |
| `/clear` | duele | **irrelevante** |

### 11.2 · Qué se pierde hoy y aquí se salva

| Información | Hoy | v2 |
|---|---|---|
| Estado ("dónde quedamos") | ✅ RETOMAR | ✅ |
| Hechos ("qué se construyó") | ✅ memorias | ✅ |
| **Alcance ("qué SÍ y qué NO")** | 🔴 muere | ✅ **campo del bloque** |
| **Criterio ("por qué así")** | 🔴 muere | ✅ **decisiones del bloque** |
| **Grafo ("qué toco y hasta dónde")** | 🔴 muere | ✅ **conexiones del sub-bloque** |

**Regla operativa:** *si una decisión no está escrita, no está tomada.* Se escribe **durante**, no
al cerrar — así sobrevive a muerte súbita (cupo agotado, crash, auto-compactación).

### 11.3 · ⭐ CARGA POR TIERS — el bloque NO se carga entero

**Es la pirámide de coste del cold-start, aplicada DENTRO del bloque.**

> ⚠️ **Corrección de diseño (2026-07-27):** los tiers **NO son archivos separados** — son el
> **orden de las secciones DENTRO de `BLOQUE.md`**. Partir 70 líneas en varios archivos no ahorra
> nada y añade sitios que se desincronizan (§3.2-TER).

| Tier | Secciones del `BLOQUE.md` | Cuándo |
|---|---|---|
| **1 · por defecto** | **A** identidad · **B** límites · **C** conexiones · **D** estándares · **E** estado | **siempre** |
| **2 · a demanda** | **F** sub-bloques · **G** decisiones · **H** roces | cuando hace falta el *por qué* |
| **3 · a demanda** | **I** guardados · **J** contexto · `docs/` | cuando hace falta el detalle |

**Coste del Tier 1: ~60 líneas.** En la práctica se lee el archivo entero (~150) porque es barato —
igual que `memory/RETOMAR.md`, que nunca se lee por partes.

### 11.4 · ⭐ CRITERIO DE SUFICIENCIA — la prueba que valida el diseño

> **¿Las secciones A-E bastan para reiniciar el trabajo con seguridad?**

Esto convierte *"ser dueños del contexto"* en algo **medible**, no declarativo:

- **Sí basta** → el bloque está bien escrito.
- **No basta** → el bloque está mal escrito y **no se cierra** (criterio del Encargado 3, §4).

> Sin esta prueba, escribir a disco es **acumular**, no ser dueño del contexto.

### 11.5 · ⭐ RESOLUCIÓN DETERMINISTA — sin match, se para

**Cada bloque tiene un identificador único.** Al retomar:

```
1. Buscar el bloque por ID EXACTO
2. ¿Match?  ── SÍ ──▶ cargar Tier 1
       │
       └── NO ──▶ ⛔ PARAR Y PREGUNTAR
                   nunca inferir por nombre parecido
                   nunca elegir "el más probable"
```

**Prohibido:** match difuso · inferencia por nombres parecidos · escoger el bloque más reciente
"porque seguramente es ese".

> **Por qué es la regla más importante de esta sección:** la IA que infiere **suena igual de segura**
> que la que sabe. Ese es el mecanismo exacto de *"no, así no iba"*. Parar y preguntar convierte una
> pérdida silenciosa en una pregunta visible.

### 11.6 · AISLAMIENTO ENTRE BLOQUES

- **No** se leen archivos de otro bloque por defecto.
- **No** se escanea ampliamente `_activos/`.
- **No** se infiere por nombres parecidos.
- Cruzar dos bloques requiere **petición explícita** o una conexión **declarada** en `BLOQUE.md`.

> Es el gate de Puentes —verificado al 100% de cumplimiento— aplicado **entre bloques**. Sin esto,
> "leer los otros bloques por contexto" reproduce dentro del sistema el problema de consumo que el
> gate ya resolvió fuera.

---

## 12 · ESTRUCTURA DE CARPETAS

### 12.0 · DIAGRAMA — el árbol de archivos de la v2

```
~/for3s/
│
├── CLAUDE.md ......................... ⚙️ ARRANQUE AUTOMÁTICO (inyectado)
│                                          reglas indispensables + apunta a todo
│
└── Mente/
    │
    ├── REGLAS_BASE.md ................ 🔑 las reglas mínimas del sistema
    │                                      (portátil: cualquier IA lo lee)
    │
    ├── Alma/  ........................ 👤 LOS 3 ENCARGADOS
    │   ├── ENCARGADO_1_Documentacion.md ... formato de docs y planes
    │   ├── ENCARGADO_2_Desarrollo.md ...... criterios + veto/retroceso
    │   │   ├── expertise/dev-backend.md ....... ⭐ criterio de Brian
    │   │   ├── expertise/dev-frontend.md ...... ⭐ criterio de Brian
    │   │   └── expertise/base_datos.md .... ⭐ criterio de Brian
    │   └── ENCARGADO_3_Validacion.md ...... "que nada quede suelto"
    │
    ├── Cerebro/ ...................... 📐 REGLAS UNITARIAS Y ESTRUCTURAS
    │   ├── CONTRATO_Bloque.md ............. qué campos lleva un bloque
    │   ├── CONTRATO_Documento.md .......... plantilla de todo doc
    │   ├── REGLA_Carriles.md .............. cómo se elige el carril
    │   ├── REGLA_Fix_No_Parche.md ......... el procedimiento anti fix-sobre-fix
    │   ├── REGLA_Roce.md .................. cumplir→registrar→seguir→proponer
    │   ├── casos/ ......................... 🎓 aprendizaje (error→forma)
    │   │   └── CASO_Default_Peligroso.md ..    (ya existe, se muda aquí)
    │   └── Registro_Conversaciones.md ..... 📊 telemetría (ya existe)
    │
    ├── bin/ .......................... 🔧 LOS VALIDADORES (§12-TER)
    │   ├── check-blocks ................... campos · límites · ID único
    │   ├── generate-index ................. 🤖 produce INDEX y STATES
    │   ├── flag-stale ..................... estados sin actualizar
    │   ├── check-sufficiency .............. ⭐ ¿A-E basta para reiniciar?
    │   ├── grade-block .................... ⭐⭐ QA capa 1 (§12-Q.4)
    │   └── check-health ................... ⭐⭐ el sistema se audita SOLO
    │
    ├── Cuerpo/ ....................... 📦 EL SISTEMA DE BLOQUES
    │   ├── _activos/
    │   │   └── DEMO/
    │   │       ├── BLOQUE.md .............. ⭐⭐ ARCHIVO ÚNICO · secciones A-K  ≤150
    │   │       │     A identidad · B límites · C conexiones · D estándares
    │   │       │     E estado · F sub-bloques · G decisiones · H roces
    │   │       │     I guardados · J contexto · K cierre
    │   │       ├── docs/ .................. 📄 el detalle largo vive AQUÍ
    │   │       └── cache/ ................. 💾 caché del bloque
    │   ├── _bloqueados/
    │   ├── _archivados/ ................... ✅ cerrados = experiencia consultable
    │   │   └── DEMO_2026-07/
    │   │       ├── RESUMEN.md
    │   │       └── conexiones.md
    │   └── ESTANDAR_Metodo_Fases_F.md ..... (se absorbe en los encargados)
    │
    ├── Doc/ .......................... 📖 MEMORIA E ÍNDICES
    │   ├── RETOMAR.md ..................... cold-start (ya existe · con límite ✅)
    │   ├── INDICE.md ...................... 🤖 GENERADO — reemplaza al README que miente
    │   ├── ESTADOS.md ..................... 🤖 GENERADO — todos los bloques + salud
    │   ├── PENDIENTES.md .................. 🔴 240 KB — a revisar
    │   ├── Bitacora_Progreso.md
    │   └── README.md ...................... 🔴 §5 y §7 obsoletos
    │
    ├── Tickets/ ...................... 🌉 CONEXIÓN CON OTRO MENTE OS
    │   ├── Puentes_Mente_OS.md ............ el gate (ya existe, se muda)
    │   └── punteros.tsv ................... fuente única (ya existe)
    │
    └── secrets/ ................ 🔒 SECRETOS (fuera de git)
```

**Leyenda:** ⭐ = criterio que diseña Brian · 🤖 = generado por el sistema ·
sin marca = se escribe una vez y evoluciona.



> ⭐ **NOMBRES EN INGLÉS (decidido 2026-07-27).** El estándar completo vive en
> **`rules/NAMING_CONVENTION.md`**. Razón: **el LLM lee las rutas y debe resolverlas con precisión**;
> el inglés es el idioma de todas las convenciones sobre las que se apoya el estándar
> (Claude Code, repos, ADR). **El CONTENIDO sigue en español** — es el pensamiento de Brian.

| Hoy | **v2 (inglés)** | Función |
|---|---|---|
| — | **`Mente/`** (raíz) | REGLAS BASE |
| `Alma/` | **`principles/`** | el POR QUÉ · **los 3 encargados** · expertise por disciplina |
| `Cerebro/` | **`rules/`** | contratos · reglas unitarias · casos · el estándar de nombres |
| `Cuerpo/` | **`blocks/`** | ⭐ **el sistema de bloques** — la unidad da nombre a la carpeta |
| `Doc/` | **`docs/`** | RETOMAR · índice · estados · pendientes · bitácora |
| `Maestro/` | **`registry/`** | registro de ramas · punteros · permisos |
| `Tickets/` | **`bridges/`** | conexión con otros Mente OS |
| `secrets/` | **`secrets/`** | ⚠️ nunca en git |
| *(nuevo)* | **`bin/`** | los validadores |

**Dentro de `blocks/`:** `active/` · `blocked/` · `archive/` (sin prefijos `_`).

**Nombres de archivo:** `minusculas-con-guiones.md` · prefijos `ADR-NNN-` · `rule-` · `case-` ·
`contract-` · `spec-` · `analysis-`.
**MAYÚSCULAS solo para puertas de entrada:** `CLAUDE.md` · `README.md` · `memory/RETOMAR.md` · `BLOCK.md`.

> 🔴 **Nombres RESERVADOS de Claude Code — no se renombran nunca:** `CLAUDE.md` ·
> `.claude/{output-styles,hooks,skills,agents,commands}/` · `.claude/settings.json`. Renombrarlos **apaga la
> funcionalidad**.

> ⭐ **Hallazgo (doc de Anthropic):** los output styles *"inyectan instrucciones en el system prompt"*
> y tienen **el mayor peso de cumplimiento de cualquier método de personalización** — por encima de
> `CLAUDE.md`. **La VOZ (F0-4) es la palanca más fuerte del sistema**, no una capa cosmética.

**Los bloques viven en Mente OS, versionados en git** ✅ *(decidido por Brian)*.

> ⚠️ **Advertencia de migración:** esta estructura **redefine** el significado actual
> (hoy: Alma=visión · Cerebro=marcos teóricos · Cuerpo=implementación). Hay **188 documentos** y
> múltiples punteros que asumen el significado viejo. La Ronda F0 debe resolver la transición sin
> romper referencias.

---

## 12.1 · ✅ MIGRACIÓN DE CARPETAS — LA ESTRUCTURA NUEVA CONVIVE *(decidido 2026-07-27)*

> **El riesgo que evita:** la estructura de §12 **redefine** el significado actual de
> `Alma/` (hoy visión) · `Cerebro/` (hoy marcos teóricos) · `Cuerpo/` (hoy implementación).
> Hay **188 documentos** y ~150 punteros que asumen el significado viejo.

**Decisión: NO se reorganiza nada. Lo nuevo se añade AL LADO de lo viejo.**

```
Mente/
├── Alma/          ← INTACTA (visión) ...... + expertise/        🆕
├── Cerebro/       ← INTACTA (marcos) ...... + CONTRATO_*.md     🆕
│                                             + REGLA_*.md       🆕
│                                             + casos/           🆕
├── Cuerpo/        ← INTACTA (rondas) ...... + _activos/         🆕
│                                             + _archivados/     🆕
├── Doc/           ← INTACTA ............... + INDICE.md 🤖      🆕
├── Tickets/       ← INTACTA
├── secrets/ ← INTACTA
└── _bin/          ← 🆕 NUEVA (los validadores)
```

| Ventaja | Detalle |
|---|---|
| **Cero punteros rotos** | ningún documento cambia de sitio |
| **Cero riesgo** | si el v2 no convence, se borran las carpetas nuevas y todo sigue igual |
| **Reversible** | no hay operación destructiva |

**El coste aceptado:** durante un tiempo conviven dos significados de `Alma/` (visión + encargados).
Se mitiga con el `INDICE.md` generado, que dice qué es cada cosa.

> **Coherente con la decisión 8** (migración por demanda): *lo que se toca se migra, lo que no se
> toca se queda*. Aquí se aplica a las carpetas.

---

## 12-BIS · INVENTARIO DE ARCHIVOS — qué se ocupa, qué se crea, qué se reusa

> **Sin este inventario no se puede planificar la construcción.** Marca de origen:
> ✅ **YA EXISTE** (se reusa o se muda) · 🆕 **NUEVO** (hay que crearlo) ·
> 🤖 **GENERADO** (lo produce el sistema, nunca se escribe a mano).

### A · Arranque y reglas base

| Archivo | Origen | Qué contiene | Quién lo escribe |
|---|---|---|---|
| `CLAUDE.md` | ✅ existe (6.5 KB) | arranque automático · apunta a todo lo demás | IA + Brian aprueba |
| `base-rules.md` 🇺🇸 | 🆕 **nuevo** | reglas mínimas · **portátil a cualquier IA** | Brian define · IA redacta |
| `CLAUDE.md` §enrutador | 🆕 **nuevo** ⭐ | **capa A** (§12-QUATER): ~15 líneas · qué estándar cargar según el trabajo | IA redacta |
| `.claude/settings.json` hooks | 🆕 **nuevo** ⭐ | **capa D**: inyecta el estándar o **bloquea** las 3 acciones críticas | IA construye |

### B · Los 3 encargados (`Alma/`)

| Archivo | Origen | Qué contiene | Quién lo escribe |
|---|---|---|---|
| `principles/owner-0-voice.md` 🇺🇸 | 🆕 **nuevo ⭐** | **THE VOICE** (§12-SEXIES): 8 reglas negativas · portátil | Brian valida · IA redacta |
| `~/.claude/output-styles/for3s.md` 🇺🇸 | 🆕 **nuevo** | ⭐ el vehículo · **mayor peso del sistema** | IA construye |
| `principles/owner-1-docs.md` 🇺🇸 | 🆕 nuevo | formato de docs y planes · apartados base | Brian define · IA redacta |
| `principles/owner-2-dev.md` 🇺🇸 | 🆕 nuevo | criterios de aceptación · veto y retroceso | Brian define · IA redacta |
| `principles/owner-3-validation.md` 🇺🇸 | 🆕 nuevo | qué revisar para que "nada quede suelto" | Brian define · IA redacta |
| `principles/expertise/dev-database.md` 🇺🇸 | ✅ **estructura + cableado** ⭐ | 6 dimensiones · reglas duras · 8 preguntas de entrevista · criterio ⬜ | **Brian** |
| `principles/expertise/dev-backend.md` 🇺🇸 | ✅ **estructura + cableado** ⭐ | idem · 7 preguntas | **Brian** |
| `principles/expertise/dev-frontend.md` 🇺🇸 | ✅ **estructura + cableado** ⭐ | idem · 7 preguntas | **Brian** |

> ⭐ **Los 3 nacen CONECTADOS aunque estén vacíos:** el bloque los declara en §D → el hook los
> inyecta → owner-3 los aplica → `check-blocks` verifica. **Índice de huecos: `docs/PENDING-BRIAN.md`.**
| `rules/qa-dimensions.md` 🇺🇸 | ✅ **estructura hecha** ⭐⭐ | las 6 dimensiones + **evidencia exigida** · criterio ⬜ Brian | Brian define · IA redacta |
| `rules/contract-adr.md` 🇺🇸 | ✅ **hecho** ⭐ | el estándar de decisiones: 6 campos + 3 reglas | IA · Brian aprobó |
| `docs/PENDING-BRIAN.md` 🇺🇸 | ✅ **hecho** ⭐ | **el índice ÚNICO de huecos de criterio** | IA mantiene |

### C · Reglas unitarias y estructuras (`Cerebro/`)

| Archivo | Origen | Qué contiene |
|---|---|---|
| `rules/contract-block.md` 🇺🇸 | 🆕 nuevo | las secciones A-K obligatorias (§3.2-TER) |
| `rules/contract-document.md` 🇺🇸 | 🆕 nuevo | plantilla y metadata de todo documento |
| `rules/rule-lanes.md` 🇺🇸 | 🆕 nuevo | cómo se elige el lane por propagación (§5) |
| `rules/rule-fix-not-patch.md` 🇺🇸 | 🆕 nuevo | procedimiento anti fix-sobre-fix (§7) |
| `rules/rule-friction.md` 🇺🇸 | 🆕 nuevo | comply→log→continue→propose (§8) |
| `rules/rule-isolation.md` 🇺🇸 | 🆕 nuevo | aislamiento entre bloques (§11.6) |
| `rules/NAMING_CONVENTION.md` 🇺🇸 | ✅ **existe** | el estándar de nombres (escrito 2026-07-27) |
| `rules/case-dangerous-default.md` | ✅ **existe** | se **muda** desde `Cuerpo/` |
| `Cerebro/Registro_Conversaciones.md` | ✅ **existe** (16 KB) | telemetría — **se conserva tal cual** |
| `Cerebro/For3s_OS_Grafo_Maestro.md` | ✅ existe (65 KB) | fuente de verdad arquitectónica — no se toca |

### D · El sistema de bloques (`Cuerpo/`)

| Ruta | Origen | Qué es | Tier | Límite |
|---|---|---|---|---|
| `Cuerpo/_activos/<BLOQUE>/BLOQUE.md` | 🆕 nuevo | ⭐⭐ **ARCHIVO ÚNICO** · secciones A-K (§3.2-TER) | — | **≤150 líneas** |
| `Cuerpo/_activos/<BLOQUE>/docs/` | 🆕 nuevo | el detalle largo (cronologías, análisis) | — | sin límite |
| `Cuerpo/_activos/<BLOQUE>/cache/` | 🆕 nuevo | 💾 caché del bloque | — | — |
| `Cuerpo/_bloqueados/` · `_archivados/` | 🆕 nuevo | estados del bloque | — | — |
| `rules/ESTANDAR_Metodo_Fases_F.md` | ✅ **existe** (7 KB) | **se absorbe** en los 3 encargados | — | — |
| `docs/Arquitectura_Mente_OS_v2_Bloques.md` | ✅ **este archivo** | el plano | — | — |

### D-bis · Los validadores 🔧 *(§12-TER — resuelven el bloqueante A)*

| Archivo | Origen | Qué comprueba |
|---|---|---|
| `bin/check-blocks` 🇺🇸 | 🆕 **nuevo** | campos · **límites** · ID único · conexiones válidas |
| `bin/generate-index` 🇺🇸 | 🆕 **nuevo** | 🤖 produce `docs/INDEX.md` + `docs/STATES.md` |
| `bin/flag-stale` 🇺🇸 | 🆕 nuevo | `State` sin actualizar · bloques parados |
| `bin/check-sufficiency` 🇺🇸 | 🆕 **nuevo** | ⭐ ¿las secciones A-E bastan para reiniciar? |
| `bin/grade-block` 🇺🇸 | 🆕 **nuevo ⭐⭐** | **QA capa 1**: dead code · duplication · tests · graph · cycles (§12-Q.4) |
| `bin/check-health` 🇺🇸 | 🆕 **nuevo ⭐⭐** | **el sistema se audita solo** · corre en `SessionStart` (§12-T.3) |

### E · Memoria e índices (`Doc/`)

| Archivo | Origen | Nota |
|---|---|---|
| `memory/RETOMAR.md` | ✅ existe (14 KB) | **se conserva** — funciona (arranque 38-40K) |
| `docs/INDEX.md` 🇺🇸 | 🤖 **generado** | ⚠️ **reemplaza al README que hoy miente** (35/188) |
| `docs/STATES.md` 🇺🇸 | 🤖 **generado** | estado de todos los bloques de un vistazo |
| `memory/PENDIENTES.md` | ✅ existe (240 KB) | 🔴 **a revisar**: hoy es ilegible |
| `memory/Bitacora_Progreso.md` | ✅ existe (162 KB) | se conserva |
| `memory/archive/README.md` | ✅ existe | 🔴 su §5 y §7 están obsoletos |

### F · Puentes y secretos

| Archivo | Origen | Nota |
|---|---|---|
| `bridges/Puentes_Mente_OS.md` | ✅ **existe** | el gate — **verificado: se cumple 100%** |
| `Maestro/punteros.tsv` | ✅ **existe** | fuente única de ramas — funciona |
| `Maestro/permisos.md` + `Maestro/maestro_lib.sh` | ✅ **existe** | fail-closed en **código** — 100% |
| `secrets/*` | ✅ existe | secretos, fuera de git — no se toca |

### G · Resumen de esfuerzo

| Categoría | Archivos | Comentario |
|---|---|---|
| ✅ **Ya existen y se conservan** | **9** | lo que funciona no se reescribe |
| ✅ Existen y se mudan/absorben | 2 | el caso y el Método F |
| 🆕 Documentos nuevos a crear | **~15** | de los cuales **3 los define Brian** (expertise) |
| 🔧 **Validadores nuevos** | **4** | comprueban lo comprobable |
| ⭐ **Mecanismos de lectura** | **2** | enrutador (capa A) + hooks (capa D) — §12-QUATER |
| 🤖 **Generados** | 2 | índice y estados — nunca a mano |
| 📦 **Por bloque** | **1 archivo** + `docs/` + `cache/` | ⭐⭐ archivo único, ~150 líneas |

> ⭐ **Tres piezas críticas, por razones distintas:**
> - **`Alma/expertise/*` (3 archivos)** — son **criterio de Brian**; la IA no puede escribirlos.
> - **Los hooks (capa D)** — lo **único** que no depende del criterio de la IA. Sin ellos, el v2
>   repite el fallo del Método F: existe, es encontrable, **y no se lee**.
> - **`_bin/*` (4 validadores)** — la red al cerrar.
>
> Todo lo demás la IA puede redactarlo a partir de este plano.

---

## 12-TER · ⭐ LOS VALIDADORES — la respuesta al bloqueante A

> **LA DOCTRINA ES DOCUMENTO. LA VERIFICACIÓN ES SCRIPT.**

**El problema que resuelve.** La ley medida de este sistema:

| Forma de la regla | Cumplimiento medido |
|---|---|
| **Código** (gate de Puentes, permisos fail-closed) | ✅ **100%** |
| **Documento** (Método F, registro pre-`/clear`, índice) | 🔴 **falla 40-60%** |

**La solución no es llevar el criterio a código** — el criterio es de Brian y debe seguir siendo
legible y evolutivo. **La solución es llevar la VERIFICACIÓN a código.**

El script **no decide nada**. Solo comprueba **lo comprobable**:

```
   ¿existe el archivo?          ¿tiene los campos obligatorios?
   ¿cabe en su límite?          ¿el ID es único?
   ¿está obsoleto?              ¿las conexiones apuntan a bloques reales?
```

### Los 4 validadores

| Validador | Qué comprueba | Cuándo corre |
|---|---|---|
| **`revisar-bloques`** | archivos presentes · campos obligatorios · **límites de tamaño** · ID único · conexiones válidas | al abrir y al cerrar |
| **`generar-indice`** | 🤖 produce `docs/INDEX.md` y `docs/STATES.md` **desde los bloques reales** | tras cualquier cambio |
| **`avisar-obsoletos`** | detecta `estado.md` sin actualizar y bloques activos sin movimiento | periódico |
| **`verificar-suficiencia`** | ⭐ ¿las secciones **A-E** bastan para reiniciar? (§11.4) | al cerrar un bloque |
| **`grade-block`** | ⭐⭐ **dead code · duplication · tests · dependents · cycles** (§12-Q.4) | al cerrar · a demanda |
| **`check-health`** | ⭐⭐ **el SISTEMA se audita solo**: permisos contradictorios · índices que mienten · higiene · contexto (§12-T.3) | 🤖 **`SessionStart`, sin pedirlo** |

> ⭐ **Los validadores no solo verifican: COMPLETAN lo derivable** (§12-T.1) — pero nunca el criterio.
> Y cuando una puerta bloquea, se emite un **RECIBO DE APROBACIÓN** (§12-T.2).

### 12-T.1 · ⭐ VALIDADORES QUE COMPLETAN, no solo verifican *(incorporado 2026-07-27)*

**Origen:** referencia externa madura — su middleware *"compromete y abre el PR automáticamente **si
el agente no lo hizo**"*. No solo comprueba: **completa el paso omitido.**

**Por qué nos importa, medido:** la regla *"sin registro no hay `/clear`"* existe desde el 14-jul y
**se incumplió 5 de 11 veces**. Un validador que solo avisa habría avisado 5 veces… y seguiríamos
con 5 sesiones sin registrar.

| Situación | Validador que solo **verifica** | Validador que **completa** |
|---|---|---|
| `estado.md` sin actualizar al cerrar | 🔴 "falta actualizar" | ✅ **lo escribe** con lo que sabe · marca `auto:` |
| Índice desincronizado | 🔴 "el índice miente" | ✅ **lo regenera** |
| Bloque cerrado sin resumen | 🔴 "falta el resumen" | ✅ **redacta un borrador** para que Brian lo revise |
| Sub-bloque sin declarar dependientes | 🔴 "falta el grafo" | ✅ **lo calcula por grep** y lo propone |

**Regla dura de esta capacidad:**

> **Completar es para lo DERIVABLE, nunca para el criterio.**

| ✅ Se puede completar | ⛔ NUNCA se completa |
|---|---|
| el grafo de dependientes (se calcula) | los **límites qué SÍ / qué NO** (es alcance) |
| el índice y los estados (son derivados) | las **decisiones y su rationale** (es criterio) |
| el conteo de líneas, tests, duplicación | el **veredicto de calidad** (§12-QUINQUIES) |
| un borrador de resumen, marcado `auto:` | los **estándares obligatorios** del bloque |

> Todo lo autocompletado se marca **`auto:`** para que se distinga de lo que escribió una persona.
> **Un campo autocompletado que se hace pasar por decidido es peor que un campo vacío.**

### 12-T.2 · ⭐ RECIBO DE APROBACIÓN — cuando una puerta bloquea

**Origen:** referencia externa — *"superficies de aprobación compactas que muestran los cambios
propuestos **antes** de ejecutar"*.

**El hueco que cierra:** el v2 tiene 3 puertas que bloquean (§12-QUATER), pero **no tenía forma de
presentar el cambio para que Brian apruebe de un vistazo**. Bloquear sin dar salida es fricción.

```
🔴 PUERTA CERRADA · editar pieza con dependientes

  pieza:        lib/demo/userStore.ts
  propaga a:    session.ts · for3sChat.ts · admin.ts · route.ts · accountStore.ts
  bloque:       blq-demo-2026-07
  estándar:     Cerebro/REGLA_Fix_No_Parche.md

  lo que se quiere cambiar:
    → resolver la instancia real en vez de leer `kind` de la cookie

  evaluación de la construcción (§7):
    ✔ causa raíz identificada: `kind` se usa como si fuera la instancia
    ✔ los 6 sitios afectados están mapeados
    ✔ solución propuesta: un punto único que resuelvan los 6

  ┌──────────────────────────────────────────────┐
  │  [ APROBAR ]   [ VER LOS 6 SITIOS ]   [ NO ] │
  └──────────────────────────────────────────────┘
```

**Tres reglas del recibo:**
1. **Cabe en una pantalla.** Si no cabe, el cambio es demasiado grande y hay que partirlo.
2. **Muestra la propagación**, no solo el archivo — es lo que Brian no podía ver antes.
3. **Incluye la evaluación de la construcción** (§7): sin ella, la puerta no se abre.

> **El recibo convierte el bloqueo en una decisión informada de 10 segundos**, en vez de un muro.

### 12-T.3 · ⭐⭐ `check-health` — EL SISTEMA SE AUDITA SOLO

> **Brian, 2026-07-27:** *"el usuario no te debe decir 'oye, realiza esta conexión' o 'limpia la
> basura' — es algo que ya deberíamos estar automatizando."*

**La regla que sale de ahí:**

> ## Si hay que PEDIRLO, no está automatizado.

#### El problema que resuelve — tres fallos con la misma causa

| Fallo | Cuánto llevaba así | ¿Quién lo encontró? |
|---|---|---|
| `additionalDirectories` daba acceso a NavigoX, contradiciendo el gate | **semanas** | Brian, preguntando |
| `Maestro/registro.md` decía 173 docs / 4.5 MB · realidad 195 / 17 MB | desde el 17-jul | Brian, preguntando |
| 999 archivos de `file-history` >30 días · `cleanupPeriodDays` sin fijar | meses | Brian, preguntando |

> **Los tres son el mismo fallo: nada vigila el estado del sistema.**
> El v2 tenía validadores para los **bloques** y ninguno para **su propia salud**.

#### Qué comprueba

```
bin/check-health

  🔴 PERMISSIONS
     · additionalDirectories contradicting a deny rule      ← the NavigoX hole
     · allow entries pointing at paths that no longer exist
     · deny missing for any gated branch in pointers.tsv

  🔴 TRUTH
     · registro.md figures vs measured reality
     · docs/INDEX.md older than the blocks it indexes
     · pointers.tsv rows whose index file does not exist

  🟡 HYGIENE
     · file-history entries older than cleanupPeriodDays
     · empty directories
     · cleanupPeriodDays not set
     · files over their declared size limit (§3.2-bis)

  🟡 SESSION
     · live context over 200K / 500K  ← the 21-jul threshold
     · session open longer than 48h
     · repeated "Connection closed mid-response"
```

#### Las reglas del validador

**① No arregla nada — REPORTA.** Misma doctrina que `grade-block`: *la doctrina es documento, la
verificación es script*. Excepción: lo **derivable** puede completarse (§12-T.1), marcado `auto:`.

**② Corre SOLO, en el hook `SessionStart`.** No se invoca. Aparece al arrancar.
> ⚠️ **Debe ser barato** (<1s) o se vuelve fricción en cada arranque y alguien lo desactiva.

**③ ⛔ NUNCA borra evidencia forense.** Los `.jsonl` de sesión **no se tocan**: de ahí salió el
incidente del 21-jul que no estaba documentado en ningún sitio. **Reporta el peso, no lo limpia.**

**④ Silencio cuando todo está bien.** Si no hay hallazgos, no imprime nada. Un validador que habla
siempre se ignora siempre.

#### Precedente real — la limpieza del 2026-07-27

Primera pasada manual, para calibrar qué debe detectar:

| Encontrado | Acción |
|---|---|
| 999 archivos de `file-history` >30 días (~19 MB) | ✅ borrados |
| `cache/changelog.md` del 04-mayo (268 KB) | ✅ borrado |
| `paste-cache/` vacía | ✅ borrada |
| `.claude/` total | **464 MB → 442 MB** |
| `projects/*.jsonl` (371 MB) | ⛔ **NO se tocó — evidencia forense** |
| `get-shit-done/` (3.1 MB, sin tocar desde mayo) | ⛔ **NO se tocó — dependencia de 9 hooks** |

> **Lo que esta pasada enseñó:** *"sin tocar desde mayo"* **no significa basura.** `get-shit-done/`
> lleva meses quieto y alimenta los 9 hooks activos. **El criterio no es la fecha: es si algo depende
> de ello.** El validador debe distinguir *viejo* de *huérfano*.

### Qué NO hacen los validadores

- **No** juzgan si el código es bueno → eso es el Encargado 2.
- **No** deciden el carril → eso lo decide la propagación (§5).
- **No** aprueban ni rechazan trabajo → eso es de Brian.
- **No** completan nada que sea criterio, alcance o veredicto → solo lo **derivable** (§12-T.1).

> **Su único poder es negarse a dejar cerrar un bloque mal formado.** Con eso basta: es la diferencia
> entre una regla que se cumple y una que se olvida.

### El índice que no puede mentir

**Hoy:** `memory/archive/README.md` inventaría **35 de 188 documentos** — regla incumplida ~150 veces, y lista
"R2-R10 pendientes" cuando están todas LOCKED.

**En el v2:** `docs/INDEX.md` y `docs/STATES.md` se **generan**. Incluyen por bloque:
nombre · estado · fase · dueño · **salud** · ruta · última actualización.

> Es el mismo criterio que Brian ya aplicó en `Maestro/punteros.tsv` — *"aquí NO se duplica la tabla:
> la sincronía a mano murió"*. **Ese criterio ya existe en el sistema; aquí solo se extiende.**

---

## 12-QUATER · ⭐⭐ CÓMO SE GARANTIZA QUE UN ARCHIVO SE LEA

> **La pregunta de Brian (2026-07-27):** *"¿cómo sabe que realmente ese es el carril o el archivo
> que tiene que leer, sin omitir? Porque si no, va a pasar lo del Método F, que nunca se leyó
> aunque se puso."*

**Es la pregunta que decide si el v2 funciona o repite el fracaso.**

### El problema, con precisión

Hay **tres cosas distintas** que se confunden:

| | Qué es | ¿Se cumple hoy? |
|---|---|---|
| **Existir** | el archivo está escrito | ✅ el Método F existe desde 04-jul |
| **Ser encontrable** | se sabe que existe y dónde | ✅ `CLAUDE.md` lo menciona |
| **SER LEÍDO** | **entra en contexto en el momento correcto** | 🔴 **falló en 2 de 5 sesiones** |

**El Método F cumplía las dos primeras y falló la tercera.**

> ⚠️ **Lo que lo hace invisible:** la IA **no sabe lo que no leyó**. Sin abrir el estándar no siente
> que le falte nada — trabaja con lo que tiene y **suena igual de segura**. Es el mismo mecanismo de
> la degradación del 21-jul.

### Por qué las soluciones obvias no bastan

| Intento | Qué pasa |
|---|---|
| *"que CLAUDE.md diga que hay que leerlo"* | **ya lo dice. Falló.** |
| *"meter los estándares en CLAUDE.md"* | ~15 archivos → el arranque pasa de 38K a cientos de miles de tokens. **Reproduce el problema de consumo del 9-jul** |

> **El conflicto de fondo:** lo que se **inyecta** se cumple (100%) pero cuesta tokens siempre;
> lo que se lee **a demanda** es barato pero depende del criterio de la IA (falla 40-60%).
> **Ninguna sirve sola.**

### La solución: 4 CAPAS ✅ *(aprobado por Brian 2026-07-27)*

Cada capa cubre el fallo de la anterior:

```
   ┌─────────────────────────────────────────────────────────────┐
   │ A · ENRUTADOR en CLAUDE.md            ~15 líneas · siempre  │
   │   "si tocas backend → carga expertise/dev-backend.md ANTES"     │
   │   ✔ barato · ✔ siempre presente · ✘ aún depende de la IA    │
   └───────────────────────────┬─────────────────────────────────┘
                               ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ B · EL BLOQUE DECLARA sus estándares   §D del BLOQUE.md     │
   │   el estándar viaja CON el trabajo, no en un índice general │
   │   ✔ específico del trabajo · ✘ lo escribe quien abre        │
   └───────────────────────────┬─────────────────────────────────┘
                               ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ D · HOOK del harness       ANTES de editar un archivo       │
   │   detecta el tipo de trabajo → INYECTA el estándar          │
   │   o BLOQUEA la acción                                       │
   │   ⭐ ÚNICA capa que NO depende del criterio de la IA         │
   └───────────────────────────┬─────────────────────────────────┘
                               ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ C · VALIDADOR al cerrar    red de seguridad                 │
   │   sin rastro de que se aplicó el estándar → no cierra       │
   │   ✔ verificable · ✘ llega tarde (el código ya está escrito) │
   └─────────────────────────────────────────────────────────────┘
```

**Sobre la portabilidad:** el hook (D) es **aceleración, no fundamento**. Con otra IA sin hooks
quedan A + B + C y el sistema **sigue funcionando** — con menos garantía. *El protocolo es portátil;
el hook es el turbo cuando existe.*

### ⭐ LAS 3 PUERTAS CERRADAS ✅ *(decidido con Brian)*

El hook tiene **tres respuestas**:

| | Qué hace | Cuándo |
|---|---|---|
| 🟢 **PASAR** | nada, sigo | cambio trivial |
| 🟡 **AVISAR** | **inyecta el estándar** en contexto y lo registra · sigo trabajando | la mayoría de los casos |
| 🔴 **BLOQUEAR** | **la acción NO se ejecuta** hasta cumplir algo | solo 3 casos |

**Solo se bloquean tres acciones, cada una con su razón medida:**

| Acción bloqueada | Por qué | Evidencia |
|---|---|---|
| **Editar una pieza con dependientes declarados** | es el mecanismo exacto del fix-sobre-fix | `userStore.ts` ×21 · **42%** de commits = fixes |
| **Tocar la base de datos** | propaga a todo lo que lee la tabla y no se ve venir | Brian: *"si no tenemos control estamos mal"* |
| **Cerrar un bloque sin pasar suficiencia** | la próxima sesión arrancaría ciega **sin saberlo** | *"no, así no iba"* · 5/11 sesiones sin registrar |

**Ejemplo real de bloqueo:**

```
Intento:   Edit lib/demo/userStore.ts
             ↓
Hook:      ¿esta pieza tiene dependientes declarados? → SÍ, 5
             ↓
🔴 BLOQUEADO
   "userStore.ts propaga a: session.ts · for3sChat.ts · admin.ts ·
    route.ts · accountStore.ts
    Antes de editar: evalúa la construcción completa (§7 fix ≠ parche).
    Si ya lo hiciste, declara el alcance en el bloque."
```

> **Sin el bloqueo, eso mismo fue:** edito un archivo → funciona → cierro → y 4 commits después
> *"barrido completo del patrón"*. **Los 21 toques a `userStore.ts` empezaron exactamente así.**

**Por qué solo tres:** es la lógica del gate de Puentes — **protege UNA sola cosa y por eso se cumple
el 100% de las veces**. Si se bloquean veinte cosas, el sistema estorba, se desactiva, y volvemos al
inicio. **Pocas puertas cerradas, bien elegidas.**

> **Bloquear no es prohibir:** es *"para aquí, haz esto primero, y sigue"*. Brian siempre puede
> ordenar que se pase igual.

---

## 12-QUINQUIES · ⭐⭐⭐ EL VEREDICTO DE CALIDAD — QA dentro de Mente OS

> **El dolor que resuelve (Brian, 2026-07-27):** *"en la demo, ANTES del clear me dijo 'todo está
> perfecto, me encantó'. Le di clear y me dijo 'sí está bien lo que se hizo, mejoró, pero aún sigue
> roto'. Y en mi cabeza estoy pensando: ¿me mientes o qué está pasando? **Ese dolor es el que más
> me impide trabajar en estos momentos.** Ya no es ver si funciona, es ver si lo que está escrito
> es un producto o es un MVP hecho para que funcione, hecho por IA."*

### 12-Q.1 · La evidencia — está medida, no es una impresión

| Momento | Lo que dije |
|---|---|
| 24-jul 21:15 · sesión 1, inicio | *"el sistema **está completo**"* |
| 26-jul 06:24 · sesión 1, cierre | *"tiene el estado completo para retomar **sin perder nada**"* |
| **26-jul 06:33 · sesión 2, tras `/clear`** | *"lo que está mal es que este archivo **lo implementa a medias**"* |
| 26-jul 23:59 · sesión 2, cierre | *"🔴 **lo que sigue siendo de MVP**"* |

> **9 minutos separan "completo, sin perder nada" de "lo implementa a medias".**
> Lo único que ocurrió entre medias fue un `/clear`.

### 12-Q.2 · Por qué pasa — no es mentira, es que el juicio no valía nada

**Los dos juicios eran sinceros. Ninguno era fiable.** Tres sesgos lo explican:

| Sesgo | Qué ocurre |
|---|---|
| **Esfuerzo reciente** | acabo de arreglar 5 cosas → mi contexto dice "arreglé, arreglé" → concluyo "está bien". **Medí cuánto trabajé, no cómo quedó** |
| **Solo veo lo que toqué** | toqué 6 de 40 archivos → mi juicio cubre 6. Digo "está completo" queriendo decir "**lo que toqué** está completo" |
| **Tras el `/clear` desaparece el sesgo** | leo el archivo sin recordar que costó 21 commits → veo lo que vería un tercero |

> ⭐ **Ese "tercero" es el juicio correcto. El problema es que hoy solo aparece por accidente,
> después de un `/clear`.**

**Y la conexión que Brian identificó:** *"¿está todo conectado?"* y *"¿lo que dices está bien, está
bien?"* **son la misma pregunta.** Ambas piden un juicio que **no dependa de quién lo emite ni de
cuándo**. Hoy el veredicto es una opinión, y una opinión que cambia con el contexto **no es un
veredicto: es un estado de ánimo**.

### 12-Q.3 · LA REGLA MADRE DE ESTA SECCIÓN

> ## 🚫 La IA NO declara "está bien". La IA REPORTA LA MEDICIÓN.

Un bloque no se cierra con un adjetivo. Se cierra con **una calificación reproducible**.

### 12-Q.4 · CAPA 1 — QA MEDIBLE (script · sin criterio humano)

Lo que un script puede comprobar sin opinar:

| Métrica | Qué detecta | Ataca |
|---|---|---|
| **Archivos sin consumidor** | nadie los importa | ⭐ **código muerto** |
| **Exports nunca importados** | función escrita y jamás usada | ⭐ *"lo dejé por si acaso"* |
| **Bloques de código duplicados** | la misma lógica en 2+ sitios | ⭐ **redundancia** |
| **Archivos tocados sin test** | cambio sin red | *"solo funciona lo indispensable"* |
| **Dependientes no declarados** | el bloque miente sobre su grafo | fix-sobre-fix |
| **Ciclos de importación** | arquitectura enredada | deuda estructural |
| **Cobertura de caminos críticos** | los 5 flujos que importan | los tapones de la demo |

**Salida — el mismo resultado antes y después del `/clear`:**

```
BLOQUE DEMO — calificación medida · 2026-07-27
  archivos sin consumidor (código muerto):        3  🔴
  exports nunca importados:                       7  🔴
  bloques duplicados (≥8 líneas):                 2  🟡
  archivos tocados sin test:                      8  🔴
  dependientes no declarados en el bloque:        1  🔴
  ciclos de importación:                          0  🟢
  cobertura de caminos críticos:                0/5  🔴
  ──────────────────────────────────────────────────
  VEREDICTO MEDIBLE: 🔴 MVP — no es producto
```

**Tres propiedades que lo cambian todo:**
1. **No depende del contexto** → mismo comando, mismo resultado. **Aquí muere la contradicción.**
2. **Cubre TODO el bloque**, no solo lo que se tocó (los 40 archivos, no los 6).
3. **Brian puede reproducirlo** → no hay que creerle a la IA: se corre y se ve.

### 12-Q.5 · ⭐⭐ CAPA 2 — QA DE CRITERIO (la revisión del senior)

> **Brian, 2026-07-27:** *"esto lo necesito, le diste al clavo. Que la arquitectura es correcta, si
> el diseño de datos es bueno, si la abstracción es la adecuada, si el nombre es claro. **Porque así
> v2 se diferencia**: no cumplimos con solo lo que nos dijo la IA, cumplimos porque sabemos qué
> requerimientos necesitas. **Tenemos QA como uno de los elementos internos de Mente OS y eso vale
> oro.** Que no sea 'me lo dio la IA y no sé', sino que **se sienta hecho por un senior de 50 años
> de experiencia**."*

**Esto es lo que diferencia al v2.** Lo medible lo tiene cualquier linter. **Lo que ningún linter
tiene es el criterio de un senior — y ese criterio es lo que Brian aporta y el sistema aplica.**

#### Cómo se convierte criterio en algo verificable

Un criterio suelto (*"la arquitectura debe ser correcta"*) **no sirve** — es tan vago como "está
bien". Cada criterio se declara con **3 partes**:

| Parte | Para qué |
|---|---|
| **La pregunta** | qué se juzga, en una frase concreta |
| **La evidencia exigida** | 🔴 **qué hay que MOSTRAR** para responder — no basta afirmar |
| **El fallo típico** | cómo se ve cuando está mal (viene de casos reales) |

> ⭐ **La evidencia es lo que impide que la IA se autoapruebe.** No se puede responder "sí, la
> arquitectura es correcta": hay que **mostrar el árbol de dependencias**. La respuesta sin
> evidencia **no cuenta**.

#### Las 6 dimensiones de criterio

| # | Dimensión | La pregunta | Evidencia exigida |
|---|---|---|---|
| **1** | **Arquitectura** | ¿cada pieza tiene una sola responsabilidad y está en la capa correcta? | el árbol de dependencias + señalar qué pieza haría fallar a cuántas |
| **2** | **Diseño de datos** | ¿el esquema representa el dominio? ¿normalizado? ¿los estados imposibles son imposibles? | el esquema real + un caso que el modelo NO puede representar mal |
| **3** | **Abstracción** | ¿está al nivel correcto — ni copiada 3 veces ni generalizada de más? | los sitios donde se repite, o los usos reales de la abstracción |
| **4** | **Nombres** | ¿el nombre dice lo que hace, sin leer el cuerpo? | 3 nombres del bloque explicados sin abrir el archivo |
| **5** | **Contratos** | ¿las interfaces entre piezas están declaradas? ¿los errores son parte del contrato? | la firma real + qué pasa cuando falla |
| **6** | **Necesidad** | 🔴 ¿**cada archivo que existe TIENE que existir**? | por cada archivo nuevo: quién lo consume y por qué no podía vivir en otro sitio |

> **La dimensión 6 es la respuesta directa a Brian:** *"que lo que está es necesario, y no se lo
> inventó, o lo quiso mover, o dijo 'ah, lo dejo aquí por si lo necesitamos'"*.

#### Salida de la capa 2

```
BLOQUE DEMO — revisión de criterio · 2026-07-27
  1 arquitectura ... 🟡  userStore concentra 5 responsabilidades
                         evidencia: árbol adjunto · 5 módulos dependen de él
  2 datos ......... 🟢  esquema normalizado, 7 FKs, sin estados imposibles
                         evidencia: schema.sql + caso "invitado sin dueño" imposible
  3 abstracción ... 🔴  "resolver instancia" copiado en 6 sitios
                         evidencia: rutas de las 6 copias
  4 nombres ....... 🟡  `kind` no dice qué distingue
                         evidencia: 3 nombres explicados; `kind` requiere leer el cuerpo
  5 contratos ..... 🔴  4 funciones sin declarar qué pasa al fallar
                         evidencia: firmas sin tipo de error
  6 necesidad ..... 🔴  accountStore.ts: 0 consumidores tras la migración
                         evidencia: grep sin resultados
  ──────────────────────────────────────────────────────────────
  VEREDICTO DE CRITERIO: 🔴 no pasa — 3 dimensiones en rojo
```

#### De dónde sale el criterio

| Quién | Qué aporta |
|---|---|
| **Brian** | ⭐ **el criterio** — qué exige un senior en backend, frontend y BD (`Alma/expertise/*`) |
| **La IA** | aplicar ese criterio y **traer la evidencia**, no emitir opinión propia |

> **Es la misma regla de §9.1: la IA no inventa criterio.** Aquí además **no puede autoaprobarse**,
> porque cada respuesta exige evidencia mostrable.

### 12-Q.6 · EL VEREDICTO FINAL DEL BLOQUE

```
   ┌──────────────────────────────────────────────┐
   │ CAPA 1 · MEDIBLE   (script)                  │
   │ código muerto · duplicación · tests · grafo  │
   └───────────────────┬──────────────────────────┘
                       ▼
   ┌──────────────────────────────────────────────┐
   │ CAPA 2 · CRITERIO  (6 dimensiones + prueba)  │
   │ arquitectura · datos · abstracción · nombres │
   │ contratos · NECESIDAD                        │
   └───────────────────┬──────────────────────────┘
                       ▼
        ┌────────────────────────────────┐
        │ 🟢 PRODUCTO   · ambas en verde │
        │ 🟡 CASI       · sin rojos      │
        │ 🔴 MVP        · algún rojo     │
        └────────────────────────────────┘
```

**Reglas de cierre:**
- El veredicto se **escribe en el bloque con fecha** (campo `calificación`).
- 🔴 en cualquier capa → **el bloque no se cierra como producto**. Puede cerrarse marcado
  explícitamente como **MVP**, con la deuda listada — *lo que no se puede es cerrarlo diciendo
  "está bien"*.
- **La comparación entre veredictos** (hoy vs el anterior) responde *"¿mejoramos o empeoramos?"*
  con números, no con impresiones.

> ⭐ **Lo que esto le da a Brian:** ya no *"me lo dijo la IA y no sé"*. Es **QA como elemento interno
> de Mente OS**: requisitos declarados por él, verificados con evidencia, reproducibles. **Se siente
> hecho por un senior porque el criterio ES de un senior — el sistema solo garantiza que se aplique
> siempre, y no solo cuando la IA se acuerda.**

---

## 12-SEXIES · ⭐⭐ LA VOZ — cómo se comunica Mente OS

> **Brian, 2026-07-27:** *"necesito tenerlo, porque debe existir esa diferencia, ocupando Mente OS."*
>
> **El principio:** si Mente OS gobierna **cómo se construye**, también debe gobernar
> **cómo se comunica**. Un sistema que produce código de senior y lo explica como un folleto
> genérico está a medias.

### 12-S.1 · El hallazgo — no hay nada configurado

Medido en este entorno (2026-07-27):

| Capa | Estado |
|---|---|
| `CLAUDE.md` del proyecto | 🔴 **cero reglas de tono o estilo** — solo arranque, scope, seguridad |
| `~/.claude/output-styles/` | 🔴 **la carpeta no existe** |
| `.claude/settings.json` (proyecto y global) | 🔴 sin `outputStyle` |
| Hooks activos en el entorno | ✅ **9 hooks funcionando** (sistema externo) |

> **Conclusión:** *"se siente hecho por IA"* **no viene de un archivo mal configurado. Viene de que
> nadie escribió el archivo.** Se estaba recibiendo el comportamiento por defecto, sin ninguna
> instrucción de forma.
>
> ✅ **Y el mecanismo está probado:** ya hay 9 hooks corriendo en este entorno. La capa D de
> §12-QUATER no es una hipótesis — es algo que aquí ya funciona.

### 12-S.2 · Dónde vive la voz

| Archivo | Alcance | Precedencia |
|---|---|---|
| `~/.claude/output-styles/for3s.md` | **todos** los proyectos de Brian | reemplaza parte del prompt de sistema |
| `principles/owner-0-voice.md` | **este** Mente OS | se inyecta vía `CLAUDE.md` |
| `.claude/settings.json` → `"outputStyle": "for3s"` | activa el estilo global | — |

> ⚠️ **Nota de portabilidad:** `output-styles` es específico de Claude Code. Por eso **el contenido
> canónico vive en `principles/owner-0-voice.md`** (portátil, cualquier IA lo lee) y el `output-style`
> es solo **el vehículo** que lo aplica aquí. Mismo criterio que los hooks: *aceleración, no fundamento*.

### 12-S.3 · ⭐ El contenido — reglas NEGATIVAS y verificables

**La lección de diseño:** *"sé claro y directo"* **no cambia nada** — es exactamente el tipo de
instrucción vaga que produce el problema. **Lo que funciona son prohibiciones concretas.**

| # | Regla | Qué elimina |
|---|---|---|
| 1 | **No abrir validando** (*"excelente pregunta"*, *"tienes toda la razón"*). Ir al contenido | apertura de relleno |
| 2 | **Comprometerse con UNA recomendación.** Si hay opciones, elegir y decir por qué. Prohibido *"depende"* sin resolver | el hedging que no decide |
| 3 | **Decir "no lo sé"** en vez de generalizar | seguridad falsa |
| 4 | **Viñetas solo si hay lista real.** No 3 puntos por costumbre | estructura decorativa |
| 5 | **No cerrar repitiendo** lo ya dicho | el párrafo-resumen inútil |
| 6 | **Prohibido:** *"es importante destacar"*, *"cabe mencionar"*, *"en resumen"*, *"profundizar"* | muletillas delatoras |
| 7 | ⭐ **Afirmación de hecho sin verificar = prohibida.** Se mide, o se dice que no se midió | 🔴 **la más importante** |
| 8 | **Omitir lo que no importa.** Cubrir el ángulo que importa, no todos | el exceso que delata |

> ⭐ **La regla 7 es la misma del veredicto de calidad (§12-Q.3):**
> **la IA no declara — reporta la medición.** Aplicada al texto en vez de al código.
>
> Por eso la voz **no es cosmética**: es la misma doctrina de evidencia, en otra superficie.

### 12-S.4 · Por qué es la misma enfermedad que el código

Brian usó **la misma frase** para las dos cosas: *"se siente hecho por IA"*.

| Texto hecho por IA | Código hecho por IA |
|---|---|
| dice mucho, decide nada | funciona, no está bien hecho |
| tres viñetas por costumbre | archivos donde cayeron |
| repite en vez de profundizar | lógica repetida en 6 sitios |
| suena seguro sin serlo | *"está completo"* → *"a medias"* |
| formato en lugar de criterio | patrón en lugar de arquitectura |

> **Causa común: producir la forma correcta sin el juicio detrás.**
> Y el antídoto es el mismo en ambos casos: **que haya algo verificable detrás de cada afirmación.**

### 12-S.5 · Por qué es el ENCARGADO 0 y no un cuarto encargado

Los encargados son **tres y no pueden ser más** (regla de Brian). La voz **no es un cuarto**:
es **transversal** — gobierna cómo los tres se comunican, no qué hacen.

```
        ┌──────── ENCARGADO 0 · LA VOZ ────────┐
        │  (transversal — no es un cuarto)     │
        └──┬─────────────┬─────────────┬───────┘
           ▼             ▼             ▼
      ① documentación ② desarrollo ③ validación
```

Por eso se numera **0**: precede a los tres y no compite con ellos.

---

## 12-SEPTIES · ⭐⭐⭐ HIGIENE DE CONFIGURACIÓN — las 4 reglas

> **El patrón común de los 3 fallos del 2026-07-27:** en los tres la regla existía o era obvia.
> **Lo que faltaba era el mecanismo.** Misma historia que el Método F.

| Fallo medido | La convención existía | Faltaba |
|---|---|---|
| Password **331 veces** en `settings.local.json` | `secrets/` era el sitio correcto | **nada obligó a referenciarlo** |
| **689 rutas absolutas** `/home/brianweb3/` | — | **nada exigió portabilidad** |
| `additionalDirectories` daba acceso a NavigoX | el gate lo prohibía | **nada pidió justificar la ruta** |

---

### 12-S.1 · REGLA 1 — Los secretos se REFERENCIAN, nunca se pegan

```
⛔  sshpass -p '«en secrets/Conectar_Servidor_For3s.md»' ssh brianweb3@for3s
✅  sshpass -p "$FOR3S_SSH_PASS" ssh brianweb3@for3s
```

**Por qué es una regla y no un consejo:** al aprobar un comando, Claude Code **lo archiva literal**
como permiso permanente. Un secreto pegado en un comando aprobado **queda grabado para siempre**.
Medido: **331 entradas** con la contraseña del servidor, en un archivo **sin `.gitignore`**.

| Dónde vive un secreto | Estado |
|---|---|
| `secrets/` (antes `secrets/`) | ✅ ignorado por git |
| Variable de entorno | ✅ nunca en disco |
| **Un comando aprobado** | 🔴 **prohibido** |
| **Un archivo de settings** | 🔴 **prohibido** |

> ⚠️ **Purgar no invalida.** El secreto purgado el 27-jul **sigue en el `.jsonl` de la sesión**
> (los transcripts no se editan). **Todo secreto que se filtró se ROTA, no solo se borra.**

---

### 12-S.2 · REGLA 2 — Toda ruta declara su POR QUÉ

> **Brian:** *"cuando cargue una nueva ruta debe tener un por qué en especial, no solo por cargar."*

**Ninguna ruta entra sin justificación.** Formato obligatorio:

```jsonc
"additionalDirectories": [
  // 2026-07-27 · el proyecto entero · trabajo diario
  "$CLAUDE_PROJECT_DIR"
]
```

**Estado medido de las 9 entradas actuales — ninguna tenía justificación:**

| Entrada | Veredicto |
|---|---|
| `/tmp/h2` | 🔴 **no existe** |
| `.../2a5131d3/scratchpad` | 🔴 **no existe** — sesión muerta el 13-jul |
| `.../repo-backend/__pycache__` | 🔴 **no existe** + contradecía el gate |
| `5M-incubathon` | 🔴 **contradecía el gate de NavigoX** |
| `for3s/Mente/Cuerpo` · `Mente/Doc` · `marca-personal/*` ×2 | 🟡 **4 entradas, misma raíz** |
| `/tmp` | ✅ legítima |

---

### 12-S.3 · ⭐⭐ REGLA 3 — UN MECANISMO, UNA ENTRADA

> **Brian:** *"que las rutas no se creen por crear... aunque se ocupen para otras cosas eso no
> importa, es el mismo mecanismo. **No buscamos volumen, buscamos claridad y certeza.**"*

#### La prueba que decide si una entrada merece existir

> ## ¿Esta entrada autoriza algo que NINGUNA otra ya autoriza?
> Si no → **no entra.**

#### Tres criterios, todos verificables por script

| # | Criterio | Ejemplo medido |
|---|---|---|
| 1 | **Sin solapamiento** — si A contiene a B, B no entra | `/tmp` ya contenía `/tmp/h2` · `5M-incubathon` ya contenía su `__pycache__` |
| 2 | **Sin rutas muertas** — la ruta existe o se borra | **3 de 9** no existían |
| 3 | **Una entrada por MECANISMO, no por invocación** | **234** entradas `Bash(sshpass...)` para un solo mecanismo |

#### La evidencia de por qué esta regla existe

**Los 1,010 permisos agrupados por mecanismo:**

| Patrón | Entradas | Debería ser |
|---|---|---|
| `Bash(sshpass...)` | **234** | 1 |
| `Bash(curl...)` | **139** | 1-2 |
| `Bash(python3...)` | **101** | 1 |
| `Bash(awk...)` · `grep` · `node` | 161 | 3 |

> **234 entradas para "usar sshpass" no es una lista de permisos: es un registro de cada vez que se
> dijo sí.** El mecanismo es uno; las entradas son 234.
>
> **La granularidad correcta es el MECANISMO, no el comando.** `Bash(sshpass *)`, no 234 variantes.

**Con esta regla: las 9 rutas serían 2 · los 1,010 permisos serían ~30.**

---

### 12-S.4 · REGLA 4 — Rutas portables

**Medido:** 689 rutas `/home/brianweb3/` en `settings.local.json` · **9 de 9 hooks** con ruta
absoluta. **Nadie más puede usar esto.**

| ⛔ No portable | ✅ Portable |
|---|---|
| `/home/brianweb3/for3s/Mente` | `$CLAUDE_PROJECT_DIR/Mente` |
| `/home/brianweb3/.claude/hooks/x.js` | `$HOME/.claude/hooks/x.js` |

> ⚠️ **Excepción honesta:** los 9 hooks son de un sistema externo (GSD) con rutas absolutas propias.
> **Se documentan como no portables** en vez de fingir que se arreglan. Un límite declarado es
> ingeniería; un límite oculto es deuda.

---

### 12-S.5 · Lo que `check-health` añade por estas reglas

```
🔴 SECRETS
   · secret-looking values inside settings files
   · secrets pasted into approved commands
   · a secret present in both secrets/ and anywhere else

🔴 PORTABILITY
   · absolute paths tied to one machine
   · additionalDirectories entries with no declared reason

🔴 REDUNDANCY                                    ← regla 3
   · overlapping paths (A contains B)
   · dead paths (target does not exist)
   · N allow entries collapsible into one mechanism
```

> **Los tres fallos del 27-jul habrían salido en el primer arranque.** Vivieron semanas porque
> nada mira.

---

## 13 · SISTEMAS TRANSVERSALES

| Sistema | Qué debe hacer | Estado hoy |
|---|---|---|
| **Apuntadores por índices de memoria** | conectar sin replicar | 🟡 parcial (`Maestro/punteros.tsv`) |
| **Índice que NUNCA miente** | **generado** por `generar-indice` (§12-TER) | 🔴 hoy miente (inventaría 35/188) |
| **Telemetría** | rastro de todo proceso | 🟡 parcial (5/11 sesiones sin registrar) |
| **Caché por bloque** | reutilizable y aislado | 🔴 no existe |
| **Contexto por bloque** | **por tiers** (§11.3) + criterio de suficiencia (§11.4) | 🔴 no existe |
| **Resolución determinista** | ID exacto · sin match → parar (§11.5) | 🔴 no existe |
| **Aislamiento entre bloques** | no leer bloques ajenos por defecto (§11.6) | 🔴 no existe |
| **Validadores** | comprueban **y completan lo derivable** (§12-TER) | 🔴 no existen |
| **Recibo de aprobación** | presentar el cambio bloqueado en 1 pantalla (§12-T.2) | 🔴 no existe |
| **Auto-auditoría del sistema** | `check-health` en `SessionStart` (§12-T.3) | 🔴 **no existe — 3 fallos vivieron semanas** |
| **Higiene de configuración** | 4 reglas: secretos · por qué · no-redundancia · portabilidad (§12-SEPTIES) | 🔴 **no existía — 331 secretos, 689 rutas absolutas** |
| **Límites por tipo de documento** | tabla + *un archivo se parte cuando contiene 2 cosas* (§3.2-QUATER) | 🔴 **no existía — este doc llegó a 2,347 líneas** |
| **Garantía de lectura** | 4 capas + 3 puertas cerradas (§12-QUATER) | 🔴 **no existe — es el fallo del Método F** |
| **QA medible** | código muerto · duplicación · tests (§12-Q.4) | 🔴 **no existe — el juicio cambia con el `/clear`** |
| **QA de criterio** | 6 dimensiones con evidencia exigida (§12-Q.5) | 🔴 **no existe — es lo que diferencia al v2** |
| **La VOZ** | 8 reglas negativas · Encargado 0 (§12-SEXIES) | 🔴 **no existe — nadie escribió el archivo** |
| **Sistema de expertise** | criterio por disciplina | 🔴 no existe |
| **Sistema de aprendizaje** | errores → forma aprendida | 🟡 existe 1 caso, no es sistema |
| **Puentes entre Mente OS** | comunicación controlada | ✅ existe y se cumple |
| **Determinar FOCO** | en qué se enfoca cada bloque | 🔴 no existe |
| **Puertas de entrada/salida** | qué información entra y sale del bloque | 🔴 no existe |

---

## 14 · MIGRACIÓN POR DEMANDA ✅ *(decidido 2026-07-27)*

**Regla:** no se migra en masa. Se migra **cuando se vuelve a tocar**.

| Caso | Qué pasa |
|---|---|
| **Trabajo nuevo** | nace como bloque, siempre |
| **Trabajo viejo que se retoma** | se convierte en bloque **en ese momento**, arrastrando su historia |
| **Lo que nunca se vuelve a tocar** | **no se migra** — queda como archivo histórico |

**Por qué:** migrar algo que no se va a tocar es trabajo sin retorno. Y migrar bajo demanda da algo
mejor: **cada bloque nace con su contexto real fresco**, no reconstruido a la fuerza.

**⭐ Excepción deliberada — el piloto:** la **DEMO** se migra primero y a propósito. Es el bloque
activo y el que más duele. Sirve de prueba real de si el sistema funciona.

---

## 15 · LO QUE NO SE TOCA

> **Brian, 2026-07-27:** *"hay que evaluar qué nos conviene y cómo funciona actualmente, aún no
> está definido al 100%, **porque hay cosas que funcionan muy bien en Mente OS**."*

**Esta sección gobierna la Ronda F0.** El riesgo real de la v2 no es que no funcione: **es que
rompa lo que ya funciona.**

| Pieza | Evidencia medida | Veredicto |
|---|---|---|
| **Capacidad documental** | 188 docs, nada se pierde, continuidad real | ✅ **el mayor logro — se conserva** |
| **Cold-start brief** | arrancar cuesta **38-40K tokens**, constante | ✅ funciona |
| **Gate de Puentes** | 1 solo acceso real, con puente declarado | ✅ **100% de cumplimiento** |
| **Permisos fail-closed** | código real con exit codes | ✅ **100% de cumplimiento** |
| **Registro de Conversaciones** | umbrales calibrados con datos reales | ✅ el diseño es bueno |
| **Regla madre del Método F** | explicar→aprobar→construir | ✅ se conserva y se hace **exigible** |
| **Casos de estudio** | patrón error→método reutilizable | ✅ se sistematiza (§10) |

---

## 16 · PRINCIPIOS DE DISEÑO NO NEGOCIABLES

1. **Mejora continua — no hay reglas inmutables, hay APUNTADORES a reglas.**
2. **No se llaman por palabras reservadas.**
3. **Los estándares mejoran con el criterio del usuario.**
4. **Controlar el proceso de la IA: ejecuta instrucciones claras, no lo hace solo.**
5. **Estandarizar · Trazabilizar · Saber dónde está la data.**
6. **Ser dueño del contexto por bloque** — el disco manda, la conversación es caché.
7. **Conservar la capacidad documental actual.**
8. **Portabilidad:** cualquier IA debe poder operar el sistema.
9. **La IA no inventa criterio.** El criterio es de Brian; la forma es trabajo de la IA.
10. ⭐ **Si hay que PEDIRLO, no está automatizado.** El sistema audita su propia salud sin que Brian
    lo pida (§12-T.3). Y **nunca borra evidencia forense** — de los `.jsonl` salió el incidente del
    21-jul que no estaba documentado.
11. ⭐⭐ **UN MECANISMO, UNA ENTRADA.** *No buscamos volumen, buscamos claridad y certeza* (Brian).
    Sin solapamiento · sin rutas muertas · granularidad = el mecanismo, no la invocación (§12-S.3).
13. ⭐⭐ **Un archivo no se parte por tamaño: se parte cuando contiene DOS COSAS DISTINTAS.**
    El límite es la **señal**, no la causa (§3.2-QUATER). Y **todo tipo de archivo tiene su límite
    declarado** — el único que no se desbordó en v1 fue el único que lo tenía.
12. ⭐ **Los secretos se REFERENCIAN, nunca se pegan.** Y todo secreto filtrado **se ROTA**, no solo
    se borra — purgar no invalida (§12-S.1).

---

## 16-BIS · INCORPORACIONES DE REFERENCIA EXTERNA *(2026-07-27)*

> Análisis completo: **`docs/analysis-internos-v1.md`**.
> Notación interna; lo que se construya **no cita la fuente** (regla LOCKED, Método F §1).

**Hallazgo marco:** un framework independiente y ya estable llegó a **la misma estructura de dos
niveles** que el v2 (su proyecto→workstream ≈ nuestro bloque→sub-bloque) y a la misma doctrina
(archivos = estado · reconstrucción sin transcript · aislamiento por defecto). **Validación externa
del diseño** — y su madurez nos ahorra iteraciones.

### ✅ Lo incorporado — YA INTEGRADO en el cuerpo de este documento

| # | Incorporación | Integrada en |
|---|---|---|
| 1 | **Límites de tamaño por tipo de archivo** | **§3.2-bis** + tabla D de §12-BIS |
| 2 | **Resolución determinista: sin match → PARAR** | **§11.5** |
| 3 | **Carga por TIERS dentro del bloque** | **§11.3** |
| 4 | **Aislamiento ENTRE bloques por defecto** | **§11.6** |
| 5 | **Criterio de suficiencia** (¿el Tier 1 basta para reiniciar?) | **§11.4** + §4 Encargado 3 |
| 6 | **Cierre como PROCEDIMIENTO de 8 pasos** | **§6.1-bis** |
| 7 | **Índice generado con salud** | **§12-TER** + `docs/INDEX.md` 🤖 |
| 8 | **Los 4 validadores** | **§12-TER** ⭐ |
| 9 | **Anidamiento** → ✅ decidido: **máximo 3 niveles** | **§3.1-ter** |

### Lo que NO se copia
Su binding a hilos de chat (Discord/Slack) · la dependencia `tick.md` · `STAKEHOLDERS.md` por
unidad · los adapters por framework · su nomenclatura (**el v2 conserva la suya**).

### Los 3 aprendizajes de fondo

**① La disciplina de tamaño es una función del sistema, no una buena costumbre.**
Ellos ponen el límite en la especificación y lo validan con script. Nosotros lo dejamos como nota:
resultado, 240 KB. **El único archivo nuestro con límite es el único que no se desbordó** (§3.2-bis).

**② "Los archivos son el estado" solo funciona si hay criterio de suficiencia.**
No basta escribir a disco. Sin la prueba del §11.4, escribir a disco es **acumular**, no ser dueño
del contexto.

**③ La respuesta al bloqueante A ya estaba probada:**
> **La doctrina es documento. La verificación es script.** (§12-TER)

---

## 17 · PENDIENTES PARA LA RONDA F0

### 17.1 · Resueltos ✅ *(2026-07-27)*

> 🤖 **FUENTE ÚNICA: `docs/DECISIONS.md`** (generado) + un ADR por decisión en `rules/decisions/`.
> **Esta tabla es un RESUMEN de lectura, no la fuente.** Se borra en F7, cuando el índice se genere
> automáticamente. Contrato: `rules/contract-adr.md`.
> ⚠️ Mientras exista, **está duplicada con `Visión §6`** — motivo por el que se creó el estándar ADR.

| # | Pregunta | Decisión |
|---|---|---|
| 1 | ¿Qué es un bloque? | **Unidad de trabajo** que agrupa tareas con la misma relación. **Sub-bloque = tarea que ataca una pieza de código.** |
| 2 | ¿Para quién es? | Para que la **IA trabaje mejor**, con reglas de expertos, y que **cualquiera tenga el mismo criterio**. |
| 3 | ¿De dónde sale el criterio? | **Brian lo diseña** desde su experiencia. La IA le da forma. |
| 4 | ¿Cuánta fricción? | **3 carriles**; el carril lo decide **la propagación**, no la IA (§5). |
| 5 | ¿Reglas que estorban? | **Cumplir · registrar · seguir · proponer al cerrar.** Excepción: daño real (§8). |
| 6 | ¿Dónde viven los bloques? | **Mente OS, versionado en git.** |
| 7 | ¿El bloque muere al cerrarse? | **No: se archiva como completado, con experiencia de memoria.** |
| 8 | ¿Se migra lo viejo? | **Sí, por demanda.** La demo es el piloto (§14). |
| 9 | **¿Un archivo por bloque o varios?** | **ARCHIVO ÚNICO** (`BLOQUE.md`, secciones A-K, ≤150 líneas). Precedente: `memory/RETOMAR.md` funciona así; la demo dispersa en 5 archivos, no (§3.2-TER). |
| 10 | **¿Régimen de completitud?** | **PROGRESIVO con MÍNIMO DURO**: 4 campos al abrir (A-D), todo al cerrar. *Barato de abrir, caro de cerrar.* |
| 11 | **¿Cómo se garantiza que un archivo se lea?** | **4 CAPAS**: enrutador · el bloque declara · **hook que inyecta o bloquea** · validador al cerrar (§12-QUATER). |
| 12 | **¿Qué acciones BLOQUEAN?** | **Solo 3**: editar pieza con dependientes · tocar BD · cerrar sin suficiencia. **Todo lo demás avisa.** |
| 13 | ⭐⭐⭐ **¿Cómo se sabe si es producto o MVP?** | **VEREDICTO EN 2 CAPAS** (§12-QUINQUIES): medible por script + criterio en 6 dimensiones **con evidencia exigida**. Regla madre: **la IA no declara "está bien", reporta la medición**. |
| 14 | **¿Quién aporta el criterio de QA?** | **Brian** — sus 6 dimensiones por disciplina en `Alma/expertise/*`. La IA **aplica y trae evidencia**, no opina. Es lo que hace que *"se sienta hecho por un senior"*. |
| 15 | **¿Cuántos niveles de anidamiento?** | ✅ **MÁXIMO 3** — `BLOQUE › GRUPO › SUB-BLOQUE` (§3.1-ter). El grupo es opcional; el nivel 3 es tope duro. |
| 16 | **¿Cómo se migran las carpetas?** | ✅ **LA ESTRUCTURA NUEVA CONVIVE** — se crean las carpetas nuevas SIN tocar los 188 docs. Cero punteros rotos (§12.1). |
| 17 | **¿Cómo se consulta el aprendizaje?** | ✅ **El bloque los declara (§D) + el hook los inyecta** — mismo mecanismo que los estándares. No se inventa uno nuevo (§10.4). |
| 27 | ⭐⭐⭐ **¿Cómo se controla el tamaño de TODO, no solo de los bloques?** | **Tabla de límites por TIPO** (§3.2-QUATER): puerta ≤200 · regla ≤250 · **arquitectura ≤800** · plan ≤400 · `BLOCK.md` ≤150 · `MEMORY.md` ≤80 · append-only **sin límite pero con rotación anual** · índices generados. **Regla madre: un archivo se parte cuando contiene DOS COSAS DISTINTAS — el límite es la señal.** Medido: este doc llegó a **2,347 líneas** (+1,352 en una sesión) y `RETOMAR`, el único con límite, es el único que no se desbordó. |
| 25 | ⭐⭐⭐ **¿Cómo se evita que la config se degrade?** | **4 reglas de higiene** (§12-SEPTIES): ① secretos se referencian, nunca se pegan · ② toda ruta declara su POR QUÉ · ③ ⭐ **un mecanismo, una entrada** (*no buscamos volumen, buscamos claridad*) · ④ rutas portables. Medido: 331 secretos · 689 rutas absolutas · 3 de 9 rutas muertas · **234 entradas para un solo mecanismo**. |
| 26 | **¿La granularidad de un permiso?** | **El MECANISMO, no la invocación.** `Bash(sshpass *)` en vez de 234 variantes literales. Prueba: *¿esta entrada autoriza algo que ninguna otra ya autoriza?* Si no, no entra. |
| 24 | ⭐⭐ **¿Quién vigila la salud del sistema?** | **`bin/check-health`, y corre SOLO en `SessionStart`** (§12-T.3). Regla: **si hay que pedirlo, no está automatizado.** Motivo medido: 3 fallos (permisos contradictorios · registro que miente · 999 archivos viejos) vivieron **semanas** y los encontró Brian preguntando. ⛔ Nunca borra evidencia forense. |
| 23 | ⭐⭐ **¿En qué idioma va el sistema?** | **Todo lo que la IA lee como INSTRUCCIÓN en 🇺🇸 inglés de EE.UU.** (incluido `BLOCK.md`, los owners, los contratos, las reglas, los casos, la salida de los validadores). **El pensamiento de Brian en 🇪🇸** (visión, plan, análisis, RETOMAR, bitácora, memorias). Vocabulario canónico traducido: block · owner · lane · scope IN/OUT · friction · quality verdict (§0-BIS). |
| 21 | **¿Cuándo un error merece ser caso?** | **Prueba de 3 preguntas** (¿otro sitio? ¿criterio equivocado? ¿regla accionable?) + **umbral automático a las 2 repeticiones** + **límite de 12 casos activos** (§10.5). |
| 22 | **¿Cómo se detecta una regla que estorba?** | **Aritmética, no interpretación:** roce de 4 campos · dispara a los **3 bloques DISTINTOS** · **no caduca** · ⛔ la regla **no se cambia sola, se eleva a Brian** (§10.6). |
| 19 | ⭐ **¿Los validadores solo verifican?** | **NO — COMPLETAN lo derivable** (grafo, índice, borradores marcados `auto:`). ⛔ Nunca completan criterio, alcance ni veredicto (§12-T.1). Motivo: un validador que solo avisa habría avisado 5 veces y seguiríamos con 5 sesiones sin registrar. |
| 20 | ⭐ **¿Qué pasa cuando una puerta bloquea?** | **RECIBO DE APROBACIÓN** en 1 pantalla: pieza · propagación · evaluación de la construcción · aprobar/ver/no (§12-T.2). Convierte el bloqueo en decisión de 10 segundos. |
| 18 | ⭐⭐ **¿Mente OS gobierna también cómo se comunica?** | ✅ **SÍ — ENCARGADO 0 · LA VOZ** (§12-SEXIES). 8 reglas **negativas y verificables**. Transversal, no un cuarto encargado. Medido: no había NADA configurado — *"se siente hecho por IA" viene de que nadie escribió el archivo*. |

### 17.2 · Abiertos — solo quedan 2 preguntas, ambas en la fase F0

> ✅ **Todos los bloqueantes estructurales están resueltos.** Lo que queda son 2 criterios del
> sistema de aprendizaje, que se cierran en **F0** del plan (tickets F0-1 y F0-2):
> 1. ¿Cuándo un error **merece** convertirse en caso? (no todos lo merecen)
> 2. ¿Cómo se detecta que una regla estorbó **3 veces** y debe revisarse?

**Histórico de los bloqueantes (todos cerrados):**

| # | Pendiente | Por qué bloquea |
|---|---|---|
| ~~A~~ | ~~¿Qué va a código y qué queda documento?~~ | ✅ **RESUELTO (§12-TER):** *la doctrina es documento, la verificación es script*. **4 validadores definidos.** |
| ~~B~~ | ~~¿Los encargados son documentos o ejecutables?~~ | ✅ **RESUELTO:** documentos, **verificados** por validadores (§12-TER) e **inyectados** por hooks (§12-QUATER). |


| ~~E~~ | ~~Plan de implementación con fases y tickets~~ | ✅ **RESUELTO:** `docs/plan-v2-rollout.md` — **9 fases · 38 tickets · 4 leyes del orden**. |


---

👉 **Plan de construcción: `docs/plan-v2-rollout.md`** (9 fases · 38 tickets · las 4 leyes del orden).

Relacionado: `principles/vision-mente-os-v2.md` (el porqué + el diagnóstico medido) ·
`rules/ESTANDAR_Metodo_Fases_F.md` (se absorbe en los encargados) ·
`memory/archive/CASO_Default_Peligroso_Tema_Hilo.md` (el patrón de caso reutilizable, semilla de §10) ·
[[project_mente_os_v2_bloques]] · [[project_ser_duenos_del_contexto]] ·
[[project_incidente_degradacion_21jul]].

---

Related: `principles/vision-mente-os-v2.md` (el porqué) · `docs/architecture/how-it-runs.md` (el flujo) · `rules/contract-block.md` (la forma que impone).
