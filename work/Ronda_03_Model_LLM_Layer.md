# Ronda 3 — Model / LLM Layer (Master)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Tercera de las 10 rondas técnicas. Documento maestro de R3.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-01
**Última actualización:** 2026-06-03
**Estatus:** ✅ **CERRADO 100%** (4/4 bloques LOCKED · 14/14 sub-temas)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — §4 Nodo 3 sugiere "Claude Sonnet"
- [Mente/Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md](../Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md) — Nodo 3 PFC
- [Mente/Cuerpo/Ronda_01_Compute_Lenguaje.md](Ronda_01_Compute_Lenguaje.md) — Python 3.12 + anthropic SDK
- [Mente/Cuerpo/Ronda_02_Data_Layer.md](Ronda_02_Data_Layer.md) — R2 100% cerrado
- [Mente/Doc/Estado_Sesion_Continuidad.md](memory/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Sub-documentos detallados:**
- ✅ [Ronda_03_Bloque_1_LLM_Principal.md](Ronda_03_Bloque_1_LLM_Principal.md) — LLM Principal (4/4 LOCKED)
- ✅ [Ronda_03_Bloque_2_Prompt_Context.md](Ronda_03_Bloque_2_Prompt_Context.md) — Prompt & Context (4/4 LOCKED)
- ✅ [Ronda_03_Bloque_3_Streaming_Performance.md](Ronda_03_Bloque_3_Streaming_Performance.md) — Streaming & Performance (3/3 LOCKED)
- ✅ [Ronda_03_Bloque_4_Observability_Cost.md](Ronda_03_Bloque_4_Observability_Cost.md) — Observabilidad & Costo (3/3 LOCKED) ⭐ CIERRA R3

**Decisiones loggeadas en for3s-inter:**
- [D-012 — Stack LLM Principal LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-013 — Stack Prompt & Context Management LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-014 — Stack Streaming & Performance LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-015 — Stack Observabilidad & Costo LLM LOCKED + R3 100% CERRADO](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos, modelos cerrados aceptables con disclaimer)
- 3.D — Equipo pequeño (preferir simplicidad operacional)

**Constraint LOCKED aplicado:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes cap operacional

---

## Tabla de contenidos

1. [Propósito de R3](#1-propósito-de-r3)
2. [Pre-preguntas P1-P5 LOCKED](#2-pre-preguntas-p1-p5-locked)
3. [Aclaración arquitectónica crítica](#3-aclaración-arquitectónica-crítica)
4. [Estructura B+A — 4 bloques · 14 sub-temas](#4-estructura-ba--4-bloques--14-sub-temas)
5. [Resumen ejecutivo Bloque 1 — LLM Principal](#5-resumen-ejecutivo-bloque-1--llm-principal)
6. [Status Bloques 2, 3, 4](#6-status-bloques-2-3-4)
7. [Cobertura del Grafo Maestro](#7-cobertura-del-grafo-maestro)
8. [Costo total v1 actualizado](#8-costo-total-v1-actualizado)
9. [Spillovers hacia for3s-inter/](#9-spillovers-hacia-for3s-inter)
10. [Próximo paso](#10-próximo-paso)

---

## 1. Propósito de R3

R3 — Model / LLM Layer define el **cerebro generativo** de For3s OS. Es donde vive el razonamiento, la generación de outputs, y la orquestación de tools (puente con R4).

### Lo que R3 materializa del Grafo Maestro

```
   ╔══════════════════════════════════════════════════════════╗
   ║   PIEZAS DEL GRAFO MAESTRO ATERRIZADAS EN R3              ║
   ║                                                          ║
   ║   • Nodo 3 — PFC / Orchestrator (LLM principal)           ║
   ║   • Nodo 9 — Dual-Process Check (preparación R5)          ║
   ║   • Nodo 10 — CLS (Haiku ya integrado B2 2.6)             ║
   ║   • Nodo 11 — Neuromoduladores (preparación tier dynamic) ║
   ║   • Pilar 2 — Escalabilidad (resiliencia fallback)        ║
   ║   • Pilar 3 — Autonomía Generativa (foundation)           ║
   ╚══════════════════════════════════════════════════════════╝
```

### Relación con R1 y R2

- **R1** (Compute / Lenguaje) lockeó Python 3.12 + anthropic SDK + asyncio.
- **R2** (Data Layer) lockeó memoria + storage + backup. Claude Haiku ya integrado para CLS.
- **R3** define LLM PRINCIPAL para razonamiento del agente.

R3 sin R1+R2 = LLM sin contexto.
R1+R2 sin R3 = memoria sin generación.

---

## 2. Pre-preguntas P1-P5 LOCKED

Antes de los sub-temas técnicos, R3 abrió con 5 preguntas contextuales que definieron el espacio de soluciones.

### P1 — Uso principal del LLM ✅ LOCKED

```
MIXTO UNIVERSAL
   • Razonamiento profundo + Q&A rápido
   • Para CUALQUIER dominio (salud, belleza, código, etc.)
   • NO solo PRs
   • For3s OS es plataforma universal ("segundo cerebro")
```

### P2 — Prioridad LLM principal ✅ LOCKED

```
SONNET 4.6 DEFAULT → OPUS 4.7 SELECTIVO
   • Sonnet como modelo principal balanceado
   • Opus como upgrade tier per workspace
   • Haiku solo para CLS (B2 2.6 LOCKED)
```

### P3 — Privacy LLM principal ✅ LOCKED

```
CLOUD ANTHROPIC CON DISCLAIMER
   • DPA firmado con Anthropic
   • Datos sensibles via TLS 1.3
   • Cliente puede opt-out con flag allow_llm_fallback
   • Local LLM diferido a v3+ (sin GPU v1)
```

### P4 — Multi vs single model ✅ LOCKED

```
SINGLE-MODEL v1 (SONNET)
   • Un solo modelo por workspace (per tier)
   • Sin routing per request v1
   • Routing automático defer v2 con Nodo 9 R5
```

### P5 — Budget AI principal ✅ LOCKED

```
USD 50-200/mes CAP OPERACIONAL
   • Default workspace (Sonnet): ~$50/mes
   • Premium workspace (Opus): ~$200/mes max
   • Alarma 75% cap ($150/mes)
   • Hard stop 100% cap ($200/mes) → BudgetExceeded
```

---

## 3. Aclaración arquitectónica crítica

Durante R3, Brian aclaró un punto fundamental que aplica a TODAS las decisiones:

```
For3s = empresa
   │
   ├── For3s OS (plataforma universal "segundo cerebro")
   │      • Este chat habla SOLO de esto
   │      • Carpeta: Mente/
   │      • R1, R2, R3-R10 = construir For3s OS
   │      • Sirve para CUALQUIER dominio
   │      • Aprende de todo, refuerza lo aprendido
   │
   └── For3s QA (primer "agente vertical" sobre For3s OS)
          • Carpeta: for3s-inter/
          • Equipo trabajando aparte
          • Es el primer caso comercial para validar/cobrar
          • USA For3s OS como base
          • NO es scope de este chat

✅ Arquitectura R1+R2 = PERFECTA porque ES universal
✅ Wedge QA = primer agente vertical encima
✅ Fuente de verdad LOCKED: For3s_OS_Grafo_Maestro.md
```

Esta aclaración aplica retroactivamente: cuando R3 menciona casos de uso, son UNIVERSALES (no específicos a QA).

---

## 4. Estructura B+A — 4 bloques · 14 sub-temas

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 1 — LLM PRINCIPAL (4 sub-temas)  ✅ LOCKED            ║
║   ──────────────────────────────────────────────              ║
║   3.1.1 Provider LLM principal                                 ║
║   3.1.2 Modelo específico (Sonnet vs Opus configuración)       ║
║   3.1.3 Multi-model routing strategy                            ║
║   3.1.4 Local LLM fallback                                     ║
║                                                                ║
║   BLOQUE 2 — PROMPT & CONTEXT MANAGEMENT (4 sub-temas) ⏳      ║
║   ──────────────────────────────────────────────────────       ║
║   3.2.1 Prompt engineering framework                            ║
║   3.2.2 Context window management                               ║
║   3.2.3 Prompt caching strategy                                 ║
║   3.2.4 Function calling / tool use patterns                    ║
║                                                                ║
║   BLOQUE 3 — STREAMING & PERFORMANCE (3 sub-temas) ⏳           ║
║   ──────────────────────────────────────────────────             ║
║   3.3.1 Streaming responses                                     ║
║   3.3.2 LLM concurrency control                                  ║
║   3.3.3 Retry & fallback patterns                                ║
║                                                                ║
║   BLOQUE 4 — OBSERVABILIDAD & COSTO LLM (3 sub-temas) ⏳        ║
║   ──────────────────────────────────────────────────────         ║
║   3.4.1 LLM observability                                        ║
║   3.4.2 Cost monitoring per workspace                            ║
║   3.4.3 LLM quality evaluation                                    ║
║                                                                ║
║   TOTAL R3: 4 bloques · 14 sub-temas                           ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

### Modo operativo B+A

Mismo patrón que R2: bloques temáticos con sub-temas explícitos. Cada sub-tema sigue estructura ⑦ (contexto, mapeo, candidatos, tabla, tensión, recomendación, decisión).

---

## 5. Resumen ejecutivo Bloque 1 — LLM Principal

**Documento detallado:** [Ronda_03_Bloque_1_LLM_Principal.md](Ronda_03_Bloque_1_LLM_Principal.md)

### Las 4 decisiones LOCKED

```
3.1.1 Provider          → Anthropic + abstraction layer
3.1.2 Modelo específico → Sonnet default + Opus opt-in workspace
3.1.3 Multi-model       → NO routing v1, defer v2 con Nodo 9
3.1.4 Local LLM fallback → Cloud OpenAI fallback (sin GPU)
```

### Filosofía emergente del Bloque 1

```
"Provider único maduro con fallback automático, sin sobre-
ingeniería, alineado con Grafo Maestro §4 Nodo 3."

   • PROVIDER ÚNICO Anthropic (alineación Grafo Maestro)
   • TIERS per workspace (Sonnet/Opus configurable)
   • ABSTRACTION LAYER LLMProvider (swap futuro)
   • RESILIENCIA via OpenAI fallback (sin GPU local)
   • SIMPLICIDAD v1 (sin routing per request)
```

### Stack LLM v1 LOCKED

```
PRIMARY PROVIDER:
   • Anthropic (Claude family)
   • SDK: anthropic (oficial MIT)

MODELOS:
   • Default workspace: Claude Sonnet 4.6
   • Premium upgrade: Claude Opus 4.7 (opt-in)
   • CLS background: Claude Haiku 4.5 [B2 2.6 LOCKED]

FALLBACK PROVIDER:
   • OpenAI (GPT-4o)
   • Activación automática ante outages
   • SDK: openai (oficial)

EMBEDDINGS [B2 2.2 LOCKED]:
   • Primary: Stella local @ 1024 dim
   • Fallback: OpenAI text-embedding-3-small

ROUTING v1:
   • Tier per workspace (sonnet | opus)
   • Sin routing per request (defer v2)

ARQUITECTURA:
   • LLMProvider abstract Protocol
   • FailoverManager orquesta primary + fallback
   • Compatible swap futuro (Gemini, local LLM)
```

### Score honesto Bloque 1 R3

```
9.5/10 — Excelente

Fortalezas:
   • Alineación Grafo Maestro 10/10 (Nodo 3 sugiere Claude)
   • Coherencia con R1+R2 9.5/10 (anthropic SDK ya en stack)
   • Cumplimiento Anclas 10/10 (3/3 respetadas)
   • Cumplimiento Pre-preguntas P1-P5 10/10 (todas cumplidas)
   • Costo vs P2 10/10 (margen 92%)
   • Costo vs P5 10/10 (dentro cap $50-200/mes)
   • Future-proofing 9/10 (abstraction layer permite swap)
   • Simplicidad operacional 9/10 (sin routing complejo v1)

Áreas de vigilancia:
   • Dependencia Anthropic (mitigada con fallback OpenAI)
   • Local LLM diferido (esperado v3+ con GPU)
```

---

## 6. Status Bloques 2, 3, 4

### Bloque 2 — Prompt & Context Management ✅ LOCKED 2026-06-03

**Documento detallado:** [Ronda_03_Bloque_2_Prompt_Context.md](Ronda_03_Bloque_2_Prompt_Context.md)

**Las 4 decisiones LOCKED:**

```
3.2.1 Prompt framework      → Jinja2 + Pydantic + dataclasses
3.2.2 Context window mgmt   → Budget 15K + relevance + tier-aware
3.2.3 Prompt caching         → Stratificado 4 capas (-62% Sonnet)
3.2.4 Function calling       → Anthropic native + ToolRegistry
```

**Filosofía emergente:**

> "Foundation universal de razonamiento: templates versionables,
> contexto inteligente, caching agresivo, tool use limpio.
> R4 y R5 solo necesitan llenar el qué — el cómo ya está."

**Patrones clave:**
- Jinja2 + Pydantic templates versionables, type-safe, auditables
- Context budget 15K tokens distribuidos en 7 slots tier-aware
- 4 cache breakpoints Anthropic por estabilidad descendente
- ToolRegistry acepta 3 backends (LocalPython | MCPServer | AgentDelegation)
- 5 core tools LOCAL v1 predefinidas
- Permission model granular + audit chain por tool_call
- MAX_ITERATIONS=10 + TOOL_TIMEOUT=30s [B3 3.4 LOCKED reused]

**Foundation entregada a R4, R5, R7, R8, R9:**
- R4: MCPServerTool clase + tool_definitions cacheables + permission model
- R5: AgentDelegationTool + tool_use schema sub-agent + ContextBuilder
- R7: Streaming tool_use compatible + partial results foundation
- R8: Cache metrics + tool metrics + audit chain
- R9: Permission model granular + audit chain inmutable

**Score honesto B2 R3:**

```
9.5/10 — Excelente

Fortalezas:
   • Alineación Grafo Maestro 10/10 (Nodo 3 PFC + Nodo 1 + Nodo 5)
   • Coherencia con B1 9.5/10 (ClaudeProvider + FailoverManager)
   • Cumplimiento Anclas 10/10 (3/3 respetadas)
   • Cumplimiento Pre-preguntas 10/10
   • Costo vs P2 10/10 (margen 94.6%)
   • Costo vs P5 10/10 (28% del cap, margen $144)
   • Future-proofing 9.5/10 (abstracciones permiten v2-v3)
   • Simplicidad operacional 9/10 (vanilla Python stack)
   • Foundation R4-R9 9.5/10 (puentes limpios)

Áreas de vigilancia:
   • Re-ranking calibration v1 (puede omitir crítico)
   • Cache invalidation patterns (estabilidad layers)
```

### Bloque 3 — Streaming & Performance ✅ LOCKED 2026-06-03

**Documento detallado:** [Ronda_03_Bloque_3_Streaming_Performance.md](Ronda_03_Bloque_3_Streaming_Performance.md)

**Las 3 decisiones LOCKED:**

```
3.3.1 Streaming responses    → SSE (Server-Sent Events) HTTP
3.3.2 LLM concurrency control → CapacityLimiter + Token Bucket per workspace
3.3.3 Retry & fallback        → Taxonomía + RetryPolicy + Circuit Breaker
```

**Filosofía emergente:**

> "Resiliencia operacional sin sobre-ingeniería. Cada componente del Bloque 3 maneja un tipo específico de falla con la mínima complejidad necesaria. La UX percibida del usuario es lo más importante."

**Patrones clave:**
- Streaming SSE estándar HTTP con eventos canónicos LOCKED
- Cancel anticipado vía is_disconnected() + partial preserve con audit_flag
- CapacityLimiter(3) reused + Token Bucket per workspace en Valkey
- Tiers LOCKED: Pilot Light 10 RPM/10K TPM, Pilot Pro 50 RPM/50K TPM
- Token estimation chars/3.5 × 1.1 margin + refund post-call con números reales
- Taxonomía 14 ErrorTypes con RetryPolicy explícita por tipo
- Circuit Breaker per provider (5 errors/60s → OPEN, 30s → HALF_OPEN)
- NO retry mid-stream + Tool retry separado del LLM retry
- Idempotency metadata per tool + headers cliente Retry-After/X-LLM-Provider/X-Error-Type

**Foundation entregada a R3 B4, R4, R5, R7, R8, R9:**
- B4: métricas obligatorias 60+ definidas, cost tracking nativo, observability foundation
- R4: tool retry separado + idempotency metadata + tool error types
- R5: streaming sub-agent compatible + concurrency hereda + resilience reused
- R7: SSE protocol LOCKED + eventos canónicos + cancel API + heartbeat
- R8: métricas + audit chain + circuit breaker state observable
- R9: AUTH_FAILURE alarma + audit inmutable + idempotency integrity

**Score honesto B3 R3:**

```
9.5/10 — Excelente

Fortalezas:
   • Alineación Grafo Maestro 10/10 (Nodo 3 PFC + Nodo 6 + Pilar 2)
   • Coherencia con B1+B2 10/10 (zero duplicación, extensión limpia)
   • Cumplimiento Anclas 10/10 (3/3 respetadas)
   • Costo vs P2 10/10 (sin cambio neto, -10-15% LLM por errores)
   • Cap P5 10/10 (enforcement AUTOMÁTICO per workspace)
   • UX percepción 10/10 (3-10x mejor TTFT)
   • Resiliencia 9.5/10 (95% reducción 429s)
   • Future-proofing 9.5/10 (foundation R7/R8/R9)
   • Simplicidad operacional 9/10 (todo en código vanilla)

Áreas de vigilancia:
   • Token estimation calibración v1
   • Circuit breaker thresholds calibración v1
   • Cloudflare Tunnel SSE compatibility (tests prod)
```

### Bloque 4 — Observabilidad & Costo LLM ✅ LOCKED 2026-06-03 ⭐ CIERRA R3 100%

**Documento detallado:** [Ronda_03_Bloque_4_Observability_Cost.md](Ronda_03_Bloque_4_Observability_Cost.md)

**Las 3 decisiones LOCKED:**

```
3.4.1 LLM observability       → Audit chain + Prometheus metrics LOCAL
3.4.2 Cost monitoring          → Sistema completo (5 capacidades coordinadas)
3.4.3 LLM quality evaluation   → Framework híbrido 4 capas (rule+golden+judge+human)
```

**Filosofía emergente:**

> "Observability LLM-specific + cost monitoring + quality evaluation no son features — son lo que separa 'wrapper Claude bonito' de plataforma producción-ready B2B. Cada capa de B4 mitiga debilidades de las anteriores con interdependencia coordinada."

**Patrones clave:**
- Prometheus LOCAL ~200 MB RAM + audit chain Postgres (forensics 13 meses)
- ~25 métricas LLM-specific LOCKED, cardinality limit ~1200 series
- LLMCallRecorder wrapper atomic (audit + metrics juntos)
- Cost monitoring 5 capacidades: alarmas 50/75/90% + dashboard cliente self-service + anomaly 3-sigma + forecast + reporting (daily Brian + weekly/monthly clientes)
- 4 tipos anomaly clasificados: spike_hour, spike_sustained, key_leaked (AUTO-SUSPEND), bug_loop
- Eval framework 4 capas: rule-based (sync blocking critical) + golden datasets (CI/CD + weekly cron) + LLM-judge Haiku async 5% sample + human review weekly Brian
- Anti-sesgo eval: 5 strategies LOCKED (anonymization, multi-prompt rotation, golden refs, weekly calibration, evaluator diversity v2)
- Golden datasets v1: general (50 samples) + code (30 wedge QA)
- 5 tablas SQL nuevas (cost_alarms, cost_anomalies, eval_runs, eval_results, golden_datasets)
- Templates Jinja2 reused (B2 3.2.1) + Arq cron reused (R2 B3)

**Foundation entregada a R4-R10 (cierre R3 completo):**
- R4 Tools/MCP: tool metrics + tool eval rule-based + tool cost tracking
- R5 Orchestration: eval informa Nodo 9 Dual-Process + cost tracking sub-agent
- R6 Memory: eval informa CLS promotion + cost-aware retrieval
- R7 Frontend: dashboard cliente HTMX + quality scores expuestos
- R8 Observability: Prometheus ready + ~25 métricas + audit chain inmutable
- R9 Security: eval safety per dominio + anomaly key_leaked auto-suspend + PII detection
- R10 CI/CD: eval pre-deploy regression check + cost forecasting foundation billing

**Score honesto B4 R3:**

```
9.5/10 — Excelente

Fortalezas:
   • Alineación Grafo Maestro 10/10 (Nodo 3 + 10 + 11 + 3 Pilares)
   • Coherencia con B1+B2+B3 10/10 (reusa Haiku, Arq, Jinja2, Valkey, audit)
   • Cumplimiento Anclas 10/10 (3/3 respetadas)
   • Costo vs P2 10/10 (eval $5-15/mes dentro cap P5)
   • Cap P5 10/10 (alarmas graduales + hard cap + enforcement auto)
   • UX enterprise B2B 10/10 (dashboard cliente + transparencia)
   • Defendibilidad comercial 10/10 (eval framework respondible)
   • Foundation R4-R10 9.5/10 (todos los puentes claros)
   • Anti-sesgo eval 9/10 (5 strategies + calibración)

Áreas de vigilancia:
   • Golden datasets curation Brian (sesgo personal)
   • Cardinality Prometheus a escala
   • Human review queue discipline weekly
```

---

## R3 — STATUS FINAL POST-B4

```
╔══════════════════════════════════════════════════════════════╗
║   ✅✅✅ R3 — MODEL/LLM LAYER 100% CERRADO ✅✅✅              ║
║                                                                ║
║   Bloque 1 ✅ LOCKED (4/4) — D-012                              ║
║   Bloque 2 ✅ LOCKED (4/4) — D-013                              ║
║   Bloque 3 ✅ LOCKED (3/3) — D-014                              ║
║   Bloque 4 ✅ LOCKED (3/3) — D-015 ⭐ CIERRA R3                  ║
║                                                                ║
║   TOTAL: 14/14 sub-temas LOCKED (100%)                          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 7. Cobertura del Grafo Maestro

### Nodos servidos por R3 COMPLETO (post-B1+B2+B3+B4)

```
NODO                         BLOQUE 1   BLOQUE 2   BLOQUE 3   BLOQUE 4
─────────────────────────────────────────────────────────────────────────
Nodo 1 Hipocampo              —          ✅ context  —         —
Nodo 3 PFC (Orchestrator)    ✅ LLM     ✅ tmpl+tool ✅ resilien ✅ obs+cost+eval
Nodo 4 Cuerpo Calloso         —          🟡 found   —          —
Nodo 5 Memoria Largo          —          ✅ context  —         —
Nodo 6 Sistema Sensorial      —          —          🟡 stream   —
Nodo 8 Tálamo                 —          🟡 found   🟡 concurrent —
Nodo 9 Dual-Process Check    🟡 prep    —          —          🟡 eval informa
Nodo 10 CLS                   ✅ Haiku   ✅ tmpl    —          ✅ cost+eval
Nodo 11 Neuromoduladores     🟡 prep    🟡 prep    🟡 stress    🟡 signals B4

Status post-R3 COMPLETO:
   ✅ Nodos servidos plenos: 3, 10 (2 nodos)
   ✅ Nodos servidos contexto: 1, 5 (2 nodos)
   🟡 Foundation: 4, 6, 8, 9, 11 (5 nodos preparados R5+)
```

### Pilares — Cobertura por R3 COMPLETO (post-B1+B2+B3+B4)

```
Pilar 1 — Seguridad E2E
   ✅ Meta-audit todas las operaciones LLM (B1+B2+B3+B4)
   ✅ Cliente opt-out fallback (B1)
   ✅ Permission model granular (B2 3.2.4)
   ✅ Transparencia provider via headers (B1 + B3 X-LLM-Provider)
   ✅ TLS 1.3 cloud providers (B1)
   ✅ Audit chain inmutable retry/CB/fallback (B3) + eval/cost (B4)
   ✅ Tool timeout enforcement (B2 3.2.4)
   ✅ Idempotency tools preserve data integrity (B3 3.3.3)
   ✅ Workspace fairness anti-DoS interno (B3 3.3.2)
   ✅ AUTH_FAILURE alarma crítica (B3 3.3.3)
   ✅ Eval safety dimension per dominio (B4 3.4.3)
   ✅ Anomaly detection key_leaked AUTO-SUSPEND (B4 3.4.2)
   ✅ PII leakage detection eval rule-based (B4 3.4.3 CAPA 1)
   ⏳ Prompt injection detection (R9)

Pilar 2 — Escalabilidad por nodo
   ✅ FailoverManager resiliencia (B1 3.1.4)
   ✅ CapacityLimiter concurrency (R2 B3 reused)
   ✅ Caching -62% costo Sonnet maduro (B2 3.2.3)
   ✅ Context budget evita explosión costos (B2 3.2.2)
   ✅ Tool parallel execution con limiter (B2 3.2.4)
   ✅ Streaming reduce memoria servidor (B3 3.3.1)
   ✅ Token Bucket per workspace (B3 3.3.2)
   ✅ Circuit Breaker evita cascadas (B3 3.3.3)
   ✅ Cap P5 enforcement AUTOMÁTICO + graduales (B3+B4)
   ✅ Observability tiempo real Prometheus LOCAL (B4 3.4.1)
   ✅ Forecast proactive end-of-month (B4 3.4.2)
   ✅ Anomaly detection statistical (B4 3.4.2)

Pilar 3 — Autonomía Generativa
   ✅ LLM principal habilita razonamiento autónomo (B1)
   ✅ LLM decide tools autónomamente con guardrails (B2 3.2.4)
   ✅ Templates evolucionables per dominio (B2 3.2.1)
   ✅ Agente decide qué error reintentar (B3 3.3.3)
   ✅ Tool retry separado del LLM loop (B3 3.3.3)
   ✅ Eval feedback informa LLM-judge calibration (B4 3.4.3)
   ✅ Anomaly auto-actions sin Brian intervention (B4 3.4.2)
   ⏳ Meta-Orchestrator (Pilar 3 completo) v3+
```

### Anclas LOCKED — Status post-B1+B2 (verificado)

```
1.D Dedicated SaaS  ✅ tier per workspace (B1)
                     ✅ templates per workspace, cache separado (B2)
                     ✅ allowed_tools whitelist per workspace (B2 3.2.4)

2.B Open Core       ✅ SDKs abiertos:
                        • anthropic (MIT) [B1]
                        • openai (MIT) [B1]
                        • Jinja2 (BSD) [B2 3.2.1]
                        • Pydantic v2 (MIT) [B2]
                     Modelos cerrados aceptable con disclaimer (P3 LOCKED)

3.D Equipo pequeño  ✅ provider único maduro, sin routing complejo v1 (B1)
                     ✅ stack vanilla Python sin frameworks pesados (B2)
                     ✅ abstracciones limpias para extensión R4+R5 (B2)
```

---

## 8. Costo total v1 FINAL (post-R3 100% LOCKED)

```
Hardware Linux LOCAL Brian:                   USD 0
Electricidad servidor 24/7:                   USD ~5/mes
Cloudflare Tunnel + R2:                       USD 0 (free tier)
Dominio for3s.ai:                             USD ~$1/mes
PostgreSQL + AGE + pgvector + pgcrypto:       USD 0
Custom memory + Stella + HDBSCAN:             USD 0
Valkey + Arq + pgbouncer:                     USD 0
asyncio + anyio + librerías pool:             USD 0
Backup tools:                                  USD 0
OpenAI fallback embeddings:                   USD <1/mes
Claude Haiku 4.5 (CLS, B2 2.6 R2):              USD ~37/mes
─────────────────────────────────────────────────────────────
SUBTOTAL R1+R2:                                USD ~43/mes

R3 BLOQUE 1:
Claude Sonnet 4.6 (principal):                 USD ~50/mes
OpenAI fallback LLM (raro):                    USD ~$0.30/mes

R3 BLOQUE 2 (impacto neto caching):
Caching maduro saving (-62%):                  USD ~-$31/mes
Tool overhead (~20% calls):                    USD ~+$6/mes (compensado)

R3 BLOQUE 3 (impacto neto resilience):
Streaming SSE infra:                           USD 0 (sse_starlette MIT)
Token Bucket infra:                            USD 0 (Valkey ya en stack)
Resilience taxonomía:                          USD 0 (todo en código)
Reducción errors mal manejados:                USD ~-$5-10/mes (estimado)

R3 BLOQUE 4 (impacto observability + eval):
Prometheus LOCAL:                              USD 0 (200 MB RAM, 5 GB disco)
Cost monitoring (5 capacidades):               USD 0 (reusa Arq+Valkey+Jinja2)
Eval Haiku (5% sample):                        USD ~+$5-15/mes
Email SMTP local:                              USD 0
─────────────────────────────────────────────────────────────
TOTAL v1 FINAL (R1+R2+R3 100% LOCKED):         USD ~62-77/mes
```

### Vs constraint P2 <25% pilot revenue (FINAL post-R3 100%)

```
Pilot Light USD 3,500 (3 semanas)
   Techo AI+infra: USD 875 (25%)
   Consumo real v1 FINAL (3 sem): USD ~55
   → 6.3% del techo
   → MARGEN 93.7% disponible para R4-R10

Pilot Pro USD 8,000 (3 semanas)
   Techo: USD 2,000
   Consumo v1: USD ~55
   → 2.8% del techo
   → MARGEN 97.2%

CONCLUSIÓN: R3 100% LOCKED deja margen MASIVO para R4-R10.
```

### Verificación P5 cap LLM ($50-200/mes) FINAL

```
LLM total v1 FINAL con caching maduro:
   • Claude Haiku CLS:                       ~$37/mes
   • Claude Sonnet con caching maduro:       ~$19/mes (-62%)
   • Claude Haiku eval (5% sample, B4):      ~$5-15/mes
   • OpenAI fallback:                         ~$0.30/mes (raro)
   ─────────────────────────────────────────────
   TOTAL:                                     ~$61-71/mes

Cap P5 LOCKED:           $50-200/mes
% del cap (medio):       31-36%
Margen disponible:       $130-140 para escalado workspaces

   → Caching + eval + observability DENTRO del cap P5
   → 2.5x más volumen disponible vs hard cap teórico
```

---

## 9. Spillovers hacia for3s-inter/

Aplicando **Protocolo Bidireccional** (Estado_Sesion §3.1.quater).

### Spillovers escritos al cerrar Bloque 1 R3 (2026-06-01)

```
✅ for3s-inter/07-operations/decision-log.md
   + D-012 (Stack LLM Principal LOCKED)

✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (este master)
✅ Mente/Cuerpo/Ronda_03_Bloque_1_LLM_Principal.md (detallado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.decies
```

### Spillovers escritos al cerrar Bloque 2 R3 (2026-06-03)

```
✅ for3s-inter/07-operations/decision-log.md
   + D-013 (Stack Prompt & Context Management LOCKED)

✅ Mente/Cuerpo/Ronda_03_Bloque_2_Prompt_Context.md (detallado)
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (este master actualizado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.undecies
```

### Spillovers escritos al cerrar Bloque 3 R3 (2026-06-03)

```
✅ for3s-inter/07-operations/decision-log.md
   + D-014 (Stack Streaming & Performance LOCKED)

✅ Mente/Cuerpo/Ronda_03_Bloque_3_Streaming_Performance.md (detallado)
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (este master actualizado)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.duodecies
```

### Spillovers escritos al cerrar Bloque 4 R3 (2026-06-03) ⭐ CIERRA R3

```
✅ for3s-inter/07-operations/decision-log.md
   + D-015 (Stack Observabilidad & Costo LLM LOCKED + R3 100% CERRADO)

✅ Mente/Cuerpo/Ronda_03_Bloque_4_Observability_Cost.md (detallado)
✅ Mente/Cuerpo/Ronda_03_Model_LLM_Layer.md (este master 100% CERRADO)
✅ Mente/Doc/Estado_Sesion_Continuidad.md §3.1.terdecies
```

### Spillovers FASE 2 (cierre formal R3, en ejecución)

```
⏳ for3s-inter/09-technical-architecture/model-llm-layer.md
   (agregar Bloque 4 al sub-doc consolidado público-formal)

⏳ for3s-inter/09-technical-architecture/README.md
   (status R3 → ✅ CERRADO 100%, 14/14 sub-temas)

⏳ for3s-inter/02-product/mvp-scope.md
   (LLM stack annotation FINAL R3 100%)

⏳ for3s-inter/05-finance/unit-economics.md
   (refresh costo total v1 final post-R3)
```

Estos 4 archivos se actualizan en FASE 2 (OPCIÓN 1) inmediatamente después de FASE 1 para cierre formal R3 público-formal completo.

---

## 10. Próximo paso

**R3 100% CERRADO** — los 4 bloques LOCKED, 14/14 sub-temas, 4 decisiones (D-012, D-013, D-014, D-015).

**Inmediato (FASE 2 cierre formal):**
- Actualizar `09-technical-architecture/model-llm-layer.md` con Bloque 4
- Actualizar `09-technical-architecture/README.md` (R3 → ✅ CERRADO 100%)
- Actualizar `02-product/mvp-scope.md` (stack annotation FINAL R3)
- Actualizar `05-finance/unit-economics.md` (costo total final)

**Después de FASE 2:**
- Iniciar **R4 — Tools / MCP Layer** (siguiente ronda técnica)
  - Foundation lista: tool_use schema, ToolRegistry 3 backends, MCPServerTool clase abstracta, tool metrics observables, tool eval rule-based, tool cost tracking
  - Decisiones a tomar: MCP client framework, MCP servers concretos (GitHub QA wedge), tool discovery/registration, hosting LOCAL/cloud, tool authorization workflows