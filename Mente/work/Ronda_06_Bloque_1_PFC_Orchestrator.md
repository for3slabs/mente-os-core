# Ronda 6 — Bloque 1 — PFC Orchestrator Completo

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 1 de R6.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Estado original:** ✅ **4/4 sub-temas LOCKED**
**Master doc:** [Ronda_06_Memory_Stack_Extensions.md](work/Ronda_06_Memory_Stack_Extensions.md)
**Materializa:** Grafo Maestro Nodo 3 PFC verdadero v1 (cierra parcial R3+R5)

⚠️ **Flag global:** TODO R6 requires re-review pre-código (`project_r6_critical_pre_code_review.md`).

---

## 1. Propósito

El PFC es el control ejecutivo del cerebro. Decide:
- Cómo planear (6.1.1)
- Qué tan confiable es el resultado (6.1.2)
- Cuándo re-planear (6.1.3)
- Cuándo promover plan a skill reutilizable (6.1.4)

R3 LLM Layer + R5 Tálamo solo cubrieron LLM provider + routing. R6 B1 cierra el PFC al 100%.

---

## 2. Sub-tema 6.1.1 — Planning Framework

### Decisión LOCKED: C — Plan-then-execute con Claude

### Pipeline

```
REQUEST llega
   ↓
ROUTING (R5 B1+B2)
   ↓
Planning trigger check:
   • MINIMUM subgraph → SKIP planning
   • COMPLETE → GENERATE PLAN
   • EMERGENCY → GENERATE PLAN (fast)
   ↓
PFC GENERATES PLAN (LLM Sonnet, structured)
   ↓
Persist Postgres pfc_plans
   ↓
Pre-flight validation (reuse 5.3.4 layer 1)
   ↓
EXECUTE step by step + checkpoints
   ↓
Post-execution: skill candidate (hook 6.1.4)
```

### PFCPlan model

```python
class PFCPlan(BaseModel):
    plan_id: str
    workspace_id: str
    request_summary: str
    intent_summary: str
    approach: str
    subgraph_mode: str
    neuromod_mode: str
    llm_tier_used_for_planning: str
    
    steps: list[PlanStep]
    
    estimated_total_cost_usd: float
    estimated_total_duration_seconds: int
    confidence_in_plan: float
    risks: list[str]
    
    promotion_candidate_pattern: Optional[str]
    source_skill_id: Optional[str]  # NEW si skill aplicada
    
    re_plan_count: int = 0
    re_plan_history: list[dict] = []
    
    created_at: float
    completed_at: Optional[float]
    actual_total_cost_usd: float
    plan_confidence: Optional[ConfidenceScore]
```

### PlanStep model

```python
class PlanStep(BaseModel):
    step_id: str
    description: str
    specialist_or_tool: str
    specialists: Optional[list[str]]  # if multi-agent
    expected_outcome: str
    estimated_cost_usd: float
    estimated_duration_seconds: int
    fallback_if_fails: Optional[str]
    checkpoint: bool
    checkpoint_criteria: Optional[str]
    status: PlanStepStatus
    actual_cost_usd: float
    actual_duration_seconds: float
    actual_outcome: Optional[str]
    confidence: Optional[ConfidenceScore]
```

### Audit events
- `pfc_plan_generated`
- `pfc_plan_step_started / completed / failed`
- `pfc_plan_checkpoint_evaluated`
- `pfc_plan_completed`
- `pfc_plan_promoted_to_skill`

---

## 3. Sub-tema 6.1.2 — Confidence Scoring (8 signals)

### Decisión LOCKED: C — Multi-signal heurístico

### Signal weights

```python
SIGNAL_WEIGHTS = {
    'llm_self_report': 1.0,
    'tool_success': 2.0,
    'schema_valid': 2.5,
    'cost_accuracy': 1.5,
    'plan_consistency': 2.0,
    'multi_agent_consensus': 3.0,
    'historical': 2.5,
    'rule_eval': 3.0,
}
```

### Confidence levels

```python
class ConfidenceLevel(str, Enum):
    HIGH = "high"            # 0.90+
    MEDIUM_HIGH = "med_high" # 0.70-0.89
    MEDIUM = "medium"        # 0.50-0.69
    LOW = "low"              # 0.30-0.49
    CRITICAL = "critical"    # <0.30
```

### Stack reused
- R3 4.4 eval framework (rule_eval signal 8)
- R5 5.3.3 multi-agent message bus (consensus signal 6)
- R3 audit log (historical confidence signal 7)
- Stella embeddings (consensus computation)

### Plan-level aggregation
```python
class PlanConfidenceAggregator:
    async def aggregate(self, plan: PFCPlan) -> ConfidenceScore:
        # Weighted by step criticality (checkpoint steps = peso 2.0)
        total_weighted = sum(
            step.confidence.value * (2.0 if step.checkpoint else 1.0)
            for step in plan.steps
        )
        total_weight = sum(
            2.0 if step.checkpoint else 1.0
            for step in plan.steps
        )
        return ConfidenceScore.from_value(total_weighted / total_weight)
```

### Audit events
- `confidence_calculated` (per step)
- `plan_confidence_aggregated` (per plan)

---

## 4. Sub-tema 6.1.3 — Confidence Check Loop

### Decisión LOCKED: C — Estratificado severity + partial re-plan

### Decision matrix

```python
class CheckLoopAction(str, Enum):
    CONTINUE = "continue"
    CONTINUE_WITH_MONITORING = "continue_with_monitoring"
    CONTINUE_WITH_WARNING = "continue_with_warning"
    RE_PLAN_PARTIAL = "re_plan_partial"
    HUMAN_ESCALATE = "human_escalate"
    ABORT_GRACEFUL = "abort_graceful"
```

| Confidence Level | Default Action | Bypass Conditions |
|---|---|---|
| CRITICAL | HUMAN_ESCALATE (if workspace.human_in_loop_on_critical) OR ABORT_GRACEFUL | — |
| LOW | RE_PLAN_PARTIAL (if budget ok) OR ABORT | re_plan_count, cost budget |
| CHECKPOINT + <0.7 | RE_PLAN_PARTIAL obligatorio | re_plan budget |
| MEDIUM | CONTINUE_WITH_MONITORING | — |
| MED_HIGH / HIGH | CONTINUE | — |

### Bounds

```python
DEFAULT_MAX_RE_PLANS = 2  # workspace.max_re_plans_per_plan override
RE_PLAN_COST_BUDGET_RATIO = 0.3  # 30% extra del estimado original
CHECKPOINT_CONFIDENCE_THRESHOLD = 0.7
```

### PartialRePlanner

Preserves completed_steps exitosos. LLM genera solo steps from failed onwards con contexto outputs disponibles.

### Workspace controls (5.4.3 pattern)

```python
workspace.human_in_loop_on_critical: bool
workspace.allow_continue_after_re_plan_exhaustion: bool
workspace.max_re_plans_per_plan: int
```

### Audit events
- `confidence_check_loop_decision`
- `pfc_plan_re_planned` (con from_step + reason + count)
- `re_plan_budget_exhausted`
- `pfc_plan_human_escalated`
- `pfc_plan_aborted_graceful`

---

## 5. Sub-tema 6.1.4 — Plan → Skill Promotion (7 fases)

### Decisión LOCKED: C — 7 fases lifecycle Grafo Maestro §8.2

### Las 7 fases

**FASE 1 — DETECTION (DMN scheduled):**
- Buscar plans con mismo `promotion_candidate_pattern`
- Filter: ≥3 executions + avg_confidence ≥0.85 + success ≥0.80
- Output: `SkillCandidate` list

**FASE 2 — PROPUESTA (LLM genera spec):**
- LLM Sonnet sintetiza skill spec desde plans históricos
- Pydantic metadata + Markdown body (P1 LOCKED C+A)
- Skill state: DETECTED

**FASE 3 — SANDBOX (7 días aislado):**
- Skill state: SANDBOX
- Shadow mode (no afecta producción)
- Skill ejecuta paralelo al plan original
- Compare outputs

**FASE 4 — EVALUACIÓN (PASS/MARGINAL/FAIL):**
- ≥5 sandbox runs requeridos
- Métricas vs plan baseline
- PASS si: confidence ≥, cost ≤+10%, duration ≤+20%, success ≥0.85
- Skill state: EVALUATION → PROMOTED | ARCHIVED

**FASE 5 — PROMOCIÓN (3 tiers):**

| Tier | Approval | Threshold |
|---|---|---|
| WORKSPACE | Auto (P2 A) | Eval PASS |
| CORE | Brian 1-click approve (P2 A+B) | ≥50 usos + ≥0.90 success |
| COMMON_STACK | Brian + opt-in cliente (P2 A + P3 B) | ≥100 usos + genericity ≥0.7 |

**FASE 6 — VIDA ÚTIL:**
- Skill state: ACTIVE
- Aplicada cuando intent_pattern match (6.2.2 OPCIÓN D foundation)
- PFC usa skill como plan template
- Dopaminergic scoring continuous (6.2.4)

**FASE 7 — DECLIVE (microglía):**
- Si uso decreciente → mark DECLINING
- Documentar lessons learned
- Microglía cron archive después 30 días

### Audit events
- `skill_detected`
- `skill_proposed / moved_to_sandbox / evaluated`
- `skill_promoted_workspace / core / common_stack`
- `skill_declining / archived`

### Integration con resto Bloque
- 6.1.1: `promotion_candidate_pattern` en plan
- 6.1.2: confidence threshold para detection
- 6.1.3: re-plans documentados informan promotion
- 6.2.x: skill storage + dopaminergic + lifecycle ops

---

## 6. Eventos audit Bloque 1

Total events nuevos R6 B1: **~15 events**

- `pfc_plan_generated`
- `pfc_plan_step_started / completed / failed`
- `pfc_plan_checkpoint_evaluated`
- `pfc_plan_completed`
- `pfc_plan_promoted_to_skill`
- `confidence_calculated`
- `plan_confidence_aggregated`
- `confidence_check_loop_decision`
- `pfc_plan_re_planned`
- `re_plan_budget_exhausted`
- `pfc_plan_human_escalated`
- `pfc_plan_aborted_graceful`
- `skill_detected / proposed / moved_to_sandbox / evaluated`
- `skill_promoted_workspace / core / common_stack`
- `skill_declining / archived`

Todos workspace-scoped, payload preview ≤200 chars.

---

**Bloque 1 ✅ CERRADO — Foundation Nodo 3 PFC verdadero v1 ⚠️ flag pre-código aplica.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_06_Bloque_1_PFC_Orchestrator.md`).
