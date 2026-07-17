# Ronda 5 — Bloque 3 — Multi-Agent Network

**Sub-doc detallado del Bloque 3 de R5. ⭐ Bloque con hardening 18 capas defense-in-depth.**

**Owner:** Brian López
**Fecha:** 2026-06-06
**Status:** ✅ **4/4 sub-temas LOCKED**
**Master doc:** [Ronda_05_Orchestration_Multi_Agent.md](Ronda_05_Orchestration_Multi_Agent.md)
**Materializa:** Grafo Maestro Multi-Agent Network

---

## Tabla de contenidos

1. [Propósito del Bloque 3](#1-propósito)
2. [Sub-tema 5.3.1 — Agent Topology](#2-sub-tema-531)
3. [Sub-tema 5.3.2 — Agent Lifecycle HARDENED (18 capas)](#3-sub-tema-532)
4. [Sub-tema 5.3.3 — Inter-Agent Communication](#4-sub-tema-533)
5. [Sub-tema 5.3.4 — Sub-Agent Cost Control](#5-sub-tema-534)
6. [Eventos audit Bloque 3](#6-eventos-audit)

---

## 1. Propósito

Multi-Agent Network materializa la capacidad For3s OS de coordinar N specialists para tareas complejas.

P1 LOCKED: **Híbrido single + multi on-demand**.
- Default: single-agent por workspace (Pilot Light viable)
- On-demand: spawn N specialists cuando query justifica

Bloque 3 responde:
- ¿Cómo se estructuran? (5.3.1 topology)
- ¿Cómo nacen/viven/mueren? (5.3.2 lifecycle)
- ¿Cómo se hablan? (5.3.3 communication)
- ¿Cómo controlamos costo? (5.3.4 cost control)

---

## 2. Sub-tema 5.3.1 — Agent Topology

### Decisión LOCKED: C — Hub-and-spoke con specialists

```
PFC main (siempre activo, R5 B1)
   ↓ detecta multi-agent trigger
SPAWN HUB AGENT
   ↓ analyzes task → decide specialists needed
SPAWN N SPECIALISTS (paralelo, cap 5 v1)
   ↓ each: system_prompt + tools subset + LLM tier
SPECIALISTS EJECUTAN PARALELO
   ↓ reportan HUB via message bus (5.3.3)
HUB CONSOLIDA
   ↓ merge resultados, resolve conflicts
PFC RETURNS al cliente
```

### Specialists v1 registrados

```python
SPECIALISTS_V1 = {
    'code_analyzer': SpecialistDefinition(
        name='code_analyzer',
        system_prompt="""Eres un Code Analyzer experto.
        Lee código y reporta arquitectura, calidad,
        patterns, smells, mejoras.""",
        allowed_tools=['fs_read', 'github_get_file_contents'],
        llm_tier=LLMTier.OPUS,
    ),
    'security_auditor': SpecialistDefinition(
        name='security_auditor',
        system_prompt="""Eres Security Auditor OWASP Top 10.
        Escanea SQL injection, XSS, CSRF, IDOR, SSRF,
        auth deficiente, exposed secrets, dep vulns.
        Reporta severidad + remediation.""",
        allowed_tools=['fs_read', 'github_search', 'github_search_code'],
        llm_tier=LLMTier.OPUS,
    ),
    'test_generator': SpecialistDefinition(
        name='test_generator',
        system_prompt="""Eres Test Generator. Escribe tests
        unitarios, integration, edge cases.""",
        allowed_tools=['fs_read', 'fs_write'],
        llm_tier=LLMTier.SONNET,
    ),
    'performance_analyzer': SpecialistDefinition(
        name='performance_analyzer',
        system_prompt="""Eres Performance Analyzer. Identifica
        bottlenecks: O(n²), N+1 queries, blocking I/O,
        memory leaks. Sugiere optimizaciones impacto estimado.""",
        allowed_tools=['fs_read', 'github_get_file_contents'],
        llm_tier=LLMTier.SONNET,
    ),
    'doc_writer': SpecialistDefinition(
        name='doc_writer',
        system_prompt="""Eres Doc Writer técnico. Documentación
        clara, concisa basada en cambios código.""",
        allowed_tools=['fs_read', 'fs_write'],
        llm_tier=LLMTier.SONNET,
    ),
}
```

### Tool intersection

```python
effective_tools = (
    set(workspace.allowed_tools) &
    set(specialist.allowed_tools)
)
```

### Cap

- N specialists ≤ 5 v1 (workspace configurable)
- Extensible v2: workspace custom specialists

---

## 3. Sub-tema 5.3.2 — Agent Lifecycle HARDENED (18 capas)

### Decisión LOCKED: C — Asyncio task per specialist + 18 capas defense-in-depth

Base: `asyncio.create_task` per specialist (spawn ~50μs vs 10s Docker)

### 5-phase lifecycle

```
PHASE 1: SPAWN
   ↓ asyncio.create_task + lifecycle_id assignment
   ↓ audit: specialist_lifecycle_spawn

PHASE 2: EXECUTION (safety bounds)
   ↓ async with timeout (specialist.timeout_seconds)
   ↓ async with token_budget_guard (specialist.max_tokens)
   ↓ async with cancellation_propagation

PHASE 3: TERMINATION (5 outcomes)
   • SUCCESS → return result
   • TIMEOUT → SpecialistFailure('timeout')
   • TOKEN_EXCEEDED → SpecialistFailure('token_budget')
   • CANCELLED → propagate (cliente abort)
   • CRASH → SpecialistFailure('crash')

PHASE 4: CLEANUP (always finally)
   ↓ release DB connections, etc

PHASE 5: ARCHIVE
   ↓ persist metrics → feed 5.2.2 history-aware routing
```

### HARDENING CONTRA 1 — Aislamiento weaker (7 capas)

**CAPA 1: ContextVar isolation (Python nativo per-task)**
```python
_specialist_ctx: ContextVar[SpecialistContext] = ContextVar('specialist_context')

@asynccontextmanager
async def bind_specialist_context(ctx: SpecialistContext):
    token = _specialist_ctx.set(ctx)
    try:
        yield ctx
    finally:
        _specialist_ctx.reset(token)
```

**CAPA 2: Tools whitelist enforcement runtime (R4 4.1.2)**
```python
async def invoke_tool(self, tool_name, tool_args):
    ctx = get_current_specialist_context()
    if tool_name not in ctx.allowed_tools:
        await audit_logger.log(
            event_type='SECURITY_VIOLATION_tool_not_allowed',
            severity='HIGH',
        )
        raise ToolNotAllowedError(...)
```

**CAPA 3: KEK scoping (master queda main, specialist solo derived)**
```python
ctx.workspace_kek_derived = await kek_manager.derive_for_workspace(workspace.id)
# Master KEK NUNCA en specialist scope
# No hay método get_master_kek()
```

**CAPA 4: Postgres Row-Level Security**
```sql
ALTER TABLE workspace_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON workspace_data
USING (workspace_id = current_setting('app.current_workspace_id'));
```
```python
@asynccontextmanager
async def specialist_db_session():
    ctx = get_current_specialist_context()
    async with db_pool.acquire() as conn:
        await conn.execute(
            "SET LOCAL app.current_workspace_id = $1",
            ctx.workspace_id,
        )
        yield conn
```

**CAPA 5: Resource quotas (anyio Semaphore)**
- DB connection: max 2 per specialist
- Valkey connection: max 1 per specialist
- File descriptors: max 10 per specialist
- HTTP calls: max 5/sec per specialist (TokenBucket)

**CAPA 6: Mutation guards (default read-only + OCC)**
```python
async def update_with_occ(self, table, row_id, updates, expected_version):
    ctx = get_current_specialist_context()
    if not ctx.can_mutate:
        raise MutationNotAllowedError(...)
    # OCC check version
```

**CAPA 7: Runtime anomaly detection + emergency kill**
- > 10 tool calls/sec → kill
- > 50 total tool calls → kill
- Cross-workspace ID in args → SECURITY_ALERT + kill
- Alert oncall (R3 B4 observability)

### HARDENING CONTRA 2 — Blocking calls (5 capas)

**CAPA 1: Static check CI/CD**
- ruff banned-api: `requests`, `urllib.request`, `time.sleep`, `subprocess.*`
- AST scan: `open`, `json.load`, `pd.read_csv`
- CI bloquea merge

**CAPA 2: Tool Protocol async-only**
```python
@runtime_checkable
class AsyncTool(Protocol):
    name: str
    async def execute(self, args: dict) -> Any: ...

# Registry validation
if not inspect.iscoroutinefunction(tool.execute):
    raise ToolMustBeAsyncError(...)
```

**CAPA 3: anyio thread pool con CapacityLimiter aislado**
```python
class SyncInteropGuard:
    _SYNC_INTEROP_LIMITER = anyio.CapacityLimiter(20)

    @staticmethod
    async def run_sync(func, *args, **kwargs):
        return await anyio.to_thread.run_sync(
            lambda: func(*args, **kwargs),
            limiter=SyncInteropGuard._SYNC_INTEROP_LIMITER,
        )
```

**CAPA 4: Event loop stall detector (heartbeat background)**
- WARN: stall > 500ms → log + alert
- KILL: stall > 5000ms → cancel culprit task + alert critical

**CAPA 5: Process circuit breaker (graceful restart)**
- Si > 3 stalls/hour → drain + systemd restart

### HARDENING CONTRA 3 — Memory leaks (6 capas)

**CAPA 1: Weak references por design**
```python
self._active_specialists: weakref.WeakValueDictionary[uuid.UUID, asyncio.Task]
```

**CAPA 2: Resource bounds declarativos**
- BoundedCache wrapper forza `maxsize` + `ttl_seconds`
- CI lint banned: `@lru_cache(maxsize=None)`, `@cache`

**CAPA 3: Memory metrics realtime**
- tracemalloc + psutil + Prometheus
- `for3s_process_rss_bytes`, `for3s_specialist_memory_delta_bytes`, `for3s_cache_size_entries`

**CAPA 4: RSS threshold alert**
- WARN: 2GB RSS → alert
- CRITICAL: 4GB RSS → trigger restart preventivo

**CAPA 5: Restart preventivo (3 triggers)**
- MAX_REQUESTS_BEFORE_RESTART = 10,000
- MAX_UPTIME_HOURS = 24
- MAX_RSS_MB = 3,072
- systemd timer cada 6h randomized

**CAPA 6: Leak forensics automático**
```python
LEAK_THRESHOLD_MB = 50

async def with_leak_detection(self, specialist):
    snap_pre = tracemalloc.take_snapshot()
    try:
        result = await specialist.execute()
        return result
    finally:
        snap_post = tracemalloc.take_snapshot()
        diff = snap_post.compare_to(snap_pre, 'lineno')
        total_delta_mb = sum(s.size_diff for s in diff) / (1024*1024)
        if total_delta_mb > self.LEAK_THRESHOLD_MB:
            await audit_logger.log(
                event_type='LEAK_DETECTED_specialist',
                payload={'top_culprits': diff[:10], ...},
            )
```

### Resumen hardening

```
CONTRA              ANTES (mitigaciones)    DESPUÉS (defense-in-depth)
────────────────────────────────────────────────────────────────────
1. Aislamiento     2 mitigaciones papel    7 capas (cada suficiente)
2. Blocking calls  2 mitigaciones parcial  5 capas + circuit breaker
3. Memory leaks    2 mitigaciones genérico 6 capas + forensics

TOTAL: 18 capas defensivas
Overhead: ~5% runtime aceptable
Compliance B2B: audit per violación
```

---

## 4. Sub-tema 5.3.3 — Inter-Agent Communication

### Decisión LOCKED: C — asyncio.Queue + event broadcast

### MultiAgentMessageBus per batch

```python
class MultiAgentMessageBus:
    HUB_INBOX_MAXSIZE = 1000
    SPECIALIST_INBOX_MAXSIZE = 100
    MAX_MESSAGES_PER_SEC_PER_SPECIALIST = 50

    def __init__(self, batch_id, workspace_id, specialist_names):
        self.hub_inbox = asyncio.Queue(maxsize=self.HUB_INBOX_MAXSIZE)
        self.specialist_inboxes = {
            name: asyncio.Queue(maxsize=self.SPECIALIST_INBOX_MAXSIZE)
            for name in specialist_names
        }
        self.broadcast_event = asyncio.Event()
        self.broadcast_payload = None
        self._send_buckets = {
            name: TokenBucket(rate=self.MAX_MESSAGES_PER_SEC_PER_SPECIALIST, capacity=10)
            for name in specialist_names + ['hub']
        }
```

### 4 patrones soportados

```
PATRÓN 1: SPECIALIST → HUB
   Pydantic msg → hub_inbox.put()
   HUB loop: msg = await hub_inbox.get()

PATRÓN 2: HUB → SPECIALIST
   Pydantic msg → specialist_inboxes[name].put()
   Specialist checkpoint: self._check_inbox()

PATRÓN 3: SPECIALIST → SPECIALIST (peer ask_peer)
   correlation_id-based request-response

PATRÓN 4: HUB → ALL (broadcast)
   broadcast_payload + event.set()
   Specialists background listener: event.wait()
```

### 10 message types Pydantic v1

```python
class MessageType(str, Enum):
    PROGRESS = "progress"
    RESULT_PARTIAL = "result_partial"
    RESULT_FINAL = "result_final"
    ERROR = "error"
    CRITICAL_FINDING = "critical_finding"
    EXTRA_CONTEXT = "extra_context"
    CANCEL = "cancel"
    MODE_CHANGE = "mode_change"
    REQUEST_HELP = "request_help"
    HELP_RESPONSE = "help_response"


class MultiAgentMessage(BaseModel):
    from_: str = Field(alias='from')
    to: str
    type: MessageType
    payload: dict
    timestamp: float = Field(default_factory=time.time)
    batch_id: str
    correlation_id: Optional[str] = None
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
```

### Validations send

```python
async def send(self, msg: MultiAgentMessage):
    # Cross-batch detection (SECURITY)
    if msg.batch_id != self.batch_id:
        await audit_logger.log(
            event_type='SECURITY_VIOLATION_cross_batch_message',
            severity='CRITICAL',
        )
        raise CrossBatchMessageError(...)

    # Sender legítimo
    if msg.from_ != 'hub' and msg.from_ not in self.specialist_inboxes:
        raise InvalidSenderError(...)

    # Rate limit
    bucket = self._send_buckets.get(msg.from_)
    if bucket and not await bucket.try_acquire(1):
        raise MessageRateLimitExceededError(...)

    # Audit
    await audit_logger.log(
        event_type='multi_agent_message_sent',
        payload={'from': msg.from_, 'to': msg.to, 'type': msg.type.value},
    )

    # Route
    if msg.to == 'broadcast':
        self.broadcast_payload = msg
        self.broadcast_event.set()
    elif msg.to == 'hub':
        self._put_hub(msg)
    else:
        self._put_specialist(msg.to, msg)
```

### Critical_finding backpressure override

Si hub_inbox lleno y msg.type == CRITICAL_FINDING:
- Drop oldest non-critical
- Force put critical

### SpecialistMessenger API conveniente

```python
class SpecialistMessenger:
    @staticmethod
    async def report_progress(step, total, detail=''): ...

    @staticmethod
    async def report_critical_finding(severity, finding): ...

    @staticmethod
    async def ask_peer(peer_name, question) -> Optional[dict]:
        # Request-response con correlation_id + timeout 10s
        ...
```

### Foundation v2

Valkey backend agregable manteniendo misma API → cross-worker multi-agent.

---

## 5. Sub-tema 5.3.4 — Sub-Agent Cost Control

### Decisión LOCKED: C — Multi-layer enforcement 7 capas

### LAYER 1: Pre-flight check

```python
class MultiAgentCostGuard:
    SAFETY_BUFFER_RATIO = 1.3
    WARNING_THRESHOLD_RATIO = 0.5
    DEFAULT_MULTI_AGENT_BUDGET_RATIO = 0.30

    async def check_can_spawn(self, workspace_id, specialists_count, estimated_specialists):
        workspace = await get_workspace(workspace_id)
        multi_agent_remaining = await self._get_multi_agent_remaining(workspace_id)

        estimated = await self._estimate_total_cost(estimated_specialists)
        estimated_with_buffer = estimated * self.SAFETY_BUFFER_RATIO

        if specialists_count > workspace.max_specialists_per_request:
            return SpawnDecision.REJECT(reason='specialist_count_exceeds_limit')

        if estimated_with_buffer > multi_agent_remaining:
            return SpawnDecision.REJECT(reason='insufficient_multi_agent_budget')

        if estimated > multi_agent_remaining * self.WARNING_THRESHOLD_RATIO:
            return SpawnDecision.ALLOW_WITH_WARNING(...)

        return SpawnDecision.ALLOW()
```

### LAYER 2: Per-specialist budget

```python
class SpecialistBudgetGuard:
    DEFAULT_MAX_TOKENS_PER_SPECIALIST = 10_000
    MAX_LLM_CALLS_PER_SPECIALIST = 20

    async def record_llm_call(self, tokens_in, tokens_out):
        self.tokens_used += tokens_in + tokens_out
        self.calls_made += 1
        if self.tokens_used > self.max_tokens:
            raise SpecialistTokenBudgetExceeded(...)
        if self.calls_made > self.max_calls:
            raise SpecialistCallBudgetExceeded(...)
```

### LAYER 3: Real-time monitoring

```python
class MultiAgentCostMonitor:
    CHECK_INTERVAL_MS = 500
    EMERGENCY_ABORT_CAP_RATIO = 0.95
    WARNING_CAP_RATIO = 0.80

    async def monitor_batch(self, batch):
        while batch.active:
            total = sum(spec.cost_so_far for spec in batch.specialists)
            spent = await cost_tracker.get_monthly_spent_multi_agent(batch.workspace_id)
            projected = spent + total
            cap_ratio = projected / multi_agent_cap

            if cap_ratio > self.EMERGENCY_ABORT_CAP_RATIO:
                await self._trigger_emergency_abort(batch, reason='cap_imminent')
                return

            # Push status via 5.3.3 message bus
            await batch.message_bus.send(MultiAgentMessage(
                from_='cost_monitor', to='hub',
                type=MessageType.PROGRESS,
                payload={'cost_so_far': total, 'cap_ratio': cap_ratio},
                batch_id=batch.id,
            ))

            await asyncio.sleep(self.CHECK_INTERVAL_MS / 1000)
```

### LAYER 4: Circuit breaker

```python
async def _trigger_emergency_abort(self, batch, reason):
    await audit_logger.log(
        event_type='multi_agent_emergency_abort',
        payload={'reason': reason, 'cost_so_far': ...},
        severity='WARNING',
    )

    # Broadcast cancel via 5.3.3
    await batch.message_bus.send(MultiAgentMessage(
        from_='cost_monitor', to='broadcast',
        type=MessageType.CANCEL,
        payload={'reason': reason},
        batch_id=batch.id,
    ))

    # Cancel asyncio tasks (5.3.2 hardened cancellation)
    for spec in batch.specialists:
        if spec.task and not spec.task.done():
            spec.task.cancel()

    batch.aborted = True
    batch.abort_reason = reason
```

### LAYER 5: Partial results rescue

```python
class MultiAgentPartialResultsCollector:
    async def collect(self, batch) -> MultiAgentResult:
        completed = []
        partial = []
        cancelled = []

        for spec in batch.specialists:
            if spec.task.done():
                if spec.task.cancelled():
                    cancelled.append({'specialist': spec.name, 'cost_so_far': spec.cost_so_far})
                    if spec.partial_results:
                        partial.append({...})
                else:
                    try:
                        result = spec.task.result()
                        completed.append({...})
                    except Exception as e:
                        partial.append({...status: 'failed'})

        return MultiAgentResult(
            batch_id=batch.id,
            workspace_id=batch.workspace_id,
            total_cost=sum(s.cost_so_far for s in batch.specialists),
            aborted=batch.aborted,
            abort_reason=batch.abort_reason,
            completed_specialists=completed,
            partial_specialists=partial,
            cancelled_specialists=cancelled,
        )
```

### LAYER 6: Client visibility stream

```python
# SSE R3 B3 reused
async def stream_multi_agent_progress(batch_id):
    async for msg in message_bus.subscribe_hub(batch_id):
        if msg.type == MessageType.PROGRESS:
            yield ServerSentEvent(
                event='cost_update',
                data=json.dumps({
                    'cost_so_far': msg.payload['cost_so_far'],
                    'cap_ratio': msg.payload['cap_ratio'],
                })
            )
```

### LAYER 7: Workspace isolation

```python
DEFAULT_MULTI_AGENT_BUDGET_RATIO = 0.30  # 30% del cap P5 max

async def _get_multi_agent_remaining(self, workspace_id):
    workspace = await get_workspace(workspace_id)
    multi_agent_cap = workspace.p5_cap * (
        workspace.multi_agent_budget_ratio or self.DEFAULT_MULTI_AGENT_BUDGET_RATIO
    )
    spent = await cost_tracker.get_monthly_spent_multi_agent(workspace_id)
    return max(0, multi_agent_cap - spent)
```

Multi-agent budget separado de single-agent. Runaway no afecta otros budgets.

---

## 6. Eventos audit Bloque 3

**Lifecycle (5.3.2):**
- `specialist_lifecycle_spawn`
- `specialist_lifecycle_success` / `_timeout` / `_token_exceeded` / `_cancelled` / `_crash`
- `specialist_lifecycle_terminated`

**Security violations (5.3.2 hardened):**
- `SECURITY_VIOLATION_tool_not_allowed`
- `SECURITY_VIOLATION_mutation_blocked`
- `SECURITY_ALERT_cross_workspace_id_in_args`
- `SECURITY_EMERGENCY_specialist_killed`
- `LEAK_DETECTED_specialist`
- `event_loop_stall_warning` / `_critical`
- `process_circuit_breaker_triggered`
- `preventive_restart_triggered`

**Communication (5.3.3):**
- `multi_agent_message_sent`
- `message_dropped_inbox_full`
- `message_rate_limit_exceeded`
- `multi_agent_message_bus_shutdown`
- `SECURITY_VIOLATION_cross_batch_message`

**Cost control (5.3.4):**
- `multi_agent_spawn_pre_flight_decision`
- `multi_agent_emergency_abort`
- `multi_agent_cap_warning`
- `multi_agent_partial_results_returned`

---

**Bloque 3 ✅ CERRADO — Multi-Agent Network producción multi-tenant con 18 capas defensivas.**