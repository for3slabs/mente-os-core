# 🛠️ TALLER "Dale un trabajo a tu agente" — Diseño (FASE 1: AGNÓSTICO)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

> **Doc VIVO** — se enriquece incrementalmente (Brian 2026-07-07).
> **Formato:** TALLER PRÁCTICO (hands-on) · ponente = Brian · **30 min total, ~25 min reales**.
> **Reto del taller:** el asistente **monta un BACKEND que su agente CONSUME** (una API con
> herramientas que el agente llama para hacer trabajo real).
> **⭐ FASE 1 = AGNÓSTICO DE AGENTE:** diseñado para que CUALQUIERA lo siga con SU agente comercial
> (OpenClaw, Hermes, Claude, etc.). **For3s OS se deja de lado en esta fase** (se especializa en Fase 2).
> **Base:** PENDIENTES §VALIDACION_WEB3 · `work/Charla_Web3_Plan_Maestro.md`.

---

## 0 · LA IDEA CENTRAL (lo que todos se llevan)

> **"Un agente sin herramientas solo habla. Un agente con un backend HACE.
> Darle un backend = darle un trabajo real. Y es más fácil de lo que crees."**

El asistente sale con: **su agente llamando a un backend propio para hacer algo útil** — y
entendiendo el patrón universal que sirve con CUALQUIER agente (no atado a un producto).

## 1 · EL PATRÓN AGNÓSTICO (por qué funciona con OpenClaw, Hermes, Claude…)

Todos los agentes modernos consumen backend por el MISMO patrón conceptual:

```
   AGENTE (OpenClaw / Hermes / Claude / …)
      │  "necesito hacer X"
      ▼
   HERRAMIENTA (tool / function / MCP)  ← el contrato: nombre + params + qué devuelve
      │  HTTP request
      ▼
   TU BACKEND (una API con endpoints)   ← lo que montamos hoy
      │
      ▼
   TRABAJO REAL (BD, cálculo, servicio, on-chain…)
```

- **OpenClaw:** skills/tools que llaman endpoints.
- **Hermes:** tools vía RPC / MCP.
- **Claude / Claude Code:** tool use + MCP servers.
- **El común denominador:** una API HTTP con endpoints claros = "el trabajo" que el agente puede hacer.

→ El taller enseña **montar esa API** y **conectarla al agente que cada quien traiga.**

## 1-BIS · ARQUITECTURA — ¿qué necesita algo para SER un agente (y poder darle un trabajo)?

> La pregunta teórica del taller. Respuesta agnóstica, sirve para OpenClaw / Hermes / Claude /
> el que sea. Basada en los **4 ejes de agente** (marco de Hermes/Nous, verificado en For3s).

**Un CHATBOT** recibe mensaje → responde → olvida. Reactivo. No puede tener un "trabajo".
**Un AGENTE** cumple 4 ejes → por eso SÍ se le puede dar un trabajo:

| Eje | Qué significa | Qué componente lo da |
|---|---|---|
| 🧠 **PERSISTENTE** | recuerda entre sesiones (contexto, estado, quién eres) | **memoria** (BD / archivos / vector store) |
| 🛠️ **EJECUTA** | actúa en el mundo, no solo habla | **herramientas + un BACKEND que consumir** ← el taller |
| 🔄 **AUTÓNOMO** | decide y actúa por su cuenta (no paso a paso dictado) | **loop de razonamiento** (tool-loop) + disparadores |
| 📈 **SE MEJORA** | aprende de la experiencia | opcional para v1 (skills / feedback) |

**Los COMPONENTES mínimos de un agente que trabaja** (esto es lo que el asistente debe entender):

```
┌─────────────────────────────────────────────────────────┐
│  1. CEREBRO (LLM)        — razona: ¿qué hago?             │
│  2. LOOP / ORQUESTADOR   — percibe→decide→actúa→repite    │
│  3. MEMORIA              — recuerda (sin esto = chatbot)  │
│  4. HERRAMIENTAS (tools) — el CONTRATO: qué puede hacer   │
│  5. BACKEND / API        — el TRABAJO real ← montamos hoy │
│  6. DISPARADOR           — quién lo activa:               │
│       · REACTIVO: un mensaje del usuario                  │
│       · PROACTIVO: un CRON (cada X tiempo, sin que le     │
│         pidas — "revisa esto cada mañana")                │
└─────────────────────────────────────────────────────────┘
```

**¿Qué se necesita entonces?** (respuesta directa a la pregunta de Brian):
- **Agente (LLM + loop):** el que ya trae cada quien (OpenClaw/Hermes/Claude). NO lo montamos.
- **Memoria:** casi todos los agentes comerciales YA la traen. NO la montamos.
- **⭐ Herramientas + Backend/API:** ESTO es lo que le da el "trabajo". **Lo montamos hoy.**
- **Cron (opcional pero potente):** convierte "responde cuando le hablo" en "trabaja solo cada
  mañana". Se menciona en teoría; si hay tiempo, se muestra como bonus.
- **NO se necesita** (mito a derribar): entrenar un modelo, infra gigante, ni saber ML. Un
  agente que trabaja = LLM que ya tienes + una API tuya + declararla como tool. Eso es todo.

## 1-TER · CASO REAL — cómo For3s OS se dio a sí mismo un trabajo (crédito de autoridad)

> Prueba de que el patrón funciona en serio. **NO se vende For3s** (Fase 2) — se usa como
> EJEMPLO REAL de un agente que recorrió este camino de "habla" → "trabaja".

For3s empezó como un bot que solo respondía en Telegram. Se volvió agente-que-trabaja
agregando EXACTAMENTE los componentes de §1-BIS, uno por uno:
- **Memoria** (Postgres+grafo) → dejó de olvidar → puede retomar "¿en qué quedamos?".
- **Herramientas + backend** → GitHub (lee repos, crea issues) + un **sandbox** propio donde
  ejecuta código real. Ese sandbox ES un backend que For3s consume para "hacer el trabajo".
- **Loop de razonamiento** (tool-loop) → decide qué herramienta usar solo.
- **Cron nocturno** → trabaja SIN que Brian esté (backup, consolida memoria, se mejora).

**La lección para el taller:** For3s no es magia — es el mismo patrón §1 aplicado con cuidado.
Cualquiera puede darle un trabajo a su agente montando el paso 5 (backend). *Detalle:
`memory/archive/For3s_Bot_vs_Agente_vs_Hermes.md` (4 ejes verificados) · `docs/analysis/For3s_OS_En_Bloques.md`.*

## 1-QUATER · COMPARATIVA — agente BIEN armado vs MAL armado (qué evitar)

> Sección pedida por Brian. El "durante el taller cuídate de esto". Basado en errores reales
> vistos en el desarrollo de For3s (los bugs que lo hacían "sentirse bot").

| Aspecto | ✅ BIEN armado | ❌ MAL armado |
|---|---|---|
| **La tool (contrato)** | nombre claro + descripción de CUÁNDO usarla + params tipados | nombre vago, sin descripción → el agente no sabe cuándo llamarla |
| **El backend** | 1 endpoint que hace 1 cosa bien, responde rápido y con formato claro | endpoint que hace de todo, lento, devuelve un dump enorme que confunde al LLM |
| **Respuesta al agente** | JSON corto y estructurado (lo justo) | HTML/texto gigante → el agente se pierde y gasta tokens |
| **Errores** | el backend devuelve error claro ("falta el campo X") | el backend truena / timeout → el agente no sabe qué pasó |
| **Estado/idempotencia** | acciones seguras de repetir; el agente puede reintentar | una acción se ejecuta 2 veces por un reintento (¡cobra 2 veces!) |
| **Seguridad** | validación + límites + confirmación para acciones sensibles | el agente puede borrar/pagar sin control → desastre |
| **Velocidad** | respuesta en < 2-3s → la demo fluye | tarda 15s → silencio incómodo, se siente "roto" aunque funcione |
| **Memoria** | el agente recuerda el resultado y lo usa después | sin memoria → repite la misma llamada, no aprende del resultado |

**La regla de oro del taller:** *un agente es tan bueno como las herramientas que le das. Una
tool mal descrita o un backend lento hacen que un buen agente parezca tonto.* (Lección literal
de For3s: muchos "bugs" eran el agente sano sintiéndose roto por herramientas mal armadas.)

## 2 · ESTRUCTURA DEL TALLER (25 min — teórico + técnico)

| Bloque | Min | Qué | Tipo |
|---|---:|---|---|
| **A. Gancho + teoría** | 0-5 | El problema (agente que solo habla) → la idea (backend = trabajo) → el patrón agnóstico §1 | 🧠 teórico |
| **B. El backend en vivo** | 5-13 | Montar una API mínima con 1-2 endpoints útiles (ej. una "tool" que el agente llama). Código real, en vivo | 🔧 técnico |
| **C. Conectar el agente** | 13-20 | Registrar el backend como herramienta en el agente (mostrar cómo se declara la tool en OpenClaw/Hermes/Claude — el mismo concepto, distinta sintaxis) | 🔧 técnico |
| **D. El agente HACE el trabajo** | 20-24 | Prompt al agente → llama el backend → devuelve resultado real. El "wow" | ✨ demo |
| **E. Cierre + siguiente paso** | 24-25 | Qué acaban de lograr + cómo escalarlo (más tools, blockchain, producción) | 🧠 teórico |

**Regla de tiempo:** 25 min es POCO → el backend debe ser **mínimo pero real** (1 endpoint que
funcione > 5 endpoints a medias). Pre-cargar todo lo que se pueda (repo base listo para clonar).

## 3 · EL BACKEND DE EJEMPLO ✅ DECIDIDO (Brian 2026-07-07)

**🔒 LOCKED: "PRECIO DE UN TOKEN" con enfoque ESCALONADO** (lo más básico apegado a blockchain):

> **El agente pregunta un precio → llama TU backend → devuelve el precio en vivo.**
> **Estrategia de 2 niveles (la más pedagógica — nadie se queda atrás):**
> - **NIVEL 1 (bloque B, todos):** `GET /price/{token}` que por dentro consulta una **API
>   (CoinGecko)**. Facilísimo de montar → el agente ya "hace un trabajo" en minutos. El "wow"
>   sale rápido y seguro.
> - **NIVEL 2 (bloque E, avanzados):** mostrar cómo el MISMO endpoint leería el precio
>   **ON-CHAIN de verdad** (oracle de Chainlink o pool de Uniswap) → "esto es web3 real, no
>   una API centralizada". Aguanta la pregunta "¿es blockchain?" con un SÍ honesto.

**Por qué esta decisión (razonado con Brian):**
- ✅ **Básico:** un solo endpoint `GET /price/{token}`, montable en < 8 min (Nivel 1).
- ✅ **Blockchain real:** el Nivel 2 lee la cadena de verdad (oracle/DEX), conecta con el evento
  (tracks DeFi/Micropayments) sin arriesgar el timing de los 25 min.
- ✅ **A prueba de fallos:** SOLO LECTURA — sin wallet con fondos, sin firmar tx, sin gas, sin
  riesgo de que truene en vivo (a diferencia de "cobrar/pagar", descartado por 🔴 alto para 25 min).
- ✅ **Agnóstico:** cualquier agente (OpenClaw/Hermes/Claude) puede consumir `GET /price/{token}`.
- ✅ **Escala natural al cierre:** "hoy leímos precio; el siguiente nivel es ESCRIBIR (pagos,
  contratos) — eso es la parte avanzada" → deja a la gente con ganas de más.

**Descartados y por qué:** mini-CRUD/consulta simple (no tocan blockchain) · micropago
(escritura on-chain = wallet+gas+fondos = se cae en vivo, no cabe en 25 min).

## 4 · STACK ✅ DECIDIDO (Brian 2026-07-07)

- **🔒 Stack:** **Python + FastAPI** (`GET /price/{token}` son ~15 líneas, es el más leído).
- **🔒 IDEA CENTRAL — el "wow" máximo:** NO monta Brian el backend. **Se le PIDE AL AGENTE EN VIVO
  que arme TODO** (crea el archivo, instala FastAPI, escribe el endpoint, levanta el server, lo
  prueba). Eso ES "dale un trabajo a tu agente" en su máxima expresión: el agente construye el
  backend que él mismo va a consumir.
- **🔒 Paracaídas:** un **repo PRE-HECHO** (backend ya funcionando) listo para clonar/correr, SOLO
  por si el agente falla en vivo. Se prueba idéntico antes. → entregable §5.

### 4.1 · ⭐ EL AGENTE que arma en vivo — orden de probabilidad (Brian 2026-07-07)

Brian NO controla qué agente le tocará (los organizadores conectan los 4 talleres). Los 3
posibles, en orden de probabilidad:

1. **🥇 Pi Coding Agent** (https://pi.dev) — **el MÁS probable.** Los 4 talleres se conectan y
   uno es "Lanza tu propio agente (Pi Coding Agent)" → el público ya tendrá Pi instalado, y este
   taller sería el "dale un trabajo" a ESE Pi. Es un agente CLI (npm `@earendil-works/pi-coding-agent`)
   que escribe archivos + corre comandos + cambia de modelo (`/model`) + `pi -p "tarea"`. Muy
   parecido a Claude Code. **Ejecuta de verdad → ideal para armar en vivo.**
2. **🥈 Claude Code** — respaldo sólido. También escribe archivos, corre comandos, levanta servers.
   Máximo control, el guion se prueba idéntico.
3. **🥉 For3s OS / Foresito** — "por si acaso" (Brian lo dijo). Ejecuta en su sandbox. Sería
   tocar Fase 2, pero disponible como plan C.

**→ El guion debe funcionar con LOS 3.** Como los 3 son agentes-que-ejecutan (CLI/sandbox), los
PROMPTS son casi idénticos — cambia el "cómo se invoca", no el "qué se le pide". El guion §9 se
escribe agnóstico y con las 3 variantes de arranque.

### 4.2 · Contexto: los 4 talleres se CONECTAN (dato de Mel)

Los 4 talleres del track son un hilo: **Fundamentos de IA → Lanza tu propio agente (Pi) → ⭐ Dale
un trabajo a tu agente (ESTE) → Haz que tu agente cobre por su trabajo.** Implicación para el guion:
- El público **YA trae un agente corriendo** (del taller 2, probablemente Pi). No se instala aquí.
- Este taller = darle el PRIMER trabajo real (leer precio on-chain).
- El cierre (§E) enlaza con el taller 4 ("cobrar"): "hoy tu agente CONSULTA; el siguiente taller
  le enseña a COBRAR por hacerlo". Continuidad perfecta.

## 9 · ⭐ GUION DE PRECISIÓN — los prompts EXACTOS (a prueba de fallos)

> Lo que Brian escribe/dice, minuto a minuto. Cada prompt PROBADO idéntico antes del evento.
> Regla: **prompts CERRADOS y específicos** (no "hazme un backend" → el agente divaga; sí "crea
> este archivo con este endpoint" → resultado predecible). Agnóstico: funciona con Pi/Claude/For3s.

### PRE-EVENTO (lo que Brian deja listo — nadie lo ve)
- [ ] Agente instalado y logueado (Pi o el que toque), modelo fijo probado.
- [ ] Carpeta vacía `taller-precio/` lista (cwd del agente).
- [ ] Conexión a internet del venue verificada (CoinGecko + RPC on-chain responden).
- [ ] **Repo pre-hecho clonado en otra carpeta** (`taller-precio-backup/`) por si falla en vivo.
- [ ] `python3` + `pip` disponibles. Puerto 8000 libre.
- [ ] Los prompts de abajo copiados en un archivo aparte (para pegar sin errores de tipeo).

### BLOQUE B (5-13 min) — el agente ARMA el backend en vivo

**Prompt 1 — crear el backend (el central):**
```
Crea un archivo main.py con una API FastAPI que tenga un endpoint
GET /price/{token} que reciba el símbolo de un token (ej. bitcoin, ethereum)
y devuelva su precio actual en USD consultando la API pública de CoinGecko
(https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd).
Devuelve JSON: {"token": ..., "price_usd": ...}. Maneja el error si el token
no existe devolviendo {"error": "token no encontrado"}. Nada más, código mínimo.
```
*Esperado:* el agente crea `main.py` (~15-20 líneas). **Verificación en vivo:** abrir el archivo.

**Prompt 2 — instalar y levantar:**
```
Instala fastapi y uvicorn con pip, y levanta el server en el puerto 8000.
```
*Esperado:* `pip install fastapi uvicorn` + `uvicorn main:app --port 8000`. **Verif:** "running on 8000".

**Prompt 3 — probar el backend (el 1er "wow" pequeño):**
```
Haz una petición a http://localhost:8000/price/bitcoin y muéstrame la respuesta.
```
*Esperado:* `curl` → `{"token":"bitcoin","price_usd":XXXXX}`. **El backend YA funciona.**

### BLOQUE C (13-20 min) — CONECTAR el backend como herramienta del agente

**Prompt 4 — declarar la tool (adaptar a Pi/Claude/For3s):**
```
Ahora quiero que TÚ, como agente, puedas usar este backend como una herramienta.
Crea una skill/tool llamada "consultar_precio" que llame a
GET http://localhost:8000/price/{token} y me devuelva el precio. Regístrala para
que puedas usarla cuando yo te pregunte por un precio.
```
*Esperado:* el agente crea la definición de tool en su formato (Pi: skill/extension · Claude:
MCP/tool · For3s: skill). **Mostrar en pantalla el "contrato" de la tool** (nombre + qué hace).
*Nota:* aquí se ve el §1-QUATER en acción (tool bien descrita = el agente sabe cuándo usarla).

### BLOQUE D (20-24 min) — el agente HACE EL TRABAJO (el "wow" grande)

**Prompt 5 — el momento estelar (lenguaje NATURAL, no técnico):**
```
¿Cuánto vale ethereum ahora mismo?
```
*Esperado:* el agente **decide solo** usar `consultar_precio` → llama al backend → responde
"Ethereum vale $X USD ahora". **Ese es el clímax:** un prompt en lenguaje natural, el agente
eligió la herramienta y la usó. Le dimos un trabajo y lo hizo.

**Prompt 5-bis (redundancia por si el 5 falla):**
```
Usa tu herramienta consultar_precio para decirme el precio de bitcoin.
```
*(Más explícito — fuerza la tool si el agente no la eligió solo.)*

### BLOQUE E (24-25 min) — cierre + Nivel 2 on-chain + enlace al taller 4

**Prompt 6 (si hay tiempo — el gancho web3 REAL):**
```
Modifica el backend para que el precio lo lea ON-CHAIN desde un oracle de
Chainlink (o el pool de Uniswap) en vez de la API de CoinGecko. Muéstrame el cambio.
```
*Esperado:* el agente muestra cómo se leería on-chain (web3.py + dirección del oracle). **No
hace falta que corra** — con MOSTRAR el código basta para el mensaje "esto es blockchain real".
**Cierre hablado:** "hoy tu agente CONSULTA un precio; en el siguiente taller aprende a COBRAR
por hacerlo" (enlace al taller 4).

### 9.1 · REGLAS DE ORO DEL GUION (para que NO falle en vivo)
1. **Todo prompt se pega, no se teclea** (evita typos en vivo). Copiados en un archivo aparte.
2. **Cada prompt probado idéntico** en el ensayo, con el MISMO agente/modelo del evento.
3. **Prompts cerrados y específicos** (dan el endpoint exacto, la URL exacta) → resultado predecible.
4. **Redundancia** en los pasos críticos (5/5-bis) por si el agente improvisa distinto.
5. **Paracaídas visible:** si el agente falla en el prompt N, `cd taller-precio-backup && uvicorn
   main:app` levanta el backend ya hecho → se sigue desde el prompt de conectar la tool.
6. **Cupo:** si se usa For3s, apagar los otros 4 agentes del server (1 cupo compartido).
7. **Tiempos:** si va lento, saltar el prompt 6 (Nivel 2) — es el único opcional.

## 5 · MATERIALES A PRODUCIR (entregables)

- [ ] **⭐ Repo PRE-HECHO** del backend `main.py` FastAPI `/price/{token}` (paracaídas — clonar y
      correr en < 1 min). El más importante: es el seguro de vida de la demo en vivo.
- [ ] **Prompts en archivo aparte** (§9) para pegar sin typos — los 6 + redundancias.
- [ ] **Slides teóricas** (bloques A y E): §1-BIS arquitectura + §1-QUATER comparativa + el "por qué".
- [ ] **Guion del ponente** minuto a minuto (§9 ya lo tiene — cronometrar en ensayo).
- [ ] **Variantes de arranque por agente** (Pi / Claude / For3s): cómo se invoca cada uno (el
      "qué se le pide" es igual — §9). Especialmente **Pi** (el más probable, https://pi.dev).
- [ ] **Handout** de 1 página (el patrón §1 + los 6 prompts + el repo) para que se lo lleven.
- [ ] **Ensayo completo** con el agente/modelo real, cronometrado, ≥2 veces.

## 6 · DECISIONES (Brian)

1. ✅ **Backend de ejemplo (§3):** "precio de token" escalonado (API → on-chain). LOCKED 2026-07-07.
3. ✅ **Web3 (§3):** SÍ, en el Nivel 2 (on-chain real al cierre). LOCKED.
2. ⏳ **¿Qué stack + método de arranque?** (§4) — FastAPI/Node/serverless + cómo lo corren los
   asistentes (local / deploy 1-click / repo pre-hecho). **← SIGUIENTE decisión.**
4. ⏳ **¿Público:** qué tanto saben de código los asistentes? (define profundidad técnica).

## 7 · 🔮 FASE 2 (después — NO ahora): especialización a For3s OS

Una vez el taller agnóstico esté sólido, se hace la versión For3s OS: en vez de "monta una API
genérica", mostrar cómo For3s ya trae ejecución de código + MCP + memoria, y cómo se le da un
backend a Foresito. Pero **eso es Fase 2** — hoy diseñamos para que todos entiendan con su agente.

## 8 · 📓 BITÁCORA
**2026-07-07 — reencuadre.** Brian cambió el enfoque: de "demo de For3s" a "TALLER práctico
agnóstico de montar un backend que el agente consume". For3s de lado en Fase 1. Ángulo elegido:
backend que el agente CONSUME (API/tools). Diseño inicial de 5 bloques en 25 min. Faltan las 4
decisiones de §6.

**2026-07-07 (b) — teoría agregada (pedido de Brian).** 4 secciones nuevas:
- §1-BIS ARQUITECTURA: qué necesita algo para SER agente (4 ejes) + los 6 componentes mínimos
  (cerebro/loop/memoria/tools/backend/disparador) + respuesta directa "qué se necesita: agente,
  API, cron, etc." (basado en el marco de Hermes verificado en For3s).
- §1-TER CASO REAL: cómo For3s se dio a sí mismo un trabajo (ejemplo de autoridad, NO venta).
- §1-QUATER COMPARATIVA bien vs mal armado (8 aspectos, con la lección real de los bugs de For3s).
- Fuentes: `For3s_Bot_vs_Agente_vs_Hermes.md` (4 ejes) · `docs/analysis/For3s_OS_En_Bloques.md`.

**2026-07-07 (c) — stack + guion de precisión.** Decisiones LOCKED: Python+FastAPI · IDEA CENTRAL
= pedirle AL AGENTE EN VIVO que arme todo (no lo monta Brian) · repo pre-hecho solo como
paracaídas. Contexto NUEVO (screenshot de Mel): los 4 talleres se CONECTAN → el público ya trae
un agente (probablemente Pi Coding Agent, https://pi.dev) → este taller le da el 1er trabajo →
enlaza con el taller 4 ("cobrar"). Agente en vivo, orden de probabilidad: 🥇 Pi · 🥈 Claude Code ·
🥉 For3s. **§9 GUION DE PRECISIÓN escrito:** 6 prompts exactos (crear backend → instalar/levantar →
probar → conectar tool → "¿cuánto vale ethereum?" = clímax → Nivel 2 on-chain) + redundancias +
7 reglas de oro anti-fallo (pegar no teclear, probar idéntico, paracaídas visible, cupo, tiempos).
Faltan: producir el repo pre-hecho + ensayar + confirmar fecha exacta + qué agente confirma Mel.

---
*Cruza con: `work/Charla_Web3_Plan_Maestro.md` (el contenedor) · PENDIENTES §VALIDACION_WEB3.*
