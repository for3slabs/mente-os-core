# Estimación de Tiempo de Programación — Por Sub-Tema

> **El cronograma con números.** El `Plan_Maestro_Programacion.md` da el ORDEN; este documento da el TIEMPO, bajando a nivel de cada sub-tema de las 10 rondas. Convierte los `[EST.]` del plan en una estimación granular y trazable.

**Owner:** Brian López
**Fecha:** 2026-06-09
**Estatus:** ✅ Estimación de tiempo v1 — recalibrar contra realidad al programar
**Capa:** Doc — planeación de ejecución (acompaña al Plan Maestro de Programación)

**PARÁMETROS DE ESTA ESTIMACIÓN (confirmados por Brian):**
```
   • Equipo:       Brian SOLO, tiempo completo (~40h/semana = ~5 días/sem)
   • Experiencia:  ALTA (Brian domina el stack — construyó OpenClaw/Hermes)
   • Profundidad:  Por sub-tema (máximo detalle, ~100 sub-temas)
```

**⚠️ NATURALEZA DE ESTOS NÚMEROS — leer antes de usar:**
```
   Esta es una estimación DERIVADA, NO un dato de los documentos maestros.
   Los maestros NO contienen tiempos de programación (solo el hito Telegram
   de R1 = 6 semanas, que sí es lockeado). Los tiempos de abajo los calculo
   por: conteo real de sub-temas + complejidad documentada (scores, riesgos,
   capas, # de componentes) + velocidad realista de un dev senior full-time.

   Unidad base: DÍAS-DEV (1 día = ~8h efectivas de programación + tests).
   Las estimaciones incluyen: código + tests unitarios + integración básica.
   NO incluyen: pentest externo, onboarding de pilots, SOC2 cert real.

   Margen: ±30%. La realidad recalibra. R6 (Pilar 3) es la más incierta.
```

**Documentos hermanos:**
- `Plan_Maestro_Programacion.md` — el ORDEN de construcción (este da el TIEMPO)
- `Reporte_Maestro_Consolidado_R1-R10.md` §8 — estimación gruesa previa

---

## Tabla de contenidos

1. [Cómo se calculó (metodología)](#1-cómo-se-calculó)
2. [Resumen ejecutivo — el número](#2-resumen-ejecutivo)
3. [Estimación por ronda (vista rápida)](#3-estimación-por-ronda)
4. [Estimación detallada por sub-tema](#4-estimación-detallada-por-sub-tema)
   - [Fase 0 — Setup + CI/CD](#fase-0--setup--cicd)
   - [R1 — Compute/Lenguaje](#r1--computelenguaje)
   - [R2 — Data Layer](#r2--data-layer)
   - [R3 — Model/LLM Layer](#r3--modelllm-layer)
   - [R4 — Tools/MCP Layer](#r4--toolsmcp-layer)
   - [R5 — Orchestration/Multi-Agent](#r5--orchestrationmulti-agent)
   - [R6 — Memory Stack (Pilar 3)](#r6--memory-stack-pilar-3)
   - [R7 — Frontend/Channel](#r7--frontendchannel)
   - [R8 — Observabilidad](#r8--observabilidad)
   - [R9 — Security/Compliance](#r9--securitycompliance)
   - [R10 — CI/CD/Deploy](#r10--cicddeploy)
5. [Calendario consolidado (semanas y meses)](#5-calendario-consolidado)
6. [El MVP pilotable — desglose](#6-el-mvp-pilotable)
7. [Factores que pueden mover los números](#7-factores-que-pueden-mover-los-números)
8. [Diagrama: distribución del esfuerzo](#8-diagrama-distribución-del-esfuerzo)
9. [Cómo recalibrar contra la realidad](#9-cómo-recalibrar)

---

## 1. Cómo se calculó

### 1.1 Método de estimación

Para cada sub-tema asigné días-dev usando 3 factores:

```
   FACTOR 1 — TAMAÑO: ¿cuántos componentes tiene el sub-tema?
      (clases, tablas SQL, funciones, integraciones)

   FACTOR 2 — COMPLEJIDAD: ¿qué tan difícil es la lógica?
      Trivial (CRUD, config)        → 0.5-1 día
      Simple (1 clase + tests)      → 1-2 días
      Media (varias clases + integr)→ 2-4 días
      Alta (algoritmos + edge cases)→ 4-7 días
      Muy alta (auto-modificante,   → 7-12 días
        security crítica, 18 capas)

   FACTOR 3 — RIESGO/NOVEDAD: ¿es terreno conocido o nuevo?
      Conocido (Brian lo domina)    → sin ajuste
      Parcialmente nuevo            → +20%
      Frontier (Pilar 3, governor)  → +40%
```

### 1.2 Ajuste por experiencia ALTA (Brian)

Como Brian domina el stack (OpenClaw/Hermes en Python), apliqué la **velocidad de dev senior**: las piezas conocidas (FastAPI, asyncio, SQLAlchemy, prompts) van rápido. El margen de aprendizaje se reserva solo para lo genuinamente nuevo (AGE, Pilar 3 auto-modificante, governor).

### 1.3 Qué incluye 1 "día-dev"

```
   1 día-dev ≈ 8h efectivas =
      • código del sub-tema
      • tests unitarios
      • integración básica con lo ya construido
      • debugging del happy path + edge cases principales

   NO incluye (se suma aparte como overhead): refactors grandes,
   debugging profundo de bugs raros, reuniones, documentación extensa.
   → Por eso al total se le aplica un factor de overhead realista (§5).
```

---

## 2. Resumen ejecutivo

```
   ╔═══════════════════════════════════════════════════════════════════╗
   ║   ESTIMACIÓN: Brian solo · full-time · experiencia alta            ║
   ║                                                                    ║
   ║   ESFUERZO NETO (días-dev de código):     ~155-175 días-dev        ║
   ║   + OVERHEAD realista (~25%):              ~39-44 días             ║
   ║   ─────────────────────────────────────────────────────           ║
   ║   ESFUERZO TOTAL:                          ~194-219 días-dev       ║
   ║                                                                    ║
   ║   A 5 días/semana:                         ~39-44 semanas          ║
   ║   = ~9-10 meses (full-time, 1 dev senior)                          ║
   ║                                                                    ║
   ║   ★ MVP PILOTABLE (Fase 0+1 = R2+R3+R4):   ~63-72 días = ~13-15 sem║
   ║     = ~3-3.5 meses                                                  ║
   ║                                                                    ║
   ║   ▲ Hito Telegram (R1 §10, sub-conjunto):  6 semanas [LOCKED]      ║
   ╚═══════════════════════════════════════════════════════════════════╝
```

**Lectura honesta:** con Brian solo full-time, el sistema completo es **~9-10 meses**. El MVP pilotable (lo que puedes mostrar a un cliente) está en **~3-3.5 meses**. Estos números son más altos que la estimación gruesa previa (~6-9 meses) porque al ir sub-tema por sub-tema aparecen los detalles que se subestiman a nivel grueso — y porque "Brian solo" no permite paralelizar (un solo dev hace todo en secuencia).

**Por qué más que la estimación gruesa:** la estimación previa (~6-9 meses) asumía posible paralelización con 2 devs. Con 1 dev solo, **todo es secuencial** → el calendario se alarga aunque el esfuerzo total sea similar.

---

## 3. Estimación por ronda (vista rápida)

```
   ┌────────┬──────────────────────────┬─────────────┬──────────────┐
   │ FASE/R │ Qué                      │ Días-dev    │ Semanas      │
   ├────────┼──────────────────────────┼─────────────┼──────────────┤
   │ Fase 0 │ Setup + CI/CD            │ 4-5         │ ~1           │
   │ R1     │ Compute (integrado F0+F1)│ 3-4         │ ~0.7         │
   │ R2     │ Data Layer (20 sub-temas)│ 30-34       │ ~6-7         │
   │ R3     │ Model/LLM (14 sub-temas) │ 21-24       │ ~4-5         │
   │ R4     │ Tools/MCP (11 sub-temas) │ 22-26       │ ~4.5-5       │
   │ R5     │ Orchestration (14 sub-t) │ 26-30       │ ~5-6         │
   │ R6     │ Memory/Pilar 3 (13+gov)  │ 30-36       │ ~6-7         │
   │ R7     │ Frontend (12 sub-temas)  │ 18-21       │ ~3.5-4       │
   │ R8     │ Observabilidad (12 sub-t)│ 14-17       │ ~3           │
   │ R9     │ Security (9 sub-temas)   │ 17-20       │ ~3.5-4       │
   │ R10    │ Deploy (9 sub-temas)     │ 14-17       │ ~3           │
   ├────────┴──────────────────────────┼─────────────┼──────────────┤
   │ ESFUERZO NETO                      │ ~155-175    │ ~31-35       │
   │ + OVERHEAD ~25%                    │ ~39-44      │ ~8-9         │
   │ TOTAL                              │ ~194-219    │ ~39-44 sem   │
   └────────────────────────────────────┴─────────────┴──────────────┘

   NOTA: R1 aparece pequeño porque su grueso (setup) está en Fase 0,
   y su lógica de agente mínimo se absorbe en R2/R3 (no se duplica).
```

---

## 4. Estimación detallada por sub-tema

Cada sub-tema con su estimación en días-dev + nota de complejidad. **Suma neta de código, antes de overhead.**

### Fase 0 — Setup + CI/CD

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tarea                                   │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ uv init + estructura monorepo (apps/packages)│ 0.5  │ trivial     │
   │ pyproject + uv.lock + python-version        │ 0.5  │ trivial     │
   │ CI GitHub Actions (ruff+ty+pytest)          │ 1.5  │ simple      │
   │ Pilar 3 GATE skeleton (vacío, listo R6)     │ 1    │ simple      │
   │ Installer base (one-line script)            │ 1    │ simple      │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL FASE 0                             │ 4.5  │             │
   └─────────────────────────────────────────────┴──────┴─────────────┘
```

### R1 — Compute/Lenguaje

```
   R1 es decisiones de stack (ya tomadas). Lo "programable" de R1 es el
   agente mínimo CLI + LLM call, que se absorbe en R2/R3. Aquí solo el
   esqueleto del agent_runtime.

   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tarea                                   │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ Agent runtime skeleton (loop + CLI rich)    │ 2    │ simple      │
   │ Profiles base (multi-agente isolation)      │ 1.5  │ simple      │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R1                                 │ 3.5  │             │
   └─────────────────────────────────────────────┴──────┴─────────────┘
```

### R2 — Data Layer

```
   La ronda más grande (20 sub-temas) y la más bloqueante. Foundation crítica.

   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 1.1 PostgreSQL 16 setup + extensiones       │ 1    │ simple      │
   │     (AGE + pgvector + pgcrypto)             │      │             │
   │ 1.2 Knowledge Graph (AGE) + Cypher wrapper  │ 3    │ media+nuevo │
   │ 1.3 Vector store (pgvector + HNSW tuneado)  │ 2    │ media       │
   │ 1.4 ORM (SQLAlchemy 2 + asyncpg)            │ 1.5  │ conocido    │
   │ 1.5 Migraciones (Alembic multi-schema)      │ 2    │ media       │
   │ 1.6 Event Sourcing (events tables+triggers) │ 2.5  │ media       │
   │ 2.1 Memory framework (módulo memory/)       │ 2    │ media       │
   │ 2.2 Embeddings (Stella local + fallback)    │ 2    │ media+nuevo │
   │ 2.3 Vector indexing (HNSW params + monitor) │ 1    │ simple      │
   │ 2.4 Memory tiers (Working/Short/Long)       │ 2.5  │ media       │
   │ 2.5 Forgetting (Microglía: soft+decay+arch) │ 2.5  │ media       │
   │ 2.6 CLS Consolidation (HDBSCAN + Haiku)     │ 3    │ alta        │
   │ 2.7 Mapeo Nodo↔Tabla (doc, ya hecho)        │ 0    │ —           │
   │ 3.1 Valkey setup + scope mínimo             │ 0.5  │ trivial     │
   │ 3.2 Arq background jobs + cron              │ 1.5  │ simple      │
   │ 3.3 pgbouncer + asyncpg pool                │ 1    │ simple      │
   │ 3.4 Async patterns (7 patterns + wrappers)  │ 1.5  │ simple      │
   │ 4.1 File storage (filesystem + metadata)    │ 1    │ simple      │
   │ 4.2 S3 provider (NO v1 — solo decisión)     │ 0    │ —           │
   │ 4.4 Backup strategy (3-2-1 scripts)         │ 2    │ media       │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R2                                 │ 32   │ (30-34)     │
   └─────────────────────────────────────────────┴──────┴─────────────┘

   ⚠️ R2 es el cuello de botella. 1.2 (AGE) y 2.6 (CLS) son los más
   pesados. Si algo se atrasa aquí, atrasa TODO. Dedicarle foco.
```

### R3 — Model/LLM Layer

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 3.1.1 Provider Anthropic + LLMProvider abstr│ 1.5  │ conocido    │
   │ 3.1.2 Modelo Sonnet/Opus + tier per-workspace│ 1   │ simple      │
   │ 3.1.3 Multi-model routing (NO v1 — decisión)│ 0    │ —           │
   │ 3.1.4 Local LLM fallback (FailoverManager)  │ 1.5  │ simple      │
   │ 3.2.1 Prompt framework (Jinja2 + registry)  │ 2    │ media       │
   │ 3.2.2 Context window mgmt (budget+ranking)  │ 2.5  │ media       │
   │ 3.2.3 Prompt caching (4 capas + invalidation)│ 2   │ media       │
   │ 3.2.4 Function calling (ToolRegistry+executor)│ 3  │ alta        │
   │ 3.3.1 Streaming SSE (eventos + cancel)      │ 2    │ media       │
   │ 3.3.2 Concurrency (Token Bucket per-ws)     │ 2    │ media       │
   │ 3.3.3 Retry & fallback (14 ErrorTypes+CB)   │ 2    │ media       │
   │ 3.4.1 Observability (Prometheus + recorder) │ 1.5  │ simple      │
   │ 3.4.2 Cost monitoring (5 capacidades)       │ 2    │ media       │
   │ 3.4.3 Eval framework (4 capas + anti-sesgo) │ 3    │ alta        │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R3                                 │ 22.5 │ (21-24)     │
   └─────────────────────────────────────────────┴──────┴─────────────┘

   Más pesados: 3.2.4 (tool executor, foundation R4/R5) y 3.4.3 (eval).
```

### R4 — Tools/MCP Layer

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 4.1.1 MCP client framework (mcp SDK + abstr)│ 2    │ media+nuevo │
   │ 4.1.2 Tool discovery (5 triggers hot-reload)│ 2.5  │ media       │
   │ 4.1.3 Docker multi-tenant 3 capas           │ 4    │ alta+nuevo  │
   │ 4.1.4 Secrets KEK hierarchy (HKDF+AES-GCM)  │ 3    │ alta        │
   │ 4.2.1 GitHub MCP (oficial + auth + cache)   │ 2.5  │ media       │
   │ 4.2.2 Filesystem MCP (custom + path valid.) │ 2.5  │ media       │
   │ 4.2.3 HTTP MCP (custom + SSRF 5-capa)       │ 3    │ alta        │
   │ 4.2.4 Telegram MCP (custom + Hermes patterns)│ 2.5 │ media       │
   │ 4.3.1 Authorization workflows (7 capacidades)│ 3   │ alta        │
   │ 4.3.2 Versioning + rollback (SemVer+SHA)    │ 1.5  │ simple      │
   │ 4.3.3 Testing & sandbox (5 capas)           │ 2    │ media       │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R4                                 │ 28.5 │ (22-26 nucleo│
   │   (MVP usa B1+B2; B3 puede diferirse parcial)│      │  +B3 extra) │
   └─────────────────────────────────────────────┴──────┴─────────────┘

   Más pesados: 4.1.3 (Docker multi-tenant, nuevo) y 4.1.4 (KEK, crítico).
   Para MVP: B1+B2 (~22 días). B3 (lifecycle, ~6 días) puede ir después.
```

### R5 — Orchestration/Multi-Agent

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 5.1.1 Tool Selection (B+C híbrido)          │ 1.5  │ simple      │
   │ 5.1.2 Context Routing (4 tiers + skip)      │ 2    │ media       │
   │ 5.1.3 Subgraph Activation (3 modos)         │ 1.5  │ simple      │
   │ 5.1.4 Neuromoduladores (4 modos)            │ 1.5  │ simple      │
   │ 5.2.1 Dual-Process S1/S2 (multi-señal)      │ 2    │ media       │
   │ 5.2.2 LLM Tier Routing (6 factores+history) │ 3    │ alta        │
   │ 5.2.3 Fast Path (3 layers)                  │ 2    │ media       │
   │ 5.3.1 Agent Topology (hub-and-spoke + 5 spec)│ 2   │ media       │
   │ 5.3.2 Lifecycle HARDENED (18 capas defense) │ 6    │ MUY alta    │
   │ 5.3.3 Inter-Agent Comm (message bus)        │ 2.5  │ media       │
   │ 5.3.4 Cost Control (7 layers)               │ 2.5  │ media       │
   │ 5.4.1 Idle Detection + DMN Scheduler        │ 2    │ media       │
   │ 5.4.2 DMN Tasks (8 action_fn — ya refinados)│ 4    │ alta        │
   │ 5.4.3 DMN Budget + 9 controles              │ 2    │ media       │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R5                                 │ 36.5 │ (26-30 sin  │
   │   (5.3.2 las 18 capas es el monstruo)        │      │  margen amp)│
   └─────────────────────────────────────────────┴──────┴─────────────┘

   ⚠️ 5.3.2 (18 capas defense-in-depth) es el sub-tema individual MÁS
   pesado de TODO el proyecto junto con R6. 6 días solo eso.
```

### R6 — Memory Stack (Pilar 3)

```
   ⭐ LA MÁS DELICADA. Código auto-modificante. Sigue el orden interno §7
   del Plan Maestro (10 pasos). Incluye +40% de riesgo (frontier).

   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema (orden de programación R6 §E)       │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 6.2.1 Skill Schema (FS+PG+pgvector+RLS)     │ 3    │ alta        │
   │ 6.1.1 PFC core (plan-then-execute+executor) │ 3    │ alta        │
   │ 6.1.2 Confidence scoring (8 señales)        │ 2.5  │ alta        │
   │ 6.1.3 Check loop (re-plan + ask-human)      │ 2.5  │ alta        │
   │ 6.2.2 Skill GO (skill_to_plan + parser)     │ 3    │ alta+frontier│
   │ 6.2.3 Vía NO-GO (3 niveles + HARD bootstrap)│ 3    │ alta+segur. │
   │ 6.2.4 Dopaminergic scoring (TD-learning)    │ 2.5  │ alta        │
   │ 6.2.5 Lifecycle manager (8 estados+sandbox) │ 3.5  │ alta        │
   │ 6.1.4 Plan→Skill promotion (7 fases)        │ 3.5  │ MUY alta    │
   │ ⭐ Meta-Orchestrator (governor 6 frenos)     │ 4    │ MUY alta+   │
   │    (Pre-Code §A — ANTES de activar auto-gen) │      │  frontier   │
   │ Failure handling (compensating + rollback)  │ 2.5  │ alta        │
   │ 6.3.1 Time-aware queries (DSL)              │ 2    │ media       │
   │ 6.3.2 Forgetting refined (GDPR + 5-layer)   │ 2.5  │ media       │
   │ 6.3.3 Memory observability dashboard        │ 1.5  │ simple(reuso)│
   │ 6.4.1 Memory regression (4 layers+7 canaries)│ 2.5 │ media       │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R6 (antes de margen frontier)      │ 47   │             │
   │ ⚠️ pero con experiencia alta y mucho ya       │ 33   │ (30-36)     │
   │ diseñado en Pre-Code, se ajusta a ~33        │      │             │
   └─────────────────────────────────────────────┴──────┴─────────────┘

   ⚠️ R6 es donde la incertidumbre es MÁXIMA. El Pre-Code Review ya
   resolvió 5 gaps de pseudocódigo (C.1-C.5), lo que REDUCE el tiempo
   (no se diseña al programar). Pero el debugging del bucle auto-
   modificante puede sorprender. Margen real aquí: ±40%.
```

### R7 — Frontend/Channel

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 7.1.1 Telegram production (8 components)     │ 2    │ media(reuso)│
   │ 7.1.2 REST API formal (8 comp + OpenAPI)    │ 2    │ media       │
   │ 7.1.3 GitHub App webhook (8 components)      │ 2    │ media       │
   │ 7.2.1 Output Gate (signing HMAC/Ed25519)    │ 2.5  │ alta        │
   │ 7.2.2 Response format (QA Pack + 4 renderers)│ 2.5 │ media       │
   │ 7.2.3 Streaming unificado (25+ events)      │ 2    │ media       │
   │ 7.3.1 Auth unificado (identity + 6 cred)    │ 2    │ media       │
   │ 7.3.2 RBAC (35+ permisos + roles)           │ 1.5  │ media       │
   │ 7.3.3 Session management (per-channel)      │ 1.5  │ media       │
   │ 7.4.1 Dashboard v2 (módulos + search)       │ 2    │ media(reuso)│
   │ 7.4.2 Notifications (multi-channel)         │ 1.5  │ simple      │
   │ 7.4.3 PWA + responsive                      │ 1.5  │ simple      │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R7                                 │ 23   │ (18-21)     │
   └─────────────────────────────────────────────┴──────┴─────────────┘

   Mucho reuso (PlatformAdapter de Hermes, SSE de R3, KEK de R4) → rápido.
```

### R8 — Observabilidad

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 8.1.1 Métricas por nodo (~3,500 series)     │ 2    │ media       │
   │ 8.1.2 Métricas cross-cutting + Tempo        │ 2    │ media       │
   │ 8.1.3 Unit economics real-time (5 comp)     │ 2    │ media       │
   │ 8.2.1 Operations Dashboard (Grafana)        │ 1.5  │ simple      │
   │ 8.2.2 Analytics Dashboard                   │ 1.5  │ simple      │
   │ 8.2.3 Scalability Dashboard + simulator     │ 1.5  │ simple      │
   │ 8.3.1 Audit Chain (ya foundation R2)        │ 1.5  │ media       │
   │ 8.3.2 Retention multi-tier + GDPR pseudonym │ 2    │ media       │
   │ 8.3.3 Audit Query Engine (6 templates)      │ 2    │ media       │
   │ 8.4.1 SLO/SLA (3 tiers + self-service)      │ 1.5  │ media       │
   │ 8.4.2 Alerts Aggregation (cross-system)     │ 2    │ media       │
   │ 8.4.3 Incident Management (lifecycle)       │ 1.5  │ simple      │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R8                                 │ 21   │ (14-17 con  │
   │   (mucho es provisioning + reuso de R2/R3)   │      │  reuso fuerte│
   └─────────────────────────────────────────────┴──────┴─────────────┘

   R8 es config + provisioning + reuso. Va más rápido de lo que parece.
```

### R9 — Security/Compliance

```
   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 9.1.1 Input Threat Scanner (5 capas)        │ 3    │ alta        │
   │ 9.1.2 Anomaly Detection (4 detectores+EWMA) │ 3    │ alta        │
   │ 9.1.3 Threat Coordinator (DEFCON+modula)    │ 2.5  │ alta        │
   │ 9.2.1 Threat Model STRIDE+DREAD (DOC)       │ 2    │ doc         │
   │ 9.2.2 Pentest Plan + custom attack suite    │ 3    │ media       │
   │ 9.2.3 Security Playbooks (8 PICERL+forensics)│ 2.5 │ media       │
   │ 9.3.1 SOC2 Control Mapping (DOC + evidence) │ 2    │ doc         │
   │ 9.3.2 GDPR Program (DSAR+consent+DPA+RoPA)  │ 2.5  │ media       │
   │ 9.3.3 Evidence + Gap + Readiness            │ 1.5  │ media(reuso)│
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R9                                 │ 22   │ (17-20)     │
   └─────────────────────────────────────────────┴──────┴─────────────┘

   Amígdala (9.1.x) es lo pesado. Compliance (9.3.x) es más doc que código.
```

### R10 — CI/CD/Deploy

```
   ⚠️ La parte CI/CD (10.1.1) ya se hizo en Fase 0. Aquí va el resto.

   ┌─────────────────────────────────────────────┬──────┬─────────────┐
   │ Sub-tema                                    │ Días │ Complejidad │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ 10.1.1 CI Pipeline (ampliar el de Fase 0)   │ 1.5  │ media       │
   │ 10.1.2 Build + Staging + migration dry-run  │ 2    │ media       │
   │ 10.1.3 Prod Deploy + rollback + health gate │ 2    │ media       │
   │ 10.2.1 Runtime systemd + Docker (services)  │ 2    │ media       │
   │ 10.2.2 Networking dual-plane (CF+Tailscale) │ 1.5  │ simple      │
   │ 10.2.3 Secrets KEK offline (TPM/USB)        │ 2    │ media       │
   │ 10.3.1 Backup multi-capa (WAL PITR)         │ 1.5  │ media       │
   │ 10.3.2 DR Testing (5 escenarios + RTO/RPO)  │ 2    │ media       │
   │ 10.3.3 Pre-flight + 12 ops runbooks (DOC)   │ 1.5  │ doc         │
   ├─────────────────────────────────────────────┼──────┼─────────────┤
   │ SUBTOTAL R10                                 │ 16   │ (14-17)     │
   └─────────────────────────────────────────────┴──────┴─────────────┘
```

---

## 5. Calendario consolidado

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  SUMA NETA (días-dev de código):                                   │
   │                                                                    │
   │   Fase 0:  4.5      R5:    36.5                                    │
   │   R1:      3.5      R6:    33  (ajustado por Pre-Code)            │
   │   R2:      32       R7:    23                                      │
   │   R3:      22.5     R8:    21                                      │
   │   R4:      28.5     R9:    22                                      │
   │                     R10:   16                                      │
   │   ─────────────────────────────────                               │
   │   NETO:    ~242 días-dev                                          │
   │                                                                    │
   │   ⚠️ AJUSTE: las sumas individuales arriba son "generosas" (con   │
   │   margen por sub-tema). Aplicando velocidad de dev senior con      │
   │   experiencia alta (reuso fuerte, sin curva en lo conocido), el    │
   │   neto realista baja a ~155-175 días-dev de código efectivo.       │
   │                                                                    │
   │   + OVERHEAD (~25%): refactors, debugging profundo, integración    │
   │     entre rondas, documentación = ~39-44 días                     │
   │   ──────────────────────────────────────────────                  │
   │   TOTAL: ~194-219 días-dev                                         │
   │                                                                    │
   │   A 5 días/semana (full-time):                                     │
   │   = ~39-44 semanas = ~9-10 meses                                   │
   └──────────────────────────────────────────────────────────────────┘
```

### Calendario por fase (acumulado)

```
   ┌────────┬────────────────────┬─────────────┬──────────────────────┐
   │ FASE   │ Rondas             │ Semanas     │ Acumulado            │
   ├────────┼────────────────────┼─────────────┼──────────────────────┤
   │ 0      │ Setup + CI/CD      │ ~1          │ Semana 1             │
   │ 1      │ R1+R2+R3+R4(B1B2)  │ ~12-14      │ Semana 13-15 ★MVP    │
   │ 2      │ R5                 │ ~5-6        │ Semana 18-21         │
   │ 3      │ R6 (Pilar 3)       │ ~6-7        │ Semana 24-28         │
   │ 4      │ R7+R8              │ ~6-7        │ Semana 30-35         │
   │ 5      │ R9+R10+R4 B3       │ ~7-8        │ Semana 37-43         │
   ├────────┴────────────────────┴─────────────┴──────────────────────┤
   │ TOTAL: ~39-44 semanas = ~9-10 meses (Brian solo, full-time)        │
   │                                                                    │
   │ ★ MVP PILOTABLE: Semana ~13-15 (~3-3.5 meses)                      │
   │ ▲ Hito Telegram: Semana ~6 (sub-conjunto del MVP) [LOCKED R1]      │
   └────────────────────────────────────────────────────────────────────┘

   NOTA: con Brian SOLO no hay paralelización (R7/R8 que en el Plan
   Maestro iban en paralelo, aquí van secuenciales). Por eso ~9-10 meses
   en vez de los ~6-9 de la estimación gruesa (que asumía 2 devs).
```

---

## 6. El MVP pilotable

El número más importante para ti: **¿en cuánto puedes mostrar algo a un cliente?**

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  MVP PILOTABLE = "For3s en Telegram + memoria + Claude + GitHub"   │
   │                                                                    │
   │  Incluye:  Fase 0 (setup+CI) + R1 + R2 + R3 + R4 (B1+B2)          │
   │                                                                    │
   │   Fase 0:        4.5 días                                          │
   │   R1:            3.5 días                                          │
   │   R2:            32 días   ← el grueso (cuello de botella)         │
   │   R3:            22.5 días                                         │
   │   R4 (B1+B2):    22 días   (B3 lifecycle se difiere post-MVP)      │
   │   ──────────────────────                                          │
   │   NETO:          ~84.5 días generosos → ~63-72 ajustado senior     │
   │   + overhead 25%: ~16-18 días                                     │
   │   ──────────────────────                                          │
   │   TOTAL MVP:     ~79-90 días = ~16-18 semanas                      │
   │                  ≈ ~3.5-4 meses                                    │
   │                                                                    │
   │   ▲ Pero el HITO TELEGRAM (R1 §10, sub-conjunto del MVP:           │
   │     CLI+Telegram+persistencia+profiles+installer SIN el KG/CLS/    │
   │     tools completos) = 6 SEMANAS [LOCKED, dato de los docs].       │
   │     Ese es el primer "se ve algo funcionando".                    │
   └──────────────────────────────────────────────────────────────────┘

   ESCALERA DE HITOS VISIBLES:
   • Semana ~6:    Telegram funcionando (hito R1 lockeado) — "habla conmigo"
   • Semana ~13-15: MVP pilotable real — "analiza PRs con memoria" → 1er pilot
   • Semana ~21:   + coordinación cognitiva (multi-agent, DMN)
   • Semana ~28:   + aprende solo (Pilar 3) — el diferenciador
   • Semana ~35:   + interfaz formal + observabilidad
   • Semana ~43:   PRODUCCIÓN completa (seguridad + deploy + compliance)
```

---

## 7. Factores que pueden mover los números

```
   ┌─────────────────────────────────────────┬──────────────────────────┐
   │ Factor                                  │ Impacto en el calendario │
   ├─────────────────────────────────────────┼──────────────────────────┤
   │ ↗️ ACELERA:                                                          │
   │ Contratar 1 dev en Fase 2+ (paraleliza  │ -20 a -30% (R7∥R8,       │
   │   R7/R8 mientras Brian hace R5/R6)      │ R9-doc∥código)           │
   │ Reuso de código de OpenClaw/Hermes      │ -10 a -15% en R1/R2/R7   │
   │ Pre-Code Review ya resolvió diseño R6   │ -2 a -4 semanas en R6    │
   │ AGE/pgvector sin sorpresas              │ -1 semana en R2          │
   ├─────────────────────────────────────────┼──────────────────────────┤
   │ ↘️ RETRASA:                                                          │
   │ R6 Pilar 3 debugging del bucle auto-mod │ +2 a +4 semanas (riesgo  │
   │   (lo más impredecible)                 │ #1 del calendario)       │
   │ AGE inmaduro da problemas (es joven)    │ +1 a +2 semanas en R2    │
   │ Pilots reales interrumpen (soporte)     │ +variable (bueno: revenue│
   │   durante la construcción               │ malo: distrae)           │
   │ Brian medio-tiempo en vez de full       │ ~×2 el calendario        │
   │ Imprevistos normales de software        │ ya en el ±30% del margen │
   └─────────────────────────────────────────┴──────────────────────────┘

   ESCENARIO REALISTA (con algunos retrasos R6 + reuso):  ~10-11 meses
   ESCENARIO OPTIMISTA (todo fluye + reuso fuerte):        ~8-9 meses
   ESCENARIO CON 1 CONTRATADO desde Fase 2:                ~7-8 meses
```

---

## 8. Diagrama: distribución del esfuerzo

Dónde se va el tiempo (días-dev netos generosos, ~242 base):

```
   R2  Data         ████████████████████████████████  32  (13%) ← cuello botella
   R5  Orchestration███████████████████████████████████ 36.5 (15%) ← 18 capas
   R6  Memory/Pilar3 █████████████████████████████████  33  (14%) ← más delicada
   R4  Tools        █████████████████████████████      28.5 (12%)
   R7  Frontend     ███████████████████████            23  (10%)
   R3  Model/LLM    ██████████████████████             22.5 (9%)
   R9  Security      ██████████████████████            22  (9%)
   R8  Observab.    █████████████████████              21  (9%)
   R10 Deploy       ████████████████                   16  (7%)
   Fase0+R1         ████████                           8   (3%)

   LECTURA: el 42% del esfuerzo está en 3 rondas (R2+R5+R6).
   Son el "núcleo cognitivo" — datos + coordinación + aprendizaje.
   Las rondas de gobierno (R8/R9/R10) son más livianas (config+reuso).
```

```
   POR TIPO DE TRABAJO:
   Lógica nueva compleja (R5,R6 núcleo):  ████████████████  ~35%
   Foundation/storage (R2):                ████████          ~14%
   Integración/reuso (R7,R8,R3):           ██████████████    ~28%
   Config/deploy (R10,R8 dashboards):      ██████            ~13%
   Documentación (threat model, runbooks): █████             ~10%
```

---

## 9. Cómo recalibrar

Esta estimación es v1. Para hacerla cada vez más exacta a medida que programas:

```
   1. Al terminar Fase 0 + primeros sub-temas de R2:
      → mide tu velocidad REAL (días reales vs estimados).
      → calcula tu "factor de calibración" (real/estimado).
      → aplica ese factor al resto del calendario.

   2. Lleva un registro simple:
      Sub-tema | estimado | real | factor
      → después de ~10 sub-temas, tu factor es confiable.

   3. R6 (Pilar 3) recalíbrala APARTE:
      es la más incierta; tu factor de R2-R5 puede no aplicar a R6.

   4. Actualiza este documento con los números reales conforme avances.
      Conviértelo en el "tracker" real de construcción.
```

---

## Cierre

```
   ╔═══════════════════════════════════════════════════════════════════╗
   ║   ESTIMACIÓN — Brian solo, full-time, experiencia alta             ║
   ║                                                                    ║
   ║   SISTEMA COMPLETO:    ~9-10 meses (~39-44 semanas)                ║
   ║   MVP PILOTABLE:       ~3.5-4 meses (~16-18 semanas)               ║
   ║   PRIMER HITO VISIBLE: ~6 semanas (Telegram, LOCKED)               ║
   ║                                                                    ║
   ║   El 42% del esfuerzo está en R2+R5+R6 (núcleo cognitivo).         ║
   ║   El mayor riesgo de calendario es R6 (Pilar 3, ±40%).            ║
   ║                                                                    ║
   ║   ⚠️ Margen ±30%. Realista: ~10-11 meses. Optimista: ~8-9.        ║
   ║   Con 1 contratado desde Fase 2: ~7-8 meses.                      ║
   ║                                                                    ║
   ║   Estos números son DERIVADOS, no de los docs. Recalibrar          ║
   ║   contra velocidad real tras Fase 0 (§9).                         ║
   ╚═══════════════════════════════════════════════════════════════════╝
```

**Decisión de negocio que estos números informan:**
- Runway necesario: ~10-12 meses de pista para llegar a producción solo.
- Punto de revenue posible: ~mes 4 (MVP pilotable → primer pilot pagando).
- Cuándo considerar contratar: si quieres bajar de 10 a ~7-8 meses, un dev en Fase 2.

---

**Fin de la Estimación de Tiempo por Sub-Tema.**

**Con esto, los 3 refuerzos pre-código quedan completos:**
- ✅ #1 Plan Maestro de Programación (el ORDEN)
- ✅ #2 Reconciliación de numeración de nodos
- ✅ #3 Estimación de tiempo por sub-tema (el TIEMPO) ← este
