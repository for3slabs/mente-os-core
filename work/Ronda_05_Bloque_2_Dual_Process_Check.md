# Ronda 5 — Bloque 2 — Dual-Process Check

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** desde v1 (2026-07-30, ADR-029)

**Sub-doc detallado del Bloque 2 de R5.**

**Owner:** Brian López
**Fecha:** 2026-06-06
**Estado original:** ✅ **3/3 sub-temas LOCKED**
**Master doc:** [Ronda_05_Orchestration_Multi_Agent.md](work/Ronda_05_Orchestration_Multi_Agent.md)
**Materializa:** Grafo Maestro Nodo 9 (Sistema 1 vs Sistema 2 Kahneman)

---

## Tabla de contenidos

1. [Propósito del Bloque 2](#1-propósito)
2. [Sub-tema 5.2.1 — Sistema 1 vs Sistema 2 detection](#2-sub-tema-521)
3. [Sub-tema 5.2.2 — LLM Tier Routing HISTORY-AWARE](#3-sub-tema-522)
4. [Sub-tema 5.2.3 — Fast Path Optimization](#4-sub-tema-523)
5. [Eventos audit Bloque 2](#5-eventos-audit)

---

## 1. Propósito

Daniel Kahneman ganó el Nobel describiendo que el cerebro tiene 2 sistemas:
- **Sistema 1:** rápido, automático, heurístico (95% decisiones)
- **Sistema 2:** lento, deliberado, analítico (5% decisiones críticas)

For3s OS replica esto:
- **S1 → Haiku** ($0.25/MTok input)
- **S1.5/S2 ligero → Sonnet** ($3/MTok input)
- **S2 profundo → Opus** ($15/MTok input)

Bloque 2 decide:
- ¿Esta query es S1 o S2? (5.2.1)
- ¿Qué tier específico (Haiku/Sonnet/Opus)? (5.2.2)
- ¿Puedo skip LLM entirely vía cache? (5.2.3)

Sin Bloque 2, todo va a Opus (cost runaway) o todo a Haiku (calidad pobre).

---

## 2. Sub-tema 5.2.1 — Sistema 1 vs Sistema 2 detection

### Decisión LOCKED: C — Multi-señal heurístico

### Signals + pesos

```
QUERY SIGNALS (peso 1.0):
  - len(query) > 200
  - keywords S2: analyze, refactor, debug, compare, design, evaluate
  - query.count('?') > 2
  - query.count('\\n') > 5 (multi-paragraph)

CONTEXT SIGNALS (peso 1.5):
  - subgraph_mode == COMPLETE
  - subgraph_mode == EMERGENCY
  - neuromod_mode == HIGH_ATTENTION
  - neuromod_mode == CONSOLIDATION
  - estimated_tool_calls > 3
  - context_tokens > 5000
  - kg_facts_count > 5

HISTORY SIGNALS (peso 2.0):
  - workspace_avg_complexity > 0.6
  - similar_query_required_s2

WORKSPACE OVERRIDE (peso 3.0):
  - workspace.force_system_2
  - workspace.tier == 'enterprise'
```

### Threshold

Default 3.0, tunable per workspace (`workspace.s2_threshold`).

### Stack

```python
class DualProcessChecker:
    DEFAULT_THRESHOLD = 3.0
    QUERY_KEYWORDS_S2 = {
        'analyze', 'analizar', 'refactor', 'debug',
        'compare', 'comparar', 'design', 'architect',
        'plan', 'evaluate', 'evaluar', 'review profundo',
    }

    async def detect_system(
        self, query: str, signals: ContextSignals,
    ) -> CognitiveSystem:
        query_score = sum([
            len(query) > 200,
            any(kw in query.lower() for kw in self.QUERY_KEYWORDS_S2),
            query.count('?') > 2,
            query.count('\\n') > 5,
        ]) * 1.0

        context_score = sum([
            signals.subgraph_mode == SubgraphMode.COMPLETE,
            signals.subgraph_mode == SubgraphMode.EMERGENCY,
            signals.neuromod_mode == NeuromodMode.HIGH_ATTENTION,
            signals.neuromod_mode == NeuromodMode.CONSOLIDATION,
            signals.estimated_tool_calls > 3,
            signals.context_tokens > 5000,
            signals.kg_facts_count > 5,
        ]) * 1.5

        history_score = sum([
            signals.workspace_avg_complexity > 0.6,
            signals.similar_query_required_s2,
        ]) * 2.0

        workspace_score = sum([
            signals.workspace.force_system_2,
            signals.workspace.tier == 'enterprise',
        ]) * 3.0

        total = query_score + context_score + history_score + workspace_score
        threshold = signals.workspace.s2_threshold or self.DEFAULT_THRESHOLD
        decision = CognitiveSystem.SYSTEM_2 if total >= threshold else CognitiveSystem.SYSTEM_1

        await audit_logger.log(
            event_type='dual_process_decision',
            payload={
                'workspace_id': signals.workspace.id,
                'scores': {
                    'query': query_score, 'context': context_score,
                    'history': history_score, 'workspace': workspace_score,
                    'total': total,
                },
                'threshold': threshold,
                'decision': decision.name,
            }
        )
        return decision
```

### Foundation

- Reusa signals R5 B1 (subgraph + neuromod)
- Logs estructurados → datos para ML clasificador v3+

---

## 3. Sub-tema 5.2.2 — LLM Tier Routing HISTORY-AWARE ⭐

### Decisión LOCKED: C + History-Aware (input Brian)

**6 factores routing:**

1. **BASE por score (5.2.1)**
2. **NEUROMOD adjustment (5.1.4)**
3. **COST CAP P5 protection**
4. **WORKSPACE TIER (enterprise vs pilot)**
5. **CACHE PRE-CHECK (handoff 5.2.3)**
6. **⭐ HISTORY-AWARE PRECISION (input Brian)**:
   - 6a. Similar queries (pgvector audit log)
   - 6b. KG patterns (Cypher AGE + CLS)
   - 6c. Session deep flow (Hipocampo episodes)

### Por qué HISTORY-AWARE cambia todo

Brian input verbatim:
> "TAMBIEN LO PODEMOS A HACER A TRAVEZ DEL ENTRENAMIENTO SI HAY PERSONAS QUE YA PASARON POR LA MISMA SITUACION PODEMOS MEJOR EN PRECICION. O DE ANTECEDENTES QUE TIENE, QUE TENEMOS EN LA MEMORIA"

Esto activa **capacidad generativa Nodo 9** (Grafo Maestro: "aprende qué tipos de query siempre necesitan profundidad") **desde v1**, no v3.

### Pipeline factor 6

```python
async def _gather_history_signals(self, query, signals):
    # 6a. pgvector similarity search en routing audit log
    query_emb = await stella.embed(query)
    similar = await self._search_similar_routing_history(
        workspace_id=signals.workspace.id,
        query_embedding=query_emb,
        lookback_days=90,
    )

    # 6b. KG Cypher pattern match (consolidated via CLS)
    features = await self._extract_query_features(query, signals)
    kg_pattern = await knowledge_graph.match_routing_pattern(
        workspace_id=signals.workspace.id,
        features=features,
    )

    # 6c. Hipocampo episodes recent session
    if signals.session_id:
        recent = await hippocampus.search(
            workspace_id=signals.workspace.id,
            user_id=signals.user_id,
            session_id=signals.session_id,
            max_age_hours=2, limit=10,
        )
        session_tiers = [ep.metadata.get('llm_tier_used') for ep in recent]
        in_deep_flow = len([t for t in session_tiers if t in ['sonnet','opus']]) >= 2
    else:
        session_tiers, in_deep_flow = [], False

    return HistoryAwareSignals(
        similar_queries_tier_distribution=self._count_tiers(similar),
        similar_queries_avg_eval_score=self._avg_eval_by_tier(similar),
        similar_queries_total=len(similar),
        kg_pattern_match=kg_pattern,
        session_episodes_recent_tiers=session_tiers,
        session_in_deep_flow=in_deep_flow,
    )
```

### Decision matrix

```
Si similar_queries_total >= 5:
    Si tier X usado en >70% similares con eval > 0.8:
        recommend X (evidence_strength > 0.7 → aplicar)

Si kg_pattern_match.confidence > 0.7:
    current = pattern.recommended_tier

Si session_in_deep_flow:
    recent_max = max(session_tiers)
    if recent_max > current: current = recent_max (continuidad)
```

### Cold start protection

- <5 similar queries → skip factor 6a
- Sin KG patterns → skip factor 6b
- Sin session episodes → skip factor 6c
- Fallback: factors 1-5 funcionan solos

### Overhead

~35ms per query (sin LLM extra):
- pgvector query: ~10ms (workspace-indexed)
- KG Cypher: ~15ms (workspace-indexed)
- Hipocampo recall: ~10ms (cache hot)

### Stack reused

- R2 B2 Stella embeddings + pgvector
- R2 KG (Apache AGE) + CLS (R2 4.4) consolidation
- R2 Hipocampo episodes
- R3 4.4 eval framework (eval_score per decision)
- R3 audit log (llm_tier_routing audit)

---

## 4. Sub-tema 5.2.3 — Fast Path Optimization

### Decisión LOCKED: C — 3 layers fast path

```
QUERY LLEGA
   ↓
LAYER 1: CACHE EXACT (Valkey R2 B3)
   ↓ hit → return (5ms)
   ↓ miss
LAYER 2: CACHE SEMÁNTICO (Stella + pgvector)
   ↓ similarity > 0.92 → return (~30ms)
   ↓ miss
LAYER 3: HEURÍSTICAS LOCALES (Python handlers)
   ↓ match → return (~10ms)
   ↓ no match
FALLBACK: ROUTING NORMAL (5.2.1 + 5.2.2)
   ↓ LLM call

POST-RESPONSE:
   ↓ cachear response (exact + semantic)
   ↓ TTL workspace-configurable
```

### Layer 1: Cache exact

```python
cache_key = hash(workspace_id + query_normalized + context_hash)
cached = await valkey.get(cache_key)
if cached:
    return FastPathResult(hit=True, response=cached, layer='cache_exact')
```

### Layer 2: Cache semántico

```python
query_emb = await stella.embed(query)
similar = await semantic_cache.search(
    workspace_id=workspace_id,
    query_embedding=query_emb,
    threshold=0.92,
    limit=1,
)
if similar:
    return FastPathResult(
        hit=True,
        response=similar[0].response,
        layer='cache_semantic',
    )
```

### Layer 3: Heurísticas locales

Handlers extensibles. Implementados v1:

```python
class WorkspaceInfoHandler(FastPathHandler):
    name = 'workspace_info'
    KEYWORDS = ['workspace id', 'mi workspace', 'workspace?']

    async def matches(self, query, signals):
        return any(kw in query.lower() for kw in self.KEYWORDS)

    async def execute(self, query, signals):
        return f"Tu workspace_id es {signals.workspace.id}"


class ListToolsHandler(FastPathHandler):
    name = 'list_tools'
    KEYWORDS = ['lista tools', 'tools disponibles', 'qué puedo hacer']
    ...


class LastQueryHandler(FastPathHandler):
    name = 'last_query'
    KEYWORDS = ['última query', 'last query']
    ...

FAST_PATH_HANDLERS_V1 = [
    WorkspaceInfoHandler(),
    ListToolsHandler(),
    LastQueryHandler(),
]
```

### Cobertura/cost

- 50-60% queries trivial hit fast path
- Latencia 5-50ms vs 800ms+ LLM
- Cost saving 50-60% real

### Foundation DMN B4

Layer E (pre-computed warm cache) defer a DMN B4 tarea 6 (cache_prewarming). DMN puede pre-generar respuestas top-100 queries últimos 7 días en idle → fast path hits aumentan.

---

## 5. Eventos audit Bloque 2

- `dual_process_decision` (5.2.1)
- `llm_tier_routing` (5.2.2) — incluye `history_signals` payload
- `fast_path_cache_exact_hit` (5.2.3)
- `fast_path_cache_semantic_hit` (5.2.3)
- `fast_path_heuristic_hit` (5.2.3)
- `fast_path_miss` (5.2.3)

---

**Bloque 2 ✅ CERRADO — Dual-Process Check Nodo 9 verdadero con capacidad generativa v1.**

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_05_Bloque_2_Dual_Process_Check.md`).
