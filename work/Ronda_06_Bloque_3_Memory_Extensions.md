# Ronda 6 — Bloque 3 — Memory Extensions Transversales

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 3 de R6.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Estado original:** ✅ **3/3 sub-temas LOCKED**
**Master doc:** [Ronda_06_Memory_Stack_Extensions.md](work/Ronda_06_Memory_Stack_Extensions.md)
**Materializa:** Grafo Maestro Nodo 2 Hipocampo (extendido) + Nodo 5 Microglía (extendido) + Observability infraestructura

⚠️ **Flag global:** TODO R6 requires re-review pre-código (`project_r6_critical_pre_code_review.md`).

---

## 1. Propósito

Extensiones transversales que afectan TODOS nodos memoria. Sin estas:
- Sin time-aware queries → DMN tasks 5.4.2 (pattern_detection) imposibles
- Sin forgetting refined → compliance B2B fail (GDPR)
- Sin dashboard → cliente abandona (invisibility)

---

## 2. Sub-tema 6.3.1 — Time-aware Queries

### Decisión LOCKED: C — DSL completo (semantic + temporal + aggregation)

### TemporalQuery DSL

```python
class TemporalQuery(BaseModel):
    semantic_query: Optional[str] = None
    semantic_top_k: int = 10
    
    time_window: Optional[TimeWindow] = None
    order_by_time: Optional[str] = None
    order_by_relevance_decay: Optional[float] = None
    
    filters: dict = {}
    
    relative_to_event: Optional[RelativeToEvent] = None
    
    aggregate: Optional[Aggregation] = None
    
    output: str = 'episodes'


class TimeWindow(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    relative_to_now: Optional[str] = None  # '-30d', '+1h'


class RelativeToEvent(BaseModel):
    event_id: str
    relation: str  # 'before' | 'after' | 'around'
    window_seconds: int = 3600


class Aggregation(BaseModel):
    operation: str  # 'count' | 'sum' | 'avg' | 'trend' | 'compare'
    bucket_size: Optional[str] = None  # '1h' | '1d' | '1w' | '1m'
    group_by: list[str] = []
    metric_field: Optional[str] = None
    compare_periods: Optional[list[TimeWindow]] = None
```

### QueryBuilder dynamic SQL safe

```python
class TemporalQueryBuilder:
    """Build dynamic SQL con parameter binding."""
    
    async def build(self) -> tuple[str, list]:
        # SELECT clause per aggregation
        select_sql = self._build_select()
        
        # WHERE workspace_id (RLS reused)
        self.where_clauses.append("workspace_id = $1")
        self.params.append(self.workspace_id)
        
        # Temporal filters
        if self.query.time_window:
            await self._add_time_window()
        
        if self.query.relative_to_event:
            await self._add_relative_to_event()
        
        # Generic filters
        for field, value in self.query.filters.items():
            self.where_clauses.append(f"{field} = ${self._param(value)}")
        
        # Semantic + temporal decay
        if self.query.semantic_query:
            await self._add_semantic_search()
        
        return final_sql, self.params
```

### Use cases v1

- Compliance audit (Q1 decisions)
- Pattern detection (DMN 5.4.2 task)
- Skill ROI analysis (6.2.4 outcomes post-application)
- Trend reporting (dashboard 6.3.3)
- Debugging (before incident X)
- Comparison (week-over-week)
- Forecast (5.4.2 eval_regression base)

### Performance targets

- Range query workspace 30 días: **<50ms**
- Semantic + temporal top-20: **<100ms**
- Aggregation 90 días bucket weekly: **<200ms**

### Indexes Postgres migration

```sql
CREATE INDEX episodes_workspace_created ON episodes (workspace_id, created_at);
-- HNSW pgvector (R2 B2 reused):
CREATE INDEX episodes_embedding_hnsw ON episodes
    USING hnsw (embedding vector_cosine_ops)
    WITH (m=16, ef_construction=128);
```

### Audit event
- `hippocampus_temporal_query` (flags has_semantic/temporal/aggregation)

---

## 3. Sub-tema 6.3.2 — Forgetting Policies Refined

### Decisión LOCKED: C — Multi-dimensional + GDPR + custom rules

### 5-layer policy hierarchy

```
1. Custom rules workspace (highest priority)
2. Legal hold (immutable)
3. Workspace data type overrides
4. Workspace tier multipliers
5. Default data type policies (base)
```

### 10 DataTypes

```python
class DataType(str, Enum):
    EPISODE_GENERAL = "episode_general"
    EPISODE_DECISION = "episode_decision"
    EPISODE_AUDIT = "episode_audit"
    EPISODE_PII = "episode_pii"
    KG_FACT = "kg_fact"
    SKILL_METADATA = "skill_metadata"
    SKILL_BODY = "skill_body"
    PFC_PLAN = "pfc_plan"
    LLM_AUDIT_LOG = "llm_audit_log"
    CONVERSATION = "conversation"
```

### Default policies

```python
DEFAULT_POLICIES = {
    EPISODE_GENERAL: DataTypePolicy(
        active_days=90, archive_days=180, purge_days=395,
    ),
    EPISODE_DECISION: DataTypePolicy(
        active_days=180, archive_days=365, purge_days=730,
        legal_hold_capable=True,
    ),
    EPISODE_AUDIT: DataTypePolicy(
        active_days=365, archive_days=730, purge_days=2555,  # 7 años
        immutable=True,
        compliance_retention_years=7,
    ),
    EPISODE_PII: DataTypePolicy(
        active_days=30, archive_days=60, purge_days=90,
        redact_pii_after_days=30,
    ),
    KG_FACT: DataTypePolicy(
        active_days=365, archive_days=730, purge_days=1825,
    ),
    SKILL_METADATA: DataTypePolicy(
        active_days=365, archive_days=730, purge_days=1825,
    ),
    PFC_PLAN: DataTypePolicy(
        active_days=90, archive_days=180, purge_days=395,
    ),
    LLM_AUDIT_LOG: DataTypePolicy(
        active_days=730, archive_days=1825, purge_days=2555,
        immutable=True,
    ),
}
```

### Tier multipliers

```python
TIER_MULTIPLIERS = {
    'pilot_light': WorkspaceTierMultiplier(0.5, 0.5, 0.5),
    'standard': WorkspaceTierMultiplier(1.0, 1.0, 1.0),
    'enterprise': WorkspaceTierMultiplier(2.0, 3.0, 5.0),
}
```

### 10 ForgettingDecisions

```python
class ForgettingDecision(str, Enum):
    RETAIN = "retain"
    RETAIN_LEGAL_HOLD = "retain_legal_hold"
    RETAIN_IMMUTABLE = "retain_immutable"
    RETAIN_CUSTOM = "retain_custom"
    MARK_FOR_REVIEW = "mark_for_review"
    ARCHIVE = "archive"
    ARCHIVE_CUSTOM = "archive_custom"
    REDACT_PII = "redact_pii"
    PURGE = "purge"
    PURGE_CUSTOM = "purge_custom"
```

### GDPR workflow

```python
async def gdpr_right_to_be_forgotten(
    self, workspace_id, user_id, ticket_id, requested_by,
) -> GDPRDeletionResult:
    workspace = await workspace_repo.get(workspace_id)
    
    if workspace.forgetting_policy.right_to_be_forgotten_workflow == 'manual_review':
        await notification_service.send_to_brian(...)
        return GDPRDeletionResult(status='pending_review')
    
    # Automatic
    user_episodes = await episodes_store.find_by_user(workspace_id, user_id)
    legal_holds = [e for e in user_episodes if await self._has_legal_hold(e)]
    
    if legal_holds:
        await audit_logger.log(
            event_type='gdpr_request_partial_legal_hold',
            severity='HIGH',
        )
    
    deletable = [e for e in user_episodes if e not in legal_holds]
    for episode in deletable:
        await episodes_store.hard_delete(
            episode.id, reason=f'GDPR ticket {ticket_id}',
        )
    
    return GDPRDeletionResult(
        status='completed',
        deleted_count=len(deletable),
        legal_hold_preserved=len(legal_holds),
    )
```

### Microglía Extended (cron daily 3 AM)

```python
class MicrogliaExtended:
    async def daily_scan(self):
        for workspace in await workspace_repo.get_active():
            await self._scan_workspace(workspace)
    
    async def _scan_workspace(self, workspace):
        for data_type in DataType:
            episodes = await episodes_store.find_by_type(
                workspace.id, data_type, limit=10000,
            )
            actions_summary = defaultdict(int)
            for episode in episodes:
                decision = await forgetting_engine.evaluate_episode(
                    episode, workspace.id,
                )
                await self._apply_decision(episode, decision)
                actions_summary[decision.value] += 1
            
            if any(v > 0 for v in actions_summary.values()):
                await audit_logger.log(
                    event_type='microglia_workspace_scan',
                    payload={
                        'workspace_id': workspace.id,
                        'data_type': data_type.value,
                        'actions_summary': dict(actions_summary),
                    }
                )
```

### Cliente APIs self-service

```
GET    /workspace/{ws}/forgetting/policy
PATCH  /workspace/{ws}/forgetting/policy
POST   /workspace/{ws}/forgetting/custom_rule
POST   /workspace/{ws}/forgetting/gdpr_request
POST   /workspace/{ws}/forgetting/legal_hold
```

### Audit events
- `microglia_workspace_scan`
- `gdpr_request_pending_review / completed / partial_legal_hold`
- `episode_redacted_pii / purged`
- `legal_hold_applied`
- `forgetting_policy_updated`

---

## 4. Sub-tema 6.3.3 — Memory Observability Dashboard

### Decisión LOCKED: C — HTMX completo + actions + multi-vista

### Stack
- Jinja2 + HTMX (R3 B4 reused)
- Tailwind CSS (CDN)
- Chart.js (CDN)
- FastAPI router /dashboard + /admin

### Cliente dashboard structure (10 sections)

```
/dashboard (root) — overview workspace
├── /dashboard/memory
│   ├── episodes (list + filter)
│   ├── kg (Knowledge Graph view)
│   ├── temporal (time-aware queries UI)
│   ├── storage (usage breakdown)
│   └── health (regression detection 6.4.1)
├── /dashboard/skills
│   ├── go (list)
│   ├── no_go (list + approve flows)
│   ├── {id} (detail + score history)
│   └── lifecycle (visualization)
├── /dashboard/plans
│   ├── recent
│   ├── {id} (detail + confidence)
│   └── re_plans (history)
├── /dashboard/forgetting
│   ├── policy (view + edit)
│   ├── custom_rules
│   ├── gdpr (requests + new)
│   └── legal_holds (list)
├── /dashboard/dmn
│   ├── status
│   ├── history
│   ├── outputs (pending review)
│   └── settings (9 controls)
├── /dashboard/cost
│   ├── current
│   ├── forecast
│   ├── breakdown
│   └── anomalies
├── /dashboard/eval
│   ├── recent
│   ├── regression
│   └── golden_datasets
├── /dashboard/audit
│   ├── search
│   ├── export (CSV/JSON/PDF)
│   └── security_events
└── /dashboard/settings
```

### Brian admin dashboard (5 sections)

```
/admin/dashboard — global view
├── /admin/workspaces (todos workspaces, status, alerts)
├── /admin/system (health checks, DB perf, LLM status, DMN scheduler)
├── /admin/skills_approval (pending queues)
├── /admin/gdpr_requests
└── /admin/security_events
```

### DashboardMetricsAggregator

```python
class DashboardMetricsAggregator:
    async def get_workspace_overview(
        self, workspace_id,
    ) -> WorkspaceOverview:
        # Reusa 6.3.1 temporal queries + skill_store + R3 cost + DMN + GDPR
        ...
    
    async def get_admin_global_overview(self) -> AdminGlobalOverview:
        ...
```

### Actions 1-click HTMX

```html
<!-- Approve skill core promotion -->
<button hx-post="/admin/skills/{{ skill.id }}/approve_core"
        hx-confirm="Promote to core?"
        hx-swap="outerHTML">
    Approve Core
</button>

<!-- Toggle DMN per task -->
<input type="checkbox"
       hx-patch="/workspace/{{ ws.id }}/dmn/settings"
       hx-vals='{"dmn_pattern_detection_enabled": "true"}'
       hx-trigger="change"
       {% if settings.dmn_pattern_detection_enabled %}checked{% endif %}>
```

### Real-time HTMX SSE updates

```html
<div hx-ext="sse" sse-connect="/dashboard/sse/{{ ws.id }}">
    <div sse-swap="cost_update">...</div>
    <div sse-swap="skill_promoted">...</div>
    <div sse-swap="dmn_run_completed">...</div>
</div>
```

### Compliance exports

```python
@router.get('/dashboard/audit/export')
async def export_audit_compliance(
    workspace_id: str,
    format: str = 'csv',  # | 'json' | 'pdf'
    time_range: str = '90d',
    event_types: list[str] = None,
):
    query = TemporalQuery(
        time_window=TimeWindow(relative_to_now=f'-{time_range}'),
        filters={'event_type': event_types} if event_types else {},
        output='episodes',
    )
    audit_events = await hippocampus_time_query_engine.query(workspace_id, query)
    
    if format == 'csv':
        return StreamingResponse(generate_csv(audit_events.episodes), ...)
    elif format == 'json':
        return JSONResponse(content=[e.dict() for e in audit_events.episodes])
    elif format == 'pdf':
        return StreamingResponse(generate_pdf_report(...), ...)
    
    await audit_logger.log(event_type='audit_compliance_export', ...)
```

### Auth/RBAC

```python
class DashboardAccessControl:
    async def check_access(self, user, workspace_id, endpoint):
        if endpoint.startswith('/admin/'):
            return user.is_brian_admin
        if endpoint.startswith('/dashboard/') or endpoint.startswith('/workspace/'):
            return await self._user_has_workspace_access(user, workspace_id)
        return False
```

### Foundation R7 Frontend

- v1: minimal pages (overview + skills + dmn + cost + audit)
- v2 (R7 Frontend): expand all sections + advanced charts
- Mobile-responsive desde v1 (Tailwind)

### Audit events
- `dashboard_view` (per endpoint)
- `dashboard_action` (per 1-click)
- `audit_compliance_export`

---

## 5. Eventos audit Bloque 3

Total events nuevos R6 B3: **~15 events**

Temporal queries (6.3.1): hippocampus_temporal_query

Forgetting (6.3.2): microglia_workspace_scan, gdpr_request_pending_review/completed/partial_legal_hold, episode_redacted_pii/purged, legal_hold_applied, forgetting_policy_updated

Dashboard (6.3.3): dashboard_view, dashboard_action, audit_compliance_export

---

**Bloque 3 ✅ CERRADO — Memory extensions transversales + compliance B2B + observability v1. ⚠️ flag pre-código aplica.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_06_Bloque_3_Memory_Extensions.md`).
