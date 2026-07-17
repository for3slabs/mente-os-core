# Ronda 6 — Bloque 4 — Memory Eval & Regression

**Sub-doc detallado del Bloque 4 de R6. ⭐ CIERRA R6 100%.**

**Owner:** Brian López
**Fecha:** 2026-06-07
**Status:** ✅ **1/1 sub-temas LOCKED**
**Master doc:** [Ronda_06_Memory_Stack_Extensions.md](Ronda_06_Memory_Stack_Extensions.md)
**Materializa:** Memory health monitoring + foundation Pilar 3 capacidad generativa

⚠️ **Flag global:** TODO R6 requires re-review pre-código (`project_r6_critical_pre_code_review.md`).

---

## 1. Propósito

Memory regression detection es el "doctor del sistema". Detecta cuando memoria degrada (forgetting agresivo, consolidation errónea, embeddings stale, skill drift, KG orphans, temporal query degradation, cross-workspace leak silent, DMN outputs inútiles).

Sin esto, issues silent → cliente abandona.

---

## 2. Sub-tema 6.4.1 — Memory Regression Detection

### Decisión LOCKED: C — Multi-layer (4 layers + alerts + auto-actions)

### Daily health scan

```python
class MemoryRegressionDetector:
    LAYER_WEIGHTS = {'l1': 0.40, 'l2': 0.30, 'l3': 0.20, 'l4': 0.10}
    REGRESSION_THRESHOLDS = {
        'golden_f1_drop': 0.10,
        'trend_change_significant': 0.20,
        'trend_change_high': 0.40,
        'overall_score_critical': 60,
        'overall_score_warning': 70,
    }
    
    async def daily_health_scan(self, workspace_id) -> MemoryHealthReport:
        """Cron daily 4 AM (post-microglía 3 AM)."""
        report = MemoryHealthReport(workspace_id=workspace_id)
        
        report.layer1 = await self._run_golden_retrieval_tests(workspace_id)
        report.layer2 = await self._run_canary_queries(workspace_id)
        report.layer3 = await self._analyze_trends(workspace_id)
        report.layer4 = await self._evaluate_dmn_outputs(workspace_id)
        
        report.overall_score = self._aggregate_health_score(
            report.layer1, report.layer2, report.layer3, report.layer4,
        )
        
        await self._trigger_alerts_if_degraded(report)
        await memory_health_store.persist(report)
        
        await audit_logger.log(
            event_type='memory_health_scan_completed',
            payload={
                'workspace_id': workspace_id,
                'overall_score': report.overall_score,
                'layer1_f1': report.layer1.avg_f1,
                'layer2_critical_failures': len(report.layer2.critical_failures),
                'layer3_degraded': report.layer3.degraded_metrics_count,
                'layer4_efficacy': report.layer4.overall_efficacy_score,
            }
        )
        
        return report
```

### LAYER 1 — Golden Retrieval Tests (40% weight)

```python
async def _run_golden_retrieval_tests(self, workspace_id) -> Layer1Results:
    golden_set = await golden_datasets_store.get_for_workspace(
        workspace_id, dataset_type='memory_retrieval',
    )
    
    if not golden_set:
        # Auto-bootstrap from successful past queries
        golden_set = await self._auto_generate_golden_set(workspace_id)
    
    results = []
    for golden_query in golden_set:
        # Run via 6.3.1 temporal query engine
        actual = await hippocampus_time_query_engine.query(
            workspace_id,
            TemporalQuery(
                semantic_query=golden_query.query_text,
                semantic_top_k=20,
            ),
        )
        retrieved_ids = {e.id for e in actual.episodes}
        expected_ids = set(golden_query.expected_episode_ids)
        
        recall = len(retrieved_ids & expected_ids) / len(expected_ids)
        precision = len(retrieved_ids & expected_ids) / len(retrieved_ids)
        f1 = 2 * recall * precision / (recall + precision)
        
        results.append(GoldenRetrievalResult(
            query=golden_query.query_text,
            recall=recall, precision=precision, f1=f1,
        ))
    
    baseline = await self._get_baseline_layer1(workspace_id)
    regression_detected = (
        np.mean([r.f1 for r in results]) < baseline.avg_f1 * 0.9
    )
    
    return Layer1Results(
        tests_run=len(results),
        avg_f1=np.mean([r.f1 for r in results]),
        regression_detected=regression_detected,
        individual_results=results,
        pass_rate=len([r for r in results if r.f1 > 0.7]) / len(results),
    )
```

### LAYER 2 — Canary Queries (30% weight)

```python
CANARIES_V1 = [
    CanaryQuery(
        name='workspace_boundary',
        severity='CRITICAL',
        # Cross-workspace leak detection
    ),
    CanaryQuery(
        name='kg_facts_have_source',
        severity='HIGH',
        # No orphaned KG facts
    ),
    CanaryQuery(
        name='recent_episodes_accessible',
        severity='HIGH',
        # Episodes <7 days accessible
    ),
    CanaryQuery(
        name='skills_queryable',
        severity='MEDIUM',
        # Active skills semantic search
    ),
    CanaryQuery(
        name='embeddings_dimensions',
        severity='CRITICAL',
        # No Stella version mismatch
    ),
    CanaryQuery(
        name='audit_log_integrity',
        severity='CRITICAL',
        # Audit writable + readable
    ),
    CanaryQuery(
        name='forgetting_policy_honored',
        severity='HIGH',
        # No episodes past purge_days still active
    ),
]


async def _run_canary_queries(self, workspace_id) -> Layer2Results:
    results = []
    for canary in CANARIES_V1:
        try:
            passed = await self._execute_canary(canary, workspace_id)
            results.append(CanaryResult(canary=canary, passed=passed))
        except Exception as e:
            results.append(CanaryResult(canary=canary, passed=False, error=str(e)))
    
    failed = [r for r in results if not r.passed]
    critical_failures = [r for r in failed if r.canary.severity == 'CRITICAL']
    
    return Layer2Results(
        canaries_run=len(CANARIES_V1),
        failed_count=len(failed),
        critical_failures=critical_failures,
        individual_results=results,
    )
```

### LAYER 3 — Trend Analysis (20% weight)

```python
METRICS_TRACKED = [
    'episodes_created_count',
    'episodes_archived_count',
    'episodes_purged_count',
    'kg_facts_count',
    'kg_facts_promoted_via_cls',
    'skills_active_count',
    'skills_avg_score',
    'memory_search_avg_similarity_top1',
    'memory_search_avg_latency_ms',
    'temporal_query_avg_latency_ms',
    'gdpr_requests_count',
    'storage_mb_total',
]


async def _analyze_trends(self, workspace_id) -> Layer3Results:
    degraded = []
    improved = []
    stable = []
    
    for metric in METRICS_TRACKED:
        # 7d avg vs 30d baseline
        last_7d = await self._get_metric_avg(workspace_id, metric, days=7)
        baseline_30d = await self._get_metric_avg(workspace_id, metric, days=30, exclude_recent=7)
        
        if baseline_30d > 0:
            change_pct = (last_7d - baseline_30d) / baseline_30d
            
            # Direction-aware (higher vs lower better)
            if metric in HIGHER_IS_BETTER:
                if change_pct < -0.20:
                    degraded.append(MetricTrend(
                        metric=metric, current=last_7d, baseline=baseline_30d,
                        change_pct=change_pct,
                        severity='HIGH' if change_pct < -0.40 else 'MEDIUM',
                    ))
                elif change_pct > 0.20:
                    improved.append(MetricTrend(...))
            elif metric in LOWER_IS_BETTER:
                if change_pct > 0.30:
                    degraded.append(MetricTrend(...))
            
            if abs(change_pct) < 0.10:
                stable.append(metric)
    
    return Layer3Results(
        metrics_tracked=len(METRICS_TRACKED),
        degraded_metrics_count=len(degraded),
        improved_metrics_count=len(improved),
        stable_metrics_count=len(stable),
        degraded_metrics=degraded,
        improved_metrics=improved,
    )
```

### LAYER 4 — DMN Efficacy (10% weight)

```python
async def _evaluate_dmn_outputs(self, workspace_id) -> Layer4Results:
    dmn_outputs = await dmn_outputs_store.get_recent(workspace_id, days=30)
    
    usage_stats = defaultdict(lambda: {'total': 0, 'applied': 0, 'rejected': 0, 'pending': 0})
    
    for output in dmn_outputs:
        usage_stats[output.task_name]['total'] += 1
        if output.status == 'applied':
            usage_stats[output.task_name]['applied'] += 1
        elif output.status == 'rejected':
            usage_stats[output.task_name]['rejected'] += 1
        else:
            usage_stats[output.task_name]['pending'] += 1
    
    tasks_efficacy = {}
    for task_name, stats in usage_stats.items():
        applied_rate = stats['applied'] / stats['total']
        tasks_efficacy[task_name] = TaskEfficacy(
            task_name=task_name,
            total_outputs=stats['total'],
            applied=stats['applied'],
            applied_rate=applied_rate,
            efficacy='HIGH' if applied_rate > 0.7 else (
                'LOW' if applied_rate < 0.2 else 'MEDIUM'
            ),
        )
    
    # Tasks consistently low efficacy → propose disable
    low_efficacy = [t for t in tasks_efficacy.values()
                    if t.efficacy == 'LOW' and t.total_outputs >= 10]
    if low_efficacy:
        await self._propose_dmn_task_disable(workspace_id, low_efficacy)
    
    overall = np.mean([t.applied_rate for t in tasks_efficacy.values()])
    
    return Layer4Results(
        tasks_evaluated=len(tasks_efficacy),
        overall_efficacy_score=overall,
        low_efficacy_tasks=low_efficacy,
        individual_tasks=list(tasks_efficacy.values()),
    )
```

### Aggregate health score

```python
def _aggregate_health_score(self, l1, l2, l3, l4) -> float:
    l1_score = l1.pass_rate * 100
    
    l2_penalty = (
        len(l2.critical_failures) * 30 +
        (l2.failed_count - len(l2.critical_failures)) * 10
    )
    l2_score = max(0, 100 - l2_penalty)
    
    l3_degraded_ratio = l3.degraded_metrics_count / max(l3.metrics_tracked, 1)
    l3_score = (1 - l3_degraded_ratio) * 100
    
    l4_score = l4.overall_efficacy_score * 100
    
    return (
        l1_score * 0.40 +
        l2_score * 0.30 +
        l3_score * 0.20 +
        l4_score * 0.10
    )
```

### Alert tiers

```python
async def _trigger_alerts_if_degraded(self, report):
    # CRITICAL canary → Brian inmediato
    if report.layer2.critical_failures:
        for failure in report.layer2.critical_failures:
            await audit_logger.log(
                event_type='memory_regression_CRITICAL_canary_failed',
                payload={
                    'workspace_id': report.workspace_id,
                    'canary_name': failure.canary.name,
                    'severity': 'CRITICAL',
                }
            )
            await notification_service.send_to_brian(
                template='memory_critical_canary_failed', ...,
            )
    
    # Score critical
    if report.overall_score < 60:
        await notification_service.send_to_brian(
            template='memory_health_degraded',
            payload={...},
        )
    
    # Score warning → cliente
    if report.overall_score < 70:
        await notification_service.send(
            workspace=workspace,
            template='memory_health_warning',
            payload={'recommended_actions': self._recommend_actions(report)},
        )
```

### Auto-actions

- Low efficacy DMN task → propose disable cliente
- memory_search_similarity degrade trend → propose Stella re-embedding
- Cross-workspace canary fail → SECURITY emergency alert

### Dashboard integration

```
/dashboard/memory/health
- Overall score over time chart
- Layer breakdown (L1/L2/L3/L4)
- Recent canary failures
- Trend metrics
- DMN efficacy
- Recommended actions
```

### Audit events
- `memory_health_scan_completed`
- `memory_regression_CRITICAL_canary_failed`
- `memory_health_degraded`
- `memory_health_warning`
- `dmn_task_disable_proposed`
- `stella_re_embedding_proposed`

### Foundation
- R8 Observability (extended metrics)
- R9 Security (canary 1, 5, 6 hooks)
- R10 CI/CD (golden tests in pipeline)

---

## 3. Eventos audit Bloque 4

Total events nuevos R6 B4: **~6 events**

- `memory_health_scan_completed`
- `memory_regression_CRITICAL_canary_failed`
- `memory_health_degraded`
- `memory_health_warning`
- `dmn_task_disable_proposed`
- `stella_re_embedding_proposed`

---

**Bloque 4 ✅ CERRADO — Memory health monitoring verdadero v1 ⚠️ flag pre-código aplica.**
**🏆 R6 100% CERRADO ⭐⭐⭐**