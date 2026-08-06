# Ronda 6 — Pre-Code Review Detailed (Re-revisión crítica pre-programación)

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Documento de re-revisión profunda de R6 ANTES de programar. Núcleo Pilar 3.**

**Owner:** Brian López
**Fecha inicio:** 2026-06-09
**Estado original:** 🔄 EN PROGRESO (re-revisión pre-código)
**Trigger:** Brian instruyó "VOLVER A REVISAR Y PLANIFICAR TODO EL R6" pre-programación (memory: `project_r6_critical_pre_code_review`)
**Documentos base:**
- [Ronda_06_Bloque_1_PFC_Orchestrator.md](work/Ronda_06_Bloque_1_PFC_Orchestrator.md) — B1 LOCKED v1
- [Ronda_06_Bloque_2_Ganglios_Basales_Skills.md](work/Ronda_06_Bloque_2_Ganglios_Basales_Skills.md) — B2 LOCKED v1 ⭐ Pilar 3
- Grafo Maestro Nodo 3 PFC + Nodo 4 Ganglios Basales + Pilar 3 + §8 autonomía

**IMPORTANTE:** Este documento NO re-abre las decisiones lockeadas de R6. Las REFINA a nivel implementación + AÑADE governance (Meta-Orchestrator) + calibra thresholds. Brian aprueba ANTES de código producción.

---

## Tabla de contenidos

1. [Sección A — Meta-Orchestrator (governance Pilar 3)](#a-meta-orchestrator) ✅ ACEPTADO
2. [Sección B — Calibración de thresholds](#b-calibracion) 🔄
3. [Sección C — Pseudocode + schemas formales](#c-pseudocode) ⏳
4. [Sección D — Failure modes + recovery](#d-failure-modes) ⏳
5. [Sección E — Plan de programación R6](#e-plan-programacion) ⏳

---

## A. META-ORCHESTRATOR — Governance central de Pilar 3 {#a-meta-orchestrator}

**Status:** ✅ ACEPTADO por Brian (2026-06-09, opción A)

### A.1 — El problema que resuelve

R6 diseñó un **sistema auto-modificante** (DMN detecta → LLM propone skill → sandbox → promueve → dopaminergic refuerza → auto-NO-GO). Cada componente tiene control LOCAL, pero NO había un **freno central** que vea el ecosistema completo de skills. El Grafo Maestro anticipó un "Meta-Orchestrator" (deferido a R10+) que nunca se diseñó. Esta sección lo diseña.

**NO es un nodo cerebral nuevo** (los 11/11 se mantienen). Es la capa de **governance** sobre Nodo 4 (Skills) + Nodo 6 (DMN).

### A.2 — Los 6 feedback loops peligrosos (justificación)

| # | Loop | Riesgo | Componente afectado |
|---|------|--------|---------------------|
| 1 | Runaway generation | DMN propone N skills sin techo → agota presupuesto generando, no sirviendo | 6.1.4 Fase 1-2 + DMN |
| 2 | Score inflation | Skill que "ganó temprano" domina → lock-in óptimo local, ceguera a mejores | 6.2.2 + 6.2.4 |
| 3 | NO-GO over-blocking | NO-GO se acumulan sin expiración → sistema se auto-estrangula | 6.2.3 + 6.2.4 |
| 4 | Cross-tier contradiction | Skill GO de un tier contradice GO/NO-GO de otro → comportamiento impredecible | 6.2.2 precedence |
| 5 | Promotion sin budget global | Skills proliferan sin techo → búsqueda lenta, precedence ambigua | 6.1.4 Fase 5 + 6.2.5 |
| 6 | Sandbox poisoning | Skill se valida vs los planes que la originaron (juez y parte) → falso PASS | 6.2.5 + 6.1.4 Fase 4 |

### A.3 — SkillEcosystemGovernor (6 frenos, 1 por loop)

```python
class SkillEcosystemGovernor:
    """Governance central del ecosistema de skills (Pilar 3).
       Corre como gates síncronos (path crítico, ~ms) +
       DMN task alta prioridad (background, pesado)."""

    # ── FRENO LOOP 1: Generation budget ──
    MAX_NEW_SKILLS_PER_DAY_PER_WORKSPACE = 5      # techo semántico (≠ P5 cap costo)
    MAX_SANDBOX_RUNS_PER_DAY = 20                 # techo costo generación
    # Excedente → cola (no descarta, difiere al día siguiente)

    # ── FRENO LOOP 2: Forced exploration (anti lock-in) ──
    EXPLORATION_EPSILON = 0.10                    # 10% requests prueban skill alternativa (#2)
    # rompe el rico-se-hace-más-rico; mide si alternativa es mejor

    # ── FRENO LOOP 3: NO-GO health ──
    NO_GO_REVIEW_INTERVAL_DAYS = 30
    NO_GO_FALSE_POSITIVE_THRESHOLD = 0.2          # >20% bypass legítimos → candidato retiro
    NO_GO_MAX_PER_WORKSPACE = 50                  # techo reglas negativas

    # ── FRENO LOOP 4: Contradiction detection ──
    CONTRADICTION_SIMILARITY_THRESHOLD = 0.85     # alta similarity + acciones opuestas

    # ── FRENO LOOP 5: Active skill budget ──
    MAX_ACTIVE_SKILLS_PER_WORKSPACE = 100         # techo complejidad
    # exceso → menor score va a DECLINING (poda natural, no archive directo)

    # ── FRENO LOOP 6: Independent eval ──
    # sandbox NO se compara solo vs plan fuente:
    #   golden set independiente (R3 4.4) + Microglia (R5/R6) segunda opinión
    #   CORE/COMMON_STACK → Brian approval con reporte del governor

    # ── KILL SWITCH global ──
    # Brian congela TODA generación de skills (workspace o global).
    # Freno de emergencia del Pilar 3.
```

### A.4 — Gates síncronos (path crítico) vs DMN task (background)

| Función | Modo | Cuándo |
|---------|------|--------|
| `can_generate(workspace)` | síncrono | DMN Fase 1 antes de proponer (freno 1) |
| `should_explore(workspace)` | síncrono | SkillApplicationEngine (freno 2) |
| `no_go_budget_ok(workspace)` | síncrono | NO-GO auto-propose (freno 3) |
| `check_contradictions(skill)` | síncrono (gate promo) | Promotion Fase 5 (freno 4) |
| `active_budget_ok(workspace)` | síncrono (gate promo) | Promotion Fase 5 (freno 5) |
| `independent_eval(skill)` | síncrono (gate eval) | Sandbox Fase 4 (freno 6) |
| `ecosystem_health_report(workspace)` | async DMN task | background continuo |
| `review_no_go_health(workspace)` | async DMN task | cada 30d (freno 3 review) |
| `detect_contradictions_full(workspace)` | async DMN task | background (freno 4 sweep) |

### A.5 — Ecosystem Health Report (observabilidad del Pilar 3)

```python
@dataclass
class EcosystemHealth:
    workspace_id: str
    active_skills: int          # vs MAX_ACTIVE_SKILLS (100)
    new_skills_today: int       # vs MAX_NEW_SKILLS_PER_DAY (5)
    sandbox_runs_today: int     # vs MAX_SANDBOX_RUNS_PER_DAY (20)
    no_go_count: int            # vs NO_GO_MAX (50)
    no_go_false_positive_rate: float   # vs 0.2 threshold
    contradictions_pending: int
    score_distribution: dict    # detectar inflation (¿todas 9+?)
    exploration_findings: int   # ¿la #2 ganó alguna vez? (loop 2 working)
    generation_cost_today_usd: float   # vs P5 cap (R8)
    kill_switch_active: bool
    health_verdict: str         # HEALTHY | WARNING | THROTTLED | FROZEN
```

Se expone en el **dashboard Analytics R8 8.2.2** (sección Skills Lifecycle) + alerta R8 8.4.2 si `health_verdict` degrada.

### A.6 — Integración (envuelve, no reescribe)

```
ANTES (R6 actual):
  DMN → propone → sandbox → promueve → dopaminergic → aplicar → ...

DESPUÉS (con governor):
  DMN → [GOVERNOR.can_generate] → propone → sandbox →
    [GOVERNOR.independent_eval] → promueve →
    [GOVERNOR.check_contradictions + active_budget_ok] →
    dopaminergic → aplicar [GOVERNOR.should_explore] → ...
  + ecosystem_health_report continuo
  + KILL SWITCH Brian (freno emergencia)
```

### A.7 — Audit events nuevos (Meta-Orchestrator)

- `governor_generation_throttled` (freno 1 — DMN excedió budget diario)
- `governor_exploration_triggered` (freno 2 — probó alternativa)
- `governor_exploration_winner_found` (freno 2 — alternativa ganó → re-rank)
- `governor_no_go_budget_exceeded` (freno 3)
- `governor_no_go_retirement_proposed` (freno 3 — NO-GO con falsos positivos)
- `governor_contradiction_detected` (freno 4 — CRITICAL, bloquea promo)
- `governor_active_budget_exceeded` (freno 5 — fuerza DECLINING)
- `governor_independent_eval_result` (freno 6)
- `governor_kill_switch_activated / deactivated` (Brian)
- `governor_health_report_generated`

### A.8 — Métricas Prometheus (R8 8.1.1 specialized)

- `governor_skills_generated_total` (workspace, throttled/allowed)
- `governor_explorations_total` (workspace, winner_found)
- `governor_contradictions_detected_total` (workspace)
- `governor_active_skills` (gauge, workspace)
- `governor_no_go_false_positive_rate` (gauge, workspace)
- `governor_health_verdict` (gauge enum, workspace)

### A.9 — Decisión LOCKED

**Meta-Orchestrator (SkillEcosystemGovernor) AÑADIDO a R6 como governance central de Pilar 3.** 6 frenos mapeados 1:1 a 6 loops. Gates síncronos (path) + DMN task (background) + kill switch Brian. Envuelve componentes existentes sin reescribirlos. Thresholds en A.3 son **bootstrap conservador** — se calibran en Sección B.

---

## B. CALIBRACIÓN DE THRESHOLDS {#b-calibracion}

**Status:** ✅ LOCKED — Estrategia "MUY CONSERVADOR v1" (Brian 2026-06-09)

### B.0 — Principio rector

> ❝ Un sistema auto-modificante debe arrancar PESIMISTA y ganarse la confianza con datos, no arrancar optimista y perderla con fallos. ❞

**Decisión Brian:** bootstrap **MUY CONSERVADOR** para v1 (primeros clientes pilot reales). Pilar 3 arranca casi "apagado" — genera y observa skills pero casi no las auto-aplica; fallback a PFC planning por defecto; Brian aprueba más; se suelta gradualmente cuando los datos demuestran confianza.

### B.1 — Trampa de la calibración pre-código

NO podemos calibrar con datos reales (el sistema aún no está en producción). Pedir "calibración perfecta" pre-código es imposible. La solución NO es adivinar mejor, sino:

1. **Bootstrap conservador** (errar hacia lo seguro/lento)
2. **Todo observable** (cada threshold → métrica predicted vs actual)
3. **Protocolo de tuning definido** (cómo ajustar con datos, no guess)
4. **Nada hardcoded** (thresholds configurables global/workspace/tier)

### B.2 — Clasificación por riesgo (3 categorías)

| Categoría | Si falla | Bootstrap | Tuning |
|-----------|----------|-----------|--------|
| **SEGURIDAD** | compromete seguridad/compliance | MUY restrictivo | lento + Brian approval |
| **COSTO** | infla costo sin valor | conservador | con métricas ROI |
| **APRENDIZAJE** | degrada calidad gradual | lento | con outcome data |

- **Seguridad:** NO-GO HARD_BLOCK (nunca relajan), cross-tier contradiction (0.85), common_stack promotion
- **Costo:** generation budget, re-plan budget, PFC planning cost estimate
- **Aprendizaje:** confidence weights, dopaminergic, promotion thresholds, exploration epsilon

### B.3 — Confidence Scoring (6.1.2) recalibrado

- **Separar señales DURAS vs BLANDAS:**
  - DURAS (deterministas, peso alto): schema_valid, tool_success, rule_eval, cost_accuracy
  - BLANDAS (opiniones, peso bajo): llm_self_report, plan_consistency
  - CONTEXTUALES (peso medio): multi_agent_consensus, historical
- **Bootstrap pesimista:** confidence calculada se sesga A LA BAJA (margen seguridad). Mejor re-plan/escalate de más que confiar de más.
- **Observable:** registrar (confidence_predicha vs outcome_real) → calibration curve.
- **Tuning:** tras ~200 planes reales, ajustar pesos por calibración. Brian approval (categoría aprendizaje).
- **Config:** SIGNAL_WEIGHTS global configurable (no hardcoded).

### B.4 — Dopaminergic Scoring (6.2.4) recalibrado

- **Decay más suave inicial:** 0.98/día (≈50% en ~34d) vs 0.95 original — no castigar skills prematuramente por no-uso.
- **Reward NO es única señal de aplicación:** governor freno 2 (epsilon exploración) rompe inflación independiente del score.
- **Skills nuevas = score 5.0 neutral,** necesitan EVIDENCIA para subir (no beneficio de la duda).
- **Observable:** score_distribution (health report A.5). Convergencia a 9+ → inflación → recalibrar.
- **Tuning:** score debe CORRELACIONAR con success_rate real. Si no correlaciona → fórmula mal.

### B.5 — Promotion Thresholds recalibrados (MUY CONSERVADOR v1)

| Tier | Bootstrap v1 (conservador) | Aprobación |
|------|----------------------------|------------|
| WORKSPACE (auto) | eval PASS + ≥3 usos exitosos + **shadow-heavy inicial** (se aplica poco, fallback PFC default) | auto (con governor gates) |
| CORE | ≥30 usos + score ≥8.0 + 0 contradicciones (freno 4) + independent eval PASS (freno 6) + **estabilidad** (success_rate consistente, baja varianza) | Brian SIEMPRE (no auto) |
| COMMON_STACK | genericity ≥0.7 (DEFINIDA: % skill que NO referencia workspace-specific) + ≥100 usos + 0 contradicciones cross-workspace | Brian + opt-in cliente |

**v1 muy conservador:** WORKSPACE skills se generan + observan pero auto-aplicación mínima al inicio (shadow-heavy); fallback a PFC planning por defecto hasta acumular evidencia fuerte. Exploration epsilon bajo (0.05 v1 vs 0.10 estándar).

**Observable:** tasa promoción + tasa democión (CORE que luego declina = promovimos mal). Si democión >20% → subir bar.

### B.6 — NO-GO Thresholds recalibrados (categoría seguridad)

- **NO auto-activar NO-GO por streak solo.** Requerir: ≥5 fallos EN VENTANA + misma causa raíz + NO atribuibles a outage externo (cruzar incidents R8) + **Brian review** (auto-NO-GO son PROPUESTAS, no activaciones).
- **Expiración:** NO-GO auto-generado tiene TTL (90d) + review (freno 3). No inmortales (excepto HARD compliance).
- **False positive tracking:** bypass legítimo >20% → candidato retiro (freno 3).
- **Observable:** no_go_count + false_positive_rate (health report).

### B.7 — Budgets recalibrados (categoría costo)

- **Re-plan:** max 2 conservador OK. Ratio 0.3 → configurable per-TIER (enterprise más que pilot).
- **Generation budget (governor):** 5 skills/día per-workspace conservador OK v1. Mantener.
- **⚠️ BUG DETECTADO — PFC_PLANNING_COST_ESTIMATE ($0.05):** NO es threshold, es una ASUNCIÓN que infla el "cost_saved" de aplicar skills. DEBE MEDIRSE real (instrumentar PFC planning cost en R8 8.1.3) y usar valor MEDIDO. Si planning real cuesta $0.02, el ROI de skills es menor de lo asumido. **Acción: medir antes de reportar cost_saved.**

### B.8 — Protocolo de tuning (cómo ajustar con datos)

```
1. Cada threshold → métrica observable (predicted vs actual)
2. Ventana mínima de datos antes de tunear:
   - Confidence: ~200 planes con outcomes
   - Dopaminergic: ~50 ejecuciones por skill
   - Promotion: ~10 promociones con seguimiento de democión
3. Cambios por categoría:
   - SEGURIDAD → Brian approval obligatorio + audit
   - COSTO → automático si dentro de guardrails + reporte
   - APRENDIZAJE → Brian approval + calibration curve evidence
4. Todo cambio de threshold → audit event (threshold_recalibrated)
5. Config versionada (no hardcoded, no requiere re-deploy)
```

### B.9 — Decisión LOCKED

**Calibración R6 = bootstrap MUY CONSERVADOR v1 + 4 principios (conservador + observable + protocolo tuning + nada hardcoded) + clasificación 3 categorías de riesgo.** Thresholds recalibrados en B.3-B.7. Bug PFC_PLANNING_COST identificado (medir, no asumir). Tuning con datos reales post-producción, cambios seguridad/aprendizaje con Brian approval.

---

## C. PSEUDOCODE + SCHEMAS FORMALES {#c-pseudocode}

**Status:** ✅ LOCKED — 5 gaps críticos resueltos. (Pseudocode trivial se resuelve al programar.)

### C.1 — `_skill_to_plan()` — conversión skill→plan con validación de obsolescencia

**Por qué crítica:** donde una skill (markdown) se vuelve plan ejecutable. En B2 solo mencionada (líneas 265, 651). Riesgo: skill vieja referencia tool eliminado → ejecuta y falla a mitad.

```python
async def _skill_to_plan(self, skill, request, signals) -> PFCPlan:
    # 1. Parse markdown → steps (C.2). Corrupto → fallback
    try:
        raw_steps = parse_skill_steps_section(skill.body_markdown)
    except SkillParseError:
        raise SkillToPlanError('parse_failed', fallback=True)
    # 2. VALIDACIÓN OBSOLESCENCIA: tools/specialists ¿existen HOY?
    for step in raw_steps:
        if step.specialist_or_tool not in tool_registry.available_tools():
            raise SkillToPlanError('tool_unavailable', fallback=True)
    # 3. VALIDACIÓN: subgraph_mode compatible con signals actuales
    if skill.subgraph_mode_required == 'complete' and signals.subgraph_mode == MINIMUM:
        raise SkillToPlanError('subgraph_mismatch', fallback=True)
    # 4. PFCPlan con source_skill_id (trazable) + estimaciones de métricas
    #    históricas de la skill (NO re-estimar con LLM = el ahorro)
    plan = PFCPlan(source_skill_id=skill.id,
                   steps=[PlanStep.from_skill_step(s, request) for s in raw_steps],
                   estimated_total_cost_usd=skill.metrics.avg_cost_usd, ...)
    # 5. Pre-flight validation (reusa 5.3.4 layer 1)
    await preflight_validate(plan)
    return plan
```
**Gap resuelto:** validación de obsolescencia ANTES de ejecutar skill vieja.

### C.2 — `parse_skill_steps_section()` — parser robusto (estaba en `...`)

**Por qué:** B2 líneas 300-307 = stub. Lee markdown que el LLM generó (puede ser inconsistente).

```python
def parse_skill_steps_section(markdown_body) -> list[SkillStep]:
    section = extract_markdown_section(markdown_body, ['Pasos', 'Steps'])
    if not section: raise SkillParseError('no_steps_section')
    steps = []
    for raw in split_by_heading(section, level=3):
        step = SkillStep(description=..., specialist_or_tool=...,
                         expected_outcome=..., checkpoint=...)
        if not step.specialist_or_tool:    # Pydantic strict: rechaza step sin tool
            raise SkillParseError(f'step missing tool: {raw.title}')
        steps.append(step)
    if not steps: raise SkillParseError('empty_steps')
    return steps
```

### C.3 — Sandbox eval INDEPENDIENTE (Fase 4) — cumple freno 6

**Por qué:** B2 líneas 645-662 ejecuta sandbox pero el compare era vago. Sección A freno 6 exige eval independiente (no solo vs fuente).

```python
async def evaluate_sandbox_run(self, skill, sandbox_result, baseline) -> SandboxEvaluation:
    vs_baseline = {confidence_delta, cost_delta_pct, duration_delta_pct}  # señal 1
    # EVAL INDEPENDIENTE (freno 6):
    golden_score = await eval_framework.run_golden(sandbox_result.output, skill.category)  # R3 4.4
    microglia_verdict = await microglia.evaluate_output(sandbox_result.output)             # R5/R6
    passed = (confidence_delta >= 0 and cost_delta_pct <= 0.10 and
              duration_delta_pct <= 0.20 and golden_score >= GOLDEN_MIN and
              microglia_verdict.passed)
    verdict = 'PASS' if passed else ('MARGINAL' if golden_score >= GOLDEN_MARGINAL else 'FAIL')
    await audit_logger.log('governor_independent_eval_result', skill_id=skill.id, verdict=verdict)
    return SandboxEvaluation(verdict=verdict, ...)
```

### C.4 — `partial_re_plan()` (6.1.3) — preservar estado REAL

**Por qué:** B1 líneas 206-208 dice "preserva completed" sin cómo. Riesgo: re-plan inconsistente con estado real.

```python
async def partial_re_plan(self, original_plan, failed_step_idx, failure_reason) -> PFCPlan:
    # 1. GATE budget (6.1.3 + governor)
    if original_plan.re_plan_count >= workspace.max_re_plans_per_plan: raise RePlanBudgetExhausted()
    if spent_ratio > (1 + RE_PLAN_COST_BUDGET_RATIO): raise RePlanBudgetExhausted('cost')
    # 2. Preservar completed + CAPTURAR estado de salida REAL
    completed = original_plan.steps[:failed_step_idx]
    completed_outputs = {s.step_id: s.actual_outcome for s in completed}
    # 3. LLM re-planea desde failed CON contexto del estado REAL (consistencia)
    new_tail = await llm_replan(completed_context=completed_outputs, failure_reason=..., ...)
    # 4. plan = completed (preservados) + new_tail (re-planeados)
    re_plan.steps = completed + new_tail; re_plan.re_plan_count += 1
    return re_plan
```
**Gap resuelto:** LLM ve el estado REAL producido (no asumido) → re-plan consistente.

### C.5 — Schemas Pydantic formales (faltaban)

```python
class SkillMetadata(BaseModel):
    skill_id, workspace_id, tier, category, pattern, version, state
    intent_pattern, intent_keywords, trigger_confidence_threshold: float = Field(ge=0, le=1)
    required_tools, required_specialists, subgraph_mode_required
    metrics: SkillMetrics; scoring: SkillScoring
    # NO-GO (faltaba formalizar):
    blocks_tools: list = []; blocks_patterns: list = []; blocks_skills: list = []
    no_go_severity: Optional[NoGoSeverity] = None
    no_go_ttl_days: Optional[int] = None         # expiración (B.6)
    governor_flags: list[str] = []               # contradictions etc (Sección A)
    source_plans: list[str] = []

class SkillMetrics(BaseModel):
    total_executions, successful_executions, success_rate, avg_confidence,
    avg_cost_usd, avg_duration_seconds
    success_rate_variance: float = 0.0           # estabilidad (B.5 CORE promo)
    last_used_at: Optional[datetime]

class SkillToPlanError(Exception):               # excepción tipada (faltaba)
    def __init__(self, reason, fallback=True):
        self.reason, self.fallback = reason, fallback  # fallback → PFC planning
```

---

## D. FAILURE MODES + RECOVERY {#d-failure-modes}

**Status:** ✅ LOCKED — Skill failure = "Re-plan + rollback" (Brian 2026-06-09)

### D.1 — Skill auto-aplicada falla a mitad de ejecución (CRÍTICO)

**Escenario:** skill ejecuta, ya hizo acciones reales (creó archivos, llamó APIs, modificó estado), y un step posterior falla.

**Decisión: Re-plan + rollback de efectos (compensating actions).**

```python
async def handle_skill_execution_failure(self, plan, failed_step_idx, error):
    # 1. ROLLBACK: compensating actions de steps ya ejecutados (orden inverso)
    completed = plan.steps[:failed_step_idx]
    for step in reversed(completed):
        if step.compensating_action:          # ← cada step declara su rollback
            try:
                await execute_compensating_action(step.compensating_action, step.actual_outcome)
                await audit_logger.log('skill_step_rolled_back', step_id=step.step_id)
            except CompensationFailed:
                # 2. Rollback imposible (acción irreversible) → escalate
                await audit_logger.log('skill_rollback_failed', step_id=step.step_id, severity='critical')
                incident = await incident_engine.create(    # R8 8.4.3
                    severity='SEV2', title='Skill rollback failed — manual intervention',
                    cause=f'irreversible effect in skill {plan.source_skill_id}')
                await notification_service.send_critical(...)  # Brian
                break  # no seguir rollback si uno irreversible

    # 3. RE-PLAN parcial desde punto sano (C.4) si budget permite
    if can_re_plan(plan):
        re_plan = await partial_re_plan(plan, failed_step_idx, str(error))
        return await pfc_executor.execute_plan(re_plan, workspace)

    # 4. PUNISHMENT dopaminergic FUERTE a la skill (6.2.4)
    await dopaminergic_scorer.record_punishment(
        plan.source_skill_id, severity='execution_failure', magnitude='high')

    # 5. Si esta skill acumula failures → auto-NO-GO proposal (governor freno 3)
```

**Requisito nuevo:** cada `PlanStep` / `SkillStep` declara su `compensating_action` (cómo deshacer su efecto). Para steps sin compensating action posible (irreversibles) → se marca `reversible=False` y un fallo posterior escala directo a Brian (no intenta rollback que empeore).

### D.2 — Otros failure modes (resumen)

| Failure | Recovery |
|---------|----------|
| Skill markdown corrupto (C.2) | SkillParseError → fallback PFC planning + flag skill para review |
| Tool de skill ya no existe (C.1) | SkillToPlanError → fallback PFC planning + skill → review (obsoleta) |
| Re-plan budget exhausted (C.4) | abort graceful o human escalate (6.1.3 workspace setting) |
| Sandbox eval FAIL (C.3) | skill → ARCHIVED (no promueve) + audit |
| Governor detecta contradiction (A freno 4) | bloquea promoción + Brian review |
| Governor budget exceeded (A frenos 1/5) | throttle/cola (no descarta) |
| DMN genera skill que viola HARD NO-GO | bloqueada en generación (no llega a sandbox) |
| Concurrent skill modification (6.2.5) | Postgres advisory lock + SkillConcurrentModificationError → retry |
| Embedding compute falla (Stella) | skill write difiere indexing (cola) — no bloquea write |

### D.3 — Principio de failure

> Toda acción auto-generada (Pilar 3) debe ser **reversible o escalable**. Si no es ninguna → no se auto-aplica (requiere human-in-loop). El sistema NUNCA deja efectos irreversibles a medias sin avisar a Brian (incident SEV2).

---

## E. PLAN DE PROGRAMACIÓN R6 {#e-plan-programacion}

**Status:** ✅ LOCKED — orden de implementación foundation-first

### E.1 — Orden de programación R6 (dependencias)

```
1. Schemas + storage (6.2.1): SkillMetadata/Metrics/Scoring Pydantic +
   Postgres tables + RLS + filesystem layout + atomic write
   → foundation, todo lo demás depende de esto

2. PFC core (6.1.1): PFCPlan + PlanStep + executor + pre-flight
   → el motor de ejecución

3. Confidence (6.1.2) + Check loop (6.1.3): scoring + re-plan + C.4
   → calidad de ejecución (bootstrap pesimista B.3)

4. Skill application GO (6.2.2): _skill_to_plan (C.1) + parser (C.2) +
   PFCRouter integration
   → aplicar skills (shadow-heavy v1 — B.5)

5. NO-GO (6.2.3): checker + enforcement + HARD bootstrap + TTL (B.6)
   → seguridad (categoría 1)

6. Dopaminergic (6.2.4): scoring + lifecycle triggers (decay 0.98 B.4)
   → aprendizaje

7. Lifecycle manager (6.2.5): state machine + sandbox + microglia + APIs

8. Plan→Skill promotion (6.1.4): 7 fases + sandbox eval independiente (C.3)
   → generación (conservador B.5)

9. ⭐ META-ORCHESTRATOR (Sección A): governor gates + DMN task + kill switch
   → SE PROGRAMA EN PARALELO/ANTES de activar auto-generación (8)
   → es el FRENO; debe existir ANTES de soltar el bucle

10. Failure handling (Sección D): compensating actions + rollback
    → transversal, integrar en executor (2)
```

### E.2 — Gates de validación pre-producción R6

- [ ] Schemas Pydantic + RLS testeados (aislamiento workspace)
- [ ] Confidence calibration curve instrumentada (B.3 observable)
- [ ] PFC_PLANNING_COST medido real (B.7 bug — no asumido)
- [ ] Governor gates funcionando ANTES de activar auto-generación
- [ ] Kill switch probado (congela generación)
- [ ] Compensating actions definidas para tools con efectos reales
- [ ] Sandbox eval independiente (golden + Microglia) funcionando
- [ ] HARD NO-GO bootstrap (§8.4 compliance) cargados
- [ ] Bootstrap MUY CONSERVADOR activo (shadow-heavy, fallback default)
- [ ] Custom attack suite (R9 9.2.2) incluye intentos de skill poisoning

### E.3 — Definición de "Pilar 3 listo para v1"

```
Pilar 3 está listo cuando:
• Genera skills (observación) ✓
• Las aplica de forma MUY conservadora (shadow-heavy, evidencia fuerte) ✓
• Governor frena los 6 loops ✓
• Kill switch disponible (Brian) ✓
• Failures reversibles o escalados (nunca irreversible a medias) ✓
• Todo observable (health report + calibration curves) ✓
• Thresholds tunables sin re-deploy ✓

→ Pilar 3 GOBERNADO, no solo activado.
```

---

## Resumen de la re-revisión R6

| Sección | Status | Output |
|---------|--------|--------|
| A — Meta-Orchestrator | ✅ LOCKED | Governor 6 frenos + kill switch (gap arquitectónico cerrado) |
| B — Calibración | ✅ LOCKED | Muy conservador v1 + 4 principios + bug PFC cost |
| C — Pseudocode/schemas | ✅ LOCKED | 5 gaps resueltos (obsolescencia, parser, eval indep, re-plan, schemas) |
| D — Failure modes | ✅ LOCKED | Re-plan + rollback compensating + principio reversible/escalable |
| E — Plan programación | ✅ LOCKED | Orden foundation-first + gates pre-prod + def "listo v1" |

**R6 re-revisión COMPLETA. Lista para programar con governance + calibración + failure handling. Brian aprobó: Meta-Orchestrator (A), muy conservador (B), re-plan+rollback (D).**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_06_Pre_Code_Review_Detailed.md`).
