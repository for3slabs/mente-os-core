# Ronda 6 — Memory Stack Extensions (Master)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_06_Memory_Stack_Extensions.md → work/Ronda_06_Memory_Stack_Extensions.md (2026-07-30, ADR-029)

## Purpose

Ronda 6 — Memory Stack Extensions (Master)


**Sexta de las 10 rondas técnicas. Documento maestro de R6.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-07
**Última actualización:** 2026-06-07
**Estatus:** ✅ **R6 CERRADO 100%** (4 bloques · 13/13 sub-temas LOCKED)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — §4 Nodos 2, 3, 4, 5 + §8 Pilar 3 Autonomía Generativa
- [Mente/work/Ronda_05_Orchestration_Multi_Agent.md](work/Ronda_05_Orchestration_Multi_Agent.md) — R5 100% CERRADO
- [Mente/work/Ronda_04_Tools_MCP_Layer.md](work/Ronda_04_Tools_MCP_Layer.md) — R4 v1 100% CERRADO
- [Mente/memory/Estado_Sesion_Continuidad.md](../memory/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Sub-documentos detallados:**
- ✅ [Ronda_06_Bloque_1_PFC_Orchestrator.md](work/Ronda_06_Bloque_1_PFC_Orchestrator.md) — PFC Orchestrator Completo (4/4 LOCKED)
- ✅ [Ronda_06_Bloque_2_Ganglios_Basales_Skills.md](work/Ronda_06_Bloque_2_Ganglios_Basales_Skills.md) — Ganglios Basales / Skills (5/5 LOCKED) ⭐ CORE Pilar 3
- ✅ [Ronda_06_Bloque_3_Memory_Extensions.md](work/Ronda_06_Bloque_3_Memory_Extensions.md) — Memory Extensions Transversales (3/3 LOCKED)
- ✅ [Ronda_06_Bloque_4_Memory_Eval.md](work/Ronda_06_Bloque_4_Memory_Eval.md) — Memory Eval & Regression (1/1 LOCKED) ⭐ CIERRA R6

**Decisiones loggeadas en for3s-inter:**
- [D-023 — Stack PFC Orchestrator Completo LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-024 — Stack Ganglios Basales / Skills LOCKED + Pilar 3 ACTIVADO](../../for3s-inter/07-operations/decision-log.md)
- [D-025 — Stack Memory Extensions Transversales LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-026 — Stack Memory Eval & Regression LOCKED + R6 100% CERRADO](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core
- 3.D — Equipo pequeño (preferir simplicidad operacional)

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes
- P3 — Workspace isolation
- P4 — Encryption at rest

**⚠️ FLAG GLOBAL CRÍTICO:** `project_r6_critical_pre_code_review.md` — TODO R6 requiere replanificación detallada ANTES de programar (Brian marcó "EXTREMANDAMENTE IMPORTANTE").

---

## Tabla de contenidos

1. [Propósito de R6](#1-propósito-de-r6)
2. [Pre-preguntas P1-P3 LOCKED](#2-pre-preguntas-p1-p3-locked)
3. [Estructura B+A — 4 bloques · 13 sub-temas](#3-estructura-ba--4-bloques--13-sub-temas)
4. [Resumen ejecutivo Bloque 1 — PFC Orchestrator](#4-resumen-ejecutivo-bloque-1)
5. [Resumen ejecutivo Bloque 2 — Ganglios Basales / Skills](#5-resumen-ejecutivo-bloque-2)
6. [Resumen ejecutivo Bloque 3 — Memory Extensions](#6-resumen-ejecutivo-bloque-3)
7. [Resumen ejecutivo Bloque 4 — Memory Eval](#7-resumen-ejecutivo-bloque-4)
8. [Cobertura del Grafo Maestro](#8-cobertura-del-grafo-maestro)
9. [Pilar 3 Autonomía Generativa ACTIVADO](#9-pilar-3-autonomía-generativa-activado)
10. [Costo total v1 actualizado post-R6](#10-costo-total-v1-actualizado-post-r6)
11. [Riesgos consolidados R6 + mitigaciones](#11-riesgos-consolidados)
12. [Notas críticas pendientes](#12-notas-críticas)
13. [Próximos pasos R7](#13-próximos-pasos)

---

## 1. Propósito de R6

R6 — Memory Stack Extensions es la **capa de aprendizaje y autonomía** de For3s OS. Las rondas anteriores construyeron:

- **R1-R4:** Substrate (lenguaje, memoria, LLM, tools)
- **R5:** Orquestación cognitiva (Tálamo + Dual-Process + Multi-Agent + DMN)

**R6 responde:** ¿cómo APRENDE el sistema y MEJORA con experiencia?

R6 materializa:
- **Nodo 3 PFC** completo (planning + metacognición + confidence + skill bridge)
- **Nodo 4 Ganglios Basales / Skills** NUEVO 100% (GO/NO-GO + dopaminergic + lifecycle)
- **Nodo 2 Hipocampo** extendido (time-aware queries)
- **Nodo 5 Microglía** extendido (forgetting policies refined + GDPR)
- **Memory observability** (dashboard + regression detection)

**Sin R6, For3s OS es un wrapper Claude reactivo. Con R6, es un sistema cognitivo que aprende autónomamente (Pilar 3).**

---

## 2. Pre-preguntas P1-P3 LOCKED

| # | Pregunta | Decisión | Justificación |
|---|---|---|---|
| **P1** | Skill schema | **C+A — Híbrido enriquecido** (metadata Pydantic + markdown body filesystem archivos físicos) | Brian audita visualmente + LLM consumable + DB indexable |
| **P2** | Skill promotion | **A+C+B — Triple combinada** (auto WS + Brian core + cliente flexibility + threshold notification) | Brian SIEMPRE control final + ayuda sistema + flexibilidad cliente |
| **P3** | Skills cross-workspace | **B — Stack común opt-in** (workspace.contribute_to_common_stack default False) | Compliance B2B + escalabilidad |

---

## 3. Estructura B+A — 4 bloques · 13 sub-temas

```
BLOQUE 1 — PFC ORCHESTRATOR COMPLETO (Nodo 3)
   6.1.1 ✅ Planning Framework (C — Plan-then-execute con Claude)
   6.1.2 ✅ Confidence Scoring (C — Multi-signal 8 signals)
   6.1.3 ✅ Confidence Check Loop (C — Estratificado severity + partial re-plan)
   6.1.4 ✅ Plan → Skill Promotion (C — 7 fases lifecycle Grafo Maestro)

BLOQUE 2 — GANGLIOS BASALES / SKILLS (Nodo 4) ⭐ NÚCLEO PILAR 3
   6.2.1 ✅ Skill Schema (C — Híbrido FS + Postgres + pgvector)
   6.2.2 ✅ Vía GO (C — Plan-template + checkpoint validation)
   6.2.3 ✅ Vía NO-GO (C — 3-niveles HARD/SOFT/WARN)
   6.2.4 ✅ Dopaminergic Scoring (C — Multi-signal TD-learning 7 signals)
   6.2.5 ✅ Skill Lifecycle Operations (C — Manager + state machine + APIs)

BLOQUE 3 — MEMORY EXTENSIONS TRANSVERSALES
   6.3.1 ✅ Time-aware Queries (C — DSL completo semantic+temporal+agg)
   6.3.2 ✅ Forgetting Policies Refined (C — Multi-dim + GDPR + custom rules)
   6.3.3 ✅ Memory Observability Dashboard (C — HTMX completo + actions)

BLOQUE 4 — MEMORY EVAL & REGRESSION
   6.4.1 ✅ Memory Regression Detection (C — Multi-layer 4 layers)

TOTAL R6: 4 bloques · 13 sub-temas · 13/13 LOCKED ✅
```

---

## 4. Resumen ejecutivo Bloque 1 — PFC Orchestrator Completo

**Materializa: Grafo Maestro Nodo 3 PFC verdadero v1**

### 6.1.1 — Planning Framework: Plan-then-execute
- PFC genera `PFCPlan` Pydantic estructurado ANTES de ejecutar
- Skip planning si `subgraph == MINIMUM` (cost optimization)
- Hooks: 6.1.2 confidence + 6.1.3 re-plan + 6.1.4 skill promotion
- Audit: `pfc_plan_generated`, `pfc_plan_step_*`, `pfc_plan_completed`
- Schema: `PFCPlan` con `steps[]`, `estimated_cost/duration`, `confidence`, `risks[]`, `promotion_candidate_pattern`

### 6.1.2 — Confidence Scoring: 8 signals
- **8 signals + weights:**
  - llm_self_report (1.0)
  - tool_success (2.0)
  - schema_valid (2.5)
  - cost_accuracy (1.5)
  - plan_consistency (2.0)
  - multi_agent_consensus (3.0)
  - historical (2.5)
  - rule_eval (3.0)
- 5 niveles: HIGH/MED_HIGH/MEDIUM/LOW/CRITICAL
- Reusa R3 4.4 eval + R5 5.3.3 multi-agent consensus

### 6.1.3 — Confidence Check Loop: Estratificado
- Decision matrix por severity:
  - CRITICAL → HUMAN_ESCALATE | ABORT_GRACEFUL
  - LOW → RE_PLAN_PARTIAL (if budget ok)
  - CHECKPOINT + <0.7 → RE_PLAN_PARTIAL obligatorio
  - MEDIUM → CONTINUE_WITH_MONITORING
- Bounds: MAX_RE_PLANS 2, RE_PLAN_COST_BUDGET 30%
- `PartialRePlanner` preserva completed_steps exitosos

### 6.1.4 — Plan → Skill Promotion: 7 fases Grafo Maestro
- **7 fases lifecycle §8.2 Grafo Maestro:**
  1. DETECTION (DMN scheduled)
  2. PROPUESTA (LLM genera SkillSpec)
  3. SANDBOX (7 días aislado shadow mode)
  4. EVALUACIÓN (≥5 runs → PASS/MARGINAL/FAIL)
  5. PROMOCIÓN (3 tiers: workspace auto / core Brian / common opt-in)
  6. VIDA ÚTIL (skill activa)
  7. DECLIVE (microglía detecta uso bajo)
- Match P1+P2+P3 R6 LOCKED

---

## 5. Resumen ejecutivo Bloque 2 — Ganglios Basales / Skills ⭐

**Materializa: Grafo Maestro Nodo 4 + Pilar 3 Autonomía Generativa**

### 6.2.1 — Skill Schema: Híbrido FS + Postgres + pgvector
- **Source-of-truth:** archivo `.md` filesystem (Brian audita visualmente)
- **Postgres mirror:** metadata + embeddings + scoring
- **SHA256 integrity check**
- **RLS workspace isolation** (5.3.2 pattern reused)
- **HNSW indexes:** `intent_embedding` + `body_embedding`
- **3-layer isolation:** filesystem path + Postgres RLS + common stack policy
- File format: YAML frontmatter Pydantic + markdown body

### 6.2.2 — Vía GO: Plan-template + checkpoint validation
- `SkillApplicationEngine` 9-step pipeline
- **Cost saving real:** ~$0.05 per skill applied (no LLM planning)
- Precedence: workspace > core > common stack
- Threshold similarity ≥ trigger_confidence_threshold (default 0.85)
- NO-GO interference check (6.2.3 hook)
- Fallback gracioso a PFC planning si match débil
- Plan compatible mismo schema 6.1.1 (`source_skill_id` NEW field)

### 6.2.3 — Vía NO-GO: 3-niveles HARD/SOFT/WARN
- **HARD_BLOCK:** imposible bypass (compliance §8.4)
- **SOFT_BLOCK:** bypass via workspace setting + human-in-loop + audit reason
- **WARN:** audit + continue
- **4 generation sources:** DMN auto + cliente manual + Brian core + common stack
- Integration points: planning (6.1.1) + skill apply (6.2.2) + runtime + multi-agent spawn
- Hardcoded HARD_BLOCK foundation §8.4:
  - cross_workspace_data_access
  - unsandboxed_code_execution
  - customer_data_without_optin

### 6.2.4 — Dopaminergic Scoring: TD-learning 7 signals
- **7 signals + weights:**
  - reward (0.30)
  - prediction_error TD (0.15)
  - recency decay (0.10)
  - context per (ws, subgraph_mode) (implícito)
  - cost_efficiency (0.20)
  - confidence_avg rolling (0.15)
  - consistency variance (0.10)
- Smooth update: new = 0.3 × weighted + 0.7 × old
- Auto lifecycle triggers:
  - Score ≥8.5 + rewards ≥50 → core promotion notification (P2 A+B)
  - Score <3.0 + punishments ≥5 → mark DECLINING
  - 5 failures consecutivos GO → propose NO-GO skill (§8.1 #1)

### 6.2.5 — Skill Lifecycle Operations: Manager + state machine
- **State machine 8 states** + valid transitions enforced
- **Atomic write protocol:** Postgres advisory lock (cross-worker) + 2PC filesystem+DB + SHA verify
- **Versioning:** SemVer bump + inherit score × 0.9 + cutover graceful
- **Microglía skill scan:** cron daily 3 AM (DECLINING >30d → archive)
- **Sandbox execution shadow mode** (Fase 3 hook 6.1.4)
- **Admin API Brian:** approve_core, approve_no_go, archive, override_score
- **Cliente API self-service:** list, toggle, feedback, settings

---

## 6. Resumen ejecutivo Bloque 3 — Memory Extensions

### 6.3.1 — Time-aware Queries: DSL completo
- `TemporalQuery` Pydantic rico:
  - semantic_query + semantic_top_k
  - time_window (absolute o relative_to_now '-30d')
  - relative_to_event (before/after/around)
  - aggregate (count/sum/avg/trend/compare)
  - output ('episodes' | 'aggregated' | 'trend')
- `TemporalQueryBuilder` SQL dinámico safe (parameter binding)
- **Performance targets:** range <50ms, semantic+temporal <100ms, agg <200ms
- Hooks: DMN 5.4.2 pattern_detection + 6.3.3 dashboard + 6.2.4 skill ROI

### 6.3.2 — Forgetting Policies Refined: Multi-dim + GDPR
- **5-layer policy hierarchy:** custom rules > legal hold > data type overrides > tier multipliers > defaults
- **10 data types:** episodes (general/decision/audit/pii), kg_fact, skill_metadata/body, pfc_plan, llm_audit_log, conversation
- **Tier multipliers:** pilot_light 0.5×, standard 1×, enterprise 2-5×
- **10 forgetting decisions:** RETAIN/REVIEW/ARCHIVE/REDACT_PII/PURGE + variants
- **GDPR workflow:** automatic | manual_review + right-to-be-forgotten
- **Legal hold + PII redact + cascade strategies**
- Microglía extended cron daily 3 AM
- Cliente APIs self-service

### 6.3.3 — Memory Observability Dashboard: HTMX completo
- Stack: Jinja2 + HTMX (R3 B4) + Tailwind + Chart.js
- **Cliente dashboard 10 sections:** memory, skills, plans, forgetting, dmn, cost, eval, audit, settings, overview
- **Brian admin dashboard 5 sections:** workspaces, system, skills_approval, gdpr_requests, security_events
- **Actions 1-click HTMX:** approvals, toggles, GDPR submit, legal hold
- **Real-time HTMX SSE updates:** cost, skill_promoted, dmn_run_completed
- **Compliance exports:** CSV/JSON/PDF
- Foundation R7 Frontend natural

---

## 7. Resumen ejecutivo Bloque 4 — Memory Eval & Regression

### 6.4.1 — Memory Regression Detection: 4 layers
- **Daily health scan cron 4 AM** (post-microglía 3 AM)
- **LAYER 1 — Golden Retrieval Tests (40%):** auto-bootstrap golden set, recall/precision/F1, regression si F1 drops >10%
- **LAYER 2 — Canary Queries (30%):** 7 canaries (workspace boundary CRITICAL, kg facts source HIGH, recent episodes HIGH, skills queryable MEDIUM, embeddings dimensions CRITICAL, audit integrity CRITICAL, forgetting compliance HIGH)
- **LAYER 3 — Trend Analysis (20%):** 12 metrics tracked, 7d vs 30d baseline, direction-aware
- **LAYER 4 — DMN Efficacy (10%):** per task applied_rate, low efficacy → propose disable
- **Aggregate health score 0-100:** L1×0.40 + L2×0.30 + L3×0.20 + L4×0.10
- **Alert tiers:** CRITICAL canary → Brian inmediato, <60 → Brian, <70 → cliente
- **Auto-actions:** propose disable DMN task, propose re-embedding Stella, SECURITY emergency cross-workspace

---

## 8. Cobertura del Grafo Maestro

**Nodos cerebrales materializados post-R6:**

| Nodo | Nombre | Status post-R6 | Round |
|---|---|---|---|
| 1 | Knowledge Graph | ✅ Completo | R2 |
| **2** | **Hipocampo** | ✅ **Extendido** (R2 + R6 6.3.1 time-aware) | R2 + R6 |
| **3** | **PFC / Orchestrator** | ✅ **COMPLETO 100%** (R3 + R5 + R6 B1) ⭐ | R3+R5+R6 |
| **4** | **Ganglios Basales / Skills** | ✅ **COMPLETO 100% NUEVO** (R6 B2) ⭐⭐ | R6 |
| **5** | **Microglía** | ✅ **Extendido** (R2 + R6 6.3.2 forgetting refined) | R2 + R6 |
| 6 | DMN | ✅ Completo | R5 |
| 7 | Amígdala | ⏳ Defer R9 Security | R9 |
| 8 | Tálamo | ✅ Completo | R5 |
| 9 | Dual-Process Check | ✅ Completo | R5 |
| 10 | Consolidación CLS | ✅ Completo | R2 |
| 11 | Neuromoduladores | ✅ Completo | R5 |

**Coverage post-R6: 10/11 nodos COMPLETOS (solo Amígdala R9 pending)**

---

## 9. Pilar 3 Autonomía Generativa ACTIVADO ⭐⭐⭐

Grafo Maestro §8 Pilar 3 — 4 capacidades generativas:

| Capacidad | Status post-R6 |
|---|---|
| **1. Generar skills nuevas (Ganglios Basales)** | ✅ **ACTIVO** (R6 B2 completo) |
| 2. Generar nuevos tipos de relaciones (KG) | ⏳ v3+ |
| 3. Generar sub-agentes especializados (Multi-Agent) | ⏳ v2 (R5 B3 foundation) |
| 4. Generar nuevos modos globales (Neuromoduladores) | ⏳ v3+ |

**Capacidad #1 — Skills:**
- ✅ Plans exitosos → SkillCandidate (6.1.4 Fase 1)
- ✅ LLM genera SkillSpec (6.1.4 Fase 2)
- ✅ Sandbox isolation (6.1.4 Fase 3 + 6.2.5)
- ✅ Evaluación PASS/MARGINAL/FAIL (6.1.4 Fase 4)
- ✅ Promoción 3-tier (6.1.4 Fase 5 + P2 A+C+B)
- ✅ Vida útil con dopaminergic scoring (6.2.4)
- ✅ Auto-decline + microglía archive (6.1.4 Fase 7 + 6.2.5)
- ✅ Auto NO-GO from failures (6.2.4)

**Esto es lo que NO existe en NINGÚN agente actual** (Grafo Maestro Pilar 3).

---

## 10. Costo total v1 actualizado post-R6

| Componente | Costo USD/mes |
|---|---|
| Subtotal R1+R2+R3+R4 v1+R5 100% | ~$74-96/mes |
| R6 B1 PFC planning (LLM calls Sonnet planning) | +$3-5/mes |
| R6 B2 Skills (storage + Dopaminergic scoring async) | +$0 infra +$1 dopaminergic LLM occasional |
| R6 B3 Memory extensions (queries + dashboard + forgetting) | +$0 (reused) |
| R6 B4 Memory eval (Haiku para LLM-judge regression) | +$2-3/mes |
| **TOTAL v1 FINAL post-R6** | **~$80-105/mes** |

**Verificación P2 <25%:**
- Pilot Light $3,500 → techo $875
- Consumo v1 (4 sem): ~$92
- **10.5% del techo → margen 89.5%** para R7-R10

**Verificación P5 cap LLM ($50-200/mes):**
- LLM total v1 FINAL post-R6: ~$79-99/mes
- **40-50% del cap → margen $100-120 escalado workspaces**

**Recursos servidor post-R6: ~5.5 GB RAM (de 30 GB disponibles)**
- R6 B2 skills filesystem: ~50 MB (1000 skills × ~50 KB markdown)
- R6 B3 dashboard: ~50 MB
- R6 monitoring: ~50 MB

**Compliance v1 post-R6:**
- OWASP LLM Top 10
- SOC2 path real (audit + retention + GDPR + 9 DMN controls + 5-layer forgetting hierarchy)
- 18 capas defense-in-depth multi-agent (R5)
- 9 controles DMN granular B2B (R5)
- GDPR full workflow (R6 6.3.2)
- Legal hold + PII redact + cascade (R6 6.3.2)
- 7 canaries health monitoring (R6 6.4.1)

---

## 11. Riesgos consolidados R6 + mitigaciones

| Riesgo | Capa | Mitigación |
|---|---|---|
| PFC planning añade latencia (~2-5s) | B1 | Skip si subgraph MINIMUM |
| Confidence signals mal calibrados | B1 | ⚠️ flag pre-código + tunable workspace |
| Re-plan loop infinito | B1 | MAX_RE_PLANS 2 + cost budget 30% |
| Skill schema rígido vs LLM creativo | B2 | YAML frontmatter validado Pydantic + markdown body libre |
| Skills proliferación sin control | B2 | 7 fases lifecycle + sandbox eval obligatoria |
| NO-GO bypass abuse | B2 | 3 gates (workspace setting + h-i-l + audit reason) |
| Dopaminergic scoring inestable | B2 | Smoothing factor 0.3 + 7 signals balanced |
| Concurrent skill writes corruption | B2 | Postgres advisory locks cross-worker |
| Temporal queries performance | B3 | Indexes compuestos + HNSW pgvector reused |
| Forgetting agresiva pierde data importante | B3 | 5-layer hierarchy + importance scoring |
| GDPR mal implementado compliance fail | B3 | Workflow automatic | manual + legal hold + audit defendible |
| Dashboard cliente confunde | B3 | Defaults sensatos + UX wizard + helper tooltips |
| Memory regression undetected | B4 | 4 layers defense + 7 canaries + 12 metrics + DMN feedback |
| Golden tests stale | B4 | Auto-bootstrap + workspace puede curate |
| False positive alerts fatigue | B4 | Aggregate daily digest vs per-event |

---

## 12. Notas críticas pendientes

### ⚠️ TODO R6 — Re-revisión profunda pre-código

**Memoria global:** `project_r6_critical_pre_code_review.md`

**Brian quote verbatim (2026-06-07):**
> "NOTA IMPORTANTE VOLVER A REVISAR Y PLANIFICAR CUANDO ESTEMOS REALIZANDO CODIGO TODO EL R6 POR QUE ES UN R EXTREMANDAMENTE IMPORTANTE"

**Plan re-revisión ANTES de programar R6:**

Crear `work/Ronda_06_Pre_Code_Review_Detailed.md` con:

1. **Por cada sub-tema lockeado:**
   - Pseudocode completo de cada función crítica
   - Schema Pydantic formal input/output
   - Trigger thresholds calibrados con razonamiento
   - Failure modes + recovery strategies
   - Interaction graph con otras decisiones R5/R6
   - Eval criteria valor per decisión (ROI medible)
   - Cost ROI estimado vs medido (post-producción)

2. **Específicamente para R6 B2 (Skills):**
   - Skill file format STRICT spec (YAML frontmatter + markdown sections)
   - Directorio físico structure (workspace_id, common_stack, _archive)
   - Indexing strategy pgvector (intent + body separate)
   - Lifecycle states + transitions reglas + audit
   - Dopaminergic scoring formula explícita (pesos calibrados)

3. **Específicamente para PFC (R6 B1):**
   - Plan schema completo Pydantic todos los campos
   - Re-plan trigger conditions + max iterations bound
   - Confidence signals calibración casos reales wedge QA
   - Hook points exactos intercept ejecución

### ⚠️ 5.4.2 DMN Tasks Refinamiento (carryover R5)

Memory global: `project_dmn_tasks_critical_refinement.md`

R6 6.1.4 + 6.2.4 + 6.4.1 integran con DMN tasks 5.4.2 — refinamiento DMN debe coordinarse con refinamiento R6.

---

## 13. Próximos pasos R7

R7 — Frontend / Channel (planeado):
- Dashboard cliente expansion (6.3.3 v2)
- Telegram adapter producción (R4 4.2.4 reused)
- API REST completo
- WebSocket support
- Mobile app foundation (defer v3+)

R8 — Observability completa:
- Prometheus metrics R3 B4 + R5 + R6 expand
- Grafana dashboards (Brian internal)
- Audit log retention policies
- Alarms multi-channel

R9 — Security / Compliance:
- Nodo 7 Amígdala (último nodo Grafo Maestro)
- SOC2 evidence collection
- Penetration testing
- Compliance audit reports

R10 — CI/CD / Deploy:
- GitHub Actions R4 B3 expand
- Multi-env (dev/staging/prod)
- Blue-green deploy
- Foundation Meta-Orchestrator (Pilar 3 capacidades 2+3+4)

**Programación arranca post-R9 o R10 (per instrucción Brian) + re-revisión R6 obligatoria.**

---

**R6 ✅ CERRADO 100% — Foundation Pilar 3 Autonomía Generativa ACTIVADO ⭐⭐⭐**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_06_Memory_Stack_Extensions.md`).
