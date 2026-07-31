# Ronda 6 — Bloque 2 — Ganglios Basales / Skills ⭐ NÚCLEO PILAR 3

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 2 de R6. ⭐ NÚCLEO Pilar 3 Autonomía Generativa.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Estado original:** ✅ **5/5 sub-temas LOCKED**
**Master doc:** [Ronda_06_Memory_Stack_Extensions.md](work/Ronda_06_Memory_Stack_Extensions.md)
**Materializa:** Grafo Maestro Nodo 4 + Pilar 3 Autonomía Generativa

⚠️ **Flag global:** TODO R6 requires re-review pre-código (`project_r6_critical_pre_code_review.md`).

---

## 1. Propósito

**Esto es lo más radical del Grafo Maestro.** El sistema:
- ESCRIBE sus propias skills (Pilar 3 capacidad #1)
- Aplica skills sin LLM planning (cost saving real)
- Aprende qué evitar (NO-GO learning)
- Refuerza dopaminérgicamente (TD-learning)
- Lifecycle 7 fases auto-gestionado

Sin Bloque 2, For3s OS NO tiene autonomía generativa real.

---

## 2. Sub-tema 6.2.1 — Skill Schema (Híbrido FS+PG+pgvector)

### Decisión LOCKED: C — Híbrido filesystem + Postgres + pgvector

### Filesystem layout

```
/var/lib/for3s/skills/
   workspace_{ws_id}/
      go/
         {pattern_slug}_v{semver}.md
      no_go/
         {pattern_slug}_v{semver}.md
   common_stack/
      go/
      no_go/
   _archive/
      workspace_{ws_id}/
         {pattern_slug}_v{semver}.md
```

LUKS encrypted disk + perms 0o700.

### File format (P1 LOCKED C+A)

```markdown
---
# YAML frontmatter (Pydantic validated)
skill_id: sk_acme_analyze_python_pr_001
workspace_id: ws_acme
tier: workspace
category: go
pattern: analyze_python_pr_with_tdd
version: 1.0.0
state: active

intent_pattern: "analyze.*python.*pr"
intent_keywords: [analyze, python, pr, code_review]
trigger_confidence_threshold: 0.85

required_tools: [github_get_pr_files, ...]
required_specialists: [code_analyzer, test_generator]
subgraph_mode_required: complete

metrics:
  total_executions: 47
  successful_executions: 44
  success_rate: 0.936
  avg_confidence: 0.89
  avg_cost_usd: 0.42

scoring:
  score: 8.7
  reward_history_count: 44
  punishment_history_count: 3

promotion_history: [...]
source_plans: [p-abc123, ...]
---

# Skill: Analyze Python PR with TDD focus

## Cuándo aplicar
...

## Approach
...

## Pasos
### Step 1: ...
...

## Checkpoints críticos
...

## Fallbacks conocidos
...

## Lessons learned (NO-GO references)
...
```

### Postgres table

```sql
CREATE TABLE skills (
    skill_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    tier TEXT NOT NULL,
    category TEXT NOT NULL,
    pattern TEXT NOT NULL,
    version TEXT NOT NULL,
    state TEXT NOT NULL,
    
    file_path TEXT NOT NULL,
    file_sha256 TEXT NOT NULL,
    
    intent_pattern TEXT NOT NULL,
    intent_keywords TEXT[],
    trigger_confidence_threshold REAL,
    
    required_tools TEXT[],
    required_specialists TEXT[],
    subgraph_mode_required TEXT,
    
    -- Metrics (denormalized)
    total_executions INT,
    successful_executions INT,
    success_rate REAL,
    avg_confidence REAL,
    avg_cost_usd REAL,
    avg_duration_seconds REAL,
    last_used_at TIMESTAMP,
    
    -- Dopaminergic
    score REAL,
    reward_history_count INT,
    punishment_history_count INT,
    last_reward_at TIMESTAMP,
    decay_factor REAL,
    
    -- Embeddings
    intent_embedding VECTOR(1024),
    body_embedding VECTOR(1024),
    
    -- Lifecycle
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    sandbox_started_at TIMESTAMP,
    promoted_at TIMESTAMP,
    core_promoted_at TIMESTAMP,
    core_approved_by TEXT,
    declining_since TIMESTAMP,
    archived_at TIMESTAMP,
    archive_reason TEXT,
    
    source_plans TEXT[]
);

CREATE INDEX skills_intent_emb_hnsw ON skills
    USING hnsw (intent_embedding vector_cosine_ops);
CREATE INDEX skills_body_emb_hnsw ON skills
    USING hnsw (body_embedding vector_cosine_ops);

ALTER TABLE skills ENABLE ROW LEVEL SECURITY;
CREATE POLICY skills_workspace_isolation ON skills
    USING (
        workspace_id = current_setting('app.current_workspace_id')
        OR tier = 'common_stack'
    );
```

### Atomic write protocol
1. Build file path
2. Build markdown content
3. Atomic file write (tmp + rename)
4. SHA256 compute
5. Stella embeddings (intent + body)
6. Postgres UPSERT
7. Audit log

### 3-layer isolation
1. Filesystem path (`/workspace_{id}/`)
2. Postgres RLS (`workspace_id = current_setting`)
3. Common stack policy (opt-in P3 B)

### Audit events
- `skill_written / loaded`
- `SECURITY_skill_file_integrity_mismatch`
- `skill_version_pinned / archived`

---

## 3. Sub-tema 6.2.2 — Vía GO (Skills Positivas)

### Decisión LOCKED: C — Plan-template + checkpoint validation

### SkillApplicationEngine pipeline (9 steps)

```python
class SkillApplicationStatus(str, Enum):
    APPLIED = "applied"
    NO_MATCH = "no_match"
    FALLBACK_TO_PFC_PLANNING = "fallback_to_pfc_planning"
    BLOCKED_BY_NO_GO = "blocked_by_no_go"


class SkillApplicationEngine:
    PRECEDENCE_TIER_ORDER = [
        SkillTier.WORKSPACE,
        SkillTier.CORE,
        SkillTier.COMMON_STACK,
    ]
    PFC_PLANNING_COST_ESTIMATE_USD = 0.05  # cost saved if skill applied
    
    async def find_and_apply(
        self, workspace_id, request, signals,
    ) -> SkillApplicationResult:
        # 1. Search GO skills
        matches = await skill_store.search_by_intent(
            workspace_id, request,
            tier_filter=self.PRECEDENCE_TIER_ORDER,
            category_filter=SkillCategory.GO,
            top_k=5,
        )
        
        if not matches:
            return SkillApplicationResult(status=SkillApplicationStatus.NO_MATCH)
        
        # 2. Precedence applied
        best_skill, similarity = matches[0]
        
        # 3. Threshold check
        if similarity < best_skill.metadata.trigger_confidence_threshold:
            return SkillApplicationResult(
                status=SkillApplicationStatus.FALLBACK_TO_PFC_PLANNING,
                fallback_reason='similarity_below_threshold',
            )
        
        # 4. NO-GO interference (6.2.3 hook)
        no_go_conflicts = await no_go_checker.check_conflicts(
            workspace_id, candidate_skill=best_skill, request=request,
        )
        if no_go_conflicts:
            return SkillApplicationResult(
                status=SkillApplicationStatus.BLOCKED_BY_NO_GO,
                fallback_reason='no_go_interference',
            )
        
        # 5. State check
        if best_skill.metadata.state != SkillLifecycleState.ACTIVE:
            return SkillApplicationResult(
                status=SkillApplicationStatus.FALLBACK_TO_PFC_PLANNING,
                fallback_reason='skill_not_active',
            )
        
        # 6. Convert skill → PFCPlan
        plan = await self._skill_to_plan(best_skill, request, signals)
        
        # 7. Audit application (cost_saved ~$0.05)
        await audit_logger.log(
            event_type='skill_applied_go',
            payload={
                'skill_id': best_skill.metadata.skill_id,
                'similarity': similarity,
                'cost_saved_estimated_usd': self.PFC_PLANNING_COST_ESTIMATE_USD,
            }
        )
        
        # 8. Execute (reuse 6.1.x infrastructure)
        execution_result = await pfc_executor.execute_plan(plan, workspace)
        
        # 9. Dopaminergic feedback (6.2.4)
        await dopaminergic_scorer.record_outcome(
            best_skill, plan, execution_result,
        )
        
        await skill_store.update_metrics(
            best_skill.metadata.skill_id, execution_result,
        )
        
        return SkillApplicationResult(
            status=SkillApplicationStatus.APPLIED,
            skill_id=best_skill.metadata.skill_id,
            plan_id=plan.plan_id,
            cost_saved_usd=self.PFC_PLANNING_COST_ESTIMATE_USD,
        )
```

### Markdown parsers

```python
def parse_skill_steps_section(markdown_body: str) -> list[dict]:
    """Parse '## Pasos' → list of step dicts (regex + Pydantic validate)."""
    ...

def parse_skill_risks_section(markdown_body: str) -> list[str]:
    """Parse '## Fallbacks conocidos' → list of risks."""
    ...
```

### Integration en PFCRouter

```python
class PFCRouter:
    async def route_request(self, workspace_id, request, signals):
        # Skip skill check si MINIMUM
        if signals.subgraph_mode == SubgraphMode.MINIMUM:
            return RoutingDecision.PFC_PLANNING
        
        # Try skill first (foundation D 6.1.1)
        skill_result = await skill_application_engine.find_and_apply(
            workspace_id, request, signals,
        )
        
        if skill_result.status == SkillApplicationStatus.APPLIED:
            return RoutingDecision(
                action='SKILL_APPLIED',
                skill_id=skill_result.skill_id,
                cost_saved_usd=skill_result.cost_saved_usd,
            )
        
        return RoutingDecision(action='PFC_PLANNING')
```

### Audit events
- `skill_match_below_threshold` (fallback)
- `skill_blocked_by_no_go`
- `skill_applied_go` (con cost_saved)
- `skill_metrics_updated`

---

## 4. Sub-tema 6.2.3 — Vía NO-GO (Skills Negativas)

### Decisión LOCKED: C — 3-niveles HARD/SOFT/WARN

### Severity levels

```python
class NoGoSeverity(str, Enum):
    HARD_BLOCK = "hard_block"
    # Imposible bypass. Compliance §8.4.
    
    SOFT_BLOCK = "soft_block"
    # Bypass condicional (3 gates)
    
    WARN = "warn"
    # Audit + continue
```

### NoGoChecker 3 detection types

```python
async def check_conflicts(
    self, workspace_id, candidate_skill, candidate_plan, candidate_tools, request,
) -> list[NoGoConflict]:
    # Search NO-GO skills relevantes
    no_go_candidates = await skill_store.search_by_intent(
        workspace_id=workspace_id,
        query_text=query_text,
        category_filter=SkillCategory.NO_GO,
        top_k=20,
    )
    
    conflicts = []
    for no_go_skill, similarity in no_go_candidates:
        if similarity < 0.7:
            continue
        
        # Check 1: blocked tools intersection
        if candidate_tools:
            blocked_tools = set(no_go_skill.metadata.blocks_tools)
            intersect = blocked_tools & set(candidate_tools)
            if intersect:
                conflicts.append(NoGoConflict(...))
        
        # Check 2: blocked patterns match
        if candidate_plan and candidate_plan.promotion_candidate_pattern:
            if candidate_plan.promotion_candidate_pattern in no_go_skill.metadata.blocks_patterns:
                conflicts.append(NoGoConflict(...))
        
        # Check 3: blocked skills match
        if candidate_skill:
            if candidate_skill.metadata.skill_id in no_go_skill.metadata.blocks_skills or []:
                conflicts.append(NoGoConflict(...))
    
    return conflicts
```

### Enforcement matrix

```python
async def enforce_or_bypass(self, conflicts, workspace, context):
    hard_blocks = [c for c in conflicts if c.severity == HARD_BLOCK]
    soft_blocks = [c for c in conflicts if c.severity == SOFT_BLOCK]
    warns = [c for c in conflicts if c.severity == WARN]
    
    # HARD: imposible bypass
    if hard_blocks:
        return NoGoEnforcementResult(blocked=True, bypass_available=False)
    
    # SOFT: 3 gates check
    for sb in soft_blocks:
        # Gate 1: workspace setting
        workspace_allows = getattr(workspace, sb.bypass_workspace_setting, False)
        if not workspace_allows:
            return NoGoEnforcementResult(blocked=True, bypass_instructions=...)
        
        # Gate 2: human-in-loop
        if sb.bypass_requires_human_in_loop:
            approval = await human_approval_service.request_bypass(...)
            if not approval.approved:
                return NoGoEnforcementResult(blocked=True)
        
        # Gate 3: audit reason
        if sb.bypass_requires_audit_reason and not context.get('user_reason'):
            return NoGoEnforcementResult(blocked=True)
    
    # WARNS: audit + continue
    for w in warns:
        await audit_logger.log(event_type='no_go_WARN_proceeded', ...)
    
    return NoGoEnforcementResult(blocked=False, warnings=warns)
```

### Generation sources (4)

1. **Auto DMN:** plan falla N veces → NO-GO candidate (Brian review)
2. **Manual cliente:** workspace settings → NO-GO auto-generated
3. **Core Brian:** hardcoded compliance (HARD)
4. **Common stack:** best practices universales

### Hardcoded HARD_BLOCK foundation §8.4

```python
HARDCODED_HARD_BLOCKS = [
    {
        'pattern': 'cross_workspace_data_access',
        'reason': 'Grafo Maestro §8.4: NUNCA',
    },
    {
        'pattern': 'unsandboxed_code_execution',
        'blocks_tools': ['exec_arbitrary_code', 'eval_python_dynamic'],
        'reason': 'Grafo Maestro §8.4: NUNCA',
    },
    {
        'pattern': 'customer_data_without_optin',
        'reason': 'Grafo Maestro §8.4: NUNCA',
    },
]
```

Bootstrap como common_stack skills al startup.

### Audit events
- `no_go_HARD_BLOCK_enforced` (CRITICAL)
- `no_go_SOFT_BLOCK_enforced` (HIGH)
- `no_go_SOFT_BLOCK_bypassed` (WARNING)
- `no_go_SOFT_BLOCK_human_denied`
- `no_go_WARN_proceeded` (INFO)

---

## 5. Sub-tema 6.2.4 — Dopaminergic Scoring (TD-learning 7 signals)

### Decisión LOCKED: C — Multi-signal TD-learning

### 7 signals + weights

```python
SIGNAL_WEIGHTS = {
    'reward': 0.30,
    'prediction_error': 0.15,
    'recency': 0.10,
    'cost_efficiency': 0.20,
    'confidence_avg': 0.15,
    'consistency': 0.10,
}

DAILY_DECAY_FACTOR = 0.95
REWARD_THRESHOLD = 0.7
PUNISHMENT_THRESHOLD = 0.3
SMOOTHING_FACTOR = 0.3
```

### SkillScoring model

```python
class SkillScoring(BaseModel):
    score: float = 5.0  # 0-10 range
    reward_score: float = 0.0
    prediction_error: float = 0.0
    recency_weight: float = 1.0
    cost_efficiency: float = 0.0
    confidence_avg: float = 0.0
    consistency_score: float = 0.0
    
    reward_history_count: int = 0
    punishment_history_count: int = 0
    last_reward_at: Optional[datetime]
    last_punishment_at: Optional[datetime]
    last_execution_at: Optional[datetime]
    decay_factor: float = 0.95
    
    # Per (workspace, subgraph_mode)
    context_scores: dict[str, float] = {}
```

### Auto lifecycle triggers

```python
CORE_PROMOTION_SCORE_THRESHOLD = 8.5
CORE_PROMOTION_REWARDS_REQUIRED = 50
DECLINE_SCORE_THRESHOLD = 3.0
DECLINE_PUNISHMENTS_REQUIRED = 5
NO_GO_FAILURE_STREAK = 5

async def _check_lifecycle_transitions(self, skill, update):
    # Core promotion (P2 A+B)
    if (skill.metadata.tier == WORKSPACE and
        score >= 8.5 and rewards >= 50):
        await plan_to_skill_promoter.check_core_promotion_eligibility(skill)
    
    # Decline detection
    if (state == ACTIVE and score < 3.0 and punishments >= 5):
        await plan_to_skill_promoter.mark_declining(skill)
    
    # Auto NO-GO from failures (§8.1 #1)
    recent_failures = await self._get_recent_failures(skill.id, limit=5)
    if len(recent_failures) >= 5 and category == GO:
        await self._propose_no_go_from_failures(skill, recent_failures)
```

### Audit events
- `dopaminergic_scoring_updated` (per execution)
- `no_go_auto_proposed_from_failures`
- `skill_core_promotion_eligible`
- `skill_decline_detected`

Performance: ~50ms async background (no critical path).

---

## 6. Sub-tema 6.2.5 — Skill Lifecycle Operations (Manager)

### Decisión LOCKED: C — Manager completo + state machine + APIs

### State machine (8 states + transitions)

```python
VALID_TRANSITIONS = {
    DETECTED: [PROPOSED, ARCHIVED],
    PROPOSED: [SANDBOX, ARCHIVED],
    SANDBOX: [EVALUATION, ARCHIVED],
    EVALUATION: [PROMOTED, SANDBOX, ARCHIVED],
    PROMOTED: [ACTIVE, ARCHIVED],
    ACTIVE: [DECLINING, ARCHIVED],
    DECLINING: [ACTIVE, ARCHIVED],
    ARCHIVED: [],  # terminal
}
```

### Atomic write protocol (7 steps)

```python
async def transition_state(self, skill, new_state, reason, actor):
    if new_state not in VALID_TRANSITIONS[skill.state]:
        raise SkillStateTransitionError
    
    # 1. Postgres advisory lock (cross-worker)
    async with postgres_advisory_lock(f'skill_{skill.id}'):
        # 2. Reload (avoid stale)
        skill = await skill_store.load_skill(skill.id)
        
        # 3. Re-validate concurrency
        if skill.state != current_state:
            raise SkillConcurrentModificationError
        
        # 4. Apply transition + timestamps
        skill.state = new_state
        skill.promotion_history.append(PromotionEvent(...))
        
        # State-specific
        if new_state == SANDBOX:
            skill.sandbox_started_at = now()
            skill.sandbox_until = now() + 7 days
        elif new_state == ARCHIVED:
            await self._physical_archive(skill)
        
        # 5. Atomic filesystem + DB write
        await skill_store.write_skill(skill)
        
        # 6. Audit
        await audit_logger.log('skill_state_transitioned', ...)
        
        # 7. Release lock
```

### Versioning

```python
NEW_VERSION_SCORE_INHERITANCE_FACTOR = 0.9  # unproven penalty

async def create_new_version(self, skill, new_body, bump_type='patch'):
    new_version = semver.bump(skill.version, bump_type)
    new_skill = skill.copy()
    new_skill.skill_id = f'{pattern}_v{new_version}'
    new_skill.version = str(new_version)
    new_skill.body_markdown = new_body
    new_skill.state = SANDBOX  # nuevas versions a sandbox
    new_skill.scoring.score = old.score * 0.9
    
    await self.atomic_write_skill(new_skill, actor='system')
```

### Microglía skill scan (cron daily 3 AM)

```python
MICROGLIA_DECLINING_DAYS_BEFORE_ARCHIVE = 30

async def microglia_skill_scan(self):
    for workspace in await workspace_repo.get_active():
        declining = await skill_store.find_skills_in_state(
            workspace.id, state=DECLINING, older_than_days=30,
        )
        for skill in declining:
            await self.transition_state(
                skill, ARCHIVED,
                reason='microglia_declining_30d',
                actor='system_microglia',
            )
```

### Sandbox execution (Fase 3 hook)

```python
async def execute_in_sandbox(self, skill, original_plan, workspace):
    if skill.state != SANDBOX:
        raise SkillNotInSandboxError
    
    # Workspace prefixed _sandbox_ (isolated)
    sandbox_plan = await skill_application_engine._skill_to_plan(
        skill, original_plan.request_summary, signals=...,
    )
    sandbox_plan.workspace_id = f'_sandbox_{workspace.id}'
    
    result = await pfc_executor.execute_plan(
        sandbox_plan, workspace, sandbox_mode=True,
    )
    
    # Persist sandbox run (informa Fase 4 evaluación)
    await skill_sandbox_runs_store.persist(SandboxRun(...))
    
    return SandboxExecutionResult(success=True, result=result)
```

### Admin API (Brian)

```
GET    /admin/skills (list filters)
GET    /admin/skills/{id} (detail + history)
POST   /admin/skills/{id}/approve_core (1-click)
POST   /admin/skills/{id}/approve_no_go (1-click NO-GO proposal)
POST   /admin/skills/{id}/archive
POST   /admin/skills/{id}/override_score
```

### Cliente API (self-service)

```
GET    /workspace/{ws}/skills
GET    /workspace/{ws}/skills/{id}
PATCH  /workspace/{ws}/skills/{id}/toggle
POST   /workspace/{ws}/skills/{id}/feedback
PATCH  /workspace/{ws}/settings/skills
```

### Audit events
- `skill_state_transitioned` (with from/to/reason/actor)
- `skill_atomic_write`
- `skill_new_version_created`
- `skill_cutover_executed`
- `skill_sandbox_execution_failed`
- `skill_microglia_archived`
- `skill_brian_approved_core / no_go / archived`
- `skill_cliente_toggled / feedback_submitted`

---

## 7. Pilar 3 Autonomía Generativa ACTIVADO ⭐

Grafo Maestro Pilar 3 capacidad #1: **GENERAR SKILLS NUEVAS**

| Etapa Grafo Maestro §8.2 | Implementado |
|---|---|
| 1. Detección pattern | ✅ 6.1.4 Fase 1 (DMN) |
| 2. Propuesta spec | ✅ 6.1.4 Fase 2 (LLM) |
| 3. Sandbox aislado | ✅ 6.2.5 execute_in_sandbox |
| 4. Evaluación PASS/MARGINAL/FAIL | ✅ 6.1.4 Fase 4 |
| 5. Promoción 3-tier | ✅ 6.1.4 Fase 5 (P2 A+C+B) |
| 6. Vida útil scoring | ✅ 6.2.4 dopaminergic |
| 7. Declive + archive | ✅ 6.2.5 microglía + transition |

**Autonomía generativa 100% v1 OPERATIVA. ⭐⭐⭐**

---

## 8. Eventos audit Bloque 2

Total events nuevos R6 B2: **~30 events**

Storage (6.2.1): skill_written, loaded, integrity_mismatch, version_pinned, archived

GO (6.2.2): skill_match_below_threshold, blocked_by_no_go, applied_go, metrics_updated

NO-GO (6.2.3): HARD_BLOCK_enforced, SOFT_BLOCK_enforced/bypassed/human_denied, WARN_proceeded

Dopaminergic (6.2.4): scoring_updated, no_go_auto_proposed, core_promotion_eligible, decline_detected

Lifecycle (6.2.5): state_transitioned, atomic_write, new_version_created, cutover_executed, sandbox_execution_failed, microglia_archived, brian_approved_core/no_go/archived, cliente_toggled/feedback_submitted

---

**Bloque 2 ✅ CERRADO — Foundation Nodo 4 + Pilar 3 Autonomía Generativa ACTIVADA ⭐ ⚠️ flag pre-código aplica.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_06_Bloque_2_Ganglios_Basales_Skills.md`).
