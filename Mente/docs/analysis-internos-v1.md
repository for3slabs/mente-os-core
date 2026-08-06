# 🔬 ANÁLISIS — internOS v1.0.0 → qué incorporar al Mente OS v2
**Status:** current · **Type:** analysis · **Updated:** 2026-07-29 · **Owner:** brian
**Fecha:** 2026-07-27 · **Repo:** `github.com/fruteroclub/intern-os` · **Versión analizada:** v1.0.0 (2026-07-24)
**Petición de Brian:** *"analizar a detalle para ver qué podemos incorporar, la estructura está muy buena con ese v2"*

## Purpose

Qué de internOS v1.0.0 vale la pena incorporar a Mente OS v2, y qué no. Es el cuarto framework
analizado; los tres primeros están en `docs/analysis-frameworks-v2.md`.

> ✅ **ESTADO (2026-07-27): las 9 incorporaciones YA ESTÁN INTEGRADAS** en el plano
> (`Cuerpo/Arquitectura_Mente_OS_v2_Bloques.md`). Este documento queda como **registro del análisis
> y su trazabilidad** — ver §6 para el mapa de dónde quedó cada una.
>
> ⚠️ **Notación INTERNA de Mente OS.** Aquí se nombra la fuente para el análisis; **el código o los
> documentos que salgan NO citan el origen** (regla LOCKED, Método F §1).
> **Análisis previos:** `docs/analysis/Analisis_internOS_vs_For3s_OS.md` (2026-06-23, v0.4.1, 62 archivos) ·
> `docs/analysis/Analisis_intern-os_para_For3s.md` (2026-07-01). **Este doc cubre lo NUEVO de v1.0.0 y su
> cruce específico con el v2 de bloques.**
---

## 1 · QUÉ CAMBIÓ desde nuestro último análisis (v0.4.1 → v1.0.0)

| Versión | Aporte relevante para el v2 |
|---|---|
| **v1.0.0** (24-jul) | **Primera versión estable.** Patrón de **proyecto anidado**: workstreams a cualquier profundidad (`projects/club/club-app/workstreams/`). Resolver que hace match a cualquier nivel |
| v0.5.0-α.1 | **`session-wrap`**: skill que **cura las decisiones de la sesión y escribe checkpoints** ⭐ |
| v0.5.0-α.1 | **`export-sessions`**: migración de proyecto completo con bundles cifrados |
| v0.5.0-α.0 | **Transfer Modules (TM)**: estándar de estructura base + tipo engagement-delivery |
| v0.5.0-α.0 | Convención de git en 3 niveles (workspace-repo / project-repo / clones en `code/`) |
| v0.4.0 | **Isolated-session handoff con manifest verificable** |

**Lo importante:** desde nuestro análisis pasó de alpha a **estable**, y añadió justo las piezas que
al v2 le faltan: **checkpoints curados, contenedores anidados y validación por scripts**.

---

## 2 · SU ARQUITECTURA (las 3 capas)

| Capa | Qué hace | Equivalente en Mente OS v2 |
|---|---|---|
| **Storage** | los archivos del workstream **son** el estado autoritativo | ✅ mismo principio: *el disco es la fuente de verdad* |
| **Resolution** | `thread_id` en BRIEF.md = binding **exacto** hilo↔workstream | ✅ **incorporado**: ID único por bloque (§11.5) |
| **Runtime** | carga por **tiers**: solo lo necesario del turno | ✅ **incorporado**: tiers dentro del archivo (§11.3) |

### Su equivalencia conceptual con nuestros bloques

| internOS | Mente OS v2 | ¿Coinciden? |
|---|---|---|
| **Project** | **BLOQUE** (unidad de trabajo) | ✅ casi idéntico |
| **Workstream** | **SUB-BLOQUE** (tarea → pieza de código) | ✅ casi idéntico |
| `projects/[p]/workstreams/[w]/` | `Cuerpo/_activos/<BLOQUE>/sub-bloques/` | ✅ misma forma |

> ⭐ **Hallazgo mayor:** llegamos por caminos distintos a **la misma estructura de dos niveles**.
> Eso valida el diseño del v2 — y significa que su especificación, ya probada en producción, se
> puede aprovechar sin rediseñar nada.

---

## 3 · SUS ARCHIVOS DE ESTADO vs LOS CAMPOS DEL v2

| Archivo suyo | Contenido | Límite | En el v2 |
|---|---|---|---|
| **BRIEF.md** | identidad + `thread_id` + objetivo | — | ✅ **§A-D** del `BLOQUE.md` (≤60 líneas) |
| **STATUS.md** | **phase · next · blockers · owner · updated** | **≤10 líneas** | ✅ **§E** — mismo límite de 10 |
| **MEMORY.md** | contexto durable **curado, NO log** | **≤80 (meta ≤50)** | ✅ **§J** — mismo límite |
| **DECISIONS.md** | decisión + fecha + **rationale** | — | ✅ **§G** |
| **STAKEHOLDERS.md** | quién es quién | — | ⛔ **descartado a propósito** (Brian es dueño de casi todo) |
| **RESOURCES.md** | registro de artefactos | — | ⛔ descartado |
| **docs/** | artefactos de trabajo | — | ✅ `docs/` del bloque |

> ⚠️ **Diferencia de diseño deliberada:** ellos usan **7 archivos por unidad**; el v2 usa **UNO**
> con secciones. Motivo medido: `memory/RETOMAR.md` (1 archivo, 203 líneas) es lo que mejor funciona en
> Mente OS; la demo dispersa en 5 archivos es lo que peor funciona. Ver §3.2-TER del plano.

**A nivel proyecto:** `PROJECT.md` (propósito, alcance, dueño humano, objetivo, criterios de éxito,
**fecha de archivado**) · `AGENTS.md` (contexto para el agente) · `TICK.md` (tareas).

---

## 4 · ⭐ LO QUE HAY QUE INCORPORAR (ordenado por valor)

### 🥇 4.1 · LÍMITES DE TAMAÑO POR ARCHIVO — *lo más valioso*

> `STATUS.md` **≤10 líneas** · `MEMORY.md` **≤80 líneas, meta ≤50** · *"resumen curado, nunca un log
> crudo"* · *"la cronología detallada va en docs/, no en MEMORY"* · *"consolidar ANTES del cierre de
> sesión, no después"* · **un script valida el conteo**.

**Por qué nos importa, con nuestros datos:**

| Nuestro archivo | Tamaño | Problema |
|---|---|---|
| `memory/PENDIENTES.md` | **240 KB** | ilegible; se lee 39 veces en una sesión |
| `memory/Estado_Sesion_Continuidad.md` | 196 KB | fósil que sigue vivo |
| `memory/Bitacora_Progreso.md` | 162 KB | crece sin recorte |
| `MEMORY.md` (memorias) | 19.5 KB | **la pieza más pesada del arranque, sin regla** |
| `memory/RETOMAR.md` | 14.4 KB | ✅ **tiene límite (~200 líneas) y funciona** |

**El único archivo nuestro con límite es el único que no se desbordó.** Eso confirma la regla.

**→ INCORPORAR:** límite declarado **por tipo de archivo** en `rules/contract-block.md` y
`rules/contract-document.md`, con **validador que lo verifique** (no una nota de buena voluntad).

### 🥈 4.2 · RESOLUCIÓN DETERMINISTA — *"exacta, determinista, no heurística"*

> *"Match exacto por `thread_id` en BRIEF.md — nunca fuzzy ni inferencia heurística.
> **Si no hay match: PARAR y PREGUNTAR — nunca adivinar.**"*

**Esto es literalmente la regla que el v2 ya pide** (*"si el bloque falta o está incompleto, la IA lo
dice en voz alta en vez de inferir"*) — pero ellos la tienen **especificada y verificada por script**.

**→ INCORPORAR:** un **identificador único por bloque** (equivalente a su `thread_id`) que ate el
bloque a su conversación/trabajo, y la regla dura **"sin match → parar y preguntar"**.

### 🥉 4.3 · CARGA POR TIERS — el contexto por bloque, mejor resuelto

| Tier | Qué carga |
|---|---|
| **1 · por defecto** | BRIEF + STATUS (identidad + estado) |
| **2 · a demanda** | DECISIONS + STAKEHOLDERS |
| **3 · a demanda** | MEMORY + RESOURCES + docs/ |

Y un **protocolo de arranque por plataforma**: LIGHT (ACK primero, luego archivos) vs FULL.

**→ INCORPORAR:** el bloque del v2 **no se carga entero**. Por defecto: **límites + estado**.
El resto (decisiones, contexto, sub-bloques) a demanda. Es la pirámide de coste del cold-start,
aplicada dentro del bloque.

### 4.4 · DOCTRINA DE AISLAMIENTO — *directamente aplicable*

> *"No leer archivos de otro workstream por defecto · no escanear ampliamente · **no inferir por
> nombres parecidos** · la síntesis cruzada requiere petición humana explícita."*

**Es nuestro gate de Puentes, pero aplicado ENTRE bloques.** Hoy no tenemos nada que impida a la IA
leer bloques ajenos "por contexto" — el mismo problema de consumo que el gate ya resolvió a nivel
de Mente OS.

**→ INCORPORAR:** aislamiento entre bloques por defecto; cruzar bloques requiere petición explícita.

### 4.5 · DOCTRINA DE RECUPERACIÓN — *la respuesta a "ser dueños del contexto"*

> *"En sesiones degradadas o reseteadas: **reconstruir desde los archivos, NO desde el transcript**.
> BRIEF + STATUS deben bastar para reiniciar con seguridad."*

**Esta es exactamente nuestra pregunta de hoy, con criterio de aceptación medible:**
**¿bastan los 2 archivos por defecto para reiniciar?** Si no, el bloque está mal escrito.

**→ INCORPORAR:** como **criterio de validación** del Encargado 3 — un bloque no se cierra si no se
puede reconstruir desde sus archivos por defecto.

### 4.6 · `session-wrap` — checkpoint curado ⭐ *(v0.5.0, nuevo desde nuestro análisis)*

Skill que **cura las decisiones de la sesión y escribe el checkpoint**.

**Ataca nuestro fallo medido:** 5 de 11 sesiones nunca se registraron · 8 auto-compactaciones sin
revisar. Y su regla *"consolidar ANTES del cierre, no después"* es idéntica a la nuestra
(*"se escribe durante, no al final"*) — pero ellos la tienen **como herramienta, no como intención**.

**→ INCORPORAR:** el cierre de bloque como **procedimiento con pasos fijos**, no como voluntad.

### 4.7 · SCRIPTS DE VALIDACIÓN — *el puente entre documento y código*

| Script | Qué valida |
|---|---|
| `sync-check.sh` | archivos presentes · formato/unicidad de IDs · **límites de tamaño** |
| `generate-registry.sh` | **genera** el índice de todos los workstreams |
| `checkpoint-reminder.sh` | detecta STATUS obsoletos |
| `verify-handoff.sh` | valida el manifest de delegación |

**⭐ ESTO RESUELVE NUESTRO BLOQUEANTE A** (*"¿qué va a código y qué queda documento?"*).

Su respuesta es elegante: **la doctrina es documento; la VERIFICACIÓN es script.** No intentan que
un script tome decisiones — solo que compruebe lo comprobable (existe / tiene el campo / cabe en el
límite / el ID es único).

**Cruza con nuestra ley medida:** documento = falla 40-60% · código = 100%.
**→ INCORPORAR:** un `sync-check` de bloques + un **`generate-registry` que produzca el índice que
hoy miente** (35 de 188).

### 4.8 · REGISTRY generado — el índice que no puede mentir

`projects/REGISTRY.md` **generado por script**, con: proyecto · thread_id · fase · dueño · **salud** · ruta.

**→ INCORPORAR:** exactamente lo que el v2 llama `docs/INDEX.md` 🤖 y `docs/STATES.md` 🤖.
Ellos ya tienen el precedente funcionando: **incluye "salud"**, que nosotros no habíamos previsto.

### 4.9 · Proyectos ANIDADOS a cualquier profundidad *(v1.0.0)*

`projects/club/club-app/workstreams/` — el resolver hace match a cualquier nivel.

**→ EVALUAR:** ¿un bloque puede contener bloques, o solo bloque→sub-bloque (2 niveles)? Hoy el v2
define 2 niveles. Su v1.0.0 sugiere que en la práctica **hacen falta más**.
⚠️ Decisión de Brian — afecta al diseño del grafo.

### 4.10 · Handoff aislado con manifest verificable

Manifest en `<workstream>/handoffs/<id>.yml` que declara: qué debe cargar el especialista, su tarea,
y **dónde escribe**. **Ámbito de escritura acotado** (el especialista NO puede tocar BRIEF/STATUS/
DECISIONS — son del coordinador). Verificado por script.

**→ INCORPORAR:** si un bloque delega en un sub-agente, el manifest declara qué carga y **qué puede
escribir**. Conecta con nuestro caso real: los 421 comandos Bash sin subagentes del 20-jul.

---

## 5 · LO QUE **NO** DEBEMOS COPIAR

| Suyo | Por qué NO |
|---|---|
| `thread_id` atado a Discord/Slack/Telegram | Nuestro bloque no se ata a un hilo de chat, sino a una **unidad de trabajo** |
| Integración `tick.md` | Dependencia externa; ya tenemos `memory/PENDIENTES.md` (a arreglar, no a reemplazar) |
| `STAKEHOLDERS.md` por workstream | Brian es dueño de casi todo; sería burocracia sin uso |
| Adapters por framework | Nuestra portabilidad es **un protocolo legible**, no adapters por herramienta |
| Su nomenclatura completa | El v2 ya tiene la suya (bloque/sub-bloque/encargados) — **no renombrar lo decidido** |

> **Diferencia de fondo:** internOS es **0 infraestructura** (markdown + bash). Mente OS tiene
> agente + Postgres + grafo + memoria semántica. **Lo valioso son sus CONCEPTOS y su disciplina de
> tamaño**, no su implementación.

---

## 6 · ✅ TRAZABILIDAD — dónde quedó cada incorporación

| # | Qué se incorporó | Sección del plano | Estado |
|---|---|---|---|
| 1 | **Límites de tamaño por archivo** | **§3.2-bis** + tabla D de §12-BIS | ✅ integrado |
| 2 | **Resolución determinista + "sin match, parar"** | **§11.5** | ✅ integrado |
| 3 | **Carga por tiers dentro del bloque** | **§11.3** | ✅ integrado |
| 4 | **Aislamiento entre bloques** | **§11.6** | ✅ integrado |
| 5 | **Criterio de suficiencia como cierre** | **§11.4** + §4 Encargado 3 | ✅ integrado |
| 6 | **Validadores** → resolvió el bloqueante A | **§12-TER** (4 scripts) | ✅ **resolvió el bloqueante** |
| 7 | **Índice generado con salud** | **§12-TER** · `docs/INDEX.md` 🤖 | ✅ integrado |
| 8 | **Cierre como procedimiento** | **§6.1-bis** (8 pasos) | ✅ integrado |
| 9 | **Manifest de delegación acotado** | §4 encargados | 🟡 anotado, sin detallar |
| 10 | **Anidamiento** | **§3.1-ter** | ✅ **decidido: máximo 3 niveles** |

### Lo que el v2 añadió y NO viene de aquí

Estas piezas son propias y **no existen en la referencia externa** — son el diferenciador del v2:

| Pieza | Sección |
|---|---|
| ⭐⭐⭐ **Veredicto de calidad en 2 capas** (¿producto o MVP?) | §12-QUINQUIES |
| ⭐⭐ **QA de criterio: 6 dimensiones con evidencia exigida** | §12-Q.5 |
| ⭐⭐ **LA VOZ · Encargado 0** | §12-SEXIES |
| **Fix ≠ parche** | §7 |
| **3 carriles de fricción** decididos por propagación | §5 |
| **Protocolo del roce** (evolución de reglas) | §8 |
| **Las 3 puertas cerradas** | §12-QUATER |

> **Ellos resolvieron coordinación. El v2 resuelve coordinación + calidad verificable.**
> Es una categoría distinta.

---

## 7 · LOS 3 APRENDIZAJES DE FONDO

**① La disciplina de tamaño es una función del sistema, no una buena costumbre.**
Ellos ponen el límite **en la especificación** y lo **validan con script**. Nosotros lo dejamos como
nota: resultado, 240 KB. **El único archivo nuestro con límite es el único que no se desbordó.**

**② "Los archivos son el estado" solo funciona si hay criterio de suficiencia.**
No basta escribir a disco. Su prueba es concreta: *¿BRIEF + STATUS bastan para reiniciar con
seguridad?* Sin esa prueba, escribir a disco es acumular, no ser dueño del contexto.

**③ La respuesta al bloqueante A ya existe y está probada.**
> **La doctrina es documento. La verificación es script.**
El script no decide — comprueba lo comprobable: existe · tiene el campo · cabe en el límite · el ID
es único · no está obsoleto. **Eso es exactamente lo que convierte una regla que falla el 40-60% en
una que se cumple.**

---

## 8 · VALIDACIÓN CRUZADA DEL v2

Que un framework **independiente, en producción y ya estable** haya llegado a la misma estructura de
dos niveles (proyecto→workstream ≈ bloque→sub-bloque), a la misma doctrina (archivos = estado,
reconstrucción sin transcript, aislamiento por defecto) y a las mismas necesidades (índice generado,
checkpoints curados) **es evidencia externa de que el diseño del v2 va bien encaminado.**

La diferencia está en la **madurez**: ellos llevan v1.0.0 y 15 versiones de iteración; nosotros
tenemos el plano. **Podemos saltarnos varias de esas iteraciones.**

---

Relacionado: `Cuerpo/Arquitectura_Mente_OS_v2_Bloques.md` (el plano) ·
`principles/vision-mente-os-v2.md` (el porqué) ·
`docs/analysis/Analisis_internOS_vs_For3s_OS.md` + `docs/analysis/Analisis_intern-os_para_For3s.md` (análisis previos, v0.4.1) ·
[[project_intern_os_adopcion]] (lo ya adoptado: AI1-AI7, C1-C3) · [[project_mente_os_v2_bloques]].

---

Related: `docs/analysis-frameworks-v2.md` (el análisis hermano) · `memory/PENDIENTES.md` (dónde aterrizaron sus hallazgos).
