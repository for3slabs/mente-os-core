# Ronda 7 — Bloque 2 — Output Gate (Pilar 1 Seguridad)

**Status:** current · **Type:** analysis · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** desde v1 (2026-07-30, ADR-029)

## Purpose

Ronda 7 — Bloque 2 — Output Gate (Pilar 1 Seguridad)


**Sub-doc detallado del Bloque 2 de R7.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Estado original:** ✅ **3/3 sub-temas LOCKED**
**Master doc:** [Ronda_07_Frontend_Channel.md](work/Ronda_07_Frontend_Channel.md)
**Materializa:** Grafo Maestro Output Gate (líneas 266-271) + OUTPUT layer (líneas 274-277) + Pilar 1 Seguridad

---

## 1. Propósito

Grafo Maestro líneas 266-271:
> "OUTPUT GATE (Seguridad + Trazabilidad)
> • Firma criptográfica del output
> • Trace completo: qué nodos decidieron
> • Encripta para entrega"

Y líneas 274-277:
> "OUTPUT (Usuario / API): QA Pack + Trace + Confidence + Audit"

Sin Output Gate, response es solo texto plano. Con Output Gate, response es documento legal digital firmable + structured + cross-channel.

---

## 2. Sub-tema 7.2.1 — Output Signing + Trace + Encrypt (C — Híbrido P2 LOCKED)

### Decisión LOCKED: C — Híbrido (pragmatic default + strict opt-in)

### 2 TIERS COEXISTEN

**TIER PRAGMATIC** (default 80% workspaces):
- HMAC-SHA256 signature (workspace shared secret)
- Trace básico (plan_id + nodes + confidence + cost)
- TLS 1.3 transport
- Overhead <10ms

**TIER STRICT** (enterprise opt-in):
- Ed25519 signature (workspace keypair, non-repudiation)
- Trace completo (every node decision + reasoning)
- AES-256-GCM payload encrypt (KEK R4 4.1.3 reused)
- Overhead 50-100ms
- Key rotation supported

### 5 Components

1. **OutputGate** (pipeline orchestrator)
2. **WorkspaceKeyManager** (HMAC + Ed25519 generation + rotation)
3. **SignatureStore** (long-term Postgres)
4. **OutputVerifier** (cliente SDK helper)
5. **TraceBuilder** (basic vs complete per tier)

### Pipeline 7 steps

```
1. Build trace per tier
2. Build OutputPayload
3. Sign (HMAC o Ed25519)
4. Encrypt opcional (strict tier)
5. Build SignedOutput
6. Persist long-term audit
7. Audit log event
```

### Postgres tables NEW (2)

```sql
CREATE TABLE workspace_signing_keys (
    workspace_id TEXT NOT NULL,
    key_type TEXT NOT NULL,
    key_version INT NOT NULL,
    public_key BYTEA,
    private_key_kid TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT NOW(),
    rotated_at TIMESTAMP,
    PRIMARY KEY (workspace_id, key_type, key_version)
);

CREATE TABLE output_signatures (
    response_id UUID PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    signature TEXT NOT NULL,
    signature_algorithm TEXT NOT NULL,
    tier TEXT NOT NULL,
    key_version INT NOT NULL,
    trace_hash TEXT NOT NULL,
    encrypted BOOLEAN DEFAULT false,
    channel TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Audit events (4)
- `output_signed`
- `workspace_keys_generated`
- `workspace_keys_rotated`
- `output_verification_failed`

### Stack reused
- R4 4.1.3 KEK hierarchy + AES-GCM
- R3 B3 SSE (channels)
- R4 4.3.1 audit

---

## 3. Sub-tema 7.2.2 — Response Format Estructurado (C — Pydantic + 4 renderers)

### 8 Pydantic Models

1. **QAPack** (root universal — Grafo Maestro literal)
2. **QAPackSection** (per content area)
3. **QAItem** (individual finding)
4. **Location** (file + line)
5. **QAPackAttachment** (file artifact)
6. **QAPackAction** (next-step CTA)
7. **Metadata** (ConfidenceMetadata + CostMetadata + PerformanceMetadata + TraceSummary)
8. **QAPackError**

### 4 Renderers

| Renderer | Channel | Format |
|---|---|---|
| TelegramRenderer | Telegram | Markdown max 4k chars + dashboard link |
| APIRenderer | REST API | JSON schema OpenAPI |
| GitHubRenderer | GitHub | Markdown collapsible details + suggestions |
| DashboardRenderer | Dashboard | HTML Jinja2 rich UI |

### QAPackRendererRegistry
Channel → renderer auto-select. Extensible v2.

### Output Pipeline End-to-End

```
1. PFCExecutionResult
2. QAPackBuilder.build() → QAPack
3. RendererRegistry.render_for_channel() → rendered
4. OutputGate.process_output() → SignedOutput (7.2.1)
5. DeliverableOutput (qa_pack + rendered + signed)
```

### Versioning
`qa_pack_version: "1.0"` field permite evolución:
- v1.x additive (no breaking)
- v2.x breaking (dual-period support)

### Multi-language ready
`language` field (en/es/pt). i18n templates Jinja2 + JSON locale files.

### Audit events (3)
- `qa_pack_built`
- `qa_pack_rendered`
- `qa_pack_version_mismatch`

### Stack reused
- R6 6.1.2 ConfidenceMetadata
- R3 4.4.2 CostMetadata
- R5 5.3 specialists output
- R3 B4 audit chain
- R2 B4 attachments storage

---

## 4. Sub-tema 7.2.3 — Streaming Output Unificado (C — 25+ events + 4 adapters)

### 25+ Stream Event Types

```python
class StreamEventType(str, Enum):
    # Lifecycle
    STREAM_START, STREAM_END, STREAM_ERROR, STREAM_CANCELLED, HEARTBEAT
    
    # PFC pipeline
    PLAN_GENERATED, PLAN_STEP_STARTED, PLAN_STEP_COMPLETED,
    PLAN_STEP_FAILED, PLAN_RE_PLAN_TRIGGERED, PLAN_COMPLETED
    
    # Skills
    SKILL_APPLIED, SKILL_FALLBACK_TO_PLANNING
    
    # Multi-agent
    SPECIALIST_SPAWNED, SPECIALIST_PROGRESS, SPECIALIST_COMPLETED,
    MULTI_AGENT_CONSOLIDATING
    
    # LLM (R3 B3 reused)
    TEXT_DELTA, TOOL_USE
    
    # Metadata
    CONFIDENCE_UPDATED, COST_UPDATE
    
    # QA Pack
    QA_PACK_SECTION_ADDED, QA_PACK_ITEM_FOUND, QA_PACK_FINAL
    
    # Final
    SIGNED_OUTPUT
```

### Stream Event Model

```python
class StreamEvent(BaseModel):
    event_id: str
    event_type: StreamEventType
    timestamp: float
    sequence_number: int
    payload: dict
    progress_percentage: Optional[float]  # 0-100
    stream_id: str
```

### StreamingExecutor
Wraps PFCExecutor + emits StreamEvents durante pipeline.

### 4 Channel Adapters

| Adapter | Channel | Strategy |
|---|---|---|
| SSEStreamAdapter | REST | text/event-stream + Cache-Control no-cache |
| TelegramStreamAdapter | Telegram | typing indicator + edited messages + rate limit 2s |
| GitHubStreamAdapter | GitHub | check_run progress + final PR comment |
| DashboardStreamAdapter | Dashboard | HTMX SSE swap per event type |

### Infrastructure
- **StreamCancellationManager**: is_disconnected check + abort
- **StreamHeartbeat**: 15s interval inyectado automático
- **Backpressure**: async iterator natural

### Progress + Cost tracking
- `progress_percentage` 0-100 per event
- Cumulative cost incremental updates
- Re-plan triggered events visibles

### Audit events (4)
- `stream_started`
- `stream_event_emitted` (sampled, no flood)
- `stream_cancelled_by_client`
- `stream_completed`

### Stack reused
- R3 B3 SSE infrastructure + heartbeat + cancellation
- R5 5.3.3 multi-agent message bus events
- R6 6.1.1 PFC plan events
- R6 6.1.3 confidence check loop events
- R7 7.2.2 QAPack final event
- R7 7.2.1 SignedOutput final event

---

## 5. Eventos audit Bloque 2

Total events nuevos R7 B2: **~11 events**

Output Signing (7.2.1): 4 events
Response Format (7.2.2): 3 events
Streaming (7.2.3): 4 events

---

**Bloque 2 ✅ CERRADO — Foundation Grafo Maestro Output Gate + Pilar 1 completo v1.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_07_Bloque_2_Output_Gate.md`).
