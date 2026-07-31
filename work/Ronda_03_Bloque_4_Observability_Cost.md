# Ronda 3 — Bloque 4: Observabilidad & Costo LLM

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_03_Bloque_4_Observability_Cost.md → work/Ronda_03_Bloque_4_Observability_Cost.md (2026-07-30, ADR-029)

## Purpose

Ronda 3 — Bloque 4: Observabilidad & Costo LLM


**Sub-documento detallado de R3 — Model/LLM Layer. Bloque 4 de 4 (CIERRA R3).**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-03
**Estatus:** ✅ LOCKED (3/3 sub-temas) — **CIERRA R3 100%**
**Modo de debate:** B+A (bloque + sub-tema por sub-tema con profundidad R2)
**Documento padre:** [Ronda_03_Model_LLM_Layer.md](work/Ronda_03_Model_LLM_Layer.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (SDKs abiertos)
- 3.D — Equipo pequeño

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P5 — Budget LLM USD 50-200/mes

**Dependencias resueltas en B1 + B2 + B3:**
- ✅ LLM provider abstraction + tiers per workspace (B1)
- ✅ ContextBuilder + Cache + ToolRegistry (B2)
- ✅ Streaming SSE + Token Bucket + Resilience (B3)
- ✅ CapacityLimiter + Valkey + asyncio + anyio (R2 B3)
- ✅ audit_events chain + Arq cron + Postgres (R2 B1+B3)

**Fuente de verdad:**
- [`For3s_OS_Grafo_Maestro.md`](../Cerebro/For3s_OS_Grafo_Maestro.md) §4 Nodo 3 PFC + Pilar 1 + Pilar 2 + Pilar 3

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 3.4.1 — LLM observability](#3-sub-tema-341--llm-observability)
4. [Sub-tema 3.4.2 — Cost monitoring per workspace](#4-sub-tema-342--cost-monitoring-per-workspace)
5. [Sub-tema 3.4.3 — LLM quality evaluation](#5-sub-tema-343--llm-quality-evaluation)
6. [Stack final consolidado](#6-stack-final-consolidado)
7. [Cobertura del Grafo Maestro post-R3](#7-cobertura-del-grafo-maestro-post-r3)
8. [Costo total post-R3 100%](#8-costo-total-post-r3-100)
9. [Exploraciones futuras NO adoptadas v1](#9-exploraciones-futuras-no-adoptadas-v1)
10. [Implicaciones en rondas futuras](#10-implicaciones-en-rondas-futuras)
11. [Riesgos legítimos aceptados](#11-riesgos-legítimos-aceptados)
12. [Cierre R3 100% — síntesis final](#12-cierre-r3-100--síntesis-final)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 4 — OBSERVABILIDAD & COSTO LLM                        ║
║   3 sub-temas LOCKED el 2026-06-03                             ║
║   ⭐ CIERRA R3 100% (14/14 sub-temas, 4/4 bloques)              ║
║                                                                ║
║   3.4.1 LLM observability    → Audit chain + Prometheus LOCAL  ║
║   3.4.2 Cost monitoring       → Sistema completo (5 capacid.) ║
║   3.4.3 Quality evaluation    → Framework híbrido 4 capas      ║
║                                                                ║
║   Foundation cerrada para:                                      ║
║   • R4 Tools/MCP Layer                                          ║
║   • R5 Orchestration/Multi-Agent                                ║
║   • R6 Memory Stack extensions                                  ║
║   • R7 Frontend / Channel                                        ║
║   • R8 Observability completa (Grafana, alerting)                ║
║   • R9 Security / Compliance                                     ║
║   • R10 CI/CD / Deploy                                           ║
║                                                                ║
║   Costo incremental B4 R3:      ~+$5-15/mes (eval Haiku)        ║
║   Costo total v1 FINAL R3:       ~USD 62-77/mes                  ║
║   % techo Pilot Light:           6.3% (margen 93.7%)             ║
║   % cap P5 LLM:                  31-36% (margen $130-140)        ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Observability LLM-specific + cost monitoring + quality evaluation
no son features — son lo que separa 'wrapper Claude bonito' de
plataforma producción-ready B2B. Cada capa de B4 mitiga
debilidades de las anteriores con interdependencia coordinada."
```

Las 3 decisiones convergen en patrones consistentes:

```
1. OBSERVABILITY DUAL (3.4.1)
   → Audit chain Postgres (forensics 13 meses)
   → Prometheus time-series (operational 15 días)
   → Foundation R8 sin compromiso futuro

2. COST MONITORING COORDINADO (3.4.2)
   → 5 capacidades interdependientes
   → Hard cap (B3) + graduales (B4) + anomaly + forecast + reporting
   → UX enterprise B2B + foundation R10 billing

3. EVAL HÍBRIDO ANTI-SESGO (3.4.3)
   → 4 capas complementarias con cobertura ~95%
   → Cada capa mitiga debilidades de las otras
   → Defendible B2B + regresión auto

4. INTEGRACIÓN PROFUNDA CON B1+B2+B3
   → Reusa Arq cron, Jinja2 templates, Haiku, Valkey
   → No duplica abstracciones existentes
   → audit chain extendida, no reemplazada

5. FOUNDATION COMERCIAL REAL
   → Defendible en comité técnico enterprise B2B
   → Respuestas a las preguntas críticas que ChatGPT/Claude no tienen
   → Diferenciador venta sostenible
```

### Por qué esta filosofía importa

**Para Pilar 1 Seguridad:** anomaly detection = security primitive (key_leaked auto-suspend), eval safety dimension preserve compliance, audit chain inmutable forensics-ready.

**Para Pilar 2 Escalabilidad:** observability es prerequisito de escalar, cost predictability habilita pricing tiers maduros, eval automático detecta regresión en escala.

**Para Pilar 3 Autonomía:** agente debe poder "introspeccionarse" (métricas), gestionar su propio costo (anomaly + forecast), auto-evaluarse continuamente (eval framework).

---

## 3. Sub-tema 3.4.1 — LLM observability

### Decisión LOCKED

```
Audit chain Postgres (forensics) + Prometheus metrics exportados (operational)
```

### Contexto

Tienes ~60 métricas obligatorias dispersas en B1+B2+B3. Sin agregación = datos crudos sin contexto. Sin observability tiempo real = enterarse por reclamo cliente.

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** decisiones requieren métricas para tunear
- **Nodo 10 CLS:** consolidación usa métricas históricas
- **Nodo 11 Neuromoduladores:** "stress level" = métricas saturación
- **Pilar 1 Seguridad:** audit + observability = forensics
- **Pilar 2 Escalabilidad:** observability prerequisito escalar
- **Pilar 3 Autonomía:** agente introspectivo via métricas

### Candidatos evaluados

```
A) Solo audit chain Postgres (R2 B1 ya LOCKED)            ⚠️ Insuficiente solo
B) Audit chain + Prometheus metrics exportados             ✅ ELEGIDO
C) OpenTelemetry full stack                                 ❌ Premature, R8 territory
D) SaaS observability (Helicone/Langfuse)                  ❌ Viola P3 compliance
E) Custom dashboard FastAPI                                 ⚠️ Reinventa Prometheus
```

### Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│  FastAPI app                                              │
│  • prometheus_fastapi_instrumentator MIT                  │
│  • Custom metrics LLM-specific                            │
│  • /metrics endpoint (auth interno)                        │
└───────────────┬─────────────────────────────────────────┘
                │ scrape every 15s
                ▼
┌─────────────────────────────────────────────────────────┐
│  Prometheus (LOCAL servidor Brian)                        │
│  • Time-series DB                                          │
│  • Retención 15 días                                       │
│  • ~200 MB RAM, ~5 GB disco                                │
└───────────────┬─────────────────────────────────────────┘
                │ exporta a Grafana (R8 futuro)
                ▼
┌─────────────────────────────────────────────────────────┐
│  Grafana (R8 — futuro)                                    │
│  • Dashboards visuales                                     │
│  • Alerting rules                                          │
│  • All-system metrics                                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  audit_events Postgres (R2 B1 PRESERVED)                  │
│  • Forensics individual call                                │
│  • Inmutable chain                                          │
│  • Retención 13 meses                                       │
└─────────────────────────────────────────────────────────┘
```

### Métricas LLM-specific LOCKED v1 (~25 métricas)

```python
# Tokens
llm_input_tokens_total{workspace_id, model, provider}
llm_output_tokens_total{workspace_id, model, provider}
llm_cache_read_tokens_total{workspace_id, layer}
llm_cache_write_tokens_total{workspace_id, layer}

# Latency
llm_request_duration_seconds{workspace_id, model, provider}  # histogram
llm_ttft_seconds{workspace_id, model}                        # histogram
llm_tokens_per_second{workspace_id, model}

# Cost
llm_cost_usd_total{workspace_id, model, provider}
llm_cost_saved_caching_usd{workspace_id}

# Cache
llm_cache_hit_rate{workspace_id, layer}                       # gauge
llm_cache_ttl_renewals{workspace_id, layer}

# Concurrency (B3 3.3.2)
llm_concurrency_acquire_total{workspace_id, tier}
llm_concurrency_acquire_wait_seconds{workspace_id}            # histogram
llm_rate_limit_exceeded_total{workspace_id, dimension}
llm_anthropic_429_total{workspace_id}
token_bucket_rpm_remaining{workspace_id}                       # gauge
token_bucket_tpm_remaining{workspace_id}                       # gauge
capacity_limiter_in_flight                                     # gauge
capacity_limiter_queue_depth                                   # gauge

# Resilience (B3 3.3.3)
llm_retry_attempts_total{workspace_id, provider, error_type}
llm_retry_success_total{workspace_id, attempts_taken}
llm_fallback_activated_total{workspace_id, from, to}
circuit_breaker_state{provider}                                # gauge

# Tools (B2 3.2.4)
tool_execution_total{workspace_id, tool_name, status}
tool_execution_duration_seconds{tool_name}                     # histogram
tool_retry_total{tool_name, error_type}

# Streaming (B3 3.3.1)
stream_active_count{workspace_id}                              # gauge
stream_partial_total{workspace_id}
stream_cancelled_total{workspace_id}

# Quality (foundation 3.4.3)
llm_eval_score{workspace_id, eval_name}                        # gauge
```

### Wrapper LLMCallRecorder

```python
class LLMCallRecorder:
    """
    Registra cada LLM call atomicamente en:
    1. Prometheus metrics (tiempo real)
    2. audit_events Postgres (forensics)
    """
    async def record_llm_call(self, **params):
        # 1. Prometheus
        LLM_INPUT_TOKENS.labels(...).inc(params['input_tokens'])
        LLM_OUTPUT_TOKENS.labels(...).inc(params['output_tokens'])
        LLM_REQUEST_DURATION.labels(...).observe(params['duration_seconds'])
        # ...
        
        # 2. Audit
        await audit_logger.log(
            event_type='llm_call',
            payload=params,
        )
```

### Queries operacionales típicas (PromQL)

```promql
# Top 5 workspaces consumo 24h
topk(5, sum by (workspace_id) (
   increase(llm_input_tokens_total[24h]) +
   increase(llm_output_tokens_total[24h])
))

# Latencia p95 Sonnet vs Opus
histogram_quantile(0.95,
  rate(llm_request_duration_seconds_bucket{model=~"claude-sonnet|claude-opus"}[5m])
) by (model)

# Cache hit rate
llm_cache_read_tokens_total /
(llm_cache_read_tokens_total + llm_cache_write_tokens_total)

# % cap P5 actual
sum by (workspace_id) (
  increase(llm_cost_usd_total[30d])
) / 50 * 100
```

### Reglas duras LOCKED

```
✅ Prometheus LOCAL en mismo servidor Brian (no externalizado)
✅ Retención 15 días default (configurable)
✅ Scrape interval 15s
✅ Métricas LLM-specific LOCKED (~25 métricas)
✅ Audit chain PRESERVED (no reemplazado, complementado)
✅ /metrics endpoint protegido por auth interno
✅ Cardinality limit: ~1200 series max
✅ Label naming convention LOCKED
✅ Histogram buckets calibrados
✅ Wrapper LLMCallRecorder: audit + metrics atomic
✅ NO datos sensibles en labels (privacy)
✅ Foundation R8: Grafana consumirá
```

### Cost impact

```
Setup adicional:
   • Prometheus binary: $0
   • prometheus_fastapi_instrumentator: $0 (MIT)
   • prometheus_client: $0 (Apache)
   • Recursos: +200 MB RAM (30 GB disp), +5 GB disco (1 TB)
   
Costo recurring: $0
Costo tiempo Brian: 2-3 días setup
```

---

## 4. Sub-tema 3.4.2 — Cost monitoring per workspace

### Decisión LOCKED

```
Sistema completo (alarmas + dashboard + anomaly + forecast + reporting)
```

### Contexto

B3 3.3.2 ya cerró cap P5 enforcement (hard cap automático). Pero esto NO basta:
- Cliente sin warning = UX horrible
- Sin anomaly detection = enterarse 30 días tarde
- Sin forecast = reactivo no proactivo
- Sin dashboard cliente = support tickets Brian

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** decisiones costo afectan tier
- **Nodo 10 CLS:** consolidación usa cost histórico
- **Nodo 11 Neuromoduladores:** "ansiedad" = cap acercándose
- **Pilar 1 Seguridad:** anomaly = security primitive
- **Pilar 2 Escalabilidad:** cost predictability habilita pricing
- **P5 LOCKED:** cap operacional + alarmas graduales

### Candidatos evaluados

```
A) Solo hard cap B3 3.3.2 (sin alarmas)                       ❌ UX horrible
B) Alarmas graduales + dashboard Brian                          ⚠️ MVP no escala
C) Sistema completo (alarmas + dashboard + anomaly + forecast + reporting) ✅ ELEGIDO
D) Integración Stripe/Lago billing                              ❌ Premature R10
E) AI-powered FinOps automático                                  📚 Futuro v3
```

### Las 5 capacidades coordinadas

```
CAPACIDAD 1: ALARMAS GRADUALES
   • 50% cap → notificación informativa (email cliente + dashboard)
   • 75% cap → warning (email cliente + dashboard + Telegram Brian)
   • 90% cap → warning crítico (email cliente + Telegram Brian inmediato)
   • 100% cap → hard stop (B3 3.3.2 ya cubre)
   • Dedupe: 1 alarma por threshold por mes
   • Background job Arq cada 15 min

CAPACIDAD 2: DASHBOARD CLIENTE SELF-SERVICE
   • Endpoint /workspaces/{id}/cost-dashboard
   • Auth: workspace_id token
   • Métricas mostradas:
     - Cap actual + consumido + %
     - Días restantes
     - Forecast end-of-month
     - Breakdown por modelo (Sonnet/Opus/Haiku)
     - Cache savings
     - Tier actual + upgrade button
   • Renderizado: HTMX + Jinja2 (B2 3.2.1 reused)

CAPACIDAD 3: ANOMALY DETECTION (statistical)
   • Algoritmo 3-sigma sobre baseline 7d
   • 4 tipos clasificados:
     - spike_hour:        bug nuestro probable (loop?)
     - spike_sustained:   cliente growth → suggest upgrade
     - key_leaked:        AUTO-SUSPEND + alarma crítica
     - bug_loop:          notify Brian crítico
   • Background job Arq cada 5 min

CAPACIDAD 4: FORECAST end-of-month
   • Algoritmo: daily_avg × days_in_month
   • Refinamiento weekday/weekend
   • Mostrar dashboard con color:
     verde <75%, amarillo 75-90%, rojo >90%
   • Alarma si forecast >100% cap

CAPACIDAD 5: REPORTING recurring (Arq cron)
   • DAILY 9 AM digest Brian (Telegram)
   • WEEKLY Monday 9 AM digest clientes (email)
   • MONTHLY day 1 9 AM report clientes (email)
   • Templates Jinja2 (B2 3.2.1 reused)
```

### Esquemas SQL

```sql
ALTER TABLE shared.workspaces ADD COLUMN
    monthly_cap_usd NUMERIC(10,2) NOT NULL DEFAULT 50.00;

ALTER TABLE shared.workspaces ADD COLUMN
    alarm_thresholds_pct INTEGER[] NOT NULL DEFAULT ARRAY[50, 75, 90];

ALTER TABLE shared.workspaces ADD COLUMN
    notification_email TEXT;

CREATE TABLE shared.cost_alarms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES shared.workspaces(id),
    threshold_pct INTEGER NOT NULL,
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    cost_at_trigger NUMERIC(10,4) NOT NULL,
    cap_at_trigger NUMERIC(10,2) NOT NULL,
    channels_notified TEXT[] NOT NULL,
    month TEXT NOT NULL,
    audit_event_id UUID NOT NULL REFERENCES audit_events(id),
    UNIQUE (workspace_id, threshold_pct, month)
);

CREATE TABLE shared.cost_anomalies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES shared.workspaces(id),
    detected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    anomaly_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    baseline_value NUMERIC,
    observed_value NUMERIC,
    deviation_sigma NUMERIC,
    action_taken TEXT,
    audit_event_id UUID NOT NULL REFERENCES audit_events(id)
);
```

### Reglas duras LOCKED

```
✅ 3 thresholds graduales: 50%, 75%, 90% (+ 100% hard cap B3 3.3.2)
✅ Dedupe: 1 alarma por threshold por mes por workspace
✅ Notificaciones multi-canal: email + Telegram Brian
✅ Background jobs Arq:
   - 15 min: alarmas check
   - 5 min: anomaly detection
   - daily 9 AM: digest Brian
   - weekly Mon 9 AM: digest clientes
   - monthly day 1 9 AM: report clientes
✅ Dashboard endpoint con workspace_id auth (no admin)
✅ Forecast: heurística simple v1 (refinar v2)
✅ Anomaly detection: 3-sigma rule sobre baseline 7d
✅ 4 tipos anomaly LOCKED
✅ Acciones automáticas:
   - key_leaked → SUSPEND workspace + notify crítico
   - bug_loop → notify crítico (no auto-suspend)
   - spike_sustained → notify (suggest upgrade)
   - spike_hour → notify Brian investigate
✅ Audit cada alarma + anomalía + tier change
✅ SQL schemas: 2 tablas nuevas
✅ Templates Jinja2 reused (B2 3.2.1)
✅ Email engine: SMTP simple v1 (sendgrid/SES v2)
✅ NO multi-currency v1 (USD only, R10 maneja v2)
```

### Cost impact

```
Setup adicional:
   • SMTP: $0 (Postfix local o SendGrid free)
   • Templates Jinja2: $0 (reusa B2)
   • Arq cron: $0 (reusa R2 B3)
   • Tablas Postgres: $0 (storage trivial)
   
Costo recurring: $0
Costo tiempo Brian: 4-5 días setup
```

---

## 5. Sub-tema 3.4.3 — LLM quality evaluation

### Decisión LOCKED

```
Framework híbrido 4 capas (rule + golden + LLM-judge + human)
```

### Contexto

Calidad LLM no es binaria. Sin eval = vendes wrapper Claude. Sin defensa B2B = comité técnico rechaza. Sin regresión auto = subes Sonnet 4.6 → 4.7 ciegamente.

### Mapeo al Grafo Maestro

- **Nodo 3 PFC:** eval guía iteración prompts/modelos
- **Nodo 9 Dual-Process Check (R5):** eval informa qué tier
- **Nodo 10 CLS:** consolidación aprende de feedback
- **Nodo 11 Neuromoduladores:** scores modulan confidence
- **Pilar 1 Seguridad:** safety dimension critical
- **Pilar 3 Autonomía:** agente auto-evalúa

### Candidatos evaluados

```
A) Sin eval framework v1                                       ❌ Inaceptable
B) LLM-as-judge built-in (Claude evaluates Claude)              ⚠️ Sesgo masivo
C) Eval framework híbrido (LLM-judge + golden + rule-based)     ✅ ELEGIDO
D) DeepEval / Ragas / Promptfoo                                 ⚠️ Wrapper opcional
E) Anthropic Workbench Evaluations                              📚 Futuro v2
```

### Las 4 capas complementarias

```
CAPA 1: RULE-BASED CHECKS (sync, deterministic, blocking critical)
   • Format compliance (JSON, Pydantic schema)
   • Length checks (no truncated)
   • Forbidden phrases (anti-references)
   • Required keywords (workspace config)
   • PII leakage detection (regex)
   • Tool call validity (schema post-execution)
   • Citation presence (si requiere)
   
   Costo: $0 | Latencia: <10ms | Cobertura: ~30%

CAPA 2: GOLDEN DATASETS (ground truth, CI/CD + weekly)
   • golden_datasets/general/ (50 Q&A)
   • golden_datasets/code/    (30 ejemplos análisis PR — wedge QA)
   • golden_datasets/{domain}/ (futuros — 30-50 per dominio)
   • YAML format con expected_outputs + eval_methods
   • Ejecución:
     - CI/CD pre-deploy: full dataset
     - Weekly cron: full dataset (regression check)
     - Daily cron: 5 random samples (smoke test)
   
   Costo: ~$0.10/full run | Latencia: ~5 min | Cobertura: ~50%

CAPA 3: LLM-AS-JUDGE Haiku (async background, 5% sample)
   • Sample rate config per workspace (default 5%)
   • Modelo: Claude Haiku 4.5 (barato, ya integrado)
   • Multi-prompt rotation (3 evaluator prompts)
   • Anti-sesgo:
     - Evaluator no sabe qué modelo generó respuesta
     - Rotating prompts (v1_strict, v2_balanced, v3_user_perspective)
     - Golden references comparative
     - Weekly human calibration
   • Dimensiones per dominio:
     - General: correctness, relevance, completeness, coherence, safety, format
     - Code: correctness, no_bugs, idiomatic, complete
     - Health: safety_first, evidence_based, no_diagnosis, refs
   
   Costo: ~$5-15/mes | Latencia: async | Cobertura: ~70%

CAPA 4: HUMAN REVIEW (escalation Brian weekly)
   • Triggers:
     - LLM-judge score <3 sostenido (3+ veces)
     - Cliente marca "respuesta mala"
     - Anomaly detection signals quality drop
     - Random 1 per día (calibration)
   • Workflow:
     1. Sistema flagea call
     2. Telegram Brian: "5 calls pending review"
     3. Brian dashboard: /admin/quality-review
     4. Brian scoring manual (1-5 + comments)
     5. Scores feed back calibra LLM-judge
   
   Frecuencia: ~5-10/semana max
   Tiempo Brian: ~30 min/semana
   Cobertura: 100% issues complejos
```

### Arquitectura integrada

```
Cliente envía query → Sistema responde con Sonnet
                     │
                     ▼
   CAPA 1: Rule-based (sync, blocking critical)
   Format/length/PII/forbidden
                     │ (response delivered)
                     ▼
   CAPA 3: LLM-judge sample (async Arq, 5%)
   Haiku evaluates con anti-sesgo
   Score <3 → trigger Capa 4
                     │
                     ▼
   CAPA 4: Human review queue
   Brian revisa weekly
   Feedback calibra Capa 3
   
   CAPA 2: Golden datasets (CI/CD + cron)
   Pre-deploy: full dataset
   Weekly: full dataset regression
   Daily: 5 random smoke test
```

### Esquemas SQL

```sql
CREATE TABLE shared.eval_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_type TEXT NOT NULL,         -- 'golden_full', 'golden_smoke', 'llm_judge_sample', 'human_review'
    workspace_id UUID,
    dataset_name TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    total_samples INTEGER NOT NULL,
    results_summary JSONB NOT NULL,
    trigger_event TEXT,
    audit_event_id UUID NOT NULL REFERENCES audit_events(id)
);

CREATE TABLE shared.eval_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    eval_run_id UUID NOT NULL REFERENCES shared.eval_runs(id),
    sample_id TEXT,
    call_audit_id UUID REFERENCES audit_events(id),
    scores JSONB NOT NULL,
    evaluator TEXT NOT NULL,
    evaluator_reasoning TEXT,
    flagged_for_human BOOLEAN DEFAULT false,
    human_reviewed BOOLEAN DEFAULT false,
    human_scores JSONB,
    human_reviewed_at TIMESTAMPTZ,
    human_reviewer TEXT
);

CREATE TABLE shared.golden_datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_name TEXT NOT NULL,
    version TEXT NOT NULL,
    sample_id TEXT NOT NULL,
    query TEXT NOT NULL,
    context JSONB,
    expected_outputs JSONB NOT NULL,
    safety_check TEXT,
    eval_methods TEXT[] NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (dataset_name, version, sample_id)
);
```

### Anti-sesgo strategies LOCKED (5)

```
1. EVALUATOR ANONYMIZATION
   LLM-judge NO sabe qué modelo generó respuesta

2. MULTI-PROMPT ROTATION
   3 prompts evaluator (strict/balanced/user_perspective)

3. GOLDEN REFERENCES COMPARATIVE
   Evaluator ve golden + new response, compara

4. PERIODIC HUMAN CALIBRATION
   Weekly: Brian revisa 5 random
   Divergencia >1.0 → recalibrar prompts

5. EVALUATOR DIVERSITY (futuro v2)
   v1: solo Haiku
   v2: agregar GPT-4o-mini cross-validator
   Disagreement → escalation human
```

### Reglas duras LOCKED

```
✅ 4 capas LOCKED: rule + golden + LLM-judge + human
✅ Sample rate LLM-judge: 5% default (configurable)
✅ Modelo evaluador: Claude Haiku 4.5
✅ Golden datasets v1: general (50) + code (30 wedge QA)
✅ Golden datasets storage: YAML + tabla SQL versioned
✅ Anti-sesgo: 5 strategies LOCKED
✅ CI/CD trigger: pre-deploy full dataset
✅ Cron triggers:
   - weekly full dataset
   - daily 5 samples smoke
✅ Human review triggers (4):
   - LLM-judge score <3
   - Cliente "respuesta mala"
   - Anomaly detection
   - Random 1/día calibration
✅ Storage: 3 tablas SQL nuevas
✅ Prometheus métricas: eval scores per workspace + dataset
✅ Multi-dominio: yaml config per dataset
✅ Dimensiones LOCKED per dominio
✅ Cost cap eval: $15/mes (5% sample ~1K calls)
✅ Audit cada eval run + result
✅ Eval failures NO bloquean response (excepto critical rule)
✅ Human review feedback → recalibra LLM-judge prompts
```

### Cost impact

```
Setup adicional:
   • Golden datasets curation: 2-3 días Brian time
   • Framework code: 3-4 días dev
   • Storage SQL: <100 MB
   • Prometheus storage: <500 MB extra

LLM-judge calls (5% sample):
   • Workspaces v1: 3-5 pilots
   • Calls/día/ws: ~50 avg
   • Total calls/día: ~250 max
   • Sample 5%: ~12 evals/día
   • Haiku tokens/eval: ~1K input + 200 output
   • Cost/eval: ~$0.0006
   • Mensual: ~$5-15

Costo total eval v1: ~$5-15/mes (dentro cap P5)
```

---

## 6. Stack final consolidado

```
COMPONENTE                          DECISIÓN                          COSTO
─────────────────────────────────────────────────────────────────────────
Observability persistence 1         audit_events Postgres [R2 B1]     $0
Observability persistence 2         Prometheus LOCAL                   $0
Instrumentación FastAPI              prometheus_fastapi_instrumentator $0 (MIT)
Métricas LLM-specific               ~25 LOCKED                         $0
Cardinality limit                   ~1200 series max                   $0
Wrapper                              LLMCallRecorder atomic              $0

Cost monitoring engine              CostMonitor (5 capacidades)        $0
Alarmas graduales                   50%, 75%, 90% (+ 100% B3 3.3.2)    $0
Dashboard cliente                    HTMX + Jinja2 (reused B2)          $0
Anomaly detection                   Statistical 3-sigma 7d baseline   $0
Forecast end-of-month               daily_avg × days_in_month          $0
Reporting recurring                 Arq cron (reused R2 B3)            $0
SQL nuevas                           cost_alarms, cost_anomalies        $0
Email engine                         SMTP simple v1                     $0

Eval framework híbrido              4 capas LOCKED                      $0
Rule-based evaluator                Regex + Pydantic                    $0
Golden datasets v1                  general (50) + code (30)            $0
LLM-judge                            Haiku 5% sample                    ~$5-15/mes
Human review                         Weekly Brian (~30 min)             $0
Anti-sesgo                           5 strategies LOCKED                 $0
SQL nuevas                           eval_runs, eval_results,
                                     golden_datasets                    $0
─────────────────────────────────────────────────────────────────────────
TOTAL incremental B4 R3                                                ~+$5-15/mes
TOTAL v1 FINAL (R1+R2+R3 100%)                                        ~$62-77/mes
```

### Estructura módulo for3s_os/llm/ extendida (post-B4)

```
for3s_os/llm/
├── base.py                         → LLMProvider Protocol (B1)
├── anthropic_provider.py           → ClaudeProvider (B1)
├── openai_provider.py              → GPTProvider fallback (B1)
├── failover.py                     → FailoverManager (B1, ext B3)
├── prompts/                        → 3.2.1 (B2)
├── context_builder.py              → 3.2.2 (B2)
├── reranker.py                     → 3.2.2 (B2)
├── token_packer.py                 → 3.2.2 (B2)
├── cache.py                        → 3.2.3 (B2)
├── cache_invalidator.py            → 3.2.3 (B2)
├── tools/                          → 3.2.4 (B2)
├── streaming/                      → 3.3.1 (B3)
├── concurrency/                    → 3.3.2 (B3)
├── resilience/                     → 3.3.3 (B3)
├── observability/                  → 3.4.1 NUEVO B4
│   ├── llm_metrics.py              → Prometheus métricas
│   ├── recorder.py                 → LLMCallRecorder atomic
│   └── instrumentator.py           → FastAPI setup
├── cost/                           → 3.4.2 NUEVO B4
│   ├── monitor.py                  → CostMonitor 5 capacidades
│   ├── alarms.py                   → 3 thresholds
│   ├── anomaly.py                  → Statistical 3-sigma
│   ├── forecast.py                 → daily_avg × days
│   ├── dashboard.py                → Endpoint cliente
│   └── reporting.py                → Cron digest/report
├── eval/                           → 3.4.3 NUEVO B4
│   ├── framework.py                → Orchestrator
│   ├── rule_based.py               → CAPA 1
│   ├── golden_dataset.py           → CAPA 2
│   ├── llm_judge.py                → CAPA 3 Haiku
│   ├── human_review.py             → CAPA 4 queue
│   ├── calibration.py              → Anti-sesgo
│   └── golden_datasets/            → YAML files
│       ├── general/v1.0/
│       └── code/v1.0/
├── cost_tracker.py                 → per-workspace (B1)
└── llm_observability.py            → métricas (B1, ext B3+B4)
```

### Patrones obligatorios añadidos B4

```
✓ Prometheus LOCAL en mismo servidor (NO externalizado)
✓ Retención 15 días Prometheus + 13 meses audit Postgres
✓ Scrape interval 15s, métricas LOCKED ~25
✓ /metrics endpoint con auth interno
✓ Cardinality limit hard (1200 series)
✓ LLMCallRecorder atomic (audit + metrics juntos)
✓ Alarmas graduales 50/75/90% dedupe per mes
✓ Background jobs Arq:
   - alarmas check 15 min
   - anomaly detection 5 min
   - daily digest 9 AM
   - weekly digest Mon 9 AM
   - monthly report day 1 9 AM
✓ Dashboard cliente con workspace_id auth
✓ Anomaly 3-sigma sobre baseline 7d
✓ 4 tipos anomaly clasificados
✓ Auto-actions: key_leaked SUSPEND
✓ Eval 4 capas obligatorias
✓ Sample rate LLM-judge 5%
✓ Anti-sesgo: 5 strategies LOCKED
✓ Golden datasets versioned YAML + SQL
✓ CI/CD pre-deploy full dataset
✓ Human review triggers automáticos (4)
✓ Audit cada eval run + alarm + anomaly
✓ Critical rule failures REJECT response
✓ Otros eval failures NO bloquean (audit + flag)
✓ Cost cap eval $15/mes hard
```

---

## 7. Cobertura del Grafo Maestro post-R3

### Nodos servidos por R3 COMPLETO

```
NODO                                 STATUS POST-R3 100%
──────────────────────────────────────────────────────────
Nodo 1 Hipocampo                    ✅ context (B2)
Nodo 3 PFC (Orchestrator)           ✅ pleno (B1+B2+B3+B4)
Nodo 4 Cuerpo Calloso                🟡 foundation (B2)
Nodo 5 Memoria Largo                ✅ context (B2)
Nodo 6 Sistema Sensorial             🟡 foundation (B3 streaming)
Nodo 8 Tálamo                        🟡 foundation (B2 ranking + B3)
Nodo 9 Dual-Process Check           🟡 preparación (eval informa)
Nodo 10 CLS                          ✅ Haiku + tmpl + eval (B4)
Nodo 11 Neuromoduladores            🟡 foundation (B3+B4 signals)

Status post-R3:
   ✅ Nodos servidos plenos: 3, 10 (2 nodos)
   ✅ Nodos servidos contexto: 1, 5 (2 nodos)
   🟡 Foundation: 4, 6, 8, 9, 11 (5 nodos preparados R5+)
```

### Pilares — Cobertura por R3 COMPLETO

```
Pilar 1 — Seguridad E2E
   ✅ Meta-audit todas las operaciones LLM
   ✅ Cliente opt-out fallback
   ✅ Permission model granular (B2 3.2.4)
   ✅ Transparencia provider headers
   ✅ TLS 1.3 cloud providers
   ✅ Audit chain inmutable retry/CB/fallback
   ✅ Tool timeout enforcement
   ✅ Idempotency tools preserve integrity
   ✅ Workspace fairness anti-DoS interno
   ✅ AUTH_FAILURE alarma crítica
   ✅ Eval safety dimension per dominio (B4 3.4.3)
   ✅ Anomaly detection key_leaked auto-suspend (B4 3.4.2)
   ✅ PII leakage detection eval (B4 3.4.3 CAPA 1)
   ⏳ Prompt injection detection (R9)

Pilar 2 — Escalabilidad por nodo
   ✅ FailoverManager resiliencia
   ✅ CapacityLimiter concurrency (R2 B3)
   ✅ Caching -62% costo Sonnet maduro (B2 3.2.3)
   ✅ Context budget evita explosión costos (B2 3.2.2)
   ✅ Tool parallel execution con limiter
   ✅ Streaming reduce memoria servidor (B3 3.3.1)
   ✅ Token Bucket per workspace (B3 3.3.2)
   ✅ Circuit Breaker evita cascadas (B3 3.3.3)
   ✅ Cap P5 enforcement AUTOMÁTICO + graduales (B3+B4)
   ✅ Observability tiempo real (B4 3.4.1)
   ✅ Forecast proactive (B4 3.4.2)

Pilar 3 — Autonomía Generativa
   ✅ LLM principal habilita razonamiento autónomo (B1)
   ✅ LLM decide tools autónomamente con guardrails (B2 3.2.4)
   ✅ Templates evolucionables per dominio (B2 3.2.1)
   ✅ Agente decide qué error reintentar (B3 3.3.3)
   ✅ Tool retry separado del LLM loop
   ✅ Eval feedback informa LLM-judge calibration (B4 3.4.3)
   ✅ Anomaly auto-actions sin Brian intervention (B4 3.4.2)
   ⏳ Meta-Orchestrator (Pilar 3 completo) v3+
```

### Anclas LOCKED — Verificación post-R3 COMPLETO

```
1.D Dedicated SaaS  ✅ tiers per workspace (B1)
                     ✅ templates per workspace cache separado (B2)
                     ✅ allowed_tools whitelist (B2 3.2.4)
                     ✅ Token Bucket per workspace (B3 3.3.2)
                     ✅ alarmas + dashboard per workspace (B4 3.4.2)
                     ✅ eval scores per workspace (B4 3.4.3)

2.B Open Core       ✅ SDKs abiertos:
                        • anthropic MIT
                        • openai MIT
                        • Jinja2 BSD
                        • Pydantic v2 MIT
                        • sse_starlette MIT
                        • prometheus_fastapi_instrumentator MIT
                        • prometheus_client Apache
                     Modelos cerrados con disclaimer P3

3.D Equipo pequeño  ✅ provider único maduro (B1)
                     ✅ stack vanilla Python (B2+B3+B4)
                     ✅ alarmas a Brian directo Telegram
                     ✅ eval framework operable por 1 persona
                     ✅ todo en código + Postgres + Valkey + Prometheus
                     ✅ NO microservicios overhead
```

---

## 8. Costo total post-R3 100%

```
COMPONENTE                                          COSTO USD/mes
─────────────────────────────────────────────────────────────────
SUBTOTAL R1+R2:                                     ~$43/mes

R3 BLOQUE 1:
   Claude Sonnet 4.6 (principal):                   ~$50/mes
   OpenAI fallback LLM (raro):                      ~$0.30/mes

R3 BLOQUE 2 (impacto neto caching):
   Caching maduro saving (-62%):                    ~-$31/mes
   Tool overhead (~20% calls):                      ~+$6/mes

R3 BLOQUE 3 (impacto resilience):
   Streaming SSE infra:                             $0
   Token Bucket infra:                              $0 (Valkey reused)
   Resilience taxonomy:                             $0
   Reducción errors mal manejados:                  ~-$5-10/mes

R3 BLOQUE 4 (impacto observability + eval):
   Prometheus LOCAL:                                $0
   Cost monitoring (5 capacidades):                 $0
   Eval Haiku (5% sample):                          ~+$5-15/mes
   Email SMTP local:                                $0
─────────────────────────────────────────────────────────────────
TOTAL v1 FINAL (R1+R2+R3 100% LOCKED):              ~$62-77/mes
```

### Verificación P2 <25% pilot revenue

```
Pilot Light USD 3,500 (3 semanas):
   Techo AI+infra: USD 875 (25%)
   Consumo v1 (3 sem): USD ~55
   → 6.3% del techo
   → MARGEN 93.7% para R4-R10

Pilot Pro USD 8,000 (3 semanas):
   Techo: USD 2,000
   Consumo v1: USD ~55
   → 2.8% del techo
   → MARGEN 97.2%

CONCLUSIÓN: R3 completo deja margen MASIVO para R4-R10.
```

### Verificación P5 cap LLM ($50-200/mes)

```
LLM TOTAL v1 FINAL con caching maduro:
   • Claude Haiku CLS:                       ~$37/mes
   • Claude Sonnet (caching maduro -62%):    ~$19/mes
   • Claude Haiku eval (5% sample):          ~$5-15/mes
   • OpenAI fallback:                         ~$0.30/mes
   ─────────────────────────────────────────────
   TOTAL LLM v1 FINAL:                        ~$61-71/mes

Cap P5 LOCKED:           $50-200/mes
% del cap (medio):       31-36%
Margen disponible:       $130-140 para escalado workspaces

   → Caching + eval + observability DENTRO del cap P5
   → 2.5x más volumen disponible vs hard cap teórico
```

### Compras únicas (sin cambio)

```
UPS básico:                                ~$80-150 una vez
Disco externo USB 2 TB (backup):           ~$60 una vez
Dominio for3s.ai (registro inicial):       ~$10 una vez
─────────────────────────────────────────
TOTAL una vez:                              ~$150-220
```

---

## 9. Exploraciones futuras NO adoptadas v1

### 📚 Sub-tema 3.4.1 — Observability alternativos

```
📚 Candidato A — Solo audit chain Postgres
   • Cuándo: dev local Brian, <3 workspaces
   • No para producción real

📚 Candidato C — OpenTelemetry full stack
   • Cuándo: v2-v3 con SRE team dedicado
   • Beneficio: distributed tracing real, vendor-neutral
   • Trigger: R8 LOCKED OTel stack + >10 workspaces

📚 Candidato D — SaaS observability (Helicone/Langfuse)
   • Cuándo: NUNCA para B2B enterprise (viola P3)
   • Solo viable: dev tooling personal

📚 Candidato E — Custom dashboard FastAPI
   • Cuándo: NUNCA (reinventar Prometheus)

📚 Distributed tracing con OpenTelemetry
   • Cuándo: v2 con microservicios reales
   • Beneficio: visualizar request flow E2E
   • Trigger: R5 Multi-Agent activo

📚 Log aggregation Loki
   • Cuándo: R8 LOCKED stack observability
   • Beneficio: full-text search logs
   • Hoy: audit_events SQL queries bastan

📚 Anomaly detection con ML
   • Cuándo: v3 con datos históricos suficientes
   • Beneficio: detección sin thresholds manuales
```

### 📚 Sub-tema 3.4.2 — Cost monitoring alternativos

```
📚 Candidato A — Solo hard cap B3 3.3.2
   • Cuándo: NUNCA producción real

📚 Candidato B — Alarmas básicas + dashboard Brian
   • Cuándo: 1-3 pilots iniciales
   • Defer C cuando >5 pilots

📚 Candidato D — Stripe/Lago billing integration
   • Cuándo: R10 LOCKED billing strategy
   • Trigger: >10 pilots activos + invoicing real

📚 Candidato E — AI-powered FinOps automático
   • Cuándo: v3 con >100 workspaces + ML data
   • Beneficio: optimization automatic
   • Trigger: ROI ML > complexity

📚 Multi-currency / IVA support
   • Cuándo: R10 LOCKED billing real
   • Beneficio: facturación LATAM nativa
   • Hoy: USD-only

📚 Tier upgrade automation
   • Cuándo: v2 cuando pricing tiers maduros
   • Beneficio: cliente upgrade auto vs flow manual

📚 Cost prediction con ML
   • Cuándo: v3 con histórico
   • Beneficio: forecast más exacto

📚 Customer billing portal
   • Cuándo: R10
   • Self-service tier changes, invoices, etc.

📚 Per-tool cost tracking granular
   • Cuándo: v2 con MCP tools costosos
   • Trigger: tools R4 con costo real
```

### 📚 Sub-tema 3.4.3 — Eval alternativos

```
📚 Candidato A — Sin eval framework
   • Cuándo: NUNCA producción real

📚 Candidato B — LLM-as-judge solo
   • Cuándo: NUNCA solo (sesgo)
   • SÍ como CAPA 3 de framework C

📚 Candidato D — DeepEval/Ragas/Promptfoo
   • Cuándo: posible wrapper INTERNO de C
   • Beneficio: best practices community
   • Defer decisión a implementación

📚 Candidato E — Anthropic Workbench Evaluations
   • Cuándo: v2 cuando GA + workspace tier permite
   • Beneficio: native Anthropic
   • Hoy: viola P3 strict + premature beta

📚 Cross-validator GPT-4o-mini
   • Cuándo: v2 anti-sesgo strategy 5
   • Beneficio: disagreement con Haiku → human escalation
   • Costo: +$5-10/mes eval

📚 ML-trained custom evaluator
   • Cuándo: v3 con dataset >10K reviewed
   • Beneficio: evaluator específico For3s OS dominio
   • Trigger: golden datasets maduros + human reviews

📚 Community-sourced golden datasets
   • Cuándo: v2-v3 con multi-dominio
   • Beneficio: scale dominio dueño
   • Implementación: GitHub repo público golden_datasets

📚 A/B testing prompts framework
   • Cuándo: v2 con tráfico suficiente
   • Beneficio: empirical prompt iteration
   • Implementación: split workspace traffic

📚 Reinforcement learning from feedback
   • Cuándo: v3 con human reviews >1K
   • Beneficio: prompts auto-tune
   • Estado: research-grade, no producción

📚 Multi-modal eval (vision, audio)
   • Cuándo: R3 wedges con vision/audio
   • Hoy: text-only eval

📚 Adversarial eval (red team auto)
   • Cuándo: v2-v3 con safety crítico
   • Beneficio: detectar jailbreaks
   • Trigger: R9 Security activa esto

📚 Domain expert evaluator network
   • Cuándo: v3 con clientes enterprise
   • Beneficio: validación humana especialista
   • Costo: marketplace tipo Scale AI
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**

---

## 10. Implicaciones en rondas futuras

### Para R4 — Tools / MCP Layer

```
✅ Tool retry separado + idempotency (B3 3.3.3)
✅ Tool metrics observables (B4 3.4.1)
✅ Tool eval rule-based (B4 3.4.3 CAPA 1)
✅ Tool cost tracking per workspace (B4 3.4.2)

R4 decidirá:
   • MCP client framework (FastMCP, anthropic-mcp)
   • MCP servers concretos (GitHub QA, Slack, Notion)
   • Tool discovery/registration runtime
   • MCP server health monitoring (usa Prometheus B4)
```

### Para R5 — Orchestration / Multi-Agent

```
✅ Streaming sub-agent compatible (B3 3.3.1)
✅ Concurrency control hereda (B3 3.3.2)
✅ Resilience taxonomy reused (B3 3.3.3)
✅ Eval feedback informa Nodo 9 Dual-Process (B4 3.4.3)
✅ Cost tracking sub-agent (B4 3.4.2)

R5 decidirá:
   • Nodo 8 Tálamo (routing aware concurrency + eval scores)
   • Nodo 9 Dual-Process Check (eval informa qué tier)
   • Nodo 11 Neuromoduladores (B4 stress signals)
   • Multi-Agent Network lifecycle
```

### Para R6 — Memory Stack extensions

```
✅ Eval informa qué memorias promover en CLS (B4 3.4.3)
✅ Cost-aware retrieval budget (B4 3.4.2)
✅ Memory metrics observables (B4 3.4.1)

R6 decidirá:
   • Memory tier rebalancing automático
   • Procedural memory (skills R5)
   • Semantic memory extensions
```

### Para R7 — Frontend / Channel

```
✅ Streaming SSE protocol LOCKED (B3 3.3.1)
✅ Dashboard cliente foundation HTMX (B4 3.4.2)
✅ Cost dashboard self-service ready (B4 3.4.2)
✅ Quality scores expuestos cliente (B4 3.4.3)

R7 decidirá:
   • Frontend framework
   • Dashboard layout
   • Telegram bot integration (Hermes-style)
   • UX progress indicators streaming
```

### Para R8 — Observability completa

```
✅ Prometheus métricas ~25 LLM-specific (B4 3.4.1)
✅ Audit chain inmutable (R2 B1 + ext B3+B4)
✅ Eval metrics exportadas (B4 3.4.3)
✅ Cost metrics observables (B4 3.4.2)
✅ Foundation Grafana dashboards LOCKED

R8 decidirá:
   • Grafana setup + dashboards
   • Distributed tracing OpenTelemetry
   • Log aggregation Loki
   • Alerting rules Prometheus AlertManager
   • SLO/SLI formal
```

### Para R9 — Security / Compliance

```
✅ AUTH_FAILURE alarma crítica (B3 3.3.3)
✅ Anomaly key_leaked auto-suspend (B4 3.4.2)
✅ Eval safety dimension per dominio (B4 3.4.3)
✅ PII leakage detection rule-based (B4 3.4.3 CAPA 1)
✅ Audit chain inmutable forensics

R9 decidirá:
   • Nodo 8 Amígdala (security checks pre-execution)
   • Prompt injection detection
   • Adversarial eval (red team auto)
   • SOC2 / ISO27001 path
```

### Para R10 — CI/CD / Deploy

```
✅ Eval pre-deploy regression check (B4 3.4.3 CI/CD)
✅ Cost forecasting foundation (B4 3.4.2)
✅ Observability metrics foundation (B4 3.4.1)

R10 decidirá:
   • Stripe/Lago billing integration
   • Multi-currency / IVA LATAM
   • CI/CD pipeline GitHub Actions
   • Deploy strategy (canary, blue-green)
   • Backup/restore automation
```

---

## 11. Riesgos legítimos aceptados

6 riesgos B4 identificados, todos mitigables.

### Riesgo 1 — Cardinality explosion Prometheus

```
PROBLEMA:
   Alto número labels únicos → Prometheus memory bloat.
   Ej: workspace_id × user_id × model = millones de series.

IMPACTO v1:    BAJO (3-5 workspaces v1)
IMPACTO v3:    MEDIO (más workspaces amplifican)

MITIGACIÓN:
   • Límites duros: ~50 workspaces × 3 modelos × 2 providers × 4 layers = ~1200 max
   • NO incluir user_id en labels (privacy + cardinality)
   • Cardinality audit mensual con script
   • Alarma si memoria Prometheus >80%
```

### Riesgo 2 — False positive anomaly detection

```
PROBLEMA:
   Cliente legítimo escala uso → marcado como bug_loop.
   Pérdida confianza si suspendemos por error.

IMPACTO v1:    MEDIO
IMPACTO v3:    MEDIO

MITIGACIÓN:
   • Cliente puede reportar "anomaly is OK"
   • Auto-suspend solo para key_leaked (high signal)
   • Otros tipos: notify Brian, no auto-action
   • Ajustar thresholds 3-sigma con feedback post-launch
   • Audit toda anomaly decision
```

### Riesgo 3 — Email delivery falla (SMTP issues)

```
PROBLEMA:
   Cliente no recibe alarmas → entera al hard cap.
   Reputation damage.

IMPACTO v1:    BAJO (3-5 clientes)
IMPACTO v3:    MEDIO (más clientes amplifican)

MITIGACIÓN:
   • Retry queue Arq para emails fallidos
   • Fallback Telegram Brian si email falla 3x
   • Monitoring email_delivery_failed metric
   • v2: SendGrid/SES con webhooks delivery
```

### Riesgo 4 — LLM-judge sesgo Anthropic-self

```
PROBLEMA:
   Haiku evalúa Sonnet → ambos Claude → sesgo +20%.
   Eval inflated, no detecta problemas reales.

IMPACTO v1:    MEDIO
IMPACTO v3:    MEDIO

MITIGACIÓN:
   • 5 anti-bias strategies LOCKED
   • Multi-prompt rotation (3 evaluators)
   • Golden datasets ground truth (no sesgo posible)
   • Human calibration weekly (Brian)
   • v2: cross-validator GPT-4o-mini para disagreement
   • Audit divergence LLM-judge vs human consistente
```

### Riesgo 5 — Golden datasets sesgo curation Brian

```
PROBLEMA:
   Brian cura golden datasets → sesgo personal.
   Eval mide "lo que Brian considera bueno", no realidad cliente.

IMPACTO v1:    MEDIO
IMPACTO v3:    BAJO (dominio dueños toman over)

MITIGACIÓN:
   • Versioned datasets (cliente puede proponer cambios)
   • Diversificar curators cuando lleguen +3 dominios
   • Community-sourced datasets v2 (GitHub público)
   • A/B prompts vs golden = validar eval mismo
   • Monthly review datasets accuracy
```

### Riesgo 6 — Human review queue se acumula

```
PROBLEMA:
   Brian busy → queue creciente → eval feedback se pierde.
   LLM-judge calibration degrada.

IMPACTO v1:    MEDIO (Brian solo)
IMPACTO v3:    BAJO (puede delegar)

MITIGACIÓN:
   • Telegram alert si queue >20 items
   • Dashboard prioritization (críticos primero)
   • Auto-archive si >7 días pending
   • Weekly batch review optimizado (30 min)
   • v2: delegar a co-founder o consultor
```

---

## 12. Cierre R3 100% — síntesis final

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅✅✅ R3 — MODEL/LLM LAYER 100% CERRADO ✅✅✅              ║
║                                                                ║
║   14/14 sub-temas LOCKED                                       ║
║   4/4 bloques LOCKED                                            ║
║   4 decisiones logged (D-012, D-013, D-014, D-015)              ║
║   3 días de debate (2026-06-01 → 2026-06-03)                    ║
║                                                                ║
║   ─────────────────────────────────────────────────────       ║
║                                                                ║
║   FOUNDATION ENTREGADA:                                         ║
║                                                                ║
║   • R4 Tools/MCP Layer        — ready to start                  ║
║   • R5 Orchestration           — foundation Nodo 9 + eval        ║
║   • R6 Memory extensions       — eval-aware promotion            ║
║   • R7 Frontend / Channel      — SSE + dashboards ready          ║
║   • R8 Observability completa  — Prometheus ready Grafana        ║
║   • R9 Security/Compliance     — eval safety + anomaly ready    ║
║   • R10 CI/CD / Deploy         — eval pre-deploy + cost monitor  ║
║                                                                ║
║   ─────────────────────────────────────────────────────       ║
║                                                                ║
║   MÉTRICAS FINALES:                                             ║
║                                                                ║
║   • Costo total v1: ~$62-77/mes                                  ║
║   • % techo P2 Pilot Light: 6.3% (margen 93.7%)                 ║
║   • % cap P5 LLM: 31-36% (margen $130-140)                      ║
║   • UX percepción: 3-10x mejor (TTFT streaming)                  ║
║   • Anthropic 429s: -95% (token bucket)                          ║
║   • LLM costs: -10-15% (mejor manejo errores)                    ║
║   • Cache savings maduro: -62% Sonnet                            ║
║                                                                ║
║   ─────────────────────────────────────────────────────       ║
║                                                                ║
║   PRÓXIMO PASO: Iniciar R4 — Tools / MCP Layer                  ║
║   (después de cierre formal FASE 2 público-formal)               ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_03_Bloque_4_Observability_Cost.md`).
