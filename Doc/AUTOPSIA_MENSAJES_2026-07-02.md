# 🔬 Autopsia FORENSE mensaje por mensaje — sesión de pruebas (2026-07-02)

> Análisis extremo: cada burbuja del screenshot + la timeline REAL de logs (por timestamp) + BD + código.
> Reconstruye qué pasó EXACTAMENTE en cada mensaje. Incluye síntomas que Brian NO reportó (los cazó la
> curiosidad). Al final: inventario COMPLETO de lo hardcodeado.

## Contexto de la sesión (reconstruido de logs)
- Arranque del agent: **01:59:43** UTC (el screenshot marca 08:46 PM = otra zona horaria; es la MISMA sesión).
- Modelo de embeddings cargó OK a 01:59:56 → memoria semántica lista.
- Primer indicio de actividad del usuario: **02:53** (los cache fails empiezan ahí).
- **32 mensajes tuyos / 33 respuestas** del bot en la sesión → el bot SÍ respondió a todo (no se comió mensajes).
- La sesión terminó con un **reinicio duro** que TÚ pediste (03:41:17 "reinicio duro solicitado por el dueño").

---

## 📩 MENSAJE POR MENSAJE

### Burbuja 1 (visible) — respuesta del bot: "Lo que yo puedo confirmar… H1-H12… Lo que no sé: qué cambió Brayan más recientemente… pregúntale a Brayan"
**Qué pasó:** respondiste a "¿qué hay nuevo/qué cambió?". El bot contestó desde el LLM en CHARLA, NO desde
`/version`. Dijo "no tengo changelog automático de cada deploy".
**🐛 BUG (traza #6):** el detector `_es_pregunta_version` NO capturó tu frase → NO se inyectó el bloque de
versión real (que SÍ existe: v0.14.0) → el LLM respondió a ciegas y sonó desactualizado.
**Evidencia:** `version.py` en el contenedor = 0.14.0; pero el bot no lo usó porque la frase no disparó el
detector. Es un bug de DETECCIÓN, no de datos.
**Además:** el bot dijo "**Brayan**" — tu nombre real es **Brian** (con i). El LLM lo escribió mal (alucinó
una variante). Y esto FUE ANTES de que se curara el nombre (se curó cuando escribiste, ver abajo).

### Burbuja 2 (tuya) — "Acuérdate que mi color favorito es el verde y mi LENGUAJE favorito es python"
**Qué pasó:** mensaje normal (no comando).
**✅ Bien:** el bot respondió con el indicador "🔍 Trabajando en eso…" (feedback de progreso — esto SÍ
funciona en mensajes normales, línea 1331 del código).

### Burbuja 3 (bot) — "🔍 Trabajando en eso — puede tardar un momento, ya te traigo el resultado…"
**🐛 SÍNTOMA (traza #8/#11 lentitud):** este mensaje de "espera" aparece porque el turno TARDÓ. ¿Por qué
tardó un simple "acuérdate de X"? → **por el cache roto** (cada operación pierde 1.5s×2 en timeout a
127.0.0.1). En la timeline: cache fails a 02:53:00, 02:53:05, 02:53:08… cada pocos segundos.
**⚠️ Comportamiento cuestionable:** para "acuérdate que me gusta el verde" NO debería activar el modo
"trabajando/traigo resultado" (eso es para búsquedas/tools). Está tratando una afirmación simple como si
fuera a buscar algo. **Bug de UX/enrutamiento:** afirmación de perfil ≠ tarea de búsqueda.

### Burbuja 4 (bot) — "¡Anotado! 🟢🐍 Color favorito: Verde · Lenguaje favorito: Python… si hay que escribir código va en Python…"
**✅ FUNCIONA:** captó y guardó color=verde, lenguaje=Python. Bien.
**Observación:** respuesta larga y decorada (emojis, negritas) para algo simple. Consistente con el rol,
pero verboso.

---

## 🔴 LO QUE LA TIMELINE REVELÓ (síntomas que NO se ven en el screenshot pero pasaron)

### A) CACHE ROTO — 14+ fallos, cada pocos segundos (RAÍZ de la lentitud)
`for3s.cache cache get/set falló: Error 111 connecting to 127.0.0.1:6379` repetido. **Cada turno que toca
una tool cacheable pierde ~3s.** Esta es la causa #1 de "tarda demasiado" (#8, #11).

### B) /equipo TARDÓ 110+ segundos (traza #8 "agente-desarrollador tarda")
Timeline del `/equipo` (03:11:34 → 03:13:25):
- 5 specialists en paralelo: 17s, 17s, 15s, 22s, **41s (doc_writer)** → el equipo terminó en **75.9s**.
- Luego synthesizer: **+35s** → total **~110s** para una respuesta.
**Diagnóstico:** NO es un bug per se (5 agentes reales × 1500 tokens c/u es costoso), PERO 110s sin
feedback claro se siente eterno. doc_writer (41s) es el cuello de botella. **Falta:** progreso más
granular + quizá menos specialists o menos tokens por specialist para tareas simples.

### C) 🐛 create_issue FALLÓ con excepción (traza #10 GitHub write)
`03:15:48 falló la ejecución de la write tool create_issue` → ExceptionGroup / McpError en `mcp_client.py:168`.
**Qué pasó:** intentaste crear un issue (§10 de las pruebas). El MCP write hermano lanzó un error (TaskGroup
sin manejar). **Bug real:** el manejo de errores del MCP write no captura limpio la McpError → el usuario ve
o un error o nada. Causa exacta del McpError: probablemente el repo/permiso o el contenedor write efímero.
**Requiere:** capturar la McpError y dar un mensaje claro ("no pude crear el issue: <razón>").

### D) 🐛 MCP github "aclose desde otra tarea" (cancel scope)
`03:40:19 aclose del MCP github desde otra tarea (no crítico): Attempted to exit cancel scope in a
different task than it was entered in`. **Bug conocido de anyio/MCP:** el cliente MCP se cierra desde una
tarea distinta a la que lo abrió. Marcado "no crítico" pero ensucia y puede dejar conexiones colgadas.

### E) Red Telegram inestable (BadRequest) a 03:05:55
`Red Telegram inestable (BadRequest) — reintenta solo`. Un parpadeo de red; el bot lo absorbió. No es bug
del código, es la red doméstica del server (ya conocido).

### F) Reinicio duro a 03:41 (lo pediste tú)
`reinicio duro solicitado por el dueño — saliendo`. Tras el reinicio, embeddings recargaron (normal). O sea:
probaste `/reiniciar_duro` y **funcionó**.

---

## ✅ LO QUE SÍ FUNCIONÓ (confirmado en BD/logs, aunque parecía que no)

| Elemento | Evidencia | Veredicto |
|---|---|---|
| Guardar color/lenguaje | burbuja 4 | ✅ |
| Cambiar de tema | logs: tema 'backend'(02:56) → 'general'(02:58) → 'backend'(02:59) | ✅ /tema funciona |
| C2 decisiones | logs: #6 registrada, #7 registrada, #7→superada | ✅ /decidi + /decision funcionan |
| Perfil rol | logs: 03:07 "set rol" | ✅ /perfil funciona |
| Equipo multi-agente | logs: 5/5 specialists ok, síntesis, handoff corrida=4 | ✅ funciona (pero lento) |
| Nombre del dueño | BD: nombre='Brian🍓🥭' | ✅ se capturó (era tu nombre de TG con emojis) |
| /reiniciar_duro | logs: reinicio ejecutado | ✅ |

---

## 🐛 BUGS CONFIRMADOS (de tus 11 + los que cacé)

| # | Síntoma (tuyo) | Causa raíz REAL | Tipo |
|---|---|---|---|
| 1 | (implícito) lentitud | 🔴 **cache → 127.0.0.1 hardcodeado** (cache.py:55, conversation.py:43 no lee VALKEY_HOST) | Hardcodeo |
| 8/11 | tarda demasiado | consecuencia de #1 + /equipo 110s real | Perf |
| 10 | comandos sin "escribiendo…" | comandos no llaman _mantener_typing | UX |
| 2 | confunde memoria con analizar repo | orden: decide tool ANTES de aprovechar memoria | Diseño |
| 3 | no busca en toda la memoria | búsqueda acotada al session_id actual (no cross-hilo del dueño) | Diseño |
| 4 | pide URL teniendo memoria | huele_a_web dispara antes de revisar memoria | Diseño |
| 5 | C1 estado_tema no funciona | tabla vacía — RE-PROBAR sin lentitud (código OK y registrado) | Verificar |
| 6 | version no refleja | detector _es_pregunta_version no capta la frase natural | Detección |
| — | create_issue falló | 🐛 McpError sin capturar limpio (nuevo, cazado) | Error handling |
| — | "Brayan" en vez de "Brian" | el LLM alucina el nombre; + nombre no inyectado al rol | Comportamiento |
| — | trata afirmación simple como búsqueda | "acuérdate X" activa modo trabajando | Enrutamiento |
| 7 | nombre no funciona | ✅ SÍ funciona (BD lo tiene) — no es bug | — |

---

# 🔧 INVENTARIO COMPLETO DE HARDCODEOS (petición de Brian)

Barrido de TODO el código. Clasificados por RIESGO:

## 🔴 HARDCODEOS QUE SON BUGS (arreglar)
1. **`cache.py:55`** — `host = "127.0.0.1"` fijo. NO lee `VALKEY_HOST`. **← EL BUG RAÍZ de la sesión.**
   `conversation.py:43` crea `GitHubCache()` sin host → siempre 127.0.0.1 → cache muerto en contenedor.

## 🟡 HARDCODEOS TOLERABLES (tienen default + env, pero conviene revisar)
2. `tasks.py:39` — `VALKEY_HOST = os.environ.get("VALKEY_HOST", "127.0.0.1")` — OK (lee env, default local).
   *Lección:* cache.py debería hacer EXACTAMENTE esto.
3. `execute.py:26` — `FOR3S_SANDBOX_URL` default `http://sandbox:8090` — ✅ lee env, default = hermano. Bien.
4. `web_fetch.py:42` / `health.py:277` — `FOR3S_RENDER_URL` default `http://render:8080/` — ✅ lee env. Bien.

## 🟢 HARDCODEOS DE DISEÑO (constantes de negocio — legítimos, pero centralizables)
5. **Modelos LLM fijos** en varios sitios:
   - `dmn_tasks.py:213` `HYP_MODEL = "claude-opus-4-8"` · `:274` `"claude-sonnet-4-6"`
   - `consolidator.py` sonnet-4-6 · `concurrency.py:117-119` límites por modelo · `llm.py:76-78` precios ·
     `modelos.py:34-35` catálogo.
   *Riesgo:* si cambia un modelo, hay que tocar N archivos. **Recomendación:** centralizar en config/modelos.py.
   ⚠️ Nota: `consolidator.py:11` menciona "sonnet-4-7" en docstring pero usa 4-6 → inconsistencia de doc.
6. **Rutas fijas** (contenedor): `autodeteccion.py:34` `/app/.for3s` · `:37` `/app/mods` ·
   `secret_store.py:17` `~/.for3s/master.key` · `tasks.py:398-400` (3 rutas de owner json) ·
   `telegram_channel.py:764` `/app/.for3s/_guardian_revirtio`. *Legítimo* (son rutas del contenedor), pero
   acopladas a `/app` — si cambia la estructura, se rompen.
7. **Topes/umbrales mágicos** (muchos): `_TIMEOUT=1.5` (cache) · `MAX_HISTORY_TURNS=12` · `_DIST_MAX_RECUERDO=0.55`
   · `_MAX_CHARS_BLOQUE_RECUERDOS=2500` · `MAX_LLAMADAS_POR_CORRIDA=8` · `MAX_TOKENS_POR_CORRIDA=15000` ·
   `PAUSA_ENTRE_CLUSTERS_SEG=3.0` · `MAX_WAIT_SECONDS=60` · horas de cron `HORA_*_UTC`. *Legítimos* como
   constantes, pero algunos afectan comportamiento clave (el 0.55 de relevancia, el 12 de historial) y
   podrían querer ser configurables sin rebuild.

## ⚪ REFERENCIAS A IDs (revisar)
8. `telegram_channel.py:951` — menciona `tg:1923367928` en un COMENTARIO (migración legado 'brian'→id).
   Es doc, no lógica. Pero confirma que hubo un id hardcodeado histórico (ya migrado a BD).

---

## 📊 PRIORIDAD DE ARREGLO (recomendación)
1. **P0 — cache 127.0.0.1** (#1). Cura la lentitud de golpe. 1 archivo.
2. **P1 — typing en comandos** (#10) + **create_issue error handling** (cazado).
3. **P1 — comportamiento de memoria** (#2/#3/#4): recordar primero + cross-hilo del dueño + no pedir URL si
   hay memoria. Es el trabajo de fondo real (requiere diseño).
4. **P2 — detector de versión** (#6) + **"acuérdate X" no debe activar modo búsqueda** (enrutamiento).
5. **P2 — centralizar modelos LLM** (hardcodeo de diseño) + revisar umbrales configurables.
6. **Re-probar** C1/estado_tema con el cache sano antes de asumir que está roto.

*Autopsia 2026-07-02 · timeline de logs (32 msgs/33 respuestas) + BD (decisiones/perfil/nombre OK, tema_estado
vacío) + código (barrido de hardcodeos completo). El bug del cache (hardcodeo 127.0.0.1) es la raíz de la
sensación de "no funciona nada" — era lentitud, no ausencia.*
