# Ronda 2 — Bloque 1: Storage Foundation

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
⚪ **Registro histórico** — se consulta, no se mantiene: partirlo falsearía lo que pasó.
**Migrated:** Cuerpo/Ronda_02_Bloque_1_Storage_Foundation.md → work/Ronda_02_Bloque_1_Storage_Foundation.md (2026-07-30, ADR-029)

## Purpose

Ronda 2 — Bloque 1: Storage Foundation


**Sub-documento detallado de R2 — Data Layer. Bloque 1 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-01
**Estatus:** ✅ LOCKED (6/6 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema)
**Documento padre:** [Ronda_02_Data_Layer.md](work/Ronda_02_Data_Layer.md)
**Sesión:** 2026-06-01

> ⚠️ **HARDWARE LOCKED REVISADO 2 VECES (última: 2026-06-01 via D-009)**
>
> Evolución de la decisión de hardware:
>
> 1. **B1 1.1 original:** Hetzner CX32 (8 GB RAM, ~USD 13/mes)
> 2. **B2 2.2 update:** Hetzner CX42 (16 GB RAM, ~USD 25/mes) — motivado por Stella embeddings local de 1.6 GB
> 3. **D-009 LOCKED (FINAL v1):** Linux LOCAL de Brian (30 GB RAM, 1 TB disco, 24/7) — USD 0 hardware + ~USD 5/mes electricidad + Cloudflare Tunnel free
>
> **Hardware vigente v1:** Linux LOCAL Brian (NO Hetzner cloud).
>
> Razón: Brian aclaró post-B3 que despliegue v1 es local. Stack técnico NO cambia (PostgreSQL + AGE + pgvector siguen idénticos), solo el host físico.
>
> Detalle completo: [decision-log.md D-009](../../for3s-inter/07-operations/decision-log.md)

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (licencias permisivas obligatorias)
- 3.D — Equipo pequeño (0 servicios extra preferido)

**Constraint LOCKED aplicado:**
- P2 — AI+infra <25% pilot revenue (USD 875 techo en Pilot Light)

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 1.1 — BD relacional principal](#3-sub-tema-11--bd-relacional-principal)
4. [Sub-tema 1.2 — Knowledge Graph](#4-sub-tema-12--knowledge-graph)
5. [Sub-tema 1.3 — Vector store](#5-sub-tema-13--vector-store)
6. [Sub-tema 1.4 — ORM](#6-sub-tema-14--orm)
7. [Sub-tema 1.5 — Migraciones (estrategia)](#7-sub-tema-15--migraciones-estrategia)
8. [Sub-tema 1.6 — Event Sourcing tablas](#8-sub-tema-16--event-sourcing-tablas)
9. [Stack final consolidado](#9-stack-final-consolidado)
10. [Arquitectura emergente — diagrama](#10-arquitectura-emergente--diagrama)
11. [Cobertura del Grafo Maestro](#11-cobertura-del-grafo-maestro)
12. [Costo total v1](#12-costo-total-v1)
13. [Evaluación honesta 8.9/10](#13-evaluación-honesta-8910)
14. [Riesgos legítimos aceptados](#14-riesgos-legítimos-aceptados)
15. [Implicaciones en bloques siguientes](#15-implicaciones-en-bloques-siguientes)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 1 — STORAGE FOUNDATION                                ║
║   6 sub-temas LOCKED el 2026-06-01                             ║
║                                                                ║
║   1.1 BD relacional       → PostgreSQL 16+ (Hetzner CX32)      ║
║   1.2 Knowledge Graph     → Apache AGE → Neo4j v3 si escala    ║
║   1.3 Vector store        → pgvector + HNSW → Qdrant v3        ║
║   1.4 ORM                 → SQLAlchemy 2 + Pydantic v2          ║
║   1.5 Migraciones         → Single Alembic, multi-schema       ║
║   1.6 ES tables           → Por aggregate (no tabla única)      ║
║                                                                ║
║   Servicios extra:        0                                    ║
║   Costo incremental:      USD 0 sobre Postgres base             ║
║   Costo total v1:         ~USD 13/mes (Hetzner CX32)            ║
║   Licencias:              100% open-source permisivas           ║
║   Nodos servidos:         8/11 del Grafo Maestro                ║
║   Anclas respetadas:      3/3 (100%)                            ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

Las 6 decisiones convergen en una sola filosofía no planeada de antemano pero coherente al final:

> **"Centralizar en PostgreSQL todo lo que se pueda."**

```
1.1 Postgres como base
   ↓
1.2 KG dentro de Postgres vía Apache AGE
   ↓
1.3 Vector dentro de Postgres vía pgvector
   ↓
1.4 ORM que habla nativamente con Postgres (SQLAlchemy 2)
   ↓
1.5 Migrations unificadas para todo Postgres (Alembic)
   ↓
1.6 Event Sourcing tablas dentro del mismo Postgres
```

### Por qué esta filosofía importa

**Para equipo pequeño (Ancla 3.D):** UN solo sistema, UN solo backup, UN solo monitoring, UN solo set de credenciales. Comparar con stacks típicos:

```
Stack típico de competidor:
   • PostgreSQL (relacional)
   • Neo4j (KG)
   • Qdrant (vectors)
   • Redis (cache)
   • Kafka (events)
   • S3 (files)
   = 6 sistemas distintos, 6 backups, 6 monitorings.

Stack For3s v1:
   • PostgreSQL con extensiones (relacional + KG + vector + ES)
   • (Redis vendrá en Bloque 3)
   = 1 sistema en Bloque 1. 1 backup. 1 monitoring.
```

**Para constraint P2 <25%:** Costo Hetzner CX32 con todo = ~USD 13/mes. Vs típico que excede USD 200/mes solo en infra.

**Para Open Core (Ancla 2.B):** Todas licencias permisivas (BSD/MIT/Apache 2/Public Domain). Sin BSL ni GPL-viral. Versión community sin caveats legales.

---

## 3. Sub-tema 1.1 — BD relacional principal

### Decisión LOCKED

```
PostgreSQL 16+ (self-hosted Hetzner CX32 ~USD 13/mes)
```

### Contexto

Una BD relacional es el "tabla maestra" donde viven los datos estructurados del sistema: metadata (workspaces, users), configuración (api_keys, roles), event store (con P5 ES híbrido), audit chain (Pilar 1), y donde se instalan las extensiones críticas (Apache AGE para Nodo 1, pgvector para Nodo 2, pgcrypto para P4).

### Mapeo al Grafo Maestro

- **Pilar 1 — Seguridad E2E:** Workspace boundaries via schemas, audit_events table, RBAC.
- **Pilar 2 — Escalabilidad:** Sharding por workspace, foundation para connection pooling.
- **Hosting de Nodos:** Nodo 1 (AGE), Nodo 2 (pgvector), Nodo 4 (Skills tables), Nodo 9 (HNSW).

### Candidatos evaluados

```
A) PostgreSQL 16+         ✅ ELEGIDO
B) SQLite con FTS5        ❌ No tiene Apache AGE ni schemas multi-tenant
C) MySQL / MariaDB        ❌ Sin equivalente serio a pgvector / AGE
D) CockroachDB            ❌ BSL no es OSI open-source; sin extensiones Postgres
```

### Tabla comparativa

```
┌────────────────────────┬──────────┬─────────┬──────────┬──────────┐
│ Criterio               │ Postgres │ SQLite  │ MySQL    │ Cockroach│
├────────────────────────┼──────────┼─────────┼──────────┼──────────┤
│ pgvector / vector ext  │   ✅✅✅  │ parcial │   ❌    │    ❌    │
│ Apache AGE / KG        │   ✅✅✅  │   ❌    │   ❌    │    ❌    │
│ Schemas nativos (P3)   │   ✅✅✅  │   ❌    │ parcial │    ✅    │
│ RLS multi-tenant       │   ✅✅   │   ❌    │   ❌    │    ✅    │
│ Async Python tooling   │   ✅✅✅  │   ✅    │   ✅    │    ✅    │
│ Costo operacional v1   │   ✅✅✅  │  ✅✅✅  │   ✅✅   │    ❌    │
│ Compliance B2B reading │   ✅✅✅  │   ❌    │   ✅✅   │    ✅✅  │
│ Open-source puro       │   ✅✅✅  │  ✅✅✅  │  ⚠️/✅   │    ❌    │
│ Hostea Nodos del Grafo │   4/4    │   0/4   │   0/4    │   0/4    │
└────────────────────────┴──────────┴─────────┴──────────┴──────────┘
   PostgreSQL gana 9 de 10 criterios para For3s OS.
```

### Razones de la decisión

1. **Único candidato que hostea Apache AGE + pgvector** → habilita Nodo 1 + Nodo 2 + Nodo 9 en una sola BD
2. Schemas nativos = P3 (schema-per-tenant) directo, sin librerías raras
3. RLS multi-tenant nativo (defensa adicional Pilar 1)
4. Open-source puro (PostgreSQL License BSD) = compatible 2.B Open Core
5. Async Python tooling de primera clase (asyncpg, psycopg3)
6. Costo USD ~13/mes Hetzner CX32 = holgado en P2 (<25%)
7. Compliance B2B la espera ver
8. WAL archiving + point-in-time recovery para audit serio
9. LISTEN/NOTIFY (puede reducir necesidad de Redis para algunos casos)

### Path futuro

```
v1: PostgreSQL 16 self-hosted Hetzner CX32 (~USD 13/mes)
v2: evaluar managed (Supabase, Railway) cuando >5 clientes
v3: read replicas + DB-per-tenant para clientes enterprise
```

---

## 4. Sub-tema 1.2 — Knowledge Graph

### Decisión LOCKED

```
Apache AGE (v1) → Neo4j (v3 si escala)
```

**Esta fue la decisión MÁS tensionada del bloque.**

### Contexto

Un Knowledge Graph guarda información donde lo importante son **las relaciones entre cosas**, no las cosas mismas. Para For3s QA esto habilita razonamiento multi-hop crítico:

```
EJEMPLO CONCRETO:
   "Encuentra PRs que tocan código que históricamente
    ha causado bugs reportados por clientes enterprise"

   Con SQL puro: queries anidados de pesadilla
   Con KG (Cypher):
      MATCH (pr:PR)-[:TOUCHES]->(file:File)
            -[:HISTORICALLY_CAUSED]->(bug:Bug)
            -[:REPORTED_BY]->(client:Client {tier:'enterprise'})
      RETURN pr
```

### Mapeo al Grafo Maestro

- **Nodo 1 — Knowledge Graph (Neocorteza semántica):** Razón de ser
- **Nodo 4 — Ganglios Basales (Skills):** Skills viven en contexto grafo
- **Pilar 3 — Autonomía Generativa:** Razonamiento multi-hop diferencia For3s de wrapper LLM

### Candidatos evaluados

```
A) Apache AGE             ✅ ELEGIDO (extensión Postgres, Apache 2.0)
B) Neo4j Community         ⚠️ GPL v3 viral, +1 servicio
C) Memgraph               ❌ BSL, +1 servicio, RAM-heavy
D) ArangoDB               ❌ BSL desde 2024, AQL no Cypher
E) NO KG dedicado          ❌ Pierde Nodo 1 del Grafo Maestro
```

### Tabla comparativa

```
┌────────────────────────┬─────────┬────────┬─────────┬────────┬─────────┐
│ Criterio               │ AGE     │ Neo4j  │ Memgraph│ Arango │ NO-KG   │
├────────────────────────┼─────────┼────────┼─────────┼────────┼─────────┤
│ Open-source puro       │  ✅✅✅  │  ⚠️    │   ❌   │   ❌   │  ✅✅✅  │
│ Costo operación v1     │ +USD 0  │+$15-30 │ +$20-50│+$15-30 │ +USD 0  │
│ Servicios extra        │   0     │   +1   │   +1   │   +1   │   0     │
│ Cypher (estándar)      │  ✅✅   │ ✅✅✅  │  ✅✅  │   ❌   │   ❌    │
│ Joins KG↔SQL nativos   │ ✅✅✅   │  ❌    │   ❌   │   ❌   │   ✅    │
│ Backup unificado c/SQL │  ✅✅✅  │  ❌    │   ❌   │   ❌   │  ✅✅✅  │
│ Compatible Anclas      │   3/3   │  2/3   │   1/3  │  1/3   │   3/3   │
└────────────────────────┴─────────┴────────┴─────────┴────────┴─────────┘
```

### Razones de la decisión

1. **CERO servicios extra** → respeta 3.D Equipo pequeño
2. **CERO costo incremental** → respeta P2 <25%
3. Apache 2.0 → respeta 2.B Open Core sin caveats
4. **Joins NATIVOS KG↔SQL** → único candidato que permite
5. Backup UNIFICADO con Postgres
6. Cypher = lenguaje grafo más usado del mundo (skill transferible)
7. Suficiente performance para v1-v2 (escala 5-10M nodos)

### Tensión real

```
COMPLEJIDAD OPERACIONAL  vs  POTENCIA TÉCNICA
   • Neo4j = más potencia + más complejidad
   • AGE   = menos potencia + cero complejidad
   • NO-KG = cero complejidad + sub-óptimo arquitectónico

AGE es el punto donde alineación arquitectónica se encuentra
con pragmatismo de equipo pequeño.
```

### Path futuro

```
v1: Apache AGE en mismo Postgres
v3: migrar a Neo4j si:
    • Volumen >5M nodos
    • Queries multi-hop >5 saltos rutinarias
    • Cliente enterprise lo exige específicamente
```

---

## 5. Sub-tema 1.3 — Vector store

### Decisión LOCKED

```
pgvector + HNSW (v1) → Qdrant (v3 si escala)
```

**Esta fue la segunda decisión más tensionada del bloque.**

### Contexto

Un vector store guarda embeddings (representaciones numéricas) de cosas como texto, código, conceptos. La magia: vectores similares = significados similares. Permite búsqueda semántica (no por palabras exactas sino por significado).

Operaciones críticas:
- INSERT vector
- Nearest Neighbor Search (k-NN)
- Filtered search (combinar similitud + metadata)
- Pattern Separation (distinguir episodios "casi idénticos")

### Mapeo al Grafo Maestro

- **Nodo 2 — Hipocampo (memoria episódica):** Uso principal
- **Nodo 9 — Pattern Separation:** Función hipocampal crítica
- **Nodo 1 — KG semántico:** Búsqueda semántica complementaria al graph traversal
- **Nodo 4 — Skills:** Embeddings de contextos de aprendizaje

### Candidatos evaluados

```
A) pgvector               ✅ ELEGIDO (extensión Postgres, BSD)
B) Qdrant                 ⚠️ Excelente Rust DB pero +1 servicio
C) Weaviate               ❌ +1 servicio pesado, GraphQL overhead
D) Pinecone               ❌ Closed source, viola 2.B Open Core
E) Chroma                 ❌ Joven, ecosystem chico
F) Milvus                 ❌ Overkill para v1 (arquitectura distribuida)
```

### Tabla comparativa

```
┌────────────────────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Criterio               │pgvector │ Qdrant  │Weaviate │Pinecone │ Chroma  │ Milvus  │
├────────────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ Open-source puro       │  ✅✅✅  │  ✅✅✅  │  ✅✅✅  │   ❌    │  ✅✅✅  │  ✅✅✅  │
│ Costo operación v1     │ +USD 0  │ +$5/mes │+$10/mes │ $70+/mo │ +$5/mes │ $30+/mo │
│ Servicios extra        │   0     │   +1    │   +1    │ cloud   │   +1    │   +1    │
│ Joins KG↔Vector        │  ✅✅✅  │   ❌    │   ❌    │   ❌    │   ❌    │   ❌    │
│ ACID transactions      │  ✅✅✅  │   ❌    │   ❌    │   ❌    │   ❌    │   ❌    │
│ Backup unificado c/SQL │  ✅✅✅  │   ❌    │   ❌    │   ❌    │   ❌    │   ❌    │
│ Performance v1 (chico) │  ✅✅✅  │  ✅✅✅  │  ✅✅✅  │  ✅✅✅  │  ✅✅   │  ✅✅✅  │
│ Compatible Anclas      │   3/3   │  2/3    │   2/3   │   0/3   │   2.5/3 │   2/3   │
└────────────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
```

### Razones de la decisión

1. CERO servicios extra → respeta 3.D Equipo pequeño
2. CERO costo incremental → respeta P2 <25%
3. BSD → respeta 2.B Open Core sin caveats
4. **JOINS NATIVOS vector ↔ KG ↔ SQL en UNA query** (único)
5. ACID transactions cross-system (raro en vector stores)
6. Backup UNIFICADO con AGE y SQL
7. Workspace isolation con schemas (consistente con P3)
8. Performance suficiente para 1000x el tamaño v1
9. **COHERENCIA con 1.2 AGE** — filosofía unificada

### Capacidades técnicas confirmadas

```
• Dimensiones soportadas: hasta 16,000 (modelos OpenAI OK)
• Índices: HNSW (rápido + memoria), IVFFlat (compacto)
• Distance metrics: cosine, L2, inner product, L1, hamming
• Filtros: cualquier WHERE clause SQL nativo
• Transacciones ACID: SÍ
```

### Tensión real

```
SIMPLICIDAD ARQUITECTÓNICA  vs  PERFORMANCE A FUTURO
   • pgvector → UN servicio para SQL + Graph + Vector
   • Qdrant   → DOS servicios separados

Coherencia con 1.2 (AGE en Postgres) decidió.
```

### Path futuro

```
v1: pgvector con índice HNSW
v3: migrar a Qdrant si:
    • Volumen >5M vectores por workspace
    • Latencia <10ms crítica
    • Quantization necesaria por memoria
    • Cliente enterprise lo exige
```

---

## 6. Sub-tema 1.4 — ORM

### Decisión LOCKED

```
SQLAlchemy 2 + Pydantic v2 (separados)
```

### Contexto

Un ORM (Object-Relational Mapper) es el traductor entre código Python y PostgreSQL. Convierte filas en objetos Python y viceversa. Para For3s NO es CRUD simple — debe soportar pgvector custom types, Apache AGE Cypher pass-through, JSONB queries complejas, multi-schema dinámico, Event Sourcing patterns.

### Mapeo al Grafo Maestro

ORM no materializa nodos directamente — es capa de abstracción. Pero afecta cómo se sirven:
- Nodo 1 KG → ORM debe permitir Cypher pass-through
- Nodo 2 Hipocampo → ORM debe soportar pgvector operators
- Pilar 1 Seguridad → ORM previene SQL injection automáticamente
- Pilar 2 Escalabilidad → ORM coordina connection pooling

### Candidatos evaluados

```
A) SQLAlchemy 2 + Pydantic v2  ✅ ELEGIDO (estándar industria 19 años)
B) SQLModel                     ⚠️ Magia frágil en casos complejos
C) Tortoise ORM                 ❌ Sin soporte pgvector serio
D) Sin ORM (raw SQL)            ❌ Reinventar plumbing manualmente
```

### Tabla comparativa

```
┌────────────────────────┬─────────────┬─────────┬──────────┬─────────┐
│ Criterio               │ SQLAlchemy 2│SQLModel │ Tortoise │ Raw SQL │
├────────────────────────┼─────────────┼─────────┼──────────┼─────────┤
│ Soporte pgvector       │    ✅✅✅    │  ✅✅   │   ❌    │  ✅✅✅  │
│ Soporte Apache AGE     │   ✅ (raw)  │ ✅ (raw)│ parcial  │  ✅✅✅  │
│ Pydantic v2 integration│   manual    │ ✅✅✅  │   ⚠️    │ manual  │
│ Multi-schema (P3)      │    ✅✅✅    │  ✅✅   │   ⚠️    │ manual  │
│ Alembic migrations     │    ✅✅✅    │  ✅✅✅  │ Aerich  │   ❌    │
│ Madurez                │ 19 años     │ 4 años  │ 7 años   │ 8 años  │
│ Listeners para hooks   │    ✅✅✅    │  ✅✅   │   ⚠️    │   ❌    │
│ Compatible Anclas      │     3/3     │   3/3   │  2.5/3   │  2/3    │
└────────────────────────┴─────────────┴─────────┴──────────┴─────────┘
```

### Razones de la decisión

1. **ESTÁNDAR DE FACTO en Python** — 19 años madurez
2. Soporte OFICIAL pgvector vía pgvector-python
3. Permite raw SQL fácilmente → Cypher para AGE OK
4. Multi-schema (P3) soportado nativamente
5. **Alembic = mismo autor** → integración perfecta (1.5)
6. Type-safe con `Mapped[T]` (Python 3.12 idiomático)
7. **Listeners → hooks naturales para ES events (1.6)**
8. Ecosystem masivo + Stack Overflow gigante
9. Battle-tested a escala extrema
10. Hire fácil (todos los Pythonistas serios lo conocen)

### Patrón For3s

```python
# Pseudocódigo:

# Truth de BD (SQLAlchemy)
class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    workspace_id: Mapped[UUID] = mapped_column(ForeignKey(...))

# Truth de API (Pydantic)
class UserOut(BaseModel):
    id: UUID
    email: str
    model_config = ConfigDict(from_attributes=True)

# Conversión: UserOut.model_validate(orm_user) → 1 línea
```

### Por qué NO SQLModel

```
Para For3s, donde tendremos modelos COMPLEJOS:
   • ES events con triggers
   • Apache AGE queries (Cypher) embebidas
   • pgvector custom types con operadores
   • Multi-schema dinámico
   • Encryption híbrida campos BYTEA
   • Audit chain con hash linking

En cada uno, SQLModel "cae" a SQLAlchemy por debajo.
Si SQLAlchemy es necesario debajo, mejor usarlo directo.
```

---

## 7. Sub-tema 1.5 — Migraciones (estrategia)

### Decisión LOCKED

```
Single Alembic, multi-schema iteration
```

**Dado SQLAlchemy 2 LOCKED en 1.4, Alembic es la herramienta obvia.** La decisión real era la ESTRATEGIA multi-schema.

### Contexto

Una migración es un script versionado de schema. Para For3s el desafío único es multi-tenancy con schema-per-tenant (P3):

```
ESCENARIO:
   Postgres tiene schemas: shared, wks_A, wks_B, ..., wks_Z
   Cambia columna en tabla que existe en TODOS los wks_X.
   Pregunta: ¿migration se corre 1 vez o N veces?
```

### Mapeo al Grafo Maestro

- **Pilar 1 — Seguridad E2E:** Migraciones respetan workspace isolation, cuidado con audit_events (hash chain)
- **Pilar 2 — Escalabilidad:** N clientes = N schemas = automatización obligatoria
- **Ancla 3.D — Equipo pequeño:** Sin estrategia clara → bottleneck operacional

### Estrategias evaluadas

```
A) Single Alembic, multi-schema iteration  ✅ ELEGIDA
B) Multiple Alembic environments            ⚠️ 2x configuración
C) Template-based schema cloning             ⚠️ Confunde problemas distintos
D) Migraciones manuales SQL puras            ❌ Reinventar Alembic mal
```

### Tabla comparativa

```
┌─────────────────────────┬──────────┬────────────┬──────────┬─────────┐
│ Criterio                │ A:Single │ B:Multiple │C:Template│ D:Raw   │
├─────────────────────────┼──────────┼────────────┼──────────┼─────────┤
│ Autogenerate            │  ✅✅✅   │  ✅✅✅     │  ✅✅    │   ❌    │
│ Tracking de versión     │  ✅✅✅   │  ✅✅✅     │  ✅✅    │ manual  │
│ Multi-schema (P3)       │  ✅✅✅   │  ✅✅✅     │   ⚠️     │ manual  │
│ Rollback                │  ✅✅✅   │  ✅✅✅     │  ✅✅    │   ❌    │
│ Mantenimiento ongoing   │   baja   │   alta     │   media  │  alta   │
│ Migración a existentes  │  ✅✅✅   │  ✅✅      │   ⚠️     │ manual  │
│ Deploy unificado        │  ✅✅✅   │   ⚠️      │  ✅✅    │ manual  │
└─────────────────────────┴──────────┴────────────┴──────────┴─────────┘
```

### Razones de la decisión

1. UNA FUENTE DE VERDAD para todas las migrations
2. Autogenerate funciona perfecto con SQLAlchemy 2
3. Multi-schema P3 soportado vía env.py custom
4. Onboarding workspace = script "create_workspace" que crea schema + aplica todas las migrations
5. Rollback global posible
6. Deploy unificado — un solo `alembic upgrade head`
7. Funciona hasta ~1000 workspaces sin problema
8. Hire fácil — Alembic es estándar industria

### Estrategia operacional detallada

```
/alembic/
   env.py            ← itera schemas dinámicamente
   versions/
      001_*.py
      002_*.py

Tipos de migrations marcadas con scope:
   • SHARED-ONLY (workspaces, users, api_keys)
   • TENANT-ONLY (episodes, skills, KG subgraph)
   • GLOBAL (CREATE EXTENSION age, vector, pgcrypto)

Función onboarding:
   def create_workspace(workspace_id):
       1. CREATE SCHEMA wks_{workspace_id}
       2. Inicializar alembic_version table
       3. Aplicar TODAS las tenant migrations
       4. INSERT en shared.workspaces

Migration safety:
   • Online por default (CREATE INDEX CONCURRENTLY)
   • Transacciones donde es posible
   • Locks cortos
```

---

## 8. Sub-tema 1.6 — Event Sourcing tablas

### Decisión LOCKED

```
Diseño por aggregate (no tabla única + JSONB)
```

Este sub-tema **aterriza P5 (ES Híbrido)** en tablas concretas. P5 lockeó la decisión filosófica (ES en Hipocampo/Skills/Audit, CRUD resto). 1.6 lockea la **forma física** de esas tablas.

### Contexto

Un sistema ES tiene 3 piezas:

1. **Event Store** — Tabla append-only con TODOS los eventos. Solo INSERT, nunca UPDATE/DELETE.
2. **State Projections** — Tablas "normales" derivadas de los eventos. Vistas materializadas para lectura rápida.
3. **Projection Handlers** — Código que escucha eventos y actualiza state tables.

7 decisiones interdependientes a tomar:

```
1. Forma del Event Store    (tabla única vs por aggregate)
2. Formato del payload      (JSONB vs BYTEA vs híbrido)
3. Versioning de eventos    (campo version, type+version, upcasting)
4. Hash chain del audit     (previous_hash explícito, externo, Merkle)
5. Inmutabilidad enforcement (triggers, grants, defensa profundidad)
6. Identidad de eventos     (UUID v4, UUID v7, BIGSERIAL)
7. Particionado             (sin, por workspace, por mes)
```

### Mapeo al Grafo Maestro

- **Nodo 2 — Hipocampo:** episodes_events es el corazón
- **Nodo 4 — Ganglios Basales (Skills):** skills_events
- **Nodo 10 — CLS:** consolidation_events (futuro)
- **Microglía:** forgetting_events (futuro)
- **Pilar 1 — Seguridad §6.4:** Audit chain criptográfica REQUERIDA

### Candidatos evaluados

```
A) Diseño Minimalista (tabla única + JSONB)  ❌ Pierde separación por nodo
B) Diseño por Aggregate                      ✅ ELEGIDO
C) Diseño con Snapshots desde día 1           ❌ Premature optimization
```

### Tabla comparativa

```
┌─────────────────────────┬──────────┬──────────┬──────────┐
│ Criterio                │ A: Único │ B: Por   │ C: B +   │
│                         │ tabla    │ aggregate│ Snapshots│
├─────────────────────────┼──────────┼──────────┼──────────┤
│ Simplicidad mental      │  ✅✅✅   │  ✅✅    │   ⚠️     │
│ Escalabilidad por nodo  │   ⚠️     │  ✅✅✅   │  ✅✅✅   │
│ Performance v1 (chico)  │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │
│ Audit chain limpia      │   ⚠️     │  ✅✅✅   │  ✅✅✅   │
│ Retention granular      │   ❌    │  ✅✅✅   │  ✅✅✅   │
│ Code overhead v1        │   bajo   │  medio   │   alto   │
│ Refactor a siguiente    │  doloroso│   fácil  │   N/A    │
└─────────────────────────┴──────────┴──────────┴──────────┘
```

### Decisiones concretas dentro de B

```
DECISIÓN 1 — Forma del store
   ✅ Tablas por aggregate:
      episodes_events, skills_events, audit_events
      + state projections (episodes_state, skills_state)

DECISIÓN 2 — Payload
   ✅ JSONB queryable + metadata JSONB
   ✅ Campos críticos (P4 híbrido) en columnas BYTEA cifradas

DECISIÓN 3 — Versioning
   ✅ event_version INT en cada fila
   ✅ Upcasting en Python al replayear

DECISIÓN 4 — Hash chain
   ✅ SOLO en audit_events (no en business events)
   ✅ previous_hash + event_hash explícitos
   ✅ Verificación independiente posible

DECISIÓN 5 — Inmutabilidad
   ✅ Trigger PostgreSQL rechaza UPDATE/DELETE
   ✅ Rol app con grants restringidos (defensa en profundidad)

DECISIÓN 6 — Identidad
   ✅ UUID v7 (time-ordered, mejor indexing)
   ✅ sequence_number BIGINT por aggregate (orden estricto)

DECISIÓN 7 — Particionado
   ✅ SIN particionado v1 — schema-per-tenant ya particiona
   ⏳ v2: evaluar partition por mes para retention
```

### Esquema concreto

```sql
-- HIPOCAMPO (Nodo 2)
CREATE TABLE episodes_events (
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

-- GANGLIOS BASALES (Nodo 4)
CREATE TABLE skills_events (
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

-- AUDIT CHAIN (Pilar 1, schema shared)
CREATE TABLE shared.audit_events (
    id              UUID PRIMARY KEY DEFAULT gen_uuid_v7(),
    workspace_id    UUID,
    actor_id        UUID,
    action          TEXT NOT NULL,
    resource_type   TEXT NOT NULL,
    resource_id     TEXT,
    payload         JSONB NOT NULL DEFAULT '{}',
    previous_hash   BYTEA,
    event_hash      BYTEA NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- STATE PROJECTIONS
CREATE TABLE episodes_state ( ... );
CREATE TABLE skills_state ( ... );

-- INMUTABILIDAD
CREATE OR REPLACE FUNCTION prevent_event_mutation()
RETURNS TRIGGER AS $$ BEGIN
  RAISE EXCEPTION 'Events are immutable';
END $$ LANGUAGE plpgsql;

CREATE TRIGGER no_update_episodes_events
  BEFORE UPDATE OR DELETE ON episodes_events
  FOR EACH ROW EXECUTE FUNCTION prevent_event_mutation();
-- (repetir en skills_events y audit_events)
```

### Razones de la decisión

1. **RESPETA P5 Híbrido** — tablas por nodo cerebral
2. Audit chain AISLADA — Pilar 1 puro
3. Performance escala por aggregate independientemente
4. Schema evolution localizada (cambias episodes sin tocar skills)
5. Retention policy granular (audit eterno, episodes purgables)
6. Inmutabilidad por trigger explícito
7. Cabe en P2 <25% (es Postgres ya elegido)
8. Future-proof sin sobre-ingeniería
9. Refactor a snapshots en v2 = trivial

---

## 9. Stack final consolidado

```
COMPONENTE                  DECISIÓN                            COSTO
──────────────────────────────────────────────────────────────────────
BD relacional               PostgreSQL 16+                       USD ~13/mo
Knowledge Graph             Apache AGE (extensión)               USD 0
Vector store                pgvector + HNSW (extensión)          USD 0
Encryption                  pgcrypto (extensión)                  USD 0
ORM                         SQLAlchemy 2 + Pydantic v2            USD 0
Migrations                  Alembic con env.py custom             USD 0
Event Sourcing              Tablas por aggregate                  USD 0
──────────────────────────────────────────────────────────────────────
TOTAL incremental v1                                              USD ~13/mo
```

### Multi-tenancy materializado

```
PostgreSQL instance:
   ├── schema: shared
   │     • workspaces, users, api_keys, roles, permissions (CRUD)
   │     • audit_events (ES + hash chain)
   │     • AGE graph: conceptos globales
   │     • alembic_version
   │
   ├── schema: wks_A  (cliente A)
   │     • episodes_events + episodes_state (ES + CRUD)
   │     • skills_events + skills_state (ES + CRUD)
   │     • pgvector embeddings (HNSW index)
   │     • AGE subgraph: KG por workspace
   │     • outputs, configs (CRUD)
   │     • alembic_version_wks_A
   │
   ├── schema: wks_B  (cliente B) — mismo patrón
   ├── schema: wks_C  (cliente C) — mismo patrón
   └── ...
```

### Seguridad consolidada

```
✓ Schema-per-tenant (P3 isolation)
✓ Encryption híbrida (P4: app-layer AES-GCM + LUKS filesystem)
✓ Inmutabilidad de eventos (triggers Postgres)
✓ Hash chain en audit_events (tamper-evident)
✓ Rol app con grants restringidos (defensa en profundidad)
✓ RLS multi-tenant disponible (defensa adicional v2)
```

---

## 10. Arquitectura emergente — diagrama

```
                  ┌──────────────────────────────┐
                  │   APLICACIÓN PYTHON           │
                  │                                │
                  │   FastAPI + asyncio           │
                  │      │                         │
                  │      ▼                         │
                  │   SQLAlchemy 2 (async)        │
                  │      │                         │
                  │      ▼                         │
                  │   asyncpg driver              │
                  │      │                         │
                  └──────│─────────────────────────┘
                         │
                         ▼
   ┌────────────────────────────────────────────────────┐
   │   PostgreSQL 16 (single instance, Hetzner CX32)     │
   │                                                      │
   │   Extensiones cargadas:                              │
   │     • age          (Cypher para KG)                  │
   │     • vector       (HNSW para embeddings)            │
   │     • pgcrypto     (helpers AES-GCM)                 │
   │                                                      │
   │   ┌──────────────────────────────────────────┐      │
   │   │ schema: shared                            │      │
   │   │   tablas CRUD:                            │      │
   │   │     workspaces, users, api_keys,          │      │
   │   │     roles, permissions, configs           │      │
   │   │   tabla ES:                               │      │
   │   │     audit_events (hash chain inmutable)   │      │
   │   │   AGE graph: conceptos globales            │      │
   │   └──────────────────────────────────────────┘      │
   │                                                      │
   │   ┌──────────────────────────────────────────┐      │
   │   │ schema: wks_A                             │      │
   │   │   tablas ES:                              │      │
   │   │     episodes_events                       │      │
   │   │     skills_events                         │      │
   │   │   tablas state (projections CRUD):        │      │
   │   │     episodes_state, skills_state          │      │
   │   │   pgvector embeddings + HNSW index        │      │
   │   │   AGE subgraph: KG del workspace          │      │
   │   │   outputs, configs (CRUD)                 │      │
   │   └──────────────────────────────────────────┘      │
   │                                                      │
   │   ┌──────────────────────────────────────────┐      │
   │   │ schema: wks_B, wks_C, ...                 │      │
   │   │   mismo patrón replicado por workspace    │      │
   │   └──────────────────────────────────────────┘      │
   │                                                      │
   │   ┌──────────────────────────────────────────┐      │
   │   │ Storage físico:                           │      │
   │   │   • LUKS encripta disco completo (P4 fs)  │      │
   │   │   • WAL archiving + PITR para audit       │      │
   │   └──────────────────────────────────────────┘      │
   └────────────────────────────────────────────────────┘
```

---

## 11. Cobertura del Grafo Maestro

### Nodos servidos por Bloque 1

```
NODO                          BLOQUE 1                STATUS
────────────────────────────────────────────────────────────────
Nodo 1 KG (Neocorteza)        Apache AGE              ✅ HOSTEADO
Nodo 2 Hipocampo              pgvector + episodes_ES  ✅ HOSTEADO
Nodo 3 PFC                    (R5 lo cubre)           ⏳
Nodo 4 Skills                 skills_events ES        ✅ HOSTEADO
Nodo 5 Ganglios Basales        skills_state            ✅ HOSTEADO (parcial)
Nodo 6 Microglía              (Bloque 2 lo define)    ⏳
Nodo 7 DMN                    (R5)                    ⏳
Nodo 8 Amígdala               CRUD foundation         ✅ FOUNDATION
Nodo 9 Pattern Separation     pgvector HNSW           ✅ HOSTEADO
Nodo 10 CLS                   (Bloque 2 + R3)         ⏳
Nodo 11 Neuromoduladores      CRUD foundation         ✅ FOUNDATION

Bloque 1 cubre 5 nodos directos + 3 parciales = 8/11 (73%)
Resto se cubre en Bloque 2 + R3-R5.
```

### Pilares — Cobertura por Bloque 1

```
Pilar 1 — Seguridad E2E
   ✓ Workspace isolation por schemas (P3)
   ✓ Encryption híbrida (P4: app + filesystem)
   ✓ Audit chain inmutable con hash (1.6)
   ✓ Inmutabilidad por triggers Postgres
   ✓ Grants restringidos al rol app
   → Estado: BIEN servido. Nivel SOC2-ready desde día 1.

Pilar 2 — Escalabilidad por nodo
   ✓ Foundation correcta (schema-per-tenant + multi-schema migrations)
   🟡 Connection pooling pendiente (3.3 Bloque 3)
   🟡 Cache pendiente (3.1 Bloque 3)

Pilar 3 — Autonomía Generativa
   🟡 Storage listo, lógica en R3-R5
```

### Anclas LOCKED — Verificación post-Bloque 1

```
1.D Dedicated SaaS:  ✅ PostgreSQL por instalación (Hetzner)
2.B Open Core:       ✅ Todas licencias permisivas:
                        • PostgreSQL License (BSD)
                        • Apache 2.0 (AGE)
                        • PostgreSQL License (pgvector)
                        • MIT (SQLAlchemy, Pydantic, Alembic)
3.D Equipo pequeño:  ✅ Una sola BD reduce ops dramatically
                        0 servicios extra hasta ahora
```

---

## 12. Costo total v1

```
Hetzner CX32 (4 vCPU, 8 GB RAM, 80 GB SSD):     USD ~13/mes
PostgreSQL 16 (self-hosted):                     USD 0
Apache AGE extension:                            USD 0
pgvector extension:                              USD 0
SQLAlchemy 2 + Pydantic v2 + Alembic:            USD 0
─────────────────────────────────────────────────────────────
TOTAL infra Bloque 1:                            USD ~13/mes
```

### Vs constraint P2 <25%

```
Pilot Light USD 3,500 (3 semanas)
   25% techo = USD 875
   Infra Bloque 1 = USD ~13 (3 semanas) = USD 9.75
   → CONSUME 1.1% del techo

Pilot Pro USD 8,000 (3 semanas)
   25% techo = USD 2,000
   → CONSUME 0.5% del techo

CONCLUSIÓN: Infra holgada por 100x.
   Margen disponible para LLM/embeddings APIs.
```

---

## 13. Evaluación honesta 8.9/10

Brian pidió evaluación brutal. Score promedio: **8.9/10**.

### Calificación por dimensión

```
┌──────────────────────────────────────┬─────────┬────────────┐
│ Dimensión                            │ Score   │ Análisis   │
├──────────────────────────────────────┼─────────┼────────────┤
│ Alineación con Grafo Maestro         │  9.0/10 │ Muy alta   │
│ Coherencia interna (las 6 decisiones)│  9.5/10 │ Excelente  │
│ Pragmatismo para equipo pequeño      │  9.0/10 │ Realista   │
│ Costo (vs P2 <25%)                   │ 10.0/10 │ Holgado    │
│ Open Core compliance                 │ 10.0/10 │ Perfecto   │
│ Future-proofing                      │  7.5/10 │ Razonable* │
│ Velocidad a primer pilot             │  8.0/10 │ Buena      │
│ Riesgo de lock-in                    │  8.5/10 │ Bajo       │
│ Madurez tecnológica                  │  8.0/10 │ Aceptable  │
│ Performance v1 (a tu escala)         │ 10.0/10 │ Sobra      │
├──────────────────────────────────────┼─────────┼────────────┤
│ PROMEDIO PONDERADO                   │  8.9/10 │ Sólido     │
└──────────────────────────────────────┴─────────┴────────────┘

* Future-proofing más bajo es DELIBERADO (P5 híbrido evitó ES completo).
```

### Vs Hermes (referencia de agente AI en producción)

```
For3s es MÁS sofisticado donde TIENE que serlo:
   • Multi-tenant vs single user (Hermes)
   • Compliance B2B vs personal (Hermes)
   • Audit forensic vs logs simples (Hermes)
   • Hash chain inmutable vs logs (Hermes)

For3s es MENOS modular en un punto:
   • Vector provider único (pgvector) vs Hermes que tiene
     interfaz pluggable (Qdrant/Chroma/pgvector swap).
   • Mitigable con abstracción en Bloque 2 sub-tema 2.1.

Decisiones óptimas para escenarios distintos.
Ninguno está "menos avanzado" — escenarios diferentes.
```

---

## 14. Riesgos legítimos aceptados

5 riesgos identificados conscientemente. Ninguno es bloqueante.

### Riesgo 1 — Apache AGE es joven (5 años vs Neo4j 18)

```
PROBLEMA:
   AGE rinde ~30-50% de Neo4j en grafos grandes (>5M nodos).
   Features Cypher incompletos. Sin Neo4j GDS equivalente.
   Comunidad ~1/100 de Neo4j.

IMPACTO v1:    NO (escala chica)
IMPACTO v3:    POSIBLEMENTE (cuando volumen grande)

MITIGACIÓN:
   • Migración planeada AGE → Neo4j (Cypher portable)
   • Vigilar latencia p95 queries grafo
   • Vigilar cliente que pida algoritmos GDS
```

### Riesgo 2 — Postgres como SPOF/bottleneck único

```
PROBLEMA:
   Una sola Postgres = SPOF compartido entre:
   tablas + AGE + pgvector + ES events + audit.
   "Noisy neighbor" dentro del mismo Postgres.

IMPACTO v1:    NO (Hetzner CX32 holgado)
IMPACTO v3:    POSIBLEMENTE (workspaces grandes)

MITIGACIÓN:
   • Connection pooling (3.3) limita daño
   • Database-per-tenant (P3 v2) separa workspaces grandes
   • Read replicas en v3 si necesario
   • Monitor CPU sostenido >70%
   • Monitor lock contention en audit_events
```

### Riesgo 3 — ES Híbrido tiene deuda cognitiva

```
PROBLEMA:
   Devs deben aprender CUÁNDO usar ES vs CRUD.
   Schema evolution asimétrico (CRUD trivial, ES doloroso).
   Versionado de eventos (upcasting) es trampa para bugs.
   Sin internalizar la distinción → eventos mal modelados.

IMPACTO v1:    SÍ (deuda desde día 1)
IMPACTO v3:    SÍ (escala con team)

MITIGACIÓN REQUERIDA:
   • Documentar EXPLÍCITAMENTE qué va a ES y qué a CRUD
   • Decision flowchart en docs internos
   • Code review estricto en PRs de eventos
   • Onboarding doc para devs nuevos
```

### Riesgo 4 — HNSW es RAM-hungry

```
PROBLEMA:
   HNSW carga índice completo en RAM.
   Cálculo: 5M vectores × 1536 dims × 4 bytes × 1.5 overhead
            = ~30 GB RAM solo para índice vector.

IMPACTO v1:    NO (Hetzner CX32: 8 GB holgado)
IMPACTO v2:    SÍ (planear scale-up)

MITIGACIÓN:
   • Memory monitor desde día 1
   • Scale-up plan: CX32 → CX52 (16GB) → CCX22 (32GB)
   • Considerar IVFFlat para reducir RAM (menos performance)
   • Quantization pgvector 0.7+ (scalar, binary)
   • Eventualmente Qdrant con quantization 4-32x
```

### Riesgo 5 — Memory framework no cerrado

```
PROBLEMA:
   Bloque 1 dice "tendremos episodes_events" pero NO cómo
   el agente decide qué guardar como evento.
   ¿Cada step LLM? ¿Cada batch? ¿Cada sesión?

IMPACTO v1:    NO INMEDIATAMENTE
IMPACTO BLOQUE 2: SÍ (lo resuelve 2.1 + 2.4)

NO ES DEFECTO — ES PROGRESIÓN.
Mencionado para no confundir "Storage completo" con
"semántica de uso definida".
```

---

## 15. Implicaciones en bloques siguientes

### Para Bloque 2 — Memory Architecture

```
✅ pgvector ya disponible para sub-tema 2.2 (embeddings)
✅ HNSW ya elegido, 2.3 confirma o revisa con datos RAM
✅ episodes_events + skills_events ya definidas para 2.4 (tiers)
✅ Audit chain inmutable disponible (excepción para 2.5 forgetting)
✅ Apache AGE disponible para 2.6 (CLS consolidation → KG)
✅ 2.7 mapeo nodo↔tabla puede empezar con base de Bloque 1
```

### Para Bloque 3 — Performance & Async

```
✅ Postgres connection pooling decisión obvia (asyncpg pool + pgbouncer)
✅ Background jobs (3.2) deberán correr CLS (2.6) y forgetting (2.5)
✅ Redis (3.1) puede usar Postgres LISTEN/NOTIFY como alternativa
```

### Para Bloque 4 — Files & External Data

```
✅ Backup strategy (4.4) ya tiene base: pg_dump --schema=wks_X
✅ pg_dump cubre TODO (relacional + AGE + vectors) en UN comando
```

### Para R3+ — Model/LLM, MCP, Orchestration, etc.

```
✅ Schema episodes_events servirá como source-of-truth para
   training data en R3 (fine-tuning embeddings, GEPA, etc.)
✅ Audit chain disponible para compliance reports en R9
```

---

## Cierre del Bloque 1

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ BLOQUE 1 — STORAGE FOUNDATION CERRADO                     ║
║                                                                ║
║   6/6 sub-temas LOCKED                                         ║
║   Score: 8.9/10 (evaluación honesta)                           ║
║   Riesgos legítimos: 5 identificados, todos planeables          ║
║   Spillover: D-005, D-006 logged + 09-tech-arch creado          ║
║                                                                ║
║   Próximo: Bloque 2 — Memory Architecture                      ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

Related: `docs/plan-v1-to-v2-migration.md` (migrado desde `work/Ronda_02_Bloque_1_Storage_Foundation.md`).
