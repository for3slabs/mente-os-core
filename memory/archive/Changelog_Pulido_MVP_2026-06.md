# Changelog técnico — Pulido del MVP (sesiones 2026-06-15 a 2026-06-18)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Changelog_Pulido_MVP_2026-06.md → memory/archive/Changelog_Pulido_MVP_2026-06.md (2026-07-30, ADR-029)

> **Qué es:** registro detallado y trazable de TODO lo que se cambió en el código
> de For3s OS durante el pulido del MVP. **Propósito:** si algo deja de funcionar,
> aquí está EXACTAMENTE qué se tocó, en qué archivo, por qué, y cómo se verificó —
> para poder rastrear el origen del cambio y revertir o arreglar con contexto.
>
> **Servidor:** `for3s` (Tailscale 100.112.177.53). Código en
> `~/for3s-os/packages/for3s-core/src/for3s_core/`. Deploy: systemd
> `for3s-telegram.service` (`sudo systemctl restart for3s-telegram`).
> Modelo en producción: `claude-sonnet-4-6` (OAuth de suscripción) — a propósito.
> Tests: `cd ~/for3s-os && uv run pytest -q` → **123 passed, 4 skipped** (2026-06-18).
> Lint: `uv run ruff check <archivo>`.

---

## 📋 Cómo usar este doc para debuggear

1. ¿Falla algo relacionado con **leer páginas web / SPAs / Amazon**? → §1 (web_fetch).
2. ¿Falla con **fotos / PDF / Word / Excel**? → §2 (multimodal).
3. ¿Falla un **conteo de PRs/issues**? → §3 (search tools).
4. ¿Falla al **comentar / crear issue o PR** (botones)? → §4 (write tools).
5. ¿Lentitud o datos viejos de GitHub? → §5 (cache Valkey).
6. ¿El bot **no arranca** tras un cambio? → ver §7 (cómo verificar) + revisar
   `journalctl -u for3s-telegram`.

Regla de oro: cada feature tiene **tests** en `tests/test_pulido_mvp.py`. Si algo
se rompe, correr `uv run pytest tests/test_pulido_mvp.py -q` aísla rápido si el
problema es de lógica pura o de integración/red.

---

## 1. Web fetch híbrido (JS/SPA + login + redirects + anti-bot)

**Archivo:** `web_fetch.py` · **Infra nueva:** imagen Docker `for3s-render`
(`~/for3s-os/docker/render/Dockerfile` + `render.py`).

**Qué cambió y por qué:**
- For3s no podía leer SPAs (páginas que pintan todo con JS): el HTML llegaba vacío.
- **Solución 2 capas:** `fetch_url()` intenta httpx primero (rápido); si el
  contenido es pobre (<350 chars = `UMBRAL_SPA`, una SPA cáscara), cae al
  contenedor `for3s-render` (imagen oficial de Playwright + Chromium headless) que
  ejecuta el JS y devuelve el texto pintado.
- **Por qué Docker y no Playwright directo:** el server es Ubuntu 26.04, y
  Playwright NO tiene build nativo para esa versión. El contenedor lo sortea.
- **Login:** `_huele_a_login()` → aviso honesto, NO pelea el muro de sesión.
- **Redirects:** httpx ya los seguía; ahora se EXPONE la URL final
  (`ENLACE FINAL: …`) tras seguir links cortos (a.co/bit.ly/amzn.to).
- **Anti-bot:** `_huele_a_antibot()` (Amazon "continue shopping", Cloudflare, etc.)
  → aviso honesto + dice a dónde llevaba el link. NO pelea el anti-bot.

**Funciones clave:** `fetch_url`, `_render_headless` (lanza el contenedor),
`_html_a_texto`, `_largo_contenido`, `_huele_a_login`, `_huele_a_antibot`,
`_normaliza`. Constantes: `UMBRAL_SPA=350`, `RENDER_IMAGE="for3s-render:latest"`,
`RENDER_TIMEOUT=45.0`.

**Punto de fallo posible:** si el contenedor `for3s-render` no existe o Docker
está caído, `_render_headless` devuelve error y se degrada a lo que trajo httpx.
Reconstruir imagen: `cd ~/for3s-os/docker/render && docker build -t for3s-render:latest .`

**Verificado:** example.com (httpx 1.7s), react.dev (render 2.6s), Amazon
(aviso anti-bot + URL), httpbin redirect (muestra ENLACE FINAL).

---

## 2. Multimodal — imágenes + PDF + Word + Excel

**Archivos:** `multimodal.py` (NUEVO) · `llm.py` · `agent.py` · `conversation.py`
· `telegram_channel.py`. **Deps nuevas:** `python-docx`, `openpyxl`.

**Qué cambió y por qué:**
- For3s era solo-texto: ignoraba fotos/documentos. Ahora los LEE.
- **`multimodal.py` → `procesar_adjunto(datos, nombre, mime)`** convierte un
  archivo en bloques de contenido para la API de Messages:
  - Imágenes (jpg/png/gif/webp) → bloque `image` base64 (visión nativa de Claude).
  - PDF → bloque `document` base64 (lectura nativa; requiere beta `pdfs-2024-09-25`).
  - Word (.docx) → texto extraído con `python-docx`.
  - Excel (.xlsx) → celdas extraídas con `openpyxl`.
  - Límites: `MAX_BYTES=20MB`, errores claros (`ArchivoNoSoportado`).
- **`llm.py` → `complete(..., adjuntos=None)`:** si vienen adjuntos, el `content`
  pasa de string a lista de bloques. Si hay un PDF, añade el beta `pdfs` (constante
  `PDFS_BETA`). `_headers(betas_extra=...)` ahora acepta betas por-request.
- **`agent.py` → `ask_with_history(..., adjuntos=None)`** y **`conversation.py` →
  `send(..., adjuntos=None)`** encadenan los adjuntos. ⚠️ El base64 NO se guarda en
  memoria (solo una nota de texto) — el base64 es enorme.
- **`telegram_channel.py` → `on_adjunto`** (NUEVO handler): captura PHOTO y
  Document.ALL, descarga el archivo, lo procesa y lo manda a Claude. Registrado en
  el builder: `MessageHandler(filters.PHOTO, ...)` + `filters.Document.ALL`.

**⚠️ Efecto colateral ARREGLADO (2026-06-18):** añadir `adjuntos` a `complete()`
rompió `tests/test_h2.py::test_agente_arma_historial` (su `FakeProvider.complete`
mock no aceptaba el param). Arreglado: el FakeProvider ahora acepta `adjuntos` +
`**kwargs`. **Lección:** al añadir params a `complete()`/`ask_with_history`,
revisar los mocks en tests/.

**Audio:** DESCARTADO por ahora (Whisper ~1-2GB para algo poco usado).

**🐞 FIX (2026-06-19) — PDF/adjunto grande daba ReadTimeout:** en pruebas en vivo,
un PDF grande hacía `httpcore.ReadTimeout` en `on_adjunto` → "error procesando
adjunto" (y de rebote el modelo improvisaba "soy solo texto"). Causa: el provider
tenía timeout HTTP de 60s (default `llm.py`); un base64 grande hace que Claude
tarde más. Arreglo 2 capas: (1) `ClaudeProvider(timeout=180.0)` en
`telegram_channel.setup` (alineado con ANALYSIS_TIMEOUT) — beneficia también
repos grandes; (2) `multimodal._exigir_no_gigante`: si un PDF/imagen supera
`MAX_BYTES_NATIVO` (8MB) → aviso honesto ("mándame las páginas clave") en vez de
morir por timeout. 2 tests nuevos. NOTA: los PDF chicos siempre funcionaron (18
páginas verificado); esto cubre los grandes.

**🐞 FIX (2026-06-19) — "comentar en un repo" no funcionaba (routing write):** en
pruebas en vivo, pedir "comenta X en el issue de github.com/o/r" daba "no puedo
comentar" o "no pude listar el repo". Causa RAÍZ: era un bug de ROUTING, no de las
write tools. Un URL de repo completo activaba `extraer_owner_repo` → el mensaje se
enrutaba a `analizar_repo_completo` (flujo de ANÁLISIS), que intentaba listar
archivos del repo y nunca llegaba a proponer la escritura. Arreglo en
`telegram_channel.on_message`: detector `quiere_escribir` (palabras comenta/crear
issue/PR/review) — si hay intención de escritura, se fuerza `repo_completo=None`
para que el mensaje caiga en la rama `usa_tools` → `send_with_tools` → las write
tools con botón de confirmación. Verificado: "comenta…" → write, "analiza…" →
análisis (sin colisión). 1 test nuevo. (El otro factor de la prueba fallida: el
repo `fruterito101/Proyecto` estaba VACÍO sin issue #1 — para reprobar usar un
repo con un issue real.)

**Verificado E2E con API real (OAuth+sonnet-4-6):** imagen roja→"Rojo",
PDF con texto→leyó "FRUTERO-2026". Word/Excel por tests unitarios.

---

## 3. Conteos GitHub exactos (search tools)

**Archivos:** `tool_loop.py` (`MVP_TOOLS`) · `conversation.py` (`TOOL_DIRECTIVE`).

**Qué cambió y por qué:**
- Contar "cuántos PRs cerrados" PAGINANDO con `list_*` (30-100/página) agotaba el
  loop (`MAX_TOOL_ROUNDS=5`) en repos grandes → conteo parcial.
- **Fix:** añadir `search_issues` + `search_pull_requests` a `MVP_TOOLS`. Devuelven
  `total_count` EXACTO en 1 llamada (query `repo:o/n is:closed` + perPage=1).
- Guía en `TOOL_DIRECTIVE`: usar search SOLO para contar, no para listar.
- **NO se subió `MAX_TOOL_ROUNDS`** (sigue en 5) — subirlo dispara el rate-limit.
  Hay un test que lo protege (`test_max_tool_rounds_no_subio`).

**Verificado E2E:** "¿PRs cerrados de cli/cli?" → el agente usó
search_pull_requests → **4206** (número real).

---

## 4. Write tools de GitHub (subconjunto seguro CON confirmación)

**Archivos:** `mcp_client.py` (`ejecutar_write`) · `tool_loop.py` (gate +
whitelist + schemas) · `conversation.py` (propaga `accion_pendiente`) ·
`telegram_channel.py` (botones + ejecución). **Sin dep nueva** (usa el MCP server).

**Qué cambió y por qué:** For3s pasó de read-only a poder ESCRIBIR, pero SOLO 4
acciones reversibles y SIEMPRE con confirmación por botón.

**Las 4 write permitidas** (`WRITE_TOOLS_PERMITIDAS` en `tool_loop.py`):
`add_issue_comment`, `create_issue`, `create_pull_request`,
`create_pull_request_review`. NADA destructivo.

**Arquitectura de seguridad (3 capas):**
1. **Cliente de lectura sigue read-only SIEMPRE** (`GitHubMCPClient(read_only=True)`).
   La escritura usa `mcp_client.ejecutar_write(pat, name, args)` — un contenedor
   MCP write-capable EFÍMERO que se levanta solo para la write confirmada y muere.
2. **Gate de intención** (`tool_loop.py`, en el bucle de ejecución de tools): si la
   tool está en `WRITE_TOOLS_PERMITIDAS` → NO la ejecuta, la captura en
   `out.accion_pendiente`. Si es cualquier otra write/destructive → RECHAZO duro.
   Los schemas de las write se INYECTAN a mano (`WRITE_TOOL_SCHEMAS`) porque el
   MCP read-only no las expone.
3. **Confirmación por botón** (`telegram_channel.py`): `_proponer_write` muestra
   InlineKeyboard ✅/❌ + preview (`_preview_write`); `on_confirmar_write`
   (CallbackQueryHandler, pattern `^w(ok|no):`) ejecuta al confirmar. Expira a
   5 min, solo el dueño confirma. Estado en `self._writes_pendientes` (dict por id).
   PAT guardado en `self._pat` (en `setup`).

**Audit:** cada escritura → `audit.append(action="github_write", ...)`; cada
cancelación → `github_write_cancelado`. Cadena inmutable.

**Flujo del dato:** `conversation.accion_pendiente` (atributo, porque LLMResponse
es frozen) ← `run_tool_loop` devuelve `result.accion_pendiente`. El canal lo lee
tras `send_with_tools`.

**Punto de fallo posible:** si el botón no aparece, revisar que
`CallbackQueryHandler` esté registrado y que `convo.accion_pendiente` se setee. Si
la write falla al confirmar, el error se audita igual (`ok: false`).

**Verificado E2E:** pidió comentar → propuso add_issue_comment (args correctos),
`tool_calls ejecutadas=[]` (NO escribió), texto "confirma abajo".

**Nota PAT:** el `ghp_` ya tiene scope `repo`+`workflow` (puede crear/operar). La
whitelist dura es lo que impide que For3s use ese poder para algo destructivo.

---

## 5. Cache Valkey de lecturas de GitHub

**Archivos:** `cache.py` (NUEVO) · `tool_loop.py` (integración) · `conversation.py`
(singleton + workspace_id). **Dep nueva:** `redis` 8.0. **Infra:** Valkey ya
corría en `127.0.0.1:6379`.

**Qué cambió y por qué:**
- Re-leer lo mismo de GitHub gastaba llamadas a la API. Ahora se cachea.
- **`cache.py` → `GitHubCache`:** capa async sobre Valkey.
  - `cacheable(name)` → TTL si la tool es cacheable, None si no (`CACHEABLE_TOOLS_TTL`:
    get_file_contents 300s, list_* 30s, search_code 900s, etc.).
  - `NEVER_CACHE` (status/files de PR) y TODAS las write → None (no cachean).
  - `_key(workspace_id, name, args)` → key estable (args ordenados, hash) con
    workspace_id (multi-tenant futuro, sin reescribir).
  - **DEFENSIVA:** si Valkey falla, get→None (lee de GitHub), set→no-op. El bot
    NUNCA se cae por el cache. `socket_timeout=1.5s`.
- **`tool_loop.py`:** `run_tool_loop(..., cache=None, workspace_id="default")`. En
  el gate READ: mira cache → hit lo usa, miss ejecuta + guarda. Las write NO tocan
  cache. `tool_calls` ahora incluye `"cacheado": bool`.
- **`conversation.py`:** singleton perezoso `_get_gh_cache()`; `send_with_tools`
  pasa `cache=_get_gh_cache(), workspace_id=self._session_id`.

**Punto de fallo posible:** si Valkey muere, NO pasa nada (degrada). Verificar
Valkey: `systemctl status valkey-server`. Limpiar cache: el cliente apunta a
`:6379` DB 0, keys con prefijo `for3s:gh:`.

**Verificado E2E:** 1ª lectura MISS→GitHub (0.56s), 2ª lectura HIT→Valkey (0.000s),
contenido idéntico.

---

## 5b. Apartados de ARCHIVOS y WEB consultados (migración 006, 2026-06-19)

**Archivos:** `migrations/006_consulted.sql` (NUEVO) · `memory.py` · `telegram_channel.py`.

**Qué cambió y por qué:** antes los documentos (PDF/Word/Excel/img) y las páginas
web que el usuario manda se procesaban y se TIRABAN (solo quedaba msg+respuesta en
episodes_events). Brian pidió un registro LIGERO de "qué me han mandado".

- **`consulted_files`** (tabla nueva): `tipo, nombre, resumen, consulted_at` +
  session/workspace. SIN el binario (el PDF/imagen NO se guarda — pesa megas,
  innecesario). El `resumen` = el análisis que ya generó Claude.
- **`consulted_web`** (tabla nueva): `url, titulo, descripcion, consulted_at` +
  session/workspace. SIN el HTML. El título se saca de la cabecera `TÍTULO:` que
  arma web_fetch; la descripción = la respuesta de Claude.
- **`memory.save_consulted_file()` / `save_consulted_web()`**: DEFENSIVAS (si
  fallan, no rompen el turno — son registro secundario). Resumen topado a 2000
  chars (no volcar análisis enteros).
- **Conectado:** `on_adjunto` guarda el archivo tras responder; el flujo `url_web`
  de `on_message` guarda la web tras `fetch_url`.
- **TODA fila tiene `consulted_at` (TIMESTAMPTZ)** — directriz de Brian: saber
  CUÁNDO se consultó es clave para el panorama de cómo se aloja la info. (El resto
  de tablas ya tenían su columna de tiempo: audit→ts, episodes→created_at,
  gh_resources→fetched_at, secrets, sessions.)

Schema v5 → **v6**. Verificado: roundtrip guardar+leer OK con consulted_at.
NOTA: la MEMORIA a fondo (motor event-sourcing, ventana de 12) NO se tocó —
Brian la revisará a profundidad más adelante. Esto es un avance puntual del MVP.

**🐞 FIX (2026-06-19) — URL web tomada como repo GitHub (falso positivo):** al
mandar "https://tvazteca.com/aztecadeportes/... el partido", el bot NO leía la
página y respondía "no puedo abrir páginas" + arrastraba contexto de otra acción.
Causa RAÍZ: `huele_a_github` daba FALSO POSITIVO — el patrón `owner/repo` del hint
regex matcheaba `tvazteca.com/aztecadeportes` como si fuera un repo → el mensaje se
desviaba al flujo GitHub en vez del flujo web (`url_web`) → no se leía ni se
guardaba en `consulted_web`. Arreglo en `conversation.huele_a_github`: ANTES de
evaluar, `_quitar_urls_no_github()` reemplaza por espacio las URLs que NO son de
github.com (las de github.com se conservan). Así el detector no ve paths de
dominios web. VALIDADO aislado contra 17 casos (0 fallos) + en el código real:
tvazteca/react.dev/luma/ethglobal → web ✅; github.com/owner/repo + "owner/repo"
en texto humano + godinez-studio → GitHub ✅. 2 tests nuevos. Suite: 128 passed.

## 6. Otros cambios menores del periodo (contexto)

- **`tiempo.py`** (NUEVO): hora LOCAL del usuario (no del servidor UTC), deducida
  del language_code de Telegram. `contexto_temporal()` se inyecta al prompt.
- **`md_html.py`** (NUEVO): conversor Markdown→HTML de Telegram (código en `<pre>`).
- **Error handler de red** (`telegram_channel.py`): `on_error`, `_responder_seguro`,
  `_enviar_html` — el server está en red doméstica que parpadea.
- **Borrado lo artesanal:** `github_tool.py` + `pr_review.py` ELIMINADOS (el bot
  corre 100% por MCP). Recuperables vía git. ⚠️ NO declara cerrado el MVP.
- **`test_h4.py`** migrado: se quitaron tests del artesanal; quedan crypto/KEK +
  sandbox.

---

## 7. Cómo verificar que todo sigue sano (checklist post-cambio)

```bash
export SSHPASS='«en secrets/Conectar_Servidor_For3s.md»'
# 1. Tests (lógica pura — rápido, sin red)
sshpass -e ssh brianweb3@100.112.177.53 "cd ~/for3s-os && uv run pytest -q"
#    → debe dar 123 passed, 4 skipped, 0 failed

# 2. Lint del archivo tocado
sshpass -e ssh brianweb3@100.112.177.53 "cd ~/for3s-os && uv run ruff check packages/for3s-core/src/for3s_core/<archivo>.py"

# 3. Import sano
sshpass -e ssh brianweb3@100.112.177.53 "cd ~/for3s-os && uv run python -c 'from for3s_core import <modulo>; print(\"OK\")'"

# 4. Reiniciar y verificar arranque limpio
sshpass -e ssh brianweb3@100.112.177.53 "sudo systemctl restart for3s-telegram && sleep 5 && systemctl is-active for3s-telegram"
sshpass -e ssh brianweb3@100.112.177.53 "sudo journalctl -u for3s-telegram -n 8"
#    → debe verse: "GitHub MCP conectado (read-only)" + "Application started", sin tracebacks
```

**Señales de arranque sano en los logs:**
- `token de Telegram cargado desde SecretStore cifrado`
- `cerebro conectado (modelo=claude-sonnet-4-6 auth=oauth)`
- `GitHub MCP conectado (read-only)`
- `Application started`

**Ruido conocido (NO es error):** tracebacks `cancel scope`/`anyio` al cerrar
scripts de prueba del MCP — es el cierre del AsyncExitStack desde otra tarea,
documentado en `mcp_client.aclose()`. El bot en producción no lo sufre.

---

## 8. Lo que NO se hizo (y por qué) — para no buscar en vano

- **Webhooks GitHub + multi-tenant:** DIFERIDOS. Bloqueadores: (1) sin ingreso de
  red (falta Cloudflare Tunnel, red doméstica inestable); (2) el diseño no define
  qué procesa el webhook; (3) multi-tenant es refactor grande y solo vale con 2º
  cliente. Detalle en `memory/PENDIENTES.md`.
- **Audio multimodal:** descartado por recursos (Whisper ~1-2GB).
- **CI con Apache AGE:** pospuesto a H5 (AGE es para el grafo de H5, aún no existe).