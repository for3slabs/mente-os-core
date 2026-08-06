# Ronda 5 — Orchestration / Multi-Agent (Master)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_05_Orchestration_Multi_Agent.md → work/Ronda_05_Orchestration_Multi_Agent.md (2026-07-30, ADR-029)

## Purpose

Ronda 5 — Orchestration / Multi-Agent (Master)


**Quinta de las 10 rondas técnicas. Documento maestro de R5.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-06
**Última actualización:** 2026-06-06
**Estatus:** ✅ **R5 CERRADO 100%** (4 bloques · 14/14 sub-temas LOCKED)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — §4 Nodos 6, 8, 9, 11 + Multi-Agent Network
- [Mente/work/Ronda_04_Tools_MCP_Layer.md](work/Ronda_04_Tools_MCP_Layer.md) — R4 v1 100% CERRADO (foundation tools)
- [Mente/work/Ronda_03_Model_LLM_Layer.md](work/Ronda_03_Model_LLM_Layer.md) — R3 100% CERRADO (foundation LLM)
- [Mente/memory/Estado_Sesion_Continuidad.md](../memory/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Sub-documentos detallados:**
- ✅ [Ronda_05_Bloque_1_Talamo_Routing.md](work/Ronda_05_Bloque_1_Talamo_Routing.md) — Tálamo & Routing (4/4 LOCKED)
- ✅ [Ronda_05_Bloque_2_Dual_Process_Check.md](work/Ronda_05_Bloque_2_Dual_Process_Check.md) — Dual-Process Check (3/3 LOCKED)
- ✅ [Ronda_05_Bloque_3_Multi_Agent_Network.md](work/Ronda_05_Bloque_3_Multi_Agent_Network.md) — Multi-Agent Network (4/4 LOCKED) ⭐ hardening 18 capas
- ✅ [Ronda_05_Bloque_4_DMN_Default_Mode.md](work/Ronda_05_Bloque_4_DMN_Default_Mode.md) — DMN / Default Mode Network (3/3 LOCKED) ⚠️ 5.4.2 refinamiento pendiente

**Decisiones loggeadas en for3s-inter:**
- [D-019 — Stack Tálamo & Routing LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-020 — Stack Dual-Process Check LOCKED + history-aware extension](../../for3s-inter/07-operations/decision-log.md)
- [D-021 — Stack Multi-Agent Network LOCKED + hardening 18 capas](../../for3s-inter/07-operations/decision-log.md)
- [D-022 — Stack DMN LOCKED + R5 100% CERRADO](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño (preferir simplicidad operacional)

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes
- P3 — Workspace isolation
- P4 — Encryption at rest

---

## Tabla de contenidos

1. [Propósito de R5](#1-propósito-de-r5)
2. [Pre-preguntas P1-P3 LOCKED](#2-pre-preguntas-p1-p3-locked)
3. [Estructura B+A — 4 bloques · 14 sub-temas](#3-estructura-ba--4-bloques--14-sub-temas)
4. [Resumen ejecutivo Bloque 1 — Tálamo & Routing](#4-resumen-ejecutivo-bloque-1)
5. [Resumen ejecutivo Bloque 2 — Dual-Process Check](#5-resumen-ejecutivo-bloque-2)
6. [Resumen ejecutivo Bloque 3 — Multi-Agent Network](#6-resumen-ejecutivo-bloque-3)
7. [Resumen ejecutivo Bloque 4 — DMN](#7-resumen-ejecutivo-bloque-4)
8. [Cobertura del Grafo Maestro](#8-cobertura-del-grafo-maestro)
9. [Costo total v1 actualizado post-R5](#9-costo-total-v1-actualizado-post-r5)
10. [Riesgos consolidados R5 + mitigaciones](#10-riesgos-consolidados)
11. [Notas críticas pendientes](#11-notas-críticas)
12. [Próximos pasos R6](#12-próximos-pasos)

---

## 1. Propósito de R5

R5 — Orchestration / Multi-Agent es la **capa cerebral coordinadora** de For3s OS. Las rondas anteriores construyeron:

- **R1:** lenguaje + runtime (Python 3.12 + FastAPI + asyncio)
- **R2:** memoria (Postgres + AGE + pgvector + 3-tier)
- **R3:** LLM Layer (Claude Sonnet/Opus + budgets + SSE + cost)
- **R4:** tools/MCP (57 tools + workspace isolation + lifecycle)

**R5 responde:** ¿quién COORDINA todo esto cuando llega una request?

R5 materializa 4 nodos del Grafo Maestro (6 DMN, 8 Tálamo, 9 Dual-Process Check, 11 Neuromoduladores) + Multi-Agent Network completo.

**Sin R5, For3s OS es un wrapper LLM con memoria. Con R5, es un sistema cognitivo coordinado.**

---

## 2. Pre-preguntas P1-P3 LOCKED

| # | Pregunta | Decisión | Justificación |
|---|---|---|---|
| **P1** | Single-agent vs Multi-agent | **C — Híbrido** (single default + multi on-demand) | Pilot Light viable + capability batch grandes wedge QA |
| **P2** | Imperativo vs Autónomo orquestación | **C — Híbrido** (esqueleto imperativo + ramas LLM) | Predictable security/audit + flexible context decisions |
| **P3** | Idle DMN | **B+C híbrido refinado** (real pero restrictible) | Cumple "agente piensa mientras humanos no activos" + cost-controlled |

**Brian quote P3 (verbatim):** "DEBE DE SER ALGO ENTRE B +C ALGO QUE PODAMOS ELEGIR Y RESTRINGIR PERO QUE EL PUEDA PENSAR CUANDO NO ESTAMOS ACTIVOS LOS HUMANOS Y MEJORE"

---

## 3. Estructura B+A — 4 bloques · 14 sub-temas

```
BLOQUE 1 — TÁLAMO & ROUTING (Nodo 8 + 11)
   5.1.1 ✅ Tool Selection Strategy (B+C híbrido)
   5.1.2 ✅ Context Routing (C+D híbrido)
   5.1.3 ✅ Subgraph Activation (C — 3 modos GM)
   5.1.4 ✅ Neuromoduladores (B — 4 modos GM)

BLOQUE 2 — DUAL-PROCESS CHECK (Nodo 9)
   5.2.1 ✅ Sistema 1 vs Sistema 2 detection (C multi-señal)
   5.2.2 ✅ LLM Tier Routing (C + HISTORY-AWARE Brian)
   5.2.3 ✅ Fast Path Optimization (C — 3 layers)

BLOQUE 3 — MULTI-AGENT NETWORK
   5.3.1 ✅ Agent Topology (C — Hub-and-spoke)
   5.3.2 ✅ Agent Lifecycle HARDENED (C — asyncio + 18 capas)
   5.3.3 ✅ Inter-Agent Communication (C — asyncio.Queue + broadcast)
   5.3.4 ✅ Sub-Agent Cost Control (C — 7 layers)

BLOQUE 4 — DMN / DEFAULT MODE NETWORK (Nodo 6)
   5.4.1 ✅ Idle Detection + Scheduling (C híbrido)
   5.4.2 ✅ Tasks Declarativas (C — 8 tasks) ⚠️ refinamiento crítico pendiente
   5.4.3 ✅ Budget + Cliente Controls (C — 9 controles)

TOTAL R5: 4 bloques · 14 sub-temas · 14/14 LOCKED ✅
```

---

## 4. Resumen ejecutivo Bloque 1 — Tálamo & Routing

**Materializa: Grafo Maestro Nodo 8 Tálamo + Nodo 11 Neuromoduladores**

### 5.1.1 — Tool Selection Strategy: B+C Híbrido
- **Workspace whitelist estático** (R4 4.1.2 reused) **+ Semantic ranking runtime**
- Stella embeddings R2 B2 + cosine similarity
- Top-K default 10 (configurable per workspace)
- Always-include list per workspace (override)
- Cumple budget tool slot R3 B2 3.2.2 (≤1,500 tok)
- Audit: `thalamus_tool_selection` event

### 5.1.2 — Context Routing: C+D Híbrido
- **Budget enforcement R3 B2 3.2.2 + Semantic selection per tier**
- 4 tiers contextuales: working_memory + episodes + kg_facts + embeddings
- SKIP_THRESHOLD 0.3 (omite tier si similarity insuficiente)
- NER ligero para entity extraction (KG Cypher)
- Ahorro ~50-70% tokens vs cargar todo
- Audit: `thalamus_context_routing` event

### 5.1.3 — Subgraph Activation: 3 modos Grafo Maestro
- **MÍNIMO** (80% queries trivial)
- **COMPLETO** (15% queries complejas)
- **EMERGENCIA** (5% security/compliance)
- Classifier heurístico v1 → ML v2
- Workspace override `force_complete_mode`
- Foundation Dual-Process B2 + Amígdala R9

### 5.1.4 — Neuromoduladores: 4 modos Grafo Maestro
- **EXPLORATION** (default business hours)
- **CONSOLIDATION** (idle >5min o cron nocturno)
- **HIGH_ATTENTION** (emergency subgraph)
- **REST** (idle >30min o cost cap P5 >80%)
- Triggers event-driven (subgraph, idle, cron, cost)
- Audit: `neuromod_transition` event
- Foundation DMN B4 (consolidation activa DMN)

---

## 5. Resumen ejecutivo Bloque 2 — Dual-Process Check

**Materializa: Grafo Maestro Nodo 9 (Kahneman S1/S2)**

### 5.2.1 — Sistema 1 vs Sistema 2 detection: C multi-señal
- 4 grupos signals con pesos:
  - QUERY (peso 1.0): length, keywords, ?marks
  - CONTEXT (peso 1.5): subgraph + neuromod + tools
  - HISTORY (peso 2.0): workspace avg + similar query
  - WORKSPACE OVERRIDE (peso 3.0): force_s2 + tier
- Threshold default 3.0, tunable per workspace
- Cero LLM overhead per query
- Audit: `dual_process_decision` event

### 5.2.2 — LLM Tier Routing: C + HISTORY-AWARE (input Brian) ⭐
- **6 factores routing** (5 base + 1 history-aware Brian):
  1. BASE por score (5.2.1)
  2. NEUROMOD adjustment (5.1.4)
  3. COST CAP P5 protection
  4. WORKSPACE TIER (enterprise vs pilot)
  5. CACHE PRE-CHECK (handoff 5.2.3)
  6. ⭐ **HISTORY-AWARE PRECISION**:
     - 6a. Similar queries (pgvector + audit log)
     - 6b. KG patterns (Cypher AGE + CLS)
     - 6c. Session deep flow (Hipocampo episodes)
- Overhead: ~35ms per query (sin LLM extra)
- ACTIVA capacidad generativa Nodo 9 v1 (no v3)
- Cold start protection (skip factor 6 si <5 datos)

### 5.2.3 — Fast Path Optimization: 3 layers
- **LAYER 1:** Cache exact (Valkey R2 B3)
- **LAYER 2:** Cache semántico (Stella + pgvector)
- **LAYER 3:** Heurísticas locales (Python handlers)
- **FALLBACK:** routing normal (5.2.1 + 5.2.2)
- Cobertura: 50-60% queries trivial
- Latencia: 5-50ms (vs 800ms+ LLM)
- Cost saving: 50-60% real
- Handlers v1: workspace_info, list_tools, last_query

---

## 6. Resumen ejecutivo Bloque 3 — Multi-Agent Network

**Materializa: Grafo Maestro Multi-Agent Network**

### 5.3.1 — Agent Topology: Hub-and-spoke con specialists
- PFC main → spawnea HUB → HUB spawnea N specialists
- Specialists ejecutan paralelo → reportan HUB → HUB consolida
- **5 specialists v1 registrados:**
  - code_analyzer (Opus)
  - security_auditor (Opus)
  - test_generator (Sonnet)
  - performance_analyzer (Sonnet)
  - doc_writer (Sonnet)
- Cada specialist: system_prompt + tools subset + LLM tier
- Cap N specialists ≤ 5 v1 (workspace configurable)
- Extensible v2: workspace custom specialists

### 5.3.2 — Agent Lifecycle HARDENED: 18 capas defense-in-depth ⭐
- Base: asyncio.Task per specialist (spawn ~50μs)
- 5-phase lifecycle: SPAWN → EXECUTION → TERMINATION → CLEANUP → ARCHIVE

**HARDENING CONTRA 1 (Aislamiento) — 7 capas:**
1. ContextVar isolation (Python nativo per-task)
2. Tools whitelist enforcement runtime (R4 4.1.2)
3. KEK scoping derived (R4 4.1.3, master KEK queda main)
4. Postgres Row-Level Security (`SET LOCAL app.current_workspace_id`)
5. Resource quotas (anyio Semaphore: DB max 2, HTTP max 5/s)
6. Mutation guards default read-only + OCC
7. Runtime anomaly detection + emergency kill

**HARDENING CONTRA 2 (Blocking) — 5 capas:**
1. Static check CI/CD (ruff banned-api + AST scan)
2. Tool Protocol async-only (`inspect.iscoroutinefunction`)
3. anyio.to_thread pool con CapacityLimiter aislado
4. Event loop stall detector (heartbeat background)
5. Process circuit breaker (graceful restart si N stalls/hour)

**HARDENING CONTRA 3 (Memory) — 6 capas:**
1. Weak references (WeakValueDictionary registries)
2. Resource bounds declarativos (maxsize + TTL forzado)
3. Memory metrics realtime (tracemalloc + psutil + Prometheus)
4. RSS threshold alert (2GB warn, 4GB critical)
5. Restart preventivo (10k req OR 24h OR 3GB RSS)
6. Leak forensics automático (snapshot diff pre/post)

Overhead total: ~5% runtime aceptable vs riesgo runaway

### 5.3.3 — Inter-Agent Communication: asyncio.Queue + broadcast
- `MultiAgentMessageBus` per batch:
  - hub_inbox (Queue maxsize 1000)
  - specialist_inboxes (dict[name, Queue maxsize 100])
  - broadcast_event + payload
  - status_callbacks (push-on-update)
- **4 patrones:**
  - SPECIALIST → HUB (progress/result/error)
  - HUB → SPECIALIST (cancel/extra_context)
  - SPECIALIST → SPECIALIST (peer ask_peer correlation_id)
  - HUB → ALL (broadcast mode_change/cancel)
- **10 message types Pydantic** v1
- Rate limit 50 msg/sec per specialist
- Critical_finding override (drops oldest)
- Compatible 5.3.2 ContextVar isolation

### 5.3.4 — Sub-Agent Cost Control: 7 layers
1. **PRE-FLIGHT CHECK** (estimate × 1.3 buffer)
2. **PER-SPECIALIST BUDGET** (max_tokens 10k, max_calls 20)
3. **REAL-TIME MONITORING** (background 500ms check)
4. **CIRCUIT BREAKER** (cap_ratio > 0.95 → emergency abort)
5. **PARTIAL RESULTS RESCUE** (salvar trabajo aborted)
6. **CLIENT VISIBILITY STREAM** (SSE R3 B3)
7. **WORKSPACE ISOLATION** (multi-agent budget 30% cap P5)

Pilot Light protected verdaderamente.

---

## 7. Resumen ejecutivo Bloque 4 — DMN / Default Mode Network

**Materializa: Grafo Maestro Nodo 6 DMN**

### 5.4.1 — Idle Detection + DMN Scheduling: C híbrido
- `DMNScheduler` singleton background (check 60s)
- MAX_CONCURRENT_DMN_TASKS = 5 global cap
- **6 signals collect candidates:**
  1. idle_seconds > threshold (default 300s)
  2. active_requests == 0
  3. cost_ratio < dmn_cost_threshold (default 0.7)
  4. neuromod_mode != HIGH_ATTENTION
  5. workspace.dmn_enabled (cliente toggle)
  6. cooldown elapsed (default 30 min)
- **Priority scoring:**
  - idle accumulated (max 10 pts)
  - cost safety (max 5 pts)
  - tier (enterprise +5, pilot -3)
  - CONSOLIDATION neuromod boost (+3)
  - local night hours boost (+4)

### 5.4.2 — DMN Tasks Declarativas: 8 tasks ⚠️ REFINAMIENTO PENDIENTE
**Grafo Maestro LITERAL (3):**
1. memory_consolidation (R2 4.4 CLS)
2. pattern_detection ("3 PRs similares")
3. hypothesis_generation ("módulo va a romper")

**Grafo Maestro IMPLÍCITO (5):**
4. prompt_improvement (eval scores bajos)
5. routing_learning (feed 5.2.2 history-aware)
6. cache_prewarming (5.2.3 layer E)
7. embedding_precompute (R2 B2 batch pending)
8. eval_regression_detection (R3 4.4 weekly)

`DMNTaskDefinition` Pydantic + `DMNTaskExecutor` con budget per run ($1 default).

> **⚠️ NOTA CRÍTICA:** Brian marcó 5.4.2 para refinamiento profundo posterior. Ver §11.

### 5.4.3 — DMN Budget + Cliente Controls: 9 controles
1. TOGGLE GLOBAL (`workspace.dmn_enabled`)
2. TOGGLE PER TASK (8 flags)
3. BUDGET PER RUN ($1 default)
4. BUDGET MENSUAL (10% cap P5 / 20% enterprise)
5. HORARIO PERMITIDO (allowed_hours + allowed_days)
6. COST GATE (cap P5 threshold 0.7)
7. ALARMAS (50%/75%/90%/100% thresholds)
8. DASHBOARD (4 API endpoints + UI v2)
9. APROBACIÓN OUTPUTS (auto_apply + risk categories)

**Risk categories outputs:**
- LOW (auto-apply OK): embed, routing, cache
- MEDIUM (review recomendado): consol, pattern, regression
- HIGH (review obligatorio): hypothesis, prompt

Compliance B2B: SOC2 path verdadero.

---

## 8. Cobertura del Grafo Maestro

**Nodos cerebrales materializados post-R5:**

| Nodo | Nombre | Status post-R5 | Round |
|---|---|---|---|
| 1 | Workspace Gate | ⚠️ Parcial (R4 4.1.3 KEK) | R9 completar |
| 2 | PFC (Prefrontal Cortex) | ⚠️ Parcial (R3 LLM Layer) | R6 completar |
| 3 | Hipocampo | ✅ Completo | R2 |
| 4 | Knowledge Graph | ✅ Completo | R2 |
| 5 | Microglía | ✅ Completo | R2 |
| **6** | **DMN** | ✅ **Completo (R5 B4)** | **R5** |
| 7 | Amígdala | ⏳ Defer | R9 Security |
| **8** | **Tálamo** | ✅ **Completo (R5 B1)** | **R5** |
| **9** | **Dual-Process Check** | ✅ **Completo (R5 B2)** | **R5** |
| 10 | Consolidación CLS | ✅ Completo | R2 |
| **11** | **Neuromoduladores** | ✅ **Completo (R5 B1.4)** | **R5** |

**Multi-Agent Network:** ✅ Completo (R5 B3)

**Edges Grafo Maestro materializadas R5:**
- E2: Workspace Gate → Tálamo (5.1.1+5.1.2)
- E3-E4: Tálamo → Amígdala/PFC (5.1.3 subgraph routing)
- E9-E11: Hipocampo/KG/GB → Multi-Agent (5.3.3 message bus)
- E12: Multi-Agent → Dual-Process (5.2.1)
- E13: Dual-Process → Confidence Check (5.2.2)
- E18: DMN ◄═► Todos los nodos cerebrales (5.4.2)
- E19: Neuromoduladores → Todos los nodos (5.1.4)

**Cobertura post-R5: 8/11 nodos completos + Multi-Agent + 7 edges principales.**

---

## 9. Costo total v1 actualizado post-R5

| Componente | Costo USD/mes |
|---|---|
| Subtotal R1+R2+R3+R4 v1 100% | ~$64-79/mes |
| R5 B1 Tálamo (Stella reused, cero LLM extra) | $0/mes |
| R5 B2 Dual-Process (history-aware ~$2/mes pgvector queries) | +$2/mes |
| R5 B3 Multi-Agent (overhead 5% LLM stack base) | +$3-5/mes |
| R5 B4 DMN (budget per run $1 × runs/día × 30) | +$5-10/mes |
| **TOTAL v1 FINAL post-R5** | **~$74-96/mes** |

**Verificación P2 <25%:**
- Pilot Light $3,500 → techo $875
- Consumo v1 (4 sem): ~$85
- **9.7% del techo → margen 90.3%** para R6-R10

**Verificación P5 cap LLM ($50-200/mes):**
- LLM total v1 FINAL post-R5: ~$73-90/mes
- **37-45% del cap → margen $110-127 escalado workspaces**

**Recursos servidor post-R5: ~5 GB RAM (de 30 GB disponibles)**
- R5 B3 hardening monitoring: +~50 MB
- R5 B4 DMN scheduler + tasks: +~100 MB
- R5 B1-B2 routing overhead: +~50 MB
- Total R5 overhead: ~200 MB

**Compliance v1 post-R5:**
- OWASP LLM Top 10
- SOC2 path verdadero (audit + retention + DMN controls)
- 18 capas defense-in-depth multi-agent
- 9 controles DMN granular B2B

---

## 10. Riesgos consolidados R5 + mitigaciones

| Riesgo | Capa | Mitigación |
|---|---|---|
| Tálamo routing pobre cold start | B1 | Defaults conservadores + telemetría |
| Context routing skip tier crítico | B1 | Workspace `always_include_tiers` override |
| Neuromod transitions thrash | B1 | Hysteresis 5min + audit transitions |
| Sistema 2 false negatives (S1 cuando debía S2) | B2 | Workspace `force_system_2` override + audit |
| History-aware cold start | B2 | Skip factor 6 si <5 datos + fallback factors 1-5 |
| Fast path stale cache | B2 | TTL workspace-configurable + invalidation event-driven |
| Multi-agent cross-specialist leak | B3 | 7 capas defense-in-depth (5.3.2 hardening) |
| Specialist blocking event loop | B3 | 5 capas + circuit breaker (5.3.2 contra 2) |
| Memory leaks acumulación | B3 | 6 capas + restart preventivo (5.3.2 contra 3) |
| Multi-agent runaway cost | B3 | 7 layers cost control (5.3.4) |
| DMN cap workspace overflow | B4 | 9 controles + 4 alarmas + auto-disable (5.4.3) |
| DMN tasks no aportan valor mensurable | B4 | ⚠️ refinamiento pendiente (eval criteria per task) |
| DMN cliente no entiende controles | B4 | Defaults sensatos + dashboard wizard |

---

## 11. Notas críticas pendientes

### ⚠️ 5.4.2 DMN Tasks — Refinamiento Detallado Pendiente

**Memoria global:** `project_dmn_tasks_critical_refinement.md` (creada 2026-06-06)

**Brian marcó verbatim:** "GUARDA UNA NOTA MUY IMPORTANTE QUE DEFINIREMOS A DETALLE ESTE APARTADO DEJALO COMO COMPLETO PERO TENEMOS QUE PRESTAR MUCHA ATENCION"

**Por qué crítico:** DMN es núcleo del valor diferencial For3s OS. Sin refinamiento profundo, las 8 tasks pueden ser:
- Stubs sin implementación final
- Thresholds no calibrados
- Sin eval criteria por task
- Sin auto-improvement loop formalizado

**Plan refinamiento (antes de programar R5):**
1. Crear `work/Ronda_05_DMN_Tasks_Detailed.md` con:
   - Pseudocode completo por las 8 tasks
   - Schema input/output formal Pydantic
   - Trigger thresholds defendibles con razonamiento
   - Eval criteria valor per task (ROI medible)
   - Interaction graph entre tasks
   - Auto-improvement loop end-to-end (DMN → review queue → approve → producción)
   - Cost ROI per task (estimated vs medido real)
2. Foundation Meta-Orchestrator (Grafo Maestro §6) defer R10+

---

## 12. Próximos pasos R6

R6 — Memory Stack Extensions (planeado):
- Nodo 2 PFC completar (R3 parcial)
- Knowledge Graph schema avanzado (edges semánticas)
- Hipocampo time-aware queries
- Forgetting policies refined (más allá decay R2)
- Memory observability dashboard
- Eval framework memory (regresión)

R7 — Frontend / Channel (planeado):
- Dashboard cliente (UI 9 controles DMN)
- Telegram adapter producción (R4 4.2.4 reused)
- API REST completo

R8 — Observability completa:
- Prometheus metrics R3 B4 expand
- Audit log retention policies
- Alarms multi-channel

R9 — Security / Compliance:
- Nodo 1 Workspace Gate completar
- Nodo 7 Amígdala (security primitive)
- SOC2 evidence collection

R10 — CI/CD / Deploy:
- GitHub Actions R4 B3 expand
- Multi-env (dev/staging/prod)
- Blue-green deploy
- Foundation Meta-Orchestrator

**Programación arranca post-R9 o R10 (per instrucción Brian).**

---

**R5 ✅ CERRADO 100% — Foundation cognitiva coordinada lista para R6+.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_05_Orchestration_Multi_Agent.md`).
