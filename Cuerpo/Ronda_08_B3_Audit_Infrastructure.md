# Ronda 8 — Bloque 3 — Audit Infrastructure (GM §6.4 Literal)

**Sub-documento de R8.** Detalle implementación 3/3 sub-temas LOCKED.

**Master:** [Ronda_08_Observabilidad_Completa.md](Ronda_08_Observabilidad_Completa.md)
**Estatus:** ✅ COMPLETO (3/3 sub-temas LOCKED)
**Fecha cierre:** 2026-06-08

---

## Tabla de sub-temas LOCKED

| Sub-tema | Decisión | Componentes |
|---|---|---|
| 8.3.1 Audit Chain Criptográfico | C — Chain + triple redundancy + RBAC | 8 components |
| 8.3.2 Retention Policies | C — Multi-tier + GDPR pseudonymization | 8 components |
| 8.3.3 Audit Query Engine | C — Completo + reports + verification | 7 components |

---

## 8.3.1 — Audit Chain Criptográfico

**Decisión LOCKED:** **C — Chain + triple redundancy + RBAC (GM §6.4 LITERAL)**

### Schema Postgres

```sql
CREATE TABLE audit_events (
    id BIGSERIAL PRIMARY KEY,
    hash_prev TEXT NOT NULL,           -- SHA-256 prev event
    hash_self TEXT NOT NULL,           -- SHA-256 this event
    sequence_number BIGINT NOT NULL UNIQUE,  -- monotonic
    event_type TEXT NOT NULL,
    workspace_id UUID NOT NULL,        -- multi-tenant
    identity_id UUID,                  -- attribution
    trace_id UUID,                     -- Tempo correlation
    payload JSONB NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('info', 'warning', 'critical')),
    source_node TEXT,
    source_component TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at_ns BIGINT NOT NULL      -- nanosecond precision
);
```

### 8 Components

#### 1. AuditEventChain (compute_hash + verify_chain_integrity)

```python
class AuditEventChain:
    @staticmethod
    def compute_hash(hash_prev, sequence_number, event_type, workspace_id,
                     identity_id, payload, created_at_ns) -> str:
        content = {
            'hash_prev': hash_prev,
            'sequence_number': sequence_number,
            'event_type': event_type,
            'workspace_id': workspace_id,
            'identity_id': identity_id,
            'payload': payload,
            'created_at_ns': created_at_ns,
        }
        canonical = json.dumps(content, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_chain_integrity(events) -> ChainVerification:
        # Verify hash_self + chain_link + sequence_number gaps
        ...
```

#### 2. AuditLogger (insert with chain)

- `_sequence_lock` para chain integrity
- Genesis event `hash_prev='GENESIS'`
- Sequence_number monotonic increment
- Hash compute + Postgres insert + WAL append

#### 3. POSTGRES TRIGGERS INMUTABILIDAD (TRIPLE GUARD)

```sql
CREATE OR REPLACE FUNCTION audit_events_prevent_modification()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'audit_events table is INMUTABLE: % operation not allowed', TG_OP;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_events_no_update
    BEFORE UPDATE ON audit_events FOR EACH ROW
    EXECUTE FUNCTION audit_events_prevent_modification();

CREATE TRIGGER audit_events_no_delete
    BEFORE DELETE ON audit_events FOR EACH ROW
    EXECUTE FUNCTION audit_events_prevent_modification();

CREATE TRIGGER audit_events_no_truncate
    BEFORE TRUNCATE ON audit_events FOR EACH STATEMENT
    EXECUTE FUNCTION audit_events_prevent_modification();

REVOKE INSERT ON audit_events FROM PUBLIC;
GRANT INSERT ON audit_events TO for3s_app_role;
```

#### 4. WALWriter (SECONDARY redundancy)

- Daily rotation `audit-YYYY-MM-DD.wal`
- JSON line append + `fsync` para durabilidad
- `aiofiles` async

#### 5. R2 ARCHIVE COLD STORAGE (TERTIARY)

- Detalles en 8.3.2 retention policies

#### 6. RBAC ROW-LEVEL SECURITY (3 roles)

```sql
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY audit_admin_read ON audit_events
    FOR SELECT TO for3s_admin_role USING (true);

CREATE POLICY audit_workspace_read ON audit_events
    FOR SELECT TO for3s_workspace_role
    USING (workspace_id = current_setting('app.current_workspace_id')::UUID);

CREATE POLICY audit_compliance_read ON audit_events
    FOR SELECT TO for3s_audit_reader_role USING (true);
```

#### 7. ChainVerificationJob

- Daily 2 AM sample 1000 random events
- Critical alert si tampering detected
- Full verification on-demand

#### 8. Metrics Prometheus

- `audit_events_total` (event_type, severity)
- `audit_chain_verification_total` (status)
- `audit_chain_verification_duration_seconds`
- `audit_wal_write_duration_seconds`

### Usage integration sistema-wide

- R8 8.1.3 P5CapEnforcer events
- R5 5.4.x DMN decisions
- R5 Microglia eval blocks
- R6 LLM Gateway cost events
- R7 Identity actions

### Audit events nuevos

- `audit_chain_integrity_violation` (critical)
- `audit_chain_verification_completed`
- `audit_wal_rotation_completed`
- `audit_rbac_access_denied`

### Performance

- ~1μs per SHA-256 hash (negligible)
- `_sequence_lock` corto (insert only)
- WAL fsync ~ms (durabilidad)

### Compliance ready

- SOC2 audit trail provable
- GDPR data lineage trackable
- Forensics post-incident confiable

---

## 8.3.2 — Retention Policies Long-Term

**Decisión LOCKED:** **C — Multi-tier + GDPR pseudonymization**

### 3 tiers

| Tier | Storage | Retention | Query Latency | Cost |
|---|---|---|---|---|
| **Hot** | Postgres partition | 90 días | <50ms | $$$ |
| **Warm** | Postgres audit_events_archive | 91-365 días | <500ms | $$ |
| **Cold** | R2 .jsonl.gz | > 365 días (perpetuo) | seconds | $ |

### GDPR Pseudonymization (view-based, NO chain break)

```sql
CREATE TABLE audit_events_pseudonymized (
    identity_id UUID PRIMARY KEY,
    pseudonym TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE VIEW audit_events_safe AS
SELECT
    e.id, e.hash_prev, e.hash_self, e.sequence_number,
    e.event_type, e.workspace_id,
    CASE
        WHEN p.identity_id IS NOT NULL THEN
            ('00000000-0000-0000-0000-' || p.pseudonym)::UUID
        ELSE e.identity_id
    END AS identity_id,
    e.trace_id,
    CASE
        WHEN p.identity_id IS NOT NULL THEN
            jsonb_set(e.payload, '{pseudonymized}', 'true')
        ELSE e.payload
    END AS payload,
    e.severity, e.source_node, e.source_component,
    e.created_at, e.created_at_ns
FROM audit_events e
LEFT JOIN audit_events_pseudonymized p ON e.identity_id = p.identity_id;
```

### 8 Components

1. **Partitioned table Postgres** (monthly auto-create via PartitionAutoCreator weekly Sunday)
2. **audit_events_archive** (warm table)
3. **HotToWarmArchiver** (cron monthly 1st 3 AM): copy + verify chain + drop hot partition
4. **WarmToColdArchiver** (cron monthly 2nd 3 AM): export day .jsonl.gz + SHA-256 manifest + R2 upload + delete warm
5. **ColdStorageRestorer** (lazy on-demand): fetch + verify SHA-256 + decompress + filter workspace
6. **GDPRPseudonymizer** (on-demand, no cron): stable pseudonym SHA-256(identity_id + salt)
7. **PartitionAutoCreator** (weekly Sunday)
8. **RetentionSizeMonitor** (daily check)

### Chain integrity per tier transition

- Verified hot → warm transition
- Verified warm → cold transition (manifest SHA-256)
- Verified on cold restore
- Critical alert si tampering detected

### Metrics

- `audit_partition_events_total` (per partition + tier)
- `audit_archive_events_total`
- `audit_cold_export_events_total`
- `audit_cold_restore_events_total`
- `audit_storage_size_bytes` (per tier)
- `gdpr_pseudonymizations_total`

### Audit events nuevos

- `audit_archive_chain_violation` (critical)
- `audit_partition_archived`
- `audit_cold_export_chain_violation` (critical)
- `audit_day_cold_exported`
- `audit_cold_restore_completed`
- `gdpr_pseudonymization_completed` (warning)

---

## 8.3.3 — Audit Query Engine

**Decisión LOCKED:** **C — Completo + reports + verification**

### 7 Components

#### 1. UNIFIED QUERY API

```python
@dataclass
class AuditQuery:
    workspace_id: Optional[str] = None
    identity_id: Optional[str] = None
    event_type: Optional[str] = None
    event_type_pattern: Optional[str] = None
    severity: Optional[list[str]] = None
    source_node: Optional[str] = None
    trace_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    payload_filters: dict[str, Any] = field(default_factory=dict)
    limit: int = 100
    offset: int = 0
    order_by: str = 'created_at'
    order_direction: str = 'DESC'
    include_hot: bool = True
    include_warm: bool = True
    include_cold: bool = False     # default off (expensive)
    use_safe_view: bool = True     # GDPR pseudonymization
```

#### 2. CROSS-TIER QUERY EXECUTOR
- include_hot/warm/cold flags
- Smart restore planner pre-cold
- Merge results sorted

#### 3. EXPORT ENGINE
- Formats: JSON · CSV · JSONL
- `include_chain_proof` option (cryptographic verification embedded)

#### 4. COMPLIANCE REPORTS TEMPLATES (6 pre-built)

| Template | Sections | Audience |
|---|---|---|
| `soc2_quarterly` | critical events + security + chain integrity + enforcement actions | admin |
| `gdpr_data_access` | per identity full trail | admin |
| `workspace_activity_monthly` | per workspace summary | workspace owner |
| `critical_events_summary` | severity=critical aggregation | admin |
| `identity_audit_trail` | per identity all events | admin |
| `cost_attribution_monthly` | cost breakdown per workspace+identity+node | admin |

#### 5. CHAIN VERIFICATION API (USER-FACING)

```python
# Verify single event with cryptographic proof
GET /api/v1/audit/verify/{event_id}
Returns: EventVerification {
    hash_self_valid: bool,
    chain_link_valid: bool,
    is_authentic: bool,
    verified_at_ns: int,
}

# Verify range (admin only for > 1000 events)
POST /api/v1/audit/verify-range
```

#### 6. SMART RESTORE PLANNER (cost-aware)

- R2 cost estimation per query ($0.00036/1K GET requests)
- events_estimate based avg_per_day
- **Confirmación requerida > $5 estimated cost**
- Approximate duration estimate

#### 7. MATERIALIZED VIEWS

```sql
CREATE MATERIALIZED VIEW audit_daily_summary AS
SELECT DATE(created_at) AS day, workspace_id, event_type, severity,
       COUNT(*) AS event_count
FROM audit_events
GROUP BY DATE(created_at), workspace_id, event_type, severity;

CREATE MATERIALIZED VIEW audit_critical_summary AS
SELECT DATE(created_at) AS day, workspace_id, event_type,
       COUNT(*) AS event_count,
       array_agg(DISTINCT source_node) AS source_nodes
FROM audit_events
WHERE severity = 'critical'
GROUP BY DATE(created_at), workspace_id, event_type;

-- Refresh nightly CONCURRENTLY via Arq cron
```

### REST API endpoints

- `POST /api/v1/audit/query`
- `POST /api/v1/audit/export?format=json|csv|jsonl`
- `POST /api/v1/audit/reports/{template_name}`
- `GET /api/v1/audit/verify/{event_id}`
- `POST /api/v1/audit/verify-range`

### RBAC enforcement

- `workspace_user` → forced workspace_id scope
- `admin` → all access
- `audit_reader` → read all (compliance)
- Large range verification → admin only
- SOC2/GDPR reports → admin only

### Audit events nuevos

- `audit_query_executed`
- `audit_export_completed`
- `audit_chain_verification_requested`
- `compliance_report_generated`
- `cold_restore_cost_confirmation_required`
- `audit_rbac_access_denied`

### Metrics

- `audit_queries_total` (caller_role, tier)
- `audit_query_duration_seconds`
- `audit_exports_total` (format)
- `compliance_reports_total` (template)
- `chain_verifications_requested_total`

---

## Cobertura Grafo Maestro §6.4 LITERAL

| §6.4 spec | B3 cobertura |
|---|---|
| Cryptographic chain inmutable | ✅ 8.3.1 SHA-256 hash_prev/hash_self |
| Triple redundancy storage | ✅ Postgres + WAL + R2 (8.3.1 + 8.3.2) |
| Retention policies multi-tier | ✅ 8.3.2 (90d hot + 1y warm + perpetuo cold) |
| Workspace_id RLS enforcement | ✅ 8.3.1 RLS 3 roles + 8.3.3 RBAC enforcement |
| Audit query engine completo | ✅ 8.3.3 (7 components + 6 templates) |
| Compliance-ready SOC2/GDPR | ✅ Templates pre-built + GDPR pseudonymization |