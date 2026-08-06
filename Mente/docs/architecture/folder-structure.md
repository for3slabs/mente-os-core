# ARCHITECTURE · folder structure and file inventory

**Status:** current · **Type:** architecture · **Updated:** 2026-07-30 · **Owner:** brian
**Part of:** `docs/Arquitectura_Mente_OS_v2_Bloques.md` (§12, §12.0-BIS, §12.1, §12-BIS) ·
**Block:** `blk-split-architecture-2026-07`

## Purpose

The declared folder tree, how the migration coexists with the old structure, and the inventory of
what is used, created or reused.

⚠️ **This document ILLUSTRATES. `Maestro/piezas.tsv` DEFINES.** The canonical location of every key
piece lives in that table, read by `bin/check-structure`. A diagram nobody can run is a diagram
that drifts — which is exactly what happened here (§12.0-BIS).

Extracted verbatim on 2026-07-30 (270 lines). **Moved, not rewritten.**

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
    ├── bridges/Puentes_Mente_OS.md ....... 🌉 el gate a otro Mente OS
    │                                      ⚠️ NO se mudó a Tickets/ — ver §12.0-BIS
    ├── Maestro/ ...................... 🗂️ repo APARTE (raíz propia, remoto propio)
    │   ├── punteros.tsv ................... fuente única de RAMAS
    │   ├── piezas.tsv ..................... 🆕 fuente única de dónde vive cada PIEZA
    │   └── registro.md .................... las ramas que el Maestro conoce
    ├── Tickets/ ...................... 📋 tickets H1-H4 (histórico · NO es el puente)
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
**MAYÚSCULAS solo para puertas de entrada:** `CLAUDE.md` · `memory/archive/README.md` · `memory/RETOMAR.md` · `BLOCK.md`.

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

## 3 · INVENTARIO DE ARCHIVOS — qué se ocupa, qué se crea, qué se reusa

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
| `.claude/output-styles/for3s.md` 🇺🇸 | 🆕 **nuevo** | ⭐ el vehículo · **mayor peso del sistema** | IA construye |
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

Related: `docs/Arquitectura_Mente_OS_v2_Bloques.md` (entry point) · `Maestro/piezas.tsv`
(⭐ the canonical locations) · `bin/check-structure` (verifies the tree) ·
`rules/NAMING_CONVENTION.md`.
