# Ronda 5 — Bloque 4 — DMN / Default Mode Network

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 4 de R5.**

**Owner:** Brian López
**Fecha:** 2026-06-06
**Estado original:** ✅ **3/3 sub-temas LOCKED** ⚠️ **5.4.2 refinamiento profundo pendiente**
**Master doc:** [Ronda_05_Orchestration_Multi_Agent.md](work/Ronda_05_Orchestration_Multi_Agent.md)
**Materializa:** Grafo Maestro Nodo 6 (DMN — Default Mode Network)

---

## Tabla de contenidos

1. [Propósito del Bloque 4](#1-propósito)
2. [Sub-tema 5.4.1 — Idle Detection + DMN Scheduling](#2-sub-tema-541)
3. [Sub-tema 5.4.2 — DMN Tasks Declarativas](#3-sub-tema-542)
4. [Sub-tema 5.4.3 — DMN Budget + Cliente Controls](#4-sub-tema-543)
5. [Refinamiento crítico pendiente](#5-refinamiento-crítico)
6. [Eventos audit Bloque 4](#6-eventos-audit)

---

## 1. Propósito

**DMN (Default Mode Network)** es el modo "cerebro en reposo" del humano:
- Consolida memorias del día
- Conecta ideas
- Simula escenarios
- Genera intuiciones

For3s OS DMN: agente piensa cuando workspace está idle, mejora el sistema sin intervención cliente.

**Brian input P3 verbatim:**
> "DEBE DE SER ALGO ENTRE B +C ALGO QUE PODAMOS ELEGIR Y RESTRINGIR PERO QUE EL PUEDA PENSAR CUANDO NO ESTAMOS ACTIVOS LOS HUMANOS Y MEJORE"

Bloque 4 responde:
- ¿Cuándo activar DMN? (5.4.1 scheduling)
- ¿Qué hace DMN exactamente? (5.4.2 tasks declarativas)
- ¿Cómo cliente controla? (5.4.3 9 controles)

---

## 2. Sub-tema 5.4.1 — Idle Detection + DMN Scheduling

### Decisión LOCKED: C — Híbrido central scheduler + reactive + neuromod-aware

### DMNScheduler singleton

```python
class DMNScheduler:
    MAX_CONCURRENT_DMN_TASKS = 5
    DEFAULT_IDLE_THRESHOLD_SECONDS = 300
    DEFAULT_COST_THRESHOLD = 0.7
    DEFAULT_COOLDOWN_SECONDS = 1800
    CHECK_INTERVAL_SECONDS = 60

    def __init__(self):
        self._running_dmn_tasks: set[asyncio.Task] = set()

    async def run_forever(self):
        while True:
            try:
                await self._tick()
            except Exception as e:
                await audit_logger.log(event_type='dmn_scheduler_error', payload={'error': str(e)})
            await asyncio.sleep(self.CHECK_INTERVAL_SECONDS)
```

### 6 signals collect candidates

```python
async def _collect_candidates(self) -> list[DMNCandidate]:
    workspaces = await workspace_repo.get_active()
    candidates = []

    for ws in workspaces:
        # SIGNAL 1: idle threshold
        idle_seconds = await activity_tracker.get_idle_seconds(ws.id)
        if idle_seconds < (ws.dmn_idle_threshold or self.DEFAULT_IDLE_THRESHOLD_SECONDS):
            continue

        # SIGNAL 2: active requests
        if await request_tracker.count_active(ws.id) > 0:
            continue

        # SIGNAL 3: cost ratio
        cost_ratio = await cost_tracker.get_p5_ratio(ws.id)
        if cost_ratio > (ws.dmn_cost_threshold or self.DEFAULT_COST_THRESHOLD):
            continue

        # SIGNAL 4: neuromod (no DMN si emergency)
        current_mode = await neuromod_orchestrator.get_current_mode(ws.id)
        if current_mode == NeuromodMode.HIGH_ATTENTION:
            continue

        # SIGNAL 5: cliente toggle (5.4.3)
        if not ws.dmn_enabled:
            continue

        # SIGNAL 6: cooldown elapsed
        last_dmn = await dmn_history.get_last_run(ws.id)
        cooldown = ws.dmn_cooldown_seconds or self.DEFAULT_COOLDOWN_SECONDS
        if last_dmn and (time.time() - last_dmn) < cooldown:
            continue

        candidates.append(DMNCandidate(
            workspace=ws,
            idle_seconds=idle_seconds,
            cost_ratio=cost_ratio,
            neuromod_mode=current_mode,
            priority_score=self._compute_priority(ws, idle_seconds, cost_ratio, current_mode),
        ))

    return candidates
```

### Priority scoring

```python
def _compute_priority(self, ws, idle_seconds, cost_ratio, current_mode) -> float:
    score = 0.0

    # Longer idle = más prioridad
    score += min(idle_seconds / 3600, 10)  # max 10 points

    # Lower cost ratio = más seguro
    score += (1 - cost_ratio) * 5  # max 5 points

    # Tier
    score += {'enterprise': 5, 'standard': 2, 'pilot_light': -3}.get(ws.tier, 0)

    # CONSOLIDATION neuromod boost
    if current_mode == NeuromodMode.CONSOLIDATION:
        score += 3

    # Local night hours boost (timezone-aware)
    if self._is_workspace_local_night_hours(ws):
        score += 4

    return score
```

### Dispatch respetando concurrency cap

```python
async def _dispatch(self, candidates_sorted):
    self._running_dmn_tasks = {t for t in self._running_dmn_tasks if not t.done()}
    slots = self.MAX_CONCURRENT_DMN_TASKS - len(self._running_dmn_tasks)

    if slots <= 0:
        await audit_logger.log(event_type='dmn_scheduler_saturated', payload={...})
        return

    for candidate in candidates_sorted[:slots]:
        task = asyncio.create_task(
            self._run_dmn_for_workspace(candidate.workspace),
            name=f'dmn_workspace_{candidate.workspace.id}',
        )
        self._running_dmn_tasks.add(task)

        await audit_logger.log(
            event_type='dmn_dispatched',
            payload={
                'workspace_id': candidate.workspace.id,
                'priority_score': candidate.priority_score,
            }
        )
```

---

## 3. Sub-tema 5.4.2 — DMN Tasks Declarativas

### Decisión LOCKED: C — 8 tasks declarativas comprehensivas

> ⚠️ **LOCKED como completo v1 PERO refinamiento profundo PENDIENTE. Ver §5.**

### Catálogo 8 DMN Tasks v1

```python
DMN_TASKS_V1 = {
    'memory_consolidation': DMNTaskDefinition(
        name='memory_consolidation',
        estimated_cost_usd=0.10,
        priority=9,
        cliente_toggle_key='dmn_memory_consolidation_enabled',
        enabled_by_default=True,
        max_runtime_seconds=120,
    ),
    'pattern_detection': DMNTaskDefinition(
        name='pattern_detection',
        estimated_cost_usd=0.05,
        priority=8,
        cliente_toggle_key='dmn_pattern_detection_enabled',
        enabled_by_default=True,
        max_runtime_seconds=60,
    ),
    'hypothesis_generation': DMNTaskDefinition(
        name='hypothesis_generation',
        estimated_cost_usd=0.50,  # Opus
        priority=5,
        cliente_toggle_key='dmn_hypothesis_generation_enabled',
        enabled_by_default=False,  # opt-in
        max_runtime_seconds=180,
    ),
    'prompt_improvement': DMNTaskDefinition(
        name='prompt_improvement',
        estimated_cost_usd=0.20,
        priority=6,
        cliente_toggle_key='dmn_prompt_improvement_enabled',
        enabled_by_default=False,
        max_runtime_seconds=120,
    ),
    'routing_learning': DMNTaskDefinition(
        name='routing_learning',
        estimated_cost_usd=0.05,
        priority=7,
        cliente_toggle_key='dmn_routing_learning_enabled',
        enabled_by_default=True,
        max_runtime_seconds=60,
    ),
    'cache_prewarming': DMNTaskDefinition(
        name='cache_prewarming',
        estimated_cost_usd=0.15,
        priority=6,
        cliente_toggle_key='dmn_cache_prewarming_enabled',
        enabled_by_default=True,
        max_runtime_seconds=120,
    ),
    'embedding_precompute': DMNTaskDefinition(
        name='embedding_precompute',
        estimated_cost_usd=0.0,  # Stella local
        priority=10,
        cliente_toggle_key='dmn_embedding_precompute_enabled',
        enabled_by_default=True,
        max_runtime_seconds=180,
    ),
    'eval_regression_detection': DMNTaskDefinition(
        name='eval_regression_detection',
        estimated_cost_usd=0.05,
        priority=4,
        cliente_toggle_key='dmn_eval_regression_enabled',
        enabled_by_default=True,
        max_runtime_seconds=60,
    ),
}
```

### Origen Grafo Maestro

**LITERAL (3):**
1. memory_consolidation — "transfer episodios → KG facts"
2. pattern_detection — "3 PRs en 12 días con patrón similar"
3. hypothesis_generation — "este módulo va a romper"

**IMPLÍCITO (5):**
4. prompt_improvement — "este test es redundante"
5. routing_learning — feed 5.2.2 history-aware
6. cache_prewarming — feed 5.2.3 fast path layer E
7. embedding_precompute — R2 B2 batch pending
8. eval_regression_detection — R3 4.4 weekly

### DMNTaskExecutor

```python
class DMNTaskExecutor:
    DEFAULT_BUDGET_PER_RUN = 1.00  # $1

    async def execute_for_workspace(self, workspace) -> DMNRunResult:
        results = []
        failed = []
        total_cost = 0
        budget = workspace.dmn_budget_per_run or self.DEFAULT_BUDGET_PER_RUN

        # Filter enabled per workspace
        enabled = [
            (name, defn) for name, defn in DMN_TASKS_V1.items()
            if getattr(workspace, defn.cliente_toggle_key, defn.enabled_by_default)
        ]
        enabled.sort(key=lambda x: -x[1].priority)

        for name, defn in enabled:
            # Budget check
            if total_cost + defn.estimated_cost_usd > budget:
                await audit_logger.log(event_type='dmn_task_skipped_budget', payload={...})
                continue

            # Trigger check
            trigger_fn, action_fn = TASK_ACTIONS[name]
            if not await trigger_fn(workspace):
                continue

            # Execute con timeout
            try:
                async with asyncio.timeout(defn.max_runtime_seconds):
                    result = await action_fn(workspace)
                    results.append(result)
                    total_cost += result.cost
                    await audit_logger.log(event_type='dmn_task_completed', payload={...})
            except asyncio.TimeoutError:
                failed.append({'task': name, 'error': 'timeout'})
            except Exception as e:
                failed.append({'task': name, 'error': str(e)})

        return DMNRunResult(workspace_id=workspace.id, completed=results, failed=failed, total_cost=total_cost)
```

---

## 4. Sub-tema 5.4.3 — DMN Budget + Cliente Controls

### Decisión LOCKED: C — 9 controles granulares

### WorkspaceDMNSettings Pydantic

```python
class WorkspaceDMNSettings(BaseModel):
    # CONTROL 1: toggle global
    dmn_enabled: bool = True

    # CONTROL 2: toggle per task (8 flags)
    dmn_memory_consolidation_enabled: bool = True
    dmn_pattern_detection_enabled: bool = True
    dmn_hypothesis_generation_enabled: bool = False  # opt-in
    dmn_prompt_improvement_enabled: bool = False    # opt-in
    dmn_routing_learning_enabled: bool = True
    dmn_cache_prewarming_enabled: bool = True
    dmn_embedding_precompute_enabled: bool = True
    dmn_eval_regression_enabled: bool = True

    # CONTROL 3: budget per run
    dmn_budget_per_run_usd: float = 1.00

    # CONTROL 4: budget mensual
    dmn_budget_monthly_ratio: float = 0.10  # 10% cap P5 (20% enterprise)

    # CONTROL 5: horario permitido
    dmn_allowed_hours: list[int] = Field(default_factory=lambda: list(range(24)))
    dmn_allowed_days: list[int] = Field(default_factory=lambda: list(range(7)))

    # CONTROL 6: cost gate
    dmn_cost_threshold: float = 0.7

    # CONTROL 7: alarmas
    dmn_alert_thresholds: list[float] = [0.5, 0.75, 0.9, 1.0]

    # CONTROL 9: aprobación outputs
    dmn_output_auto_apply: bool = False

    # Heredados 5.4.1
    dmn_idle_threshold: int = 300
    dmn_cooldown_seconds: int = 1800
```

### Risk categories outputs (CONTROL 9)

```python
class DMNOutputRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

TASK_RISK_MAP = {
    'memory_consolidation': DMNOutputRisk.MEDIUM,
    'pattern_detection': DMNOutputRisk.MEDIUM,
    'hypothesis_generation': DMNOutputRisk.HIGH,
    'prompt_improvement': DMNOutputRisk.HIGH,
    'routing_learning': DMNOutputRisk.LOW,
    'cache_prewarming': DMNOutputRisk.LOW,
    'embedding_precompute': DMNOutputRisk.LOW,
    'eval_regression_detection': DMNOutputRisk.MEDIUM,
}
```

**Decision matrix:**
- HIGH risk → SIEMPRE review obligatorio
- MEDIUM + auto_apply=False → review recomendado
- LOW OR (MEDIUM + auto_apply=True) → apply directamente

### Alarms (CONTROL 7)

```python
class DMNControlsEnforcer:
    async def check_alert_thresholds(self, workspace):
        settings = workspace.dmn_settings
        dmn_monthly_cap = workspace.p5_cap * settings.dmn_budget_monthly_ratio
        dmn_monthly_spent = await cost_tracker.get_monthly_spent_dmn(workspace.id)
        spend_ratio = dmn_monthly_spent / dmn_monthly_cap

        last_alerted = await dmn_alerts_state.get_last_threshold(workspace.id)

        for threshold in sorted(settings.dmn_alert_thresholds):
            if spend_ratio >= threshold and threshold > last_alerted:
                await self._send_alert(workspace, threshold, dmn_monthly_spent, dmn_monthly_cap)
                await dmn_alerts_state.set_last_threshold(workspace.id, threshold)

                # Auto-disable al 100%
                if threshold >= 1.0:
                    workspace.dmn_settings.dmn_enabled = False
                    await workspace_repo.update(workspace)
                    await audit_logger.log(
                        event_type='dmn_auto_disabled_budget_exhausted',
                        payload={'workspace_id': workspace.id},
                    )
```

### Dashboard API endpoints (CONTROL 8)

```
GET   /workspace/{id}/dmn/status
GET   /workspace/{id}/dmn/history?days=30
GET   /workspace/{id}/dmn/outputs?status=pending_review
PATCH /workspace/{id}/dmn/settings
POST  /workspace/{id}/dmn/outputs/{id}/approve
POST  /workspace/{id}/dmn/outputs/{id}/reject
```

### Compliance B2B

9 controles + audit per cada control change + retention logs = SOC2 path verdadero.

---

## 5. Refinamiento crítico pendiente

### ⚠️ 5.4.2 marked by Brian — atención profunda pre-programación

**Memoria global:** `project_dmn_tasks_critical_refinement.md`

**Brian quote verbatim:**
> "GUARDA UNA NOTA MUY IMPORTANTE QUE DEFINIREMOS A DETALLE ESTE APARTADO DEJALO COMO COMPLETO PERO TENEMOS QUE PRESTAR MUCHA ATENCION"

### Plan refinamiento

Crear `work/Ronda_05_DMN_Tasks_Detailed.md` con:

**Por cada task de las 8:**
- Pseudocode completo `action_*`
- Schema input/output formal Pydantic
- Trigger condition con threshold defendible (razonamiento por qué ese número)
- Eval criteria (cómo medir que la task aportó valor → ROI)
- Failure modes + recovery
- Interaction graph con otras tasks

**Auto-improvement loop end-to-end:**
- DMN output → review queue (5.4.3)
- Brian/cliente aprueba/rechaza
- Aprobados → promoción a producción
- Métrica: outputs aprobados / outputs generados
- Foundation Meta-Orchestrator (Grafo Maestro §6) — defer R10+

**Cost ROI per task:**
- Estimated cost (lockeado v1) vs medida real outcome
- Si task no aporta valor mensurable → disable
- Brian dashboard ROI per task

**v2-v3 expansion path:**
- Tasks adicionales identificadas en producción
- Workspace custom tasks DSL (defer E)
- LLM-driven task selection (defer D)

---

## 6. Eventos audit Bloque 4

**Scheduler (5.4.1):**
- `dmn_dispatched`
- `dmn_completed`
- `dmn_failed`
- `dmn_scheduler_saturated`
- `dmn_scheduler_error`

**Tasks executor (5.4.2):**
- `dmn_task_completed`
- `dmn_task_skipped_budget`
- `dmn_task_timeout`
- `dmn_task_failed`

**Controls (5.4.3):**
- `dmn_settings_updated`
- `dmn_threshold_alert_sent`
- `dmn_auto_disabled_budget_exhausted`
- `dmn_output_pending_review`
- `dmn_output_auto_applied`
- `dmn_output_approved`
- `dmn_output_rejected`

---

**Bloque 4 ✅ CERRADO v1 — Foundation Nodo 6 DMN verdadero con refinamiento 5.4.2 pendiente para pre-programación.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_05_Bloque_4_DMN_Default_Mode.md`).
