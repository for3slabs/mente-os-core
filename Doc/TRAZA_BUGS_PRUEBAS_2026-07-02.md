# 🔬 Trazabilidad de BUGS — pruebas en Telegram (2026-07-02)

> Análisis mensaje por mensaje del screenshot + logs + BD + código. Cada síntoma trazado a su
> CAUSA RAÍZ. Hallazgo mayor: **un solo bug (cache mal apuntado) degrada casi TODO** — hace al bot
> lentísimo, y esa lentitud hizo parecer que muchas cosas "no funcionan" cuando sí existen.

---

## 🔴 BUG RAÍZ #1 — CACHE apunta a 127.0.0.1 en vez del hermano `valkey` (CRÍTICO)

**Evidencia:**
- Logs: `cache get/set falló: Error 111 connecting to 127.0.0.1:6379` — **14 veces** en la sesión.
- `cache.py:55`: `def __init__(self, host: str = "127.0.0.1", ...)` — host HARDCODEADO.
- `conversation.py:43`: `_gh_cache = GitHubCache()` — lo crea SIN pasar host → usa 127.0.0.1.
- El env `VALKEY_HOST=valkey` EXISTE y `valkey:6379` ES alcanzable — pero el código de conversación NO lo lee (solo `tasks.py` sí lo lee).
- Timeout del cache = 1.5s por intento (get + set) → **cada operación cacheable pierde ~3s** fallando.

**Qué explica (síntomas del usuario):**
- **#8 "tarda demasiado el agente-desarrollador"** — cada llamada a tool cacheable espera 1.5s×2 al vacío.
- **#11 "cuando le mando todo el proceso tarda mucho más"** — más tools = más timeouts de cache acumulados.
- **#10 "los comandos no dicen escribiendo..."** — parcialmente: el bot está ocupado en timeouts.
- Sensación general de "no funciona nada" → en realidad funciona pero LENTÍSIMO.

**FIX:** `GitHubCache.__init__` debe leer `VALKEY_HOST`/`VALKEY_PORT` del env (default 127.0.0.1 para
CLI local, `valkey` en contenedor). Igual que `tasks.py:39`. 1 línea + pasar al constructor.

---

## 🟠 BUG #2 — Comandos NO muestran "escribiendo…" (#10)

**Evidencia:** `_mantener_typing` solo se usa en el flujo de MENSAJE normal (telegram_channel `1331`, `3260`).
Los handlers de COMANDOS (`/salud`, `/version`, `/datos`, `/estado_tema`…) NO lo llaman → el usuario no ve
feedback y cree que "no hace nada", sobre todo si tarda (por #1).

**FIX:** envolver los comandos lentos (/salud, /datos, /diagnostico, análisis) con `send_chat_action(TYPING)`
o el helper `_mantener_typing`. Los instantáneos (/version, /cupo) no lo necesitan pero no estorba.

---

## 🟡 #5 — "No funciona nada de C1 / estado_tema"

**Traza:** el código SÍ existe y está registrado (`telegram_channel:3935 CommandHandler("estado_tema")`,
handler en `2444`, en el menú `87`). PERO la tabla `tema_estado` está **VACÍA (0 filas)** → el comando no
llegó a guardar.

**Hipótesis (a verificar en vivo):** o (a) el comando respondió tan lento que pareció no funcionar y no se
completó, o (b) hay un error silencioso en el handler (fail-safe se traga la excepción → "no pude guardar"),
o (c) el usuario no llegó a probarlo por la lentitud. **Las decisiones (C2) SÍ se guardaron (#6, #7 en BD)**
→ el mecanismo de comandos funciona; falta ver por qué C1 específicamente no dejó fila.

**Acción:** probar `/estado_tema fase: X` en vivo con el cache arreglado y ver el log de `for3s.tema_estado`.

---

## 🟢 #6 — "No sirve version, no refleja" — CÓDIGO OK, revisar detección

**Traza:** `version.py` en el contenedor dice **0.14.0 PRODUCTO DISTRIBUIBLE**, CHANGELOG[0] correcto.
El comando `/version` debería funcionar. En el screenshot, Foresito responde a "¿qué cambió?" con "no tengo
changelog automático de cada deploy" — eso es una respuesta del LLM en CHARLA, NO el comando `/version`.

**Dos cosas distintas:**
- `/version` (comando) → datos reales, debería funcionar. **Probar en vivo.**
- Pregunta natural "¿qué cambió?" → el detector `_es_pregunta_version` quizá no captó esa frase → el LLM
  respondió sin el contexto de versión inyectado → contestó vagamente. **Revisar las frases del detector.**

---

## 🟢 #7 — "No funciona el nombre" — SÍ FUNCIONÓ

**Traza:** la BD dice `personas.nombre = 'Brian🍓🥭'` para el dueño. **El fix del nombre SÍ capturó tu
nombre de Telegram.** Si el bot no lo usó en una respuesta, es otra cosa (el LLM no siempre saluda por
nombre aunque lo tenga). **No es un bug de captura** — el dato está. Verificar si lo USA al responder
"¿cómo me llamo?".

---

## 🔴 #2, #3, #4 — MEMORIA: confunde memoria con analizar repo / pide URL / no busca en toda la memoria

**Este es el segundo problema de fondo (comportamiento).** Trazas:
- **#2 "confunde memoria con analizar repo, primero ataca otra cosa"** — cuando dices "¿qué me puedes decir
  de X?", el bot decide entre: buscar en su MEMORIA (recordar) vs ir a GitHub/web. El orden de decisión hace
  que a veces vaya a analizar/pedir en vez de recordar PRIMERO lo que ya hablaron.
- **#4 "pide URL cuando solo tiene que buscar en memoria"** — si detecta que "suena a web/repo" antes de
  revisar memoria, pide la URL en vez de recuperar la conversación previa.
- **#3 "no busca en toda la memoria, no está bien conectada"** — la búsqueda semántica está acotada por
  sesión/scope; si el tema se habló en OTRO hilo, no lo trae. La cascada M1-M4 prioriza el hilo actual.

**Causa raíz probable:** el orden en `conversation.send` — la memoria (`recordar`) se ensambla, pero la
DECISIÓN de usar tools (huele_a_github / pedir URL) puede dispararse ANTES de aprovechar lo recordado, y la
búsqueda semántica está limitada al `session_id` actual (aislamiento correcto para privacidad, pero
demasiado estrecho para "¿qué hemos hablado de X?" cross-hilo del mismo dueño).

**Requiere diseño** (no es 1 línea): (a) recordar SIEMPRE primero y que el LLM vea ese contexto antes de
decidir pedir URL; (b) para el dueño, permitir búsqueda semántica cross-hilo (sus propios hilos) en preguntas
de memoria; (c) que "¿qué sabes de X?" NO dispare pedir-URL si hay memoria relevante.

---

## ⚪ #1 usuario — "La notificación de consumo no funciona"

El mensaje fijado muestra `cupo 5h: 46% · 7d: 18%`. **Verificar:** ¿qué esperabas que notificara? ¿una
alerta al llegar a X%? Hoy `/cupo` muestra el dato pero quizá no hay ALERTA automática de consumo alto.
**Aclarar con Brian** qué debía pasar (mostrar vs alertar).

---

## 📊 RESUMEN — prioridad de arreglo

| # | Síntoma | Causa raíz | Estado real | Prioridad |
|---|---|---|---|---|
| 1 | Cache 127.0.0.1 | host hardcodeado, no lee VALKEY_HOST | 🔴 BUG confirmado | **P0 (raíz de la lentitud)** |
| 8/11 | Lentitud brutal | consecuencia de #1 | 🔴 se cura con #1 | **P0** |
| 10 | No dice "escribiendo…" en comandos | comandos sin typing | 🟠 BUG confirmado | P1 |
| 2/3/4 | Memoria vs repo / pide URL / no cross-hilo | orden de decisión + scope estrecho | 🔴 comportamiento, requiere diseño | **P1** |
| 5 | C1 estado_tema | código OK, tabla vacía | 🟡 verificar en vivo (¿lentitud?) | P1 |
| 6 | version no refleja | comando OK; detector de frase natural débil | 🟢 verificar + afinar detector | P2 |
| 7 | nombre | **SÍ funciona** (BD=Brian🍓🥭) | ✅ no es bug | — |
| consumo | notificación | aclarar qué se espera | ⚪ pendiente aclarar | P2 |

**Conclusión:** el bug del cache (#1) es la BOMBA — arreglarlo primero debería resolver la sensación de
"no funciona nada" (era lentitud, no ausencia). Luego el comportamiento de memoria (#2/3/4) es el trabajo
de fondo real. C1/version hay que RE-probar con el cache sano antes de asumir que están rotos.

*Trazado 2026-07-02 desde screenshot + logs (14 fallos de cache) + BD (decisiones OK, tema_estado vacío,
nombre OK) + código (cache.py:55, conversation.py:43).*
