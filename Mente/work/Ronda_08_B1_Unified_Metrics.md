# Ronda 8 — Bloque 1 — Unified Metrics (Foundation Pilar 2)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_08_B1_Unified_Metrics.md → work/Ronda_08_B1_Unified_Metrics.md (2026-07-30, ADR-029)

## Purpose

Ronda 8 — Bloque 1 — Unified Metrics (Foundation Pilar 2)


**Sub-documento de R8.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_08_Observabilidad_Completa.md](work/Ronda_08_Observabilidad_Completa.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED)
**Fecha cierre:** 2026-06-08

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Cardinality v1 |
|---|---|---|
| 8.1.1 Métricas por nodo | C — Avanzadas + specialized | ~3,500 series |
| 8.1.2 Métricas cross-cutting | C — Completo + tracing + cardinality | ~1,650 series |
| 8.1.3 Unit economics real-time | C — Forecast + enforcement | ~50 gauges |
| **TOTAL B1** | | **~5,150 series** |

---

## 8.1.1 — Métricas por Nodo

**Decisión LOCKED:** **C — Avanzadas per nodo + cardinality + business + scaling + specialized**

### 11 nodos Grafo Maestro instrumentados

`workspace_gate` · `thalamus` · `amygdala` (R9) · `pfc` · `multi_agent` · `hippocampus` · `kg` · `skills` (ganglios_basales) · `microglia` · `cls` · `dmn` · `neuromod`

### 5 categorías métricas

1. **Operational** (requests + latency + errors + active_concurrent)
2. **Business** (cost_usd + tokens + outcomes)
3. **Scaling** (queue_depth + saturation + utilization)
4. **Storage** (bytes per tier hot/warm/cold)
5. **Specialized** per nodo

### Cardinality control v1

- `workspace_id`: SIEMPRE label
- `identity_id`: NUNCA (audit cubre)
- `request_id`: → Tempo traces (P1 LOCKED)
- Presupuesto: ~3,500 series v1

### Specialized metrics ejemplos

- **ThalamusMetrics:** routing_decisions + context_skipped
- **PFCMetrics:** plans_generated + re_plans_triggered + confidence
- **MultiAgentMetrics:** specialists + batch_size
- **SkillsMetrics:** applied + score + lifecycle + no_go
- **MicrogliaMetrics:** eval_score + blocked + correction_loop

### Instrumentation patterns DRY

```python
# Decorator
@instrument_node(node_metrics)
async def my_node_function(*args, workspace_id: str, **kwargs):
    ...

# Context manager
async with measure_node(node_metrics, workspace_id) as ctx:
    ...

# Background collector
class ScalingIndicatorsCollector:
    COLLECTION_INTERVAL_SECONDS = 10
    SATURATION_ALERT_THRESHOLD = 0.8
    async def collect_loop(self):
        # 10s polling per node
        ...
```

### Audit events nuevos

- `metric_cardinality_exceeded`
- `scaling_indicator_threshold_crossed`
- `scaling_collector_error`

### Reusa stack

R3 B4 Prometheus + R2 B3 Arq + Valkey

### Foundation

8.1.3 unit economics + 8.2.3 dashboard Pilar 2 + Pilar 2 §7 estrategias

---

## 8.1.2 — Métricas Cross-Cutting

**Decisión LOCKED:** **C — Completo + tracing correlation + cardinality strategy**

### 3 dimensiones cross-cutting

#### 1. PER REQUEST (E2E flow tracking)

```python
class RequestE2EMetrics:
    request_e2e_latency_seconds  # workspace+channel+subgraph_mode
    request_total                 # workspace+channel+status+mode
    nodes_activated_count         # workspace+channel
    request_cost_usd              # workspace+channel
```

#### 2. PER WORKSPACE (multi-tenant attribution)

```python
class WorkspaceMetrics:
    workspace_requests_month_total
    workspace_cost_month_usd
    workspace_p5_cap_ratio          # early warning
    workspace_active_identities     # 30d
    workspace_tier_indicator        # 1=pilot, 2=standard, 3=enterprise
```

#### 3. PER IDENTITY (top-10 cardinality controlled)

```python
class IdentityMetrics:
    identity_requests_day_total    # workspace + identity_id_short
    identity_cost_day_usd           # workspace + identity_id_short
    # Cardinality: 30 ws × 10 = 300 series max
```

### Tempo tracing correlation

```python
class TempoTracingIntegration:
    async def emit_trace(self, request: Request) -> TraceContext:
        with tracer.start_as_current_span(
            'request_e2e',
            attributes={
                'workspace_id': request.workspace_id,
                'identity_id': request.identity_id,
                'channel': request.channel,
                'subgraph_mode': request.subgraph_mode,
                'trace_id': request.trace_id,
            }
        ) as span:
            # Nested spans per node
            ...
```

### Cardinality presupuesto v1

- request_e2e: ~1,200 series
- workspace aggregates: ~150 series
- identity top-10: ~300 series
- **Total B1.2: ~1,650 series**

### Instrumentation principal

```python
async with request_instrumenter.instrument_request(
    workspace_id, channel, identity_id,
) as ctx:
    ctx.nodes_activated.add('thalamus')
    ctx.cost_accumulator += llm_call.cost
    ctx.subgraph_mode = signals.subgraph_mode.value
```

### Background aggregators (Arq R2 B3 reused)

- **WorkspaceAggregator** (cron hourly): monthly stats per workspace
- **IdentityTopNAggregator** (cron daily 1 AM): clear gauges + recompute top-10

### Identity cardinality strategy

- `identity_id` NUNCA per-request en Prometheus
- Per-request granularity → Tempo traces
- Aggregates top-10 only → Prometheus
- Full detail → audit_events query

### Reusa stack

R3 B4 Prometheus + R7 7.3.1 Identity + R7 7.1.x Channels + R2 B3 Arq + Tempo (P1 R8)

---

## 8.1.3 — Unit Economics Real-Time

**Decisión LOCKED:** **C — Completo + forecast + enforcement**

### 5 components

#### 1. CostAggregatorRealtime (Redis sliding windows)

```python
class CostAggregatorRealtime:
    async def record_cost(self, workspace_id, identity_id, node_name, cost_usd, trace_id):
        # 1min window (burn rate detection)
        # 1h window (forecast input)
        # day window (totals)
        # month per-node breakdown (hash)
        # month per-identity breakdown (hash)
        ...
```

#### 2. UnitEconomicsTracker

```python
request_cost_breakdown_usd          # per node histogram
workspace_unit_economics_usd        # $/request avg
workspace_margin_usd                # plan_revenue - cost
pilar2_promise_compliance_ratio     # vs $0.80 v1
```

#### 3. P5CapEnforcer (HARD enforcement)

```python
WARN_THRESHOLD = 0.80   # 80% → notify Brian + owner
BLOCK_THRESHOLD = 1.00  # 100% → block workspace requests

cap_status gauge:
    0 = OK
    1 = warned
    2 = blocked
```

#### 4. ForecastEngine

```python
# Linear regression hourly
# Skip first 12h (too noisy)
workspace_forecast_month_usd
workspace_forecast_over_cap  # 1 if projected > P5 cap
```

#### 5. BurnRateDetector

```python
BASELINE_WINDOW_DAYS = 7
ANOMALY_MULTIPLIER = 3.0

workspace_burn_rate_usd_per_min
workspace_burn_rate_anomaly  # 1 if rate > 3x baseline
```

### Integration R6 LLM Gateway

```python
class LLMGateway:
    async def call(self, request: LLMRequest) -> LLMResponse:
        response = await self._actual_call(request)
        
        # Record cost (R8 8.1.3)
        await cost_aggregator.record_cost(
            workspace_id=request.workspace_id,
            identity_id=request.identity_id,
            node_name=request.node_name,
            cost_usd=response.cost_usd,
            trace_id=request.trace_id,
        )
        
        # Check P5 cap (async, no block)
        asyncio.create_task(
            p5_cap_enforcer.check_workspace(request.workspace_id)
        )
        
        return response
```

### Arq schedules (R2 B3 reused)

- `burn_rate_detector.minute_detection` → every 1 min
- `forecast_engine.hourly_forecast` → every 1 hour
- `unit_economics_tracker.update_gauges` → every 5 min
- Daily aggregations → daily 1 AM

### Pilar 2 §7.3 promesa validation

- v1 (10 users): $0.80/análisis target
- v2 (100K users): $0.20/análisis target (4x reduction)
- Gauge real-time compliance ratio
- Alert si > 1.5x promesa

### Audit events nuevos

- `workspace_p5_cap_warning_triggered` (80%)
- `workspace_p5_cap_block_triggered` (100%)
- `workspace_forecast_over_cap`
- `workspace_burn_rate_anomaly_detected` (3x baseline)
- `pilar2_promise_compliance_violation` (> 1.5x promised)

### Reusa stack

R6 LLM Gateway + R7 7.4.2 Notifications + R3 B4 Prometheus + R2 B3 Arq + Valkey/Redis

### Foundation

8.2.2 Analytics dashboard + 8.4.1 SLO/SLA + future v2 scale validation

---

## Cobertura Grafo Maestro

| Sección GM | B1 cobertura |
|---|---|
| §6.3 Workspace Boundaries | ✅ workspace_id obligatorio en TODA métrica |
| §6.5 ObsCompleta métricas | ✅ 11 nodos + cross-cutting + business |
| Pilar 2 §7.3 Unit Economics | ✅ Real-time validation + forecast |
| Pilar 2 §7.4 P5 Cap | ✅ HARD enforcement automático |
| Pilar 2 §7.5 Capacity | ✅ ScalingIndicatorsCollector foundation |

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_08_B1_Unified_Metrics.md`).
