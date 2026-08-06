# 🧱 BLOQUES DE `Fruterito-principal` + `agents/dev` — el mapa de DESMANTELAMIENTO

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Entrenamiento_Bloques_Fruterito_Principal_Dev.md → memory/archive/Entrenamiento_Bloques_Fruterito_Principal_Dev.md (2026-07-30, ADR-029)

> **Fecha:** 2026-07-04 · **Para qué:** arrancar el HITO ENTRENAMIENTO. Este es el mapa de
> demolición controlada: QUÉ bloques existen, QUÉ contiene cada uno, QUÉ está dentro de qué,
> y a dónde va cada pieza en For3s OS.
> **Fuentes verificadas:** `docs/analysis/Radiografia_Fruterito_Principal.md` (5,786 archivos censados) +
> `docs/analysis/Radiografia_Agente_Dev_FruteroDevBot.md` (dev a fondo) — nada aquí es estimado.

---

## 0 · LA CLAVE PARA ENTENDER TODO: dev NO es una caja aparte

`agents/dev` (@fruterodev_bot) solo posee DOS cosas propias: **sus sesiones** (las
conversaciones) y **su config/auth**. Todo lo demás — identidad, memoria escrita, skills,
proyectos — vivía en el **workspace COMPARTIDO** con el Fruterito principal (mismo SOUL.md,
misma memoria). Por eso el desmantelamiento es del ÁRBOL COMPLETO, con dev como el bloque
de conversación más gordo.

---

## 1 · EL DIAGRAMA DE BLOQUES (qué está dentro de qué)

```
╔══════════════════════════════════════════════════════════════════════════╗
║              FRUTERITO-PRINCIPAL  (291 MB · 5,786 archivos)               ║
║                                                                            ║
║  ┌──────────────────────────── B1 · IDENTIDAD ───────────────────────────┐ ║
║  │ workspace/ raíz — 20 .md + 5 .docx                                    │ ║
║  │ ├─ los 8 QUE ENTRABAN AL PROMPT (receta systemPromptReport):          │ ║
║  │ │   SOUL.md · IDENTITY.md · USER.md · AGENTS.md · TOOLS.md            │ ║
║  │ │   HEARTBEAT.md · BOOTSTRAP.md · MEMORY.md(=índice de B2)            │ ║
║  │ ├─ carácter extendido: ETHICS.md · FRUTERITO-SISTEMA.md               │ ║
║  │ │   HISTORIAL-COMPLETO.md (la historia Brian↔Fruterito)               │ ║
║  │ └─ operación: PRIORIDAD.md · TOKEN-EFFICIENCY.md · SKILLS-INVENTARIO  │ ║
║  └───────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌──────────────────────── B2 · MEMORIA ESCRITA ─────────────────────────┐ ║
║  │ workspace/memory/ — 115 archivos                                      │ ║
║  │ ├─ DIARIOS: 7 finales (2026-03-26→04-04) + archive/ 34 viejos         │ ║
║  │ │   (2026-02 ×16 · 2026-03 ×18) + análisis archivados ×16             │ ║
║  │ ├─ TEMÁTICAS (8): brian-prefs · lecciones · genomad · godinez-studio  │ ║
║  │ │   github-favoritos · monad-blitz · proyectos-activos · wsl2-system  │ ║
║  │ └─ POR PROYECTO acompañado (41): acompanante/{agentcamp·arvi·genomad· │ ║
║  │     godinez-ai(21)·vibecoding}/ → learnings.md + metrics + pending    │ ║
║  │     ⛔ 5 password.txt AQUÍ DENTRO (excluir)                            │ ║
║  └───────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌──────────────── B3 · CONVERSACIÓN (memoria episódica) ────────────────┐ ║
║  │ agents/ — 174 archivos · 97.6 MB · ~39,270 turnos                     │ ║
║  │ ├─ ⭐ dev/  74.6MB · 113 sesiones · 17,096 turnos (feb-07→abr-05)     │ ║
║  │ │    · LA MADRE: 54MB DM Telegram Brian (reset 04-01)                 │ ║
║  │ │    · 12 hilos -topic- Discord (SSE, frontend, AgentCamp…)           │ ║
║  │ │    · ~50 sesiones cron aisladas (monitoreo, REPETITIVAS=ruido)      │ ║
║  │ │    · sessions.json: índice 77 sesiones (canal/tokens/prompt-report) │ ║
║  │ ├─ watchdog/  17.9MB · 17 sesiones · 20,749 turnos (1/día, reset 4AM) │ ║
║  │ ├─ main/  4.6MB · 1 sesión ×3 backups (feb; el main real está en WSL) │ ║
║  │ ├─ godin-slot-1/  211 turnos (piloto godínez) · slots 2-15 VACÍOS     │ ║
║  │ └─ ⛔ 19× agent/auth-profiles.json (excluir)                           │ ║
║  └───────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌──────────────────────────  B4 · SKILLS ───────────────────────────────┐ ║
║  │ workspace/skills/ — 16 carpetas · 655 archivos (SKILL.md + guías +    │ ║
║  │ scripts): acompanante · audit-code · bootcamp-tracker · convex ·      │ ║
║  │ cracked-dev · genetic-system · genomad · godinez-practices ·          │ ║
║  │ hackathon-mode · marketing-designer · monad-blitz · monad-dev ·       │ ║
║  │ nad-fun · risc-zero · smart-router · tick-coord                       │ ║
║  └───────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌──────────── B5 · CONOCIMIENTO DESTILADO + PROYECTOS ──────────────────┐ ║
║  │ ├─ docs/ (4: BLITZ-CDMX, ONBOARDING-V3-SPEC)                          │ ║
║  │ ├─ exports/ (11: análisis técnicos, GS-21, guía Vibecoding)           │ ║
║  │ ├─ downloads/ (16: specs backend + 6 docx Genomad + guiones sesión)   │ ║
║  │ ├─ hackathons/ (42: monad-moltiverse GENESIS/breeding/propuestas)     │ ║
║  │ ├─ bootcamps/ (37: vibecoding ×3 + builders-sprint)                   │ ║
║  │ ├─ analysis/ (344: Vibe-Coding 223 + regenmon-final 116)              │ ║
║  │ ├─ PROYECTOS CON CÓDIGO (~1,100): godinez-ai/studio/skills ·          │ ║
║  │ │   regenmon · meetup-q1-puebla · temp-reporte · openclaw-tools ×3 ·  │ ║
║  │ │   frutero-ops · acompañante · cracked-dev  (+ .git = historial)     │ ║
║  │ └─ temp/ (14 componentes React sueltos)                               │ ║
║  └───────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌───────────── B6 · CONFIG/RUNTIME ─────────────┐ ┌──── B7 · MEDIA ─────┐ ║
║  │ openclaw.json ×5 (agentes/canales/bindings)   │ │ inbound/ 1,387:     │ ║
║  │ cron/ (2 jobs + runs 838KB) · logs/audit      │ │  1,234 jpg + 33 md  │ ║
║  │ telegram/ · devices/ · subagents/ · canvas/   │ │  + 26 docx + 8 pdf  │ ║
║  │ ⛔ identity/device.json · exec-approvals      │ │  + 2 voz (feb→abr)  │ ║
║  │ workspaces/godin 14 plantillas VÍRGENES       │ │ outbound/ 2 (docx)  │ ║
║  │ memory/dev.sqlite = VACÍO (0 chunks)          │ │                     │ ║
║  └───────────────────────────────────────────────┘ └─────────────────────┘ ║
║                                                                            ║
║  ⛔ CAPA TRANSVERSAL DE SECRETOS (cruza B1/B2/B3/B6):                       ║
║     .github-token · .synthesis-credentials · 5×password.txt ·              ║
║     19×auth-profiles.json · device.json/device-auth · botTokens en        ║
║     openclaw.json · posibles secretos DENTRO de sesiones (línea x línea)  ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Cómo se conectaban los bloques EN VIVO** (la receta del systemPromptReport):
`B1 (8 .md) + índice de B2 (MEMORY.md) + catálogo de B4 (skills XML) → SYSTEM PROMPT`
→ el agente conversaba (**B3**) usando manos (`exec`) sobre **B5**, gobernado por **B6**,
recibiendo **B7** de Brian. `dev` = B3.dev + B6.cron + B6.auth; TODO lo demás compartido.

---

## 2 · FICHA DE CADA BLOQUE PARA EL DESMANTELAMIENTO

| Bloque | Qué es | Volumen | Valor | Destino en For3s OS (marco Plan Maestro §4) |
|---|---|---|---|---|
| **B1 · IDENTIDAD** | el "quién soy" de Fruterito + historia con Brian | 25 archivos, ~150KB | 🥇 ORO | USER/HISTORIAL/prefs → **perfil de Brian + episodios**; SOUL/IDENTITY/ETHICS → conocimiento; a personalidad SOLO lo que Brian apruebe (gate) |
| **B2 · MEMORIA ESCRITA** | diarios + temáticas + learnings por proyecto | 115 archivos, ~640KB | 🥇 ORO | diarios → **episodios con fecha origen**; temáticas/learnings → **conceptos del grafo** |
| **B3 · CONVERSACIÓN** | las sesiones crudas (dev/watchdog/main/godin-1) | 97.6MB, ~39K turnos | 🥇 ORO (curado) | → **episodes_events por lotes** + re-embeber + consolidación nocturna; cron-runs repetitivas = resumir o descartar |
| **B4 · SKILLS** | 16 habilidades escritas con guías | 655 archivos, 1.5MB | 🥈 MUY BUENO | → candidatas a **skills H12** una por una (curación con Brian) |
| **B5 · CONOCIMIENTO+PROYECTOS** | análisis, specs, guiones, código | ~2,300 archivos | 🥈 (docs) / 🥉 (código) | docs → **memoria semántica+grafo**; código → NO se importa, va al **backlog herramientas** |
| **B6 · CONFIG/RUNTIME** | el esqueleto OpenClaw | ~420 archivos | 🗑️ + 📋 referencia | NO se importa; openclaw.json+cron ya minados como **referencia de diseño** (OC-*/cron conversacional) |
| **B7 · MEDIA** | lo que Brian mandó por Telegram | 1,389 archivos, 110MB | 📸 caso aparte | .md/.docx/.txt adjuntos → candidatos a memoria; fotos → decisión con Brian |
| **⛔ SECRETOS** | credenciales en 4 bloques | 47+ archivos | ⛔ | **EXCLUSIÓN SELLADA** — jamás a memoria; detector línea-por-línea para B3 |

---

## 3 · ORDEN DE DESMANTELAMIENTO PROPUESTO (de más oro a menos)

1. **B1 + B2** (identidad + memoria escrita, ~140 archivos chicos) — el ALMA. Se despieza
   primero: es poco volumen, máximo valor, y CALIBRA el marco memoria-vs-personalidad con
   Brian antes de tocar lo masivo.
2. **B3.dev** (17,096 turnos) — la conversación del desarrollador: curar (fuera cron-runs
   repetitivas), lotear, importar con fecha/canal de origen.
3. **B3.watchdog** (20,749 turnos) — mismo pipeline, ya barato.
4. **B4 skills** (16) — una por una con gate: ¿skill H12, concepto, o descarte?
5. **B5 docs** (docs/exports/downloads/hackathons/bootcamps/analysis) — a semántica+grafo.
6. **B7 media** (solo los documentos adjuntos; fotos = decisión Brian).
7. **B6 + resto de B3** (main triplicado, godin-slots, plantillas) — cierre: casi todo
   basura registrada en el manifiesto; B6 ya rindió su valor como referencia de diseño.

Cada paso = ciclo del Plan Maestro (despiece→gate Brian→import→examen de conocimiento→§5-BIS).

---

*Cruza con: `work/Ronda_Entrenamiento_Plan_Maestro.md` (F0, fases y reglas) · las 2 radiografías
(detalle archivo-por-archivo de cada bloque) · PENDIENTES §ENTRENAMIENTO E1-E4.*