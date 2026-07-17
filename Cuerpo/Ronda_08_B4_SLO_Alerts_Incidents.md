# Ronda 8 — Bloque 4 — SLO/SLA + Alerts + Incidents ⭐ CIERRA R8

**Sub-documento de R8.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_08_Observabilidad_Completa.md](Ronda_08_Observabilidad_Completa.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED) — Cierra R8 al 100%
**Fecha cierre:** 2026-06-08

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Componentes |
|---|---|---|
| 8.4.1 SLO/SLA Formal | C — Framework + tiers + budgets + self-service | 7 components |
| 8.4.2 Alerts Aggregation | C — AM + custom unificado cross-system | 8 components |
| 8.4.3 Incident Management | C — Lifecycle + runbooks + postmortem + status + MTTR | 7 components |

---

## 8.4.1 — SLO/SLA Formal

**Decisión LOCKED:** **C — Framework + tiers + budgets + self-service** (alineada P3=B LOCKED self-service básico)

### 3 tiers SLO targets

| Tier | Availability | Latency p95 E2E | Error rate max | Error budget | Refund eligible |
|---|---|---|---|---|---|
| **pilot_light** (free) | 95.0% | 10.0s | 5.0% | 36 hrs/mo | ❌ |
| **standard** ($50/mo) | 99.5% | 5.0s | 1.0% | 3.65 hrs/mo | ❌ |
| **enterprise** ($500/mo) | 99.9% | 3.0s | 0.5% | 43.8 min/mo | ✅ automatic flag |

### Per channel SLOs (additive constraints)

| Channel | Latency p95 | Description |
|---|---|---|
| telegram | 5.0s | User-facing chat (síncrono) |
| rest | 8.0s | Programmatic API |
| github_webhook | 30.0s | Async event processing |

### 7 Components

#### 1. SLODefinitions
Tiers + channels constants (`SLODefinitions.SLOS` + `SLODefinitions.CHANNEL_SLOS`).

#### 2. SLOCalculator
- `compute_compliance(workspace_id, tier, period_start, period_end)` → SLOCompliance
- Availability (% time service available, computed from downtime)
- Latency p95 from `request_records` table
- Error rate
- Error budget consumed + remaining hours/%
- Violations list

#### 3. ErrorBudgetTracker (hourly cron)
- `workspace_error_budget_remaining_hours` gauge
- `workspace_error_budget_remaining_pct` gauge
- `workspace_slo_violations_total` counter
- **< 25% remaining → warning notification + audit**
- **<= 0% remaining → critical notification + audit + refund eligibility mark (enterprise)**

#### 4. SLO/SLA Self-Service API

```python
GET /api/v1/workspace/{workspace_id}/slo?period=current_month
# RBAC: workspace_user enforced workspace_id scope
# Returns:
{
    'workspace_id': '...',
    'tier': 'standard',
    'period': 'current_month',
    'compliance': SLOCompliance {...},
    'slo_targets': SLODefinitions.SLOS[tier],
    'refund_eligible': bool,
}
```

#### 5. SLO Compliance Dashboard (Grafana)
- Overall compliance per workspace table
- Error budget remaining gauges
- SLO violations trends 24h/7d/30d
- Latency p95 vs target per workspace
- Availability rolling per workspace
- Refund-eligible enterprise workspaces alert

#### 6. SLO-Aware Alerting (Prometheus rules — 4)

```yaml
groups:
  - name: slo_alerts
    rules:
      - alert: WorkspaceSLOAvailabilityBreach
        expr: |
          (1 - (sum(rate(for3s_request_total{status="error"}[1h])) by (workspace_id)
                / sum(rate(for3s_request_total[1h])) by (workspace_id))) * 100
          < on(workspace_id) for3s_workspace_slo_availability_target * 100
        for: 5m
        labels: { severity: critical, slo: availability }
      
      - alert: WorkspaceSLOLatencyBreach
        expr: |
          histogram_quantile(0.95,
            sum(rate(for3s_request_e2e_latency_seconds_bucket[5m])) by (workspace_id, le)
          ) > on(workspace_id) for3s_workspace_slo_latency_target_seconds
        for: 5m
        labels: { severity: warning, slo: latency_p95 }
      
      - alert: WorkspaceErrorBudgetExhausted
        expr: for3s_workspace_error_budget_remaining_pct <= 0
        for: 1m
        labels: { severity: critical, slo: error_budget }
      
      - alert: WorkspaceErrorBudgetLow
        expr: for3s_workspace_error_budget_remaining_pct < 25
        for: 15m
        labels: { severity: warning, slo: error_budget }
```

#### 7. ChannelSLOTracker
- `channel_slo_compliant` gauge per channel + workspace
- Hourly check compute p95 last 1h vs target

### Audit events nuevos

- `slo_compliance_computed`
- `error_budget_low_warning` (< 25%)
- `error_budget_exhausted` (<= 0%, critical)
- `slo_violation_detected`
- `workspace_slo_query_executed`
- `refund_eligible_marked`

### Metrics Prometheus

- `workspace_slo_availability_pct`
- `workspace_slo_latency_p95_seconds`
- `workspace_slo_error_rate_pct`
- `workspace_error_budget_remaining_hours`
- `workspace_error_budget_remaining_pct`
- `workspace_slo_violations_total` (workspace_id, tier, metric)
- `channel_slo_compliant` (channel, workspace_id)

### Foundation

- 8.4.2 Alerts (SLO alerts integrated)
- 8.4.3 Incident management (SLO violations = incidents)
- R9 Compliance reports (SLO included)

---

## 8.4.2 — Alerts Aggregation Cross-System

**Decisión LOCKED:** **C — Alertmanager + custom aggregator unificado**

### 8 Components

#### 1. ALERTMANAGER (Prometheus standard)

```yaml
# observability/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m

route:
  receiver: 'for3s-aggregator'
  group_by: ['workspace_id', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  routes:
    - matchers: [severity = critical]
      receiver: 'for3s-aggregator-critical'
      continue: true

receivers:
  - name: 'for3s-aggregator'
    webhook_configs:
      - url: 'http://for3s-app:8000/api/v1/alerts/ingest'
        send_resolved: true

inhibit_rules:
  - source_matchers: [severity = critical]
    target_matchers: [severity = warning]
    equal: ['workspace_id', 'alertname']
```

#### 2. CUSTOM ALERT INGESTOR (UnifiedAlert format)

Cross-system sources:
- `ingest_prometheus_webhook` (Alertmanager)
- `ingest_microglia_alert` (eval failures)
- `ingest_skills_alert` (no-go DMN blocks)
- Extensible per source

```python
@dataclass
class UnifiedAlert:
    alert_id: str               # UUID
    source_system: str           # prometheus | microglia | skills | p5_cap | ...
    alert_name: str
    severity: str                # info | warning | critical
    category: str                # slo | cost | quality | security | capacity
    workspace_id: Optional[str]
    identity_id: Optional[str]
    trace_id: Optional[str]
    source_node: Optional[str]
    title: str
    description: str
    labels: dict[str, str]
    annotations: dict[str, str]
    starts_at: datetime
    ends_at: Optional[datetime]
    status: str                  # firing | resolved
    fingerprint: str             # for dedup (SHA-256)
    group_key: str               # for grouping
```

#### 3. DEDUPLICATION ENGINE (Redis)
- Window 15 minutos
- Counter track frequency
- Suppress duplicates

#### 4. GROUPING ENGINE (Redis sorted sets)
- Window 30s o 5 alerts max
- Per workspace + severity
- Flush trigger

#### 5. CASCADE DETECTOR (3 patterns conocidos)

| Cascade name | Sequence | Message |
|---|---|---|
| `llm_gateway_failure_cascade` | LLMGatewayErrorRateHigh → MicrogliaEvalScoreDropped → WorkspaceSLOLatencyBreach | LLM Gateway failure cascading to eval scores and SLO |
| `cost_spike_cascade` | WorkspaceBurnRateAnomaly → WorkspaceP5CapWarning → WorkspaceP5CapBlock | Cost spike progressing to P5 cap block |
| `capacity_exhaustion_cascade` | NodeSaturationHigh → NodeQueueDepthHigh → WorkspaceSLOLatencyBreach | Capacity exhaustion impacting SLO |

#### 6. ROUTING RULES ENGINE (6 rules)

| Priority | Rule | Matchers | Destinations |
|---|---|---|---|
| 1 | critical_to_brian | `severity=critical` | brian_telegram |
| 1 | security_to_brian | `category=security` | brian_telegram + security_dashboard |
| 2 | capacity_to_brian | `category=capacity` | brian_telegram + capacity_dashboard |
| 2 | slo_to_workspace_owner | `slo=availability` | brian_telegram + workspace_owner_notification |
| 3 | quality_to_digest | `category=quality, severity=warning` | brian_email_digest |
| 99 | default_to_audit | (all) | audit_only |

#### 7. SILENCING + ACK TRACKER
- `create_silence(matchers, duration_minutes, created_by, reason)` → maintenance windows
- `acknowledge(alert_id, ack_by, notes)` → stops escalation
- Audit trail completo

#### 8. ESCALATION POLICY ENGINE

| Severity | Level 0 (t+0) | Level 1 (t+15min) | Level 2 (t+30min) |
|---|---|---|---|
| critical | brian_telegram | + brian_email | + brian_sms |

- Arq scheduled jobs
- Cancel if acked or resolved

### Flow Ingestion → Delivery (10 steps)

1. Source emits alert (Prometheus, Microglia, Skills, etc)
2. AlertIngestor → UnifiedAlert
3. SilencingService.is_silenced? → drop si yes
4. DeduplicationEngine.is_duplicate? → suppress + count
5. GroupingEngine.add_to_group → wait/flush
6. CascadeDetector.detect_cascade → annotate
7. RoutingRulesEngine.route → destinations
8. NotificationRouter.send → Telegram/Email/etc
9. EscalationPolicyEngine.schedule → si critical
10. AuditLogger.log

### REST API endpoints

- `POST /api/v1/alerts/ingest` (Alertmanager webhook)
- `GET /api/v1/alerts` (list active)
- `GET /api/v1/alerts/{id}`
- `POST /api/v1/alerts/{id}/ack`
- `POST /api/v1/alerts/silences`
- `GET /api/v1/alerts/silences`
- `DELETE /api/v1/alerts/silences/{id}`

### Audit events nuevos

- `alert_ingested`
- `alert_deduplicated` (with count)
- `alert_grouped` (with group_key)
- `alert_cascade_detected`
- `alert_routed` (destinations)
- `alert_silenced`
- `alert_acknowledged`
- `alert_escalated` (level)
- `alert_silence_created`

### Metrics

- `alerts_ingested_total` (source_system, severity, category)
- `alerts_deduplicated_total`
- `alerts_grouped_total`
- `alerts_cascades_detected_total` (cascade_name)
- `alerts_routed_total` (destination)
- `alerts_acknowledged_total`
- `alerts_escalated_total` (level)
- `silences_active_total`

---

## 8.4.3 — Incident Management

**Decisión LOCKED:** **C — Lifecycle + runbooks + postmortem + status + MTTR**

### 7 Components

#### 1. INCIDENT LIFECYCLE ENGINE

**7 states:** `open` → `investigating` → `identified` → `monitoring` → `resolved` → `postmortem` → `closed`

**4 severity levels:**

| Severity | Description |
|---|---|
| `sev1` | Critical (full outage workspace tier) |
| `sev2` | High (partial degradation) |
| `sev3` | Medium (single feature affected) |
| `sev4` | Low (cosmetic, minor) |

Auto-create from critical/cascade alerts via `AlertToIncidentBridge`. Dedupe per fingerprint (append alert to existing incident).

```python
@dataclass
class Incident:
    id: str
    title: str
    description: str
    severity: IncidentSeverity
    state: IncidentState
    triggered_by_alert_ids: list[str]
    cascade_pattern: Optional[str]
    affected_workspaces: list[str]
    affected_components: list[str]
    assigned_to: Optional[str]
    created_by: str
    started_at: datetime
    acknowledged_at: Optional[datetime]
    identified_at: Optional[datetime]
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    mttr_seconds: Optional[float]
    mtta_seconds: Optional[float]
    runbook_id: Optional[str]
    postmortem_id: Optional[str]
    error_budget_consumed_minutes: float
    slo_violations_caused: list[str]
```

#### 2. ONCALL ROTATION (v1 single owner Brian)

```python
class OncallRotation:
    async def get_current(self) -> User:
        # v1: Brian único
        return await user_repo.get_by_id('brian_lopez')
    
    async def schedule_rotation(self, ...):
        # v2: rotation schedule (post-MVP)
        pass
```

#### 3. RUNBOOKS LIBRARY (4+ pre-built starter)

| Runbook ID | Alert | Severity | ETA |
|---|---|---|---|
| `rb_p5_cap_block` | WorkspaceP5CapBlock | sev2 | 30 min |
| `rb_error_budget_exhausted` | WorkspaceErrorBudgetExhausted | sev1 | 60 min |
| `rb_llm_gateway_errors` | LLMGatewayErrorRateHigh | sev2 | 15 min |
| `rb_audit_chain_violation` | AuditChainIntegrityViolation | sev1 | 240 min (4h) |

Extensible per alert type. Cada runbook tiene `steps` numerados con `commands` y `options`.

#### 4. TIMELINE TRACKER

- Chronological entries per incident
- Actor + action + details + commands_executed
- Audit log integration (`incident_timeline_entry_added`)

#### 5. STATUS PAGE (Public)

- Affected components published
- Public severity terminology (`major outage` / `partial outage` / `degraded performance` / `minor issue`)
- Sanitized root cause (no internal IPs, etc)
- Workspace owner notifications

#### 6. POSTMORTEM TEMPLATE ENGINE

Auto-template generado con 7 sections:

1. **summary** (title + severity + duration + affected + cascade)
2. **timeline** (entries from timeline_tracker)
3. **root_cause** (5 whys template + placeholder)
4. **detection** (detected_via + time_to_detect + could_be_faster)
5. **response** (runbook_used + runbook_effective + manual_actions)
6. **slo_impact** (error budget consumed + SLO violations caused)
7. **lessons_learned** (what_went_well + what_went_wrong + where_we_got_lucky)
8. **action_items** (recommended + custom)

Owner fills + submit. Audit trail.

#### 7. MTTR/MTBF METRICS

```python
incident_mttr_seconds = Histogram(
    'for3s_incident_mttr_seconds',
    labelnames=['severity'],
    buckets=[60, 300, 900, 1800, 3600, 7200, 14400, 28800, 86400],
)

incident_mtta_seconds = Histogram(
    'for3s_incident_mtta_seconds',
    labelnames=['severity'],
    buckets=[30, 60, 300, 900, 1800, 3600],
)

incidents_active_total = Gauge(
    'for3s_incidents_active_total',
    labelnames=['severity', 'state'],
)

incidents_created_total = Counter(
    'for3s_incidents_created_total',
    labelnames=['severity', 'cascade'],
)

incidents_error_budget_consumed_minutes = Counter(
    'for3s_incidents_error_budget_consumed_minutes',
    labelnames=['workspace_id'],
)

postmortems_pending_total = Gauge(
    'for3s_postmortems_pending_total',
)
```

### REST API endpoints (11)

- `POST /api/v1/incidents` (manual create)
- `GET /api/v1/incidents` (list)
- `GET /api/v1/incidents/{id}` (detail)
- `POST /api/v1/incidents/{id}/ack`
- `POST /api/v1/incidents/{id}/state`
- `POST /api/v1/incidents/{id}/resolve`
- `POST /api/v1/incidents/{id}/timeline`
- `GET /api/v1/runbooks/{alert_name}`
- `GET /api/v1/postmortems/{id}`
- `POST /api/v1/postmortems/{id}/submit`
- `GET /api/v1/status-page` (public)

### Audit events nuevos (11)

- `incident_created`
- `incident_acknowledged`
- `incident_state_changed`
- `incident_resolved`
- `incident_timeline_entry_added`
- `incident_runbook_executed_step`
- `status_page_incident_published`
- `status_page_resolution_published`
- `postmortem_template_created`
- `postmortem_submitted`
- `incident_closed`

### Foundation

- R9 Security incident response (extiende runbooks)
- R10 Deploy incident management
- **R8 closure** ⭐

---

## Cobertura Grafo Maestro §6.5 (closure)

| §6.5 spec | B4 cobertura |
|---|---|
| SLO/SLA tracking | ✅ 8.4.1 framework + tiers + self-service |
| Alert management centralizado | ✅ 8.4.2 AM + custom unificado |
| Incident management | ✅ 8.4.3 lifecycle + runbooks + postmortem |
| Capacity SLO-aware decisions (Pilar 2 §7.5) | ✅ Error budget + 4 alerting rules |

**R8 CIERRE 100% — Observabilidad Completa entregada.**