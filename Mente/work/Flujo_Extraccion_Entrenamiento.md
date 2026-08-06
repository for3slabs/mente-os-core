# 🔄 FLUJO DE EXTRACCIÓN — OpenClaw → For3s OS (@For3s_Brian_bot)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Cuerpo/Flujo_Extraccion_Entrenamiento.md → work/Flujo_Extraccion_Entrenamiento.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-05 · **Estado:** DISEÑO APROBADO POR CONSTRUIR — ⛔ NADA EJECUTADO
> **Misión:** de 6 agentes OpenClaw → 1 For3s OS. Leer el CONTENIDO (no copiar archivos)
> y convertirlo en la RED de For3s: episodios + embeddings + grafo + perfil + identidad +
> skills + vault. **Repetible EXACTO por cada agente-fuente** — nada se escapa.
> **Destino:** SIEMPRE la instancia `brian` (@For3s_Brian_bot). Foresito NO se toca.
> **Base:** `memory/archive/Entrenamiento_Bloques_Fruterito_Principal_Dev.md` (7 bloques + capa secretos) ·
> `work/Ronda_Entrenamiento_Plan_Maestro.md` (F0) · radiografías (censo verificado).

---

## 0 · PRINCIPIOS (las 8 leyes del flujo)

1. **Contenido, no archivos**: cada .md/.jsonl se LEE y se DESCOMPONE en unidades de
   memoria; jamás se copia un archivo a la memoria.
2. **Repetible**: todo parametrizado por AGENTE-FUENTE; el mismo tubo corre para los 6.
3. **Nada se escapa**: manifiesto en BD con CADA archivo → decisión final. Cierre = 0 filas sin decidir.
4. **⛔ Secretos → SOLO al vault cifrado** (tabla `secrets`, KEK de brian). En memoria, un
   secreto citado se REDACTA a `[SECRETO→vault:<nombre>]`. Detector por archivo Y por línea.
5. **Reversible**: cada lote con `lote_id` → se puede deshacer quirúrgicamente.
6. **Origen preservado**: todo lleva agente-fuente, fecha REAL original, archivo/sesión de
   origen. El pasado no se disfraza de presente.
7. **Material original READ-ONLY** (`~/entrenamiento/` intacto = respaldo eterno).
8. **Gate de Brian** entre etapas y por lotes; examen de conocimiento AFIRMATIVO al cierre
   de cada etapa; batería §5-BIS al cierre de cada agente.

---

## 1 · ARQUITECTURA DE EJECUCIÓN (cómo corre sin tocar nada)

```
~/entrenamiento/<fuente>/  (host, :ro)
        │  montaje read-only
        ▼
┌──────────────────────────────────────────────┐
│  CONTENEDOR EFÍMERO "extractor"              │
│  docker run --rm                             │
│    -v ~/entrenamiento:/material:ro           │
│    --network for3s-brian_default             │
│    --env-file ~/.for3s/brian/.env            │
│    -v ~/.for3s/brian:/root/.for3s (KEK vault)│
│    for3s-agent:local                         │
│    python -m for3s_core.entrenamiento <etapa>│
│                                              │
│  USA EL PROPIO CORE de For3s:                │
│  memory.record_turn · embeddings BGE-M3 ·    │
│  kg (grafo AGE) · perfil P1 · skills H12 ·   │
│  secrets vault (KEK) · identidad (persona/)  │
└──────────────┬───────────────────────────────┘
               ▼
   BD de for3s-brian (Postgres+AGE+pgvector)
   + persona/ de brian (identidad adaptada, con gate)
```

- **Módulo nuevo:** `for3s_core/entrenamiento.py` (+ submódulos por etapa). Vive en el
  repo, con tests — se construye etapa por etapa con el Método F (no todo de golpe).
- El extractor es un proceso PUNTUAL (corre, termina, muere). Sin loops, sin daemons.
- Ventaja clave: al usar `memory.record_turn`/`kg`/`skills` REALES, lo importado es
  indistinguible de memoria nativa → CLS/DMN/microglía lo tratan como propio (el cerebro
  nocturno de brian TERMINA la digestión solo). Eso es "explotar todo el potencial".

---

## 2 · MODELO DE DATOS DEL FLUJO (migración aditiva 033)

```sql
-- 033_entrenamiento.sql (ADITIVA, no toca nada existente)
CREATE TABLE IF NOT EXISTS import_manifiesto (
  id bigserial PRIMARY KEY,
  fuente text NOT NULL,            -- 'fruterito-principal' | 'fruterito-wsl' …
  ruta text NOT NULL,              -- ruta relativa dentro del material
  sha256 text NOT NULL,
  bytes bigint NOT NULL,
  bloque text NOT NULL,            -- B1..B7 | SECRETO
  duplicado_de bigint REFERENCES import_manifiesto(id),
  clasificacion text NOT NULL,     -- propuesta automática
  decision text,                   -- importar|resumir|excluir-secreto|basura|backlog  (NULL = pendiente)
  lote_id text,                    -- lote donde entró
  estado text NOT NULL DEFAULT 'pendiente',  -- pendiente|importado|verificado|descartado
  detalle jsonb NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (fuente, ruta)
);
CREATE TABLE IF NOT EXISTS import_lotes (
  lote_id text PRIMARY KEY,        -- 'fp-B2-diarios-001'
  fuente text NOT NULL, bloque text NOT NULL,
  items int NOT NULL DEFAULT 0, episodios int NOT NULL DEFAULT 0,
  conceptos int NOT NULL DEFAULT 0, estado text NOT NULL DEFAULT 'dry-run',
  creado_at timestamptz NOT NULL DEFAULT now(), aplicado_at timestamptz
);
```

**Convenciones de origen en la memoria** (reversibilidad + trazabilidad sin tocar el esquema
de `episodes_events`): `session_id = 'oc:<fuente>:<sesion-o-doc-origen>'` · `channel = 'import'` ·
la fecha ORIGEN y el `lote_id` viajan en el contenido estructurado del episodio (prefijo de
metadatos estándar `[origen: <fuente> · <fecha-real> · <ruta> · lote <id>]`). Deshacer un
lote = `DELETE FROM episodes_events WHERE session_id LIKE 'oc:<fuente>:%' AND content LIKE '%lote <id>]%'`
(y su espejo en manifiesto/grafo). *(Si al construir FE0 resulta más limpio, se evalúa
columna aditiva `import_lote text NULL` en episodes_events — decisión de FE0.)*

---

## 3 · LAS 9 ETAPAS (FE0–FE8)

### FE0 · PREPARAR (red de seguridad demostrable)
1. Backup completo de la BD de brian (pg_dump al host, etiquetado `pre-entrenamiento`).
2. Migración 033 (tablas de control). 3. Verificar flags a máximo potencial (ya ✅
   2026-07-05: estilo/perfil/autogen/DMN-generativas ON · microglía OFF hasta el final).
4. **Prueba de reversa EN VACÍO**: importar 3 episodios de juguete → deshacer el lote →
   verificar BD idéntica. Sin reversa demostrada NO se importa nada real.

### FE1 · CENSO → MANIFIESTO (read-only, cero escritura en memoria)
- Walker de TODO `<fuente>`: ruta+hash+bytes → clasificador por bloque (reglas de la
  radiografía: agents/*→B3, workspace/memory→B2, workspace/skills→B4, raíz .md→B1,
  docs/exports/…→B5, media→B7, resto→B6) → dedup por hash (principal↔wsl) → manifiesto a BD.
- **Detector de secretos v1** (por ARCHIVO: nombres/rutas + por CONTENIDO: regex de tokens
  `sk-`, `ghp_`, `AAH…` Telegram, base64 largos, `password[:=]`, PEM) → bloque=SECRETO.
- Salida: reporte de censo (totales por bloque/decisión propuesta) → **GATE Brian**.

### FE2 · SECRETOS → VAULT (antes que nada, para que FE3+ redacte con nombre)
- Cada secreto detectado → `secrets` cifrado de brian con nombre canónico
  (`oc.fruterito.github_token`, `oc.acompanante.godinez.password`, …) + inventario legible
  para Brian (qué se guardó, de dónde salió, SIN mostrar el valor).
- Los 47+ censados deben caer TODOS aquí (verificación afirmativa contra la radiografía).

### FE3 · IDENTIDAD (B1) — lo más delicado, 3 salidas
| Material | Proceso | Destino |
|---|---|---|
| SOUL/IDENTITY/ETHICS/AGENTS/PRIORIDAD/TOKEN-EFF | leer → **ADAPTAR al formato For3s** (redactar borrador nuevo, no traducir literal) | **borrador de `persona/IDENTITY.md` + `REGLAS_USUARIO.md`** → GATE Brian → recién ahí se escribe en brian |
| USER.md + brian-prefs.md | descomponer en hechos de perfil | **perfil P1** (propuestas con gate, pipeline existente) |
| HISTORIAL-COMPLETO/FRUTERITO-SISTEMA/MEMORY.md | unidades narrativas fechadas | episodios + conceptos del grafo (historia, no personalidad) |
| SKILLS-INVENTARIO | índice para FE6 | manifiesto |
- Regla de oro: el núcleo For3s de brian NO se toca; Foresito no recibe nada.
- La estructura `mente-os/{Alma,Cerebro,Cuerpo,Doc}` de brian se puebla con lo APROBADO.

### FE4 · MEMORIA ESCRITA (B2) — el alma escrita
- Parser por TIPO: **diario** (`AAAA-MM-DD.md`, 41) → episodios con SU fecha · **temática**
  (lecciones/genomad/…) → conceptos+relaciones al grafo · **learnings por proyecto**
  (acompanante/*/learnings) → conceptos ligados al concepto-proyecto · metrics/pending →
  episodios de estado fechados.
- Lotes chicos (≤25 archivos) → dry-run → aplicar → re-embeber lote.

### FE5 · CONVERSACIONES (B3) — la masa (~39K turnos en principal)
1. Parser jsonl OpenClaw: árbol `parentId` → secuencia temporal plana; tipos `message`
   (user/assistant/toolResult) — `custom`/`model_change`/etc se descartan (runtime).
2. **Curación**: sesiones cron repetitivas (~50 en dev) → 1 episodio-resumen por día, no
   1000 iguales. `.deleted`/`.reset`/`.bak` → deduplicar contra su versión viva por prefijo.
3. **Secretos línea a línea** → redactar a `[SECRETO→vault:<nombre>]` ANTES de insertar.
4. Cada turno → `record_turn` con session `oc:<fuente>:<uuid-origen>`, rol real, fecha
   origen en metadatos; toolResults gigantes se truncan con criterio (el diálogo importa,
   el dump de un `ls` no).
5. Lote = 1 sesión-origen. Orden: dev (17,096) → watchdog (20,749, MUY curado: es
   monitoreo) → godin-slot-1 (211) → main (backups feb).
6. Re-embeber por lote → la NOCHE consolida (CLS→grafo). Ritmo: lotes espaciados para no
   saturar embeddings/cupo (medir con el lote piloto en FE0/FE5.1).

### FE6 · SKILLS (B4) — conectar, no archivar
- Por cada skill (16 en principal): leer SKILL.md + guías → destilar (qué hace, cuándo,
  cómo, ejemplos) → **crear skill H12** en BD con embedding + nota de procedencia →
  el matcher de skills la sirve cuando el tema aparezca. Una por una, con gate (¿skill
  viva / solo conocimiento al grafo / descartar?). Los scripts NO se importan (backlog).

### FE7 · CONOCIMIENTO (B5) + MEDIA-DOCS (B7)
- Docs/análisis/specs/guiones → unidades semánticas → memoria semántica + conceptos del
  grafo ligados a su proyecto (godinez, genomad, vibecoding, monad…).
- Código: NO se importa → `backlog_herramientas.md` (registrado en manifiesto).
- B7: solo adjuntos de texto (.md/.docx/.txt/.pdf legible) por el mismo tubo de B5;
  fotos (1,234 jpg) = decisión aparte de Brian al final.

### FE8 · EXAMEN + CIERRE (por agente-fuente)
1. **Examen de conocimiento**: banco de preguntas POR BLOQUE generado durante la
   extracción (ej.: "¿qué aprendiste en el bootcamp Vibecoding?", "¿qué es Genomad?",
   "¿qué pasó el 2026-03-26?", "¿qué skill usarías para un hackathon Monad?") →
   se le preguntan a @For3s_Brian_bot → respuesta DEBE salir de su memoria. Cero "más o menos".
2. Manifiesto: 0 filas sin decisión (la prueba del "nada se escapa").
3. /salud 0 FAIL + batería §5-BIS + Foresito intacto + reporte de cobertura → commit firmado.
4. → siguiente agente-fuente por el MISMO tubo.

---

## 4 · ORDEN DE LOS AGENTES-FUENTE (el tubo se repite 6 veces)

| # | Fuente | Material | Nota |
|---|---|---|---|
| 1 | **Fruterito-principal** (dev+watchdog+workspace) | 5,786 arch. ya radiografiados | AQUÍ se construye y calibra el tubo |
| 2 | Fruterito-wsl / main (Fruterito Personal) | 40 sesiones · 6,045 turnos · 23MB | el más "Brian" |
| 3 | Fruterito-wsl / workspace-empleado | 734 docs | el mar de docs |
| 4 | Fruterito-wsl / workspace-for3s-design | 16 docs | identidad rica |
| 5 | wsl: skills/mode_*, flows, credentials… | censo FE1 decide | radiografía wsl pendiente |
| 6 | Cipher + Helix | ~170 turnos | cierre rápido |

---

## 5 · CONSTRUCCIÓN (cuándo se escribe el código — Método F)

El código del extractor se construye **etapa por etapa AL ejecutarla**, cada una con su
batería (no se escribe todo por adelantado sin poder probarlo):
- FE0-FE1 → `entrenamiento.py` (walker, manifiesto, detector v1, reversa) + migr 033 + tests.
- FE2 → conector al vault + inventario. · FE3 → parsers de identidad + borradores.
- FE4-FE5 → parsers md/jsonl + curadores + loteador. · FE6-FE7 → destilador de skills/docs.
- FE8 → examinador. Cada pieza: defensiva, idempotente, dry-run default, tests, commit firmado.

**Reglas operativas**: sin procesos de fondo · si la red al server falla al 1er intento,
PARAR · lotes espaciados (cupo OAuth compartido con Foresito — vigilar el pin) · todo
corre en el server.

⚠️ **LECCIÓN KEK (cazada en E2.1):** el contenedor efímero `docker run` DEBE montar la KEK
de la instancia destino (`-v ~/.for3s/brian:/root/.for3s:ro`). Sin el montaje,
`load_or_create_master_key` GENERA una KEK nueva al vuelo → cifra secretos indescifrables
por el contenedor vivo (`InvalidTag`). Todo `docker run` del extractor que toque el vault
lleva ese `-v`. (El de censo/import de episodios no lo necesita — no usa la KEK.)

---

*Próximo paso cuando Brian dé la orden: **FE0+FE1** (backup + migración 033 + censo→manifiesto
+ prueba de reversa). Read-only sobre el material, cero imports reales todavía.*
