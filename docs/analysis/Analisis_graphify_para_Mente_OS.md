# ANÁLISIS MAESTRO · graphify vs Mente OS v2 — qué nos falta
**Status:** current · **Type:** analysis · **Updated:** 2026-08-05 · **Owner:** brian
**Fuente:** `github.com/Graphify-Labs/graphify` v0.9.33 · clonado en `~/for3s/Varios/graphify`
**Verified by:** medición directa sobre el clon (776 archivos, 281 `.py`, 361 `.md`, 17 MB)
**Licencia:** Apache-2.0 + MIT · **Producto:** YC S26, en PyPI (`graphifyy`), con Discord y clientes

---

## Purpose

Desmontar `graphify` pieza por pieza para responder **una** pregunta: qué tiene resuelto que
Mente OS v2 no, y qué de eso vale traer. No es directiva de copiar — es identificar huecos.

> ⛔ **Lo que NO es este documento:** una propuesta de adoptar `graphify`. Son productos distintos
> (uno mapea código en un grafo; el otro gobierna cómo se trabaja). Lo que se compara es **cómo
> están construidos**, no qué hacen.

---

## 1 · QUÉ ES, medido

**Un CLI en Python que convierte un repo en un grafo de conocimiento consultable**, sin LLM ni
embeddings para el código: parsea con tree-sitter (AST), resuelve referencias entre archivos y
exporta `graph.json` + `graph.html` + un informe. ~40 lenguajes.

| Dato | Valor |
|---|---|
| Código | **~35,000 líneas** de Python (`extract.py` solo, 5,985) |
| Tests | 🔴 **180 archivos · 62,159 líneas** — casi **2:1** contra el código |
| Plataformas soportadas | **18** asistentes (Claude Code, Cursor, Codex, Copilot, Gemini…) |
| Versión | 0.9.33 — pre-1.0, y lo declara |
| CI | 3 workflows: `ci` · `publish` · `release-graph` |

**El pipeline son 7 funciones puras**, cada una en su módulo, comunicadas por dicts y grafos
NetworkX: `detect → extract → build_graph → cluster → analyze → report → export`.
*"No shared state, no side effects outside `graphify-out/`."*

---

## 2 · ⭐ LOS 6 HUECOS REALES DE MENTE OS QUE ESTE PROYECTO EXPONE

Ordenados por lo que costaría no tenerlos.

### 2.1 🔴 GENERADOR ÚNICO + CI QUE CAZA LA DERIVA — `tools/skillgen`

**Lo que hacen:** los 18 adapters **no se editan a mano**. Un humano edita *fragmentos*
(`tools/skillgen/fragments/`) y un generador renderiza los artefactos comprometidos. El CI corre
**cinco** comprobaciones sobre eso:

```
--check                 diff byte a byte: render vs lo comprometido → falla si hay deriva
--audit-coverage        cada encabezado de cada host aterriza en su render exactamente una vez
--schema-singleton      el enum compartido es byte-idéntico en todas partes
--monolith-roundtrip    cada versión monolítica reproduce la fuente
--always-on-roundtrip   cada bloque always-on reproduce su constante anterior
```

> *"Fragments are the single source of truth a human edits; the files under `graphify/skill*.md`
> are generated, committed artifacts. This module renders those artifacts **and guards them
> against drift**."*

**⭐ POR QUÉ ESTO ES EL HALLAZGO PRINCIPAL PARA TI.** Es exactamente el defecto que esta sesión
cazó **cinco veces**: una pieza escrita y no cableada · dueños declarando `pending` lo ya lleno ·
`CAPABILITIES.md` sin las piezas nuevas · un techo viviendo en 9 sitios · el conteo de la batería
copiado a mano. Mente OS lo ataca **a posteriori**, con checks que detectan el desfase; `graphify`
lo hace **imposible**: si el artefacto no se genera desde la fuente, el CI no pasa.

**Mente OS ya tiene la mitad:** `bin/generate-index` y `bin/generate-metrics` generan. Lo que
**no** tiene es el `--check` que falla cuando lo comprometido difiere del render.

---

### 2.2 🔴 EL RATIO DE TESTS — 2:1

| | Tests | Código | Ratio |
|---|---|---|---|
| `graphify` | **62,159** líneas | ~35,000 | **1.8 : 1** |
| Mente OS v2 | la batería, **173 checks** | 6,059 líneas | — |
| `blk-demo` (el producto) | 🔴 **0 archivos de test** | — | **0** |

⚠️ **La comparación honesta:** los 173 checks de Mente OS **no son tests unitarios** — son
verificaciones de sistema, y son buenas (incluida una sección `SELF-TEST` que rompe sus propios
checks a propósito, algo que `graphify` **no** tiene). Pero el producto que Mente OS gobierna
tiene cero tests, y eso es lo que su propio `grade-block` marca 🔴 desde el 26 de julio.

**Un archivo de test por módulo**, y la regla escrita: *"All tests are pure unit tests — no network
calls, no file system side effects outside `tmp_path`."*

---

### 2.3 🔴 ESCRIBIR CONFIG AJENA SIN DESTRUIRLA — `install.py`

Tres piezas, cada una nacida de un bug real con número de issue:

| Pieza | Qué hace | El bug que la creó |
|---|---|---|
| `_refuse_to_modify()` | si el JSON no parsea, **aborta** en vez de reescribirlo | #2167 — el fallback a `{}` reescribía el archivo entero y **destruía toda la config del usuario** |
| `_write_settings_with_backup()` | copia a `.graphify-bak` antes de escribir; **omite la escritura si el resultado es idéntico** | idempotencia: sin churn de mtime ni de backups |
| `_replace_or_append_section()` | reemplaza su sección por marcador **exacto a columna 0** | #1688 — el match por substring anclaba en una mención dentro de una viñeta y **borraba contenido curado a mano** |

**Por qué te aplica directo:** `bin/init` de Mente OS **genera** `CLAUDE.md`, `PROJECT-RULES.md` y
toca `.claude/settings.json` — archivos que un usuario ya tiene y ha editado a mano. Ninguna de las
tres protecciones existe hoy. Y tienes registrado que **el harness reescribe `settings.local.json`
en cada aprobación**, así que el escenario no es hipotético.

---

### 2.4 🟡 SEGURIDAD DE ENTRADA EXTERNA — `security.py`

Todo lo externo pasa por un único módulo antes de usarse:

- `validate_url()` — solo http/https, **bloquea redirecciones a `file://`**
- `_ip_is_blocked()` — bloquea IP privadas, loopback, **CGNAT (100.64/10)**, **NAT64**, y hosts de
  metadatos de nube (`metadata.google.internal`) → defensa **SSRF** explícita
- `safe_fetch()` — tope duro de 50 MB, timeout
- `validate_graph_path()` — la ruta debe resolver **dentro** de `graphify-out/`
- `sanitize_label()` — quita caracteres de control, tope 256, escapa HTML

**Mente OS es local y no descarga nada**, así que la mayor parte no aplica. **Lo que sí aplica es
la forma:** un módulo único por el que pasa toda entrada externa, en vez de validaciones dispersas.
El día que Mente OS lea algo remoto —o que un clon ajeno lo haga— esa capa no existe.

---

### 2.5 🟡 MEMORIA DE TRABAJO DETERMINISTA — `reflect.py`

`graphify reflect` lee las respuestas guardadas de sesiones anteriores y produce **un artefacto de
lecciones** que el agente carga al empezar la siguiente:

| Categoría | Qué es |
|---|---|
| **Preferred sources** | nodos corroborados por varias respuestas útiles |
| **Tentative** | vistos útiles una sola vez, aún sin corroborar |
| **Contested** | con señales positivas Y negativas — **decide la recencia** |
| **Known dead ends** | marcados como callejón sin salida: **no volver a derivarlos** |
| **Corrections** | lo que el usuario corrigió, y cuál era la respuesta correcta |

*"Source nodes are scored, not counted: each citation contributes a signed, time-decayed value."*

**Comparado con Mente OS:** tu §H fricción + `memory/` + `rules/case-*.md` cubren esto **mejor en
riqueza** (llevan el porqué, no solo la señal). Lo que `graphify` tiene y tú no es que **es
automático y puntuado** — no depende de que alguien se acuerde de escribirlo.

---

### 2.6 🟡 BENCHMARKS CON JUEZ VALIDADO

No dicen *"somos mejores"*: publican el método.

- Mismo harness, mismo modelo, mismos presupuestos para todos los sistemas comparados
- **Juez validado a ciegas contra un segundo juez independiente: 90.6% de acuerdo, kappa de Cohen 0.81**
- Reglas de imparcialidad y comandos de reproducción publicados
- Declaran explícitamente: *"Most published memory benchmarks disclose no judge validation at all"*

**Lo que esto significa para Mente OS:** es la versión externa de tu propia ley — *no declara que
está bien, reporta la medición*. Tú la aplicas **hacia dentro** (la batería). Ellos la aplican
**hacia fuera**, frente a competidores. Ese segundo movimiento es el que convierte una medición en
un argumento de venta, y es justo lo que te falta para la prueba de campo.

---

## 3 · LO QUE MENTE OS TIENE Y `graphify` NO

No todo es traer. Medido sobre el clon:

| Capacidad | Mente OS v2 | graphify |
|---|---|---|
| **Criterio del DUEÑO por disciplina** | ✅ 7 disciplinas llenas, inyectadas por hook | ❌ no existe el concepto |
| **Veredicto "¿producto o MVP?"** | ✅ `grade-block`, medido, 2 capas | ❌ |
| **Checks que se prueban a sí mismos** | ✅ sección `SELF-TEST` | ❌ tiene tests, pero nada que rompa sus propios checks a propósito |
| **Puertas que se NIEGAN** (exit 2) | ✅ 3 hooks | ❌ `_refuse_to_modify` es el único caso |
| **Un dueño que puede vetar el cierre** | ✅ owner-3 | ❌ |
| **Trazabilidad de decisiones (ADR)** | ✅ 30 ADRs con contrato | ❌ solo CHANGELOG |

> ⭐ **La diferencia de fondo:** `graphify` es **excelente ingeniería de un producto**. Mente OS v2
> es **un sistema que juzga si el trabajo está bien hecho**. Lo segundo es más raro; lo primero es
> lo que a Mente OS le falta para salir de casa.

---

## 4 · QUÉ TRAER — priorizado, con su coste

| # | Qué | De dónde | Coste | Por qué |
|---|---|---|---|---|
| **1** | 🔴 **`--check` de deriva en lo generado** | §2.1 | bajo | ataca el defecto que esta sesión cazó 5 veces. `generate-index`/`generate-metrics` ya generan: falta que el CI falle si lo comprometido difiere del render |
| **2** | 🔴 **Las 3 protecciones de `install.py`** | §2.3 | bajo | `bin/init` escribe config que el usuario ya editó, **sin ninguna de las tres**. Es el riesgo directo de la prueba de campo |
| **3** | 🟡 **Un módulo único de validación de entrada** | §2.4 | medio | no urge mientras Mente OS sea local; urge el día que un clon lea algo remoto |
| **4** | 🟡 **Ratio de tests en el PRODUCTO** | §2.2 | alto | `blk-demo` tiene 0. No se copia el número, se copia la disciplina: un test por módulo, sin efectos fuera de `tmp_path` |
| **5** | 🟡 **Benchmark con método publicado** | §2.6 | medio | convierte *"funciona"* en *"medido contra X, con este juez"*. Es lo que falta para defender Mente OS ante alguien externo |
| **6** | ⬜ **Memoria de trabajo puntuada** | §2.5 | medio | tu §H es más rico; esto es más automático. Evaluar si compensa |

**⭐ Los dos primeros son los que yo haría, y en ese orden.** Ambos son baratos, ambos atacan
defectos **ya medidos** en Mente OS, y el #2 es un riesgo activo: hoy `bin/init` puede destruir la
configuración de quien clone el motor.

---

## 5 · LO QUE NO SE TRAE, Y POR QUÉ

| Qué | Por qué no |
|---|---|
| El grafo de código (tree-sitter, ~40 lenguajes) | Mente OS no analiza código ajeno; For3s OS ya tiene su grafo (AGE + pgvector) |
| Los 18 adapters | Mente OS es Claude Code por diseño. **El generador sí se trae** (§2.1); los adapters no |
| Las 35 traducciones del README | ruido para un motor de uso interno |
| Dedup por MinHash/Jaro-Winkler | resuelve un problema que Mente OS no tiene |

---

## 6 · LA MEDICIÓN QUE MÁS DUELE

| | graphify | Mente OS v2 |
|---|---|---|
| Instalaciones externas verificadas | **miles** (PyPI, Discord, YC) | 🔴 **cero** |
| Bugs reportados por usuarios | issues #1688, #2062, #2167 citados **en el código** | 🔴 ninguno — nadie ajeno lo ha roto |
| Tests sobre el producto gobernado | 1.8:1 | 🔴 0 |

⭐ **Y ese es el hallazgo honesto de todo el análisis:** las tres protecciones de `install.py` no
existen porque alguien fuera inteligente — **existen porque tres usuarios reales rompieron el
producto**. Mente OS no tiene esas cicatrices porque **nadie externo lo ha usado todavía**.

Traer el código sin la prueba de campo copia la forma sin la causa.

---

Related: `docs/analysis/Analisis_internOS_vs_For3s_OS.md` (el mismo ejercicio con `intern-os`) ·
`memory/PENDIENTES.md` (donde viven los pendientes que salen de aquí) ·
`principles/expertise/val-functional.md` (el criterio con el que se juzgará lo que se traiga) ·
`CAPABILITIES.md` (lo que Mente OS puede ejecutar hoy).
