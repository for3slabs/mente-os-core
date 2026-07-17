# Ronda 5 — Bloque 1 — Tálamo & Routing

**Sub-doc detallado del Bloque 1 de R5.**

**Owner:** Brian López
**Fecha:** 2026-06-06
**Status:** ✅ **4/4 sub-temas LOCKED**
**Master doc:** [Ronda_05_Orchestration_Multi_Agent.md](Ronda_05_Orchestration_Multi_Agent.md)
**Materializa:** Grafo Maestro Nodo 8 (Tálamo) + Nodo 11 (Neuromoduladores)

---

## Tabla de contenidos

1. [Propósito del Bloque 1](#1-propósito)
2. [Sub-tema 5.1.1 — Tool Selection Strategy](#2-sub-tema-511)
3. [Sub-tema 5.1.2 — Context Routing](#3-sub-tema-512)
4. [Sub-tema 5.1.3 — Subgraph Activation](#4-sub-tema-513)
5. [Sub-tema 5.1.4 — Neuromoduladores](#5-sub-tema-514)
6. [Integraciones con bloques posteriores](#6-integraciones)
7. [Eventos audit Bloque 1](#7-eventos-audit)

---

## 1. Propósito

El Tálamo es el router cerebral. Decide:
- ¿Qué tools activar para esta query? (5.1.1)
- ¿Qué memoria/contexto cargar? (5.1.2)
- ¿Qué subsistemas del grafo activar? (5.1.3)
- ¿Qué modo global del sistema? (5.1.4 Neuromoduladores)

Sin Bloque 1, For3s OS carga todo siempre — costo y latencia inaceptables.

---

## 2. Sub-tema 5.1.1 — Tool Selection Strategy

### Decisión LOCKED: B+C Híbrido

**B = Workspace whitelist estático (R4 4.1.2 reused)**
**C = Semantic ranking runtime (Stella + cosine similarity)**

### Pipeline

```
Query → workspace.allowed_tools (R4 whitelist)
      → workspace.always_include (boost siempre)
      → para cada tool restante: cosine(query_emb, tool_emb)
      → top-K (default 10, configurable)
      → tools al prompt
```

### Stack

```python
class ThalamicToolRouter:
    DEFAULT_TOP_K = 10

    async def select_tools(self, workspace_id: str, query: str) -> list[Tool]:
        workspace = await get_workspace(workspace_id)
        allowed = workspace.allowed_tools
        always = workspace.always_include_tools or []

        query_embedding = await stella.embed(query)

        ranked = []
        for tool_name in allowed:
            if tool_name in always:
                ranked.append((tool_name, 1.0))
                continue
            tool = await tool_registry.get(tool_name)
            similarity = cosine_similarity(query_embedding, tool.embedding)
            ranked.append((tool_name, similarity))

        ranked.sort(key=lambda x: -x[1])
        top_k = workspace.tool_selection_k or self.DEFAULT_TOP_K
        selected = ranked[:top_k]

        await audit_logger.log(
            event_type='thalamus_tool_selection',
            payload={
                'workspace_id': workspace_id,
                'query_preview': query[:100],
                'total_allowed': len(allowed),
                'selected_count': len(selected),
                'top_score': selected[0][1] if selected else None,
            }
        )

        return [tool_registry.get(name) for name, _ in selected]
```

### Stack reused

- Stella embeddings (R2 B2 lockeado, gratis local)
- pgvector (R2 B2 indexed)
- R4 4.1.2 workspace.allowed_tools
- R3 B2 3.2.2 budget tool slot (≤1,500 tok)

### Ahorro

- Workspace con 57 tools → top-10 al prompt = 500 tok vs 2,850 tok
- ~82% reducción tokens tool definitions
- Costo per query proporcional menor

---

## 3. Sub-tema 5.1.2 — Context Routing

### Decisión LOCKED: C+D Híbrido

**C = Budget enforcement R3 B2 3.2.2 (cuánto tokens cada tier)**
**D = Semantic selection per tier (CUÁL contenido cargar)**

### Pipeline

```
Query → embedding + NER ligero (entities)
      → working_memory: SIEMPRE (3000 tok)
      → episodes: semantic search Hipocampo (top-20 + recency boost)
      → kg_facts: Cypher AGE entities-related (cap 2000 tok)
      → embeddings: pgvector top-K (cap 2000 tok)
      → SKIP_THRESHOLD 0.3 (omite tier si max similarity insuficiente)
      → always_include override per workspace
      → ensamblar prompt
```

### Stack

```python
class ThalamicContextRouter:
    SKIP_THRESHOLD = 0.3

    async def route_context(
        self, workspace_id: str, query: str, budget: PromptBudget
    ) -> PromptContext:
        query_embedding = await stella.embed(query)
        entities = await ner_light.extract(query)

        working = await memory.get_working(workspace_id, max_tokens=budget.working_memory)

        episodes_raw = await hippocampus.search_semantic(
            workspace_id=workspace_id,
            query_embedding=query_embedding,
            recency_boost=2.0,
            limit=20,
        )
        episodes = self._truncate_to_budget(episodes_raw, budget.episodes)
        episodes_score = max([e.similarity for e in episodes_raw], default=0)

        kg_facts = []
        if entities:
            kg_facts = await knowledge_graph.query_related(
                workspace_id=workspace_id,
                entities=entities,
                max_tokens=budget.kg_facts,
            )

        embeds_raw = await vector_memory.search(
            workspace_id=workspace_id,
            query_embedding=query_embedding,
            limit=10,
        )
        embeds = self._truncate_to_budget(embeds_raw, budget.embeddings)
        embeds_score = max([e.similarity for e in embeds_raw], default=0)

        # SKIP threshold
        if episodes_score < self.SKIP_THRESHOLD:
            episodes = []
        if embeds_score < self.SKIP_THRESHOLD:
            embeds = []

        # Workspace override
        workspace = await get_workspace(workspace_id)
        if 'episodes' in (workspace.always_include_tiers or []):
            episodes = episodes_raw[:5]

        await audit_logger.log(
            event_type='thalamus_context_routing',
            payload={
                'workspace_id': workspace_id,
                'query_preview': query[:100],
                'tiers_activated': {
                    'working_memory': bool(working),
                    'episodes': bool(episodes),
                    'kg_facts': bool(kg_facts),
                    'embeddings': bool(embeds),
                },
            }
        )

        return PromptContext(
            working_memory=working,
            episodes=episodes,
            kg_facts=kg_facts,
            embeddings=embeds,
        )
```

### Ahorro

- 50-70% tokens vs cargar todo
- Skip tier irrelevante (no waste 2000 tok)

---

## 4. Sub-tema 5.1.3 — Subgraph Activation

### Decisión LOCKED: C — 3 modos Grafo Maestro

```
MÍNIMO (default 80% queries)
  workspace_gate, thalamus, pfc, hippocampus (working_only)
  multi_agent: False, dmn: False, dual_process: False

COMPLETO (15% queries complejas)
  todo MÍNIMO +
  hippocampus full, kg, multi_agent: on_demand,
  dual_process: True, neuromods: adaptive

EMERGENCIA (5% security/compliance)
  workspace_gate, thalamus, amygdala (R9),
  pfc: fast_only, audit: verbose, neuromods: high_attention
```

### Classifier v1 (heurístico)

```python
async def classify_mode(self, query: str, signals: dict) -> SubgraphMode:
    if signals.get('security_alert') or signals.get('compliance_violation'):
        return SubgraphMode.EMERGENCY
    if signals.get('rate_limit_exceeded') or signals.get('critical_error'):
        return SubgraphMode.EMERGENCY

    complexity_signals = [
        len(query) > 200,
        'analyze' in query.lower() or 'review' in query.lower(),
        'refactor' in query.lower() or 'debug' in query.lower(),
        signals.get('multi_step_intent', False),
        signals.get('tools_needed', 0) > 3,
    ]
    if sum(complexity_signals) >= 2:
        return SubgraphMode.COMPLETE

    return SubgraphMode.MINIMUM
```

### Workspace override

`workspace.force_complete_mode: bool` permite forzar COMPLETO siempre.

### Foundation

- Dual-Process B2 lee `subgraph_mode` como signal contextual
- Neuromod 5.1.4 lee `subgraph_mode == 'emergency'` → HIGH_ATTENTION
- Amígdala R9 hook para EMERGENCY routing

---

## 5. Sub-tema 5.1.4 — Neuromoduladores (Nodo 11)

### Decisión LOCKED: B — 4 modos fijos Grafo Maestro

```
EXPLORATION (default business hours)
  pfc: sonnet temp 0.7, hippocampus top_k 10, kg wide
  multi_agent spawn_threshold low, dmn: disabled

CONSOLIDATION (idle >5min o cron nocturno)
  pfc: opus temp 0.3, hippocampus top_k 20
  cls: aggressive, dmn: enabled aggressive
  cache TTL ×2

HIGH_ATTENTION (emergency subgraph)
  pfc: opus temp 0.2, hippocampus top_k 3 (recency 3x)
  kg: narrow, multi_agent spawn_threshold 3
  dual_process: force_system_2, audit: verbose
  retry_policy ×1.5

REST (idle >30min o cost cap P5 >80%)
  pfc: haiku, multi_agent: prohibido
  dmn: disabled, cache TTL ×3
  audit: minimal
```

### Transitions event-driven

```python
async def determine_mode(self, workspace_id: str, signals: dict) -> NeuromodMode:
    if signals.get('subgraph_mode') == 'emergency':
        return NeuromodMode.HIGH_ATTENTION

    if signals.get('is_nightly_cron'):
        return NeuromodMode.CONSOLIDATION

    idle_seconds = signals.get('idle_seconds', 0)
    if idle_seconds > self.IDLE_REST_THRESHOLD:
        return NeuromodMode.REST

    cost_ratio = signals.get('p5_cost_ratio', 0)
    if cost_ratio > self.COST_REST_THRESHOLD:
        return NeuromodMode.REST

    if idle_seconds > self.IDLE_CONSOLIDATION_THRESHOLD:
        return NeuromodMode.CONSOLIDATION

    return NeuromodMode.EXPLORATION
```

### Audit transitions

```python
if previous != mode:
    await audit_logger.log(
        event_type='neuromod_transition',
        payload={
            'workspace_id': workspace_id,
            'previous_mode': previous.value if previous else None,
            'new_mode': mode.value,
            'trigger_signals': signals,
        }
    )
```

### Foundation

- DMN B4: CONSOLIDATION mode activa DMN (signal scheduler)
- Dual-Process B2: HIGH_ATTENTION → boost tier 5.2.2
- Cost control B3: REST mode → multi_agent prohibido

---

## 6. Integraciones con bloques posteriores

| Bloque | Integración con B1 |
|---|---|
| **B2 Dual-Process** | Lee `subgraph_mode` + `neuromod_mode` como signals weight 1.5 (5.2.1) y 6 factores routing (5.2.2) |
| **B3 Multi-Agent** | Lee `neuromod.multi_agent_spawn_threshold` para decidir cuándo spawn. HIGH_ATTENTION boost specialists |
| **B4 DMN** | Lee `neuromod.dmn_enabled` config + CONSOLIDATION trigger DMN scheduler |

---

## 7. Eventos audit Bloque 1

- `thalamus_tool_selection` (5.1.1)
- `thalamus_context_routing` (5.1.2)
- `thalamus_subgraph_activation` (5.1.3)
- `neuromod_transition` (5.1.4)

Todos workspace-scoped, payload preview ≤100 chars query.

---

**Bloque 1 ✅ CERRADO — Foundation Tálamo + Neuromoduladores lista para Bloque 2.**