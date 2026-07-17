# For3s OS vs Hermes Agent (NousResearch) — comparación real (2026-06-24)

> Comparación basada en el CÓDIGO REAL de `NousResearch/hermes-agent` (clonado y
> analizado: 5.465 archivos, README + estructura agent/gateway/tools/skills). NO de
> memoria. ⚠️ Este es el Hermes de NOUS RESEARCH (MIT, público), distinto del
> "Hermes de Frutero/OpenClaw". Solicitado por Brian.

---

## 0. Qué es cada uno (marco)

| | For3s OS | Hermes Agent (Nous) |
|---|---|---|
| Qué es | Agente "segundo cerebro" QA-wedge, autodesarrollo por hitos | Agente de IA self-improving, producto maduro masivo |
| Tamaño | ~50-60 módulos core, 1 paquete | **5.465 archivos** (2.532 py + 952 TS/TSX + web/TUI/docs) |
| Madurez | MVP+H5-H8, en pulido, 1 desarrollador | Producto público grande, equipo Nous, MIT, instalador 1-línea |
| Despliegue | 1 servidor (Tailscale), bot Telegram | 6 backends (local/Docker/SSH/Singularity/Modal/Daytona), serverless |
| Modelo | Claude (OAuth suscripción), /model 3 modelos | 300+ modelos (Portal/OpenRouter/etc.), sin lock-in |
| Canales | Telegram + CLI | Telegram, Discord, Slack, WhatsApp, Signal, Email, CLI, TUI |

**Honestidad de escala:** Hermes es un producto de otra magnitud (equipo, años, web/TUI/
multi-idioma). For3s es un proyecto de 1 persona en construcción. La comparación es de
CAPACIDADES y DISEÑO, no de tamaño.

---

## 1. Comparación capacidad por capacidad

| Capacidad | Hermes (Nous) | For3s OS | Veredicto |
|---|---|---|---|
| **Multi-canal** | 7+ (TG, Discord, Slack, WhatsApp, Signal, Email, CLI/TUI) | Telegram + CLI | Hermes ▲▲ (For3s = pendiente "otros canales") |
| **Multi-modelo** | 300+, switch sin código, sin lock-in | Claude OAuth + /model (3) | Hermes ▲▲ (For3s lo bloqueó a propósito: suscripción plana) |
| **Memoria** | Agent-curated + nudges + FTS5 session search + LLM summary | pgvector + BGE-M3 (semántica) + AGE (grafo) + CLS/Microglía noche | **PAR** — enfoques distintos, For3s más "neurológico", Hermes más search |
| **Modelar al usuario** | Honcho (dialectic user modeling) | P1 perfil propio (rol/stack/estilo/rasgos) — 1ª pasada hecha | Hermes ▲ (Honcho es más sofisticado); For3s ya tiene base |
| **Skills auto-generables** | ✅ learning loop: crea skills de la experiencia, se auto-mejoran, agentskills.io | ⬜ diseñado (R6, =H10-12), NO construido | Hermes ▲▲▲ (su diferenciador estrella) |
| **Sub-agentes paralelo** | delegate_tool + async_delegation (subagentes aislados) | ✅ H8 equipo (5 specialists paralelo + synth + 18 capas) | **PAR** |
| **Ejecutar código real** | code_execution_tool + terminal (6 backends) | sandbox de lint (ruff) en H4; ejecución real = P3 pendiente | Hermes ▲▲ |
| **Cron / automatización** | ✅ scheduler con delivery a cualquier plataforma | ✅ H6 nocturno (backup/CLS/Microglía/STATUS) — pero interno, no "tareas del usuario" | Hermes ▲ (el suyo es para el usuario; el de For3s es self-care) |
| **MCP arbitrario** | ✅ mcp_tool + mcp_oauth (cualquier server + OAuth) | P4 fase 1: MCPClient genérico (GitHub); fase 2 pendiente | Hermes ▲ (For3s dejó el terreno listo) |
| **Browser/web** | ✅ browser_tool (CDP, Camofox, cloud browser) | web_fetch híbrido (httpx + Playwright contenedor) | Hermes ▲ |
| **Voz** | ✅ transcripción de notas de voz (TTS+STT) | ⬜ descartado por recursos (Whisper pesa) | Hermes ▲ |
| **Seguridad** | command approval + DM pairing + container isolation | gate aprobación + puerta + KEK cifrado + audit inmutable + whitelist write | **PAR** (For3s fuerte en cifrado/audit) |
| **Multi-usuario / equipo** | DM pairing, allowed users | ✅ H8: puerta /invitar + roles + hilos por persona + memoria híbrida + kick + gate | **For3s ▲** (más desarrollado como EQUIPO) |
| **Producto distribuible** | ✅ instalador 1-línea (curl), Windows/Mac/Linux/Termux, web/TUI | ⬜ pendiente (P1-P10 producto) | Hermes ▲▲▲ |
| **Research/trajectories** | ✅ batch trajectory gen, compresión para entrenar modelos | ⬜ no aplica | Hermes (otro propósito) |

---

## 2. Lo que Hermes tiene y For3s NO (gaps reales)

1. **Skills auto-generables (learning loop)** — su diferenciador #1: crea/mejora skills solo.
   Para For3s es H10-12 (diseñado, no construido). El más grande.
2. **Producto distribuible** — instalador 1-línea, multi-OS, web + TUI. (For3s P1-P10 pendiente.)
3. **Multi-canal real** (7+ plataformas) — For3s solo Telegram.
4. **Multi-modelo (300+)** — For3s lo bloqueó a propósito (suscripción plana).
5. **Ejecutar código real / 6 terminal backends + serverless** — For3s solo lint.
6. **Voz, browser avanzado, MCP OAuth** — For3s parcial o no.

## 3. Lo que For3s tiene que Hermes NO (o hace distinto/mejor)

1. **Memoria "neurológica"** — grafo de conocimiento (AGE) + consolidación nocturna (CLS) +
   olvido real (Microglía) con relevancia/decay. Hermes usa search (FTS5) + curación; For3s
   modela la memoria como un cerebro (hipocampo→consolidación→olvido). Enfoque más biológico.
2. **EQUIPO multi-usuario maduro** — puerta /invitar (sin user_ids), roles encargado/miembro,
   hilos por persona aislados, memoria híbrida (privada+común), gate de aprobación, kick. Hermes
   tiene "allowed users" pero no este modelo de equipo colaborativo con conocimiento compartido.
2b. **Trazabilidad/auditoría enterprise** — audit chain inmutable + cifrado KEK por workspace +
   SOC2-oriented. Más fuerte en compliance/confianza B2B.
3. **Wedge QA** — For3s nace enfocado a calidad de software con honestidad/auditabilidad; Hermes
   es generalista.

## 4. Veredicto honesto

- **Hermes = producto maduro, generalista, distribuible, con el learning-loop como joya.**
  Está MUY por delante en alcance, distribución y skills auto-generables.
- **For3s = proyecto joven, foco QA, con 2 fortalezas propias reales:** la memoria biológica
  (grafo+CLS+Microglía) y el modelo de EQUIPO multi-usuario colaborativo. En esas dos, For3s
  tiene un enfoque que Hermes no replica igual.
- **Dónde For3s debe apuntar** (lo que ya está en pendientes): skills auto-generables (H10-12,
  el mayor gap), producto distribuible (P1-P10), y completar P3/P4/P5 de paridad.

> Nota: Hermes tiene migración desde OpenClaw y "dialectic user modeling" (Honcho) — confirma
> que el ecosistema Nous/OpenClaw/Hermes está entrelazado. For3s es independiente.

---

*Repo analizado: github.com/NousResearch/hermes-agent (MIT). Clonado en WSL2 /tmp para análisis.
For3s mantiene su trazabilidad de comparación SOLO en Mente OS (privado), nunca en código.*
