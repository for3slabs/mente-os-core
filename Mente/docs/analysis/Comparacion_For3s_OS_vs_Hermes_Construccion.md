# ⚔️ FOR3S OS vs HERMES-AGENT — comparación PROFUNDA de CONSTRUCCIÓN

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Comparacion_For3s_OS_vs_Hermes_Construccion.md → docs/analysis/Comparacion_For3s_OS_vs_Hermes_Construccion.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-04 · **Enfoque: QUÉ LE FALTA a For3s OS que Hermes tiene — a nivel construcción.**
> **Método:** mismo que con OpenClaw — ambos lados verificados en CÓDIGO REAL:
> Hermes clonado de `github.com/NousResearch/hermes-agent` (2,823 .py; agent/ 144 · gateway/ 69 ·
> tools/ 110 · plugins/ 177 · 1,943 archivos de test) vs For3s OS vivo en el server (v0.15.0,
> 50 módulos / 19,504 líneas core, 32 migraciones, 30 tablas).
> **Complementa** (no reemplaza) `docs/analysis/Comparacion_For3s_OS_vs_Hermes_2026-07-04.md` (aquella fue de
> CAPACIDADES; esta es de CONSTRUCCIÓN) y `docs/analysis/Comparacion_For3s_OS_vs_OpenClaw_Construccion.md`.
> Ejes: comunicación · BD · mapeo de información · manejo de estado · archivos/memorias · ejecución.

---

## 0 · Las dos filosofías

| | Hermes (Nous Research, MIT) | For3s OS |
|---|---|---|
| Qué es | **plataforma universal de agente**: cualquier modelo, cualquier canal, cualquier backend de cómputo | **agente-producto opinado**: Claude + Telegram + SU servidor, con cerebro profundo |
| Memoria | archivos curados (MEMORY.md/USER.md) + SQLite FTS5 + **8 proveedores enchufables** (honcho, mem0…) | Postgres + pgvector + **grafo AGE** con consolidación y olvido NOCTURNOS propios |
| Modelo | agnóstico (adapters: Anthropic, Bedrock, Gemini, OpenAI/Codex, Azure…; `hermes model` cambia en vivo) | Claude fijo (sonnet-4-6), BYOK pendiente |
| Escala | 1 usuario ↔ N plataformas ↔ N backends de cómputo | N usuarios (roles/puerta/gate) ↔ 1 canal |
| Fortaleza | **amplitud**: 25+ plataformas, ~60 tools, marketplace de skills, voz completa | **profundidad**: grafo semántico, DMN/sueño, metacognición, governor, audit inmutable, auto-modificación |

Hermes es un "sistema operativo de agentes" generalista; For3s es un organismo. Las brechas de
For3s están casi todas en AMPLITUD; las de Hermes (visto desde For3s) en PROFUNDIDAD del cerebro.

---

## 1 · COMUNICACIÓN

### Hermes (verificado en gateway/ + plugins/platforms/)
- **25+ plataformas desde UN solo proceso gateway**: CLI + TUI real (autocomplete, multiline,
  interrupt-and-redirect, streaming de tool output) + nativas (Signal, WhatsApp Cloud,
  iMessage/BlueBubbles, WeChat/weixin, QQ, Yuanbao, webhook/API server, MS Graph) + plugins
  (telegram, discord, slack, whatsapp, matrix, teams, mattermost, irc, line, google_chat,
  email, sms, dingtalk, feishu, wecom, homeassistant, ntfy…). Guía `ADDING_A_PLATFORM.md`:
  la capa canal es un CONTRATO formal (base.py) — agregar canal = implementar una clase.
- **Continuidad cross-plataforma**: la MISMA conversación sigue de Telegram a CLI a Discord
  (sesiones etiquetadas por source en el state store único).
- **Voz COMPLETA**: transcripción de notas de voz (ffmpeg+whisper), **TTS** (text_to_speech,
  neutts), **voice_mode** interactivo.
- **send_message como TOOL** (proactivo, a cualquier plataforma) + delivery de cron a
  cualquier canal + mirror/relay entre canales.
- **Streaming**: stream_dispatch/stream_events/stream_consumer — salida en vivo, incluso de
  tools.
- Media rica: stickers, imágenes ENTRA y SALE, generación de imagen/video como tools.
- i18n: locales/ (el agente habla el idioma configurado).

### For3s OS
- Telegram + consola. Typing sostenido, respuesta completa al final. Entrada multimodal
  (img/PDF/docx/xlsx) SIN audio; salida solo texto. 36 comandos ricos. Multi-USUARIO real
  (roles, puerta /invitar, gate) — esto Hermes NO lo tiene (es 1 humano, N canales).

### 🔴 FALTA (constr. — mapea casi 1:1 a los OC-* ya registrados)
- Multi-canal con **capa de canal como contrato** (= OC-C1, pero Hermes da el patrón de
  diseño: platform base class + registry + un gateway).
- Continuidad cross-canal de la MISMA sesión (nuevo matiz, no estaba en OpenClaw).
- Voz entrada (=OC-C6) **+ voz SALIDA (TTS/voice mode — NUEVO)**.
- send_message proactivo (=OC-C3) · streaming (=OC-C4) · archivos/media out (=OC-C5).
- TUI de consola seria (nuestro modo consola es plano; el de Hermes es un producto).

---

## 2 · BASE DE DATOS / PERSISTENCIA

### Hermes (hermes_state.py)
- **SQLite único** (WAL) para TODAS las sesiones de TODOS los canales: metadata + historial
  completo + config de modelo por sesión + **FTS5** (búsqueda full-text sobre toda la
  historia) + **cadenas de sesión** (`parent_session_id`: cuando comprime, abre sesión hija
  encadenada — nada se pierde, todo es rastreable).
- Credenciales: credential_pool/persistence + OAuth manager para MCPs.
- Estado de todo lo demás EN ARCHIVOS versionables (~/.hermes: cron/jobs.json,
  .curator_state, MEMORY.md…).

### For3s OS
- Postgres+AGE+pgvector, 30 tablas, migraciones versionadas, audit chain SHA-256 inmutable,
  secrets CIFRADOS con KEK offline. Multiusuario con scope de memoria.

### Veredicto: For3s gana en robustez/seguridad. Lo que falta:
- **FTS/búsqueda sobre la PROPIA historia conversacional como tool del agente** (Hermes:
  session_search con 3 modos — discovery/scroll/bookends, costo LLM cero). Nuestro pgvector
  busca RECUERDOS; no hay tool para que el agente "hojee" sus conversaciones pasadas
  (≈OC-M4 ampliado: no solo memoria semántica bajo demanda, también historial crudo).
- **Cadenas de sesión** (parent_session_id) al comprimir/resetear (cruza con OC-E1/E2).

---

## 3 · MAPEO DE INFORMACIÓN (memoria y conocimiento)

### Hermes — el "closed learning loop" (su bandera)
1. **MEMORY.md + USER.md curados POR el agente** (memory_tool): notas del entorno y modelo
   del usuario; snapshot CONGELADO en el system prompt al abrir sesión (preserva el prefix
   cache — escrituras a mitad de sesión van a disco y entran al PRÓXIMO arranque).
2. **Nudges**: el loop de conversación EMPUJA periódicamente al agente a persistir
   conocimiento y a crear skills tras tareas complejas (skill_nudge_interval).
3. **Skills que se AUTO-MEJORAN**: skill creation autónoma post-tarea + **curator** — agente
   de fondo disparado por INACTIVIDAD (no cron) que revisa/consolida/archiva/parcha skills
   (pin/archive/consolidate/patch), con estado propio (.curator_state).
4. **Skills Hub** = marketplace real: fuentes GitHub, lockfile de PROCEDENCIA, cuarentena,
   auditoría AST (skills_ast_audit/skills_guard), estándar abierto agentskills.io; builtin
   (18 categorías) + optional-skills (20 más).
5. **Memoria enchufable**: 8 proveedores (honcho = modelado dialéctico del usuario, mem0,
   supermemory, byterover, hindsight, holographic, openviking, retaindb) tras una interfaz
   MemoryProvider.

### For3s OS
- Cascada automática episodios→embeddings→grafo AGE + CLS nocturno + microglía (olvido) +
  DMN generativo + skills H12 con embedding + perfil declarado+INFERIDO con gate (≈honcho,
  YA lo tenemos — P1 v2). El grafo navegable con FKs **Hermes no lo tiene**.

### 🔴 FALTA
- MEMORY.md/USER.md curados por el agente (=OC-M1/M3; Hermes añade el matiz clave del
  **snapshot congelado por sesión para no romper el prefix cache** — diseño a copiar).
- **Nudges de persistencia y de creación de skills** (NUEVO — el mecanismo que cierra el
  loop de aprendizaje: no esperar la noche; empujar EN el turno).
- **Curator por inactividad** (NUEVO matiz: nuestro DMN es nocturno/idle, pero no MANTIENE
  las skills — no consolida/archiva/parcha las creadas).
- Skills-paquete + hub con procedencia/cuarentena/auditoría (=OC-M5 ampliado con el modelo
  de seguridad concreto).
- Interfaz de memoria ENCHUFABLE (nice-to-have; nuestra memoria es integrada a propósito).

---

## 4 · MANEJO DE ESTADO

### Hermes
- **Context engine ENCHUFABLE** (ABC): decide cuándo/cómo compactar; default =
  ContextCompressor (resumen + split de sesión encadenada); alternativas por plugin (LCM
  con tool lcm_grep). Trajectory compressor aparte (para entrenamiento).
- **todo_tool + kanban** (tablero con watchers) — estado de TRABAJO del agente como tool.
- **clarify tool**: el agente PREGUNTA estructuradamente cuando le falta info (con gateway
  de clarificación).
- **checkpoint_manager** (checkpoints de archivos antes de editar) + write_approval +
  approval flows por tool.
- Cron: jobs.json + scheduler tick 60s + lifecycle_guard + **blueprint_catalog** (recetas) +
  **suggestion_catalog** (¡el agente SUGIERE automatizaciones!) + output por corrida en
  `cron/output/<job>/<ts>.md` + delivery a cualquier plataforma.
- Sesión: reset policy por canal, dynamic system prompt injection (el agente SABE desde
  dónde le hablan), scale_to_zero (hiberna), drain/restart guards, shutdown forensics.

### For3s OS
- Sesión canónica derivada + temas/hilos/handoff + tema_estado C1 + decisiones C2 + governor
  con frenos persistentes + gate de equipo + cupo pin + cron_corridas + /salud E2E.

### 🔴 FALTA
- Cron conversacional completo (=OC-E2 + el pendiente ⭐; Hermes suma: **catálogo de
  sugerencias** — el agente propone automatizaciones — y output persistido por corrida).
- **todo/kanban como TOOL** (NUEVO): nuestro tema_estado es comando del usuario; falta que
  el AGENTE gestione su lista de trabajo como herramienta en el loop.
- **clarify estructurado** (NUEVO): H10 ya detecta baja confianza y pregunta en texto;
  falta como TOOL con opciones estructuradas.
- **Checkpoints de archivos** antes de editar en sandbox (NUEVO, barato).
- Reset policy + trazas de contexto (=OC-E1/E3/E4).
- Scale-to-zero / hibernación (filosofía distinta — nuestro server es fijo; anotar, no urgente).

---

## 5 · CREACIÓN DE ARCHIVOS Y MEMORIAS

### Hermes
- El agente escribe MEMORY.md/USER.md/skills (con nudges que se lo recuerdan) + cada skill
  creada tras tarea compleja + cron outputs .md + checkpoints. Todo bajo ~/.hermes,
  legible y versionable.

### For3s OS
- Memoria automática a BD; EXECUTE_CODE crea proyectos en sandbox; automod edita SU código
  (guardián/revert — Hermes NO se auto-modifica el core); persona/mente-os existe pero el
  agente aún no es su autor.

### 🔴 FALTA — igual que con OpenClaw: el agente como AUTOR de su mente legible (OC-M1/M2/M3
con los matices de Hermes: snapshot congelado + nudges). La convergencia de los DOS
referentes en el mismo punto la vuelve la brecha más validada de todas.

---

## 6 · EJECUCIÓN Y HERRAMIENTAS (eje extra que en Hermes es enorme)

### Hermes (~60 tools registrables por toolsets configurables por agente/canal)
- **execute_code con RPC de tools**: el modelo escribe un script Python que LLAMA A LAS
  TOOLS de Hermes vía Unix socket (stub `hermes_tools.py` autogenerado) → colapsa pipelines
  de N turnos en 1 turno con costo de contexto CERO. ⭐ La idea más potente del repo.
- **6 backends de terminal**: local, Docker, SSH, Singularity, Modal, Daytona (serverless
  que hiberna). El MISMO agente elige dónde ejecutar.
- **Browser real** (Camoufox/CDP, supervisor, diálogos) + **computer_use** + generación de
  imagen/video + x_search (Twitter) + web_tools + MCP client CON OAuth manager.
- **delegate/subagentes**: hijos aislados con toolset RESTRINGIDO por hijo, single y batch
  paralelo; el padre solo ve el resumen.
- Seguridad de tools: tirith_security + threat_patterns + url/path_security + osv_check +
  tool_output_limits + approval flows.

### For3s OS
- Tool-loop: GitHub MCP (read dinámico + 4 write) + execute_code (sandbox hermano aislado,
  pip/npm, workspace persistente) + web_fetch por detección. H8 equipo interno (5
  specialists+synthesizer — razonamiento paralelo que Hermes no tiene como tal).

### 🔴 FALTA
- **⭐ execute_code que llama TOOLS vía RPC** (NUEVO y grande: convertir pipelines
  multi-turno en 1 script — encaja natural con nuestro sandbox por HTTP).
- **Toolsets POR contexto** (NUEVO): restringir qué tools ve el agente según canal/rol/
  subagente (hoy el loop es uno solo).
- Browser/computer-use (NUEVO, grande) · web_search como tool (hoy solo web_fetch reactivo).
- Backend de terminal alternativo local/SSH (ya anotado como EC-EXTRA-1).
- Subagentes con toolset restringido por hijo (H8 existe; falta la restricción fina).

---

## 7 · TABLA MAESTRA — brechas vs Hermes (HG-*) y su mapa a lo ya registrado

| # | Brecha (construcción) | Eje | ¿Ya registrada? |
|---|---|---|---|
| HG-1 | Multi-canal con contrato de canal + gateway único + continuidad cross-canal | com | = **OC-C1** (sumar matiz continuidad) |
| HG-2 | Voz entrada + **SALIDA (TTS/voice mode)** | com | OC-C6 solo entrada → ampliar |
| HG-3 | send_message proactivo · streaming · media out | com | = **OC-C3/C4/C5** |
| HG-4 | TUI de consola seria | com | NUEVA (chica) |
| HG-5 | session_search: hojear la PROPIA historia (FTS) como tool | BD/mapeo | ≈ **OC-M4** ampliado |
| HG-6 | MEMORY/USER curados + snapshot congelado (prefix cache) | mapeo | = **OC-M1/M3** + matiz diseño |
| HG-7 | ⭐ **Nudges** de persistencia/creación de skills en el turno | mapeo | NUEVA (media, mucho valor) |
| HG-8 | ⭐ **Curator**: mantenimiento de skills por inactividad (consolidar/archivar/parchar) | mapeo | NUEVA (media) |
| HG-9 | Skills hub con procedencia/cuarentena/auditoría AST | mapeo | = **OC-M5** + modelo de seguridad |
| HG-10 | Cron conversacional + sugerencias de automatización + output por corrida | estado | = **OC-E2**/pendiente ⭐ + matices |
| HG-11 | todo/kanban como TOOL del agente | estado | NUEVA (chica) |
| HG-12 | clarify estructurado como tool (H10 ya da la señal) | estado | NUEVA (chica) |
| HG-13 | Checkpoints de archivos en sandbox antes de editar | estado | NUEVA (chica) |
| HG-14 | ⭐ execute_code → tools vía RPC (pipelines en 1 turno) | ejecución | NUEVA (grande) |
| HG-15 | Toolsets restringidos por contexto/subagente | ejecución | NUEVA (media) |
| HG-16 | Browser / computer-use / web_search tool / image-gen | ejecución | NUEVA (grande, por partes) |
| HG-17 | Multi-proveedor de modelos / BYOK | modelo | ya en EXTRAS (H·BYOK) |
| HG-18 | i18n del agente | producto | NUEVA (chica) |

**Lo que For3s tiene y Hermes NO** (verificado en su código): grafo de conocimiento real
(AGE) con consolidación CLS y OLVIDO activo · DMN/sueño generativo gobernado ·
metacognición con niveles de confianza · governor de 6 frenos · audit chain inmutable +
KEK/secrets cifrados · **multi-USUARIO** con roles/puerta/gate · equipo interno de
specialists+synthesizer · **auto-modificación de su propio código** con guardián de
arranque · /salud end-to-end con alerta · multi-instancia aislada por cliente. — Hermes es
1-humano-N-canales sin grafo, sin sueño, sin governor y sin tocar su propio core.

**Las 3 brechas donde AMBOS referentes (OpenClaw + Hermes) coinciden** — máxima validación:
1. El agente AUTOR de su memoria legible (diario/MEMORY/USER + nudges).
2. Cron conversacional con sesiones aisladas (+ sugerencias).
3. Multi-canal / proactividad / voz.

---

*Fuentes: repo hermes-agent clonado (HEAD 2026-07-04) · código vivo ~/for3s-os v0.15.0 ·
docs previos: Comparacion_For3s_OS_vs_Hermes_2026-07-04.md (capacidades) ·
Comparacion_For3s_OS_vs_OpenClaw_Construccion.md · PENDIENTES §BRECHAS OPENCLAW (OC-*).*