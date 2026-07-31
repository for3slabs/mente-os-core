# Plan Maestro de Programación — For3s OS

**Status:** current · **Type:** fossil · **Updated:** 2026-07-30 · **Owner:** brian
**Migrated:** Doc/Plan_Maestro_Programacion.md → memory/archive/Plan_Maestro_Programacion.md (2026-07-30, ADR-029)

> **El cronograma de obra completo.** El diseño (las 10 rondas R1-R10) responde QUÉ construir. Este documento responde **EN QUÉ ORDEN se programa, qué depende de qué, qué es MVP vs diferido, qué se construye en paralelo, y qué gate hay que pasar antes de avanzar.** Es el mapa de ruta de la construcción de principio a fin, con diagramas y mapa de flujo de datos gráfico.

**Owner:** Brian López
**Fecha:** 2026-06-09
**Estatus:** ✅ Plan maestro de programación — la fuente única del ORDEN de construcción
**Capa:** Doc — planeación de ejecución (NO diseño; el diseño está completo en Cuerpo)
**Fuentes (datos reales, no inventados):**
- R10 §12 (secuencia oficial foundation-first)
- R1 §10 (cronograma lockeado del hito Telegram, 6 semanas)
- R6 Pre-Code §E (orden interno de programación de R6 + gates)
- Secciones "Implicaciones en rondas siguientes" de los 10 maestros (dependencias)
- `docs/analysis/Reporte_Maestro_Consolidado_R1-R10.md` §8 (estimación de tiempo derivada)

**Documentos hermanos:**
- `docs/analysis/Reporte_Maestro_Consolidado_R1-R10.md` — coherencia interna del sistema
- `docs/analysis/Reporte_Alineacion_R1-R10_vs_Grafo_Vision.md` — alineación con filosofía/visión
- Este = **CÓMO y CUÁNDO programarlo**

**⚠️ Nota de honestidad sobre tiempos:** los documentos maestros NO contienen estimaciones de tiempo de programación (solo el hito Telegram de R1 = 6 semanas, que SÍ es dato lockeado). Las estimaciones de tiempo de las fases posteriores son **DERIVADAS** (por complejidad + sub-temas + dependencias) y están marcadas `[EST.]`. No son datos de los docs. El refuerzo #3 (estimación detallada por sub-tema) las hará confiables.

---

## Tabla de contenidos

1. [Filosofía del plan](#1-filosofía-del-plan)
2. [Las 2 reglas de oro de la construcción](#2-las-2-reglas-de-oro)
3. [La secuencia oficial (de los docs)](#3-la-secuencia-oficial)
4. [Pre-requisitos antes de teclear la primera línea](#4-pre-requisitos-antes-de-teclear)
5. [Mapa de dependencias de construcción](#5-mapa-de-dependencias-de-construcción)
6. [Las 6 fases de construcción](#6-las-6-fases-de-construcción)
   - [FASE 0 — Setup + CI/CD temprano](#fase-0--setup--cicd-temprano)
   - [FASE 1 — MVP cerebral mínimo (el hito pilotable)](#fase-1--mvp-cerebral-mínimo)
   - [FASE 2 — Coordinación cognitiva](#fase-2--coordinación-cognitiva)
   - [FASE 3 — Aprendizaje y autonomía (núcleo Pilar 3)](#fase-3--aprendizaje-y-autonomía)
   - [FASE 4 — Interfaz y observabilidad](#fase-4--interfaz-y-observabilidad)
   - [FASE 5 — Seguridad, deploy y cierre](#fase-5--seguridad-deploy-y-cierre)
7. [Orden interno de R6 (la ronda más delicada)](#7-orden-interno-de-r6)
8. [Qué es MVP vs qué se difiere a v2/v3](#8-qué-es-mvp-vs-diferido)
9. [Qué se puede construir en paralelo](#9-qué-se-puede-construir-en-paralelo)
10. [Los gates de validación entre fases](#10-los-gates-de-validación)
11. [Diagrama: línea de tiempo de construcción (Gantt textual)](#11-diagrama-línea-de-tiempo)
12. [Diagrama: árbol de dependencias de construcción](#12-diagrama-árbol-de-dependencias)
13. [Mapa de flujo de datos — cómo se comporta la información](#13-mapa-de-flujo-de-datos)
14. [Estimación de tiempo consolidada](#14-estimación-de-tiempo-consolidada)
15. [Riesgos de construcción + mitigaciones](#15-riesgos-de-construcción)
16. [Checklist maestro de construcción](#16-checklist-maestro-de-construcción)

---

## 1. Filosofía del plan

```
   ╔═══════════════════════════════════════════════════════════════════╗
   ║   PRINCIPIO RECTOR: FOUNDATION-FIRST + MVP PILOTABLE TEMPRANO       ║
   ║                                                                    ║
   ║   No se construye el sistema completo antes de validar.            ║
   ║   Se construye en CAPAS, de abajo hacia arriba, y se llega a un    ║
   ║   MVP PILOTABLE (Telegram + memoria + LLM + GitHub) lo antes       ║
   ║   posible para validar mercado MIENTRAS se construye el resto.     ║
   ║                                                                    ║
   ║   Cada capa REUSA la anterior (nunca reinventa). El orden NO es    ║
   ║   arbitrario: es el orden de DEPENDENCIAS TÉCNICAS reales.         ║
   ║                                                                    ║
   ║   Alineado con Visión §11.1 ("saltar al frontier mata startups")  ║
   ║   y §8.2 ("MVP cerebral mínimo en 8-12 semanas").                 ║
   ╚═══════════════════════════════════════════════════════════════════╝
```

**La idea en una frase:** se construye el cimiento (R1-R2), luego el motor (R3-R4) → con eso ya hay un **MVP pilotable**, y a partir de ahí se añaden las capas cognitivas avanzadas (R5-R6), la interfaz (R7), y el gobierno (R8-R9-R10) — con CI/CD montado desde el día 1 para que todo se construya con red de seguridad.

---

## 2. Las 2 reglas de oro

### Regla 1 — CI/CD (R10 parcial) se monta TEMPRANO, no al final

```
   El número de ronda (R10) NO es el orden de construcción de TODO R10.
   La parte de CI/CD pipeline (R10 B1) se monta en FASE 0, ANTES de
   programar el resto, para que cada ronda se construya con:
   • tests automáticos desde el primer commit
   • security gates (SAST/Trivy) desde el inicio
   • el Pilar 3 GATE listo ANTES de activar auto-generación (R6)

   Fuente: R10 §12 literal — "Con CI/CD (R10) montado temprano para que
   el resto se programe con gates desde el inicio."
```

### Regla 2 — El Meta-Orchestrator (governor) se programa ANTES de soltar la autonomía

```
   El freno de seguridad del Pilar 3 (el governor de 6 frenos, R6 §A)
   DEBE existir ANTES de activar la auto-generación de skills (R6 paso 8).
   "Es el FRENO; debe existir ANTES de soltar el bucle."

   Fuente: R6 Pre-Code §E.1 paso 9 literal.
```

---

## 3. La secuencia oficial

Esto es **dato lockeado** de R10 §12, verbatim:

```
   R1 compute → R2 data → R3 LLM → R4 tools → R5 orchestration →
   R6 memory (post re-review) → R7 channels → R8 observability →
   R9 security → R10 deploy.

   Con CI/CD (R10) montado temprano para que el resto se programe
   con gates desde el inicio.
```

Este plan **respeta esa secuencia** pero la organiza en 6 fases con los matices de paralelización, MVP y gates que los docs detallan en sus secciones de dependencias.

---

## 4. Pre-requisitos antes de teclear

Lo que el propio diseño exige hacer ANTES de programar (de los flags críticos de los maestros + reportes):

```
   ┌────┬──────────────────────────────────────────┬─────────────────┐
   │ ✓  │ Pre-requisito                            │ Fuente          │
   ├────┼──────────────────────────────────────────┼─────────────────┤
   │ ✅ │ Re-revisión R6 crítica (Meta-Orchestrator)│ memory r6_critical│
   │    │ HECHA → Ronda_06_Pre_Code_Review_Detailed │ (2026-06-09)    │
   ├────┼──────────────────────────────────────────┼─────────────────┤
   │ ✅ │ Refinamiento DMN 5.4.2 (8 tasks)          │ memory dmn_tasks │
   │    │ HECHO → Ronda_05_DMN_Tasks_Detailed       │ (2026-06-09)    │
   ├────┼──────────────────────────────────────────┼─────────────────┤
   │ ✅ │ Reconciliar numeración de nodos           │ reporte align #2 │
   │    │ HECHA → Mapeo §0 canónico                 │ (2026-06-09)    │
   ├────┼──────────────────────────────────────────┼─────────────────┤
   │ ⏳ │ Medir PFC_PLANNING_COST real (bug B.7)    │ R6 Pre-Code B.7 │
   │    │ NO asumir $0.05 — instrumentar en R8 8.1.3 │ → durante FASE 3│
   ├────┼──────────────────────────────────────────┼─────────────────┤
   │ ⏳ │ Master KEK backup OFFLINE verificado      │ R4 4.1.4 / R10  │
   │    │ ANTES de producción (USB+paper+succession)│ → antes de prod │
   ├────┼──────────────────────────────────────────┼─────────────────┤
   │ ⏳ │ Cargar HARD NO-GO §8.4 (compliance)       │ R6 B2 / Grafo §8.4│
   │    │ bootstrap como common_stack al startup    │ → FASE 3         │
   └────┴──────────────────────────────────────────┴─────────────────┘

   → Los 3 pre-requisitos de DISEÑO ya están hechos. Los 3 ⏳ son de
   EJECUCIÓN (se atienden durante las fases correspondientes).
```

---

## 5. Mapa de dependencias de construcción

Qué necesita cada ronda de las anteriores para poder programarse. **No puedes programar X hasta tener sus dependencias.**

```
   RONDA   NO PUEDE EMPEZAR HASTA TENER...                    BLOQUEA A...
   ─────────────────────────────────────────────────────────────────────────
   R1      (nada — es la base)                                TODAS
   R2      R1 (Python/asyncio/SQLAlchemy)                     R3,R5,R6,R7,R8,R9,R10
   R3      R1 + R2 (memory tiers, Haiku, async patterns)      R4,R5,R6
   R4      R1+R2+R3 (ToolRegistry de R3, Valkey/Arq, KEK)     R5,R7,R9,R10
   R5      R2+R3+R4 (memory, LLM, 57 tools, AgentDelegation)  R6,R7
   R6      R2+R3+R5 (storage, eval, DMN, working mem, multi-ag) R7,R10(gate)
   R7      R3+R4+R5+R6 (SSE, Telegram MCP, routing, planning)  —
   R8      TODAS (instrumenta los 11 nodos)                    R9,R10
   R9      R4+R5+R8 (KEK, Tálamo/Neuromod/Microglia, audit)   R10
   R10     TODAS (despliega todo) — PERO su CI/CD va en FASE 0 PRODUCCIÓN
   ─────────────────────────────────────────────────────────────────────────

   LECTURA CLAVE:
   • R2 es el cuello de botella inicial — bloquea a 7 rondas. Hacerlo bien
     y rápido es lo más importante de las primeras semanas.
   • R6 depende de R5 (necesita DMN + working memory + multi-agent).
   • R8 y R9 pueden empezar parcialmente en paralelo a R5/R6 (instrumentan
     lo que ya existe).
   • R10 CI/CD se adelanta a FASE 0; R10 deploy se hace al final.
```

---

## 6. Las 6 fases de construcción

El plan agrupa las 10 rondas en 6 fases lógicas. Cada fase tiene: objetivo, qué se programa, qué entrega, y el gate para avanzar.

---

### FASE 0 — Setup + CI/CD temprano

```
   OBJETIVO: tener el esqueleto del proyecto + la red de seguridad (CI/CD)
   ANTES de programar lógica. Que cada commit posterior tenga tests + gates.

   QUÉ SE PROGRAMA:
   • R1 setup: uv init + estructura monorepo (apps/ packages/) + pyproject
   • R1 base: CI con ruff + ty + pytest (stage 1 de R10 B1)
   • R10 B1 PARCIAL: GitHub Actions pipeline básico (lint + unit + SAST)
     (NO el deploy completo — solo el pipeline de tests/gates)
   • Pilar 3 GATE skeleton (R10 10.1.1) — vacío pero listo para cuando
     R6 active auto-generación

   QUÉ ENTREGA:
   • Repo Python con CI verde + estructura de carpetas + installer base

   TIEMPO [EST.]: ~1 semana

   GATE PARA AVANZAR:
   ✓ CI corre en cada push (ruff + ty + pytest pasan)
   ✓ Estructura monorepo creada
   ✓ uv workspace funcional
```

---

### FASE 1 — MVP cerebral mínimo

```
   OBJETIVO: el HITO PILOTABLE. "For3s OS corriendo en Telegram con memoria
   real, razonando con Claude, analizando PRs de GitHub." Esto se puede
   mostrar a un pilot MIENTRAS se construye el resto.

   QUÉ SE PROGRAMA (R2 + R3 + R4, foundation-first):

   1. R2 Data Layer (LO MÁS IMPORTANTE — bloquea 7 rondas):
      • PostgreSQL 16 + AGE + pgvector + pgcrypto (extensiones)
      • Schemas: shared + wks_X (schema-per-tenant)
      • SQLAlchemy 2 + Alembic multi-schema
      • Event Sourcing (episodes_events, skills_events, audit_events + triggers)
      • Stella embeddings LOCAL @1024
      • 3 tiers de memoria (Working/Short/Long)
      • Microglía (forgetting) + CLS (consolidation HDBSCAN+Haiku)
      • Valkey + Arq + pgbouncer
      • Backup 3-2-1 (foundation)
      → Esto ES el cerebro de datos. Sin esto, nada más existe.

   2. R3 Model/LLM Layer:
      • ClaudeProvider (Sonnet/Opus/Haiku) + abstraction LLMProvider
      • FailoverManager OpenAI
      • Jinja2 prompts + context builder (15K budget)
      • Caching 4 capas
      • Streaming SSE + Token Bucket + Circuit Breaker
      • Cost tracking + P5 cap enforcement

   3. R4 Tools/MCP (PARCIAL para MVP):
      • mcp SDK + Discovery
      • Secrets KEK hierarchy
      • GitHub MCP (oficial) — el wedge QA
      • Filesystem MCP + HTTP MCP (custom)
      • Telegram MCP (custom + Hermes patterns)
      • Docker multi-tenant 3 capas (foundation)

   QUÉ ENTREGA:
   • For3s OS en Telegram, con memoria persistente, razonando con Claude,
     leyendo PRs de GitHub. PILOTABLE.
   • (El hito R1 §10 de 6 semanas es un sub-conjunto de esto: CLI+Telegram+
     persistencia+profiles+installer. FASE 1 lo extiende con KG+vector+tools.)

   TIEMPO [EST.]: ~11-15 semanas (R2: 4-6 · R3: 3-4 · R4: 3-4 · solapado)
   → coincide con Visión §8.2 "MVP cerebral mínimo 8-12 semanas"

   GATE PARA AVANZAR:
   ✓ Un PR de GitHub se analiza end-to-end (input → memoria → Claude → output)
   ✓ La memoria persiste entre sesiones (episodios + KG + vector)
   ✓ CLS consolida episodios a KG (job nocturno corre)
   ✓ Microglía poda (job nocturno corre, NO toca audit)
   ✓ Costo por análisis medido y dentro de P5
   ✓ Audit hash chain escribiendo (inmutable)
```

---

### FASE 2 — Coordinación cognitiva

```
   OBJETIVO: convertir el "wrapper LLM con memoria" (Fase 1) en un CEREBRO
   COORDINADO. Aquí nace la inteligencia de orquestación.

   QUÉ SE PROGRAMA (R5 completo):

   • Tálamo (Nodo 8): tool selection + context routing + 3 modos subgrafo
   • Neuromoduladores (Nodo 11): 4 modos globales
   • Dual-Process Check (Nodo 9): S1/S2 + history-aware + fast-path 3 layers
   • Multi-Agent Network: hub-and-spoke + 5 specialists + 18 capas defense
   • Cost control multi-agent (7 layers)
   • DMN (Nodo 6): idle detection + 8 tasks declarativas + 9 controles
     (usar Ronda_05_DMN_Tasks_Detailed.md para los 8 action_fn)

   QUÉ ENTREGA:
   • El agente decide tier LLM solo, enruta inteligente, paraleliza
     specialists, y procesa en background (DMN) cuando está idle.

   TIEMPO [EST.]: ~4-6 semanas (R5 es alta complejidad — 18 capas defense)

   GATE PARA AVANZAR:
   ✓ Dual-Process enruta correcto (query simple→Haiku, compleja→Opus)
   ✓ Multi-agent spawna 5 specialists en paralelo sin fuga cross-workspace
   ✓ Las 18 capas defense-in-depth testeadas (aislamiento + blocking + memory)
   ✓ DMN corre los 8 tasks en idle + respeta los 9 controles
   ✓ Cost control aborta si multi-agent excede budget
```

---

### FASE 3 — Aprendizaje y autonomía (núcleo Pilar 3)

```
   ⭐ LA FASE MÁS DELICADA. Aquí el sistema aprende solo. Requiere máximo
   cuidado porque es código auto-modificante.

   QUÉ SE PROGRAMA (R6 completo, en el orden interno de R6 §E):
   → Ver §7 de este documento para el orden EXACTO de los 10 pasos de R6.

   Resumen:
   1. Schemas + storage de skills (foundation)
   2. PFC core (plan-then-execute)
   3. Confidence (8 señales) + check loop (ask-human/re-plan)
   4. Skill application GO (shadow-heavy v1)
   5. Vía NO-GO (3 niveles HARD/SOFT/WARN)
   6. Dopaminergic scoring (TD-learning)
   7. Lifecycle manager (8 estados + sandbox)
   8. Plan→Skill promotion (7 fases)
   9. ⭐ META-ORCHESTRATOR (governor 6 frenos) — ANTES de activar paso 8
   10. Failure handling (compensating actions + rollback)

   ⚠️ AQUÍ se mide el PFC_PLANNING_COST real (bug B.7 — no asumir $0.05).
   ⚠️ AQUÍ se cargan los HARD NO-GO §8.4 (compliance).
   ⚠️ Bootstrap MUY CONSERVADOR (shadow-heavy, fallback PFC default).

   QUÉ ENTREGA:
   • El agente genera sus propias skills, las refuerza, las olvida, y se
     GOBIERNA (governor + kill switch). Pilar 3 ACTIVADO + GOBERNADO.

   TIEMPO [EST.]: ~5-7 semanas (la más larga — máxima delicadeza)

   GATE PARA AVANZAR (de R6 §E.2):
   ✓ Schemas Pydantic + RLS testeados (aislamiento workspace)
   ✓ Confidence calibration curve instrumentada
   ✓ PFC_PLANNING_COST medido real (no asumido)
   ✓ Governor gates funcionando ANTES de activar auto-generación
   ✓ Kill switch probado (congela generación)
   ✓ Compensating actions definidas para tools con efectos reales
   ✓ Sandbox eval independiente (golden + Microglia) funcionando
   ✓ HARD NO-GO bootstrap cargados
   ✓ Bootstrap MUY CONSERVADOR activo
```

---

### FASE 4 — Interfaz y observabilidad

```
   OBJETIVO: exponer el cerebro al mundo (canales formales + Output Gate)
   y poder VER todo lo que pasa (métricas + dashboards).

   QUÉ SE PROGRAMA (R7 + R8 — PUEDEN IR EN PARALELO):

   R7 Frontend/Channel:
   • Channels formales (Telegram production + REST API + GitHub App)
   • Output Gate (signing HMAC/Ed25519 + trace + encrypt)
   • QA Pack universal + 4 renderers
   • Auth/RBAC cross-channel (identity + sessions)
   • Dashboard v2 + notifications + PWA

   R8 Observabilidad (puede empezar antes, instrumentando lo que existe):
   • Prometheus (~5,150 series) instrumentando los 11 nodos
   • Grafana (Operations + Analytics + Scalability dashboards)
   • Audit Infrastructure formal (chain + triple redundancy + query engine)
   • SLO/SLA 3 tiers + alerts aggregation + incident management

   QUÉ ENTREGA:
   • Cliente interactúa formal (web/API/Telegram) con outputs firmados.
   • Brian ve todo en Grafana (30-sec glance) + audit consultable.

   TIEMPO [EST.]: ~5-7 semanas (R7: 3-4 · R8: 2-3 · solapado)

   GATE PARA AVANZAR:
   ✓ Output Gate firma cada respuesta (verificable por cliente)
   ✓ Auth cross-channel funciona (Telegram+REST+GitHub linkeados)
   ✓ Prometheus instrumenta los 11 nodos + Grafana muestra
   ✓ SLO tracking per workspace + alerts disparan
   ✓ Audit query engine + compliance templates funcionan
```

---

### FASE 5 — Seguridad, deploy y cierre

```
   OBJETIVO: cerrar las defensas (Amígdala + compliance) y poner TODO
   a correr en producción de forma segura/operable/recuperable.

   QUÉ SE PROGRAMA (R9 + R10 completo):

   R9 Security/Compliance:
   • Amígdala (Nodo 7): scanner 5 capas + anomaly + threat coordinator DEFCON
   • Threat model STRIDE+DREAD (doc) + custom attack suite (regression)
   • Security playbooks PICERL + ForensicsKit
   • SOC2 5 TSC mapping + GDPR program + readiness

   R10 Deploy (la parte que faltaba — CI/CD ya está de FASE 0):
   • Runtime híbrido (systemd + Docker)
   • Networking dual-plane (Cloudflare + Tailscale)
   • Secrets KEK offline bootstrap (TPM/USB)
   • Backup completo + WAL PITR + DR testing (cierra SOC2 A1.3)
   • Pre-flight + ops runbooks

   QUÉ ENTREGA:
   • For3s OS DEPLOYABLE + OPERABLE + RECUPERABLE en producción.
   • Perímetro Pilar 1 completo (Amígdala INPUT + Output Gate OUTPUT).
   • Compliance audit-ready (~90-95%).

   TIEMPO [EST.]: ~5-7 semanas (R9: 3-4 · R10: 2-3 · algo solapado)

   GATE PARA PRODUCCIÓN:
   ✓ Amígdala bloquea cada payload del custom attack suite (regression)
   ✓ Pilar 3 gate enforced (auto-gen NUNCA a prod sin aprobación Brian)
   ✓ DR testing real pasa (RTO/RPO medidos)
   ✓ Master KEK backup OFFLINE verificado
   ✓ Pre-flight checklist 11 checks pasa
   ✓ Deploy graceful + auto-rollback probado
```

---

## 7. Orden interno de R6 (la ronda más delicada)

R6 (Fase 3) es la única ronda que tiene su PROPIO orden de programación documentado (R6 Pre-Code §E.1), porque es código auto-modificante y el orden importa para la seguridad. **Dato lockeado, verbatim:**

```
   ┌────┬─────────────────────────────────────────────┬──────────────────┐
   │ #  │ Qué programar                               │ Por qué ese orden│
   ├────┼─────────────────────────────────────────────┼──────────────────┤
   │ 1  │ Schemas + storage (6.2.1)                   │ foundation, todo  │
   │    │ SkillMetadata + Postgres + RLS + FS layout  │ depende de esto   │
   │ 2  │ PFC core (6.1.1)                            │ el motor de       │
   │    │ PFCPlan + PlanStep + executor + pre-flight  │ ejecución         │
   │ 3  │ Confidence (6.1.2) + Check loop (6.1.3)     │ calidad ejecución │
   │    │ scoring 8 señales + re-plan (bootstrap pesim)│ (pesimista B.3)   │
   │ 4  │ Skill application GO (6.2.2)                 │ aplicar skills    │
   │    │ _skill_to_plan + parser + PFCRouter         │ (shadow-heavy v1) │
   │ 5  │ Vía NO-GO (6.2.3)                           │ SEGURIDAD         │
   │    │ checker + HARD bootstrap + TTL              │ (categoría 1)     │
   │ 6  │ Dopaminergic (6.2.4)                        │ aprendizaje       │
   │    │ scoring + lifecycle (decay 0.98)           │                  │
   │ 7  │ Lifecycle manager (6.2.5)                   │ state machine +   │
   │    │ 8 estados + sandbox + microglia + APIs      │ sandbox           │
   │ 8  │ Plan→Skill promotion (6.1.4)                │ GENERACIÓN        │
   │    │ 7 fases + sandbox eval independiente        │ (conservador)     │
   │ 9  │ ⭐ META-ORCHESTRATOR (§A)                    │ EL FRENO — debe   │
   │    │ governor 6 frenos + kill switch             │ existir ANTES de  │
   │    │ → EN PARALELO/ANTES del paso 8              │ soltar el bucle   │
   │ 10 │ Failure handling (§D)                       │ transversal —     │
   │    │ compensating actions + rollback             │ integrar en (2)   │
   └────┴─────────────────────────────────────────────┴──────────────────┘

   ⚠️ REGLA CRÍTICA: el paso 9 (governor) se programa ANTES de activar
   el paso 8 (auto-generación). El freno antes de soltar el motor.
```

---

## 8. Qué es MVP vs diferido

Separar lo que va en v1 (MVP pilotable) de lo que se difiere a v2/v3. **Esto evita el riesgo #1 de la Visión (sobre-engineering antes de validar).**

```
   ┌──────────────────────────────────────┬──────────┬─────────────────┐
   │ Componente                           │ MVP v1?  │ Fase / Versión  │
   ├──────────────────────────────────────┼──────────┼─────────────────┤
   │ Memoria (R2 completo)                │ ✅ SÍ    │ Fase 1          │
   │ LLM + caching + cost (R3)            │ ✅ SÍ    │ Fase 1          │
   │ GitHub + Telegram + FS + HTTP tools  │ ✅ SÍ    │ Fase 1          │
   │ Docker multi-tenant 3 capas          │ ✅ SÍ    │ Fase 1          │
   │ Tálamo + Dual-Process + Neuromod     │ ✅ SÍ    │ Fase 2          │
   │ Multi-Agent (5 specialists)          │ ✅ SÍ    │ Fase 2          │
   │ DMN (8 tasks)                        │ ✅ SÍ    │ Fase 2          │
   │ PFC + Skills GO/NO-GO + dopaminergic │ ✅ SÍ    │ Fase 3          │
   │ Meta-Orchestrator (governor)         │ ✅ SÍ    │ Fase 3          │
   │ Output Gate + Auth + Dashboard       │ ✅ SÍ    │ Fase 4          │
   │ Observabilidad (Prometheus/Grafana)  │ ✅ SÍ    │ Fase 4          │
   │ Amígdala + threat model + compliance │ ✅ SÍ    │ Fase 5          │
   │ Deploy + DR + backup                 │ ✅ SÍ    │ Fase 5          │
   ├──────────────────────────────────────┼──────────┼─────────────────┤
   │ R4 B4 (Slack/Notion/Google/dominios) │ ❌ NO    │ v2              │
   │ Auto-scaling distribuido / K8s       │ ❌ NO    │ v2/v3           │
   │ Multi-agent bus Valkey (cross-worker)│ ❌ NO    │ v2              │
   │ Pilar 3 cap #2 (KG relaciones auto)  │ ❌ NO    │ v3              │
   │ Pilar 3 cap #3 (sub-agentes auto)    │ ❌ NO    │ v3              │
   │ Pilar 3 cap #4 (modos auto)          │ ❌ NO    │ v3              │
   │ Routing automático per-request (R3)  │ ❌ NO    │ v2              │
   │ Pentest externo + SOC2 cert real     │ ❌ NO    │ v2 (post-rev.)  │
   │ ZK/RISC Zero                         │ ❌ NO    │ research        │
   │ Tree of Thoughts / Graph of Thoughts │ ❌ NO    │ v2/v3           │
   │ Predictive coding / world models     │ ❌ NO    │ v3+             │
   └──────────────────────────────────────┴──────────┴─────────────────┘

   REGLA: el MVP v1 incluye los 11 nodos + 3 pilares en su forma v1
   (Pilar 2 monolito, Pilar 3 capacidad #1). Lo diferido es escala
   distribuida + capacidades generativas avanzadas + integraciones extra.
```

---

## 9. Qué se puede construir en paralelo

No todo es estrictamente secuencial. Lo que se puede solapar (con 2 devs, o un dev alternando):

```
   ┌───────────────────────────────────────────────────────────────────┐
   │  SECUENCIAL OBLIGATORIO (no se puede paralelizar):                  │
   │  R1 → R2 → R3 → R4    (cada uno necesita al anterior)              │
   │  R5 → R6              (R6 necesita DMN + working mem de R5)         │
   │                                                                    │
   │  PARALELIZABLE:                                                    │
   │  • R8 (observabilidad) puede EMPEZAR en paralelo a R5/R6 —         │
   │    instrumenta lo que ya existe. Se completa en Fase 4.            │
   │  • R7 (frontend) puede empezar en paralelo a la 2da mitad de R6 — │
   │    los channels no dependen del Pilar 3 completo.                  │
   │  • R9 threat model (doc) puede escribirse en paralelo a R8.        │
   │  • R10 CI/CD va en FASE 0 (paralelo conceptual a todo).            │
   │                                                                    │
   │  DENTRO DE R6 (Fase 3):                                            │
   │  • El governor (paso 9) puede construirse en paralelo a los        │
   │    pasos 1-7, pero DEBE estar listo antes del paso 8.              │
   │  • Failure handling (paso 10) se integra en el executor (paso 2). │
   └───────────────────────────────────────────────────────────────────┘

   AHORRO POR PARALELIZACIÓN [EST.]:
   Secuencial puro: ~30-44 semanas
   Con paralelización (R8∥R5/R6, R7∥R6-2da-mitad, R9-doc∥R8): ~24-36 semanas
```

---

## 10. Los gates de validación

Un "gate" es un checkpoint: NO avanzas a la siguiente fase hasta pasarlo. Consolidados de las secciones de gate de cada ronda.

```
   ┌──────────┬───────────────────────────────────────────────────────┐
   │ GATE     │ Criterio para pasar (resumen — detalle en cada fase §6) │
   ├──────────┼───────────────────────────────────────────────────────┤
   │ GATE 0→1 │ CI verde + estructura monorepo + uv funcional          │
   │ GATE 1→2 │ PR analizado E2E + memoria persiste + CLS/Microglía    │
   │          │ corren + costo medido + audit chain escribe           │
   │ GATE 2→3 │ Dual-Process enruta + multi-agent 5 specialists sin    │
   │          │ fuga + 18 capas testeadas + DMN 8 tasks corren        │
   │ GATE 3→4 │ ⭐ governor ANTES de auto-gen + kill switch probado +  │
   │          │ PFC_PLANNING_COST medido + sandbox eval indep +       │
   │          │ HARD NO-GO cargados + bootstrap conservador           │
   │ GATE 4→5 │ Output Gate firma + auth cross-channel + Prometheus    │
   │          │ 11 nodos + SLO tracking + audit query engine          │
   │ GATE →PROD│ Amígdala bloquea attack suite + Pilar 3 gate + DR     │
   │          │ testing pasa + KEK backup verificado + pre-flight 11   │
   └──────────┴───────────────────────────────────────────────────────┘

   PRINCIPIO: cada gate es un punto donde PODRÍAS lanzar un pilot.
   Después de GATE 1→2 ya tienes un MVP pilotable real.
```

---

## 11. Diagrama: línea de tiempo de construcción

Gantt textual con las 6 fases, dependencias y paralelización. Tiempos `[EST.]` (excepto Fase 1 hito Telegram que es lockeado).

```
   SEMANA →   1   2   3   4   5   6   7   8   9  10  11  12 ... 24      36
   ─────────────────────────────────────────────────────────────────────────
   FASE 0    ███  (setup + CI/CD)
   Setup+CI

   FASE 1        ████████████████████  (MVP cerebral mínimo)
   R2 data       ██████████            (4-6 sem · bloquea todo)
   R3 LLM              ████████        (3-4 sem)
   R4 tools                ████████    (3-4 sem)
   ▲ hito Telegram (R1 §10, sem ~4-6) ──┘
   ★ GATE 1→2 ── MVP PILOTABLE AQUÍ ───────────────────┘

   FASE 2                          ████████████  (coordinación R5)
   R5 orchestr.                    ████████████  (4-6 sem · alta complej.)

   FASE 3                                      ██████████████  (Pilar 3 R6)
   R6 memory                                   ██████████████  (5-7 sem · ⭐delicada)

   FASE 4 (paralelizable)
   R8 observ.              ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄████████  (empieza parcial ∥ R5/R6)
   R7 frontend                                    ████████  (3-4 sem ∥ R6 2da mitad)

   FASE 5
   R9 security                                            ████████  (3-4 sem)
   R10 deploy                                                   ██████  (2-3 sem)
   ★ GATE →PROD ─────────────────────────────────────────────────────┘

   LEYENDA: ███ trabajo activo · ┄┄┄ trabajo parcial/preparatorio
            ▲ hito lockeado · ★ gate de validación
   ─────────────────────────────────────────────────────────────────────────
   TOTAL [EST.] con paralelización: ~24-36 semanas (~6-9 meses, 1-2 devs)
   MVP PILOTABLE [EST.]: ~11-15 semanas (~3-4 meses) — Visión §8.2 confirma 8-12
```

---

## 12. Diagrama: árbol de dependencias de construcción

Qué bloquea a qué. Las flechas = "necesita primero a".

```
                          ┌──────────┐
                          │   R1     │  (sustrato — bloquea TODO)
                          │ Compute  │
                          └────┬─────┘
                               │
                          ┌────▼─────┐
                          │   R2     │  ◄── cuello de botella inicial
                          │  Data    │      (bloquea 7 rondas)
                          └────┬─────┘
                  ┌────────────┼────────────┐
                  │            │            │
             ┌────▼───┐   ┌────▼────┐       │
             │  R3    │   │ R8 (∥)  │       │   R8 puede empezar parcial
             │  LLM   │   │ Observ. │       │   instrumentando R2/R3
             └────┬───┘   └─────────┘       │
                  │                          │
             ┌────▼───┐                      │
             │  R4    │                      │
             │ Tools  │                      │
             └────┬───┘                      │
        ┌─────────┼──────────┐               │
        │         │          │               │
   ┌────▼───┐ ┌───▼────┐ ┌───▼────┐          │
   │  R5    │ │ R9 doc │ │ R7 (∥) │          │   R9 threat model (doc)
   │ Orch.  │ │ threat │ │ channel│          │   y R7 channels pueden
   └────┬───┘ └────────┘ └────────┘          │   adelantarse parcial
        │                                     │
   ┌────▼───┐                                 │
   │  R6    │  ◄── núcleo Pilar 3 (más delicada)
   │ Memory │      contiene su propio orden interno (§7)
   └────┬───┘
        │
   ┌────▼────────────────────────────────────▼──┐
   │  R8 completo + R9 completo                   │  (instrumentan/aseguran
   │  (necesitan TODOS los nodos listos)          │   todo lo construido)
   └────┬─────────────────────────────────────────┘
        │
   ┌────▼───┐
   │  R10   │  (despliega TODO — CI/CD ya estaba de Fase 0)
   │ Deploy │
   └────────┘

   CAMINO CRÍTICO (lo que NO se puede acortar):
   R1 → R2 → R3 → R4 → R5 → R6 → R10
   (R7/R8/R9 cuelgan de este camino pero algunos paralelizan)
```

---

## 13. Mapa de flujo de datos

Cómo se comporta la INFORMACIÓN al viajar por el sistema construido. Tres vistas: (A) flujo de un request en runtime, (B) flujo de aprendizaje (background), (C) flujo de la información a través de las capas de almacenamiento.

### 13.A — Flujo de un request (runtime, con cliente)

```
   ┌─────────────┐
   │   CLIENTE   │  PR / query / comando
   └──────┬──────┘
          │ ① entra (Telegram/REST/GitHub)
          ▼
   ╔══════════════════╗
   ║ R7 CHANNEL       ║  normaliza → NormalizedMessage
   ║ + WORKSPACE GATE ║  auth + RBAC + carga keys del workspace
   ╚════════╤═════════╝
            │ ② input autenticado + workspace_id
            ▼
   ╔══════════════════╗
   ║ R9 AMÍGDALA      ║  scanner 5 capas (heurística→normalize→Haiku→
   ║ (INPUT GUARD)    ║  canary→external sanit.)
   ╚════════╤═════════╝  ¿CRITICAL? → ⛔ FAST-PATH BLOCK + alert Brian
            │ ③ input limpio + threat_score
            │   (modula ↓ Tálamo/Neuromod/Microglia si amenaza)
            ▼
   ╔══════════════════╗
   ║ R5 TÁLAMO        ║  ④ tool selection (Stella) + context routing
   ║ + NEUROMOD       ║     + subgraph mode + modo global
   ╚════════╤═════════╝
            ▼
   ╔══════════════════╗
   ║ R5 DUAL-PROCESS  ║  ⑤ S1/S2 + fast-path (cache exact→semántico→
   ║                  ║     heurística) → decide tier (Haiku/Sonnet/Opus)
   ╚════════╤═════════╝
            ▼
   ╔══════════════════╗
   ║ R6 PFC           ║  ⑥ ¿skill aplica? SÍ→skill_to_plan / NO→plan LLM
   ║ ORCHESTRATOR     ║     genera PFCPlan estructurado
   ╚════════╤═════════╝
            │
     ┌──────┼──────────────┬──────────────┬──────────────┐
     ▼ ⑦a   ▼ ⑦b           ▼ ⑦c          ▼ ⑦d            │
   ┌──────┐┌──────────┐  ┌─────────┐  ┌──────────────┐    │
   │R2 KG ││ R3 LLM   │  │ R4 TOOLS│  │R5 MULTI-AGENT│    │
   │+ Hip ││ Claude   │  │ 57 tools│  │ 5 special.   │    │
   │+ Vec ││ (caching)│  │ (KEK)   │  │ (18 capas)   │    │
   └───┬──┘└────┬─────┘  └────┬────┘  └──────┬───────┘    │
       │        │             │              │            │
       └────────┴──────┬──────┴──────────────┘            │
                       ▼ ⑧ resultados consolidados         │
   ╔══════════════════╗                                    │
   ║ R6 CONFIDENCE    ║  ⑨ ¿confío? (8 señales)            │
   ║ CHECK            ║     NO→re-plan/ask-human · SÍ→sigue │
   ╚════════╤═════════╝                                    │
            ▼                                              │
   ╔══════════════════╗                                    │
   ║ R7 OUTPUT GATE   ║  ⑩ firma (HMAC/Ed25519) + trace +  │
   ║                  ║     encrypt → QA Pack + renderer    │
   ╚════════╤═════════╝                                    │
            ▼                                              │
   ┌─────────────┐                                         │
   │   CLIENTE   │  QA Pack + Trace + Confidence + Audit   │
   └─────────────┘     (firmado, verificable)              │
                                                           │
   ═══ TRANSVERSAL (cada paso, no en secuencia) ═══════════┘
   [R8] Prometheus métricas + Tempo trace (cada ① a ⑩)
   [R2/R8] audit_events hash chain inmutable (cada decisión)
```

### 13.B — Flujo de aprendizaje (background, sin cliente)

```
   ⏰ IDLE / NIGHTLY / CRON — el sistema mejora solo

   ┌─────────────────────────────────────────────────────────────┐
   │  workspace IDLE detectado (R5 DMN scheduler)                  │
   └──────────────────────────┬───────────────────────────────────┘
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │ [R5 DMN] 8 tasks corren:                                       │
   │  housekeeping (5): embedding_precompute · cache_prewarming ·   │
   │    memory_consolidation · routing_learning · eval_regression   │
   │  generativas (3): pattern_detection · hypothesis_generation ·  │
   │    prompt_improvement                                          │
   └──────────────────────────┬───────────────────────────────────┘
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
   ┌──────────────┐  ┌────────────────┐  ┌──────────────────┐
   │ [R2 CLS]     │  │ [R6 governor]  │  │ [R2 Microglía]   │
   │ 2 AM:        │  │ gobierna las   │  │ 3 AM: forgetting │
   │ episódica →  │  │ skills/patterns│  │ soft+decay+arch  │
   │ semántica    │  │ generadas      │  │ (NO toca audit)  │
   │ (HDBSCAN +   │  │ (6 frenos +    │  │                  │
   │  Haiku → KG) │  │  kill switch)  │  │                  │
   └──────┬───────┘  └────────┬───────┘  └──────────────────┘
          │                   │
          ▼                   ▼
   ┌──────────────┐  ┌────────────────────┐
   │ KG enriquece │  │ skill candidata →  │
   │ (nuevos      │  │ review queue →     │
   │  conceptos)  │  │ Brian aprueba →    │
   │              │  │ promueve (gobernado)│
   └──────────────┘  └────────────────────┘
          │
          ▼
   ┌──────────────────────────────────────────────────────────────┐
   │ [R10] Backup 4-5 AM: 3-2-1 (Postgres+WAL → USB + R2)          │
   │ chain-preserving (audit forensic-valid tras restore)          │
   └──────────────────────────────────────────────────────────────┘

   RESULTADO: el sistema es MEJOR mañana que ayer (consolidó memoria,
   aprendió patrones, generó skills gobernadas, podó ruido, respaldó).
```

### 13.C — Flujo de la información a través del almacenamiento (3 tiers)

```
   Cómo un dato VIAJA por las capas de memoria a lo largo de su vida:

   [1] EVENTO OCURRE (request procesado)
        │
        ▼
   ┌─────────────────────┐
   │ TIER 1 — WORKING    │  R2/R6 · in-process Python (15 items, TTL 60min)
   │ (PFC Nodo 3)        │  "lo que tengo en mente AHORA"
   └──────────┬──────────┘
              │ al cerrar sesión → flush
              ▼
   ┌─────────────────────┐
   │ TIER 2 — SHORT-TERM │  R2 · Postgres episodes_events (ES inmutable)
   │ (Hipocampo Nodo 2)  │  + episodes_state + pgvector HNSW (Stella @1024)
   │ + Pattern Sep       │  "qué pasó esta semana" (30-90 días)
   └──────────┬──────────┘
              │ CLS nocturno (2 AM) si repetido N veces
              ▼
   ┌─────────────────────┐
   │ TIER 3 — LONG-TERM  │  R2 · Apache AGE (KG Cypher) + concepts pgvector
   │ (KG Nodo 1)         │  "conocimiento consolidado permanente"
   └──────────┬──────────┘
              │
              │ ┌─── Microglía (Nodo 5) poda Tier 2 cuando:
              │ │    stale 30d + relevance<0.3 + consolidated_to_kg=true
              │ │    (NUNCA toca audit_events ni events tables)
              │ ▼
   ┌─────────────────────┐
   │ COLD / ARCHIVE      │  episodes_archived (sin HNSW) → purge 12 meses
   └─────────────────────┘

   ═══ PARALELO E INMUTABLE (nunca se borra) ═══
   ┌─────────────────────┐
   │ AUDIT CHAIN         │  R2/R8 · audit_events hash chain SHA-256
   │ (Pilar 1 §6.4)      │  append-only · trigger bloquea UPDATE/DELETE
   │                     │  triple redundancy: Postgres + WAL + R2 (R8/R10)
   └─────────────────────┘

   DATO CLAVE: la información FLUYE hacia arriba (Working→Short→Long) por
   consolidación, y se PODA hacia abajo (Short→Archive) por microglía.
   El audit es la única capa que NUNCA se toca. Postgres contiene TODO
   (Tiers 2/3 + audit) = un solo backup protege todo el cerebro.
```

---

## 14. Estimación de tiempo consolidada

```
   ⚠️ RECORDATORIO: excepto el hito Telegram de R1 (6 sem, LOCKED), todos
   los tiempos son [ESTIMADOS] por complejidad. El refuerzo #3 los hará
   confiables con estimación detallada por sub-tema.

   ┌────────┬─────────────────────────┬────────────┬───────────────────┐
   │ FASE   │ Rondas                  │ Tiempo[EST]│ Acumulado [EST]   │
   ├────────┼─────────────────────────┼────────────┼───────────────────┤
   │ 0      │ Setup + CI/CD           │ 1 sem      │ 1 sem             │
   │ 1      │ R2 + R3 + R4 (MVP)      │ 11-15 sem  │ 12-16 sem ★MVP    │
   │ 2      │ R5 orchestration        │ 4-6 sem    │ 16-22 sem         │
   │ 3      │ R6 memory (Pilar 3)     │ 5-7 sem    │ 21-29 sem         │
   │ 4      │ R7 + R8 (∥)             │ 5-7 sem    │ 24-34 sem*        │
   │ 5      │ R9 + R10 deploy         │ 5-7 sem    │ 29-41 sem*        │
   ├────────┴─────────────────────────┴────────────┴───────────────────┤
   │ SECUENCIAL PURO [EST]:           ~30-44 semanas (~7-11 meses)       │
   │ CON PARALELIZACIÓN [EST]:        ~24-36 semanas (~6-9 meses)        │
   │ * paralelización: R8∥R5/R6, R7∥R6, R9-doc∥R8 reduce el acumulado    │
   │                                                                     │
   │ ★ MVP PILOTABLE [EST]:           ~11-15 semanas (~3-4 meses)        │
   │   → coincide con Visión §8.2 "MVP cerebral mínimo 8-12 semanas"     │
   │                                                                     │
   │ ▲ HITO TELEGRAM [LOCKED R1]:     6 semanas (sub-conjunto del MVP)   │
   └─────────────────────────────────────────────────────────────────────┘

   ASUNCIONES de la estimación:
   • 1-2 devs (Brian + posible contratado).
   • Reuso del diseño completo (no hay re-diseño, solo programar).
   • CI/CD desde Fase 0 (acelera al detectar bugs temprano).
   • No incluye: pentest externo, SOC2 cert real, onboarding de pilots.

   ⚠️ Estos números pueden variar ±30% según experiencia del dev con el
   stack (Python+Postgres+Claude) y cuántos imprevistos surjan en R6
   (la ronda más delicada). Es una guía de planeación, no un compromiso.
```

---

## 15. Riesgos de construcción

Riesgos específicos del PROCESO de programar (no del diseño). Qué puede salir mal al construir.

```
   ┌──────────────────────────────────────┬──────────────────────────────┐
   │ Riesgo de construcción               │ Mitigación                   │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ R2 (cuello de botella) tarda más de   │ Empezar R2 primero, dedicarle │
   │ lo previsto → retrasa TODO            │ foco total. Es lo que bloquea │
   │                                       │ 7 rondas.                    │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ R6 Pilar 3 (auto-modificante) genera  │ Bootstrap MUY CONSERVADOR +   │
   │ bugs sutiles peligrosos               │ governor ANTES de soltar +    │
   │                                       │ shadow-heavy v1 + kill switch │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ Construir sin CI → bugs se acumulan   │ CI/CD en Fase 0 (regla de oro │
   │ y se descubren tarde                  │ #1). Tests desde commit 1.    │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ Tentación de saltar al frontier       │ Disciplina MVP: GATE 1→2 antes│
   │ (ToT/multi-agent complejo) antes      │ de Fase 2. Diferir v2/v3 lo   │
   │ del MVP                               │ marcado en §8.                │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ Master KEK mal respaldado → pérdida   │ Verificar backup OFFLINE      │
   │ irrecuperable de secrets              │ (USB+paper+succession) ANTES  │
   │                                       │ de producción.               │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ Bus factor 1 (Brian solo) → si Brian  │ Runbooks Git + ONBOARDING.md  │
   │ no está, nadie puede operar           │ + documentar mientras se      │
   │                                       │ construye (R10 B3).          │
   ├──────────────────────────────────────┼──────────────────────────────┤
   │ Estimación de tiempo optimista        │ Hacer el refuerzo #3 (estim.  │
   │ (los docs no la tienen)               │ por sub-tema) antes de        │
   │                                       │ comprometer fechas a pilots. │
   └──────────────────────────────────────┴──────────────────────────────┘
```

---

## 16. Checklist maestro de construcción

El "to-do" de alto nivel para programar For3s OS de principio a fin.

```
   FASE 0 — Setup + CI/CD
   [ ] uv init + estructura monorepo (apps/ packages/)
   [ ] CI: ruff + ty + pytest verde
   [ ] GitHub Actions pipeline (lint + unit + SAST)
   [ ] Pilar 3 GATE skeleton (vacío, listo para R6)

   FASE 1 — MVP cerebral mínimo
   [ ] R2: Postgres + AGE + pgvector + schemas + ES + triggers
   [ ] R2: Stella embeddings + 3 tiers + Microglía + CLS
   [ ] R2: Valkey + Arq + pgbouncer + backup foundation
   [ ] R3: ClaudeProvider + failover + caching + streaming + cost
   [ ] R4: mcp SDK + KEK + GitHub/FS/HTTP/Telegram MCP + Docker 3-capas
   [ ] ★ GATE 1→2: PR analizado E2E + memoria persiste + costo medido
   [ ] → MVP PILOTABLE (mostrable a un pilot)

   FASE 2 — Coordinación cognitiva
   [ ] R5: Tálamo + Neuromod + Dual-Process + fast-path
   [ ] R5: Multi-Agent (5 specialists + 18 capas defense)
   [ ] R5: DMN (8 tasks de Ronda_05_DMN_Tasks_Detailed)
   [ ] ★ GATE 2→3: dual-process enruta + multi-agent sin fuga + DMN corre

   FASE 3 — Aprendizaje y autonomía (orden interno §7)
   [ ] R6 paso 1-2: Schemas skills + PFC core
   [ ] R6 paso 3: Confidence + check loop (medir PFC_PLANNING_COST real)
   [ ] R6 paso 4-5: Skill GO + NO-GO (HARD blocks §8.4)
   [ ] R6 paso 6-7: Dopaminergic + lifecycle manager
   [ ] R6 paso 9: ⭐ META-ORCHESTRATOR (ANTES del paso 8)
   [ ] R6 paso 8: Plan→Skill promotion (auto-generación)
   [ ] R6 paso 10: Failure handling (rollback)
   [ ] ★ GATE 3→4: governor + kill switch + sandbox eval + bootstrap conserv.

   FASE 4 — Interfaz y observabilidad (paralelo)
   [ ] R8: Prometheus 11 nodos + Grafana + audit infra + SLO
   [ ] R7: channels formales + Output Gate + Auth + Dashboard
   [ ] ★ GATE 4→5: Output Gate firma + auth cross-channel + Prometheus

   FASE 5 — Seguridad, deploy y cierre
   [ ] R9: Amígdala + threat model + attack suite + playbooks + compliance
   [ ] R10: runtime systemd+Docker + dual-plane + KEK offline
   [ ] R10: backup completo + DR testing + pre-flight + runbooks
   [ ] ★ GATE →PROD: Amígdala bloquea attack suite + Pilar 3 gate + DR pasa
   [ ] → PRODUCCIÓN
```

---

## Cierre

```
   ╔═══════════════════════════════════════════════════════════════════╗
   ║   ESTE PLAN RESPONDE: ¿EN QUÉ ORDEN SE PROGRAMA FOR3S OS?           ║
   ║                                                                    ║
   ║   6 FASES · foundation-first · MVP pilotable a las ~12-16 semanas  ║
   ║   · sistema completo ~24-36 semanas con paralelización             ║
   ║                                                                    ║
   ║   CAMINO CRÍTICO: R1→R2→R3→R4→R5→R6→R10                            ║
   ║   PARALELIZABLE: R8 (∥R5/R6) · R7 (∥R6) · R9-doc (∥R8)             ║
   ║   CI/CD: Fase 0 (temprano) · governor: ANTES de auto-gen           ║
   ║                                                                    ║
   ║   2 reglas de oro: (1) CI/CD temprano · (2) governor antes del bucle║
   ║                                                                    ║
   ║   ⚠️ Lo que falta para que este plan sea 100% confiable:           ║
   ║   el refuerzo #3 (estimación de tiempo detallada por sub-tema).    ║
   ║   Este plan da el ORDEN (preciso) y el tiempo (estimado).          ║
   ╚═══════════════════════════════════════════════════════════════════╝
```

**Cómo usar este documento:**
- §3 = la secuencia oficial (de los docs).
- §6 = las 6 fases con detalle de qué programar en cada una.
- §7 = el orden EXACTO interno de R6 (la ronda más delicada).
- §8 = qué es MVP vs diferido (evita sobre-engineering).
- §11-§13 = los diagramas: línea de tiempo, árbol de dependencias, mapa de flujo de datos (3 vistas).
- §16 = el checklist maestro para ir marcando el progreso de construcción.

---

**Fin del Plan Maestro de Programación.**

**Próximo refuerzo natural:** #3 — estimación de tiempo detallada por sub-tema (para convertir los `[EST.]` de este plan en números confiables que puedas comprometer a pilots/inversores).
