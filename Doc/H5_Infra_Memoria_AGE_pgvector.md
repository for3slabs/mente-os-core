# H5 — Infraestructura de Memoria: pgvector + Apache AGE (hallazgos críticos)

> **Qué es:** registro técnico de la instalación/configuración de las herramientas
> de H5 (Memoria Real) en el servidor `for3s`, con los HALLAZGOS y trampas que
> descubrimos en vivo (2026-06-19). **Propósito:** que nadie vuelva a tropezar con
> los mismos errores de Apache AGE + asyncpg, que costaron horas de diagnóstico.
> Es la "biblioteca de obra" de H5 — consultar ANTES de tocar el grafo o los vectores.

**Servidor:** `for3s` · PostgreSQL 16 (nativo, no Docker) · usuario app `for3s`
(NO superuser) · BD `for3s`. Conexión vía asyncpg (pool del bot, sin ORM).

---

## Estado actual (verificado 2026-06-19)

| Componente | Estado | Detalle |
|---|---|---|
| **pgvector** (`vector`) | ✅ activo | v0.8.2 · búsqueda de similitud verificada con el usuario `for3s` |
| **Apache AGE** (`age`) | ✅ activo | v1.6.0 · precargado en shared_preload_libraries |
| **Grafo** | ✅ creado | `for3s_kg` (propiedad de `for3s`) |
| **Funciones wrapper** | ✅ creadas | `cypher_write`, `cypher_read_json` (las que se usan), `cypher_read` (legacy, no usar) |
| **Embeddings (BGE-M3)** | ✅ activo | reemplazó a Stella (ver §"Decisión Stella→BGE-M3"). 1024-dim, español, CPU. Verificado. |
| **Columna + índice HNSW** | ✅ migración 007 | `episodes_events.embedding vector(1024)` nullable + `idx_episodes_embedding` (hnsw cosine). schema v7. |
| **Backfill embeddings** | ✅ completo | 438/438 turnos con embedding. Búsqueda semántica verificada sobre datos reales. |
| **Módulo embeddings.py** | ✅ creado | `embed()`, `embed_lote()`, `a_pgvector()`. Singleton lazy del modelo. |
| **Búsqueda semántica** | ✅ creada | `memory.buscar_semantico()` — recall por significado. Verificada con queries reales. |
| **Knowledge Graph (kg.py)** | ✅ creado | helpers idempotentes registrar/navegar repos·owners·issues·PRs. Verificado. |
| **Integración bot — Pieza A** | ✅ EN PRODUCCIÓN | send() inyecta recuerdos semánticos al contexto + precarga del modelo al arranque. |
| **Integración bot — Pieza B** | ✅ EN PRODUCCIÓN | turnos nuevos se embeben en background (fire-and-forget) — la memoria ya no se congela. |
| **Pieza B-ext (todos los flujos)** | ✅ EN PRODUCCIÓN | `_guardar_turno()` → TODOS los flujos (incl. GitHub) embeben. |
| **Integración bot — Pieza C** | ✅ EN PRODUCCIÓN | grafo se puebla al leer GitHub (junto a save_gh_tool_calls). |
| **Afinado memoria semántica** | ✅ EN PRODUCCIÓN | filtro query-a-sí-misma + dedup + prompt afirmativo + `solo_usuario=True` (corta bucle). |

> **🎉 H5 "MEMORIA REAL" COMPLETO (2026-06-20).** Los 8 sub-pasos + integración (3
> piezas) + refinamientos en producción. El bot recuerda por significado todo su
> historial, embebe cada turno nuevo (todos los flujos), y puebla un grafo de
> conocimiento al leer GitHub. Verificado E2E con pruebas en vivo de Brian.

---

## SUB-PASO 1 — pgvector (búsqueda por significado)

**Cómo se activó:**
- `CREATE EXTENSION vector` — requiere **superusuario** (el usuario `for3s` NO lo es,
  por seguridad correcta). Se hizo como `postgres`: `sudo -u postgres psql -d for3s`.
- El binario ya estaba a nivel sistema (`/usr/share/postgresql/16/extension/vector.control`).
- ⚠️ El doc de C0 decía "pgvector ya instalado" — era FALSO en la BD (solo estaba el
  binario, no la extensión activa). Verificar siempre con `SELECT * FROM pg_extension`.

**Uso:** el usuario `for3s` ya puede crear columnas `vector(N)` e indexar con HNSW.
Verificado: distancia coseno `<=>` da 0.0 (idéntico) → 1.0 (opuesto). Sin trampas.

---

## SUB-PASO 2 — Apache AGE (Knowledge Graph) — ⚠️ AQUÍ ESTÁN LAS TRAMPAS

AGE fue MUCHO más delicado que pgvector. Descubrimos **4 trampas** en vivo. Todas
resueltas, pero hay que respetarlas SIEMPRE al trabajar con el grafo.

### Trampa 1 — AGE necesita PRECARGA (shared_preload_libraries)
- Síntoma: `LOAD 'age'` → `access to library "age" is not allowed` para el usuario app.
- Causa: `LOAD` de una librería C está prohibido a usuarios no-superuser salvo que
  esté precargada al arranque.
- Solución aplicada: `ALTER SYSTEM SET shared_preload_libraries = 'age';` + **reiniciar
  PostgreSQL**. (Se hizo con el procedimiento seguro: backup → parar bot → ALTER →
  restart postgres → re-arrancar bot. El reinicio de Postgres fue limpio.)
- Con la precarga, el usuario `for3s` YA NO necesita hacer `LOAD 'age'`.

### Trampa 2 — NO hacer `SET search_path` en la conexión de la app
- Síntoma: tras `SET search_path = ag_catalog, public` en la conexión, las queries
  Cypher de lectura fallaban (issue conocido apache/age#57).
- Solución: NUNCA setear el search_path en la conexión del bot. En su lugar, las
  funciones wrapper hacen el `SET search_path` INTERNAMENTE (en su propio scope).

### Trampa 3 — asyncpg + cypher() directo en LECTURA = falla
- Síntoma: `SELECT * FROM cypher(...) AS (x agtype)` con un RETURN falla vía asyncpg
  (`syntax error at end of input` en `prepare`/`bind_execute`). Causa: asyncpg usa
  el protocolo extended (prepared statements) y AGE no lo soporta bien con RETURN.
- Solución: **funciones wrapper SQL/plpgsql** (ver abajo). La app llama la función
  como query SQL normal; asyncpg la maneja sin problema. CREATE/DELETE sí pueden ir
  por `cypher()` dentro de la función write.

### Trampa 4 (la que costó más) — palabras RESERVADAS + RETURN de propiedad
- Síntoma ENGAÑOSO: `RETURN n.desc` daba `syntax error at end of input` — parecía
  problema de asyncpg/infra, pero era el DATO.
- Causa real: **`desc` es palabra reservada en AGE** (= DESCENDING). Usarla como
  nombre de propiedad o alias rompe el Cypher.
- Reglas a respetar SIEMPRE en las queries Cypher:
  1. **`RETURN` de una propiedad escalar necesita ALIAS:** `RETURN n.x AS valor`
     (NO `RETURN n.x` a secas).
  2. **NO usar palabras reservadas** como nombres de propiedad/alias: `desc`, `asc`,
     `order`, `limit`, etc. Usar `detalle`, `descripcion`, `valor`, etc.
  3. `RETURN n` (el nodo entero) SÍ funciona sin alias.

### Trampa 5 (descubierta en sub-paso 7) — RETURN de 1 SOLA columna vía la función
- Síntoma: `kg read falló: return row and column definition list do not match`.
- Causa: la función wrapper `cypher_read_json` declara `AS (result agtype)` = UNA
  columna. Un `RETURN a, b, c` (multi-columna) NO coincide → falla.
- Reglas:
  1. Para devolver varios valores, construir un MAPA en Cypher:
     `RETURN {tipo: labels(x)[0], numero: x.numero} AS r` (1 columna = el mapa). ✓
  2. `count(*)` NO puede ir dentro del mapa directo (AGE exige GROUP BY): agregar
     primero con `WITH ... count(*) AS c` y luego `RETURN {n: c} AS r`. ✓
  3. RETURN de un escalar (`RETURN rp.nombre AS r`) o el nodo entero también son
     1 columna → OK.

### Trampa 6 (descubierta en H6 sub-paso 6) — RETURN de un INTEGER escalar
- Síntoma: `kg read falló: cannot cast agtype integer to json`.
- Causa: `cypher_read_json` convierte el resultado a json. Un `RETURN e.seq AS s`
  donde seq es INTEGER → AGE no castea el agtype integer escalar a json y falla.
  (Un string escalar como `rp.nombre` sí castea; el integer escalar NO.)
- Regla: para devolver un entero, **envolverlo en un mapa**: `RETURN {seq: e.seq} AS r`
  y leer `fila["seq"]`. (Igual que recursos_de_repo con su mapa.) ✓
  Verificado en `kg.episodios_de_concepto`.

---

## SUB-PASO 3 — Embeddings: DECISIÓN Stella → BGE-M3 (desviación del diseño LOCKED)

> ⚠️ **DESVIACIÓN del diseño:** R2 B2 eligió `dunzhang/stella_en_400M_v5`. Tras
> probarlo en vivo (2026-06-19) lo CAMBIAMOS por **`BAAI/bge-m3`**. Razón doble:
> (1) Stella no carga en CPU; (2) Stella es solo-inglés y For3s habla español.

**Por qué se descartó Stella (2 bugs reales, no resolubles a costo razonable):**
1. `please install xformers` — Stella usa atención custom (base GTE: BERT+RoPE+GLU)
   que exige xformers (GPU-only). Se intentó el `config_kwargs` oficial de la model
   card (`use_memory_efficient_attention=False, unpad_inputs=False`) → pasó ese
   error pero apareció el siguiente.
2. `IndexError` en el RoPE (`rope_cos[position_ids]` con índice basura) al generar
   embeddings en CPU con transformers 5.12 (muy nuevo). Es un bug del código custom
   remoto de la familia GTE con transformers nuevo en CPU. No es nuestro fallo.

**El hallazgo CLAVE (punto ciego del diseño):** al investigar el plan B descubrimos
que **Stella Y BGE-large-en-v1.5 son SOLO INGLÉS**, pero For3s habla **español +
código**. El diseño LOCKED eligió un modelo inglés para un agente español — habría
dado "búsquedas que no encuentran" en producción. El bug de Stella nos salvó de eso.

**Por qué BGE-M3 es la opción CORRECTA para For3s:**
- ✅ **Multilingüe (100+ idiomas, español nativo)** — lo que Stella/BGE-en NO daban.
- ✅ **1024-dim** (igual que pedía el diseño).
- ✅ **8192 tokens** de contexto (vs 512 de Stella) — útil para chunks de código/memoria.
- ✅ Arquitectura estándar (sentence-transformers), **sin código custom, sin xformers,
  sin trust_remote_code** → corre en CPU sin bugs.
- ✅ Mismo fabricante (BAAI), MIT, local, gratis, privado.

**Costo del cambio (honesto):** Stella tenía ~6 pts más de MTEB-INGLÉS (retrieval ~62
vs ~54). Pero ese score es en inglés — irrelevante para contenido español. BGE-M3 es
~560M params (más pesado que BGE-large), carga en ~160s (1ª vez) y usa ~2.6GB RAM.

**Verificado en vivo (en ESPAÑOL):**
- "error de token" vs "sesión caducó" → 0.590 (ALTA, capta sinónimos)
- "error de token" vs "receta de pastel" → 0.351 (BAJA, distingue temas)
- dim 1024 ✓ · 0.38s/4 frases · RAM pico 2.6GB.

**Cómo se carga (el patrón para el código de H5):**
```
SentenceTransformer("BAAI/bge-m3", device="cpu")   # sin trust_remote_code, sin config_kwargs
emb = model.encode(textos, normalize_embeddings=True)   # → (n, 1024)
```
Instalado: `sentence-transformers 5.6.0` + `torch 2.12.1` (CPU). Modelo en cache HF
del server. ⚠️ La 1ª carga del modelo tarda ~160s (cargar el modelo en RAM); en
producción conviene cargarlo UNA vez al arranque y reusarlo (no recargar por turno).

## EL PATRÓN CORRECTO (cómo usar el grafo desde el bot)

**Dos funciones wrapper en la BD** (creadas como superuser, con GRANT a `for3s`):

- **`cypher_write(graph_name text, query text) RETURNS void`** — para CREATE/DELETE/
  MATCH...CREATE. Hace `SET search_path` interno + `EXECUTE` del cypher() con
  dollar-quoting `$cy$`. La app la llama con `conn.execute("SELECT cypher_write($1,$2)", grafo, q)`.

- **`cypher_read_json(graph_name text, query text) RETURNS json`** — para MATCH...RETURN.
  Envuelve el resultado en `json_agg` → devuelve UN json (tipo fijo que asyncpg
  describe sin tocar el Cypher). La app la llama con
  `raw = await conn.fetchval("SELECT cypher_read_json($1,$2)", grafo, q)` y luego
  `json.loads(raw)`.

- ⚠️ `cypher_read` (RETURNS SETOF agtype) quedó de un intento anterior — **NO usar**,
  falla vía asyncpg. La buena para leer es `cypher_read_json`.

**Reglas de uso (resumen para programar H5):**
1. Las queries Cypher NUNCA usan palabras reservadas; los RETURN de propiedad llevan alias.
2. NO setear search_path en la conexión del bot (las funciones lo hacen).
3. El Cypher que se pasa NO debe contener la secuencia `$cy$` (validar a nivel app —
   también previene inyección).
4. Multi-hop verificado E2E: `MATCH (a)-[:R]->(:X)-[:R2]->(b) RETURN b.prop AS p`.

**Verificado E2E (pool del bot):** escribir nodos + relaciones, leer 1-hop y
multi-hop. Ej.: "bugs de lo que el módulo auth depende" (auth→db→bug, 2 saltos) → OK.

---

## SUB-PASO 4+5 — Columna de embeddings + backfill (2026-06-19)

**Migración 007** (schema v6→v7): añadió a `episodes_events`:
- columna `embedding vector(1024)` **NULLABLE** (los turnos viejos quedan NULL hasta
  el backfill; el bot sigue leyendo/escribiendo igual — 100% aditivo, no rompe nada).
- índice `idx_episodes_embedding` = HNSW con `vector_cosine_ops` (similitud coseno).

**Módulo `embeddings.py`** (el patrón para todo H5):
- `embed(texto)` / `embed_lote(textos)` → vectores 1024, normalizados (coseno).
- `a_pgvector(vec)` → string `'[...]'` que pgvector acepta en INSERT/UPDATE.
- **Singleton lazy del modelo** (`_get_modelo()`): BGE-M3 se carga UNA vez y se reusa.

**Backfill** (`/tmp/backfill.py`): generó el embedding de los 438 turnos existentes.
- IDEMPOTENTE (solo procesa `embedding IS NULL`) + REANUDABLE (si se corta, sigue).
  Esto SALVÓ el proceso: se cortó a 256/438 por un ajuste y se reanudó sin perder nada.
- Solo UPDATE de la columna embedding (no toca content/role/seq).

### ⚠️ LECCIÓN CRÍTICA — BGE-M3 en CPU es LENTO (afecta el diseño del sub-paso 8)
- El backfill de 438 turnos tardó ~14 min de CPU (no minutos sueltos). La carga del
  modelo sola tarda ~160s+ cada arranque.
- Lotes GRANDES con textos largos se atascan: un `encode` de 32 textos escala con el
  texto MÁS largo del lote → batches lentísimos. **Se bajó el lote de 32 a 8** para
  que cada batch termine rápido y commitee seguido (progreso fluido).
- **IMPLICACIÓN para integrar al bot (sub-paso 8):** embeber un turno nuevo toma ~3s.
  **NO se puede hacer SÍNCRONO** en el camino de respuesta del bot (añadiría ~3s a
  cada mensaje). Hay que embeber en **background/async** (tras responder, o en una
  tarea aparte). El modelo debe cargarse UNA vez al arranque del bot (no por turno).
- A futuro, si la latencia importa: GPU, o un modelo más ligero, o servicio dedicado.

**Verificado E2E:** consulta "problemas con tokens de github y autenticacion" →
recuperó por SIGNIFICADO los recuerdos reales sobre tokens/acceso/GitHub (que usaban
palabras distintas). Es lo que el MVP no podía (solo veía 12 turnos). dim 1024 ✓.

## SUB-PASO 6 — Función de búsqueda semántica (recall) (2026-06-19)

**`memory.buscar_semantico(pool, session_id, query, *, top_n=5, excluir_ultimos=0)`**
→ devuelve `list[RecuerdoRelevante]` (role, content, seq, distancia). SOLO LECTURA.

Lógica: embed la query (BGE-M3) → busca los turnos más cercanos por distancia
coseno (`embedding <=> $query::vector`, índice HNSW) filtrando por `session_id`.

Decisiones de diseño:
- **Tipo `RecuerdoRelevante`** (no Turn): añade `distancia` (0=idéntico, mayor=menos
  parecido) y `seq` (cuándo) → el caller puede umbralizar/ordenar.
- **Filtra por session_id** (no mezcla conversaciones; base del aislamiento workspace).
- **`excluir_ultimos`**: ignora los N turnos más recientes (esos ya entran por
  load_history/ventana reciente) → evita duplicados al integrar en el sub-paso 8.
- **Import LAZY de embeddings** dentro de la función: importar `memory` NO carga el
  modelo pesado (el bot importa memory siempre; el modelo solo se carga al buscar).
- **DEFENSIVA**: si el modelo falla → devuelve [] (degrada), no rompe el turno.
- Solo considera turnos con `embedding IS NOT NULL`.

**Verificado E2E:** 3 queries reales recuperaron los recuerdos correctos por
significado; filtro de sesión (inexistente → 0); `excluir_ultimos=50` baja el seq
máximo devuelto (313 vs 359). No tocó el motor de memoria existente.

## SUB-PASO 7 — Knowledge Graph navegable (kg.py) (2026-06-19)

**Decisión de poblado (Brian):** en H5 el grafo se puebla con EXTRACCIÓN SIMPLE de
entidades obvias (repos/owners/issues/PRs que ya están en gh_resources), SIN LLM. La
consolidación inteligente episodios→conceptos sigue siendo H6 (CLS).

**Módulo `kg.py`** — capa limpia sobre las funciones SQL de AGE. Esquema:
```
(Owner {nombre})  -[:DUENO_DE]->  (Repo {nombre:"owner/repo"})
(Repo)            -[:TIENE]->     (Issue {repo, numero, titulo})
(Repo)            -[:TIENE]->     (PullRequest {repo, numero, titulo})
```
Funciones: `registrar_repo`, `registrar_recurso`, `repos_de_owner`,
`recursos_de_repo`, `stats`.

Decisiones de diseño:
- **MERGE (no CREATE)** → idempotente: re-registrar el mismo repo NO duplica.
- **Defensivo** (`_write`/`_read` tragan errores): el grafo es secundario, no debe
  tumbar el guardado del turno.
- **Sanitización `_esc()`**: comillas simples duplicadas + quita `$cy$` (rompería el
  dollar-quote del wrapper) + tope 500 chars. (Para input de usuario; previene
  inyección Cypher básica.)
- Respeta las 5 reglas de AGE (incl. la nueva trampa 5: RETURN de 1 columna / mapa).

**Verificado E2E:** registrar 3 repos + 3 recursos → navegar (repos del owner,
issues/PRs del repo) → idempotencia (re-registrar no duplica) → stats
`{Owner:2, Repo:3, Issue:2, PullRequest:1}`. Grafo de prueba limpiado al final.

⚠️ **NO integrado al bot todavía** (eso es sub-paso 8). En H5 `kg.py` existe y
funciona; conectarlo al flujo de guardado (cuando el bot persiste gh_resources) +
exponerlo en build_context es el sub-paso 8.

## SUB-PASO 8 — Integración al bot (3 piezas) — PIEZA A hecha (2026-06-19)

El sub-paso más delicado: conectar la memoria nueva al flujo REAL del bot en
producción. Dividido en 3 piezas independientes (cada una verificada por separado).

### ✅ PIEZA A — Recuerdos semánticos en el contexto (EN PRODUCCIÓN)
Cuando el usuario escribe, además de los últimos 12 turnos (`load_history`), el bot
busca por SIGNIFICADO recuerdos relevantes de TODO el historial y los añade al
contexto de Claude. Es lo que el MVP no podía (solo veía 12 turnos).

Implementación (`conversation.py send()`):
- Tras cargar el historial, llama `memory.buscar_semantico(message, top_n=3,
  excluir_ultimos=MAX_HISTORY_TURNS)`. `excluir_ultimos=12` evita duplicar lo que ya
  entra por la ventana reciente. La query es `message` (corto), NO el prompt
  enriquecido (respeta la separación memoria/Claude).
- `_formatear_recuerdos()`: filtra por relevancia (`_DIST_MAX_RECUERDO=0.75` — descarta
  recuerdos lejanos = ruido) y acorta cada uno (`_MAX_CHARS_RECUERDO=300`).
- El bloque se concatena al parámetro **`contexto`** que `ask_with_history` YA acepta
  (el mismo de la hora local) → funciona en OAuth y API-key SIN cambiar firmas.
- DEFENSIVO: `buscar_semantico` degrada a [] si el modelo falla → no rompe el turno.
- Solo se tocó `send()` (chat normal). `send_with_tools` se deja para después (su
  alternancia de roles user/assistant es delicada).

⚠️ **PRECARGA del modelo al arranque** (clave de rendimiento): BGE-M3 tarda en cargar
a RAM. Si la 1ª carga ocurriera dentro del 1er `send()`, ese mensaje se colgaría.
Solución: `telegram_channel.setup()` lanza `asyncio.create_task(_precargar_embeddings)`
→ el bot arranca YA y el modelo se carga en paralelo. Verificado: "Application started"
inmediato + "modelo de embeddings precargado" ~8s después (con caché de disco; ~160s
en frío). Defensivo: si la precarga falla, la memoria semántica degrada.

**Verificado E2E:** bot arrancó sin bloquearse; filtro de relevancia descarta ruido
(dist>0.75); búsqueda real recuperó recuerdos correctos ("acceso a github" → dist
0.26-0.39); 11 tests de regresión (test_h2/h2_integration/tg_handlers) pasan.

### ✅ PIEZA B — Embedding de turnos NUEVOS en background (EN PRODUCCIÓN)
Sin esto la memoria semántica se congelaría en el turno 438 (backfill): los turnos
nuevos quedarían con embedding NULL y no serían buscables. Ahora cada turno nuevo
(user y assistant) se embebe automáticamente.

Implementación:
- **`memory.embeddear_turno(pool, session_id, seq, content)`**: calcula el embedding
  en un thread (`to_thread`, no congela el loop) y hace `UPDATE ... SET embedding
  WHERE session_id+seq`. Solo toca la columna embedding. DEFENSIVA (error → False,
  turno queda NULL, recuperable por backfill). Idempotente.
- **`Conversation._embeber_bg(seq, content)`**: dispara `asyncio.create_task` de lo
  anterior — FIRE-AND-FORGET (no espera). Verificado: el disparo toma 0.000s → la
  respuesta del bot NO se ralentiza. El embedding (~3s) se calcula aparte.
- **Referencia retenida** (`self._bg_tasks` set + done_callback): asyncio solo guarda
  weakrefs de las tasks → sin esto el GC podría matarlas antes de terminar.
- Disparado en `send()` tras CADA `record_turn` (user y assistant). `record_turn`
  NO se tocó (es el punto más sensible: lo usan CLI/Telegram/web/adjuntos/repos).
- Sin event loop (contexto CLI sync) → se ignora (se embeberá por backfill).

**Verificado E2E:** turno nuevo → disparo 0.000s (no bloquea) → embedding se llena en
background → el turno queda BUSCABLE semánticamente. 11 tests de regresión pasan.

### ✅ PIEZA B-ext — Embeddings en TODOS los flujos (EN PRODUCCIÓN, 2026-06-20)
La Pieza B original solo cubría `send()`. La auditoría del flujo completo reveló que
los turnos de GitHub (`send_with_tools`, `analizar_repo_completo`, `continuar`,
`listar_org`) quedaban con embedding NULL → no buscables. Extensión:
- **Helper `Conversation._guardar_turno(...)`**: envuelve `record_turn + _embeber_bg`
  en uno. Reemplazó los 10 call-sites de `record_turn` en conversation.py → es
  IMPOSIBLE olvidar embeber un flujo (todos pasan por el helper).
- **⚠️ BUG GRAVE cazado:** la transformación automática de los call-sites convirtió
  el `record_turn` DENTRO del propio `_guardar_turno` en una llamada recursiva a sí
  mismo (recursión infinita que habría colgado el bot). Lo detectó ruff (línea larga)
  + revisión. Lección: tras un reemplazo masivo automático, SIEMPRE revisar + lint +
  tests antes de desplegar. Corregido: el helper llama a `memory.record_turn` real.
- Verificado E2E (con modelo precargado): turno de flujo-GitHub → embedding lleno.

### ✅ PIEZA C — Poblar el grafo al leer GitHub (EN PRODUCCIÓN, 2026-06-20)
Enganchado dentro de `save_gh_tool_calls` (memory.py): tras el INSERT a gh_resources,
si hay owner/repo → `kg.registrar_repo`; si kind in (issue,pr) → `kg.registrar_recurso`.
- try/except PROPIO + import lazy: si el grafo falla, JAMÁS afecta el guardado de
  gh_resources (lo importante). kg.py ya es defensivo+idempotente (doble seguridad).
- Verificado E2E + en vivo: al analizar `cli/cli`, el grafo registró Owner+Repo.

### ✅ AFINADO de la memoria semántica (EN PRODUCCIÓN, 2026-06-20)
La auditoría en vivo reveló que el bot respondía CONSERVADOR ("no hemos hablado de
eso") por RUIDO en los recuerdos recuperados. Diagnóstico (NO era el umbral):
1. La query se recuperaba a SÍ MISMA (dist ~0) como recuerdo → ruido inútil.
2. Recuerdos duplicados (preguntas repetidas en pruebas).
3. **BUCLE de auto-confirmación**: el bot recuperaba su PROPIA negación vieja
   ("no hemos hablado de tokens") como recuerdo → la leía → la repetía.

Ajustes en `_formatear_recuerdos` + `buscar_semantico`:
- `_DIST_MIN_RECUERDO = 0.05`: excluye recuerdos casi-idénticos a la query (la
  pregunta a sí misma / duplicados exactos).
- **Dedup** por texto normalizado (colapsa preguntas repetidas a una).
- **Prompt afirmativo**: "CONTEXTO DE TU MEMORIA — esto SÍ se habló... son datos
  reales" (antes: "úsalos solo si aplican", demasiado tímido).
- **`solo_usuario=True`** (el arreglo clave): la memoria semántica solo inyecta
  turnos del USUARIO, NO las respuestas del bot → corta el bucle de raíz (la
  negación vieja es del bot → ya no entra). Las preguntas del usuario son la mejor
  señal de qué se habló.

Verificado en vivo: tras el afinado, el contexto inyectado quedó limpio (sin la
negación vieja, sin copias) y el bot responde HONESTO. Hallazgo de Brian: el bot
decir "no hemos hablado de tus tokens" es LITERALMENTE CIERTO — nunca dio tokens en
el chat (el PAT se configuró en el server). El bot ya NO infla/alucina.
⏳ PENDIENTE (anotado en PENDIENTES.md §hallazgos, "H5-mem-matiz"): afinar el JUICIO
del bot sobre "qué cuenta como haber hablado de un tema" (decir "de tokens no, pero
sí trabajamos mucho con GitHub" en vez de un "no" tajante). Es matiz de interpretación,
no de recuperación. Retomar más adelante.

## Seguridad / pendientes para H5

- El grafo `for3s_kg` es hoy GLOBAL. Cuando llegue multi-tenant, el aislamiento por
  `workspace_id` debe aplicarse (un grafo por workspace, o filtro en cada query).
- Las funciones wrapper interpolan el Cypher como texto → **validar/sanitizar a nivel
  app** lo que venga de usuario (no meter input crudo en el MATCH). Para valores de
  usuario, usar parámetros Cypher, no concatenación.
- Backup antes de cada migración pesada (se hizo: `~/for3s-backups/pre_h5_*.sql`).

---

## Cómo recrear esto (si se pierde / nuevo entorno)
1. `CREATE EXTENSION vector;` y `CREATE EXTENSION age;` (como superuser).
2. `ALTER SYSTEM SET shared_preload_libraries = 'age';` + reiniciar Postgres.
3. `LOAD 'age'; SET search_path=ag_catalog,public; SELECT create_graph('for3s_kg');`
4. GRANT de ag_catalog + ownership del schema for3s_kg al usuario `for3s`.
5. Crear las funciones `cypher_write` y `cypher_read_json` (SQL guardado en el
   changelog/scratch de la sesión 2026-06-19).