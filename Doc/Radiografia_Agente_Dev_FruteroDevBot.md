# 🩻 RADIOGRAFÍA A DETALLE — `agents/dev` (@fruterodev_bot) — cómo está CONSTRUIDO

> **Fecha:** 2026-07-04 · **Fuente:** `~/entrenamiento/Fruterito-principal/` (read-only, server)
> **Sujeto:** el agente `dev` ("Dev Agent") de OpenClaw — el Fruterito-DESARROLLADOR.
> En Telegram = **@fruterodev_bot** (dato de Brian). También vivía en **Discord** (guilds Frutero).
> **Objetivo:** mapear a profundidad cómo está construido — punto de vista para el HITO ENTRENAMIENTO.
> Hermano de: `Radiografia_Fruterito_Principal.md` (el árbol completo).

---

## 0 · Ficha del agente

| Campo | Valor (verificado en config/sesiones) |
|---|---|
| id / nombre | `dev` / "Dev Agent" |
| Modelo primario | **`anthropic/claude-opus-4-5`** (el ÚNICO agente con Opus; watchdog y godin-slots corrían sonnet-4-5) |
| Workspace | `/home/fruterito/.openclaw/workspace` — **EL MISMO del Fruterito principal** (comparte SOUL/IDENTITY/memoria) |
| Canales | Telegram (@fruterodev_bot, DM con Brian y Jazz) + **Discord** (2 guilds: frutero-club, frutero-hacking-agents) |
| Auth | perfil `anthropic:default` tipo token · errorCount 0 · último uso 2026-04-05 |
| Volumen | **115 archivos · 74.6 MB · 113 archivos de sesión · 17,096 líneas · 77 sesiones en índice** |
| Mensajes | 14,749 (7,337 assistant · 5,518 toolResult · 1,894 user) |
| Tokens | out **2,244,518** · cacheRead **679,114,453** (679M — cachear el system prompt de 50K era vital) |
| Vida | nace 2026-02-07 (1er mensaje de Brian) · pico mar-14→abr-05 (trabajo DIARIO) |
| Host real | ⭐ **AWS** — las rutas internas dicen `/home/fruterito/`: este árbol es la copia del OpenClaw de AWS (coincide con el proyecto `openclaw-aws-persistence` y el SKILLS-INVENTARIO que lista "Ubicación AWS") |

**La revelación central:** `dev` NO era un agente con otra personalidad — era **el MISMO
Fruterito (mismo workspace, misma alma, misma memoria) corriendo con Opus** para trabajo
de desarrollo, con sus propios hilos de sesión y su propio bot de Telegram. Un "modo
desarrollador" implementado como agente separado que comparte cerebro documental.

---

## 1 · Anatomía de archivos (los 115)

```
agents/dev/
├── agent/
│   └── auth-profiles.json          ⛔ SECRETO (perfil token anthropic + stats de uso)
└── sessions/
    ├── sessions.json               ÍNDICE: 2.3 MB, 77 sesiones con 26 campos c/u
    ├── 66 × *.jsonl                sesiones "vivas" al momento de la copia
    ├── 33 × *.jsonl.deleted.*      borradas por /reset pero CONSERVADAS
    ├── 12 × *-topic-<id>.jsonl     hilos (topics) de Discord/Telegram por tema
    ├──  4 × *.jsonl.reset.*        resets con timestamp (incl. LA de 54 MB)
    └──  1 × *.jsonl.bak-*          backup de proceso
```

- La sesión **madre**: `f30a7098….jsonl.reset.2026-04-01` = **54 MB** — el DM de Telegram
  con Brian (sender 1923367928, message_id 8681…): meses de conversación continua hasta
  el reset del 1-abr.
- La sesión **viva al final**: `c27178c0….jsonl` = 9.9 MB (hasta 2026-04-05, el último día).

---

## 2 · CÓMO ESTÁ CONSTRUIDO — la receta completa (esto es lo que vinimos a mapear)

### 2.1 El system prompt se ENSAMBLA en cada corrida (verificado en `systemPromptReport`)

OpenClaw guarda en el índice un reporte de CÓMO armó el prompt. Receta real de dev:

```
system prompt total = 50,228 chars
├── contexto NO-proyecto (16,733 chars): framework OpenClaw (tools, reglas, canal)
└── contexto de PROYECTO (33,495 chars) = 8 ARCHIVOS .md INYECTADOS del workspace:
    · AGENTS.md      7,804 chars   reglas de operación del workspace
    · SOUL.md        3,922 chars   el alma (quién eres)
    · TOOLS.md       1,033 chars   notas de herramientas locales
    · IDENTITY.md    2,258 chars   Fruterito DevRel (nombre, rol, vibe)
    · USER.md          830 chars   quién es Brian
    · HEARTBEAT.md     685 chars   config heartbeat
    · BOOTSTRAP.md   1,449 chars   arranque
    · MEMORY.md     15,176 chars   ⭐ EL MÁS GRANDE: índice de memoria long-term
    + skillsSnapshot: catálogo XML de skills (nombre+descripción)
```

**Las 3 ideas de diseño clave:**
1. **Identidad = archivos .md editables inyectados** (exactamente lo que replicamos en el
   Hito Identidad Viva con capa usuario + persona/).
2. **La memoria entra por DOS vías**: MEMORY.md (índice de 15K chars SIEMPRE en el prompt)
   + tool `memory_search` para buscar bajo demanda + el agente LEE sus diarios
   (`read memory/2026-04-02.md` está en las sesiones). Memoria = archivos, no BD
   (el sqlite estaba VACÍO — nunca usaron el índice semántico).
3. **Skills = catálogo liviano + carga bajo demanda**: el prompt solo lleva
   `<skill><name>…<description>…</skill>`; cuando la tarea matchea, el agente hace `read`
   del SKILL.md completo. Barato en tokens, escalable en número de skills.

### 2.2 Gestión de contexto (por qué aguantaba sesiones de 54 MB)

- `contextPruning: cache-ttl` (ttl 2h, keepLastAssistants 10, softTrimRatio 0.7) — poda
  el contexto viejo respetando el cache de Anthropic. Los **1,860 eventos
  `openclaw.cache-ttl`** en las sesiones son esta poda trabajando.
- `compaction: safeguard` — 30 compactaciones registradas (resume la sesión cuando crece).
- **cacheRead 679M tokens** = la estrategia entera dependía del prompt caching.

### 2.3 El registro de sesión (formato jsonl — importa para nuestro import)

Cada línea = `{type, id, parentId, timestamp ISO, message{role, content[], model, usage}}` —
**árbol enlazado por `parentId`**, no lista plana. Tipos vistos en dev:
`message` 14,749 · `custom` 1,982 (cache-ttl 1,860, model-snapshot 115, prompt-error 7) ·
`session` 113 · `thinking_level_change` 113 · `model_change` 109 · `compaction` 30.
Bloques de contenido: `text`, `toolCall {name, arguments}`, `toolResult`.

### 2.4 Multi-canal y sesiones (cómo UN agente vivía en 3 lados)

- `session.dmScope: per-channel-peer` → **una sesión por persona+canal**: DM Telegram
  Brian = 1 sesión (la de 54MB), DM Jazz = otra, cada canal Discord = otra.
- Discord por HILOS temáticos (12 sesiones `-topic-`): "Hilo para investigar problemas de
  conexión SSE", "solución de errores Godínez.Studio", "desarrollo de Frontend (apps/web)",
  "Planeación de Agent-Camp 2026", "conflicto de memoria entre agentes", "tasas de
  respuesta con tráfico grande", "mejoras modo hackathon"… — **canales del guild = carpetas
  de proyecto**: #vibe-coding-bootcamp, #Godínez.AI Studio [product], #GODÍNEZ STUDIO (SaaS),
  #AgentCamp, #brian-kukulcan-cto, #dudas-kukulcan.
- Índice de sesiones: 4 telegram · 23 discord · 50 sin canal (= corridas de CRON aisladas).

### 2.5 Cron nativo (dev era el agente PROGRAMADO)

- 2 jobs suyos en el índice: `godinez-studio-tickets-monitor` (cada 30 min, payload en
  lenguaje natural, `sessionTarget: isolated`) + `bootcamp-tracker-daily`.
- ~25+ sesiones etiquetadas "Cron: …" = cada corrida es una sesión aislada desechable.
  *(Modelo de referencia ya apuntado en PENDIENTES → CRON CONVERSACIONAL.)*

### 2.6 Sociedad de agentes

- `tools.agentToAgent: enabled, allow: [dev]` → **los demás agentes podían hablarle SOLO a
  dev**: dev era el hub técnico al que watchdog/godin-slots podían delegar.
- `sessions_spawn` usado 5 veces = dev LANZABA SUBAGENTES (maxConcurrent 8 configurado).
- Herramienta `message` usada 64 veces = hablaba PROACTIVAMENTE (avisos a Brian).

### 2.7 Con qué manos trabajaba (las 18 herramientas, conteo real)

| Tool | Usos | Lectura |
|---|---:|---|
| `exec` | **4,272** | 71% de todo — dev vivía en la TERMINAL (git, npm, builds, deploy) |
| `process` | 318 | procesos largos (dev servers) |
| `read` / `write` / `edit` | 316/228/169 | código y docs |
| `web_fetch` / `web_search` | 85/6 | investigar |
| `message` | 64 | avisos proactivos |
| `gateway` | 20 | control del gateway OpenClaw |
| `memory_search` | 15 | buscar en su memoria |
| `browser` | 10 | navegador |
| `cron` | 6 | ⭐ gestionaba SUS PROPIOS jobs programados |
| `sessions_spawn/list/status/history` | 12 | subagentes |
| `pdf` / `agents_list` | 1/1 | — |

**Perfil inequívoco: un DESARROLLADOR** (masivamente exec/write/edit) **con
proactividad** (message/cron) **y delegación** (spawn).

---

## 3 · Qué hizo y cuándo (timeline real, líneas de sesión por día)

```
2026-02-07  263   ← NACE: Brian lo estrena por Telegram ("quiero que sea funciona el…")
   (gap feb-mar: el trabajo estaba en el main de WSL)
2026-03-14  470   ← se muda el trabajo a AWS/dev
2026-03-15  660      03-16  992      03-17  249      03-18  1,155
2026-03-19  119      03-20  332      03-21  159      03-22  1,137
2026-03-23  1,110    03-24  225      03-25  1,713    03-26  1,964  ← PICO
2026-03-27  1,105    03-28   87      03-29  406      03-30   58
2026-03-31  814      04-01  653      04-02  570      04-03  1,695
2026-04-04  1,067    04-05   93     ← FIN de la era OpenClaw
```

Temas dominantes (por hilos + labels): **Godínez Studio / Godínez.AI** (SSE, frontend,
errores de plataforma, onboarding, tickets) · **bootcamps Vibecoding** · **Agent-Camp 2026** ·
**modo hackathon** · **infra de los propios agentes** (conflicto de memoria entre agentes,
tráfico). Interlocutores: Brian (@LPBrayan0) y Jazz (@driade_1).

---

## 4 · ⛔ Secretos de este agente (exclusión)

- `agents/dev/agent/auth-profiles.json` — token Anthropic.
- Dentro de las sesiones puede haber secretos citados en texto (Brian pegando .env,
  tokens en outputs de exec) → **el import de sesiones necesita el detector de secretos
  LÍNEA POR LÍNEA, no solo por archivo** (hallazgo para F3 del Plan Maestro).

---

## 5 · Mapa dev → For3s OS (para el punto de vista que sigue)

| Pieza de dev (OpenClaw) | Equivalente en For3s OS hoy | Estado |
|---|---|---|
| 8 .md inyectados al system prompt | Identidad en capas + ensamblador (`identidad.py`, v0.15.0) | ✅ tenemos (nuestro es blindado + capa usuario) |
| MEMORY.md 15K siempre en prompt + memory_search | `memoria.recordar()` cascada semántica→grafo | ✅ tenemos (más rico: BD+embeddings+grafo vs archivos) |
| skillsSnapshot XML + carga bajo demanda | skills H12 + APRENDE | ✅ similar |
| cache-ttl pruning + compaction | gestor de contexto propio | ✅ equivalente |
| exec masivo (4,272) | EXECUTE_CODE sandbox | ✅ (el nuestro aislado; el suyo tocaba el host) |
| cron dinámico (tool `cron` + jobs.json) | ❌ solo jobs fijos | 🔴 BRECHA (pendiente CRON CONVERSACIONAL) |
| Discord + Telegram + hilos por proyecto | solo Telegram | 🔴 BRECHA (pendiente MULTI-CANAL) |
| agentToAgent hub + sessions_spawn | H8 equipo multi-agente | ✅ (distinto diseño, mismo poder) |
| message proactivo | alertas health + gate | 🟡 parcial (avisos sí; conversación proactiva limitada) |
| Sesión = árbol jsonl con parentId | episodes_events append-only | ✅ (para el IMPORT: mapear árbol→secuencia) |

---

## 6 · Hallazgos que se lleva el HITO ENTRENAMIENTO

1. **dev = Fruterito con Opus y bata de ingeniero**, mismo workspace/alma que main → al
   importar, su conversación pertenece a la MISMA "persona" Fruterito (no crear un
   concepto-agente aparte salvo como rol).
2. El **`systemPromptReport`** nos da la receta exacta de construcción — y valida que
   nuestra Identidad Viva replicó el patrón correcto por su cuenta.
3. Las **sesiones son árboles** (`parentId`), no listas — el importador F3 debe aplanarlas
   respetando el orden temporal.
4. **Secretos DENTRO de las sesiones** (no solo en archivos) → detector línea por línea en F3.
5. Los **labels del índice** (`sessions.json`) dan contexto de canal/persona/hilo por sesión
   → metadatos de origen perfectos para los episodios importados.
6. Las 50 sesiones cron "(sin label)" son ruido repetitivo (monitoreo cada 30 min) → CURAR:
   probablemente se importan resumidas o no se importan (decisión con Brian en F2).

---

*Siguiente paso: lo define Brian ("cuando termines te digo cómo continuamos").*