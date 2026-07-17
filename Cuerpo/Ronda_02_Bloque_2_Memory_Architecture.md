# Ronda 2 — Bloque 2: Memory Architecture

**Sub-documento detallado de R2 — Data Layer. Bloque 2 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-01
**Estatus:** ✅ LOCKED (7/7 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema)
**Documento padre:** [Ronda_02_Data_Layer.md](Ronda_02_Data_Layer.md)
**Sesión:** 2026-06-01

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (licencias permisivas obligatorias)
- 3.D — Equipo pequeño (0 servicios extra preferido)

**Constraint LOCKED aplicado:**
- P2 — AI+infra <25% pilot revenue
- P3 — Schema-per-tenant
- P4 — Encryption híbrida
- P5 — ES híbrido por aggregate

> ⚠️ **COSTO HARDWARE ACTUALIZADO POR D-009 (2026-06-01)**
>
> Este documento menciona "Hetzner CX42 ~USD 25/mes" en varias secciones (cálculos hechos antes de D-009). El **costo real vigente v1** es:
>
> - **Hardware:** Linux LOCAL Brian (30 GB RAM, 1 TB disco) — USD 0
> - **Electricidad 24/7:** USD ~5/mes
> - **Cloudflare Tunnel:** USD 0 (free tier)
> - **Dominio for3s.ai:** USD ~$1/mes
> - **Resto del stack:** sin cambios
> - **TOTAL v1 corregido:** USD ~43/mes (no USD ~63/mes)
>
> Las cifras "USD ~63/mes" y "Hetzner CX42" en este documento son **históricas** (decisión original sobrescrita). Stack técnico (PostgreSQL+AGE+pgvector+Stella+etc.) NO cambia.
>
> Fuente: [decision-log.md D-009](../../for3s-inter/07-operations/decision-log.md)

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 2.1 — Memory framework](#3-sub-tema-21--memory-framework)
4. [Sub-tema 2.4 — Memory tiers](#4-sub-tema-24--memory-tiers)
5. [Sub-tema 2.2 — Embeddings](#5-sub-tema-22--embeddings)
6. [Sub-tema 2.3 — Vector indexing](#6-sub-tema-23--vector-indexing)
7. [Sub-tema 2.5 — Forgetting strategy](#7-sub-tema-25--forgetting-strategy)
8. [Sub-tema 2.6 — CLS Consolidation](#8-sub-tema-26--cls-consolidation)
9. [Sub-tema 2.7 — Mapeo Nodo ↔ Tabla SQL](#9-sub-tema-27--mapeo-nodo--tabla-sql)
10. [Stack final consolidado](#10-stack-final-consolidado)
11. [Arquitectura emergente — diagrama](#11-arquitectura-emergente--diagrama)
12. [Diccionario bilingüe cerebral ↔ técnico](#12-diccionario-bilingüe-cerebral--técnico)
13. [Cobertura del Grafo Maestro](#13-cobertura-del-grafo-maestro)
14. [Costo total actualizado](#14-costo-total-actualizado)
15. [Exploraciones futuras NO adoptadas v1](#15-exploraciones-futuras-no-adoptadas-v1)
16. [Implicaciones en bloques siguientes](#16-implicaciones-en-bloques-siguientes)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 2 — MEMORY ARCHITECTURE                               ║
║   7 sub-temas LOCKED el 2026-06-01                             ║
║                                                                ║
║   2.1 Memory framework  → Custom + librerías composables       ║
║   2.4 Memory tiers      → 3 tiers clásico (Working/Short/Long) ║
║   2.2 Embeddings        → Stella local @ 1024 + OpenAI fallback║
║   2.3 Vector indexing   → HNSW @ 1024 cosine tuneado           ║
║   2.5 Forgetting        → Soft + Decay + Archive (Microglía)    ║
║   2.6 CLS Consolidation → Híbrido Heurística + Haiku 4.5        ║
║   2.7 Mapeo Nodo↔Tabla  → Documentación oficial                 ║
║                                                                ║
║   Servicios extra:        0                                    ║
║   Costo incremental B2:   ~USD 49/mes (CX42 upgrade + CLS)     ║
║   Costo total v1 (B1+B2): ~USD 63/mes                          ║
║   % techo Pilot Light:    7% (vs 25% permitido)                ║
║   Nodos servidos B2:      6 fully + 4 foundation = 10/11       ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Custom core con librerías composables, mapeo 1:1 con
el cerebro biológico, control total sobre la semántica."
```

Las 7 decisiones convergen en patrones consistentes:

```
1. CONTROL 100% del código (2.1)
   → memory/ como módulo propio
   → librerías solo para piezas standard

2. ALINEACIÓN cerebral 1:1 (2.4 + 2.7)
   → 3 tiers cerebrales explícitos
   → Mapeo Nodo↔Tabla documentado

3. PRIVACY-FIRST (2.2 + 2.6)
   → Stella local (datos no salen)
   → CLS solo envía summaries al LLM, no datos crudos

4. REVERSIBILIDAD (2.5)
   → Forgetting en 4 etapas (~13 meses a purge final)
   → Audit del propio forgetting

5. CALIDAD/COSTO balance (2.3 + 2.6)
   → HNSW tuneado (recall ~97-99%)
   → Haiku 4.5 para CLS (no Opus)

6. CONSISTENCIA con Bloque 1
   → Todo vive en mismo Postgres
   → Cero servicios extra añadidos
```

### Por qué esta filosofía importa

**Para Pilar 3 Autonomía:** El agente tiene CONTROL total sobre su propio sistema de memoria. No depende de framework externo cuyo roadmap escape.

**Para Pilar 1 Seguridad:** Datos del cliente jamás salen de la infra (Stella local) excepto summaries focalizados (CLS).

**Para Anclas:** Cero servicios extra (3.D), Open Core puro (2.B), Dedicated por workspace (1.D).

---

## 3. Sub-tema 2.1 — Memory framework

### Decisión LOCKED

```
Híbrido — Custom core + librerías pequeñas composables
```

### Contexto

Un memory framework abstrae las operaciones de memoria del agente sobre el storage (Postgres + pgvector + AGE) ya decidido en Bloque 1. La pregunta no era "¿qué storage?" sino "¿quién es dueño de la lógica de memoria?".

### Mapeo al Grafo Maestro

- **Nodo 2 (Hipocampo):** operaciones recall/store
- **Nodo 4 (Skills):** storage y retrieval de skills
- **Nodo 1 (KG):** bridge semántico
- **Nodo 10 (CLS):** consolidación
- **Nodo 3 (PFC):** working memory dentro del framework
- **Pilar 1 Seguridad:** datos no salen sin permiso
- **Pilar 3 Autonomía:** control total sobre lógica del agente

### Candidatos evaluados

```
A) Honcho             ⚠️ Brian ya tenía API key, conflicto schema
B) Mem0               ❌ Modelo chatbot-centric
C) Zep Community      ⚠️ Stagnación + conflicto Neo4j/AGE
D) Custom build PURO  ✅ Control total
E) Híbrido            ✅ ELEGIDO (custom + composables)
```

### Razones de la decisión

1. **Alineación PERFECTA con Bloque 1 LOCKED** — usa nuestras tablas ES + AGE directamente
2. **Respeta regla R1 LOCKED** — "tecnología por criterio técnico, no preferencia"
3. **Control 100% del código** — sin riesgo discontinuación de tercero
4. **Cero servicios extra** — respeta 3.D
5. **Aprovecha estado del arte** donde importa (pgvector-python, sentence-transformers)
6. **Bloque 1 ya pintó el rincón custom** — frameworks externos no usaban NADA de nuestras decisiones previas

### Estructura del módulo memory/

```
for3s_os/memory/
├── repository.py     → CRUD sobre tablas ES con SQLAlchemy 2
├── embedder.py        → adapter para embeddings (Stella + OpenAI)
├── ranker.py          → híbrido similarity + recency
├── kg_bridge.py       → wrapper Cypher para Apache AGE
├── consolidator.py    → CLS jobs (sub-tema 2.6)
├── forgetter.py       → Microglía (sub-tema 2.5)
├── tiers.py           → working/short/long (sub-tema 2.4)
└── api.py             → API pública: recall/store/build_context
```

### Librerías composables permitidas v1

- `pgvector-python` (oficial, BSD)
- `sentence-transformers` (Apache 2.0) — Stella embeddings
- `hdbscan` (BSD) — clustering CLS
- `cryptography` (Apache 2.0 + BSD) — P4 encryption
- `anthropic` SDK (oficial) — Claude Haiku para CLS
- `openai` SDK (oficial) — fallback embeddings

### Path futuro

```
v1: Custom core + librerías composables
v2: Evaluar Honcho Dialectic API como enriquecedor (NO reemplazo)
v3: Re-evaluar si parte del custom puede usar lib externa
```

---

## 4. Sub-tema 2.4 — Memory tiers

### Decisión LOCKED

```
3 tiers clásico (Working + Short-term + Long-term)
```

### Contexto

Organizar la memoria del agente en capas con horizontes temporales y propósitos distintos, igual que el cerebro humano. Cada tier tiene storage, política y propósito específicos.

### Mapeo al Grafo Maestro

- **Tier 1 ↔ Nodo 3 PFC** (Working Memory)
- **Tier 2 ↔ Nodo 2 Hipocampo** (Short-term)
- **Tier 3 ↔ Nodo 1 KG** (Long-term semántico)
- Transiciones modelan **Nodo 10 CLS** y **Nodo 6 Microglía**

### Candidatos evaluados

```
A) 2 tiers (short + long, sin working)       ⚠️ Pierde Nodo 3 PFC
B) 3 tiers clásico                           ✅ ELEGIDO
C) 4 tiers Hermes-style (+ Redis cache)      ❌ Premature opt (3.1 pendiente)
D) Tiers por dominio                          ❌ Modelo no estándar
```

### Arquitectura LOCKED

```
TIER 1 — WORKING (Nodo 3 PFC)
   Storage: in-process Python (deque + dict por session_id)
   Duración: vida de la sesión actual
   Capacidad: ~15 items, TTL ~60 min
   Política: AGRESIVA (efímero por diseño)
   Velocidad: ~0 ms

TIER 2 — SHORT-TERM (Nodo 2 Hipocampo)
   Storage: PostgreSQL
     • episodes_events (ES inmutable)
     • episodes_state (projection)
     • pgvector embeddings + HNSW
   Duración: 30-90 días (default 60)
   Capacidad: ilimitada (limitada por retención)
   Política: CONSERVADORA (perder señal es caro)
   Velocidad: ~10-50 ms (HNSW search)

TIER 3 — LONG-TERM (Nodo 1 KG)
   Storage: Apache AGE + pgvector concepts
     • Nodos AGE: PRs, Files, Bugs, Skills, Concepts
     • Aristas: TOUCHES, CAUSED, SIMILAR, DERIVED_FROM
     • Concept embeddings en pgvector
   Duración: permanente (audit chain inmutable)
   Capacidad: ilimitada
   Política: MUY CONSERVADORA (KG es conocimiento estructurado)
   Velocidad: ~20-100 ms (Cypher)
```

### Transiciones entre tiers

```
Working → Short:
   • Al cerrar sesión (graceful shutdown)
   • Cuando working memory excede max_items
   • Eventos batch insert a episodes_events

Short → Long:
   • Job nocturno CLS (sub-tema 2.6)
   • Trigger: consolidated_to_kg = true

Forgetting:
   • Working: TTL automático + LRU
   • Short: decay scores + soft delete (2.5)
   • Long: edge weight decay + prune (2.5)
```

### Políticas de retrieval (build_context budget=8000 tokens)

```
1. Working: últimos 5 items (siempre incluidos, ~500 tok)
2. Short: top-10 episodios similares (HNSW, ~3000 tok)
3. Long: top-5 conceptos relacionados (Cypher, ~2000 tok)
4. Mezcla con re-ranking final (~500 tok overhead)
5. Retorna contexto compacto ~6000 tokens efectivos
```

### Path futuro

```
v1: 3 tiers como descrito
v2: añadir Tier intermedio Redis cache si Bloque 3 lo justifica
v3: tiers especializados por dominio si complejidad lo demanda
```

---

## 5. Sub-tema 2.2 — Embeddings

### Decisión LOCKED

```
stella_en_400M_v5 LOCAL @ 1024 dim + OpenAI 3-small fallback
```

### Contexto

Un embedding traduce texto/código a vector numérico que captura significado semántico. Es la materia prima del Tier 2 (Hipocampo) y Tier 3 (concepts KG).

### Mapeo al Grafo Maestro

- **Nodo 2 (Hipocampo):** embeddings de episodios
- **Nodo 1 (KG):** embeddings de conceptos
- **Nodo 4 (Skills):** embeddings de contexto skill
- **Nodo 9 (Pattern Separation):** calidad depende de quality embeddings
- **Pilar 1 (Seguridad):** Stella local = datos NO salen
- **Ancla 2.B (Open Core):** MIT license

### Candidatos evaluados

```
A) OpenAI text-embedding-3-small      ⚠️ API externa, MTEB 62.3
B) OpenAI text-embedding-3-large       ⚠️ API externa, MTEB 64.6, 6.5x caro
C) Voyage-3-large                      ⚠️ API externa, MTEB 65.7
D) Cohere embed-v3                     ⚠️ API externa, mid-tier
E) Local (bge-large-en-v1.5)           ⚠️ Context 512 tokens (limitado)
F) Local (nomic-embed-text-v1.5)       ✅ Equivalente OpenAI 3-small
G) Local (stella_en_400M_v5)           ✅ ELEGIDO (mejor MTEB que OpenAI large)
H) Local (e5-mistral-7b-instruct)      ⚠️ Requiere GPU $200/mes
```

### Razones de la decisión

1. **Calidad superior a OpenAI 3-large** — MTEB 66.5 vs 64.6
2. **Privacy TOTAL** — datos jamás salen de tu infra
3. **Cero costo API** — libera presupuesto AI para R3 LLMs
4. **MIT license** — 2.B Open Core puro
5. **Sin vendor lock-in** — autonomía estratégica
6. **CPU viable** — no GPU, sin pain operacional
7. **Context 8K** — cubre 99% de episodios For3s QA
8. **Prepara cliente regulado v2** sin migración

### Stack final embeddings

```
Primary embedder:
   Model:     dunzhang/stella_en_400M_v5
   Dim:       1024 (con Matryoshka parcial a 512)
   Context:   8,192 tokens
   Tamaño:    ~1.6 GB en RAM
   Licencia:  MIT
   Runtime:   CPU (sentence-transformers + PyTorch)

Fallback embedder:
   Model:     OpenAI text-embedding-3-small
   Dim:       1536 (con Matryoshka truncable)
   Activación: Solo si Stella crashea o sobrecarga
   Marcado:   embedding_model column en tablas
```

### Hardware actualizado por esta decisión

```
EVOLUCIÓN COMPLETA (3 iteraciones):

1. Bloque 1 original:    Hetzner CX32 (8 GB RAM, ~USD 13/mes)
2. Update post-2.2:      Hetzner CX42 (16 GB RAM, ~USD 25/mes)
   Razón: Stella 1.6 GB + Postgres 3 GB + HNSW 7.5 GB ≈ 12 GB
3. D-009 LOCKED v1:      Linux LOCAL Brian (30 GB RAM, 1 TB)
   USD 0 hardware + ~USD 5/mes electricidad
   Razón: despliegue local v1 (clarificado por Brian post-B3)

HARDWARE VIGENTE v1: Linux LOCAL Brian.
Sobra holgado: 30 GB RAM vs ~12 GB necesarios.
```

### Versionado de embeddings

```sql
ALTER TABLE wks_X.episodes_state ADD COLUMN
   embedding VECTOR(1024),
   embedding_model TEXT NOT NULL
   DEFAULT 'stella:dunzhang_400M_v5@1024';
```

Permite coexistencia de embeddings con distintos modelos durante migraciones futuras.

### Política de fallback

```python
try:
    vec = await stella_embedder.embed(text)
    model = 'stella:dunzhang_400M_v5@1024'
except (ModelLoadError, OOMError) as e:
    logger.warn("Stella down, fallback to OpenAI", err=e)
    vec = await openai_embedder.embed(text)
    model = 'openai:text-embedding-3-small@1536'
```

### Path futuro

```
v1: Stella local CPU @ 1024 + OpenAI fallback (CX42)
v2: Stella con instruction-tuning específico For3s QA
v3: Evaluar e5-mistral-7b con GPU si calidad insuficiente
```

---

## 6. Sub-tema 2.3 — Vector indexing

### Decisión LOCKED

```
HNSW con parámetros tuneados
   • m = 16
   • ef_construction = 128
   • ef_search = 100 (configurable por query)
   • distance metric = cosine
   • dim = 1024 (Stella)
```

### Contexto

Un índice vectorial hace que "dame los K vectores más parecidos" sea rápido en lugar de comparar contra cada uno de millones. Trade-off central: precisión vs velocidad/memoria.

### Mapeo al Grafo Maestro

- **Nodo 9 (Pattern Separation):** función crítica del índice
- **Nodo 2 (Hipocampo):** búsqueda episodios similares
- **Nodo 1 (KG):** búsqueda conceptos relacionados
- **Nodo 4 (Skills):** matching por similitud

### Candidatos evaluados

```
A) HNSW              ✅ ELEGIDO — recall ~97-99%, RAM-hungry
B) IVFFlat           ⚠️ Recall ~90-95%, memoria eficiente
C) Flat              ❌ INVIABLE en producción (sin índice)
D) Híbrido HNSW+IVF  ⚠️ Ahorro RAM marginal, complejidad +
```

### Razones de la decisión

1. **Recall superior** (~97-99%) crítico para Pattern Separation (Nodo 9)
2. **Cabe holgado** en CX42 v1 (~7.5 GB de 16 GB)
3. **Latencia <30ms** v1 con parámetros tuneados
4. **Estándar de industria** para ANN
5. **Soporte oficial** pgvector + SQLAlchemy 2
6. **Upgrade path claro:** v2 CCX22 → v3 Qdrant + quantization

### DDL de referencia para Alembic

```sql
-- Por workspace_id (multi-schema P3):
CREATE INDEX idx_episodes_state_embedding
  ON {schema}.episodes_state
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 128);

-- En cada query:
SET hnsw.ef_search = 100;
SELECT * FROM {schema}.episodes_state
WHERE deleted_at IS NULL
ORDER BY embedding <=> $1 LIMIT 10;
```

### Política multi-schema

```
shared.audit_events           → SIN índice vector
wks_A.episodes_state          → HNSW @ 1024 cosine
wks_A.skills_state            → HNSW @ 1024 cosine
wks_A.concepts (Tier 3 KG)    → HNSW @ 1024 cosine
wks_B, wks_C, ... → mismo patrón replicado
```

Ventaja: índices más pequeños por schema → menor RAM por índice individual + mejor isolation P3.

### Monitoring obligatorio desde día 1

```
Métricas:
   • RAM HNSW (pg_stat_user_indexes)
   • Latencia p50/p95/p99 por query vector
   • Recall periódico (test vs Flat ground truth)
   • shared_buffers usage Postgres

Alertas:
   • RAM HNSW >70% del total disponible → upgrade plan
   • Latencia p95 >100ms sostenida → tuning/quantization
   • Recall <95% → revisar params o cambio de algoritmo
```

### Path futuro

```
v1: HNSW @ 1024 cosine, params tuneados
v2: monitor + evaluar IVFFlat si RAM aprieta
v3: quantization o migración Qdrant según métricas
```

---

## 7. Sub-tema 2.5 — Forgetting strategy

### Decisión LOCKED

```
Soft Delete + Decay scores + Archive cold storage
```

### Contexto

Sin forgetting, el agente se ahoga en ruido acumulado. Microglía (Nodo 6) es el equivalente al sistema biológico de poda sináptica.

### Mapeo al Grafo Maestro

- **Nodo 6 (Microglía):** razón de ser
- **Nodo 2 (Hipocampo):** decay/archive episodios viejos
- **Nodo 4 (Skills):** skills bajo success_rate → forgetting
- **Nodo 1 (KG):** edge pruning
- **Nodo 10 (CLS):** trigger consolidated_to_kg
- **Pilar 1 (Seguridad):** audit_events INMUTABLE, NUNCA tocar

### Candidatos evaluados

```
A) Hard delete agresivo                  ❌ Irreversible
B) Soft + Decay + Archive                 ✅ ELEGIDO
C) Solo Decay (sin delete nunca)          ⚠️ Storage infinito
D) Consolidation-only                     ⚠️ Incompleto solo
```

### Razones de la decisión

1. **Reversibilidad en 4 etapas** (~13 meses total a purge)
2. **Modelo cerebral real** (Microglía adulta sana)
3. **Audit automático del forgetting** (Pilar 1 §6.4)
4. **Respeta inmutabilidad** del event store
5. **Compliance-friendly** (12 meses retention default)
6. **Configurable por workspace**
7. **Workers async** sin bloquear queries

### Políticas LOCKED v1

```
TIER 1 — WORKING
   • TTL: 60 minutos sin actividad
   • Cap: 15 items LRU
   • Política: AGRESIVA (efímero por diseño)

TIER 2 — SHORT-TERM
   • Decay: -5% diario sin acceso
   • Soft delete: stale 30d + relevance <0.3 + consolidated
   • Archive: soft-deleted 30d → tabla cold
   • Final purge: archived 12 meses → hard delete
   • EXCEPCIONES:
     - legal_hold
     - consolidated_to_kg = false (no consolidados)
     - referenciados desde Tier 3

TIER 3 — LONG-TERM KG
   • Edge weight decay: -5% mensual sin refuerzo
   • Edge prune: weight <0.05 sostenido 6 meses → DELETE
   • Nodos huérfanos: REVISIÓN MANUAL antes de delete
   • EXCEPCIONES:
     - skills con success_rate >0.7 (siempre persistir)
     - conceptos con flag essential = true

AUDIT CHAIN — NUNCA TOCAR
   • audit_events inmutable (trigger Postgres ya activo)
   • events tables inmutables (ES)
   • Forgetting solo en PROJECTIONS
```

### Schema changes requeridas

```sql
ALTER TABLE wks_X.episodes_state ADD COLUMN
   deleted_at TIMESTAMPTZ,
   relevance_score FLOAT NOT NULL DEFAULT 1.0,
   last_accessed_at TIMESTAMPTZ DEFAULT now(),
   consolidated_to_kg BOOLEAN NOT NULL DEFAULT false,
   legal_hold BOOLEAN NOT NULL DEFAULT false;

CREATE TABLE wks_X.episodes_archived (
   -- mismo schema, sin índice HNSW
   archived_at TIMESTAMPTZ NOT NULL DEFAULT now(),
   archive_reason TEXT
);

CREATE INDEX idx_episodes_state_active
   ON wks_X.episodes_state (last_accessed_at)
   WHERE deleted_at IS NULL;  -- partial index
```

### Workers (coordina con 3.2 Bloque 3)

```
nightly_routine():
   • Working: limpia expired in-process
   • Short: decay scores, soft delete
   • Long: decay edges
   • Log resumen a audit_events

weekly_routine():
   • Archive soft-deleted

monthly_routine():
   • Final purge archived
   • Edge prune Tier 3
```

### Meta-audit pattern obligatorio

```python
# Cada acción de forgetting →
await audit.insert(
    action='forgetting:soft_delete',
    resource_type='episode',
    payload={
        'workspace_id': 'wks_A',
        'episode_id': '...',
        'reason': 'stale_30d + low_relevance',
        'relevance_score': 0.12,
        'reversible_until': '2026-07-01'
    }
)
```

### Path futuro

```
v1: Candidato B con defaults conservadores
v2: ajustar thresholds según datos reales
v3: evaluar políticas adaptativas / ML-driven
```

---

## 8. Sub-tema 2.6 — CLS Consolidation

### Decisión LOCKED

```
Híbrido — Heurística filtra + LLM focaliza
   • Modelo LLM: Claude Haiku 4.5
   • Frecuencia: diario (cron 2 AM workspace TZ)
   • Threshold: skip si <10 episodios pending
   • Clustering: HDBSCAN con min_cluster_size=3
   • Privacy: solo summaries al LLM, no episodios crudos
   • Fallback: heurística pura si LLM cae
   • Costo estimado: ~$37/mes v1
```

### Contexto

CLS = Complementary Learning Systems (McClelland, McNaughton & O'Reilly, 1995). Es la teoría neurocientífica de cómo el cerebro durante el sueño consolida memoria episódica (Hipocampo) en memoria semántica (Neocorteza). For3s replica este proceso técnicamente.

### Mapeo al Grafo Maestro

- **Nodo 10 (CLS):** razón de ser
- **Nodo 2 (Hipocampo):** source de episodios
- **Nodo 1 (KG):** destino de conceptos
- **Nodo 4 (Skills):** consolidación de skills frecuentes
- **Nodo 9 (Pattern Separation):** función inversa (pattern completion)
- **Nodo 6 (Microglía):** trigger soft delete
- **Pilar 3 (Autonomía):** lo que hace al agente APRENDER

### Candidatos evaluados

```
A) LLM puro (Claude Opus)        ❌ $3K/mes — viola P2
B) Heurística pura               ⚠️ KG con labels pobres
C) Híbrido (Heurística + LLM)    ✅ ELEGIDO
D) Humano-asistido               ❌ Viola Pilar 3 (autonomía)
```

### Razones de la decisión

1. **Sweet spot calidad/costo** — $37/mes vs $3K (80x más barato)
2. **Cabe holgado en P2 LOCKED** — 1.1% del techo Pilot Light
3. **KG con labels RICOS** desde día 1
4. **Privacy alta** — solo summaries pasan al LLM
5. **Autonomía preservada** (Pilar 3)
6. **Fallback graceful** — heurística pura si LLM cae

### Pipeline del sleep cycle

```
1. Get pending episodes (limit max_per_run)
2. Skip si <threshold (10 episodios)
3. Clustering HDBSCAN sobre embeddings Stella
4. Por cluster: extract concept con Claude Haiku
   • Solo summary (top files, top actions, 3 ejemplos)
   • NO se envían episodios crudos
5. KG populate (Apache AGE)
   • Si concepto similar existe → strengthen edge
   • Si no existe → create node
   • Crear aristas DERIVED_FROM hacia episodios source
6. Mark consolidated_to_kg = true
   → Trigger condición soft delete (2.5 Microglía)
7. Meta-audit a audit_events
```

### Estructura del módulo consolidator.py

```
class ConsolidationPolicy    # config por workspace
class ClusteringEngine        # HDBSCAN
class ConceptExtractor        # LLM Haiku focalizado
class KGPopulator             # escribe Apache AGE
class CLSOrchestrator         # coordina sleep cycle
```

### Coordinación crítica con otros sistemas

```
2.5 Forgetting (Microglía):
   • CLS marca consolidated_to_kg = true
   • Microglía usa flag como condición soft delete
   • Simbióticos

3.2 Background jobs (Bloque 3):
   • CLSOrchestrator necesita scheduler robusto
   • Worker async sin bloquear queries
   • Retry policy si LLM cae

1.2 Apache AGE (Bloque 1):
   • KGPopulator escribe nodos + aristas Cypher
   • Conceptos = nodos AGE
   • DERIVED_FROM = aristas hacia episodes
```

### Meta-audit obligatorio

```python
# Cada run → INSERT audit_events:
await audit.insert(
    action='cls:consolidation',
    resource_type='workspace',
    payload={
        'workspace_id': 'wks_A',
        'episodes_processed': 142,
        'clusters_found': 8,
        'concepts_created': 5,
        'concepts_strengthened': 3,
        'llm_calls': 8,
        'llm_tokens_input': 4500,
        'llm_tokens_output': 1200,
        'cost_usd': 0.023,
        'duration_seconds': 45,
        'fallback_used': False
    }
)
```

### Path futuro

```
v1: Híbrido con Haiku 4.5, diario, threshold 10 eps
v2: evaluar Sonnet 4.6 si calidad insuficiente
v3: evaluar re-consolidation periódica + active learning
```

---

## 9. Sub-tema 2.7 — Mapeo Nodo ↔ Tabla SQL

### Decisión LOCKED

```
Mapeo aceptado como documentación oficial del Bloque 2
```

> **📌 DOCUMENTO CANÓNICO DEDICADO:**
>
> El mapeo completo y exhaustivo vive en su propio documento:
> **[`Mente/Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md`](../Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md)** (21 secciones)
>
> Esa es la fuente de verdad CANÓNICA para:
> - Tabla maestra de 11 nodos × 8 columnas
> - Detalle exhaustivo de cada nodo (tablas, módulos, operaciones)
> - Diccionario bilingüe cerebral ↔ técnico completo
> - Flujos cross-nodo
> - Excepciones inmutables (NUNCA tocar)
> - Protocolo de actualización del documento
>
> Esta sección §9 contiene solo el RESUMEN del mapeo para coherencia del Bloque 2.
> Para implementar o consultar, ir al documento canónico.

### Contexto

NO hay debate técnico — es documentación explícita del bridge entre el Grafo Maestro (vocabulario cerebral) y For3s OS (estructuras técnicas concretas). Sirve como referencia permanente para devs, code reviews y continuidad cross-sesión.

### Mapeo MAESTRO — 11 Nodos × Status

```
NODO                                STATUS           MÓDULO PRINCIPAL
─────────────────────────────────────────────────────────────────────
Nodo 1 KG (Neocorteza)               ✅ FULLY        memory/kg_bridge.py
Nodo 2 Hipocampo                     ✅ FULLY        memory/repository.py
Nodo 3 PFC                           🟡 PARTIAL      memory/tiers.py (R5 ext)
Nodo 4 Skills (Ganglios B.)          ✅ FULLY        memory/repository.py
Nodo 5 Action selection              🟡 FOUNDATION   memory/ranker.py (R5)
Nodo 6 Microglía                     ✅ FULLY        memory/forgetter.py
Nodo 7 DMN                           ⏳ PENDIENTE    R5 lo define
Nodo 8 Amígdala                      🟡 FOUNDATION   security/* (R9)
Nodo 9 Pattern Separation            ✅ FULLY        repository + ranker
Nodo 10 CLS                          ✅ FULLY        memory/consolidator.py
Nodo 11 Neuromoduladores             🟡 FOUNDATION   ranker + R5

6/11 FULLY mapped, 4/11 foundation ready, 1/11 pendiente
```

### Tabla detallada — TABLAS SQL por Nodo

```
Nodo 1 KG          → shared.{age}.kg_nodes + kg_edges (Apache AGE)
                     wks_X.concepts (pgvector embeddings)

Nodo 2 Hipocampo   → wks_X.episodes_events (ES)
                     wks_X.episodes_state (projection)
                     wks_X.episodes_archived (cold storage)

Nodo 3 PFC         → in-process Python (sin tabla v1)

Nodo 4 Skills      → wks_X.skills_events (ES)
                     wks_X.skills_state (projection)
                     wks_X.skills_archived (cold storage)

Nodo 5             → Reutiliza skills_state + R5 añadirá action_log

Nodo 6 Microglía   → Modifica state tables (deleted_at, scores)
                     Escribe episodes_archived
                     Audit en audit_events

Nodo 7 DMN         → Por definir en R5

Nodo 8 Amígdala    → shared.security_policies (CRUD)
                     shared.rbac_rules (CRUD)
                     R9 añadirá policy_violations

Nodo 9             → Misma tabla Nodo 2 + HNSW config tuneado

Nodo 10 CLS        → Lee episodes_state, escribe AGE
                     Marca consolidated_to_kg
                     Audit en audit_events

Nodo 11 Neuromod.  → Implícita en success_rate, relevance_score
                     R5 añadirá agent_state con tunables
```

### Diccionario bilingüe cerebral ↔ técnico

```
TÉRMINO CEREBRAL              TÉRMINO TÉCNICO FOR3S OS
─────────────────────────────────────────────────────────
Knowledge Graph / Neocorteza  Apache AGE + pgvector concepts
Hipocampo                     pgvector + episodes_events ES
Pattern Separation            HNSW recall ~97-99% threshold
Pattern Completion            HDBSCAN clustering (CLS)
PFC / Working Memory          WorkingMemory in-process deque
Ganglios Basales              skills_events + skills_state
Dopamina / Refuerzo           success_rate++ en skill use
Microglía / Sinaptic pruning  forgetter.py (Soft+Decay+Archive)
DMN / Mind-wandering          orchestrator/dmn.py (futuro R5)
Amígdala                      policy_engine.py (futuro R9)
Sleep cycle / Consolidación   consolidator.py nightly cron
Episodic memory               Tier 2 (Postgres + pgvector)
Semantic memory               Tier 3 (Apache AGE + concept emb)
Sinapsis débil                Edge weight < threshold
Neuroplasticidad              Schema evolution + re-embedding
Trauma / Inmutable            audit_events (hash chain)

OPERACIONES CEREBRALES         OPERACIONES SQL/PYTHON
─────────────────────────────────────────────────────────
"Recordar"                    memory.recall(query, budget)
"Aprender"                    memory.store(episode/skill)
"Olvidar"                     forgetter.soft_delete()
"Consolidar"                  consolidator.run_consolidation()
"Razonar"                     LLM call con context built
"Reflexionar"                 DMN job (R5+)
"Decidir"                     action_selector (R5+)
```

### Propósito eterno del mapeo

Documento VIVO actualizado al añadir/cambiar nodos. Lectura obligatoria para devs antes de tocar memory/. Code reviews verifican impacto en nodos cerebrales.

---

## 10. Stack final consolidado

```
COMPONENTE                  DECISIÓN                            COSTO
──────────────────────────────────────────────────────────────────────
Hardware (upgrade B1→B2)    Hetzner CX42 (16 GB RAM)            USD ~25/mo
Memory framework            Custom + librerías composables       USD 0
Embeddings primary          Stella local @ 1024 dim              USD 0
Embeddings fallback         OpenAI 3-small @ 1536                USD <1/mo
Vector index                HNSW tuneado (m=16, ef=128/100)      USD 0
Forgetting workers          forgetter.py (cron)                   USD 0
CLS Consolidation           Híbrido + Claude Haiku 4.5            USD ~37/mo
Clustering                  HDBSCAN (BSD)                        USD 0
──────────────────────────────────────────────────────────────────────
TOTAL incremental B2                                              USD ~50/mo
TOTAL v1 (B1 + B2)                                                USD ~63/mo
```

### Verificación P2 <25%

```
Pilot Light USD 3,500 (3 sem) → techo USD 875
Infra+AI (3 sem): USD 63 × 3/4 = USD 47.25
→ CONSUMO 5.4% del techo (vs 25% permitido)
→ MARGEN DE 94.6% disponible para R3 (LLM) + R4 (MCP)
```

---

## 11. Arquitectura emergente — diagrama

```
                  FOR3S OS — Arquitectura cerebral completa

   ┌─────────────────────────────────────────────────────────────┐
   │                                                              │
   │   Cliente → Sesión activa (HTTP/Telegram → FastAPI)          │
   │                            │                                  │
   │                            ▼                                  │
   │   ┌───────────────────────────────────────────────────┐      │
   │   │ Nodo 3 — PFC (Working Memory, Tier 1)              │      │
   │   │   for3s_os/memory/tiers.py::WorkingMemory          │      │
   │   │   In-process Python (15 items LRU, TTL 60min)      │      │
   │   └───────────────────────────────────────────────────┘      │
   │            │                              ▲                   │
   │            │ flush al cerrar              │ load context       │
   │            ▼                              │                   │
   │   ┌───────────────────────────────────────────────────┐      │
   │   │ Nodo 2 — HIPOCAMPO (Short-term, Tier 2)            │      │
   │   │   Postgres: episodes_events (ES inmutable)         │      │
   │   │           + episodes_state (projection)             │      │
   │   │   pgvector HNSW @ 1024 cosine (Stella embeddings)  │      │
   │   │   Nodo 9 Pattern Separation activo aquí            │      │
   │   └───────────────────────────────────────────────────┘      │
   │            │                              ▲                   │
   │            │ sleep cycle (diario)         │ retrieval similar  │
   │            │                              │                   │
   │            ▼                              │                   │
   │   ┌───────────────────────────────────────────────────┐      │
   │   │ Nodo 10 — CLS Consolidación                        │      │
   │   │   for3s_os/memory/consolidator.py                  │      │
   │   │   HDBSCAN clustering + LLM Haiku 4.5 focalizado    │      │
   │   │   marca consolidated_to_kg = true                   │      │
   │   └───────────────────────────────────────────────────┘      │
   │            │                                                  │
   │            ▼                                                  │
   │   ┌───────────────────────────────────────────────────┐      │
   │   │ Nodo 1 — KG NEOCORTEZA (Long-term, Tier 3)         │      │
   │   │   Apache AGE: nodos + aristas Cypher               │      │
   │   │   pgvector: embeddings de conceptos                 │      │
   │   │   Workspace subgraph (P3 isolation)                 │      │
   │   └───────────────────────────────────────────────────┘      │
   │            │                                                  │
   │            │ refuerza skills consolidadas                      │
   │            ▼                                                  │
   │   ┌───────────────────────────────────────────────────┐      │
   │   │ Nodo 4/5 — GANGLIOS BASALES (Skills)               │      │
   │   │   Postgres: skills_events + skills_state           │      │
   │   │   memory/repository.py::SkillsRepository           │      │
   │   │   Refuerzo dopaminérgico: success_rate++           │      │
   │   └───────────────────────────────────────────────────┘      │
   │                                                              │
   │   ╔═══════════════════════════════════════════════════╗      │
   │   ║ Nodo 6 — MICROGLÍA (forgetting paralelo, nightly)  ║      │
   │   ║   memory/forgetter.py                              ║      │
   │   ║   Soft delete + Decay scores + Archive              ║      │
   │   ║   PROHIBIDO tocar: audit_events, events tables     ║      │
   │   ╚═══════════════════════════════════════════════════╝      │
   │                                                              │
   │   ╔═══════════════════════════════════════════════════╗      │
   │   ║ Nodo 8 — AMÍGDALA (security/policy gating)         ║      │
   │   ║   shared.security_policies + RBAC                  ║      │
   │   ║   security/policy_engine.py (futuro R9)            ║      │
   │   ╚═══════════════════════════════════════════════════╝      │
   │                                                              │
   │   ╔═══════════════════════════════════════════════════╗      │
   │   ║ Pilar 1 — AUDIT CHAIN (inmutable, NUNCA Microglía) ║      │
   │   ║   shared.audit_events                               ║      │
   │   ║   Hash chain criptográfico (§6.4 Grafo Maestro)     ║      │
   │   ║   Trigger Postgres rechaza UPDATE/DELETE            ║      │
   │   ╚═══════════════════════════════════════════════════╝      │
   │                                                              │
   │   ⏳ PENDIENTES (R3+):                                        │
   │      Nodo 7 — DMN (idle compute) → R5                        │
   │      Nodo 11 — Neuromoduladores completos → R5               │
   │      Nodo 8 — Amígdala completa → R9                         │
   │                                                              │
   └─────────────────────────────────────────────────────────────┘
```

---

## 12. Diccionario bilingüe cerebral ↔ técnico

Ver §9.5 (Diccionario bilingüe) — mismo contenido.

---

## 13. Cobertura del Grafo Maestro

```
NODO                          BLOQUE 1   BLOQUE 2   STATUS
─────────────────────────────────────────────────────────────
Nodo 1 KG (Neocorteza)        ✅ host    ✅ uso     ✅ FULLY
Nodo 2 Hipocampo              ✅ host    ✅ uso     ✅ FULLY
Nodo 3 PFC                    ⏳         🟡 Tier 1   🟡 PARTIAL
Nodo 4 Skills (Ganglios)      ✅ host    ✅ uso     ✅ FULLY
Nodo 5 Ganglios Basales        ⏳        🟡 def      🟡 FOUNDATION
Nodo 6 Microglía              ⏳         ✅ def      ✅ FULLY
Nodo 7 DMN                    ⏳         ⏳         ⏳ PENDIENTE
Nodo 8 Amígdala               ✅ CRUD    ⏳         🟡 FOUNDATION
Nodo 9 Pattern Separation     ✅ host    ✅ uso     ✅ FULLY
Nodo 10 CLS                   ⏳         ✅ def      ✅ FULLY
Nodo 11 Neuromoduladores      ✅ CRUD    🟡 parcial  🟡 FOUNDATION

BLOQUE 2 cierra 4 nodos más (6, 9 uso, 10, 4 uso completo).
Quedan: Nodo 7 (R5), Nodo 11 completo (R5), Nodo 8 completo (R9).
```

```
Pilares — Cobertura por Bloque 2

Pilar 1 — Seguridad E2E
   ✓ Privacy: Stella local (datos no salen)
   ✓ Meta-audit de forgetting + CLS
   ✓ Inmutabilidad respetada
   → Estado: REFORZADO sobre Bloque 1

Pilar 2 — Escalabilidad por nodo
   ✓ Memory tiers escalan distinto
   ✓ Forgetting evita acumulación ruido
   🟡 Aún pendiente: connection pooling, cache (Bloque 3)

Pilar 3 — Autonomía Generativa
   ✅ Custom memory framework = control total
   ✅ CLS = agente APRENDE realmente
   ✅ Forgetting autónomo
```

```
Anclas LOCKED — Verificación post-Bloque 2

1.D Dedicated SaaS:  ✅ Schema-per-tenant respetado
2.B Open Core:       ✅ Todas licencias permisivas
                        • Stella (MIT)
                        • HDBSCAN (BSD)
                        • SDK Anthropic (oficial)
                        • SDK OpenAI (oficial fallback)
3.D Equipo pequeño:  ✅ Cero servicios extra. Solo +RAM.
```

---

## 14. Costo total actualizado

```
Hetzner CX42 (8 vCPU+, 16 GB RAM, 160 GB SSD):    USD ~25/mes
PostgreSQL 16 + AGE + pgvector + pgcrypto:        USD 0
Stella embeddings local (modelo):                  USD 0
OpenAI fallback embeddings:                        USD <1/mes
SQLAlchemy 2 + Pydantic v2 + Alembic:              USD 0
Custom memory module:                              USD 0
HDBSCAN clustering:                                USD 0
Claude Haiku 4.5 (CLS, ~$0.025/run × 30 × 50 wks): USD ~37/mes
─────────────────────────────────────────────────────────────
TOTAL infra v1 (B1 + B2):                          USD ~63/mes
```

### Vs constraint P2 <25%

```
Pilot Light USD 3,500 (3 semanas)
   25% techo = USD 875
   Infra+AI Bloque 1+2 (3 sem) = USD 47.25
   → CONSUMO 5.4% del techo

Pilot Pro USD 8,000 (3 semanas)
   25% techo = USD 2,000
   → CONSUMO 2.4% del techo

CONCLUSIÓN: Infra+memoria holgada por 18x.
   Margen disponible para LLM principal (R3) + MCP (R4).
```

---

## 15. Exploraciones futuras NO adoptadas v1

Esta sección documenta las opciones evaluadas y NO elegidas, con triggers objetivos para reconsiderarlas en el futuro. **NO alteran la línea v1.**

### 📚 Sub-tema 2.4 — Memory tiers alternativos

```
📚 Candidato C — 4 tiers Hermes-style (Redis cache)
   • Cuándo evaluar: si Bloque 3 LOCKEA Redis con propósito
     de cache caliente compartido cross-procesos.
   • Beneficio esperado: latencia 1-5 ms en queries muy
     frecuentes; pre-computed embeddings.
   • Costo a considerar: +1 servicio Redis, lógica de
     invalidación, complejidad de coherencia.
   • Trigger objetivo:
       - Latencia p95 de short-term >100ms sostenido
       - Volumen >100 req/min de queries similares
       - Cliente enterprise demanda latencia <50ms

📚 Candidato D — Tiers por dominio
   • Cuándo evaluar: si el agente desarrolla razonamiento
     suficientemente complejo que 3 tiers temporales no basten.
   • Beneficio esperado: políticas de retención específicas
     por dominio.
   • Costo: modelo mental más complejo, coordinación inter-
     dominios.
   • Trigger objetivo:
       - Skills necesitan ciclo de vida muy distinto a episodes
       - Concepts del KG requieren versionado independiente
       - Agente desarrolla "personalidades" o sub-agentes
```

### 📚 Sub-tema 2.3 — Vector indexing alternativos

```
📚 Candidato B — IVFFlat
   • Cuándo evaluar: si RAM HNSW supera 50% del total
     disponible sostenido por >2 semanas.
   • Beneficio: -30% RAM por costo de -5-7% recall.
   • Costo: pérdida de Pattern Separation precision.
   • Trigger objetivo:
       - RAM HNSW >50% sostenido
       - Volumen >100M vectores con CX42/CCX22 saturado

📚 Candidato D — Híbrido HNSW T2 + IVFFlat T3
   • Cuándo evaluar: si Tier 3 (conceptos KG) crece
     desproporcionado vs Tier 2 (episodios).
   • Beneficio: optimización por patrón de uso.
   • Costo: 2 sets de params a tunear, mayor complejidad.
   • Trigger objetivo:
       - Tier 3 supera 50% del volumen vectorial total
       - Queries cold (Tier 3) <30% de queries totales

📚 Quantization (IVFPQ, binary, scalar)
   • Cuándo evaluar: si v3 escala demanda compresión brutal.
   • Beneficio: 4-32x reducción de RAM.
   • Costo: complejidad de tuning, recall puede caer.
   • Trigger objetivo:
       - Vectores >50M total
       - Upgrade a CCX22 ya no cabe en P2 <25%

📚 Migración a Qdrant
   • PLANEADA en Bloque 1 sub-tema 1.3.
   • Trigger: >5M vectores por workspace, latencia <10ms
     crítica, quantization scalar/binary necesaria, cliente
     enterprise exige sharding nativo.
```

### 📚 Sub-tema 2.5 — Forgetting alternativos

```
📚 Candidato A — Hard delete agresivo
   • Cuándo evaluar: solo para datos NO-críticos
     (working memory cache, query temp results).
   • NUNCA aplicar a: episodes, skills, audit.

📚 Candidato C — Solo decay (sin delete nunca)
   • Cuándo evaluar: v3 si hardware sin límite o cliente
     enterprise exige zero deletion.
   • Beneficio: cero riesgo de pérdida de señal.
   • Costo: storage y RAM crecen sin tope.

📚 Candidato D — Consolidation-only forgetting
   • YA INCLUIDO como POLÍTICA dentro de Candidato B
     (trigger consolidated_to_kg = true).

📚 Forgetting basado en feedback humano (RLHF-style)
   • Cuándo evaluar: v2 cuando tengas usuarios activos.
   • Beneficio: usuario marca episodios como "no relevante".
   • Trigger: agente recurre a episodios irrelevantes y
     usuario los rechaza repetidamente.

📚 Forgetting adaptativo (ML-driven thresholds)
   • Cuándo evaluar: v3 con datos suficientes (12+ meses).
   • Beneficio: model aprende qué olvidar según patrones reales.
   • Costo: complejidad ML ops.
```

### 📚 Sub-tema 2.6 — CLS Consolidation alternativos

```
📚 Candidato A — LLM puro (Claude Opus 4.7)
   • Cuándo evaluar: clientes enterprise que pagan premium
     por máxima calidad de consolidación.
   • Costo: ~$3,000/mes vs $37 actual.
   • Trigger:
       - Cliente pide "máxima profundidad de razonamiento"
       - Tier pricing enterprise lo justifica (~$15K+/mes)
       - Review humano muestra Haiku pierde nuances críticas

📚 Modelo Sonnet 4.6 o Opus 4.7 en Híbrido
   • Cuándo evaluar: upgrade del LLM dentro del Candidato C
     si Haiku queda corto.
   • Costo: Sonnet ~$112/mes vs $37 Haiku. Opus ~$555/mes.
   • Trigger:
       - Review humano de KG muestra labels pobres
       - Aristas mal inferidas
       - Cliente reporta razonamiento insuficiente

📚 Re-consolidación periódica (rebuild KG completo)
   • Cuándo evaluar: v2-v3 con datos suficientes (12+ meses).
   • Beneficio: KG rebuild desde scratch con heurística aprendida.
   • Trigger:
       - KG saturado de conceptos obsoletos
       - Heurística clustering ha mejorado significativamente

📚 Active learning del clustering
   • Cuándo evaluar: v3 con datos suficientes.
   • Beneficio: modelo aprende qué hace bueno un cluster.
   • Costo: complejidad ML ops + entrenamiento.

📚 CLS multi-workspace (cross-tenant patterns)
   • Cuándo evaluar: v3+ si éticamente permitido.
   • Beneficio: "industry knowledge" cross-cliente.
   • Costo: ALTO en privacy/legal/contractual.
   • Trigger:
       - Cliente firma acuerdo explícito data sharing
       - For3s ofrece tier "Industry Intelligence"
       - Compliance/legal aprueban anonymization
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**
Son documentadas para investigación basada en datos reales, NO para implementación sin justificación cuantitativa.

---

## 16. Implicaciones en bloques siguientes

### Para Bloque 3 — Performance & Async

```
✅ Background jobs (3.2) deberá correr:
   • forgetter nightly/weekly/monthly (2.5)
   • consolidator nightly (2.6)
   • Decisión Celery vs Arq vs APScheduler informada por esto

✅ Redis (3.1) si se LOCKEA puede:
   • Activar Candidato C exploración (4 tiers Hermes-style)
   • Cachear embeddings frecuentes
   • Pub/sub para coordinación inter-workers

✅ Connection pooling (3.3):
   • Workers async no deben saturar Postgres
   • pgbouncer recomendado dado volumen workers

✅ Async patterns (3.4):
   • asyncio coordination entre tiers
   • Stella embeddings tienen latencia 100-300ms → async OK
```

### Para Bloque 4 — Files & External

```
✅ Backup strategy (4.4):
   • Modelo Stella debe respaldarse junto con Postgres
   • Snapshot del modelo + DB para reproducibilidad
```

### Para R3 — Model/LLM Layer

```
✅ Claude Haiku 4.5 ya está USADO en CLS
   → R3 puede confirmar Haiku para CLS + decidir LLM principal
✅ Anthropic SDK ya integrado en consolidator.py
✅ Embeddings YA definidos (no decidir de nuevo en R3)
```

### Para R5 — Orchestration

```
✅ Tier 1 Working Memory existe
   → R5 extiende con planning, metacognición, dual-process
✅ Nodo 3 PFC parcialmente mapeado
   → R5 completa con orchestrator/dmn.py, action_selector.py
✅ Nodo 7 DMN reservado para R5
```

### Para R8 — Observability

```
✅ Métricas obligatorias documentadas:
   • RAM HNSW
   • Latencia p50/p95/p99 vector queries
   • Recall periódico vs Flat ground truth
   • Costo CLS por workspace
   • Forgetting volumen + reversiones
```

### Para R9 — Security/Compliance

```
✅ Audit chain inmutable ya respetada en B2
✅ Meta-audit de forgetting + CLS ya documentado
✅ Nodo 8 Amígdala foundation lista
   → R9 completa con policy_engine.py
```

---

## Cierre del Bloque 2

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ BLOQUE 2 — MEMORY ARCHITECTURE CERRADO                    ║
║                                                                ║
║   7/7 sub-temas LOCKED                                         ║
║   Costo incremental: USD ~50/mes (CX42 upgrade + CLS)          ║
║   Costo total v1 (B1+B2): USD ~63/mes (5.4% techo Pilot)       ║
║   Servicios extra añadidos: 0                                  ║
║   Nodos cerebrales: 10/11 servidos (1 pendiente R5)            ║
║                                                                ║
║   Próximo: Bloque 3 — Performance & Async                      ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```