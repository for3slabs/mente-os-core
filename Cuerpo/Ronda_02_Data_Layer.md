# Ronda 2 — Data Layer (Master)

**Segunda de las 10 rondas técnicas. Documento maestro de R2.**

**Owner:** Brian López
**Fecha de inicio:** 2026-06-01
**Estatus:** 🟡 EN CURSO (Bloque 1 LOCKED · Bloques 2-4 pendientes)
**Modo de debate:** B+A (bloques temáticos + sub-temas explícitos uno por uno)
**Capa:** Cuerpo — implementación ejecutable
**Documentos ancla:**
- [Mente/Cerebro/For3s_OS_Grafo_Maestro.md](../Cerebro/For3s_OS_Grafo_Maestro.md) — fuente de verdad técnica
- [Mente/Cuerpo/Ronda_01_Compute_Lenguaje.md](Ronda_01_Compute_Lenguaje.md) — stack Python LOCKED
- [Mente/Doc/Estado_Sesion_Continuidad.md](../Doc/Estado_Sesion_Continuidad.md) — continuidad cross-sesión

**Estatus:** ✅ **R2 — DATA LAYER 100% CERRADO** (20/20 sub-temas LOCKED) — 2026-06-01

**Sub-documentos detallados:**
- ✅ [Ronda_02_Bloque_1_Storage_Foundation.md](Ronda_02_Bloque_1_Storage_Foundation.md) — Storage Foundation (6/6 LOCKED)
- ✅ [Ronda_02_Bloque_2_Memory_Architecture.md](Ronda_02_Bloque_2_Memory_Architecture.md) — Memory Architecture (7/7 LOCKED)
- ✅ [Ronda_02_Bloque_3_Performance_Async.md](Ronda_02_Bloque_3_Performance_Async.md) — Performance & Async (4/4 LOCKED)
- ✅ [Ronda_02_Bloque_4_Files_External.md](Ronda_02_Bloque_4_Files_External.md) — Files & External (3/3 LOCKED) ⭐ CIERRA R2

**Decisiones loggeadas en for3s-inter:**
- [D-005 — Tensión E2E resuelta vía P4 híbrido](../../for3s-inter/07-operations/decision-log.md)
- [D-006 — Stack Data Layer Storage Foundation LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-007 — Stack Memory Architecture LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-008 — Stack Performance & Async LOCKED](../../for3s-inter/07-operations/decision-log.md)
- [D-009 — Despliegue LOCAL Linux + Cloudflare Tunnel](../../for3s-inter/07-operations/decision-log.md) ⭐ sobrescribe hardware de D-006
- [D-010 — Sub-tema 4.3 movido de R2 a R4 (Tools/MCP)](../../for3s-inter/07-operations/decision-log.md)
- [D-011 — Stack Files & External LOCKED + R2 100% CERRADO](../../for3s-inter/07-operations/decision-log.md) ⭐

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core
- 3.D — Equipo pequeño contratado (2-3 personas)

---

## Tabla de contenidos

1. [Propósito de R2](#1-propósito-de-r2)
2. [Pre-rondas — 5 preguntas contextuales LOCKED](#2-pre-rondas--5-preguntas-contextuales-locked)
3. [Estructura B+A — 4 bloques · 21 sub-temas](#3-estructura-ba--4-bloques--21-sub-temas)
4. [Resumen ejecutivo Bloque 1 — Storage Foundation](#4-resumen-ejecutivo-bloque-1--storage-foundation)
5. [Status Bloques 2, 3, 4](#5-status-bloques-2-3-4)
6. [Cobertura del Grafo Maestro](#6-cobertura-del-grafo-maestro)
7. [Riesgos legítimos aceptados](#7-riesgos-legítimos-aceptados)
8. [Spillover hacia for3s-inter/](#8-spillover-hacia-for3s-inter)
9. [Próximo paso](#9-próximo-paso)

---

## 1. Propósito de R2

R2 — Data Layer es la **columna vertebral** de For3s OS. Define el storage físico, la semántica de memoria del agente, la arquitectura de performance asíncrona, y el manejo de archivos externos.

### Lo que R2 materializa del Grafo Maestro

```
   ╔══════════════════════════════════════════════════════════╗
   ║   PIEZAS DEL GRAFO MAESTRO ATERRIZADAS EN R2             ║
   ║                                                          ║
   ║   • Nodo 1 — Knowledge Graph (Neocorteza semántica)       ║
   ║   • Nodo 2 — Hipocampo + Pattern Separation               ║
   ║   • Nodo 4 — Ganglios Basales (Skills)                    ║
   ║   • Nodo 6 — Microglía (forgetting)                       ║
   ║   • Nodo 9 — Pattern Separation                           ║
   ║   • Nodo 10 — Consolidación CLS                           ║
   ║   • Pilar 1 — Seguridad E2E (workspace boundaries)        ║
   ║   • Pilar 2 — Escalabilidad por nodo                      ║
   ╚══════════════════════════════════════════════════════════╝
```

### Relación con R1

R1 LOCKED el **lenguaje y runtime** (Python 3.12 + FastAPI + Pydantic v2 + asyncio). R2 LOCKEA **dónde y cómo vive la información** que ese runtime procesa.

R1 sin R2 = código sin memoria.
R2 sin R1 = datos sin agente.

---

## 2. Pre-rondas — 5 preguntas contextuales LOCKED

Antes de los sub-temas técnicos, R2 abrió con 5 preguntas contextuales que definieron el espacio de soluciones.

### P1 — Volumen estimado por workspace v1 ✅ LOCKED

```
~50-200 PRs analizados
~100-500 episodios del agente
~20-50 skills aprendidas
~10-30 archivos output generados
```

**Implicación técnica:** Escala chica v1. pgvector basta. No necesitamos Qdrant/Pinecone/Weaviate todavía.

### P2 — AI+infra cost <25% pilot revenue ✅ LOCKED (regla dura)

```
Pilot Light USD 3,500 → techo AI+infra USD 875
Pilot Pro   USD 8,000 → techo AI+infra USD 2,000
```

**Implicación técnica:**
- ❌ Descarta Pinecone managed, Weaviate Cloud, Neo4j Aura, RDS Multi-AZ
- ✅ Favorece PostgreSQL + extensiones, Redis self-hosted, S3 barato (B2/R2)

### P3 — Workspace isolation ✅ LOCKED

```
v1: (b) Schema-per-tenant en una sola PostgreSQL
v2: migrar a (c) Database-per-tenant cuando llegue cliente enterprise
```

**Implicación técnica:** PostgreSQL native schemas para isolation. Backup/restore por cliente con `pg_dump --schema=wks_X`.

### P4 — Encryption at rest ✅ LOCKED

```
(c) Híbrido — defense in depth:
   • App-layer: AES-GCM en columnas BYTEA (campos críticos)
   • Filesystem: LUKS encripta todo el disco
```

**Implicación técnica:** Cumple `mvp-scope §9.1` (app-layer explícito). Compliance-ready story para cliente enterprise. Resuelve D-005.

### P5 — Event Sourcing ✅ LOCKED (Híbrido)

```
ES en nodos donde es NATIVO:
   ✓ Nodo 2 Hipocampo (episodios = eventos por definición)
   ✓ Nodo 4 Skills (refuerzo dopaminérgico = stream)
   ✓ Audit chain (inmutabilidad obligatoria)

CRUD en el resto:
   ✓ Workspaces, Users, RBAC, API Keys
   ✓ KG state (AGE), Configs, Policies
```

**Implicación técnica:** Una sola PostgreSQL coexiste ES + CRUD. Sin Event Store externo (Kafka/EventStoreDB).

---

## 3. Estructura B+A — 4 bloques · 21 sub-temas

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 1 — STORAGE FOUNDATION (6 sub-temas)  ✅ LOCKED       ║
║   ──────────────────────────────────────────────────────       ║
║   1.1 BD relacional principal                                  ║
║   1.2 Knowledge Graph                                          ║
║   1.3 Vector store                                             ║
║   1.4 ORM                                                      ║
║   1.5 Migraciones                                              ║
║   1.6 Event Sourcing tablas                                    ║
║                                                                ║
║   BLOQUE 2 — MEMORY ARCHITECTURE (7 sub-temas)  ✅ LOCKED      ║
║   ────────────────────────────────────────────────────         ║
║   2.1 Memory framework                                         ║
║   2.2 Embeddings (modelo + dimensiones)                        ║
║   2.3 Vector indexing (HNSW/IVF/flat)                          ║
║   2.4 Memory tiers (working/short/long-term)                   ║
║   2.5 Forgetting strategy (Microglía)                          ║
║   2.6 CLS consolidation job (sleep cycle)                      ║
║   2.7 Mapeo Nodo Cerebral ↔ Tabla SQL                          ║
║                                                                ║
║   BLOQUE 3 — PERFORMANCE & ASYNC (4 sub-temas)   ⏳ PENDIENTE  ║
║   ──────────────────────────────────────────────────────       ║
║   3.1 Redis layer                                              ║
║   3.2 Background jobs                                          ║
║   3.3 Connection pooling                                       ║
║   3.4 Async patterns                                           ║
║                                                                ║
║   BLOQUE 4 — FILES & EXTERNAL DATA (3 sub-temas) ⏳ PENDIENTE  ║
║   ──────────────────────────────────────────────────────       ║
║   4.1 File storage                                             ║
║   4.2 S3 provider                                              ║
║   4.4 Backup strategy                                          ║
║                                                                ║
║   ⚠️ 4.3 MOVIDO a R4 Tools/MCP (D-010)                          ║
║      Razón: Git integration es decisión de wedge QA,            ║
║      no de plataforma For3s OS. R4 decide MCP servers.          ║
║                                                                ║
║   TOTAL R2: 20 sub-temas (era 21, -1 por D-010)                 ║
╚══════════════════════════════════════════════════════════════╝
```

### Modo operativo B+A

Cada bloque se trabaja con dos niveles de granularidad:

**Nivel B (bloques):** Cada bloque es una unidad temática cerrada. Se presenta su alcance, sub-temas y mapa de dependencias antes de arrancar.

**Nivel A (sub-temas):** Dentro de cada bloque, se debate sub-tema por sub-tema con la estructura ⑦:
1. ¿De qué trata? (con ejemplos concretos)
2. Mapeo al Grafo Maestro
3. Candidatos (3-6) con licencia, costo, alineación, anclas
4. Tabla comparativa
5. Tensión real
6. Recomendación
7. Decisión de Brian

Al cerrar un bloque se aplica el **Protocolo Bidireccional** (Estado_Sesion_Continuidad §3.1.quater) para identificar spillovers hacia `for3s-inter/`.

---

## 4. Resumen ejecutivo Bloque 1 — Storage Foundation

**Documento detallado:** [Ronda_02_Bloque_1_Storage_Foundation.md](Ronda_02_Bloque_1_Storage_Foundation.md)

### Las 6 decisiones LOCKED

```
1.1 BD relacional       → PostgreSQL 16+ (self-hosted Hetzner CX32)
1.2 Knowledge Graph     → Apache AGE (v1) → Neo4j (v3 si escala)
1.3 Vector store        → pgvector + HNSW (v1) → Qdrant (v3 si escala)
1.4 ORM                 → SQLAlchemy 2 + Pydantic v2 (separados)
1.5 Migraciones         → Single Alembic, multi-schema iteration
1.6 ES tables           → Diseño por aggregate (episodes_events,
                          skills_events, audit_events + state projections)
```

### Filosofía emergente del Bloque 1

```
"Centralizar en PostgreSQL todo lo que se pueda."

   1.1 Postgres como base
   1.2 KG dentro de Postgres (AGE)
   1.3 Vector dentro de Postgres (pgvector)
   1.4 ORM que habla nativamente con Postgres
   1.5 Migrations unificadas para todo Postgres
   1.6 ES tables dentro del mismo Postgres

→ UN SOLO sistema, UN SOLO backup, UN SOLO monitoring.
→ Cero servicios extra. Costo USD ~13/mes.
→ Open Core 100% puro (BSD/MIT/Apache 2/Public Domain).
```

### Stack final Bloque 1

```
┌──────────────────────────────────────────────────────┐
│   PostgreSQL 16+ (single instance, Hetzner CX32)      │
│   ~USD 13/mes — cabe en P2 <25% holgado               │
│                                                        │
│   EXTENSIONES:                                         │
│     ✓ AGE (Apache 2.0)        → Nodo 1 KG con Cypher  │
│     ✓ pgvector + HNSW (BSD)   → Nodo 2 Hipocampo      │
│     ✓ pgcrypto                → P4 encryption          │
│                                                        │
│   SCHEMA: shared                                       │
│     • workspaces, users, api_keys, RBAC (CRUD)         │
│     • audit_events (ES + hash chain)                   │
│     • AGE graph: conceptos globales                    │
│                                                        │
│   SCHEMA: wks_X (uno por cliente)                      │
│     • episodes_events + episodes_state (ES + CRUD)     │
│     • skills_events + skills_state (ES + CRUD)         │
│     • pgvector embeddings (HNSW index)                 │
│     • AGE subgraph: KG por workspace                   │
│     • outputs, configs (CRUD)                          │
│                                                        │
│   CAPA Python:                                         │
│     • SQLAlchemy 2 + asyncpg                           │
│     • Pydantic v2 para API                             │
│     • Alembic con env.py custom multi-schema           │
└──────────────────────────────────────────────────────┘
```

### Score honesto Bloque 1

```
8.9/10 — Sólido

Fortalezas:
   • Coherencia arquitectónica 9.5/10
   • Cost vs P2 10/10 (1.5% del techo)
   • Open Core compliance 10/10
   • Performance v1 a escala 10/10

Áreas de vigilancia:
   • Future-proofing 7.5/10 (deliberado por P5 híbrido)
   • Madurez Apache AGE 8.0/10 (joven vs Neo4j)
```

---

## 5. Status Bloques 2, 3, 4

### Bloque 2 — Memory Architecture ✅ CERRADO 2026-06-01

**Estatus:** ✅ LOCKED 7/7 sub-temas.

**Documento detallado:** [Ronda_02_Bloque_2_Memory_Architecture.md](Ronda_02_Bloque_2_Memory_Architecture.md)

**Las 7 decisiones LOCKED:**
- 2.1 Memory framework → Custom core + librerías composables
- 2.4 Memory tiers → 3 tiers clásico (Working + Short + Long)
- 2.2 Embeddings → Stella local `dunzhang/stella_en_400M_v5` @ 1024 dim + OpenAI fallback
- 2.3 Vector indexing → HNSW tuneado (m=16, ef_construction=128, ef_search=100, cosine)
- 2.5 Forgetting → Soft Delete + Decay + Archive (Microglía Nodo 6)
- 2.6 CLS Consolidation → Híbrido HDBSCAN + Claude Haiku 4.5 (~USD 37/mes)
- 2.7 Mapeo Nodo↔Tabla → Documentación oficial bilingüe

**Hardware LOCKED v1 (D-009):** Linux LOCAL de Brian (30 GB RAM, 1 TB disco, 24/7).
- ~~Original B1: Hetzner CX32~~
- ~~Update post-B2: Hetzner CX42~~
- **Actual D-009: Linux LOCAL — USD 0 hardware + ~USD 5/mes electricidad**
- Sobra holgado para v1-v3

**Nodos cerebrales servidos post-B2:** 10/11 (6 FULLY + 4 FOUNDATION). Solo Nodo 7 DMN pendiente (R5).

**Costo total v1 (B1+B2 + D-009):** USD ~43/mes (3.7% del techo Pilot Light → margen 96.3% para R3+R4).
- ~~Era USD ~63/mes con Hetzner~~ → sobrescrito por D-009 LOCAL

**Filosofía emergente del bloque:**
> "Custom core con librerías composables, mapeo 1:1 con el cerebro biológico, control total sobre la semántica."

**D-007 loggeado en `for3s-inter/07-operations/decision-log.md`.**

### Bloque 3 — Performance & Async ✅ CERRADO 2026-06-01

**Estatus:** ✅ LOCKED 4/4 sub-temas.

**Documento detallado:** [Ronda_02_Bloque_3_Performance_Async.md](Ronda_02_Bloque_3_Performance_Async.md)

**Las 4 decisiones LOCKED:**
- 3.1 Redis layer → Valkey scope mínimo (BSD-3 fork de Redis)
- 3.2 Background jobs → Arq async-native (MIT, mismo autor que Pydantic v2)
- 3.3 Connection pooling → pgbouncer + asyncpg + redis-py (ISC + Apache + MIT)
- 3.4 Async patterns → asyncio + anyio + 7 patterns LOCKED explícitos

**Servicios extra de infra:** 0 (Valkey + pgbouncer viven en mismo CX42)

**Procesos systemd v1:**
1. PostgreSQL 16 (B1)
2. pgbouncer (B3 3.3 — pool 30, transaction mode, puerto 6432)
3. Valkey (B3 3.1 — scope mínimo, 256 MB, puerto 6379)
4. FastAPI worker (uvicorn + asyncio + anyio)
5. Arq worker (async-native + AsyncStellaWrapper)

**Uso RAM v1:** ~4 GB de 16 GB disponibles (holgura 75%)

**Costo incremental B3:** USD 0 (todo gratis, vive en CX42 ya pagado)

**Filosofía emergente del bloque:**
> "Foundation de escalabilidad con scope mínimo y patterns LOCKED."

**D-008 loggeado en `for3s-inter/07-operations/decision-log.md`.**

### Bloque 4 — Files & External Data ✅ CERRADO 2026-06-01

**Estatus:** ✅ LOCKED 3/3 sub-temas (4.3 movido a R4 vía D-010).

**Documento detallado:** [Ronda_02_Bloque_4_Files_External.md](Ronda_02_Bloque_4_Files_External.md)

**Las 3 decisiones LOCKED:**
- 4.1 File storage → Filesystem local + Postgres metadata
- 4.2 S3 provider → NO S3 v1 (defer a v2-v3)
- 4.4 Backup strategy → Local USB + Cloudflare R2 offsite (3-2-1 rule)
- ⏭️ 4.3 → MOVIDO a R4 Tools/MCP (D-010)

**Características críticas Backup 4.4:**
- 3-2-1 rule satisfecho (3 copias, 2 medios, 1 offsite)
- Encryption end-to-end (age + LUKS)
- RPO 24h / RTO 30 min local / RTO 2-4 hrs R2
- Retención compliance: 7 daily + 4 weekly + 12 monthly
- Free tier R2 cubre v1 (~3-5 GB)

**Compliance B2B enterprise ready** desde día 1.

**D-011 loggeado en `for3s-inter/07-operations/decision-log.md`.**

⭐ **ESTE BLOQUE CIERRA R2 — DATA LAYER 100%** (20/20 sub-temas LOCKED).

---

## 6. Cobertura del Grafo Maestro

### Nodos servidos por R2 (incluyendo futuros bloques)

```
NODO                            BLOQUE 1   BLOQUE 2   BLOQUE 3   BLOQUE 4
─────────────────────────────────────────────────────────────────────────
Nodo 1 KG (Neocorteza)          ✅ host     ✅ uso      —          —
Nodo 2 Hipocampo                ✅ host     ✅ uso      —          —
Nodo 3 PFC                      ⏳ R5       🟡 working —          —
Nodo 4 Skills (Ganglios)        ✅ host     ✅ uso      —          —
Nodo 5 Ganglios Basales          —          ✅ def      —          —
Nodo 6 Microglía                 —          ✅ def(2.5) ✅ jobs    —
Nodo 7 DMN                       —          —          —          —
Nodo 8 Amígdala                 ✅ CRUD     —          —          —
Nodo 9 Pattern Separation       ✅ host     ✅ uso      —          —
Nodo 10 CLS                      —          ✅ def(2.6) ✅ jobs    —
Nodo 11 Neuromoduladores        ✅ CRUD     —          —          —

R2 completo cubrirá 9/11 nodos.
Quedarán Nodo 3 PFC y Nodo 7 DMN para R3 (Model/LLM) y R5 (Orchestration).
```

### Pilares — Cobertura por R2

```
Pilar 1 — Seguridad E2E           ✅ Bloque 1 (workspace iso + audit + encrypt)
Pilar 2 — Escalabilidad por nodo  🟡 foundation B1, refinada B3 (pool + cache)
Pilar 3 — Autonomía Generativa    🟡 foundation B1, lógica en R3-R5
```

### Anclas LOCKED — Status por R2

```
1.D Dedicated SaaS  ✅ ✅ ✅ Una Postgres por instalación
2.B Open Core       ✅ ✅ ✅ Todas licencias BSD/MIT/Apache 2/PD
3.D Equipo pequeño  ✅ ✅ ✅ 0 servicios extra hasta ahora
```

---

## 7. Riesgos legítimos aceptados

5 riesgos identificados al cierre de Bloque 1, todos conscientes y planeables:

```
1. Apache AGE es joven (5 años vs Neo4j 18 años)
   → Performance grafos grandes menor.
   → Mitigación: migración planeada a Neo4j en v3.
   → Cypher portable = queries no se pierden.

2. Postgres como SPOF/bottleneck único
   → Centralización tiene costo de coordinación.
   → Mitigación: connection pooling (3.3) limita daño,
     DB-per-tenant (P3 v2) separa workspaces grandes.

3. ES Híbrido tiene deuda cognitiva permanente
   → Devs deben saber cuándo usar ES vs CRUD.
   → Mitigación: documentar decision flowchart explícito.
   → Code review estricto en PRs que toquen eventos.

4. HNSW es RAM-hungry
   → ~6MB por workspace v1, ~30GB a escala v2 (5M vectores).
   → Mitigación: monitor RAM desde día 1.
   → Scale-up CX32→CX52→CCX22 conforme RAM apriete.
   → Considerar IVFFlat o quantization en v2.

5. Memory framework no cerrado todavía
   → No es defecto, es feature de progresión.
   → Se resuelve en Bloque 2 sub-tema 2.1.
```

---

## 8. Spillover hacia for3s-inter/

Aplicando **Protocolo Bidireccional** (Estado_Sesion_Continuidad §3.1.quater):

### Spillovers escritos al cerrar Bloque 1 (2026-06-01)

```
✅ for3s-inter/07-operations/decision-log.md
   + D-005 (Tensión E2E resuelta vía P4 híbrido)
   + D-006 (Stack Data Layer LOCKED)

✅ for3s-inter/09-technical-architecture/ (carpeta nueva)
   + README.md con índice + bridge a Mente/
```

### Spillovers diferidos hasta cierre R2

```
⏳ for3s-inter/03-security/encryption-strategy.md
⏳ for3s-inter/03-security/data-handling-policy.md
⏳ for3s-inter/03-security/access-control-model.md
⏳ for3s-inter/05-finance/unit-economics.md
⏳ for3s-inter/09-technical-architecture/storage-foundation.md
⏳ for3s-inter/09-technical-architecture/memory-architecture.md
⏳ for3s-inter/09-technical-architecture/performance-async.md
⏳ for3s-inter/09-technical-architecture/files-external.md
```

Razón del diferimiento: las decisiones de Bloques 2-4 informarán y mejorarán estos documentos. Escribirlos ahora generaría re-trabajo.

---

## 9. Próximo paso

## 🎉 R2 — DATA LAYER 100% CERRADO

**Inmediato:** Arrancar **R3 — Model/LLM Layer**.

R3 decidirá:
- LLM principal para razonamiento del agente
- Routing entre Claude Opus / GPT-4o / Gemini
- Local LLM como fallback (Llama, Qwen)
- Estrategia multi-model
- Costos AI principales (margen 96.3% del techo P2 disponible)

**Bloques R2 completados:**
- ✅ Bloque 1 — Storage Foundation (6/6 sub-temas) — D-006
- ✅ Bloque 2 — Memory Architecture (7/7 sub-temas) — D-007
- ✅ Bloque 3 — Performance & Async (4/4 sub-temas) — D-008
- ✅ Bloque 4 — Files & External (3/3 sub-temas) — D-011 ⭐ CIERRA R2

**Decisiones cross-bloque R2:**
- D-005 — Tensión E2E vía P4 híbrido
- D-009 — Despliegue LOCAL Linux + Cloudflare Tunnel
- D-010 — Sub-tema 4.3 movido a R4 (Tools/MCP)

**Documentación COMPLETA R2 generada (cierre 2026-06-01):**
- ✅ Mente/Cuerpo/Ronda_02_Data_Layer.md (master + apéndice schema SQL)
- ✅ Mente/Cuerpo/Ronda_02_Bloque_1_Storage_Foundation.md
- ✅ Mente/Cuerpo/Ronda_02_Bloque_2_Memory_Architecture.md
- ✅ Mente/Cuerpo/Ronda_02_Bloque_3_Performance_Async.md
- ✅ Mente/Cuerpo/Ronda_02_Bloque_4_Files_External.md
- ✅ Mente/Cerebro/Mapeo_Nodo_Cerebral_Tabla_SQL.md (canónico)
- ✅ for3s-inter/09-technical-architecture/ (5 sub-docs: compute, storage, memory, perf, files)
- ✅ for3s-inter/07-operations/decision-log.md (D-005 → D-011)
- ✅ for3s-inter/03-security/ (encryption-strategy + data-handling + access-control)
- ✅ for3s-inter/05-finance/unit-economics.md
- ✅ Mente/Doc/Estado_Sesion_Continuidad.md (§3.1.bis → §3.1.nonies)

**Próximas rondas (R3-R10):**
- R3 — Model/LLM Layer (LLM principal)
- R4 — Tools/MCP Layer (incluye 4.3 trasladado)
- R5 — Orchestration (cierra Nodo 3 PFC + Nodo 7 DMN)
- R6 — Memory Stack extensiones
- R7 — Frontend / Channel
- R8 — Observability
- R9 — Security / Compliance (cierra Nodo 8 Amígdala)
- R10 — CI/CD / Deploy

---

## 10. Apéndice — Schema SQL completo consolidado (B1 + B2)

> **Propósito:** Schema SQL consolidado de todas las decisiones LOCKED en Bloques 1+2. Útil para implementación directa, code review, database design review.
> **Actualizado:** 2026-06-01 al cierre del Bloque 2.

### 10.1 Extensiones globales (1 vez al instalar Postgres)

```sql
-- GLOBAL migration (al instalar PostgreSQL 16)
CREATE EXTENSION IF NOT EXISTS vector;        -- B1 1.3 + B2 2.3
CREATE EXTENSION IF NOT EXISTS age;           -- B1 1.2
CREATE EXTENSION IF NOT EXISTS pgcrypto;      -- P4 encryption

-- Cargar AGE
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
```

### 10.2 Schema SHARED (un solo schema global)

```sql
-- ────────────────────────────────────────────────────────────
-- SCHEMA: shared
-- Almacena metadata global, audit chain, RBAC
-- ────────────────────────────────────────────────────────────

CREATE SCHEMA IF NOT EXISTS shared;

-- Workspaces (CRUD)
CREATE TABLE shared.workspaces (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    schema_name     TEXT NOT NULL UNIQUE,  -- wks_X
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    settings        JSONB NOT NULL DEFAULT '{}',
    encryption_key_id TEXT,  -- referencia a KMS (P4)
    UNIQUE (schema_name)
);

-- Users (CRUD)
CREATE TABLE shared.users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES shared.workspaces(id),
    email           CITEXT NOT NULL UNIQUE,
    name            TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RBAC (CRUD)
CREATE TABLE shared.roles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES shared.workspaces(id),
    name            TEXT NOT NULL CHECK (name IN ('owner', 'editor', 'viewer'))
);

CREATE TABLE shared.user_roles (
    user_id         UUID NOT NULL REFERENCES shared.users(id),
    role_id         UUID NOT NULL REFERENCES shared.roles(id),
    granted_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, role_id)
);

-- API Keys (CRUD)
CREATE TABLE shared.api_keys (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES shared.workspaces(id),
    key_hash        TEXT NOT NULL,
    name            TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    revoked_at      TIMESTAMPTZ
);

-- ────────────────────────────────────────────────────────────
-- AUDIT EVENTS (Event Sourcing + Hash Chain — Pilar 1 §6.4)
-- ────────────────────────────────────────────────────────────

CREATE TABLE shared.audit_events (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    workspace_id    UUID REFERENCES shared.workspaces(id),
    actor_id        UUID,
    action          TEXT NOT NULL,
    resource_type   TEXT NOT NULL,
    resource_id     TEXT,
    payload         JSONB NOT NULL DEFAULT '{}',
    previous_hash   BYTEA,
    event_hash      BYTEA NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Inmutabilidad (B1 1.6)
CREATE OR REPLACE FUNCTION shared.prevent_audit_mutation()
RETURNS TRIGGER AS $$ BEGIN
    RAISE EXCEPTION 'audit_events are immutable';
END $$ LANGUAGE plpgsql;

CREATE TRIGGER no_modify_audit_events
    BEFORE UPDATE OR DELETE ON shared.audit_events
    FOR EACH ROW EXECUTE FUNCTION shared.prevent_audit_mutation();

CREATE INDEX idx_audit_events_workspace_time
    ON shared.audit_events (workspace_id, created_at DESC);

-- AGE Knowledge Graph global
SELECT create_graph('shared_kg');
```

### 10.3 Schema TENANT (uno por workspace — replicado wks_A, wks_B, ...)

```sql
-- ────────────────────────────────────────────────────────────
-- SCHEMA: wks_{workspace_id}
-- Almacena episodios, skills, conceptos del cliente
-- ────────────────────────────────────────────────────────────

CREATE SCHEMA IF NOT EXISTS wks_X;

-- ────────────────────────────────────────────────────────────
-- EPISODES (Nodo 2 Hipocampo) — Event Sourcing
-- ────────────────────────────────────────────────────────────

CREATE TABLE wks_X.episodes_events (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    episode_id      UUID NOT NULL,
    event_type      TEXT NOT NULL,
    event_version   INT NOT NULL DEFAULT 1,
    payload         JSONB NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    sequence_number BIGINT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    UNIQUE (episode_id, sequence_number)
);

CREATE INDEX idx_episodes_events_aggregate
    ON wks_X.episodes_events (episode_id, sequence_number);

-- Inmutabilidad
CREATE TRIGGER no_modify_episodes_events
    BEFORE UPDATE OR DELETE ON wks_X.episodes_events
    FOR EACH ROW EXECUTE FUNCTION shared.prevent_audit_mutation();

-- ────────────────────────────────────────────────────────────
-- EPISODES STATE (projection — CRUD + Forgetting)
-- ────────────────────────────────────────────────────────────

CREATE TABLE wks_X.episodes_state (
    id                   UUID PRIMARY KEY,  -- = episode_id
    workspace_id         UUID NOT NULL,
    status               TEXT NOT NULL,
    steps_done           INT NOT NULL DEFAULT 0,
    duration_seconds     INT,

    -- Campos cifrados (P4 app-layer)
    context_encrypted    BYTEA,
    output_encrypted     BYTEA,

    -- Embeddings (B2 2.2 + 2.3)
    embedding            VECTOR(1024),
    embedding_model      TEXT NOT NULL DEFAULT 'stella:dunzhang_400M_v5@1024',

    -- Forgetting (B2 2.5)
    deleted_at           TIMESTAMPTZ,
    relevance_score      FLOAT NOT NULL DEFAULT 1.0,
    last_accessed_at     TIMESTAMPTZ DEFAULT now(),
    consolidated_to_kg   BOOLEAN NOT NULL DEFAULT false,
    legal_hold           BOOLEAN NOT NULL DEFAULT false,

    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- HNSW index (B2 2.3 — params tuneados)
CREATE INDEX idx_episodes_state_embedding
    ON wks_X.episodes_state
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

-- Partial index for active episodes (B2 2.5)
CREATE INDEX idx_episodes_state_active
    ON wks_X.episodes_state (last_accessed_at)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_episodes_state_consolidation
    ON wks_X.episodes_state (consolidated_to_kg, relevance_score)
    WHERE deleted_at IS NULL;

-- Cold storage (B2 2.5)
CREATE TABLE wks_X.episodes_archived (
    LIKE wks_X.episodes_state INCLUDING ALL,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    archive_reason TEXT
);
-- Sin índice HNSW en archived (cold storage, no se busca semánticamente)

-- ────────────────────────────────────────────────────────────
-- SKILLS (Nodo 4 Ganglios Basales) — Event Sourcing
-- ────────────────────────────────────────────────────────────

CREATE TABLE wks_X.skills_events (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    skill_id        UUID NOT NULL,
    event_type      TEXT NOT NULL,
    event_version   INT NOT NULL DEFAULT 1,
    payload         JSONB NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    sequence_number BIGINT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    UNIQUE (skill_id, sequence_number)
);

CREATE TRIGGER no_modify_skills_events
    BEFORE UPDATE OR DELETE ON wks_X.skills_events
    FOR EACH ROW EXECUTE FUNCTION shared.prevent_audit_mutation();

CREATE TABLE wks_X.skills_state (
    id                   UUID PRIMARY KEY,  -- = skill_id
    workspace_id         UUID NOT NULL,
    name                 TEXT NOT NULL,
    description          TEXT,
    code                 BYTEA,  -- cifrado P4

    -- Success tracking (Nodo 11 Neuromoduladores)
    success_count        INT NOT NULL DEFAULT 0,
    failure_count        INT NOT NULL DEFAULT 0,
    success_rate         FLOAT GENERATED ALWAYS AS (
        CASE WHEN (success_count + failure_count) = 0 THEN 0.0
        ELSE success_count::float / (success_count + failure_count) END
    ) STORED,

    -- Embeddings
    embedding            VECTOR(1024),
    embedding_model      TEXT NOT NULL DEFAULT 'stella:dunzhang_400M_v5@1024',

    -- Forgetting
    deleted_at           TIMESTAMPTZ,
    last_used_at         TIMESTAMPTZ,
    consolidated_to_kg   BOOLEAN NOT NULL DEFAULT false,

    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_skills_state_embedding
    ON wks_X.skills_state
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

CREATE INDEX idx_skills_state_success
    ON wks_X.skills_state (success_rate DESC)
    WHERE deleted_at IS NULL;

CREATE TABLE wks_X.skills_archived (
    LIKE wks_X.skills_state INCLUDING ALL,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    archive_reason TEXT
);

-- ────────────────────────────────────────────────────────────
-- CONCEPTS (Tier 3 — Nodo 1 KG) — CRUD + AGE
-- ────────────────────────────────────────────────────────────

CREATE TABLE wks_X.concepts (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    concept_type         TEXT NOT NULL,  -- pattern/risk/skill/etc.
    label                TEXT NOT NULL,
    description          TEXT,

    -- Embeddings de conceptos
    embedding            VECTOR(1024),
    embedding_model      TEXT NOT NULL DEFAULT 'stella:dunzhang_400M_v5@1024',

    -- Trazabilidad
    source_episode_ids   UUID[] NOT NULL DEFAULT '{}',
    cluster_size         INT,

    -- Refuerzo
    reinforced_count     INT NOT NULL DEFAULT 0,
    last_reinforced_at   TIMESTAMPTZ,

    -- Forgetting / esencialidad
    essential            BOOLEAN NOT NULL DEFAULT false,

    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_concepts_embedding
    ON wks_X.concepts
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

-- AGE subgraph por workspace
SELECT create_graph('wks_X_kg');

-- ────────────────────────────────────────────────────────────
-- OUTPUTS, CONFIGS (CRUD)
-- ────────────────────────────────────────────────────────────

CREATE TABLE wks_X.outputs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    episode_id      UUID REFERENCES wks_X.episodes_state(id),
    output_type     TEXT NOT NULL,
    content_encrypted BYTEA,  -- P4
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE wks_X.configs (
    key             TEXT PRIMARY KEY,
    value           JSONB NOT NULL,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ────────────────────────────────────────────────────────────
-- ALEMBIC version tracking (B1 1.5 multi-schema)
-- ────────────────────────────────────────────────────────────

CREATE TABLE wks_X.alembic_version (
    version_num TEXT NOT NULL PRIMARY KEY
);

-- ────────────────────────────────────────────────────────────
-- GRANTS RESTRINGIDOS (B1 1.6 defensa en profundidad)
-- ────────────────────────────────────────────────────────────

REVOKE UPDATE, DELETE ON wks_X.episodes_events FROM PUBLIC;
REVOKE UPDATE, DELETE ON wks_X.skills_events FROM PUBLIC;
REVOKE UPDATE, DELETE ON shared.audit_events FROM PUBLIC;

GRANT INSERT, SELECT ON wks_X.episodes_events TO for3s_app_role;
GRANT INSERT, SELECT ON wks_X.skills_events TO for3s_app_role;
GRANT INSERT, SELECT ON shared.audit_events TO for3s_app_role;

GRANT SELECT, INSERT, UPDATE, DELETE
    ON wks_X.episodes_state, wks_X.skills_state, wks_X.concepts,
       wks_X.outputs, wks_X.configs
    TO for3s_app_role;
```

### 10.4 Resumen de objetos del schema TENANT

```
TABLAS por workspace:
   episodes_events    (ES inmutable, Nodo 2)
   episodes_state     (projection CRUD + HNSW)
   episodes_archived  (cold storage forgetting)
   skills_events      (ES inmutable, Nodo 4)
   skills_state       (projection CRUD + HNSW)
   skills_archived    (cold storage forgetting)
   concepts           (Tier 3 KG, CRUD + HNSW)
   outputs            (CRUD)
   configs            (CRUD)
   alembic_version    (tracking migrations)

ÍNDICES HNSW por workspace:
   idx_episodes_state_embedding (m=16, ef_construction=128, cosine)
   idx_skills_state_embedding (mismo)
   idx_concepts_embedding (mismo)

AGE subgraph por workspace:
   wks_X_kg (Cypher queries scoped al workspace)
```

### 10.5 Función create_workspace (B1 1.5)

```sql
-- Pseudo-función Python que orquesta:
CREATE OR REPLACE FUNCTION create_workspace(p_workspace_id UUID, p_name TEXT)
RETURNS VOID AS $$
DECLARE
    v_schema_name TEXT := 'wks_' || replace(p_workspace_id::text, '-', '_');
BEGIN
    -- 1. CREATE SCHEMA
    EXECUTE format('CREATE SCHEMA IF NOT EXISTS %I', v_schema_name);

    -- 2. INSERT workspace en shared
    INSERT INTO shared.workspaces (id, name, schema_name)
    VALUES (p_workspace_id, p_name, v_schema_name);

    -- 3. (Alembic aplica TODAS las tenant migrations al schema nuevo)
    -- Esto se hace desde Python via alembic.command.upgrade

    -- 4. AGE subgraph
    PERFORM create_graph(v_schema_name || '_kg');

    -- 5. Audit
    INSERT INTO shared.audit_events
        (action, resource_type, resource_id, payload, event_hash)
    VALUES
        ('workspace:create', 'workspace', p_workspace_id::text,
         jsonb_build_object('schema', v_schema_name),
         digest('workspace_create_' || p_workspace_id::text, 'sha256'));
END;
$$ LANGUAGE plpgsql;
```

### 10.6 Estimación de tamaño por workspace v1

```
Volumen v1 (LOCKED P1):
   ~200 PRs analizados
   ~500 episodios
   ~50 skills
   ~30 outputs
   ~5,000 conceptos generados por CLS

Tamaño aproximado:
   episodes_events:     ~500 × 2 KB = 1 MB
   episodes_state:      ~500 × (1024 dim × 4B + metadata) = 3 MB
   episodes_archived:   crece con tiempo, soft delete primero
   skills_events:       ~50 × 1 KB = 50 KB
   skills_state:        ~50 × 5 KB = 250 KB
   concepts:            ~5,000 × 5 KB = 25 MB
   AGE graph:           ~10 MB
   ─────────────────────────────────────
   TOTAL por workspace: ~40 MB v1
   TOTAL 50 workspaces: ~2 GB v1

   Cabe holgado en Hetzner CX42 (160 GB SSD).
```