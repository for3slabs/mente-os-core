# Análisis profundo: internOS vs For3s OS (2026-06-23)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

## Purpose

Análisis profundo: internOS vs For3s OS (2026-06-23)


> Auditoría exhaustiva archivo-por-archivo de `intern-os` (Frutero, v0.4.1) para
> identificar qué tiene resuelto que For3s OS aún no, y qué traer. Repo clonado en
> WSL2: `~/Frutero-Empresa/Frutero/intern-os/`. 62 archivos leídos completos.
> NO es directiva de copiar — es aprender. Solicitado por Brian.

---

## 0. Qué ES intern-os (el hallazgo marco)

internOS **NO es una app** como For3s OS. Es un **SKILL** (framework de documentación +
9 scripts bash POSIX + plantillas) que se instala en CUALQUIER agente (Hermes, OpenClaw,
Claude Code) y le enseña a coordinar trabajo SIN perder contexto entre sesiones.

- **0 infraestructura:** solo filesystem + git. No BD, no servidor, no contenedores.
- **Los archivos SON el estado** (no la BD, no el transcript, no la memoria del agente).
- **Agnóstico de framework:** adapters para Hermes/OpenClaw/Claude Code/genérico.
- Licencia AGPLv3 + comercial. Es producto distribuible REAL (lo que For3s quiere ser).

**Contraste clave:** For3s OS resuelve la memoria/coordinación con PostgreSQL+pgvector+AGE+
embeddings (potente, pero atado a un servidor). internOS lo resuelve con archivos markdown
estructurados + doctrina (simple, portable, sin infra). Filosofías opuestas, ambas válidas.

---

## 1. La arquitectura de 3 capas (su columna vertebral)

| Capa | Qué hace | Equivalente en For3s |
|------|----------|----------------------|
| **Storage** | archivos del workstream = estado autoritativo | episodes_events + grafo (BD) |
| **Resolution** | `thread_id` en BRIEF.md = binding EXACTO hilo↔workstream | nuestro session_id (#6 recién hecho) |
| **Runtime** | cargar SOLO lo necesario (tiered loading) | load_history + buscar_semantico |

**Concepto Project → Workstream:** un proyecto agrupa work de un dominio; un workstream es
una unidad acotada de ejecución dentro, atada a UN hilo. Cada workstream = directorio con 6
archivos: BRIEF (identidad+thread_id), STATUS (heartbeat ≤10 líneas), MEMORY (≤80 líneas
curado, NO log), DECISIONS, STAKEHOLDERS, RESOURCES + docs/.

---

## 2. ⭐ LO QUE TIENE RESUELTO QUE FOR3S OS NO (lo que vale traer)

### 2.1 🔴 HILOS por binding determinista (lo que justo arreglamos en #6)
- `thread_id` en BRIEF.md = binding EXACTO. **Resolución NO heurística**: match exacto o
  PARA y pregunta. PROHIBIDO fuzzy match, similitud, proximidad de nombres.
- **Doctrina de AISLAMIENTO:** por defecto NO leer otro workstream, NO escanear, NO inferir
  por nombres. Síntesis cross-workstream solo si el humano la pide explícito.
- **Nosotros (#6) llegamos a lo mismo** (session_id por usuario) pero ELLOS lo tienen como
  DOCTRINA explícita + nombrada. → Aprender: documentar nuestra regla de aislamiento como
  doctrina dura, no solo código.

### 2.2 ⭐⭐ Shared-thread inbox (EXACTAMENTE nuestro caso Telegram multi-usuario)
v0.4.0 resolvió que **en Telegram/WhatsApp/Signal NO hay hilos nativos** — un DM es la
superficie de varios workstreams. Solución: `shared_thread_ids: true` +
`shared_thread_platforms`. El thread_id resuelve al PROYECTO (contenedor), y el workstream
activo se decide por estado de tareas + intención humana explícita.
→ **DIRECTAMENTE RELEVANTE:** For3s vive en Telegram. Este es el patrón canónico para
manejar "un chat, varios temas/personas". Estudiar para C/D.

### 2.3 ⭐⭐⭐ Isolated-session handoff (= nuestro H8 multi-agente, pero MEJOR documentado)
Su v0.4.0 = lo MISMO que diseñamos para H8 (coordinator delega a specialist aislado), pero:
- **Manifest file-backed** (`handoffs/<id>.yml`) versionado (`internos_handoff: v1`).
- **4 invariantes doctrinales:** resolución determinista · aislamiento explícito ·
  archivos = verdad · separación de roles (specialist solo escribe handoffs/ + MEMORY.md,
  NUNCA BRIEF/STATUS/DECISIONS — esos son del coordinator).
- **Verifier de 2 capas** (`verify-handoff.sh`, POSIX, sin deps): (A) well-formedness,
  (B) binding checks nombrados. Cazó un EXPLOIT real (flow-style YAML evadía el allowlist).
- **Alineado con A2A (Google) / OpenAI Agents SDK / MCP** — diseño con conciencia del estándar.
→ **Nuestro H8 specialists** (specialists.py) hace esto en RAM con asyncio. El de ellos es
file-backed + auditable + portable. Aprender: el **audit trail file-backed** de cada
delegación (qué se pidió .yml, qué se devolvió .md) + la **separación estricta de escritura**.

### 2.4 ⭐⭐ Hooks de ciclo de vida (auto-cargar contexto = nuestro RETOMAR.md AUTOMÁTICO)
El adapter Claude Code tiene `SessionStart`/`SessionEnd` hooks que:
- **SessionStart:** inyecta el contexto del workstream (STATUS + últimas 3 sesiones + tareas
  abiertas + warnings) como system reminder ANTES del primer token. = nuestro RETOMAR.md
  pero AUTOMÁTICO y por-sesión.
- **SessionEnd:** estampa last_updated, añade línea a SESSIONS.md, corre sync-check, escribe
  warnings para la próxima sesión. = nuestro "cierre de sesión" pero AUTOMÁTICO.
→ Aprender: el patrón de **inyectar el estado al arranque** sin que el agente tenga que leer.
For3s ya inyecta memoria; esto es la versión disciplinada + el cierre automático.

### 2.5 Disciplina de tamaño + tiered loading (anti-bloat de contexto)
- STATUS.md ≤10 líneas, MEMORY.md ≤80 (target ≤50), validado por script.
- Tier 1 (BRIEF+STATUS) por defecto; Tier 2/3 on-demand. **ACK-first** en plataformas con
  timeout (Discord ~2min): responder "cargando..." ANTES de leer archivos.
→ For3s ya tiene algo (last_n turnos, G5-recuerdos-fragmentados pendiente). Su disciplina de
  "STATUS curado corto + MEMORY summary no log" es una buena regla para nuestra memoria.

### 2.6 Registry derivado + sync-check + checkpoint (observabilidad operativa)
- `generate-registry.sh` → índice derivado de todos los workstreams (NUNCA autoritativo).
- `sync-check.sh` → health check (thread_ids faltantes/duplicados, archivos, tamaños).
- `checkpoint-reminder.sh` → detecta STATUS.md stale.
→ For3s tiene audit_events + BD. Equivalente conceptual: un "estado de salud de los hilos".

### 2.7 Self-describing + versionado (= nuestro pendiente P4/G4 version-self-awareness)
v0.4.1: el skill instalado lleva `repo:` + `VERSION` + CHANGELOG → el agente SABE qué versión
corre y de dónde vino. CI valida que VERSION == SKILL.md version == git tag (3 lugares).
→ **EXACTAMENTE el pendiente P4 (control de versiones) y G4 de For3s.** Ellos ya lo resolvieron.

---

## 3. LO QUE FOR3S OS TIENE Y internOS NO (no todo es traer)

For3s es MUCHO más potente en capacidades de agente:
- **Memoria semántica real** (pgvector + embeddings BGE-M3 + búsqueda por significado).
  internOS = grep de archivos markdown. For3s recuerda por SIGNIFICADO; internOS por archivo.
- **Knowledge Graph** (AGE) + consolidación nocturna (CLS) + olvido (Microglía). internOS no
  tiene nada de esto — su "memoria" es un .md que el humano/agente curan a mano.
- **Multi-agente REAL en paralelo** (asyncio, 5 specialists, cost-control 7 capas). El de
  internOS es secuencial/doctrina (spawn 1 specialist por handoff).
- **LLM integrado, multimodal, GitHub MCP, web fetch, write tools seguras, cifrado KEK,
  audit inmutable.** internOS no ejecuta nada de eso — es coordinación documental.
- **BD transaccional.** internOS = archivos (riesgo de corrupción/concurrencia; ellos mismos
  marcan "concurrent specialists no locked" como limitación abierta).

**Resumen:** For3s = cerebro potente atado a servidor. internOS = esqueleto de coordinación
portable y distribuible. For3s puede APRENDER de su disciplina/portabilidad/distribución;
internOS no tiene el músculo de For3s.

---

## 4. QUÉ TRAER A FOR3S OS (recomendaciones priorizadas)

| # | Qué traer | De internOS | Cruza con |
|---|-----------|-------------|-----------|
| 1 | **Doctrina de aislamiento explícita + nombrada** (no solo código) | §2.1 | #6 ✅, D |
| 2 | **Patrón shared-thread inbox** para Telegram multi-usuario | §2.2 | C, D |
| 3 | **Handoff file-backed + audit trail + separación escritura** | §2.3 | H8 gate (E), G |
| 4 | **Auto-inyectar estado al arranque + cierre automático** | §2.4 | (RETOMAR auto) |
| 5 | **version-self-awareness** (el agente sabe su versión) | §2.7 | P4, G4 |
| 6 | **Disciplina STATUS corto + MEMORY summary + tiered** | §2.5 | G5, D |
| 7 | **Registry/health de hilos** (qué está activo) | §2.6 | C (/miembros), G |
| 8 | **Ser un SKILL/producto distribuible portable** (filosofía) | §0 | P1-P10 |

**El más valioso AHORA (estamos puliendo H8 multi-usuario):** #2 (shared-thread inbox — es
LITERALMENTE nuestro caso) y #3 (handoff file-backed para el gate E). #5 cierra P4/G4.

---

## 5. Inventario de archivos leídos (exhaustividad)

Raíz: README, CHANGELOG (24KB, todas las versiones v1.0.0→v0.4.1), LICENSE, .gitignore.
Skill: SKILL.md, VERSION, assets/WORKSTREAMS.md.
References EN (7): FRAMEWORK, PLAYBOOK, COMMUNICATION, TICK-INTEGRATION, ROLLOUT, SETUP,
ISOLATED-HANDOFF (ES = traducciones paralelas, no releídas).
Scripts (5): sync-check (290L), verify-handoff (348L), checkpoint-reminder, generate-registry,
extract-changelog.
Schema: handoff-v1.yaml. Templates: handoff/manifest, project/{PROJECT,AGENTS}, workstream/
{BRIEF,STATUS,MEMORY,DECISIONS,STAKEHOLDERS,RESOURCES}.
Adapters: claude-code (CLAUDE.md, SKILL.md, SETUP, hooks/settings.json, scripts: resolve-thread,
session-start, session-end, log-session), hermes/openclaw/generic SETUP.
Docs/specs: v0.4.0-isolated-handoff (383L), v0.3.2-hermes-compat, release-automation.
Examples: isolated-session-handoff, workspace-layout. .github: workflows/release, templates.

---

*Conclusión: intern-os es el "sistema nervioso de coordinación portable" que For3s podría
adoptar en disciplina y distribución, sin perder su músculo (memoria semántica, multi-agente
real, BD). Lo más urgente de adoptar dado dónde estamos (pulido H8 multi-usuario en Telegram):
el patrón shared-thread inbox y el handoff file-backed.*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde v1, ADR-029).
