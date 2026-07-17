# Ronda 5 — DMN Tasks Detailed (Refinamiento crítico 5.4.2 pre-programación)

**Refinamiento profundo de las 8 DMN tasks ANTES de programar. Núcleo valor diferencial.**

**Owner:** Brian López
**Fecha:** 2026-06-09
**Status:** ✅ REFINAMIENTO COMPLETADO
**Trigger:** Brian marcó 5.4.2 "ATENCION PROFUNDA pre-programación" (memory: `dmn-tasks-critical-refinement`)
**Base:** [Ronda_05_Bloque_4_DMN_Default_Mode.md](Ronda_05_Bloque_4_DMN_Default_Mode.md) §3 (5.4.2 LOCKED v1)
**Sinergia:** [Ronda_06_Pre_Code_Review_Detailed.md](Ronda_06_Pre_Code_Review_Detailed.md) §A (Meta-Orchestrator)

**IMPORTANTE:** NO re-abre la decisión lockeada (8 tasks). REFINA a detalle ejecutable + conecta el auto-improvement loop al Meta-Orchestrator (R6) en vez de duplicar governance.

---

## 1. Gaps que este doc resuelve

| Gap | Descripción | Resuelto en |
|-----|-------------|-------------|
| 1 | 8 tasks son stubs (`TASK_ACTIONS` referenciado, nunca definido) | §3 + §4 |
| 2 | Triggers son nombres, no condiciones defendibles | §3 + §4 (cada task) |
| 3 | Auto-improvement loop apenas esbozado | §5 (reusa governor R6) |
| 4 | ROI no medible (task puede ser puro costo) | §6 |
| 5 | Interacciones entre tasks no formalizadas | §7 |

## 2. Clasificación: HOUSEKEEPING vs GENERATIVAS (Brian 2026-06-09)

```
   La naturaleza de las 8 tasks es radicalmente distinta. Tratarlas
   igual = burocracia a triviales + poco rigor a peligrosas.

   ┌─ HOUSEKEEPING (5) ─ mantenimiento, bajo riesgo, outcome directo ─┐
   │  • embedding_precompute    (LOW   risk · $0 Stella local)         │
   │  • cache_prewarming        (LOW   risk · $0.15)                   │
   │  • memory_consolidation    (MEDIUM risk · $0.10)                  │
   │  • routing_learning        (LOW   risk · $0.05)                   │
   │  • eval_regression_detect  (MEDIUM risk · $0.05)                  │
   │  → outcome MEDIBLE directo · auto-apply OK · NO review queue      │
   └───────────────────────────────────────────────────────────────────┘

   ┌─ GENERATIVAS (3) ─ producen ideas/cambios, alto riesgo ───────────┐
   │  • pattern_detection       (MEDIUM risk · $0.05)                 │
   │  • hypothesis_generation   (HIGH  risk · $0.50 Opus)             │
   │  • prompt_improvement      (HIGH  risk · $0.20)                  │
   │  → auto-improvement LOOP + GOVERNOR (R6 §A) + review obligatorio  │
   └───────────────────────────────────────────────────────────────────┘
```

**Principio:** housekeeping = "el sistema se mantiene solo" (seguro). Generativas = "el sistema se mejora solo" (= autonomía generativa = necesita governance, igual que skills Pilar 3).

---

## 3. HOUSEKEEPING TASKS (5) — detalle

> Pipeline housekeeping: `trigger_fn → action_fn → outcome_metric` (NO review queue — el outcome es directo y medible; si degrada, la métrica lo muestra y se auto-disable).

### 3.1 — embedding_precompute (LOW · $0)
```python
async def trigger_embedding_precompute(ws) -> bool:
    # Hay items sin embedding (episodios nuevos, skills, docs)
    pending = await embedding_queue.count_pending(ws.id)
    return pending > 0   # threshold simple: cualquier pendiente

async def action_embedding_precompute(ws) -> DMNTaskResult:
    pending = await embedding_queue.get_pending(ws.id, limit=200)
    for item in pending:
        emb = await stella.embed(item.text)        # local, $0
        await store_embedding(item, emb)
    return DMNTaskResult(items_processed=len(pending), cost=0.0,
                         outcome_metric={'embeddings_created': len(pending)})
# OUTCOME MEDIBLE: # embeddings creados. ROI: queries futuras más rápidas.
# RIESGO: ninguno (precomputar es idempotente). auto-apply directo.
```

### 3.2 — cache_prewarming (LOW · $0.15)
```python
async def trigger_cache_prewarming(ws) -> bool:
    # Patrones frecuentes con baja cache hit rate (5.2.3 fast path layer E)
    hit_rate = await cache_stats.get_hit_rate(ws.id, window='7d')
    frequent_misses = await cache_stats.frequent_misses(ws.id, top_k=10)
    return hit_rate < 0.5 and len(frequent_misses) >= 3   # threshold defendible:
    # <50% hit + ≥3 patrones recurrentes que fallan = vale pre-warmear

async def action_cache_prewarming(ws) -> DMNTaskResult:
    misses = await cache_stats.frequent_misses(ws.id, top_k=10)
    warmed = 0
    for pattern in misses:
        result = await precompute_response(ws, pattern)   # LLM, costo real
        await cache.store(ws.id, pattern, result, ttl=...)
        warmed += 1
    return DMNTaskResult(cost=warmed * 0.015,
                         outcome_metric={'patterns_warmed': warmed})
# OUTCOME MEDIBLE: cache hit rate ANTES vs DESPUÉS (próximos 7d).
# ROI: si hit rate sube → ahorro LLM real. Si no sube → disable.
# RIESGO: bajo (cache stale → TTL lo limpia).
```

### 3.3 — memory_consolidation (MEDIUM · $0.10) — Grafo Maestro LITERAL
```python
async def trigger_memory_consolidation(ws) -> bool:
    # Episodios sin consolidar a KG (R2 4.4 CLS pattern)
    unconsolidated = await episode_store.count_unconsolidated(ws.id)
    return unconsolidated >= 20   # threshold: ≥20 episodios = vale consolidar
    # (no cada episodio — batch para eficiencia, como sueño REM consolida el día)

async def action_memory_consolidation(ws) -> DMNTaskResult:
    episodes = await episode_store.get_unconsolidated(ws.id, limit=100)
    # LLM Haiku extrae facts/relaciones → KG (Apache AGE)
    facts = await llm_extract_facts(episodes)   # Haiku barato
    for fact in facts:
        await kg.upsert_fact(ws.id, fact)        # idempotente (upsert)
        await episode_store.mark_consolidated(episode_ids)
    return DMNTaskResult(cost=..., outcome_metric={'facts_extracted': len(facts),
                         'episodes_consolidated': len(episodes)})
# OUTCOME MEDIBLE: facts añadidos al KG + episodios consolidados.
# MEDIUM risk: extrae facts que se usan en contexto futuro → si extrae mal,
#   contamina KG. MITIGACIÓN: upsert idempotente + facts tienen source +
#   confidence; KG queries filtran low-confidence. NO review (volumen alto)
#   PERO eval_regression (3.5) detecta si KG degrada retrieval.
```

### 3.4 — routing_learning (LOW · $0.05)
```python
async def trigger_routing_learning(ws) -> bool:
    # Suficientes requests nuevos desde último learning (feed 5.2.2 history-aware)
    new_requests = await request_log.count_since_last_routing_learning(ws.id)
    return new_requests >= 50   # threshold: ≥50 nuevos = señal estadística útil

async def action_routing_learning(ws) -> DMNTaskResult:
    # Analiza (request → ruta elegida → outcome) histórico
    # Actualiza el history-aware index (5.2.2) — NO cambia lógica de routing,
    # solo enriquece el contexto histórico que el router consulta
    samples = await request_log.get_routing_samples(ws.id, limit=500)
    updated = await routing_history_index.update(ws.id, samples)
    return DMNTaskResult(cost=..., outcome_metric={'routing_samples_learned': updated})
# OUTCOME MEDIBLE: routing accuracy (¿el router elige mejor con más historia?).
# LOW risk: solo enriquece contexto, no cambia decisiones directamente.
```

### 3.5 — eval_regression_detection (MEDIUM · $0.05)
```python
async def trigger_eval_regression(ws) -> bool:
    # Semanal (R3 4.4 weekly) O drift detectado en métricas
    last_eval = await eval_history.get_last_run(ws.id)
    return (now() - last_eval) > 7*DAY or await metrics_drift_detected(ws.id)

async def action_eval_regression(ws) -> DMNTaskResult:
    # Corre golden set (R3 4.4) vs baseline. Compara scores.
    current = await eval_framework.run_golden(ws.id)
    baseline = await eval_history.get_baseline(ws.id)
    regression = current.score < baseline.score - REGRESSION_THRESHOLD  # 0.05
    if regression:
        await alert_service.send(ws.id, 'eval_regression_detected', ...)  # R8 8.4.2
    return DMNTaskResult(cost=..., outcome_metric={'eval_score': current.score,
                         'regression_detected': regression})
# OUTCOME MEDIBLE: detecta degradación de calidad ANTES que el cliente.
# MEDIUM risk: NO cambia nada, solo ALERTA. El valor es la detección temprana.
# Esta task es de hecho un GUARDIÁN de las otras (detecta si memory_consolidation
#   o algo degradó la calidad).
```

---

## 4. GENERATIVAS TASKS (3) — detalle + auto-improvement loop

> Pipeline generativo: `trigger_fn → action_fn → GOVERNOR gate (R6 §A) → review queue → approval → promote → measure`. Estas NO auto-aplican (v1 muy conservador, como skills Pilar 3).

### 4.1 — pattern_detection (MEDIUM · $0.05) — Grafo Maestro LITERAL
```python
async def trigger_pattern_detection(ws) -> bool:
    recent = await request_log.get_recent(ws.id, days=14)
    return len(recent) >= 10   # mínimo de datos para que un patrón sea significativo

async def action_pattern_detection(ws) -> DMNTaskResult:
    recent = await request_log.get_recent(ws.id, days=14)
    # Clustering por embedding similarity (Stella, local)
    clusters = cluster_by_similarity(recent, threshold=0.82)  # threshold DEFENDIBLE:
    # 0.82 = "claramente el mismo tipo de tarea" sin ser idéntico literal
    detected = []
    for cluster in clusters:
        if len(cluster) >= 3:   # "3 PRs similares" del Grafo Maestro = patrón real
            detected.append(DetectedPattern(
                pattern_signature=..., occurrences=len(cluster),
                example_request_ids=[r.id for r in cluster[:3]],
                # candidato a SKILL (feed Pilar 3 6.1.4 Fase 1)
            ))
    # GOVERNOR gate: ¿puede generar más patrones hoy? (R6 §A freno 1)
    detected = await governor.filter_generation_budget(ws.id, detected)
    return DMNTaskResult(cost=..., outcome_metric={'patterns_detected': len(detected)},
                         generative_output=detected)  # → review queue (§5)
# OUTCOME MEDIBLE: patrones → ¿cuántos se vuelven skills útiles? (downstream)
# MEDIUM risk: solo DETECTA (no actúa). Pero alimenta skill generation (Pilar 3)
#   → por eso pasa por governor budget. Es el PUENTE DMN→Skills.
```

### 4.2 — hypothesis_generation (HIGH · $0.50 Opus) — Grafo Maestro LITERAL
```python
async def trigger_hypothesis_generation(ws) -> bool:
    # opt-in (enabled_by_default=False) + señales de riesgo en el codebase del cliente
    if not ws.dmn_hypothesis_generation_enabled: return False
    risk_signals = await codebase_analyzer.get_risk_signals(ws.id)
    return len(risk_signals) >= 3   # ≥3 señales (churn alto, baja cobertura, etc)

async def action_hypothesis_generation(ws) -> DMNTaskResult:
    signals = await codebase_analyzer.get_risk_signals(ws.id)
    # LLM Opus genera hipótesis "este módulo va a romper porque..."
    hypotheses = await llm_opus_hypothesize(signals, ws_context)
    # GOVERNOR gate (R6 §A freno 1 budget)
    hypotheses = await governor.filter_generation_budget(ws.id, hypotheses)
    return DMNTaskResult(cost=..., outcome_metric={'hypotheses_generated': len(hypotheses)},
                         generative_output=hypotheses)  # → review queue (§5), risk=HIGH
# OUTCOME MEDIBLE: hipótesis → ¿se confirmaron? (track: hipótesis vs bugs reales)
#   = el ROI más valioso (predijo un bug antes de que pasara) PERO también el más
#   caro (Opus) y ruidoso (puede alucinar). HIGH risk → SIEMPRE review (5.4.3).
# v1 MUY CONSERVADOR: opt-in + review obligatorio + cap estricto de generación.
```

### 4.3 — prompt_improvement (HIGH · $0.20)
```python
async def trigger_prompt_improvement(ws) -> bool:
    if not ws.dmn_prompt_improvement_enabled: return False
    # Eval scores bajos consistentes en algún tipo de tarea
    low_eval_categories = await eval_history.categories_below(ws.id, threshold=0.7)
    return len(low_eval_categories) >= 1

async def action_prompt_improvement(ws) -> DMNTaskResult:
    low_cats = await eval_history.categories_below(ws.id, threshold=0.7)
    proposals = []
    for cat in low_cats:
        # LLM propone mejora del prompt template (R3 B2 Jinja2)
        improved = await llm_improve_prompt(cat.current_template, cat.failure_examples)
        proposals.append(PromptImprovement(
            category=cat, current=cat.current_template, proposed=improved,
        ))
    proposals = await governor.filter_generation_budget(ws.id, proposals)
    return DMNTaskResult(cost=..., outcome_metric={'prompt_improvements': len(proposals)},
                         generative_output=proposals)  # → review queue, risk=HIGH
# OUTCOME MEDIBLE: prompt mejorado → A/B test (eval score nuevo vs viejo en sandbox).
# HIGH risk: cambiar un prompt afecta TODAS las respuestas de esa categoría →
#   NUNCA auto-apply. Review + A/B test obligatorio (sandbox, como skills).
```

---

## 5. AUTO-IMPROVEMENT LOOP (gap 3) — reusa Meta-Orchestrator (R6 §A)

```
   CLAVE: DMN generativo es la MISMA naturaleza que skills Pilar 3
   (sistema auto-modificante). NO duplicamos governance — los outputs
   generativos de DMN se enchufan al GOVERNOR + review queue que ya
   diseñamos en R6 §A.

   FLUJO END-TO-END (generativas):
   ─────────────────────────────────
   1. DMN task genera output (pattern/hypothesis/prompt_improvement)
   2. GOVERNOR gate (R6 §A): budget OK? contradicción? → throttle/cola
   3. Risk classification (5.4.3 TASK_RISK_MAP): HIGH → review obligatorio
   4. REVIEW QUEUE (5.4.3 dmn_output_pending_review):
      • Brian/cliente ve el output en dashboard (R7 + R8 8.2.2)
      • Aprueba / rechaza / modifica
   5. Si aprobado:
      • pattern_detection → feed skill generation (Pilar 3 6.1.4 Fase 1)
      • prompt_improvement → A/B test sandbox → si mejora → promote
      • hypothesis → notifica cliente (es información, no cambio de sistema)
   6. MEDIR outcome (§6 ROI):
      • ¿el output aprobado realmente mejoró algo?
      • Feed back al task: tasks cuyos outputs se aprueban+sirven → +valor
   7. Aprobado/rechazado → audit + métrica approval_rate per task

   KILL SWITCH (R6 §A): Brian congela generación DMN igual que skills.
```

```python
class DMNAutoImprovementLoop:
    async def process_generative_output(self, ws, task_name, output, risk):
        # 1. Governor gate (reusa R6 §A)
        if not await governor.can_generate(ws.id):
            await audit_logger.log('governor_generation_throttled', task=task_name)
            return  # cola, no descarta

        # 2. Risk → review decision (5.4.3 decision matrix)
        if risk == DMNOutputRisk.HIGH or not ws.dmn_output_auto_apply:
            await review_queue.enqueue(ws.id, task_name, output, risk)
            await audit_logger.log('dmn_output_pending_review', task=task_name, risk=risk)
            return  # espera approval humano (v1 muy conservador)

        # 3. LOW risk + auto_apply → aplica directo (solo housekeeping nunca llega aquí)
        await self._apply_output(ws, task_name, output)

    async def on_approval(self, output_id, approved_by):
        output = await review_queue.get(output_id)
        if output.task_name == 'pattern_detection':
            await skill_candidate_queue.add(output)        # → Pilar 3 (6.1.4)
        elif output.task_name == 'prompt_improvement':
            await prompt_ab_test.start(output)             # sandbox A/B
        elif output.task_name == 'hypothesis_generation':
            await notify_client(output)                    # información
        await self._track_outcome(output)                  # §6 ROI
```

---

## 6. ROI TRACKING (gap 4) — cada task se gana su lugar

```
   PROBLEMA: una task puede correr 1000 veces, gastar $$ y no mejorar
   nada — y nadie lo sabría. SOLUCIÓN: cada task tiene un outcome_metric
   y un VALOR medible. Si valor ≤ costo → disable (Brian dashboard).
```

| Task | Costo | Outcome metric | Valor medible (ROI) |
|------|-------|----------------|---------------------|
| embedding_precompute | $0 | embeddings_created | query latency ↓ (siempre positivo, $0) |
| cache_prewarming | $0.15 | patterns_warmed | cache hit rate ↑ → LLM cost saved |
| memory_consolidation | $0.10 | facts_extracted | KG retrieval quality (eval) |
| routing_learning | $0.05 | samples_learned | routing accuracy ↑ |
| eval_regression | $0.05 | regression_detected | bugs caught antes que cliente (invaluable) |
| pattern_detection | $0.05 | patterns→skills útiles | skills generadas que se usan |
| hypothesis_generation | $0.50 | hipótesis confirmadas | bugs predichos correctos / total |
| prompt_improvement | $0.20 | prompts mejorados aplicados | eval score delta (A/B) |

```python
class DMNTaskROITracker:
    async def compute_roi(self, ws_id, task_name, window='30d') -> TaskROI:
        cost = await cost_tracker.get_dmn_task_cost(ws_id, task_name, window)
        value = await self._compute_value(ws_id, task_name, window)  # per task
        return TaskROI(task=task_name, cost=cost, value=value,
                       ratio=value/cost if cost > 0 else float('inf'),
                       recommendation='disable' if value < cost else 'keep')
# Dashboard Brian (R8 8.2.2): ROI per task. Auto-suggest disable si ratio < 1.
# Audit: dmn_task_roi_computed + dmn_task_auto_disable_suggested.
```

**Métricas Prometheus nuevas:** `dmn_task_roi_ratio` (task, workspace) · `dmn_task_value_usd` · `dmn_output_approval_rate` (task) · `dmn_generative_outputs_total` (task, approved/rejected).

---

## 7. INTERACTION GRAPH (gap 5) — contratos entre tasks

```
   DEPENDENCIAS (quién alimenta a quién):

   embedding_precompute ──→ pattern_detection (necesita embeddings)
                       └──→ memory_consolidation (facts necesitan emb)

   pattern_detection ──→ hypothesis_generation (patrones informan hipótesis)
                    └──→ skill generation Pilar 3 (6.1.4 Fase 1)

   eval_regression ──→ prompt_improvement (eval bajo dispara mejora)
                  └──→ GUARDIÁN de memory_consolidation (detecta si degradó KG)

   routing_learning ──→ fast path (5.2.3) [no a otra task, a producción]

   ORDEN DE EJECUCIÓN (cuando varias corren en un run):
   1. embedding_precompute (otras dependen de embeddings frescos)
   2. memory_consolidation (KG actualizado)
   3. eval_regression (mide estado tras consolidación)
   4. routing_learning + cache_prewarming (mantenimiento)
   5. pattern_detection (con embeddings frescos)
   6. hypothesis_generation (con patrones)
   7. prompt_improvement (con eval results)
   → el priority del 5.4.2 catálogo se ajusta a este orden de dependencia.

   CONTRADICCIONES (gap real): si pattern_detection sugiere skill X y
   eval_regression dice que algo degradó → governor detecta (R6 §A freno 4
   contradiction) antes de promover. Reusa la misma maquinaria.
```

---

## 8. v2-v3 expansion path (diferido, registrado)

- Tasks adicionales identificadas en producción (más housekeeping/generativas)
- Workspace custom tasks DSL (defer E — cliente define sus propias DMN tasks)
- LLM-driven task selection (defer D — LLM decide qué tasks correr, no catálogo fijo)
- Meta-Orchestrator full (ya parcialmente materializado en R6 §A — DMN reusa)

---

## 9. Resumen del refinamiento

| Gap | Resuelto |
|-----|----------|
| 1. Tasks stubs | ✅ 8 trigger_fn + action_fn detallados (§3 housekeeping, §4 generativas) |
| 2. Triggers vagos | ✅ cada trigger con threshold DEFENDIBLE + razonamiento |
| 3. Auto-improvement loop | ✅ end-to-end (§5) REUSA governor + review queue R6 §A (no duplica) |
| 4. ROI no medible | ✅ outcome_metric + value per task + auto-disable suggest (§6) |
| 5. Interacciones | ✅ interaction graph + orden ejecución + contradicción via governor (§7) |

**Decisión LOCKED:** 2 clases (housekeeping seguro auto-apply / generativo gobernado). Auto-improvement loop de DMN generativo = misma maquinaria que skills Pilar 3 (Meta-Orchestrator R6 §A). v1 MUY CONSERVADOR (generativas siempre review). ROI medible per task → disable lo que no aporta.

**Pendiente al programar:** implementar los 8 action_fn + trigger_fn (§3/§4) + DMNAutoImprovementLoop (§5) + ROITracker (§6) + enchufar al governor (R6). Calibrar thresholds de triggers con datos reales (mismo protocolo R6 §B).

**Sinergia clave confirmada:** DMN (Nodo 6, genera mientras idle) + Skills (Nodo 4, captura/reutiliza) = las dos mitades de Pilar 3 autonomía generativa, AMBAS gobernadas por el mismo Meta-Orchestrator. Esto era lo que faltaba conectar.