# ⚔️ FOR3S OS vs OPENCLAW — comparación PROFUNDA de construcción y comportamiento

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Comparacion_For3s_OS_vs_OpenClaw_Construccion.md → docs/analysis/Comparacion_For3s_OS_vs_OpenClaw_Construccion.md (2026-07-30, ADR-029)

## Purpose

⚔️ FOR3S OS vs OPENCLAW — comparación PROFUNDA de construcción y comportamiento


> **Fecha:** 2026-07-04 · **Enfoque pedido por Brian: QUÉ LE FALTA a For3s OS que OpenClaw tiene.**
> **Método:** ambos lados VERIFICADOS, no de memoria — OpenClaw desde su material real
> (`docs/analysis/Radiografia_Fruterito_Principal.md` + `docs/analysis/Radiografia_Agente_Dev_FruteroDevBot.md`: config
> openclaw.json, systemPromptReport, 17K turnos de dev) y For3s OS desde su código vivo en el
> server (`~/for3s-os`, v0.15.0: 50 módulos/19,504 líneas core, 32 migraciones, 30 tablas).
> Ejes pedidos: comunicación · base de datos · mapeo de información · manejo de estado ·
> creación de archivos y memorias.

---

## 0 · Las dos filosofías (para leer todo lo demás)

| | OpenClaw (Fruterito) | For3s OS (Foresito) |
|---|---|---|
| Cerebro | **ARCHIVOS** (.md legibles + .jsonl) | **BASE DE DATOS** (Postgres + AGE + pgvector) |
| Memoria | el agente LA ESCRIBE (diarios, índice, learnings) | el sistema LA DESTILA solo (episodios→embeddings→grafo, de noche) |
| Sesión | crece y se PODA (cache-ttl, compaction) | ventana fija + recuerdos RELEVANTES inyectados por distancia |
| Identidad | 8 .md inyectados tal cual | capas ensambladas con núcleo BLINDADO + capa usuario |
| Seguridad | tokens en texto plano, sin audit | KEK/secrets cifrados, audit chain inmutable, governor |
| Espíritu | **libertad y alcance** (multi-canal, exec al host, todo editable) | **control y profundidad** (aislado, gobernado, memoria más rica) |

Ninguno es "mejor en todo": OpenClaw gana en ALCANCE y ergonomía de canal; For3s gana en
memoria profunda, seguridad y autonomía gobernada. Abajo, eje por eje, con lo que FALTA.

---

## 1 · COMUNICACIÓN

### Cómo lo hace OpenClaw (verificado en config + sesiones)
- **Multi-canal real**: Telegram (multi-CUENTA: default + watchdog, cada una su botToken,
  allowlist, streaming propio) + **Discord** (2 guilds, permisos POR CANAL: `requireMention`,
  users allowlist, `*` wildcard) + gateway web local (puerto 18789, control UI). Plugins
  de canal enable/disable.
- **Bindings** agente↔cuenta: `watchdog ↔ cuenta watchdog`; el resto rutea al default. Un
  solo proceso sirve N bots y N agentes.
- **Hilos NATIVOS del canal**: sesión por topic de Telegram y thread de Discord
  (12 sesiones `-topic-` en dev: "Hilo para SSE", "Hilo frontend apps/web"…). Los canales
  del guild eran carpetas de proyecto.
- **Streaming parcial** (`streaming: "partial"`): el mensaje se va EDITANDO mientras el
  modelo genera — ves la respuesta crecer.
- **Salida multimedia**: mandaba ARCHIVOS (media/outbound: .docx, .md teleprompter).
- **Entrada de voz**: .ogg de voz en inbound (2 notas de voz recibidas).
- **Proactividad como TOOL**: `message` (64 usos en dev) — el AGENTE decide escribirte en
  cualquier momento (resultado de cron, aviso, hallazgo).
- **agent-to-agent**: los agentes se hablaban entre sí (hub dev).

### Cómo lo hace For3s OS (verificado en código)
- 1 canal: Telegram (python-telegram-bot) + consola. 1 bot por instancia (multi-instancia =
  N contenedores con el gestor `for3s`). 36 comandos ricos (/salud /soy /equipo /tema
  /decidi /modificar…) que OpenClaw no tiene como tales.
- Typing sostenido (`_mantener_typing`) pero **respuesta completa al final** (sin streaming).
- Entrada multimodal: imágenes/PDF/Word/Excel ✅ — **audio EXCLUIDO a propósito** (multimodal.py).
- Salida: **solo texto** (no hay send_document/send_photo en telegram_channel.py).
- No lee `message_thread_id`: los topics de grupos Telegram no mapean a nada.
- Proactivo: alertas CABLEADAS (health 04:30 vía API cruda, gate de equipo) — el agente NO
  tiene tool para iniciar conversación.
- H8 equipo: specialists+synthesizer INTERNOS (más potente que agent-to-agent para razonar,
  pero no son agentes direccionables desde fuera).

### 🔴 LO QUE LE FALTA A FOR3S OS (comunicación)
1. **Multi-canal** (Discord primero — era la sala de máquinas de dev; ya está en PENDIENTES).
2. **Hilos nativos del canal**: mapear topics de Telegram (y threads futuros) a temas/sesiones
   (`message_thread_id` → `sesion_de(uid, tema)` — el rail de temas YA existe, falta el cable).
3. **Tool `message` proactiva**: que el agente pueda escribirle al dueño por decisión propia
   (gobernada por governor + allowlist) — hoy solo hay alertas cableadas.
4. **Streaming/edición parcial de respuestas largas** (UX: ver crecer la respuesta).
5. **Salida de archivos**: generar y MANDAR .md/.docx/.pdf al chat (For3s crea archivos en
   el sandbox pero no te los puede entregar).
6. **Entrada de voz** (decisión de diseño pendiente de revertir: transcripción).
7. **Multi-cuenta/bindings**: varios bots (personal/dev/watchdog) sirviendo agentes o modos
   distintos desde una instalación (hoy eso pide multi-instancia completa).

---

## 2 · BASE DE DATOS / PERSISTENCIA

### OpenClaw
- **NO tiene BD**: todo es archivos. Sesiones .jsonl (árbol por parentId), índice
  sessions.json (26 campos/sesión: tokens, modelo, canal, **systemPromptReport** = receta
  del prompt de esa corrida, authProfileOverride, memoryFlushAt), config openclaw.json,
  memoria .md. El sqlite semántico existía y estaba **VACÍO** (nunca lo necesitó).
- Virtud oculta: **el workspace era un repo git** → la memoria tenía HISTORIAL de versiones.
- Vicio confirmado: **secretos en texto plano** (botTokens, .github-token, password.txt).

### For3s OS
- Postgres 16 + AGE (grafo Cypher) + pgvector (BGE-M3): **30 tablas** — episodios
  append-only, embeddings, grafo navegable con FKs, perfil, temas, hilos, equipo, skills,
  governor, DMN, decisiones (C2), tema_estado (C1), cron_corridas, audit chain SHA-256
  inmutable, secrets CIFRADOS (KEK offline). 32 migraciones versionadas.

### Veredicto: aquí For3s es MUY superior. Lo poco que falta:
8. **Reporte de ensamblaje del prompt por turno** (el `systemPromptReport` de OpenClaw es
   auditabilidad fina: QUÉ capas/memorias entraron al prompt y cuántos chars — For3s tiene
   /introspeccion del sistema, pero no "qué llevó ESTE turno"). Barato y muy útil para debug.
9. **Exportabilidad legible de la memoria** (la BD es opaca para el humano; OpenClaw era
   navegable con `cat`). Un `/exportar_memoria` a .md cerraría la brecha de transparencia.

---

## 3 · MAPEO DE INFORMACIÓN (cómo el conocimiento se organiza y llega al prompt)

### OpenClaw — memoria ESCRITA y CURADA por el propio agente
- **MEMORY.md (15,176 chars) SIEMPRE en el system prompt**: un índice de largo plazo que el
  agente mantenía a mano.
- **Diarios por fecha** (`memory/2026-04-02.md`) que el agente escribía Y RELEÍA (visto en
  sesiones: `read memory/2026-04-02.md`); él mismo ARCHIVABA los viejos (`archive/2026-02/`).
- **Memoria temática**: brian-prefs.md, lecciones.md, godinez-studio.md… y POR PROYECTO
  acompañado: `memory/acompanante/<proyecto>/{learnings.md, metrics.json, pending.md}`.
- **memoryFlush**: antes de compactar la sesión, volcaba lo importante a archivos
  (memoryFlushAt en el índice) — nada se perdía al podar.
- **Skills**: catálogo XML liviano en prompt + `read` del SKILL.md bajo demanda; skills =
  paquetes portables (carpeta con scripts/assets) + **clawhub** (buscar/instalar/publicar)
  + skill-creator (crear skills conversando).
- `memory_search` como tool (15 usos) — búsqueda bajo demanda decidida por el agente.

### For3s OS — memoria DESTILADA automáticamente
- Cascada `memoria.recordar()`: identidad canónica → perfil + tema activo + hilos + memoria
  semántica (relevancia por distancia coseno con presupuesto de chars anti-bloat) + grafo
  (conceptos/relaciones cuando toca) + decisiones/estado_tema cuando la pregunta lo pide.
- Consolidación NOCTURNA (CLS): episodios → conceptos del grafo; microglía olvida; DMN
  genera skills/propuestas gobernadas; relevancia se recalcula. **El humano no cura nada.**
- Skills H12: filas en BD con embedding, generadas por autogen + curadas de noche.

### 🔴 LO QUE LE FALTA A FOR3S OS (mapeo)
10. **⭐ Diario/bitácora propia del agente** — que Foresito ESCRIBA su día ("qué aprendí,
    qué quedó pendiente") en un lugar legible (persona/mente-os/Doc/ ya existe como casa
    natural). Es la pieza de OpenClaw con más alma: memoria narrativa navegable. (El
    diario_cambios actual solo registra auto-mods de código.)
11. **Learnings por tema/proyecto**: hoy el conocimiento por tema vive disperso en
    episodios+grafo; falta el "learnings.md del proyecto X" — resumen curado y ACUMULATIVO
    por tema (el rail: temas + tema_estado C1 ya existen).
12. **Índice de memoria curado de largo plazo** (el MEMORY.md): un resumen maestro SIEMPRE
    presente que el propio agente mantenga (For3s inyecta lo RELEVANTE al turno; le falta
    lo PERMANENTE elegido por él).
13. **memory_search como TOOL del loop**: que el AGENTE decida buscar más memoria a mitad
    de razonamiento (hoy la recuperación pasa 1 vez, antes del turno).
14. **Skills como paquetes portables + marketplace**: skills con scripts/assets ejecutables,
    instalables/publicables (clawhub). Las nuestras son conocimiento en BD, no herramientas
    empaquetadas.

---

## 4 · MANEJO DE ESTADO

### OpenClaw
- Sesión AUTOMÁTICA por canal+persona (`dmScope: per-channel-peer`) y por hilo (topics).
- Ciclo de vida explícito: `/new` `/reset` (rotan el jsonl conservándolo), compaction
  `safeguard` (30 vistas), poda `cache-ttl` (1,860 eventos, ttl 2h, keepLast 10, softTrim
  0.7) — **679M tokens de cacheRead**: todo el diseño gira alrededor del prompt caching.
- Eventos de estado DENTRO de la sesión: model_change, thinking_level_change,
  model-snapshot — cambiar modelo/razonamiento EN CALIENTE quedaba registrado en el hilo.
- **Sesiones aisladas desechables** para cron (`sessionTarget: isolated`) — el trabajo
  programado no contamina la conversación.
- authProfileOverride POR SESIÓN (cambiar credencial en un hilo puntual).
- exec-approvals.json: aprobaciones de ejecución persistentes.

### For3s OS
- Sesión canónica DERIVADA (`tg:<uid>[:tema]`, una sola función `sesion_de`) + hilos por
  usuario + handoff entre hilos (AI1-7) + estado operativo por tema (C1 /estado_tema) +
  decisiones con porqué (C2 /decidi) + gate de aprobación de equipo + governor con frenos
  y bloqueos persistentes + cupo Anthropic en vivo (pin 5h/7d) + cron_corridas + /model.
- Contexto: N turnos recientes + memoria selectiva (no hay sesión gigante que podar — el
  diseño evita el problema que OpenClaw resuelve con compaction).

### 🔴 LO QUE LE FALTA A FOR3S OS (estado)
15. **/reset ligero de conversación** (borrón y cuenta nueva del CONTEXTO conversacional
    conservando memoria/perfil — hoy /reiniciar es del servicio, no del hilo).
16. **Sesiones aisladas desechables** para trabajo programado/subagentes (la pieza del
    cron conversacional: cada corrida = mini-sesión que muere; ya apuntado en PENDIENTES).
17. **Registro de cambios de modelo/razonamiento EN el hilo** (hoy /model cambia global y
    no queda trazado en la conversación).
18. **Snapshot de skills/estado por sesión** (qué skills veía el agente en ese momento —
    OpenClaw lo guarda; útil para depurar "por qué respondió así").

*(La poda cache-ttl/compaction NO es brecha: nuestro diseño de ventana+memoria la vuelve
innecesaria — es la diferencia de filosofía, no un faltante.)*

---

## 5 · CREACIÓN DE ARCHIVOS Y MEMORIAS

### OpenClaw — el agente es AUTOR de su mente
- Escribía SUS memorias como archivos: diarios diarios, MEMORY.md, learnings, prefs,
  lecciones; archivaba lo viejo; hacía flush antes de compactar.
- Creaba PROYECTOS enteros en su workspace (repos git: godinez-ai, meetup-q1-puebla…),
  entregaba archivos (outbound), gestionaba su propio cron (tool cron), instalaba skills.
- Todo con `exec` DIRECTO AL HOST (4,272 usos) — poder total, riesgo total (sin sandbox,
  sin audit, secretos en claro).

### For3s OS — el sistema fabrica la memoria; el agente edita su caja
- Memorias: automáticas a BD cada turno + consolidación nocturna (el agente no redacta).
- Archivos: EXECUTE_CODE crea proyectos en el WORKSPACE DEL SANDBOX (aislado, persistente,
  sin tocar host) ✅ · automod edita SU código con guardián/revert ✅ (esto OpenClaw NO lo
  tiene: auto-modificación estructural con red) · capa persona/ + mente-os/ heredable
  existe pero la escribe el USUARIO (+ job_estilo la parte inferida).
- 🔴 El agente NO escribe todavía su propia mente documental (diario, learnings, índice) —
  misma brecha 10-12 vista desde el otro lado: en OpenClaw los ARCHIVOS eran la memoria;
  en For3s los archivos de la persona existen pero el agente aún no es su autor.
- 🔴 No entrega archivos al chat (brecha 5).

---

## 6 · TABLA MAESTRA DE BRECHAS (todo lo que le falta, priorizable por Brian)

| # | Brecha | Eje | Tamaño | Nota |
|---|---|---|---|---|
| G1 | Cron conversacional + sesiones aisladas (15/16) | estado/com | grande | YA en PENDIENTES con modelo de referencia |
| G2 | Multi-canal (Discord 1º) + multi-cuenta (1/7) | comunicación | grande | YA en PENDIENTES |
| G3 | ⭐ Diario + learnings + índice curado escritos POR el agente (10/11/12) | memorias | medio | rails listos: persona/, mente-os/, temas, DMN nocturno puede redactar |
| G4 | Tool `message` proactiva gobernada (3) | comunicación | chico | governor + allowlist ya existen |
| G5 | Hilos nativos Telegram → temas (2) | comunicación | chico | `message_thread_id` → `sesion_de()`, cable corto |
| G6 | Entregar archivos al chat (5) | comunicación | chico | send_document |
| G7 | memory_search como tool del loop (13) | mapeo | chico | memoria.recordar ya es la fachada |
| G8 | Streaming/edición parcial (4) | comunicación | medio | UX |
| G9 | Voz de entrada (6) | comunicación | medio | decisión de diseño a revisar |
| G10 | Skills-paquete + marketplace (14) | mapeo | grande | visión producto (clawhub propio) |
| G11 | systemPromptReport por turno (8) | BD/debug | chico | oro para depurar |
| G12 | /reset ligero de conversación (15) | estado | chico | — |
| G13 | Exportar memoria a .md legible (9) | BD | chico | transparencia + backup humano |
| G14 | Registro model/thinking-change en hilo (17) + skillsSnapshot (18) | estado | chico | trazabilidad |

**Y lo que For3s tiene que OpenClaw NUNCA tuvo** (para no perder el piso): memoria
semántica+grafo real con consolidación y olvido, seguridad seria (KEK, audit inmutable,
sandbox, governor), auto-modificación con guardián, equipo multi-agente interno,
metacognición, salud end-to-end, multi-usuario con roles, CI/CD firmado. La dirección del
hito ENTRENAMIENTO es absorber el ALMA de OpenClaw (G3: el agente autor de su mente) y su
ERGONOMÍA (G1/G2/G4-G6) sin ceder nada de esto.

---

*Fuentes: Radiografia_Fruterito_Principal.md · Radiografia_Agente_Dev_FruteroDevBot.md ·
código vivo `~/for3s-os` v0.15.0 · openclaw.json (5 versiones) · systemPromptReport.
Cruza con: Comparacion_For3s_OS_vs_Hermes_2026-07-04.md · PENDIENTES (cron conversacional,
multi-canal) · Plan Maestro ENTRENAMIENTO (F0).*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `docs/analysis/Comparacion_For3s_OS_vs_OpenClaw_Construccion.md`).
