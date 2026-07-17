# Anexo R4.2.1 — Migración GitHub al estándar MCP + Persistencia

> **Tipo:** Documento de diseño de implementación (anexo de R4 Bloque 2, sub-tema 4.2.1 GitHub MCP).
> **Estado:** PROPUESTA — pendiente aprobación de Brian antes de programar.
> **Fecha:** 2026-06-13.
> **Regla:** R4 §4.2.1 es LOCKED y es la fuente de verdad. Este anexo NO la contradice;
> traza el plan de migración del estado actual (H4 artesanal) hacia R4, y resuelve
> dos huecos que R4 no cubrió (persistencia en BD + puente tool_use↔MCP con OAuth).

---

## 0. Por qué este documento

Durante el endurecimiento de H4 (2026-06-13), al probar la integración GitHub a fondo,
Brian destacó que GitHub es una pieza estratégica de la que "salen muchos datos para
los siguientes H". El análisis profundo reveló tres cosas:

1. **Lo que construimos en H4 es artesanal y se desvía del diseño LOCKED de R4.**
   `github_tool.py` (403 líneas) llama la API REST de GitHub a mano con `httpx`,
   detecta recursos con regex (`detect_resource`), y soporta solo leer UN recurso
   específico (PR/issue/gist/blob). R4 §4.2.1 había decidido usar el **GitHub MCP
   server oficial** con 26 tools (read+write).

2. **NO persistimos los datos de GitHub.** Verificado en BD: al analizar el PR #134
   trajimos ~11k tokens de contexto, generamos el reporte, y **tiramos los datos
   crudos**. Solo queda en `episodes_events` el mensaje del usuario (72 chars) y el
   reporte que Claude escribió (5500 chars). El PR (título, autor, archivos, diff)
   NO se guardó. Si mañana preguntan "¿qué decía el PR 134?", For3s tendría que
   re-traerlo. **Este es un hueco real: R4 habla de CACHE temporal (Valkey TTL), no
   de persistencia permanente.**

3. **El diseño correcto YA existe en R4 (LOCKED).** Lo que Brian pidió hoy
   ("estandaricemos, no inventemos") coincide 100% con la decisión LOCKED de R4.2.1.
   No reinventamos: alineamos la implementación con el diseño.

---

## 1. Estado actual vs R4 LOCKED — la desviación

```
   ┌────────────────────────┬──────────────────────┬─────────────────────────┐
   │ ASPECTO                │ H4 ACTUAL (artesanal) │ R4 LOCKED (objetivo)    │
   ├────────────────────────┼──────────────────────┼─────────────────────────┤
   │ Cómo accede a GitHub   │ httpx → API REST a    │ GitHub MCP server       │
   │                        │ mano (github_tool.py) │ OFICIAL Anthropic       │
   │ Cómo decide usar GitHub│ regex (detect_resource│ tool-use NATIVO del     │
   │                        │ + detect_short_ref)   │ modelo (26 tools)       │
   │ Operaciones            │ leer 1 recurso        │ 14 read · 9 write ·     │
   │                        │ (PR/issue/gist/blob)  │ 4 destructive           │
   │ Listar issues/PRs      │ ❌ no soportado       │ ✅ list_issues, etc.    │
   │ Leer código completo   │ ❌ solo diff del PR   │ ✅ get_file_contents    │
   │ Escribir (comentar/PR) │ ❌ no                 │ ✅ write tools          │
   │ Persistencia datos     │ ❌ se tiran           │ 🟡 cache Valkey (hueco) │
   │ Auth GitHub            │ PAT cifrado (KEK) ✅  │ PAT por workspace ✅    │
   │ Audit                  │ ✅ gh_fetched         │ ✅ por cada call        │
   └────────────────────────┴──────────────────────┴─────────────────────────┘
```

**Conclusión:** H4 fue un MVP rápido y válido para arrancar. La migración a MCP es
"volver al plan", no un cambio de rumbo. Lo que SÍ se conserva de H4: el modelo de
seguridad (PAT cifrado con KEK), el audit, y la separación message/prompt.

---

## 2. Decisión LOCKED de R4.2.1 (recordatorio — fuente de verdad)

De `Ronda_04_Bloque_2_MCP_Servers_Core.md`:

- **Server:** GitHub MCP server OFICIAL (`@modelcontextprotocol/server-github`,
  hoy sucesor `github/github-mcp-server`). Razón: servicio maduro, 26 tools
  out-of-box, datos viven en github.com (aislamiento vía PAT), Brian no mantiene
  código GitHub-specific.
- **26 tools:** 14 read-only (default whitelist) · 9 write (audited) · 4 destructive
  (`require_confirmation=True`).
- **Auth:** PAT por workspace, scope mínimo `repo`, expiración 90 días, inyección
  per-request (NO env vars), vía SecretsManager (la KEK que ya tenemos).
- **Cache:** Valkey con TTL por tipo de tool. Write/destructive NEVER cache.
- **Seguridad:** repo allowlist por workspace, enforcement ANTES de cada tool.
- **Escalonado en R4:** webhooks async, multi-tenant, rate limit per workspace.

> ⚠️ Nota de realidad verificada: la investigación externa (2026-06-13) advirtió que
> OAuth de suscripción estaría "prohibido" para terceros. EMPÍRICAMENTE For3s funciona
> con OAuth hoy. Decisión de Brian: diseñar sobre OAuth (nuestra realidad), anotar la
> advertencia como riesgo a vigilar. MCP es capa SEPARADA de la auth con Claude:
> GitHub-MCP autentica con PAT de GitHub, independiente de cómo hablamos con Claude.

---

## 3. HUECO 1 — Persistencia de datos GitHub en BD

R4 solo previó cache temporal (Valkey). Brian pidió persistencia permanente porque
"de aquí sale información para los siguientes H". Diseño propuesto (alineado con el
esquema H2 existente: sessions, episodes_events, audit_events).

### Principio
- **Cache (Valkey, R4) ≠ Persistencia (Postgres, este anexo).** El cache acelera
  re-lecturas en minutos. La persistencia guarda el conocimiento para SIEMPRE
  (consultable por los H futuros: memoria semántica H5, knowledge graph H6, etc.).
- **Event Sourcing-friendly:** guardamos un snapshot del recurso tal como se trajo,
  con timestamp. Si el PR cambia en GitHub, un nuevo fetch = nuevo snapshot (no
  UPDATE destructivo; append como episodes_events).

### Tablas propuestas (migración 004)

```sql
-- gh_resources: un snapshot de cada recurso de GitHub traído (PR/issue/file)
CREATE TABLE IF NOT EXISTS gh_resources (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    workspace_id  TEXT NOT NULL DEFAULT 'default',
    session_id    TEXT REFERENCES sessions(id),   -- en qué conversación se trajo
    kind          TEXT NOT NULL CHECK (kind IN ('pr','issue','file','gist')),
    owner         TEXT NOT NULL,
    repo          TEXT NOT NULL,
    number        INTEGER,            -- PR/issue number (NULL para file/gist)
    path          TEXT,               -- para file/gist
    title         TEXT,
    author        TEXT,
    state         TEXT,               -- open/closed/merged
    body          TEXT,               -- descripción/cuerpo
    raw           JSONB NOT NULL DEFAULT '{}'::jsonb,  -- metadata completa estructurada
    fetched_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_gh_res_lookup ON gh_resources (workspace_id, owner, repo, kind, number);
CREATE INDEX IF NOT EXISTS idx_gh_res_session ON gh_resources (session_id);

-- gh_files: archivos/diffs asociados a un recurso (1 PR → N archivos)
CREATE TABLE IF NOT EXISTS gh_files (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resource_id   BIGINT NOT NULL REFERENCES gh_resources(id) ON DELETE CASCADE,
    filename      TEXT NOT NULL,
    status        TEXT,               -- added/modified/removed
    additions     INTEGER DEFAULT 0,
    deletions     INTEGER DEFAULT 0,
    patch         TEXT,               -- diff (posiblemente truncado)
    content       TEXT,               -- contenido completo si se trajo (get_file_contents)
    truncated     BOOLEAN DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_gh_files_resource ON gh_files (resource_id);
```

### Qué se guarda y qué NO
- ✅ Guardar: metadata (título, autor, estado, body), archivos (filename, diff,
  contenido), timestamp del fetch. → consultable por H futuros.
- ❌ NO meter en el prompt de cada turno (eso infla la memoria — la lección del
  bug PR #134). La memoria conversacional (`episodes_events`) sigue guardando solo
  mensaje corto + reporte. Los datos crudos viven en `gh_resources`/`gh_files`,
  consultables on-demand.
- **Relación:** `gh_resources.session_id` enlaza con la conversación donde se trajo,
  pero el dato es del workspace (sobrevive a la sesión).

### Reemplaza al "repo recordado" del Bug F
El Bug F guardó `last_repo` en `sessions.meta`. Con `gh_resources` el "último repo"
se deriva con `SELECT ... ORDER BY fetched_at DESC LIMIT 1`. Mantener `sessions.meta`
como atajo o migrar — decisión menor en implementación.

---

## 4. HUECO 2 — Puente tool_use ↔ MCP con nuestro agente OAuth

R4 asume MCP pero no definió cómo nuestro agente Python (que habla con Claude vía
OAuth, NO es Claude Code) conecta las tools MCP. Diseño:

### El flujo (verificado con docs MCP + Anthropic tool-use)
```
   1. Al arrancar: el bot lanza el GitHub MCP server como subproceso
      (Docker local `ghcr.io/github/github-mcp-server` o binario, stdio),
      con el PAT inyectado (descifrado de la KEK).
   2. Cliente MCP Python (pip install mcp) → session.list_tools()
      → obtiene las 26 tools con su JSON Schema.
   3. Filtrar a la whitelist (14 read en MVP) y traducir al formato Anthropic:
      {name, description, input_schema}.
   4. Pasar esas tools a Claude en cada messages.create(..., tools=[...]).
   5. PUENTE MANUAL: cuando Claude responde con stop_reason="tool_use":
      • extraer el bloque tool_use {id, name, input}
      • session.call_tool(name, input)  ← llamada MCP
      • PERSISTIR el resultado en gh_resources/gh_files (Hueco 1)
      • devolver tool_result {tool_use_id, content} a Claude
   6. Loop hasta stop_reason="end_turn".
```

### Implicaciones
- **Reemplaza `detect_resource` (regex) por tool-use nativo.** El MODELO decide
  cuándo leer un PR/issue/listar. Adiós a la fragilidad del regex (causa del Bug F).
- **agent.py / conversation.py / llm.py cambian:** hoy hacen una llamada simple a
  Claude. Necesitan el LOOP de tool-use (multi-turno interno). Es el cambio más
  grande. R3 (LLM layer) y R4 (tools) ya lo contemplaban como el destino.
- **Compatibilidad OAuth:** el tool-use estándar (tool_use/tool_result) va en el
  cuerpo de la Messages API — funciona igual con OAuth (que ya usamos). MCP es
  subproceso local con PAT, no toca la auth de Claude.
- **asyncio:** el SDK MCP es async, igual que python-telegram-bot. Conviven. La
  ClientSession MCP vive mientras el bot esté arriba.

---

## 5. Alcance de ESTA fase (MVP del MCP) — decisión de Brian

```
   ENTRA EN ESTA FASE (leer + listar + persistir):
   ✅ Lanzar GitHub MCP server local (Docker/binario) con PAT de la KEK
   ✅ Cliente MCP Python + puente tool_use↔MCP en el loop del agente
   ✅ Whitelist READ (14 tools): get_pull_request, list_pull_requests,
      get_issue, list_issues, get_file_contents, search_code, etc.
   ✅ Persistencia: tablas gh_resources + gh_files (migración 004)
   ✅ Resuelve de raíz: listar (hueco del endurecimiento) + leer código completo
      + referencias naturales (el modelo entiende, sin regex)
   ✅ Audit por cada tool call (ya lo tenemos)

   QUEDA PARA H FUTUROS (como R4 los escalonó):
   ⏳ Write tools (comentar, crear PR) → con require_confirmation
   ⏳ Destructive (merge, delete) → require_confirmation
   ⏳ Webhooks GitHub async (Arq)
   ⏳ Multi-tenant / multi-workspace / repo allowlist completo
   ⏳ Cache Valkey con TTL (optimización; la persistencia BD ya da el dato)
```

---

## 6. Orden de implementación incremental (propuesto)

```
   PASO 1 — Infra MCP: lanzar el GitHub MCP server local + cliente MCP Python.
            Verificar list_tools() trae las 26. (sin tocar el agente aún)
   PASO 2 — Migración 004: crear tablas gh_resources + gh_files.
   PASO 3 — Puente: loop de tool-use en el agente (read tools whitelist).
            Probar: "lee el PR 134" → el modelo llama get_pull_request.
   PASO 4 — Persistencia: cada tool result se guarda en gh_resources/gh_files.
   PASO 5 — Listar: "¿cuál es el issue más reciente?" → list_issues. (cierra
            el hueco que Brian descubrió hoy)
   PASO 6 — Retirar lo artesanal: deprecar detect_resource/github_tool.py una
            vez que MCP cubre todo. Migrar tests.
   PASO 7 — DEMO verificada por Brian + cerrar.
```

Cada paso: explicar a Brian → aprobar → implementar → Brian prueba → commit.
(Regla NUNCA implementar primero.)

---

## 7. Qué pasa con el endurecimiento de H4 en curso

El endurecimiento de H4 tiene 1 bug pendiente: **G (editMessageText 400 del cupo)**.
Es independiente de GitHub. Decisión pendiente de Brian: cerrar G antes de empezar
esta migración, o empezar la migración y dejar G para después. (No bloquea.)

---

## 8. Riesgos y mitigaciones

```
   RIESGO                                  MITIGACIÓN
   ─────────────────────────────────────────────────────────────────────
   El loop de tool-use es el cambio        Implementar incremental (paso 3),
   más grande (toca agent/conversation)    probar con 1 tool antes de las 14.
   MCP server local = nueva pieza viva     Docker aislado; si cae, el bot sigue
                                           (degradar a "GitHub no disponible").
   OAuth + tool-use no probado juntos      Paso 3 lo verifica antes de seguir.
   Advertencia OAuth de terceros           Anotado como riesgo; plan B = API key.
   Persistencia infla BD                   Solo metadata + diffs; no todo el repo.
```

---

## 9. Decisión pendiente

Brian debe aprobar:
- [ ] El esquema de tablas (gh_resources / gh_files) del Hueco 1.
- [ ] El enfoque del puente tool_use↔MCP del Hueco 2.
- [ ] El alcance MVP (read+listar+persistir; write/webhooks a futuro).
- [ ] Si cerrar Bug G antes o empezar la migración primero.

Aprobado esto → se implementa en el orden del §6, paso a paso.