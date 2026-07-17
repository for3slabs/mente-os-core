# 🎯 REPORTE MAESTRO DE BUGS — For3s OS (sesión de pruebas 2026-07-02)

> Consolida TODO lo analizado: mensajes del chat + hardcodeos + bugs reportados por Brian + bugs NUEVOS
> cazados corriendo pruebas técnicas en vivo. Es el documento de trabajo para arreglar **punto por punto**.
> Cada bug tiene: síntoma · causa raíz (con archivo:línea) · evidencia · fix propuesto · prioridad.
>
> **Fuentes:** screenshot del chat · timeline de logs (32 msgs / 33 respuestas) · BD en vivo · barrido de
> código · batería de pruebas técnicas re-ejecutada 2026-07-02.

---

## 🧭 RESUMEN EJECUTIVO

**Hallazgo central:** un solo hardcodeo (cache → 127.0.0.1) causa lentitud brutal que hizo parecer que
"no funciona nada". La mayoría de las funciones SÍ existen y funcionan a nivel código — el problema es
(a) lentitud del cache, (b) comportamiento de memoria mal ordenado, (c) parsers/detectores frágiles.

**Conteo:** 🔴 3 críticos · 🟠 5 altos · 🟡 4 medios · ✅ 4 "falsos bugs" (sí funcionan) · 📦 hardcodeos: 1 bug + varios de diseño.

---

## 🔴 CRÍTICOS (P0 — arreglar primero)

### BUG-C1 · Cache apunta a 127.0.0.1 (RAÍZ de toda la lentitud)
- **Síntoma (Brian #8, #11):** "tarda demasiado", "cuando le mando todo el proceso tarda mucho más".
- **Causa raíz:** `cache.py:55` → `def __init__(self, host="127.0.0.1", ...)`. `conversation.py:43` crea
  `GitHubCache()` SIN pasar host → siempre 127.0.0.1. El env `VALKEY_HOST=valkey` existe pero NO se lee.
- **Evidencia:** logs con **14 fallos** `Error 111 connecting to 127.0.0.1:6379`. Cada op pierde 1.5s×2 (timeout).
- **Fix:** que `GitHubCache.__init__` lea `os.environ.get("VALKEY_HOST","127.0.0.1")` y `VALKEY_PORT`
  (como ya hace `tasks.py:39`). 1 archivo, ~2 líneas.

### BUG-C2 · Memoria: va a GitHub ANTES de revisar la memoria (comportamiento)
- **Síntoma (Brian #2, #4):** "confunde memoria con analizar repo, primero ataca otra cosa", "pide URL
  cuando solo tiene que buscar en memoria porque ya hemos conversado del tema".
- **Evidencia dura (prueba en vivo):** `huele_a_github("que me puedes decir de godinez-studio") = True`.
  → cualquier "qué sabes de <algo que suena a repo>" dispara ir a GitHub, aunque esté en memoria.
- **Traza real (chat seq 719-720):** preguntaste por Godinez-Studio → fue a GitHub → **404** → tardó 57s.
  Recién en el siguiente mensaje usó su memoria bien.
- **Causa raíz:** `conversation.py` — `huele_a_github` es demasiado amplio y se evalúa para decidir tools
  ANTES de aprovechar lo que `recordar()` ya trajo. No hay "memoria primero, GitHub solo si no basta".
- **Fix (requiere diseño):** (a) recordar SIEMPRE y pasar ese contexto al LLM; (b) si hay memoria relevante
  del tema, NO disparar GitHub/pedir-URL automáticamente; (c) que el LLM decida usar GitHub solo si la
  memoria no alcanza. Acotar `huele_a_github` a intención explícita ("analiza el repo X", con owner/repo).

### BUG-C3 · Parser de /estado_tema frágil → C1 no guardó desde Telegram
- **Síntoma (Brian #5):** "no funciona nada de los estados, ni estado_tema, nada del C1".
- **Evidencia:** `tema_estado` = **0 filas** (no guardó desde el chat), PERO el store a nivel código
  funciona (prueba en vivo: guardar+leer = OK). El problema es el PARSER del comando.
- **Causa raíz:** `tema_estado.parsear_comando` exige el separador `|` estricto:
  - `"fase: X proximo: Y"` (sin `|`) → parsea MAL: fase = `"X proximo: Y"` (mete todo junto).
  - `"fase pruebas"` (sin `:`) → `{}` vacío → cae en modo CONSULTA, no guarda.
  - Si Brian escribió sin las barras `|`, el comando no guardó o guardó basura.
- **Fix:** parser tolerante — aceptar campos sin `|` (detectar `fase:`, `proximo:`, `bloqueo:` como
  anclas dentro del texto), o mensaje de ayuda claro cuando el formato no calza. + confirmar/echo de lo
  que entendió.

---

## 🟠 ALTOS (P1)

### BUG-A1 · Comandos NO muestran "escribiendo…"
- **Síntoma (Brian #10):** "el comando salud y otros no dicen escribiendo... eso me preocupa".
- **Causa raíz:** `_mantener_typing` solo se usa en el flujo de MENSAJE normal (líneas 1331, 3260). Los
  handlers de comandos (`/salud`, `/datos`, `/diagnostico`, `/estado_tema`…) no lo llaman.
- **Fix:** envolver comandos lentos con `send_chat_action(TYPING)` / `_mantener_typing`.

### BUG-A2 · create_issue (write GitHub) falla con McpError sin capturar
- **Síntoma:** al probar crear un issue (§10), el bot lanzó excepción.
- **Evidencia (logs 03:15:48):** `falló la ejecución de la write tool create_issue` → ExceptionGroup /
  McpError en `mcp_client.py:168` (TaskGroup sin manejar).
- **Fix:** capturar la McpError en `ejecutar_write` y devolver mensaje claro ("no pude crear el issue: <razón>").

### BUG-A3 · Detector de versión no capta frases naturales
- **Síntoma (Brian #6):** "no sirve nada de version, no refleja".
- **Evidencia (prueba en vivo):** `_es_pregunta_version` da **NO** para "que has cambiado" y "que traes de
  nuevo" (SÍ para "que version eres", "que hay nuevo", "novedades"). Brian usó justo las que fallan.
- **Traza (chat seq 713-714 / burbuja 1):** el bot respondió "no tengo changelog de cada deploy" porque
  NO se inyectó la versión real (v0.14.0 SÍ existe en el código).
- **Fix:** añadir frases al detector: "que has cambiado", "que traes", "que mejoró", "que hay de nuevo en ti".

### BUG-A4 · "Acuérdate X" activa modo búsqueda/tarea innecesario
- **Síntoma:** para "acuérdate que me gusta el verde", el bot mostró "🔍 Trabajando en eso, ya te traigo
  el resultado…" (chat burbuja 3). Una afirmación simple NO debería activar modo tool/búsqueda.
- **Fix:** afirmación de perfil/preferencia → responder directo, sin el indicador de "trabajando".

### BUG-A5 · /equipo tarda ~110s sin feedback suficiente
- **Síntoma (Brian #8):** "tarda demasiado la parte de agente-desarrollador".
- **Evidencia (logs 03:11-03:13):** 5 specialists = 75.9s (doc_writer solo 41s) + synthesizer 35s = ~110s.
- **Nota:** no es bug per se (5 agentes reales), pero se siente eterno. **Fix:** progreso más granular +
  considerar menos tokens/specialist para tareas simples, o timeout por specialist.

---

## 🟡 MEDIOS (P2)

### BUG-M1 · Alucina el nombre ("Brayan" en vez de "Brian")
- **Evidencia:** chat burbuja 1 y seq 713 el bot escribió "Brayan". El nombre real (BD) es "Brian🍓🥭".
- **Causa:** (a) el nombre no siempre se inyecta al rol/contexto; (b) el LLM alucina la variante.
- **Fix:** inyectar el nombre real de `personas` al contexto + instruir al rol a usarlo textual.

### BUG-M2 · MCP github "aclose desde otra tarea" (cancel scope)
- **Evidencia (logs 03:40:19):** `aclose del MCP github desde otra tarea (no crítico): Attempted to exit
  cancel scope in a different task`. Bug conocido anyio/MCP. Marcado no crítico pero ensucia.
- **Fix:** cerrar el cliente MCP en la misma tarea que lo abrió (o suprimir limpio).

### BUG-A6 · Notificación de consumo no se actualiza / no alerta proactivamente (CONFIRMADO)
- **Síntoma (Brian #1):** "la notificación de consumo no funciona".
- **Causa raíz:** el pin de cupo SOLO se actualiza en `telegram_channel:3546`, dentro del flujo de un
  mensaje NORMAL al LLM (usa `resp.usage_5h`). → si usas solo comandos, o el dato no llega, el pin queda
  **congelado**. Existe lógica de alerta al 80% (`ALERT_THRESHOLD`, `format_cupo:293`) pero es PASIVA
  (solo aparece si el pin se refresca), NO hay aviso PROACTIVO al cruzar el umbral.
- **Fix:** (a) refrescar el pin también tras comandos/periódicamente; (b) alerta proactiva real al 80%
  (mensaje al dueño, no solo texto en el pin). Sube a 🟠 ALTO.

### BUG-M4 · Memoria cross-hilo (parcial, verificar)
- **Síntoma (Brian #3):** "no busca en toda la memoria, no está bien conectada".
- **Evidencia (prueba en vivo):** buscar "godinez studio" en hilo general = 3 recuerdos, en hilo backend =
  3 recuerdos → SÍ trae en ambos. No está tan roto como parecía, PERO la búsqueda es por session_id →
  temas muy separados no comparten. **Verificar** con más casos reales.

---

## ✅ FALSOS BUGS (Brian pensó que fallaban, pero SÍ funcionan)

| Reportado | Realidad (evidencia) |
|---|---|
| #7 "no funciona el nombre" | ✅ BD = `nombre='Brian🍓🥭'` — se capturó bien |
| #5 "C1 no funciona" (código) | ✅ el store guarda+lee OK — el bug es el PARSER (BUG-C3), no C1 |
| #9 "la mayoría de comandos no funcionan" | ✅ /tema, /decidi, /decision, /perfil, /reiniciar_duro funcionaron (logs). Parecían rotos por LENTITUD (BUG-C1) |
| "el arranque a trabajar" (seq 711) | ✅ respondió bien en 5s |

---

# 📦 INVENTARIO DE HARDCODEOS

## 🔴 Hardcodeo = BUG
- `cache.py:55` `host="127.0.0.1"` fijo, no lee VALKEY_HOST → **BUG-C1** (el crítico).

## 🟢 Hardcodeos de diseño (legítimos, pero centralizar)
- **Modelos LLM en 6 archivos:** `dmn_tasks.py:213` (`claude-opus-4-8`), `:274` (`claude-sonnet-4-6`),
  `consolidator.py`, `concurrency.py:117-119`, `llm.py:76-78`, `modelos.py:34-35`. Si cambia un modelo →
  tocar N sitios. + `consolidator.py:11` docstring dice "sonnet-4-7" pero usa 4-6 (inconsistencia).
- **Rutas del contenedor:** `autodeteccion.py:34` `/app/.for3s`, `:37` `/app/mods`, `secret_store.py:17`
  `~/.for3s/master.key`, `tasks.py:398-400` (3 rutas owner json), `telegram_channel.py:764`.
- **~15 umbrales mágicos:** `_TIMEOUT=1.5`, `MAX_HISTORY_TURNS=12`, `_DIST_MAX_RECUERDO=0.55`,
  `_MAX_CHARS_BLOQUE_RECUERDOS=2500`, `MAX_LLAMADAS_POR_CORRIDA=8`, `MAX_TOKENS_POR_CORRIDA=15000`,
  `PAUSA_ENTRE_CLUSTERS_SEG=3.0`, `MAX_WAIT_SECONDS=60`, horas cron `HORA_*_UTC`. Legítimos pero algunos
  afectan comportamiento clave (0.55 relevancia, 12 historial).

## ✅ Bien hechos (leen env con default = hermano)
- `execute.py:26` FOR3S_SANDBOX_URL · `web_fetch.py:42` / `health.py:277-278` FOR3S_RENDER_URL ·
  `tasks.py:39` VALKEY_HOST. **cache.py debería copiar este patrón.**

---

# 🗺️ PLAN DE ARREGLO (orden recomendado)

| Paso | Bug | Esfuerzo | Impacto | Estado |
|---|---|---|---|---|
| 1 | **BUG-C1** cache 127.0.0.1 | 2 líneas | 🔥 cura la lentitud de TODO | ✅ **HECHO 2026-07-02** |
| 2 | **BUG-A1** typing en comandos | bajo | UX, se ve vivo | ✅ **HECHO** (decorador @con_typing en 7 comandos) |
| 3 | **BUG-C3** parser estado_tema | bajo | C1 usable | ✅ **HECHO** (parser tolerante sin '\|') |
| 4 | **BUG-A3** detector versión | bajo | /version por lenguaje natural | ✅ **HECHO** (+13 frases) |
| 5 | **BUG-A2** create_issue error | medio | write GitHub estable | ✅ **HECHO 2026-07-02** |
| 6 | **BUG-C2** memoria primero | **alto (diseño)** | 🎯 el comportamiento de fondo real | ✅ **HECHO 2026-07-02** |
| 7 | **BUG-A6** notificación consumo | medio | pin + alerta proactiva | ✅ **HECHO 2026-07-02** |
| 8 | **BUG-A4** afirmación activa búsqueda | medio | UX/naturalidad | ✅ **HECHO** |
| 8b | **BUG-M1** alucina "Brayan" | medio | naturalidad | ✅ **HECHO 2026-07-02** |
| 9 | Centralizar modelos + umbrales | medio | mantenibilidad + 🐛 bug oculto | ✅ **HECHO 2026-07-02** |
| 10 | Re-probar TODO con cache sano | — | confirmar qué era lentitud | ⏳ pendiente |

## ✅ FIXES APLICADOS (2026-07-02, lote 1)
- **BUG-C1 cache** — leía 127.0.0.1 hardcodeado, ignoraba VALKEY_HOST. 🔍 hallazgo intrigante: el fallo
  costaba **3.84s** (no 1.5s, redis reintenta) → ~7.7s/tool. Fix: lee VALKEY_HOST/PORT + sin reintentos
  (fallo instantáneo) + connect_timeout 0.5s + quitado retry_on_timeout deprecado. Verificado: host=valkey,
  get/set 0.004s, 0 fallos tras rebuild.
- **BUG-A1 typing** — decorador `@con_typing` (mantiene 'escribiendo…' vivo + cancela al terminar) en los
  7 comandos lentos (salud, datos, diagnostico, dmn, introspeccion, cambios, version).
- **BUG-C3 parser** — `parsear_comando` ahora tolerante: detecta claves con o SIN '\|', fallback a fase.
  Verificado: 'fase: X proximo: Y' (sin barras) → {fase:X, proximo:Y}.
- **BUG-A3 detector versión** — +13 frases ("que has cambiado", "que traes de nuevo", "novedades"…).

## ✅ FIXES APLICADOS (2026-07-02, lote 2 — comportamiento de memoria)
- **BUG-C2 memoria primero** (#2/#4) — 🔍 causa raíz localizada: `TOOL_DIRECTIVE` decía "si necesitas
  datos de un repo LLAMA las tools AHORA" pero NUNCA mencionaba la memoria → el modelo iba a GitHub (404)
  aunque el tema ya estuviera en su memoria. **Probado a fondo:** `recordar("que sabes de godinez-studio")`
  SÍ trae godinez (len 1473) → la memoria tenía el dato, el modelo lo ignoraba. Fix: regla **"MEMORIA
  PRIMERO"** al inicio de la directiva (revisa memoria antes de GitHub; ve a GitHub solo si piden datos
  frescos, dan owner/repo, o la memoria no tiene nada; NUNCA pedir URL de algo que ya está en memoria).
  Flujos probados: memoria trae godinez en ambos hilos ✅, panorama trae grafo ✅, cross-hilo funciona ✅.
- **BUG-A4 afirmación activa búsqueda** — 🔍 `huele_a_codigo("me gusta python")=True` (el regex tenía
  `python|bash|nodejs|javascript` SUELTOS → cualquier mención disparaba modo búsqueda/tarea). Fix: exigir
  verbo de acción ("script en python", "ejecuta este python"). Verificado 7/7: mención suelta NO dispara,
  pedir código SÍ.

## ✅ FIX lote 4 — notificación de consumo (BUG-A6)
El dato de cupo llega GRATIS en los headers de cada respuesta de Anthropic. La "alerta" al 80% existía
pero era SOLO texto en el pin (pasiva) — no enviaba notificación. Fix: **alerta PROACTIVA** — al CRUZAR el
80% envía UN mensaje al chat (anti-spam: una vez por cruce, se re-arma al bajar). Enganchada en
`_update_cupo_pin` (sin costo extra). Simulación verificada (46→85→90→95→50→85: avisa/silencio/re-arma/avisa).

## ✅ FIX lote 6 — centralizar modelos + BUG OCULTO de cost-control
🔍 al centralizar cacé un BUG REAL, no solo estética: `llm.py` (_PRICES) y `concurrency.py` (_DEFAULT_LIMITS)
tenían **opus-4-7** hardcodeado, pero el catálogo y dmn usan **opus-4-8**. → con Opus, `_PRICES.get()`
devolvía **(0.0, 0.0)** = el cost-control veía Opus GRATIS, y los límites caían a default. Fix: `modelos.py`
ahora es FUENTE ÚNICA (PRECIOS + LIMITES + MODELOS_POR_TAREA, todo opus-4-8); llm.py, concurrency.py y
dmn_tasks.py leen de ahí. Verificado: precio opus-4-8 = (5.0, 25.0) [antes 0,0], concurrency ya no tiene
el opus-4-7 viejo. Umbrales sueltos (0.55, 12, etc.) NO se centralizaron (son constantes locales OK; no
afectaban comportamiento como el modelo).

## ✅ FIX lote 5 — alucina "Brayan" (BUG-M1)
🔍 causa raíz reproducida: el nombre 'Brian🍓🥭' está en `personas` pero `perfil_usuario.nombre` está
VACÍO. `perfil.resumen()` solo miraba perfil_usuario → inyectaba "rol: desarrollador" SIN el nombre → el
modelo lo adivinaba ("Brayan"). Fix: `resumen()` lee el nombre de `personas` como FALLBACK. Verificado:
ahora inyecta "nombre: Brian🍓🥭" → el modelo ya no inventa el nombre.

## 🔍 VERIFICACIÓN COLATERAL (2026-07-02) — tools de LECTURA sanas
Tras descubrir que el MCP renombró tools de escritura, verifiqué si también cambiaron las de LECTURA
(riesgo de bug silencioso en el análisis de repos). **Cruce de las 10 tools de lectura que For3s usa
vs las 21 que expone el MCP read-only: TODAS existen** (get_file_contents, list_issues, list_pull_requests,
list_commits, search_*, issue_read, pull_request_read). **Probado E2E:** search_pull_requests devolvió 44
PRs abiertos de cli/cli (conteo real), get_file_contents leyó el README. → La lectura de GitHub está sana;
el renombre del MCP SOLO afectó escritura (ya arreglado). El análisis de repos funcionaba (solo era lento
por el cache). ✅ descartado bug silencioso.

## ✅ FIXES APLICADOS (2026-07-02, lote 3 — write GitHub)
- **BUG-A2 create_issue** — 🔍 causa raíz REPRODUCIDA: `McpError: unknown tool "create_issue"`. El servidor
  MCP de GitHub se actualizó y RENOMBRÓ tools: `create_issue`→`issue_write`(method='create'),
  `create_pull_request_review`→`pull_request_review_write`(method='create'). add_issue_comment y
  create_pull_request NO cambiaron. Fix SEGURO: traducción en UN punto (`_TRADUCIR_WRITE` en
  `mcp_client.ejecutar_write`), sin tocar la whitelist/directiva/seguridad. **Verificado con create real:**
  creó el issue #1 en fruterito101/for3s (y lo cerré). 🔒 la whitelist NO incluye merge/delete → siguen
  bloqueados (verificado: el MCP los expone pero For3s no los permite).

**⚠️ Faltan los bugs que Brian dijo que identificó de más — pendiente que los liste para añadirlos aquí.**

*Reporte maestro 2026-07-02 · pruebas técnicas re-ejecutadas en vivo · consolida chat + logs + BD + código.*
