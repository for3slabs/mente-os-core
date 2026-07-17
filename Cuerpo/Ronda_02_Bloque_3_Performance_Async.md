# Ronda 2 — Bloque 3: Performance & Async

**Sub-documento detallado de R2 — Data Layer. Bloque 3 de 4.**

**Owner:** Brian López
**Fecha de cierre:** 2026-06-01
**Estatus:** ✅ LOCKED (4/4 sub-temas)
**Modo de debate:** B+A (bloque + sub-tema por sub-tema)
**Documento padre:** [Ronda_02_Data_Layer.md](Ronda_02_Data_Layer.md)
**Sesión:** 2026-06-01

**Anclas estratégicas aplicadas:**
- 1.D — Dedicated SaaS
- 2.B — Open Core (licencias permisivas obligatorias)
- 3.D — Equipo pequeño (preferir simplicidad operacional)

**Constraints LOCKED aplicados:**
- P2 — AI+infra <25% pilot revenue
- P3 — Schema-per-tenant (afecta connection pooling)
- P5 — ES híbrido (afecta workers y jobs)

**Decisiones previas que afectan B3:**
- R1: Python 3.12 + asyncio + anyio + FastAPI
- B1 1.1: PostgreSQL 16
- B1 1.4: SQLAlchemy 2 + asyncpg
- B2 2.2: Stella embeddings (síncrono)
- B2 2.5: forgetter workers (nightly/weekly/monthly)
- B2 2.6: CLS consolidator (nightly + on-demand)

> ⚠️ **COSTO HARDWARE ACTUALIZADO POR D-009 (2026-06-01)**
>
> Este documento menciona "Hetzner CX42 ~USD 25/mes" y "USD ~63/mes total" en varias secciones (cálculos hechos antes de D-009). El **costo real vigente v1** es:
>
> - **Hardware:** Linux LOCAL Brian (30 GB RAM, 1 TB disco) — USD 0
> - **Electricidad 24/7:** USD ~5/mes
> - **Cloudflare Tunnel:** USD 0 (free tier)
> - **Dominio for3s.ai:** USD ~$1/mes
> - **Claude Haiku CLS:** USD ~37/mes (sin cambio)
> - **TOTAL v1 corregido:** USD ~43/mes (no USD ~63/mes)
>
> Cifras "USD ~63/mes" y "CX42" son **históricas** (sobrescritas por D-009). Stack técnico (Valkey+Arq+pgbouncer+asyncio+anyio) NO cambia.
>
> Fuente: [decision-log.md D-009](../../for3s-inter/07-operations/decision-log.md)

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Filosofía emergente del bloque](#2-filosofía-emergente-del-bloque)
3. [Sub-tema 3.1 — Redis layer (Valkey)](#3-sub-tema-31--redis-layer-valkey)
4. [Sub-tema 3.2 — Background jobs (Arq)](#4-sub-tema-32--background-jobs-arq)
5. [Sub-tema 3.3 — Connection pooling (pgbouncer)](#5-sub-tema-33--connection-pooling-pgbouncer)
6. [Sub-tema 3.4 — Async patterns (asyncio + anyio)](#6-sub-tema-34--async-patterns-asyncio--anyio)
7. [Stack final consolidado](#7-stack-final-consolidado)
8. [Arquitectura emergente — diagrama runtime](#8-arquitectura-emergente--diagrama-runtime)
9. [Cobertura del Grafo Maestro](#9-cobertura-del-grafo-maestro)
10. [Costo total actualizado](#10-costo-total-actualizado)
11. [Exploraciones futuras NO adoptadas v1](#11-exploraciones-futuras-no-adoptadas-v1)
12. [Implicaciones en bloques siguientes](#12-implicaciones-en-bloques-siguientes)

---

## 1. Resumen ejecutivo

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   BLOQUE 3 — PERFORMANCE & ASYNC                               ║
║   4 sub-temas LOCKED el 2026-06-01                             ║
║                                                                ║
║   3.1 Redis layer        → Valkey scope mínimo (BSD-3)         ║
║   3.2 Background jobs    → Arq async-native (MIT)              ║
║   3.3 Connection pooling → pgbouncer + asyncpg (ISC + Apache)  ║
║   3.4 Async patterns     → asyncio + anyio + patterns LOCKED   ║
║                                                                ║
║   Servicios extra añadidos: +2 (Valkey + pgbouncer)            ║
║   Costo incremental B3:     USD 0 (todo gratis, vive en CX42)  ║
║   Costo total v1 (B1+B2+B3): USD ~63/mes (sin cambio)          ║
║   % techo Pilot Light:      5.4% (vs 25% permitido)            ║
║   Nodos servidos B3:        TRANSVERSAL (refuerza foundation)  ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. Filosofía emergente del bloque

```
"Foundation de escalabilidad con scope mínimo y patterns LOCKED."
```

Las 4 decisiones convergen en patrones consistentes:

```
1. SCOPE MÍNIMO desde día 1 (3.1)
   → Valkey solo para 2 propósitos (job queue + rate limit)
   → No cache ni shared memory hasta justificación real

2. ASYNC-NATIVE end-to-end (3.2 + 3.4)
   → Arq match con FastAPI async
   → Patterns asyncio + anyio coherentes
   → Stella sync wrapper único punto de fricción

3. PREPARACIÓN ESCALA sin pagar AHORA (3.3)
   → pgbouncer desde día 1 evita refactor v2
   → Setup overhead trivial (~2-4 hrs)
   → Vale dividendos cuando llegue 2do cliente

4. OPEN CORE PURO (todas las decisiones)
   → BSD-3 (Valkey), MIT (Arq), ISC (pgbouncer), PSF (asyncio)
   → CERO licencias problemáticas
   → Coherencia con B1 1.1 (rechazo de CockroachDB BSL)

5. CERO SERVICIOS EXTRA INFRA
   → Valkey y pgbouncer viven en mismo CX42
   → No instancias separadas
   → Respeta 3.D Equipo pequeño
```

### Por qué esta filosofía importa

**Para Pilar 2 Escalabilidad:** foundation correcta evita rebuilds futuros. pgbouncer + Valkey + Arq son la base sobre la que TODO el sistema escala.

**Para Pilar 3 Autonomía:** workers Arq corren autónomamente (CLS, Microglía) sin bloquear API. El agente "duerme" de noche sin interrumpir clientes activos.

**Para Anclas:** todas respetadas. Open Core puro, scope mínimo, foundation que escala.

---

## 3. Sub-tema 3.1 — Redis layer (Valkey)

### Decisión LOCKED

```
Valkey self-hosted, scope MÍNIMO (BSD-3 fork de Redis)
```

### Contexto

Redis cambió licencia en marzo 2024 (SSPL/RSALv2 — no es OSI). Valkey es el fork comunitario BSD-3 respaldado por Linux Foundation + AWS + Google + Oracle. API 100% compatible drop-in replacement.

### Mapeo al Grafo Maestro

- **Pilar 2 Escalabilidad:** cache + coordinación foundation
- **Nodo 6 Microglía:** Valkey como job broker para workers
- **Nodo 10 CLS:** mismo (broker para consolidator)
- **Pilar 1 Seguridad:** rate limiting compliance B2B

### Candidatos evaluados

```
A) NO Redis (defer a v2)      ❌ Limita 3.2 a APScheduler
B) Valkey                     ✅ ELEGIDO — BSD-3 puro
C) DragonflyDB                ❌ BSL viola 2.B Open Core
D) Redis OSS 7.4+             ❌ SSPL/RSALv2 viola 2.B
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A: NO     │B: Valkey │C: Dragon │D: Redis  │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Open-source puro         │   N/A    │  ✅✅✅   │   ❌    │   ❌    │
│ Licencia                 │   N/A    │   BSD-3  │   BSL    │ SSPL/RSAL│
│ Costo v1 mensual         │   $0     │   ~$0    │   ~$0    │   ~$0    │
│ Servicios extra          │    0     │    +1    │    +1    │    +1    │
│ RAM extra                │    0     │ ~100 MB  │ ~150 MB  │ ~100 MB  │
│ Cache nativo             │   ❌    │   ✅✅   │  ✅✅✅   │   ✅✅   │
│ Pub/Sub                  │   ❌    │   ✅✅   │   ✅✅   │   ✅✅   │
│ Job queue backend        │   ❌    │   ✅✅   │   ✅✅   │   ✅✅   │
│ Rate limiting nativo     │ in-proc  │   ✅✅   │   ✅✅   │   ✅✅   │
│ Compatible Anclas        │   3/3    │   3/3    │   1/3    │   1/3    │
│ Future-proof             │   ⚠️     │  ✅✅✅   │   ⚠️    │   ❌    │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **BSD-3 puro** → respeta 2.B Open Core sin caveats
2. **Scope mínimo** → respeta 3.D Equipo pequeño
3. **Da flexibilidad a 3.2** (jobs framework no se limita a APScheduler)
4. **Rate limiting B2B compliance** desde día 1
5. **Performance overhead mínimo** (~100 MB RAM en CX42)
6. **Respaldo institucional** Linux Foundation + AWS + Google
7. **Cero servicios extra infra** (vive en mismo CX42)

### Configuración LOCKED v1

```ini
# valkey.conf
listen_addr        = 127.0.0.1
port               = 6379
maxmemory          = 256mb
maxmemory-policy   = allkeys-lru
save               = 900 1
save               = 300 10
appendonly         = yes
appendfsync        = everysec
bind               = 127.0.0.1   # solo localhost
requirepass        = <generated>
```

### Usos LOCKED v1 (scope MÍNIMO)

```
✅ Job queue backend (para 3.2)
   • forgetter + CLS workers usan Valkey como broker
   • Permite elegir Arq en sub-tema 3.2

✅ Rate limiting (compliance B2B)
   • Middleware FastAPI con redis-py async
   • Counters con TTL automático
   • Protege API antes de pilot enterprise
```

### Usos DIFERIDOS a v2

```
⏳ Cache de embeddings frecuentes
   Trigger: latencia HNSW degrada >50ms p95 sostenido

⏳ Working memory shared cross-procesos
   Trigger: multi-worker FastAPI (multi-instance load balancing)

⏳ Pub/sub coordinación inter-workers
   Trigger: workers de distintos workspaces interfieren
```

### Cliente Python

```
redis-py (oficial, async-first, Valkey compatible)
```

### Módulo for3s_os

```
for3s_os/infrastructure/
├── valkey_client.py    → ConnectionPool factory + Redis()
├── rate_limiter.py     → FastAPI middleware
└── job_broker.py       → adapter para Arq (3.2)
```

### Path futuro

```
v1: Valkey single-instance + scope mínimo (job queue + rate limit)
v2: añadir cache embeddings si HNSW degrada
v3: evaluar Sentinel/Cluster si SLA enterprise lo exige
```

---

## 4. Sub-tema 3.2 — Background jobs (Arq)

### Decisión LOCKED

```
Arq (async-native Python, MIT, Redis/Valkey backend)
```

### Contexto

For3s OS necesita 2 tipos de jobs:
- **Programados (cron):** CLS nightly, Microglía nightly/weekly/monthly
- **On-demand:** force consolidate, onboarding workspace, re-embed futuro

Arq es framework async-native creado por Samuel Colvin (mismo autor de Pydantic v2 LOCKED en R1).

### Mapeo al Grafo Maestro

- **Nodo 10 CLS:** job nocturno principal (consolidator)
- **Nodo 6 Microglía:** 3 schedules (forgetter workers)
- **Pilar 2 Escalabilidad:** background async no bloquea API
- **Pilar 3 Autonomía:** sleep cycle requiere ejecución autónoma

### Candidatos evaluados

```
A) Arq                     ✅ ELEGIDO — async-native + Pydantic
B) RQ                      ⚠️ Sync-first, async bolt-on
C) Celery                  ⚠️ OVERKILL v1, setup complejo
D) APScheduler             ❌ In-process, bloquea FastAPI
E) Dramatiq                ⚠️ LGPL menos limpio que MIT
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A: Arq    │B: RQ     │C: Celery │D: APSch. │E: Dram.  │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Open-source              │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │   ⚠️    │
│ Licencia                 │   MIT    │  BSD-2   │  BSD-3   │   MIT    │  LGPL-3  │
│ Async-first nativo       │  ✅✅✅   │   ⚠️    │   ⚠️    │   ✅✅   │   ⚠️    │
│ Cron scheduling          │  ✅✅✅   │ +addon   │  ✅✅✅   │  ✅✅✅   │   ✅✅   │
│ Pydantic v2 integration  │  ✅✅✅   │  manual  │  manual  │  manual  │  manual  │
│ Setup time               │ ~30 min  │ ~30 min  │ ~1-2 días│ ~10 min  │ ~1 hora  │
│ Curva de aprendizaje     │  baja    │  baja    │  alta    │  baja    │  media   │
│ Jobs ON-DEMAND           │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │   ⚠️    │  ✅✅✅   │
│ Match con FastAPI/async  │  ✅✅✅   │   ⚠️    │   ⚠️    │   ✅✅   │   ⚠️    │
│ Compatible Anclas        │   3/3    │   3/3    │   3/3    │   3/3    │  2.5/3   │
│ Match Pydantic v2 LOCKED │  ✅✅✅   │   ⚠️    │   ⚠️    │   ⚠️    │   ⚠️    │
│ Match Valkey LOCKED 3.1  │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │   N/A    │  ✅✅✅   │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **Async-first NATIVO** (match perfecto Python 3.12 + asyncio)
2. **Mismo autor que Pydantic v2** (Samuel Colvin, coherencia stack)
3. **Setup ~30 min** vs ~1-2 días Celery
4. **Cron scheduling nativo** (sintaxis limpia)
5. **MIT puro** → respeta 2.B Open Core
6. **Cero servicios extra** (Valkey ya LOCKED 3.1)
7. **Cubre 100% necesidades v1** (CLS + Microglía + on-demand)

### Configuración LOCKED v1

```python
# for3s_os/jobs/worker.py
from arq import cron
from arq.connections import RedisSettings

class WorkerSettings:
    redis_settings = RedisSettings(
        host=os.getenv('VALKEY_HOST', '127.0.0.1'),
        port=int(os.getenv('VALKEY_PORT', '6379')),
        password=os.getenv('VALKEY_PASSWORD'),
    )

    functions = [
        cls_consolidate_all_workspaces,
        cls_consolidate_workspace,
        microglia_nightly_workspace,
        microglia_weekly_workspace,
        microglia_monthly_workspace,
        onboarding_create_workspace,
    ]

    cron_jobs = [
        cron(cls_consolidate_all_workspaces,
             hour=2, minute=0),                     # 2 AM diario
        cron(microglia_nightly_all,
             hour=3, minute=0),                     # 3 AM diario
        cron(microglia_weekly_all,
             hour=4, minute=0, weekday='sun'),      # Dom 4 AM
        cron(microglia_monthly_all,
             hour=5, minute=0, day=1),              # Día 1 mes 5 AM
    ]

    max_jobs = 10
    job_timeout = 600       # 10 min default
    keep_result = 3600      # 1h TTL
    max_tries = 3
    retry_jobs = True
```

### Patrón retry con backoff

```python
from arq import Retry

async def cls_consolidate_workspace(ctx, workspace_id: str):
    try:
        await CLSOrchestrator.run_consolidation(workspace_id)
    except LLMError as e:
        # Exponential backoff: 60s, 120s, 180s
        raise Retry(defer=ctx['job_try'] * 60)
```

### Meta-audit obligatorio

```python
# Cada job (succeeded/failed/retried) → INSERT audit_events
INSERT INTO shared.audit_events (action, resource_type, payload)
VALUES (
  'job:cls_consolidate_workspace',
  'workspace',
  {
    'workspace_id': '...',
    'job_id': '...',
    'duration': 45,
    'retries': 0,
    'outcome': 'success',
    'cost_usd': 0.023
  }
);
```

### Estructura del módulo for3s_os/jobs/

```
for3s_os/jobs/
├── __init__.py
├── worker.py             → WorkerSettings (config Arq)
├── tasks/
│   ├── __init__.py
│   ├── cls_tasks.py       → cls_consolidate_workspace
│   ├── microglia_tasks.py → nightly, weekly, monthly
│   ├── workspace_tasks.py → onboarding_create_workspace
│   └── reembed_tasks.py   → futuro v2
├── schedules.py           → cron_jobs definitions
└── enqueue.py             → helpers para API enqueue
```

### Path futuro

```
v1: Arq + Valkey + 1 worker
v2: arq-dashboard + múltiples workers si métricas demandan
v3: evaluar Celery si workflows complejos (chains, groups)
```

---

## 5. Sub-tema 3.3 — Connection pooling (pgbouncer)

### Decisión LOCKED

```
pgbouncer + asyncpg pool (transaction mode) + redis-py pool nativo
```

### Contexto

For3s OS tiene múltiples procesos (FastAPI workers + Arq workers) que necesitan conexiones a Postgres y Valkey. Sin pooler dedicado, cada worker abre N conexiones → satura Postgres (max 100 default).

pgbouncer (ISC license, 17 años producción) centraliza pooling entre app y Postgres.

### Mapeo al Grafo Maestro

- **Pilar 2 Escalabilidad:** foundation de connection management
- **Pilar 1 Seguridad:** statement timeout previene DoS
- **TODOS los nodos** que tocan Postgres/Valkey lo usan

### Candidatos evaluados

```
A) asyncpg pool directo       ⚠️ NO escala a >5 workers
B) pgbouncer + asyncpg        ✅ ELEGIDO — estándar industria
C) PgCat                      ⚠️ Moderno pero joven (2022)
D) PgCat + asyncpg            ⚠️ Sin ventaja vs B
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A: Solo   │B: pgbnc  │C: PgCat  │D: PgCat  │
│                          │  asyncpg │+ asyncpg │ solo     │+ asyncpg │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Open-source              │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │
│ Licencia                 │ Apache 2 │   ISC    │   MIT    │   MIT    │
│ Servicios extra          │    0     │    +1    │    +1    │    +1    │
│ RAM extra                │    0     │ ~30 MB   │ ~50 MB   │ ~50 MB   │
│ Setup time               │ ~10 min  │ ~2-4 hrs │ ~3-5 hrs │ ~3-5 hrs │
│ Madurez (años)           │   15+    │   17+    │    3     │    3     │
│ Escalabilidad workers v1 │   ✅✅   │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │
│ Escalabilidad workers v2 │   ⚠️     │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │
│ Centraliza pool          │   ❌    │   ✅✅   │   ✅✅   │   ✅✅   │
│ Métricas centralizadas   │   ❌    │   ✅✅   │  ✅✅✅   │  ✅✅✅   │
│ PAUSE/RESUME ops         │   ❌    │   ✅✅   │   ✅✅   │   ✅✅   │
│ Read replica support     │   ❌    │   ❌    │   ✅✅   │   ✅✅   │
│ Hire fácil               │   ✅✅   │  ✅✅✅   │   ⚠️    │   ⚠️    │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **Escalabilidad desde día 1** (de 5 a 50+ workers sin cambiar arch)
2. **Estándar industria** (17 años battle-tested)
3. **Observabilidad centralizada** (SHOW POOLS, SHOW STATS)
4. **Mantenimiento sin downtime** (PAUSE/RESUME)
5. **RAM overhead mínimo** (~30 MB en CX42 = 0.2%)
6. **ISC license** → respeta 2.B Open Core
7. **Compatible** con AGE + pgvector + pgcrypto
8. **Evita refactor bajo presión** cuando llegue cliente Pro

### Configuración LOCKED v1

```ini
# pgbouncer.ini
[databases]
for3s = host=127.0.0.1 port=5432 dbname=for3s

[pgbouncer]
listen_addr        = 127.0.0.1
listen_port        = 6432
auth_type          = scram-sha-256
auth_file          = /etc/pgbouncer/userlist.txt
pool_mode          = transaction
max_client_conn    = 200
default_pool_size  = 30
reserve_pool_size  = 5
reserve_pool_timeout = 3
server_idle_timeout = 600
server_lifetime    = 3600
log_connections    = 1
log_disconnections = 1
```

### Configuración asyncpg (transaction mode compat)

```python
# for3s_os/infrastructure/postgres.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('PG_USER')}:"
    f"{os.getenv('PG_PASSWORD')}@"
    f"127.0.0.1:6432/"  # ← pgbouncer port, NO Postgres 5432
    f"{os.getenv('PG_DATABASE')}"
)

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # ← delega pool a pgbouncer
    connect_args={
        "statement_cache_size": 0,  # transaction mode compat
        "prepared_statement_cache_size": 0,
        "command_timeout": 60,
    },
)
```

### Configuración asyncpg pool por proceso

```
FastAPI workers:
   min_size: 2
   max_size: 10

Arq workers:
   min_size: 2
   max_size: 5

statement_cache_size:           0  (compat tx mode)
prepared_statement_cache_size:  0
command_timeout:                60
```

### Configuración redis-py pool nativo

```python
# for3s_os/infrastructure/valkey_client.py
from redis.asyncio import ConnectionPool, Redis

pool = ConnectionPool(
    host=os.getenv('VALKEY_HOST', '127.0.0.1'),
    port=int(os.getenv('VALKEY_PORT', '6379')),
    password=os.getenv('VALKEY_PASSWORD'),
    max_connections=50,        # 50 para FastAPI, 20 para Arq
    socket_timeout=5,
    socket_keepalive=True,
    decode_responses=True,
)

def get_redis() -> Redis:
    return Redis(connection_pool=pool)
```

### Cálculo real de conexiones v1

```
App pools (chicos hacia pgbouncer):
   • 2 FastAPI workers × 10 max = 20 clientes pgbouncer
   • 1 Arq worker × 5 max = 5 clientes pgbouncer
   • Total: 25 clientes simultáneos

pgbouncer pool a Postgres:
   • default_pool_size = 30
   • Postgres ve MAX 30 conexiones reales

PostgreSQL CX42 max_conn = 100
   • 30 usadas por pgbouncer + 5 reserved + 5 superuser
   • Margen 60% disponible (60-70 conexiones libres)

v2 escalado proyectado:
   • 5 FastAPI × 10 + 3 Arq × 5 = 65 clientes
   • pgbouncer sigue con pool 30 → Postgres NO se da cuenta
   • Para v2 subir default_pool_size a 50 si necesario
```

### Estructura del módulo for3s_os/infrastructure/

```
for3s_os/infrastructure/
├── postgres.py             → asyncpg pool factory + engine
├── valkey_client.py        → redis-py ConnectionPool
├── pgbouncer_config/
│   ├── pgbouncer.ini       → config principal
│   ├── userlist.txt        → auth users (scram-sha-256)
│   └── pgbouncer.service   → systemd unit
└── healthchecks.py         → /health/db, /health/cache, /health/pool
```

### Monitoring obligatorio

```
Métricas pgbouncer (SHOW POOLS):
   cl_active     (clientes activos)
   cl_waiting    (clientes esperando)
   sv_active     (server conns activas)
   sv_idle       (server conns idle)
   maxwait       (tiempo máx espera)

Alertas:
   • cl_waiting >5 sostenido     → escalar pool
   • maxwait >1s                 → cliente sufre
   • sv_active = max             → saturación

Métricas Postgres (pg_stat_activity):
   • total connections
   • idle_in_transaction (queries muertas)
   • query duration p50/p95/p99

Métricas Valkey (INFO clients):
   • connected_clients
   • blocked_clients
```

### Impacto técnico

```
⚠️ Prepared statements:
   pgbouncer transaction mode NO los soporta.
   asyncpg config: statement_cache_size=0
   SQLAlchemy 2: poolclass=NullPool
   Performance impact: ~5-10% queries simples (despreciable v1)

⚠️ LISTEN/NOTIFY:
   No funciona en transaction mode.
   Mitigación: usar Valkey pub/sub si necesario futuro.
```

### Path futuro

```
v1: pgbouncer transaction + asyncpg + redis-py pool
v2: subir default_pool_size si métricas lo demandan
v3: evaluar PgCat si necesitas read replicas o sharding
```

---

## 6. Sub-tema 3.4 — Async patterns (asyncio + anyio)

### Decisión LOCKED

```
asyncio + anyio + patterns LOCKED explícitos
```

### Contexto

For3s OS coordina 5 piezas en runtime:
- FastAPI handlers (async)
- Arq workers (async)
- SQLAlchemy 2 + asyncpg (async)
- redis-py async (async)
- Stella embeddings (SYNC — requiere wrapper)

Sin patterns claros, el código async se vuelve caos: event loop blocked, connection leaks, race conditions, cancellation no propaga.

### Mapeo al Grafo Maestro

```
3.4 es CAPA TRANSVERSAL — no materializa nodos directamente
pero AFECTA cómo TODOS los nodos funcionan en runtime.

Pilar 2 Escalabilidad: foundation runtime
Pilar 3 Autonomía: workers async autónomos
TODOS los nodos (especialmente):
  • Nodo 2 Hipocampo (Stella sync wrapper)
  • Nodo 10 CLS (LLM async + Stella sync mix)
  • Nodo 6 Microglía (workers cleanup garantizado)
```

### Candidatos evaluados

```
A) asyncio puro              ⚠️ Stack ya tiene anyio (FastAPI dep)
B) asyncio + anyio           ✅ ELEGIDO — APIs mejores + ya en stack
C) anyio puro                ⚠️ Drivers son asyncio-native igual
D) asyncio + uvloop          ⚠️ Optional optimization (defer v2)
```

### Tabla comparativa

```
┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Criterio                 │A:asyncio │B:asyncio │C: anyio  │D: +uvloop│
│                          │  puro    │  + anyio │  puro    │ optional │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Open-source              │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │  ✅✅✅   │
│ Costo                    │   $0     │   $0     │   $0     │   $0     │
│ Ya en stack R1           │  parcial │  ✅✅✅   │   ✅     │   N/A    │
│ Drivers (asyncpg, redis) │  ✅✅✅   │  ✅✅✅   │   ⚠️    │  ✅✅✅   │
│ Structured concurrency   │   ⚠️     │  ✅✅✅   │  ✅✅✅   │   N/A    │
│ CapacityLimiter built-in │   ❌    │  ✅✅✅   │  ✅✅✅   │   N/A    │
│ to_thread wrapper        │  ✅✅    │  ✅✅✅   │  ✅✅✅   │   N/A    │
│ Cancellation             │   ⚠️     │  ✅✅✅   │  ✅✅✅   │   N/A    │
│ Timeouts limpios          │  ✅✅    │  ✅✅✅   │  ✅✅✅   │   N/A    │
│ Performance              │  ✅✅    │  ✅✅    │  ✅✅    │  ✅✅✅   │
│ Compatible Anclas        │   3/3    │   3/3    │   3/3    │   3/3    │
│ Future-proof             │  ✅✅    │  ✅✅✅   │  ✅✅✅   │  ✅✅    │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### Razones de la decisión

1. **Stack ya LOCKED en R1** (asyncio + anyio)
2. **APIs mejores** que asyncio puro (CapacityLimiter, fail_after)
3. **FastAPI ya usa anyio internamente** (coherencia)
4. **Patterns obligatorios** reducen bugs sutiles
5. **Estructura explícita** async_utils/ para code reviews
6. **uvloop DEFERIBLE** a v2 sin urgencia

### 7 Patterns obligatorios LOCKED

```
1. SYNC WRAPPER para código bloqueante
   anyio.to_thread.run_sync() para Stella + librerías sync

2. CAPACITY LIMITER para CPU/API-bound
   • stella_limiter = CapacityLimiter(4)
   • llm_limiter = CapacityLimiter(3)
   • embedding_batch_limiter = CapacityLimiter(2)

3. TIMEOUTS por operación
   LLM_CALL_TIMEOUT         = 60s
   DB_QUERY_TIMEOUT         = 30s
   DB_QUERY_HEAVY_TIMEOUT   = 120s
   VALKEY_OP_TIMEOUT        = 10s
   STELLA_EMBED_TIMEOUT     = 15s
   STELLA_BATCH_TIMEOUT     = 60s
   HNSW_SEARCH_TIMEOUT      = 5s
   CYPHER_QUERY_TIMEOUT     = 30s

4. ASYNC WITH para resource cleanup
   Sin excepciones. async with AsyncSession()

5. STRUCTURED CONCURRENCY para batch
   anyio.create_task_group() para CLS clusters + Microglía

6. CANCELLATION HANDLING
   Cleanup en finally, RE-RAISE CancelledError siempre

7. RATE LIMITING para servicios externos
   Aplicar antes de LLM calls + Stella si necesario
```

### Estructura del módulo for3s_os/async_utils/

```
for3s_os/async_utils/
├── __init__.py
├── limiters.py        → CapacityLimiters globales
├── timeouts.py        → constantes timeouts LOCKED
├── sync_wrappers.py    → AsyncStellaWrapper, etc.
└── task_groups.py      → helpers structured concurrency
```

### Ejemplo limiters.py

```python
import anyio

stella_limiter = anyio.CapacityLimiter(4)
llm_limiter = anyio.CapacityLimiter(3)
embedding_batch_limiter = anyio.CapacityLimiter(2)
```

### Ejemplo timeouts.py

```python
LLM_CALL_TIMEOUT = 60       # Claude Haiku
DB_QUERY_TIMEOUT = 30
DB_QUERY_HEAVY_TIMEOUT = 120  # CLS, batch ops
VALKEY_OP_TIMEOUT = 10
STELLA_EMBED_TIMEOUT = 15
STELLA_BATCH_TIMEOUT = 60
HNSW_SEARCH_TIMEOUT = 5
CYPHER_QUERY_TIMEOUT = 30
```

### Ejemplo sync_wrappers.py — AsyncStellaWrapper

```python
import anyio
from for3s_os.async_utils.limiters import stella_limiter

class AsyncStellaWrapper:
    def __init__(self, model):
        self._model = model

    async def encode(self, text: str):
        async with stella_limiter:
            return await anyio.to_thread.run_sync(
                self._model.encode, text)

    async def encode_batch(self, texts: list[str]):
        async with stella_limiter:
            return await anyio.to_thread.run_sync(
                self._model.encode, texts)
```

### Ejemplo CLS pipeline con anyio

```python
async def cls_consolidate_workspace(ctx, workspace_id: str):
    with anyio.fail_after(600):  # timeout 10 min
        eps = await get_pending(workspace_id, limit=500)

        if len(eps) < 10:
            return

        clusters = await clustering_engine.cluster(eps)

        # Concurrencia controlada: max 3 LLM calls simultáneos
        async with anyio.create_task_group() as tg:
            for cluster in clusters:
                tg.start_soon(process_cluster_with_llm, cluster)

        await mark_consolidated([e.id for e in eps])
```

### Ejemplo cancellation handling

```python
try:
    result = await long_operation()
    return result
except anyio.get_cancelled_exc_class():
    logger.info("Operation cancelled, cleanup")
    await cleanup_resources()
    raise  # ← RE-RAISE siempre
finally:
    await release_locks()
```

### Path futuro

```
v1: asyncio + anyio + patterns LOCKED
v2: añadir uvloop si event loop blocked >10ms sostenido
v3: GPU + ProcessPoolExecutor si embeddings throughput exige
```

---

## 7. Stack final consolidado

```
COMPONENTE                  DECISIÓN                            COSTO
──────────────────────────────────────────────────────────────────────
Hetzner CX42 (B1+B2)        16 GB RAM, 8 vCPU                    USD ~25/mo
PostgreSQL 16 (B1)          + AGE + pgvector + pgcrypto          USD 0
pgbouncer (B3 3.3)          ISC, transaction mode pool 30        USD 0
Valkey (B3 3.1)             BSD-3, scope mínimo, 256 MB max      USD 0
Arq (B3 3.2)                MIT, async-native, 1 worker v1        USD 0
asyncio + anyio (B3 3.4)    PSF + MIT, 7 patterns LOCKED          USD 0
asyncpg pool (B1 1.4)       Apache 2.0, transaction mode compat   USD 0
redis-py pool nativo (B3)   MIT, 50 conn FastAPI / 20 Arq        USD 0
Stella embeddings (B2 2.2)  Local CPU, AsyncStellaWrapper        USD 0
OpenAI fallback (B2)        API, statement_cache_size=0           USD <1/mo
Claude Haiku CLS (B2 2.6)   anthropic SDK, llm_limiter(3)         USD ~37/mo
──────────────────────────────────────────────────────────────────────
TOTAL incremental B3                                              USD 0
TOTAL v1 (B1 + B2 + B3)                                           USD ~63/mo
```

### Servicios runtime corriendo en Linux LOCAL Brian (D-009)

```
Procesos systemd v1:
   1. PostgreSQL 16             (~3 GB RAM)
   2. pgbouncer                 (~30 MB RAM)
   3. Valkey                    (~100 MB RAM)
   4. FastAPI worker (uvicorn)   (~500 MB RAM)
   5. Arq worker                 (~300 MB RAM con Stella cargado)
   6. cloudflared (Cloudflare Tunnel)  (~50 MB RAM)
   ─────────────────────────────────────────────────
   Total RAM usage v1:           ~4 GB (de 30 GB disponibles)
   Holgura:                      26 GB (87%)

Hardware host:
   • Linux LOCAL Brian (30 GB RAM, 1 TB disco)
   • 24/7 con UPS recomendado
   • USD 0 hardware + ~USD 5/mes electricidad
```

---

## 8. Arquitectura emergente — diagrama runtime

```
                  FOR3S OS — Runtime completo (B1+B2+B3)

   ┌─────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │   CLIENTE (HTTP request / Telegram)                              │
   │                            │                                      │
   │                            ▼                                      │
   │   ┌───────────────────────────────────────────────────────┐      │
   │   │ FastAPI worker (uvicorn, asyncio + anyio)              │      │
   │   │   • Rate limiting middleware (Valkey)                  │      │
   │   │   • Request handlers (async)                           │      │
   │   │   • pool asyncpg max 10 (→ pgbouncer)                  │      │
   │   │   • pool redis-py max 50                               │      │
   │   └───────────────────────────────────────────────────────┘      │
   │              │                          │                          │
   │              │ DB queries               │ enqueue jobs              │
   │              ▼                          ▼                          │
   │   ┌──────────────────────┐   ┌──────────────────────┐             │
   │   │ pgbouncer            │   │ Valkey               │             │
   │   │   port 6432           │   │   port 6379           │             │
   │   │   transaction mode    │   │   maxmemory 256mb     │             │
   │   │   pool 30             │   │   AOF + RDB           │             │
   │   └──────────────────────┘   └──────────────────────┘             │
   │              │                          │                          │
   │              ▼                          ▼                          │
   │   ┌──────────────────────┐   ┌──────────────────────┐             │
   │   │ PostgreSQL 16         │   │ Arq worker            │             │
   │   │   port 5432           │   │   (async-native)     │             │
   │   │   max_conn 100         │   │   pool asyncpg max 5  │             │
   │   │   + AGE + pgvector    │   │   pool redis-py max 20│             │
   │   │   + pgcrypto          │   │   max_jobs 10         │             │
   │   │                        │   │                       │             │
   │   │   schema: shared       │   │   Cron jobs:          │             │
   │   │   schema: wks_A        │   │   • 2 AM CLS          │             │
   │   │   schema: wks_B        │   │   • 3 AM Microglía    │             │
   │   │   ...                  │   │     nightly           │             │
   │   └──────────────────────┘   │   • Dom 4 AM weekly   │             │
   │                                │   • Día 1 mensual     │             │
   │                                └──────────────────────┘             │
   │                                         │                          │
   │                                         │                          │
   │   ┌──────────────────────────────────────────────────────┐         │
   │   │ AsyncStellaWrapper (in-process en Arq + FastAPI)      │         │
   │   │   • sentence-transformers (sync)                       │         │
   │   │   • anyio.to_thread.run_sync()                         │         │
   │   │   • stella_limiter (4 concurrent)                      │         │
   │   │   • Modelo dunzhang/stella_en_400M_v5 cargado en RAM  │         │
   │   └──────────────────────────────────────────────────────┘         │
   │                                         │                          │
   │                                         ▼                          │
   │   ┌──────────────────────────────────────────────────────┐         │
   │   │ Claude Haiku 4.5 (Anthropic API)                       │         │
   │   │   • anthropic SDK async                                 │         │
   │   │   • llm_limiter (3 concurrent)                          │         │
   │   │   • anyio.fail_after(60s)                              │         │
   │   │   • Solo para CLS consolidation                        │         │
   │   └──────────────────────────────────────────────────────┘         │
   │                                                                  │
   │   PATTERNS TRANSVERSALES (3.4):                                  │
   │      ✓ async with para cleanup                                   │
   │      ✓ Timeouts por operación                                    │
   │      ✓ TaskGroups para batch                                     │
   │      ✓ CancelledError re-raise + cleanup                          │
   │      ✓ CapacityLimiters para CPU/API-bound                       │
   │      ✓ Sync wrapper para Stella                                  │
   │                                                                  │
   └─────────────────────────────────────────────────────────────────┘
```

---

## 9. Cobertura del Grafo Maestro

### B3 es CAPA TRANSVERSAL — no añade nodos, refuerza foundation

```
PILAR                            STATUS POST-B1+B2     STATUS POST-B3
─────────────────────────────────────────────────────────────────────────
Pilar 1 Seguridad E2E            ✅ REFORZADO          ✅ + rate limiting
Pilar 2 Escalabilidad             🟡 FOUNDATION B1      ✅ COMPLETO B3
Pilar 3 Autonomía Generativa     ✅ MEMORY B2          ✅ + workers autón.
```

### Nodos cerebrales — B3 NO añade nodos nuevos

```
Refuerza runtime de:
   ✅ Nodo 2 Hipocampo (Stella wrapper + connection pool)
   ✅ Nodo 6 Microglía (Arq jobs + cleanup patterns)
   ✅ Nodo 10 CLS (Arq jobs + LLM limiter + timeouts)
   ✅ Nodo 1 KG (Cypher con pool dedicado)
   ✅ Nodo 4 Skills (CRUD con pool dedicado)

Foundation transversal para TODOS los nodos.
```

### Anclas LOCKED — Verificación post-B3

```
1.D Dedicated SaaS:  ✅ Todo en CX42, schema-per-tenant respetado
2.B Open Core:       ✅ Todas licencias permisivas:
                        • Valkey (BSD-3)
                        • Arq (MIT)
                        • pgbouncer (ISC)
                        • asyncio (PSF)
                        • anyio (MIT)
                        • redis-py (MIT)
                        • asyncpg (Apache 2.0)
3.D Equipo pequeño:  ✅ Cero servicios extra de infra (todo en CX42).
                        +2 procesos systemd locales (pgbouncer + Valkey)
                        Cero overhead operacional adicional.
```

---

## 10. Costo total actualizado

```
Hardware Linux LOCAL Brian (30 GB RAM, 1 TB):     USD 0
Electricidad servidor 24/7:                        USD ~5/mes
Cloudflare Tunnel (free tier):                     USD 0
Dominio for3s.ai:                                   USD ~$1/mes ($10/año)
PostgreSQL 16 + AGE + pgvector + pgcrypto:         USD 0
pgbouncer (vive en local):                          USD 0
Valkey (vive en local):                             USD 0
Arq (Python lib):                                  USD 0
asyncio + anyio + redis-py + asyncpg:              USD 0
Stella embeddings local (modelo):                  USD 0
OpenAI fallback embeddings:                        USD <1/mes
Claude Haiku 4.5 (CLS):                            USD ~37/mes
──────────────────────────────────────────────────────────────
TOTAL infra+AI v1 (B1+B2+B3 + D-009):              USD ~43/mes
```

~~Decisión original Hetzner CX42 (USD ~63/mes) sobrescrita por D-009 (despliegue LOCAL).~~

### Vs constraint P2 <25%

```
Pilot Light USD 3,500 (3 semanas)
   Techo AI+infra: USD 875 (25%)
   Consumo real v1 (3 sem): USD ~32.25
   → 3.7% del techo
   → MARGEN 96.3% disponible

Pilot Pro USD 8,000 (3 semanas)
   Techo: USD 2,000
   → 1.6% del techo
   → Margen 98.4%

CONCLUSIÓN: Infra+memoria+async holgada por 27x.
   Margen disponible para R3 (LLM principal) + R4 (MCP tools).

Compliance boost LOCAL: datos del cliente JAMÁS salen
del hardware de Brian. Ventaja comercial enterprise.
```

---

## 11. Exploraciones futuras NO adoptadas v1

### 📚 Sub-tema 3.1 — Redis layer alternativos

```
📚 Candidato A — NO Redis (defer)
   Trigger: For3s pivot a "biblioteca embebida" no SaaS
   No aplicable a línea v1

📚 Candidato C — DragonflyDB
   Trigger: Valkey CPU >70% sostenido + re-evaluar 2.B
   Beneficio: 25x performance multi-core
   Costo: BSL viola Open Core

📚 Valkey Cluster mode
   Trigger: 1 instance no aguanta volumen
   Beneficio: sharding automático

📚 Valkey Sentinel (HA)
   Trigger: SLA enterprise 99.99%
   Beneficio: failover automático

📚 Redis Stack (search, JSON, time series)
   Probablemente NUNCA — pgvector + JSONB son superiores

📚 Cache de embeddings frecuentes
   Trigger: queries similares >100 req/min mismo workspace
   Beneficio: latencia <1ms vs ~10-30ms HNSW

📚 Working memory shared cross-procesos
   Trigger: multi-worker FastAPI deployment

📚 Pub/sub coordinación inter-workers
   Trigger: workers nightly interfieren entre sí
```

### 📚 Sub-tema 3.2 — Background jobs alternativos

```
📚 Celery upgrade
   Trigger: workflows complejos (chains, groups, chords)
   Cuándo: v3 si necesidad real surge

📚 arq-dashboard
   Trigger: logs estructurados no bastan
   Cuándo: v2 si equipo crece

📚 Múltiples workers Arq (horizontal scaling)
   Trigger: queue_depth >100 sostenido

📚 Inngest / Hatchet (cloud-native)
   Trigger: For3s decide arquitectura SaaS jobs
   Cuándo: v3+ improbable

📚 Job priorities (queues separadas)
   Trigger: jobs críticos vs background

📚 Dead Letter Queue (DLQ)
   Trigger: retry-exhausted jobs >1% del total

📚 Job result webhooks
   Trigger: cliente lo pide
```

### 📚 Sub-tema 3.3 — Connection pooling alternativos

```
📚 PgCat upgrade
   Trigger: read replica routing, sharding, multi-region
   Cuándo: v3

📚 pgbouncer session mode
   Trigger: LISTEN/NOTIFY o prepared statements críticos

📚 Twemproxy / Envoy proxy para Valkey
   Trigger: redis-py pool >50% sostenido
   Cuándo: v2-v3

📚 Múltiples pgbouncer + load balancer
   Trigger: SLA 99.99% uptime enterprise

📚 Postgres read replicas (con PgCat routing)
   Trigger: Postgres CPU >70% por reads

📚 Subir max_connections a 200+
   Trigger: pgbouncer SHOW POOLS muestra saturación

📚 Connection lifetime tuning agresivo
   Trigger: métricas muestran churn alto
```

### 📚 Sub-tema 3.4 — Async patterns alternativos

```
📚 uvloop event loop
   Cuándo: v2 si métricas event loop >10ms scheduling
   Beneficio: 2-4x I/O performance
   Trigger: latencia API limitada por loop, no queries

📚 trio backend (vía anyio)
   Muy improbable, ecosistema asyncio domina

📚 ProcessPoolExecutor para embeddings batch
   Trigger: throughput embeddings <100/s sostenido
   Beneficio: parallelism real sin GIL

📚 GPU para Stella (CUDA)
   Trigger: ver exploraciones futuras 2.2
   Costo: USD 200+/mes GPU

📚 Métricas de event loop (Prometheus)
   Cuándo: v2 con observabilidad
   Trigger: R8 Observability
```

**CRÍTICO: ESTAS EXPLORACIONES NO ALTERAN LA LÍNEA v1.**
Documentadas para investigación basada en datos reales.

---

## 12. Implicaciones en bloques siguientes

### Para Bloque 4 — Files & External

```
✅ Backup strategy (4.4):
   • pg_dump pasa directo a Postgres (puerto 5432), NO pgbouncer
   • pgbouncer es para app, no para mantenimiento
   • Backup script vía systemd timer (no Arq, es ops)

✅ File storage (4.1):
   • Workers Arq pueden subir/bajar archivos a S3
   • Pool de conexiones HTTP async
```

### Para R3 — Model/LLM Layer

```
✅ Patterns async LOCKED se aplican a R3:
   • LLM clients con llm_limiter(3)
   • anyio.fail_after(60s) para Claude/GPT
   • Reuso de AsyncStellaWrapper pattern para otros sync clients

✅ Costos AI tienen margen 94.6% del techo P2
   → R3 puede gastar USD ~800/mes en Pilot Light sin problema
```

### Para R5 — Orchestration

```
✅ Working Memory (Nodo 3 PFC) puede compartirse via Valkey si v2
   → 3.1 LOCKED dejó preparación para esto

✅ DMN (Nodo 7) puede usar Arq cron para "idle compute"
   → Trigger: cuando no hay sesiones activas por X tiempo

✅ Action selection puede usar limiters para evitar saturar
   external tools
```

### Para R8 — Observability

```
✅ Métricas obligatorias documentadas:
   • pgbouncer SHOW POOLS
   • Postgres pg_stat_activity
   • Valkey INFO clients
   • Arq jobs_succeeded/failed/queue_depth
   • Event loop scheduling time (futuro)

✅ Logs estructurados (structlog → JSON)
   ya integrados con todos los componentes B3
```

### Para R9 — Security/Compliance

```
✅ Rate limiting ya implementado vía Valkey (3.1)
✅ Audit chain integration con jobs (3.2 meta-audit)
✅ Statement timeout previene DoS (3.3)
✅ Cancellation handling previene runaway tasks (3.4)

R9 extiende:
   • Policy engine sobre RBAC
   • Encryption key rotation con jobs Arq
   • Compliance reports usando audit_events
```

### Para R10 — CI/CD / Deploy

```
✅ Deploy pipeline debe instalar:
   • PostgreSQL 16 + AGE + pgvector + pgcrypto
   • pgbouncer (systemd service)
   • Valkey (systemd service)
   • Arq worker (systemd service)
   • uvicorn FastAPI (systemd service)
   • Stella model cache

✅ Migrations Alembic conectan a pgbouncer (puerto 6432)
   EXCEPCIÓN: DDL pesado (DROP TABLE CONCURRENTLY)
   puede requerir conexión directa Postgres (5432)
```

---

## Cierre del Bloque 3

```
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ BLOQUE 3 — PERFORMANCE & ASYNC CERRADO                    ║
║                                                                ║
║   4/4 sub-temas LOCKED                                         ║
║   Costo incremental: USD 0 (todo gratis, vive en CX42)         ║
║   Costo total v1 (B1+B2+B3): USD ~63/mes (sin cambio)          ║
║   Servicios extra de infra: 0 (todo local en CX42)             ║
║   Procesos systemd añadidos: +2 (pgbouncer + Valkey)            ║
║   Capa transversal: refuerza foundation de Pilar 2 + Pilar 3   ║
║                                                                ║
║   Próximo: Bloque 4 — Files & External Data (último de R2)     ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```