# 🩻 RADIOGRAFÍA EXACTA — `Fruterito-principal/` (censo forense completo)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Radiografia_Fruterito_Principal.md → docs/analysis/Radiografia_Fruterito_Principal.md (2026-07-30, ADR-029)

## Purpose

🩻 RADIOGRAFÍA EXACTA — `Fruterito-principal/` (censo forense completo)


> **Fecha:** 2026-07-04 · **Fuente:** `~/entrenamiento/Fruterito-principal/` en el server (read-only)
> **Origen del material:** copia de `C:\...\Downloads\.openclaw` (el OpenClaw de Windows de Brian)
> **Totales verificados:** **5,786 archivos · 291 MB · 15 carpetas nivel 1 + 6 archivos raíz**
> Parte del HITO ENTRENAMIENTO (F1-censo). Árbol hermano pendiente: `Fruterito-wsl/`.

---

## 0 · Mapa de nivel 1 (los 5,786 archivos, todos contados)

| Carpeta | Archivos | Peso | Qué es (veredicto) |
|---|---:|---:|---|
| `media/` | 1,389 | 110 MB | 📸 Archivos que Brian mandó por Telegram (feb→abr): 1,234 jpg + docs |
| `agents/` | 174 | 97.6 MB | 💬 **Las conversaciones**: dev (74MB!) + watchdog (18MB) + main + 15 godin-slots |
| `workspace/` | 3,794 | 71.7 MB | 🧠 **EL CORAZÓN**: identidad + memoria + 16 skills + proyectos + docs |
| `cron/` | 7 | 0.8 MB | ⏰ 1 job real (monitor de tickets Godínez Studio) + 2 logs de corridas |
| `workspaces/` | 350 | 0.6 MB | 📋 14 plantillas godin-slot-2..15 SIN llenar (idénticas entre sí) |
| `memory/` | 1 | 70 KB | 🗃️ `dev.sqlite` — índice semántico **VACÍO** (0 chunks; nunca se usó) |
| *(raíz)* | 6 | 44 KB | ⚙️ `openclaw.json` ×5 backups + `exec-approvals.json` |
| `workspace-main/` | 25 | 39 KB | 📋 Plantilla base workspace (idéntica a godin-slot-1 en nombres+tamaños) |
| `workspace-godin-slot-1/` | 25 | 39 KB | 📋 Ídem — plantilla sin personalizar |
| `logs/` | 1 | 12 KB | `config-audit.jsonl` (auditoría de cambios de config) |
| `canvas/` | 1 | 4 KB | `index.html` de prueba |
| `devices/` | 4 | 3.6 KB | `paired.json` (dispositivos emparejados) ⚠️ |
| `identity/` | 2 | 0.8 KB | ⛔ `device.json` + `device-auth.json` (llaves) — SECRETO |
| `telegram/` | 6 | 0.2 KB | Offsets/hashes de runtime del bot |
| `subagents/` | 1 | 33 B | `runs.json` casi vacío |

**Extensiones globales:** 2,127 sin extensión (mayoría objetos `.git`) · 1,245 jpg · 630 `.sample` (hooks git) · **605 .md** · 313 tsx · 197 ts · 116 json · **84 jsonl** · 79 png · 60 docx · 54 txt · 16 pack (git) · 8 pdf…

---

## 1 · `agents/` — las conversaciones (174 archivos, 97.6 MB)

### 1.1 🔨 `agents/dev` — ⭐ HALLAZGO MAYOR: 115 archivos, 74.6 MB, **17,096 turnos**

**Nadie lo tenía censado** (el censo previo solo veía main/watchdog/cipher/helix). Es el
**2º agente con más conversación de TODO el material** y era el que TRABAJABA: el cron job
`godinez-studio-tickets-monitor` corría con `agentId: dev`. Es el Fruterito-desarrollador
de Godínez Studio.

- 113 archivos de sesión (`.jsonl` + `.reset` + `.deleted` + `.bak`) + `sessions.json`
  (índice, 2.3 MB).
- Sesiones estrella: una de **54 MB** (`f30a7098….jsonl.reset.2026-04-01`) — la madre de
  todas las sesiones; otra de 9.9 MB viva al final (`c27178c0….jsonl`, 2026-04-05).
- 12 sesiones `-topic-<id>` = hilos/topics de Telegram (marzo).
- Actividad: 2026-02-08 → 2026-04-05 (el final de la era OpenClaw).
- ⚠️ `agent/auth-profiles.json` (no listado arriba pero presente en dev también vía runtime).

### 1.2 📰 `agents/watchdog` — 19 archivos, 17.9 MB, **20,749 turnos** (el máximo)

- 17 sesiones + `sessions.json`. Patrón claro: casi todas son `.jsonl.reset.YYYY…T04-0X`
  → **el watchdog se reseteaba cada madrugada ~4AM** (job diario). Cada archivo = ~1 día
  de monitoreo (2026-03-15 → 03-31).
- Gordas: 5.0 MB (03-16), 4.9 MB (03-30), 3.0 MB (03-18).
- ⛔ `agent/auth-profiles.json` — SECRETO.

### 1.3 🍍 `agents/main` — 5 archivos, 4.6 MB, ~1,214 líneas

**Casi vacío en este árbol**: son 3 backups (`.bak-*`) de UNA MISMA sesión del 2026-02-07
(825fd4d1…, ~1.5 MB c/u = triplicada) + `sessions.json`. **El main real (40 sesiones,
6,045 turnos) vive en `Fruterito-wsl/agents/main`** — este es solo el arranque de febrero
en Windows. ⛔ `auth-profiles.json`.

### 1.4 👔 `agents/godin-slot-1..15` + `dev`/`default`

- **Solo `godin-slot-1` habló**: 18 sesiones chicas (3-77 KB), **211 turnos**, en 2 tandas
  (2026-03-25/26 y 2026-04-03) + `sessions.json` de 392 KB. Un piloto de los Godínez.
- **`godin-slot-2..15`: VACÍOS** — 1 solo archivo cada uno (⛔ `auth-profiles.json`, 460 B).
- `default`: 1 archivo de 2 bytes. Nada.

---

## 2 · `workspace/` — EL CORAZÓN (3,794 archivos, 71.7 MB)

### 2.1 Raíz: la IDENTIDAD de Fruterito DevRel (29 archivos)

Los 20 .md + 5 docx + 4 ocultos, archivo por archivo (verificado el título real de cada uno):

| Archivo | Peso | Qué es |
|---|---:|---|
| `SOUL.md` | 4.0 KB | "Who You Are" — el alma del agente (actualizada hasta 03-14) |
| `IDENTITY.md` | 2.3 KB | "Fruterito DevRel" — nombre, rol, vibe |
| `USER.md` | 1.0 KB | "About Your Human" — **Brian visto por su agente** |
| `ETHICS.md` | 5.6 KB | Código de Ética Operativo (con emoji de escudo, versión rica) |
| `AGENTS.md` | 7.9 KB | "Your Workspace" — reglas de operación del workspace |
| `FRUTERITO-SISTEMA.md` (+.docx) | 7.3+13.6 KB | 🍓 "Sistema Completo" — cómo funciona todo Fruterito |
| `HISTORIAL-COMPLETO.md` (+.docx) | 7.2+15.5 KB | 📜 "Historial Completo — Fruterito & Brian" — LA HISTORIA |
| `MEMORY.md` | 1.1 KB | Índice de memoria long-term (actualizado 04-01, el final) |
| `SKILLS-INVENTARIO.md` | 6.1 KB | 📦 Inventario de las 17 skills activas (2026-03-02) |
| `TOOLS.md` | 1.0 KB | Notas locales de herramientas |
| `TOKEN-EFFICIENCY.md` | 1.7 KB | Reglas de eficiencia de tokens (modo ahorro) |
| `PRIORIDAD.md` | 0.8 KB | 🔴 la prioridad activa del momento |
| `HEARTBEAT.md` | 0.4 KB | config del heartbeat |
| `BOOTSTRAP.md` | 1.5 KB | "Hello, World" — arranque plantilla |
| `SESION-3-CHECKPOINTS.md` (+.docx) | 9+15.8 KB | Guión teleprompter "Mi Regenmon Está Vivo" (bootcamp) |
| `SESION-3-GUION-FORMATO-BRIAN.md` | 6.8 KB | Guión sesión 3 "Stats y Evolución" **en formato-Brian** |
| `SESION-3-GUION.docx` / `-v2.docx` | 14.2+13.9 KB | Versiones docx del guión |
| `onboarding-v3-implementacion.md` | 9.9 KB | Onboarding V3 Godínez — implementación final |
| `sse-architecture.md` | 9.8 KB | Arquitectura SSE de Godínez Studio |
| `temp-onboarding-complete.md` | 23.8 KB | Godínez AI onboarding flow integrado |
| `temp-professional-flow.md` | 6.5 KB | Godínez AI flujo profesional |
| ⛔ `.github-token` | 41 B | **SECRETO — token GitHub en texto plano** |
| ⛔ `.synthesis-credentials` | 215 B | **SECRETO — credenciales** |
| `.genomad-state.json` | 116 B | estado del skill genomad |
| `.gitignore` | 22 B | — |

### 2.2 `memory/` — la memoria escrita del agente (115 archivos)

- **7 diarios** `2026-03-26 … 2026-04-04.md` (1.3–7.3 KB c/u) — los días finales, en detalle.
  *(Los 99 diarios censados antes incluyen `archive/`: 16 de 2026-02 + 18 de 2026-03.)*
- **8 memorias temáticas** en raíz: `brian-prefs.md` (⭐ preferencias de Brian), `lecciones.md`,
  `genomad.md`, `godinez-studio.md`, `github-favoritos.md`, `monad-blitz.md`,
  `proyectos-activos.md`, `wsl2-system.md`.
- `archive/` — 34 diarios viejos + `analisis-existencial-corregido/` (5) + `analisis-viejos/` (11).
- `acompanante/` — memoria por proyecto acompañado, 41 archivos en 5 proyectos:
  `agentcamp/ · arvi/ · genomad/ · godinez-ai/ (21: docs de arquitectura, learnings, tickets-state) ·
  vibecoding-bootcamp/` — cada uno con `config.json + learnings.md + metrics.json + logs/`
  y ⛔ **`password.txt` en 5 de ellos (SECRETOS en texto plano)**.

### 2.3 `skills/` — las 16 skills custom, skill por skill (655 archivos)

| Skill | Archivos | Peso | Qué hace (de su SKILL.md real) |
|---|---:|---:|---|
| `acompanante` | 75 | 202 KB | Acompañamiento de proyectos/bootcamps/lives; modos Enfocado e Incógnito |
| `audit-code` | 33 | 60 KB | Auditoría de código 2 pasadas multidisciplinaria (security/perf/UX/DX) |
| `bootcamp-tracker` | 29 | 40 KB | 🎓 Tracker de bootcamps |
| `convex-skill` | 42 | 128 KB | Backend Convex: queries, mutations, actions, schemas |
| `cracked-dev` | 33 | 66 KB | Workflow spec-driven: epics → phases → tickets → PR |
| `genetic-system` | 39 | 135 KB | 🧬 Sistema genético (base de Genomad) |
| `genomad` | 76 | 206 KB | Skill oficial Genomad: registro, breeding, custody on-chain |
| `godinez-practices` | 29 | 42 KB | Metodología del equipo Godínez: Git, PRs, commits atómicos |
| `hackathon-mode` | 48 | 75 KB | Modo focus hackathons Web3 en WSL2 (chains, sponsors, scaffolding) |
| `marketing-designer` | 36 | 102 KB | Marketing creativo estilo Peggy Olson + data-driven |
| `monad-blitz-projects` | 86 | 206 KB | 🟣 Proyectos Monad Blitz |
| `monad-development` | 29 | 39 KB | Dapps en Monad: contratos, viem/wagmi, verificación |
| `nad-fun` | 31 | 44 KB | Tokens en nad.fun (launchpad Monad, bonding curves) |
| `risc-zero` | 47 | 122 KB | RISC Zero (ZK proofs) |
| `smart-router` | 1 | 15 KB | Routing inteligente de modelos (clasifica, delega, aprende) |
| `tick-coord` | 21 | 80 KB | Coordinación multi-agente vía Markdown git-backed (tick-md) |

**El `SKILLS-INVENTARIO.md` del agente lista 17 activas** = 10 de estas custom + 7 builtin de
OpenClaw (clawhub, coding-agent, github, healthcheck, skill-creator, tmux, weather). Las
carpetas incluyen además versiones/variantes no activas.

### 2.4 Proyectos con código (los repos donde trabajó)

| Carpeta | Archivos | Peso | Qué es |
|---|---:|---:|---|
| `projects/godinez-ai` | 119 | 13.5 MB | App Godínez AI (src+convex+docs, .git 6.8MB, public 6.3MB) |
| `projects/regenmon-bootcamp` | 178 | 3.4 MB | Proyecto Regenmon del bootcamp |
| `projects/godinez-studio` | 182 | 1.1 MB | Godínez Studio |
| `projects/godinez-skills` | 43 | 95 KB | Skills de Godínez |
| `meetup-q1-puebla` | 277 | 39.8 MB | Web del meetup (Vite+React; .git 19.6MB + public 17.9MB de imágenes) |
| `temp-reporte` | 184 | 675 KB | Proyecto de reporte (src + .git) |
| `openclaw-smart-router` | 155 | 224 KB | Repo del smart-router (config, templates, examples) |
| `openclaw-token-saver` | 66 | 79 KB | Ahorro de tokens (profiles) |
| `openclaw-aws-persistence` | 41 | 44 KB | Persistencia de OpenClaw en AWS |
| `frutero-ops` | 52 | 45 KB | 🍉 Ops de Frutero: pendientes/agentes/proyectos/equipo/logs (git) |
| `acompañante` | 57 | 78 KB | Repo del sistema acompañante (templates, docs) |
| `cracked-dev` | 33 | 66 KB | Repo del workflow cracked-dev |

### 2.5 Conocimiento destilado suelto

- `analysis/vibecoding/` — **344 archivos, 6.3 MB**: `Vibe-Coding/` (223) + `regenmon-final/`
  (116) + 5 raíz → análisis masivo del bootcamp Vibecoding.
- `docs/` (4): `BLITZ-CDMX-COMPARATIVA.md`, `BLITZ-CDMX-GODINEZ-STUDIO-COMPLETO.md` +
  `-REPORTE-COMPLETO.md`, `godinez-studio/ONBOARDING-V3-SPEC.md` (42.6 KB).
- `exports/` (11): ANALISIS-TECNICO-ONBOARDING-V2 · ANALISIS-TECNICO-PERSONAL-HACKATHON
  (27.8 KB) · GODINEZ-ONBOARDING-UX-RESEARCH · GODINEZ-STUDIO-ANALISIS-COMPLETO ·
  GS-21-ERROR-OBSERVATORY (SPEC+FINAL) · ONBOARDING-FLOW-INTEGRADO-V2 ·
  REPORTE-SUBAGENTES-GODINEZ · VIBECODING-BOOTCAMP-GUIA-COMPLETA (.md+.docx) ·
  plan-implementacion-onboarding-v2.
- `downloads/` (16): specs de backend Genomad (BACKEND-SPEC ×3), 6 docx de Genomad
  (GENESIS-AGENTS, BREEDING, MVP, Economía-GMD, Modelo-Negocio, Servicios-Tarifas),
  guiones SESION-4/SESION-5 (teleprompter).
- `hackathons/` (42): `monad-moltiverse/` (40: PROJECT-AGENT-BREEDING, GENESIS-EVOLUTION,
  PRESENTACION-GENOMAD, IDEAS-LOCAS, TREND-ANALYSIS, agents/FRUTERITO-GENESIS +
  JAZZITA-GENESIS + CHILD-001-GENESIS…) + `monad-blitz-monterrey/` (1).
- `bootcamps/` (37): `vibecoding-bootcamp/` (19) + `vibecoding-arco2/` (4) +
  `vibecoding-reporte/` (5) + `frutero-builders-sprint/` (1) + scripts + `_global/`.
- `temp/` (14): componentes React del chat de Godínez Studio (ChatConversation, DropZone,
  use-chat…) + `gs24-flow-diagram.md`.
- `.git/` — **1,135 archivos, 2.3 MB**: TODO el workspace estaba versionado en git
  (el historial de commits es en sí conocimiento: qué cambió y cuándo).

---

## 3 · `media/` — 1,389 archivos, 110 MB

- `inbound/` (1,387): lo que Brian mandó por Telegram del 2026-02-06 al 2026-04-04 —
  **1,234 jpg + 42 png + 37 txt + 33 md + 26 docx + 8 pdf + 2 ogg (voz) + 1 mp4 + 1 csv** +
  3 sin extensión. Fotos de pizarras/eventos/pantallas + documentos adjuntos.
- `outbound/` (2): `ESTUDIO-SESION-2.docx` + `SESION-2-TELEPROMPTER.md` (lo que el agente
  le produjo/mandó a Brian el 02-11).

---

## 4 · Plantillas godin (`workspaces/`, `workspace-main/`, `workspace-godin-slot-1/`)

- `workspaces/godin-slot-2..15`: **14 copias IDÉNTICAS** (25 archivos, 39,402 bytes cada
  una): plantilla OpenClaw virgen — `IDENTITY.md` dice literalmente *"Fill this in during
  your first conversation"* — **nunca se personalizaron**. 18 de los 25 archivos son
  `.git/hooks/*.sample` (basura git).
- `workspace-main/` y `workspace-godin-slot-1/`: la MISMA plantilla (idénticos en nombres
  y tamaños entre sí). SOUL.md plantilla: *"You're not a chatbot. You're becoming someone."*
- **Veredicto: 350+50 archivos de plantilla sin valor de conocimiento** (solo confirma el
  diseño del sistema Godínez de 15 slots).

---

## 5 · Runtime OpenClaw (cron, memoria sqlite, config, telegram…)

- `cron/jobs.json` — **1 job real**: `godinez-studio-tickets-monitor` (agente **dev**, cada
  30 min, aún `enabled:true` al momento de la copia): *"Revisa tickets de
  fruteroclub/godinez-studio… notifica a Brian (@LPBrayan0) si hay cambios"*. + `cron/runs/`:
  2 jsonl de corridas (804 KB el grande) + 3 tmp vacíos + 1 bak.
- `memory/dev.sqlite` — índice semántico de OpenClaw **VACÍO** (tablas files/chunks/
  embedding_cache en 0). La memoria real siempre fue los .md.
- Raíz: `openclaw.json` ×5 (config completa del sistema en 5 versiones feb→mar — histórico
  de configuración) + `exec-approvals.json` (aprobaciones de ejecución).
- `logs/config-audit.jsonl` (12.5 KB) — auditoría de cambios de config.
- `telegram/` — offsets y hashes de runtime (default + watchdog). Sin valor.
- `devices/paired.json` (3.6 KB) ⚠️ dispositivos emparejados · `subagents/runs.json` (33 B,
  vacío) · `canvas/index.html` (demo).

---

## 6 · ⛔ SECRETOS detectados en ESTE árbol (lista de exclusión parcial)

| Archivo | Qué es |
|---|---|
| `identity/device.json` + `identity/device-auth.json` | llaves privadas del dispositivo |
| `agents/*/agent/auth-profiles.json` (×19: main, watchdog, dev*, godin-slot-1..15) | perfiles de auth |
| `workspace/.github-token` | **token GitHub texto plano** |
| `workspace/.synthesis-credentials` | credenciales |
| `workspace/memory/acompanante/{agentcamp,arvi,godinez-ai,vibecoding-bootcamp,…}/password.txt` (×5) | **passwords texto plano** |
| `devices/paired.json` | tokens de emparejamiento |
| `openclaw.json*` (×5) | config: puede contener botToken Telegram (verificar antes de importar) |
| `media/inbound/*` | ⚠️ revisar: docs/fotos podrían contener credenciales visibles |

*(El detector automático de F1 barrera TODO de nuevo; esta lista es lo ya confirmado a ojo.)*

---

## 7 · Lectura del despiece — dónde está el ORO

| Valor | Material | Destino natural (marco §4 del Plan Maestro) |
|---|---|---|
| 🥇 ORO | `workspace/` raíz: SOUL, IDENTITY, USER, ETHICS, HISTORIAL-COMPLETO, FRUTERITO-SISTEMA | Perfil de Brian + conocimiento; personalidad SOLO con gate |
| 🥇 ORO | `workspace/memory/` (diarios + brian-prefs + lecciones + temáticas + acompanante/learnings) | Episodios con fecha origen + conceptos al grafo |
| 🥇 ORO | `agents/dev` (17,096 turnos) + `agents/watchdog` (20,749) | episodes_events por lotes curados |
| 🥈 MUY BUENO | 16 skills custom (sus SKILL.md + guías) | candidatos a skills H12, uno por uno |
| 🥈 MUY BUENO | docs/exports/downloads/hackathons/bootcamps/analysis (conocimiento destilado Godínez/Genomad/Vibecoding/Monad) | memoria semántica + grafo |
| 🥉 BUENO | proyectos con código (godinez-ai, regenmon…) + historial git del workspace | referencia; NO se importa código a memoria — backlog |
| 🗑️ RUIDO | plantillas godin ×16, telegram/, tmp, .sample hooks, sqlite vacío, canvas | basura (registrada en manifiesto) |
| ⛔ NUNCA | los secretos de §6 | exclusión sellada |
| 📸 CASO APARTE | `media/inbound` (110 MB) | decidir con Brian: las fotos no van a memoria de texto; los .md/.docx/.txt adjuntos SÍ son candidatos |

### Los 4 hallazgos que cambian el plan

1. **`agents/dev` existe y es enorme** (74 MB, 17,096 turnos): el censo previo de "6 agentes"
   no lo incluía. Es el Fruterito-DESARROLLADOR (Godínez Studio). → **Son 7 fuentes de
   conversación, no 6.**
2. **El `main` de este árbol está casi vacío** — el Fruterito Personal real vive en
   `Fruterito-wsl`. Este árbol aporta: dev + watchdog + workspace completo.
3. **Solo godin-slot-1 llegó a hablar** (211 turnos); los otros 14 son plantilla virgen →
   el "ejército Godínez" fue diseño, no historia.
4. **Más secretos de los censados**: además de los 47 conocidos aparecieron `.github-token`,
   `.synthesis-credentials` y 5 `password.txt` — el detector de F1 es imprescindible.

---

*Siguiente en el censo: radiografía gemela de `Fruterito-wsl/` (main real 6,045 turnos +
workspace-empleado 734 docs + for3s-design + cipher/helix + credentials/ + skills mode_*).*

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `docs/analysis/Radiografia_Fruterito_Principal.md`).
