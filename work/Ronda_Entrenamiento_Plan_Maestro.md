# 🎓 RONDA ENTRENAMIENTO — Plan Maestro (F0, Ronda de diseño)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Ronda_Entrenamiento_Plan_Maestro.md → work/Ronda_Entrenamiento_Plan_Maestro.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-04 · **Estado:** BORRADOR esperando aprobación de Brian
> **Hito:** ENTRENAMIENTO — despedazar los agentes OpenClaw y absorber TODO su conocimiento
> en For3s OS (Foresito). De 6 agentes → 1.
> **Método:** Fases "F" (`rules/ESTANDAR_Metodo_Fases_F.md`). Esta ronda ES la F0.
> **Regla madre:** explicar → aprobar → construir. NADA se construye sin luz verde de Brian.

---

## 1 · Visión (Brian)

Brian entrenó por meses 6 agentes OpenClaw (un mar de conocimiento, contexto, memorias y
herramientas) que ya no usa por temas económicos. La meta:

> **Despedazar cada agente a profundidad** — archivo por archivo, sin omitir NADA — y adaptar
> cada pieza **como memoria o dentro de la personalidad** de Foresito. Resultado: **UN solo
> For3s OS que contenga todo.**

Decisión abierta (Brian, 2026-07-04): *"¿memoria o personalidad? NO LO SÉ AÚN — tenemos que
despedazar uno e ir planeando poco a poco cuál va a ser."* → El plan NO pre-decide: define un
**marco de decisión por tipo de material** (§4) y la decisión FINAL se toma **pieza por pieza
durante el despiece**, con Brian.

---

## 2 · Terreno VERIFICADO (censo 2026-07-04, por SSH al server)

Material en `~/entrenamiento/` (host del server, fuera de contenedores, **read-only para nosotros**):

### 2.1 Los dos árboles

| Árbol | Tamaño | Origen |
|---|---|---|
| `Fruterito-principal/` | 291 MB, 5786 archivos | copia de `C:\...\.openclaw` (Windows) |
| `Fruterito-wsl/` | 194 MB, 5878 archivos | copia de `~/.openclaw` (WSL2) |

### 2.2 Los agentes y sus materiales (verificado hoy)

| Agente | Dónde | Material clave |
|---|---|---|
| 🍍 **Fruterito Personal** (DevRel) | `wsl/agents/main` (19MB sesiones) + `principal/agents/main` (4.4MB) + `principal/workspace/` | 20 .md de identidad/sistema en raíz + **99 diarios** `memory/AAAA-MM-DD.md` + 459 .md en workspace |
| 🍊 **Fruterito Empleado** (Product Lead→CEO) | `wsl/workspace-empleado/` | 30 .md raíz (incl. análisis de negocio) + **101 diarios** + **734 .md** en total (projects/, frutero-ops/, hackathons/, bootcamps/, docs/…) |
| 📰 **Watchdog** | `principal/agents/watchdog` (18MB sesiones) | el que MÁS conversación tiene (20749 turnos según censo previo); sesiones grandes (hay .jsonl de 5MB) |
| 🔥 **For3s Design** | `wsl/workspace-for3s-design/` | 16 .md (identidad rica: SOUL, DESIGN-SYSTEM, AGENTS…) + templates + projects |
| 🔴 **Cipher** | `wsl/agents/cipher` (104KB) | casi vacío |
| 🔵 **Helix** | `wsl/agents/helix` (316KB) | casi vacío |

### 2.3 ⭐ Hallazgos NUEVOS del censo (nadie los tenía contemplados)

1. **Las sesiones "borradas" siguen ahí**: además de 87 `.jsonl` planos hay ~40 variantes
   `.jsonl.deleted.*`, `.jsonl.reset.*`, `.jsonl.backup` → conversaciones que OpenClaw rotó
   pero que SON conocimiento. **Se incluyen en el despiece.**
2. **Carpetas sin censar**: `agents/godin-slot-1..15` + `workspace-godin-slot-1` (¿los Godínez?),
   `agents/dev`, `agents/default`, `subagents/`, `canvas/`, `cron/runs/`, `skills/mode_{ahorro,normal,turbo,ultra}`,
   `flows/`, `tasks/`, `profiles/`, `completions/`, `extensions/token-modes/`, `telegram/`,
   `browser/openclaw/`, `logs/`, `media/`, `workspaces/`, `workspace-main/`,
   `agents.backup-20260404-*/`. → **F1 los censa TODOS**; ninguno se descarta sin mirarlo.
3. **Identidad OpenClaw en capas** en cada workspace: `SOUL.md · IDENTITY.md · USER.md ·
   ETHICS.md · AGENTS.md · MEMORY.md · HISTORIAL-COMPLETO.md · SKILLS-INVENTARIO.md · TOOLS.md ·
   HEARTBEAT.md · PRIORIDAD.md · TOKEN-EFFICIENCY.md · BOOTSTRAP.md · FRUTERITO-SISTEMA.md` —
   mapea casi 1:1 con nuestra IDENTIDAD EN CAPAS (Hito Identidad Viva v0.15.0). 🎯
4. **Memoria sqlite**: `principal/memory/dev.sqlite` + `wsl/memory/main.sqlite` (69KB c/u) —
   hay que abrir y ver qué tablas traen.
5. **⚠️ 47 archivos con pinta de SECRETO**: `credentials/`, `device.json`, `auth-profiles.json`,
   tokens de Telegram en texto plano. **Lista de exclusión obligatoria (§6.1).**
6. **Duplicación** principal↔wsl (agente `main` vive en ambos; workspace-empleado comparte
   raíz .md con workspace personal) → el pipeline DEDUPLICA por hash antes de importar.

### 2.4 Los 2 formatos de conocimiento (confirmado)

- **Sesiones `.jsonl`** (conversación cruda, turno a turno) → mapea a `episodes_events` de Foresito.
- **Docs `.md`** (conocimiento destilado: identidad, diarios, análisis, proyectos) → mapea a
  conceptos/grafo, identidad, o Mente OS según tipo (§4).

---

## 3 · Resultado final (definición de ÉXITO del hito)

1. **Cada archivo** de `~/entrenamiento/` tiene una decisión registrada en el manifiesto:
   `importado (dónde) · curado-fuera (por qué) · excluido-secreto · basura`. **Cero omitidos.**
2. Foresito **responde con ese conocimiento**: preguntas sobre Frutero Club, los bootcamps,
   los hackathones, la historia con Brian… salen de SU memoria (semántica + grafo).
3. El **perfil de Brian** en Foresito se enriquece con lo que los 6 agentes aprendieron de él
   (USER.md, diarios, patrones de 6045+20749 turnos).
4. La **personalidad** absorbe lo que Brian APRUEBE (capa usuario / Mente OS heredable), sin
   tocar el núcleo blindado.
5. **Nada se rompe**: batería §5-BIS verde tras cada import (todo el sistema, no el carril).
6. El material original queda **intacto** (read-only, es el respaldo).

---

## 4 · Marco de decisión: ¿MEMORIA o PERSONALIDAD? (por tipo de material)

> La duda central de Brian. Marco propuesto — la decisión final es pieza por pieza en el
> despiece, con Brian en los gates.

| Tipo de material | Ejemplos reales | Destino propuesto en For3s OS | ¿Memoria o personalidad? |
|---|---|---|---|
| **Conversación cruda** | sesiones .jsonl (main, watchdog…) | `episodes_events` (+embeddings +consolidación nocturna al grafo) | 🧠 MEMORIA episódica |
| **Diarios de memoria** | `memory/2026-03-26.md` (99+101) | episodios "resumen del día" + conceptos al grafo | 🧠 MEMORIA (las 2 capas) |
| **Conocimiento destilado** | análisis, REPORTE-FRUTERO-CLUB, comparativos, docs de proyectos (734 .md empleado) | conceptos/relaciones del grafo + memoria semántica | 🧠 MEMORIA semántica |
| **Sobre Brian** | USER.md, patrones en diarios | perfil de usuario (P1, con gate de aprobación) | 👤 PERFIL (ya tiene pipeline) |
| **Identidad/carácter** | SOUL.md, IDENTITY.md, ETHICS.md | **capa usuario editable + Mente OS heredable** (Identidad Viva) — SOLO lo que Brian apruebe; el núcleo For3s NO se toca | 🎭 PERSONALIDAD (gate fuerte) |
| **Habilidades descritas** | SKILLS-INVENTARIO.md, skills/mode_* | candidatos a skills H12 (curados, uno por uno) | 🛠️ SKILLS |
| **Herramientas/código** | TOOLS.md, scripts, extensions | NO se importan — se anotan en un backlog "herramientas a reconstruir" (trabajo aparte, ya lockeado en E2) | 📋 BACKLOG |
| **Config/runtime OpenClaw** | cron/, telegram/, devices/, profiles/ | normalmente basura/excluido; se censa y decide en F1 | 🗑️/📋 |
| **Secretos** | credentials/, device.json, auth-profiles.json, tokens | **EXCLUIDOS SIEMPRE** — jamás a memoria | ⛔ NUNCA |

**Regla de oro de identidad:** Foresito NO se convierte en Fruterito. La identidad de los
agentes viejos entra como *conocimiento sobre ellos* (memoria) por default; SOLO pasa a
*personalidad* (capa usuario/Mente OS) lo que Brian apruebe explícitamente en el gate. El
núcleo BASE de For3s (blindado, v0.15.0) no se toca jamás.

---

## 5 · Las FASES del hito

> Cada fase con el estándar completo: investigar terreno → construir defensivo → batería
> §5-BIS → commit firmado → server-primero. Gate de Brian entre fases.

### F1 · CENSO FORENSE TOTAL (el "no omitimos nada" hecho sistema)
- Script read-only que recorre TODO `~/entrenamiento/` y genera el **MANIFIESTO maestro**
  (tabla: ruta · hash · tamaño · tipo detectado · agente dueño · duplicado-de · clasificación
  propuesta · decisión final [vacía]). Deduplicación por hash entre principal↔wsl.
- **Detector de secretos** (patrones: tokens, llaves, credentials, .env, base64 largos…) →
  lista de exclusión sellada. Verificación afirmativa: los 47+ conocidos caen en la lista.
- Censo de las carpetas nunca miradas (godin-slots, subagents, canvas, sqlite…): qué son,
  cuánto pesan, si traen conocimiento o solo runtime.
- Abrir los 2 sqlite y mapear sus tablas.
- **Entregable:** `Doc/Entrenamiento_Manifiesto.md` ⚠️ (planned deliverable, **never produced** — verified 2026-07-30) (+ CSV/JSON de trabajo) — el tablero de
  TODO el hito. Nada se importa aún.

### F2 · DESPIECE PROFUNDO del agente 1 (el que Brian elija)
- Leer TODO lo del agente (identidad, diarios, sesiones incl. .deleted/.reset, workspace).
- **Fichas de despiece** por pieza: qué es · qué contiene (resumen honesto) · calidad
  (oro/bueno/ruido) · propuesta memoria-vs-personalidad según §4 · flags (secreto, duplicado,
  fechas para dar contexto temporal a episodios).
- Aquí "planeamos poco a poco cuál va a ser" (Brian): con el agente 1 despedazado, Brian ve
  el material real y CALIBRAMOS el marco §4 antes de tocar el siguiente.
- **Entregable:** `Doc/Entrenamiento_Despiece_<Agente>.md` + manifiesto actualizado.
- **GATE Brian:** aprueba las decisiones pieza por pieza (por lotes).

### F3 · PIPELINE DE IMPORT (construir la herramienta, una vez, bien)
- Módulo importador (idempotente, dry-run, por lotes, reanudable, con log en el manifiesto):
  - `.jsonl` → `episodes_events` (con fecha/agente/sesión de ORIGEN preservados como metadatos
    — el pasado no se disfraza de presente) → re-embeber → consolidación nocturna al grafo.
  - `.md` conocimiento → memoria semántica + conceptos/relaciones del grafo.
  - Sobre-Brian → propuestas de perfil (pipeline P1 existente, con su gate).
  - Identidad aprobada → capa usuario / Mente OS heredable (mecanismo Identidad Viva existente).
- Red de seguridad demostrable: dry-run + backup previo + import reversible por lote
  (cada lote etiquetado con `import_batch_id` → se puede borrar un lote exacto).
- Governor/curación: volúmenes por lote acotados; NADA de meter 40MB de golpe.
- **Batería §5-BIS** con un lote piloto pequeño del agente 1.

### F4 · IMPORT COMPLETO del agente 1 + verificación de que APRENDIÓ
- Importar los lotes aprobados de F2. Re-embeber. Dejar que la noche consolide (CLS/DMN).
- **Examen de conocimiento**: preguntas reales a Foresito cuyo contenido SOLO puede venir del
  material importado → verificación AFIRMATIVA de que el conocimiento está vivo.
- Batería §5-BIS completa + /salud 0 FAIL + memoria/reconexión.

### F5..Fn · CICLO POR AGENTE (repetir F2→F4 por cada uno)
- Orden propuesto (por riqueza, Brian decide): 1º el elegido para F2, luego el resto:
  **Fruterito Personal · Watchdog · Fruterito Empleado** (el 99% del mar) · For3s Design ·
  godin-slots/subagents según lo que diga el censo · Cipher/Helix (casi vacíos, cierre rápido).
- Cada ciclo es MÁS barato que el anterior (pipeline ya existe, marco ya calibrado).

### F-final · CIERRE
- Manifiesto 100% decidido (cero filas sin decisión) — la prueba del "no omitimos nada".
- Backlog "herramientas a reconstruir" entregado como doc.
- Bitácora + RETOMAR + memorias actualizadas. version.py bump. Commits firmados.
- Veredicto: 6 agentes → 1 For3s OS. Material original intacto como respaldo.

---

## 6 · Reglas DURAS del hito

1. **⛔ SECRETOS JAMÁS a memoria** — lista de exclusión de F1 es ley; el importador la
   verifica ANTES de cada lote (defensa en profundidad, no solo confianza en el censo).
2. **Material original READ-ONLY** — nunca modificar/mover `~/entrenamiento/`.
3. **Curar antes de aprender (E3)** — calidad sobre cantidad; lotes acotados; el governor
   frena, pero el filtro es NUESTRO, antes.
4. **Gates de Brian** — entre fases y por lotes de decisiones. Explicar → aprobar → construir.
5. **Identidad**: núcleo For3s blindado intacto; personalidad solo vía capa usuario/Mente OS
   con aprobación explícita. Foresito absorbe conocimiento, no se convierte en Fruterito.
6. **Server-primero** — todo corre y se prueba en el server; push a GitHub solo cuando Brian diga.
7. **⛔ Sin loops de espera contra el server** — si la red falla al 1er intento, parar y reportar.
8. **Origen preservado** — todo lo importado lleva metadatos (agente origen, fecha real,
   import_batch_id) → auditable y reversible por lote.

---

## 7 · Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Meter ruido/basura al grafo (skills basura, episodios sin valor) | Curación F2 con fichas + lotes + gate; governor como 2ª red |
| Secretos filtrados a memoria | Detector F1 + verificación pre-lote en el importador + grep post-import |
| Confusión temporal (episodios de marzo como si fueran de hoy) | Metadatos de fecha ORIGEN en cada episodio importado |
| Foresito "se vuelve Fruterito" (contaminar identidad) | Regla de oro §4: identidad = solo vía gate a capa usuario; núcleo blindado |
| Duplicados principal↔wsl inflan la memoria | Dedup por hash en F1; el manifiesto marca duplicado-de |
| Volumen (485MB, ~11.6K archivos) revienta embeddings/BD de golpe | Lotes acotados + dry-run + medir en el piloto F3 antes de escalar |
| Import corrupto / a medias | Idempotente + reanudable + reversible por import_batch_id + backup previo |
| El censo pisa el server en horas de uso | Trabajos read-only ligeros; los pesados (embeddings) de noche o espaciados |

---

## 8 · Lo que Brian decide AHORA (para arrancar)

1. **¿Aprueba este plan** (fases F1..Fn, marco §4, reglas §6)?
2. **¿Con qué agente despedazamos primero (F2)?** Propuesta: 🍍 **Fruterito Personal** —
   es el más "Brian" (DevRel, 6045 turnos, identidad más rica) y calibra mejor el marco
   memoria-vs-personalidad. Alternativas: Watchdog (más volumen) o Empleado (más docs).
3. F1 (censo) es read-only y no importa nada → ¿luz verde para arrancar F1 tras aprobar?

---

*Cruza con: PENDIENTES §ENTRENAMIENTO (E1-E4: este plan ES E1-E4 desplegado) · PR8 ·
[[project_entrenamiento_6_agentes]] · Hito Identidad Viva (destino de la capa personalidad) ·
H5/H6/H12 (memoria, consolidación, skills) · `rules/ESTANDAR_Metodo_Fases_F.md`.*