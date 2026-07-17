# Ronda 8 — Bloque 2 — Grafana Dashboards (Brian Internal)

**Sub-documento de R8.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_08_Observabilidad_Completa.md](Ronda_08_Observabilidad_Completa.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED)
**Fecha cierre:** 2026-06-08

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | UID dashboard |
|---|---|---|
| 8.2.1 Operations Dashboard | C — Custom 5 sections + drill-down | for3s-operations |
| 8.2.2 Analytics Dashboard | C — 4 sections + drill-down | for3s-analytics |
| 8.2.3 Pilar 2 Scalability | C — 5 sections + capacity simulator | for3s-scalability |

---

## 8.2.1 — Operations Dashboard

**Decisión LOCKED:** **C — Custom 5 sections + drill-down**

**Dashboard:** "For3s OS Operations" (UID: `for3s-operations`)
**Refresh:** Sections 1-4 → 30s · Section 5 (trends) → 5min

### 5 secciones

#### Section 1 — System Status Overview (top, 30-sec glance)
- System Status (green/yellow/red — computed: any critical alert firing?)
- Active Requests (gauge real-time)
- Error Rate 5min (%)
- P95 Latency E2E
- Active Workspaces
- Cost Today (USD)

#### Section 2 — Nodes Health Table (11 nodos)
- Columns: status · req/s · error% · p95 · concurrent · saturation
- Row click → drill-down "For3s Node Detail"

#### Section 3 — Channels Distribution
- Time series req/s per channel (telegram / rest / github_webhook)
- Pie chart % distribution last 1h
- Stat panels error rate per channel

#### Section 4 — Active Incidents & Alerts
- Alert list Prometheus firing
- Workspace cap status table
- Critical audit events last 15min (Loki query)
- Error logs last 15min (Loki)

#### Section 5 — Performance Trends (24h)
- Latency p50/p95/p99 time series
- Requests/min
- Error rate
- Cost/hour
- Latency heatmap by hour

### Templating variables

- `$workspace_id` (all/filter)
- `$time_range` (5m/15m/1h/6h/24h, default 15m)
- `$node_name` (all/filter 11 nodos)
- `$channel` (all/telegram/rest/github_webhook)

### Color coding

- **Green:** <70% saturation, <1% error rate
- **Yellow:** 70-90% saturation, 1-5% error rate
- **Red:** >90% saturation, >5% error rate

### Drill-down dashboards

- **"For3s Node Detail"** (per nodo specialized metrics, recent traces Tempo, logs Loki, scaling indicators, audit events)
- **"Alert Detail"** (alert metadata, related metrics graph, related logs, related traces, suggested runbook 8.4.3)

### Grafana Explore integration

- Click trace_id → opens Tempo Explore
- Click metric panel → opens PromQL Explore
- Click log line → opens Loki Explore context

### Audit events

- `dashboard_viewed_by_brian` (track usage)
- `dashboard_drill_down_triggered`

---

## 8.2.2 — Analytics Dashboard

**Decisión LOCKED:** **C — 4 sections + drill-down**

**Dashboard:** "For3s OS Analytics" (UID: `for3s-analytics`)
**Refresh:** 5 min (BI ≠ ops real-time)

### 4 secciones business-focus

#### Section 1 — Cost Analytics
- Cost This Month vs Last Month (delta)
- **Pilar 2 §7.3 Compliance ($0.80 v1)** gauge
- Cost/day last 30d
- Top-5 cost per node bar
- Cost per channel pie
- Top-10 expensive workspaces table (drill-down)
- Top-10 expensive identities table
- Cost distribution pie (LLM + Storage + Embeddings + Infra)

#### Section 2 — Eval Scores (Microglia Quality)
- Avg eval score last 7d
- % outputs rejected
- Score distribution 30d
- Heatmap score by node + hour
- Worst-scored outputs (drill-down Tempo trace)
- WoW + MoM comparison

#### Section 3 — Skills Lifecycle (Pilar 3)
- Total skills generated 30d
- % applied
- % no-go (DMN blocked)
- Generated/day time series
- **Funnel:** Generated → Tested → Applied → Retired
- Top-10 most applied skills
- Top-10 retire candidates
- Per workspace bar chart

#### Section 4 — DMN Outcomes ⚠️ CAVEAT 5.4.2 refinement pending
- Total DMN decisions 24h
- % decisions correct (outcome tracked)
- Decisions per task type (8 tasks current)
- Decision latency p95
- Most frequent decision types
- Outcomes correlation

### Bottom — Workspaces Profitability Table

- Columns: workspace + tier + requests + cost + revenue + margin
- Color: green margin>30%, yellow 0-30%, red <0

### Templating variables

- `$time_range` (7d/14d/30d default/90d)
- `$workspace_id` (all/filter)
- `$node_name` (all/filter)
- `$channel` (all/filter)

### Annotations (Grafana)

- Deploys (annotation from CI/CD R10 future)
- Audit events critical (`_triggered`)
- Pilar 2 §7.3 violations
- Brian manual notes

### Panel alerts business-relevant

- Pilar 2 §7.3 compliance > 1.5x → alert Brian
- Eval score drop > 20% WoW → alert
- Skills applied rate < 30% → alert (Pilar 3 health)
- Workspace margin < 0 → alert

### Drill-down dashboards

- Workspace row → "Workspace Detail"
- Eval-failed → Tempo trace
- Skill → Skills lifecycle history
- DMN task type → outcomes correlation

### ⚠️ Caveat DMN Section

- **v1:** 8 DMN tasks current LOCKED
- **v2:** post-5.4.2 refinement
- **Memory tag:** `project_dmn_tasks_critical_refinement`

### Audit events

- `analytics_dashboard_viewed`
- `analytics_drill_down_triggered`
- `analytics_annotation_added_by_brian`

---

## 8.2.3 — Pilar 2 Escalabilidad Dashboard

**Decisión LOCKED:** **C — 5 sections + capacity simulator**

**Dashboard:** "For3s OS Pilar 2 Scalability" (UID: `for3s-scalability`)
**Refresh:** Sections 1-3 → 1 min · Section 4 → 1 hour · Section 5 → manual variable change

### 5 secciones

#### Section 1 — Scaling Strategies Overview (11 nodos table)

| Node | Strategy | Status | Replicas/Shards |
|---|---|---|---|
| workspace_gate | stateless+replicas | green | 3/3 |
| thalamus | stateless+replicas | green | 2/2 |
| pfc | worker_pool | yellow ⚠️ | 8/10 workers |
| multi_agent | worker_pool | green | 4/10 |
| hippocampus | sharded | green | 2 shards |
| kg | sharded | yellow ⚠️ hot | 3 shards |
| skills | worker_pool | green | 1 |
| microglia | stateless+replicas | yellow | 5/5 |
| cls | spot_eligible | green | 1 |
| dmn | stateless+replicas | green | 1 |
| neuromod | spot_eligible | green | 1 |

#### Section 2 — Per-Node Load Heatmap
- Heatmap nodes × time × saturation
- Top-3 saturated nodes time series
- Queue depth per node (current bar chart)
- Active concurrent per node (24h)
- Threshold lines (70% yellow, 90% red)

#### Section 3 — Cost Efficiency Per Node
- $/req per node bar (green<0.05 / yellow<0.20 / red>0.20)
- Cost/req trend 30d per node
- Scatter cost vs latency
- ROI table (cost_per_eval_point efficiency)
- Optimization candidates flagged

#### Section 4 — Capacity Forecast + Unit Economics
- Current users (v1 target 10)
- Projected users next month
- Pilar 2 §7.3 compliance gauge
- $/análisis trajectory (v1 $0.80 → v2 $0.20) annotation lines
- Capacity forecast multi-tier table:

| Users | Cost/mo | Replicas needed |
|---|---|---|
| 10 | $107 | (current) |
| 100 | $890 | PFC+2, Microglia+1 |
| 1,000 | $7,200 | PFC+5, MA+2, Microglia+3, KG+2 |
| 10,000 | $58,000 | All nodes +N |
| 100,000 | $480,000 | Full Pilar 2 §7 strategies |

#### Section 5 — Scaling Simulator (What-If)
- Variables: `$simulate_node` + `$simulate_replicas` + `$simulate_workload`
- Estimated latency (current vs projected)
- Estimated cost delta
- Estimated saturation
- Estimated capacity headroom
- Spot instance candidates table
- Sharding candidates table (hot workspaces)

### Pilar 2 §7.2 Strategies mapping

| Strategy | Nodes | Trigger | Action |
|---|---|---|---|
| Stateless + Replicas (HPA) | workspace_gate, thalamus, dmn, microglia | saturation > 70% sustained 5min | +1 replica |
| Worker Pool | pfc, multi_agent, skills | queue_depth > 50 sustained 3min | +N workers |
| Sharded | hippocampus, kg | hot shard > 2x avg | +1 shard + rebalance |
| Spot Eligible | cls, neuromod | cost > $20/mo per node | migrate spot |

### Annotations

- Scaling events (replicas changed)
- Worker pool resize events
- Shard added/removed events
- Spot migration events
- Pilar 2 §7.3 milestones ($0.80, $0.50, $0.20)

### Panel alerts

- Saturation > 90% sustained 3min → scale alert
- Queue depth > 50 sustained 5min → worker scale
- Hot shard detected → rebalance alert
- Cost per req > 2x baseline → optimization alert
- Pilar 2 §7.3 trajectory off-path → strategic alert

### Audit events

- `scalability_dashboard_viewed`
- `capacity_simulator_run`
- `scaling_recommendation_acknowledged`

---

## Provisioning Grafana

```yaml
# docker-compose.yml
grafana:
  image: grafana/grafana-oss:latest
  ports: ["3000:3000"]
  volumes:
    - grafana_data:/var/lib/grafana
    - ./observability/dashboards:/etc/grafana/provisioning/dashboards
    - ./observability/datasources:/etc/grafana/provisioning/datasources
  environment:
    - GF_AUTH_ANONYMOUS_ENABLED=false
    - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASS}
```

```yaml
# observability/datasources/datasources.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
  - name: Loki
    type: loki
    url: http://loki:3100
  - name: Tempo
    type: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogs: { datasourceUid: loki }
      tracesToMetrics: { datasourceUid: prometheus }
```

## Foundation

- 8.4.x SLO/SLA dashboards (workspace sub-set view)
- 8.4.3 Alert Detail dashboard con runbook integration
- R9 Security dashboard (post-Amygdala)
- R10 Deploy annotations